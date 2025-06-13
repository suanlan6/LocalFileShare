from random import randint
import socket
import json
import threading
import time
import queue

from src.common.device import Device
from .super_node import SuperNode
from src.utils.logger import _logger

join_candidates = []
joined = False
heartbeat_lock = threading.Lock()
heartbeat_started = False
input_command_listener_started = False
super_ip = None
super_port = None
listener_socket = None
should_stop_listen = False
join_event = threading.Event()
should_abort_join = False
heartbeat_stop_event = threading.Event()
input_stop_event = threading.Event()
input_queue = queue.Queue()
last_ack_time = time.time()
join_triggered = False  # 是否已触发加入流程
first_start = True
already_super = False


def find_free_port():
    """从系统动态获取一个空闲端口"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def start_heartbeat(device, super_ip, super_port, interval=3):
    global heartbeat_started, last_ack_time
    with heartbeat_lock:
        if heartbeat_started:
            return
        heartbeat_started = True
        heartbeat_stop_event.clear()

    def _heartbeat_thread():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # ✅ 绑定任意空闲端口（自动分配）
            sock.bind((device.host_ip, 0))
            actual_port = sock.getsockname()[1]
            _logger.info(f"📡 子节点心跳端口绑定成功：{device.host_ip}:{actual_port}")
        except Exception as e:
            _logger.error(f"❌ 心跳端口绑定失败: {e}")
            return

        # ✅ 启动 ACK 接收线程
        def _recv_ack():
            global last_ack_time
            while not heartbeat_stop_event.is_set():
                try:
                    data, addr = sock.recvfrom(1024)
                    msg = json.loads(data.decode("utf-8"))
                    if msg.get("type") == "HEARTBEAT_ACK":
                        last_ack_time = time.time()
                        # print(f"✅ 收到 HEARTBEAT_ACK ← {addr}")
                except Exception as e:
                    _logger.error(f"⚠️ 接收 ACK 出错: {e}")
                    break

        threading.Thread(target=_recv_ack, daemon=True).start()

        # ✅ 心跳发送主循环
        while not heartbeat_stop_event.is_set():
            if joined:
                msg = {"type": "HEARTBEAT", "device_id": device.device_id}
                try:
                    sock.sendto(json.dumps(msg).encode("utf-8"), (super_ip, super_port))
                    # print(f"❤️‍🔥 已发送 HEARTBEAT → {super_ip}:{super_port}")
                except Exception as e:
                    _logger.error(f"❌ HEARTBEAT 发送失败: {e}")
            time.sleep(interval)

        sock.close()

    threading.Thread(target=_heartbeat_thread, daemon=True).start()


def listen_heartbeat_ack(self_device: Device, port_offset=100):
    def _listen():
        global last_ack_time
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self_device.host_ip, self_device.conn_port + port_offset))
        _logger.info(
            f"📡 子节点监听 HEARTBEAT_ACK @ {self_device.host_ip}:{self_device.conn_port + port_offset}"
        )

        while joined:
            try:
                data, addr = sock.recvfrom(1024)
                msg = json.loads(data.decode("utf-8"))
                if msg.get("type") == "HEARTBEAT_ACK":
                    last_ack_time = time.time()
                    _logger.info(f"✅ 收到超级节点 ACK ← {addr}")
            except Exception as e:
                _logger.error(f"⚠️ ACK 接收异常: {e}")
                break

    threading.Thread(target=_listen, daemon=True).start()


def start_super_node_timeout_checker(self_device: Device, timeout=10):
    def _check():
        global already_super
        while joined:
            if time.time() - last_ack_time > timeout:
                _logger.info("🛑 检测到超级节点掉线，启动自救")
                reset_child_node_state()
                from lan_comm import start_hello_broadcast

                start_hello_broadcast(self_device, lambda: not joined)
                listen_super_node(self_device)

                wait_time = randint(4, 8)
                _logger.info(f"⏳ 等待加入超级节点（最多 {wait_time}s）...")
                join_event.wait(timeout=wait_time)
                from lan_comm import stop_hello_broadcast

                stop_hello_broadcast()
                time.sleep(2)
                if not joined:
                    if not already_super:
                        already_super = True
                        reset_child_node_state()
                        time.sleep(0.5)

                        # 初始化
                        new_port = find_free_port()
                        self_device.conn_port = new_port
                        self_device.is_super_node = True
                        self_device.super_node_id = self_device.device_id
                        self_device.super_ip = self_device.host_ip
                        self_device.super_port = self_device.conn_port

                        _logger.info(self_device.to_dict())
                        super_node = SuperNode(self_device)
                        super_node.start()
                else:
                    _logger.info(self_device.to_dict())
                    # 缓兵之计 后面还是要想办法中断重复的线程
                    input_stop_event.clear()
                    # start_input_command_listener(self_device)

                break
            time.sleep(3)

    threading.Thread(target=_check, daemon=True).start()


def listen_super_node(
    self_device: Device, on_join_callback=None, auto_join_callback=None
):
    global listener_socket, should_stop_listen
    should_stop_listen = False

    def _listen():
        global listener_socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self_device.host_ip, self_device.conn_port))
        sock.listen(5)
        sock.settimeout(1.0)  # ⏳ 每秒检查是否退出
        listener_socket = sock
        _logger.info(f"📡 子节点监听中: {self_device.host_ip}:{self_device.conn_port}")

        while not should_stop_listen:
            try:
                conn, addr = sock.accept()
                data = conn.recv(65536).decode("utf-8")
                msg = json.loads(data)
                msg_type = msg.get("type")
                # print("msg:     ",msg)
                if msg_type == "NEW_MEMBER":
                    super_info = msg.get("super_node")
                    if super_info:
                        super_info["is_full"] = msg.get("is_full", False)
                        _logger.info(
                            f"📥 收到超级节点邀请：{super_info['device_name']}"
                        )
                        join_candidates.append(super_info)

                    global join_triggered
                    if not joined and not join_triggered:
                        join_triggered = True
                        threading.Thread(
                            target=delayed_choose_and_join,
                            args=[self_device, on_join_callback],
                        ).start()

                elif msg_type == "NEW_MEMBER_SYNC":
                    new_dev = msg.get("new_member")
                    _logger.info(f"📥 收到新成员同步：{new_dev['device_name']}")
                elif msg_type == "GLOBAL_VIEW_SYNC":
                    names = msg.get("online_device_names", [])
                    _logger.info(f"📡 全局在线设备（{len(names)}）：{', '.join(names)}")

            except socket.timeout:
                continue
            except OSError:
                break
            except Exception as e:
                _logger.error(f"⚠️ 子节点监听异常：{e}")
                continue

        _logger.info("🛑 子节点监听线程退出")

    thread = threading.Thread(target=_listen, daemon=True)
    thread.start()


def choose_and_join(self_device: Device, on_join_callback):
    global joined, super_ip, super_port, heartbeat_started, join_candidates, join_triggered, last_ack_time, first_start, already_super  # ✅ 统一声明

    # print("join_candidates", len(join_candidates))
    # print(join_candidates)

    if joined or not join_candidates:
        join_triggered = False
        return

    for chosen in join_candidates:
        if chosen.get("is_full"):
            _logger.info(f"⚠️ 超级节点 {chosen['device_name']} 已满，跳过")
            continue

        payload = {"type": "JOIN_CONFIRM", "device": self_device.to_dict()}

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((chosen["host_ip"], chosen["conn_port"]))
            sock.send(json.dumps(payload).encode("utf-8"))

            ack = sock.recv(65536).decode("utf-8")
            ack_msg = json.loads(ack)
            if ack_msg.get("type") != "JOIN_ACK":
                _logger.info(f"❌ 未收到 JOIN_ACK，加入失败")
                sock.close()
                continue

            heartbeat_port = ack_msg.get("heartbeat_port", 9999)
            sock.close()

            super_ip = chosen["host_ip"]
            self_device.super_ip = chosen["host_ip"]
            super_port = heartbeat_port
            self_device.super_port = heartbeat_port

            _logger.info(
                f"📬 发送 JOIN_CONFIRM → {chosen['host_ip']}:{chosen['conn_port']}"
            )
            _logger.info(
                f"✅ 已选择加入超级节点: {chosen['device_name']}，心跳端口：{heartbeat_port}"
            )

            # 向子节点发送自己的所有设备信息

            # 初始化子节点信息
            self_device.is_super_node = False
            # self_device.group_id = chosen["group_id"]
            self_device.super_node_id = chosen["device_id"]

            # ✅ 开启心跳
            start_heartbeat(self_device, chosen["host_ip"], heartbeat_port)
            joined = True
            join_triggered = False

            _logger.info("child_node joined:", joined)
            # listen_heartbeat_ack(self_device)
            last_ack_time = time.time()
            start_super_node_timeout_checker(self_device)

            if on_join_callback:
                on_join_callback()
            join_event.set()
            return

        except Exception as e:
            _logger.error(f"[JOIN_CONFIRM 失败]：{e}")
            continue

    _logger.warning("❗️所有超级节点都拒绝或连接失败，提升为超级节点")
    # ✅ 不论成功失败都应设置，表示尝试完成
    join_event.set()
    reset_child_node_state()
    first_start = False
    already_super = True
    _logger.warning("⚠️ 子节点内部：未能加入任何超级节点 → 自动晋升为超级节点")
    time.sleep(randint(1, 5))  # 等待 socket 彻底释放
    # ⚠️ 使用新的空闲端口，避免和子节点冲突
    from device_start import find_free_port

    new_port = find_free_port()
    self_device.conn_port = new_port
    _logger.info(f"🔁 分配新端口用于超级节点：{new_port}")

    self_device.is_super_node = True
    self_device.super_ip = self_device.host_ip
    self_device.super_port = self_device.conn_port
    self_device.super_node_id = self_device.device_id
    _logger.info(f"📦 自身设备信息：{self_device.to_dict()}")

    from super_node import SuperNode

    super_node = SuperNode(self_device)
    super_node.start()

    """
    from lan_comm import stop_hello_broadcast
    stop_listen_super_node()
    stop_hello_broadcast()
    joined = False
    heartbeat_started = False
    join_candidates.clear()
    time.sleep(0.5)  # 等待 socket 彻底释放
    from super_node import SuperNode
    from main import find_free_port
    new_port = find_free_port()
    self_device.conn_port = new_port
    super_node = SuperNode(self_device)
    print(super_node)
    super_node.start()
    """


def reset_child_node_state():
    global joined, heartbeat_started, join_candidates, should_abort_join, join_triggered, input_command_listener_started
    from .lan_comm import stop_hello_broadcast

    joined = False
    join_triggered = False
    heartbeat_started = False
    input_command_listener_started = False
    should_abort_join = False
    join_candidates.clear()
    join_event.clear()
    stop_hello_broadcast()
    stop_listen_super_node()
    stop_heartbeat()
    input_stop_event.set()

    _logger.info("🧹 已重置子节点状态")


def delayed_choose_and_join(self_device, on_join_callback):
    time.sleep(1.5)  # 模拟原来的 Timer 延时

    if should_abort_join:
        _logger.info("⛔ 中断：节点已切换身份，跳过 choose_and_join")
        return

    choose_and_join(self_device, on_join_callback)


def request_global_view(self_device, super_ip, super_port):
    payload = {"type": "REQUEST_GLOBAL_VIEW", "device_id": self_device.device_id}

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((super_ip, super_port))
            s.send(json.dumps(payload).encode("utf-8"))

            response = s.recv(65536).decode("utf-8")
            msg = json.loads(response)

            if msg.get("type") == "GLOBAL_VIEW_SYNC":
                device_info_map = msg.get("online_device_info", {})  # 新字段

                _logger.info(f"🌐 当前在线设备总数：{len(device_info_map)}")
                for dev_id, dev_info in device_info_map.items():
                    _logger.info(f"\n🆔 设备ID: {dev_id}")
                    _logger.info(
                        f"📦 设备信息: {json.dumps(dev_info, indent=2, ensure_ascii=False)}"
                    )

    except Exception as e:
        _logger.error(f"❌ 获取视图失败：{e}")


def request_one_device_info(self_device, super_ip, super_port, target_device_name):
    payload = {
        "type": "REQUEST_ONE_DEVICE_INFO",
        "device_id": self_device.device_id,
        "target_device_name": target_device_name,
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((super_ip, super_port))
            s.send(json.dumps(payload).encode("utf-8"))

            response = s.recv(65536).decode("utf-8")
            msg = json.loads(response)

            if msg.get("type") == "TARGET_DEVICE_SYNC":
                if msg.get("is_find") == True:
                    _logger.info(f"🌐 该设备信息")
                    _logger.info(msg.get("target_device_info"))

                else:
                    _logger.info("未找到该设备")
    except Exception as e:
        _logger.error(f"❌ 获取目标设备信息失败：{e}")


import threading
import queue
import time

# 控制输入监听线程的停止标志
input_stop_event = threading.Event()
input_queue = queue.Queue()


def input_reader():
    """专门读取用户输入，并放入队列中"""
    while not input_stop_event.is_set():
        try:
            time.sleep(0.5)
            line = input("💡 输入 view 获取当前在线设备列表: ")
            input_queue.put(line.strip().lower())
        except EOFError:
            break


def start_input_command_listener(self_device):

    def _input_loop():
        while not input_stop_event.is_set():
            try:
                cmd = input_queue.get(timeout=0.5)  # 非阻塞，带超时
            except queue.Empty:
                continue  # 没有输入，继续轮询

            if cmd == "view":
                _logger.info("输入指令正确")
                if joined and super_ip and super_port:
                    _logger.info("正在请求全局视图")
                    request_global_view(self_device, super_ip, super_port)
                else:
                    _logger.warning("⚠️ 未连接超级节点，无法获取视图。")
            else:
                _logger.warning("❓ 未知命令")
            """
            elif cmd == "find":
                print("输入指令正确，接下来输入要寻找的设备名：")
                try:
                    name = input("请输入设备名: ").strip()
                except EOFError:
                    break
                print(f"您的输入为 {name}")
                if joined and super_ip and super_port:
                    print(f"正在请求 {name} 设备信息")
                    request_one_device_info(self_device, super_ip, super_port, name)
                else:
                    print("⚠️ 未连接超级节点，无法获取视图。")
            """

    # 启动两个线程：一个是输入读取器，一个是命令处理器
    threading.Thread(target=input_reader, daemon=True).start()
    threading.Thread(target=_input_loop, daemon=True).start()


""""
def start_input_command_listener(self_device):

    def _input_loop():
        while True:

            cmd = input("💡 输入 view 获取当前在线设备列表: ").strip().lower()
            if cmd == "view":
                print("输入指令正确")
                if joined and super_ip and super_port:
                    print("正在请求全局视图")
                    print("self_device",self_device, "super_ip",super_ip, "super_port",super_port)
                    request_global_view(self_device, super_ip, super_port)
                else:
                    print("⚠️ 未连接超级节点，无法获取视图。")

            elif cmd =="find":
                print("输入指令正确，接下来输入要寻找的设备名： ")
                name=input().strip()
                print(f"您的输入为{name}")
                if joined and super_ip and super_port:
                    print(f"正在请求 {name} 设备信息")
                    request_one_device_info(self_device, super_ip, super_port, name)

                else:
                    print("⚠️ 未连接超级节点，无法获取视图。")

            else:
                print("❓ 未知命令")

        #print("input线程已停止")

    threading.Thread(target=_input_loop, daemon=True).start()
"""


def stop_heartbeat():
    global heartbeat_started
    heartbeat_stop_event.set()
    heartbeat_started = False
    _logger.info("🛑 心跳线程已停止")


def stop_listen_super_node():
    global listener_socket, should_stop_listen
    should_stop_listen = True
    if listener_socket:
        try:
            listener_socket.close()
        except Exception as e:
            _logger.error(f"🛑 socket 关闭失败：{e}")
        listener_socket = None
        _logger.info("🛑 已关闭子节点监听 socket")
