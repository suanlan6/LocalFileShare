from device import Device
import socket
import json
import threading
import time

join_candidates = []
joined = False
heartbeat_lock = threading.Lock()
heartbeat_started = False
super_ip = None
super_port = None
listener_socket = None
should_stop_listen = False
join_event = threading.Event()
should_abort_join = False
heartbeat_stop_event = threading.Event()
last_ack_time = time.time()
join_triggered = False  # 是否已触发加入流程
first_start=True


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
            print(f"📡 子节点心跳端口绑定成功：{device.host_ip}:{actual_port}")
        except Exception as e:
            print(f"❌ 心跳端口绑定失败: {e}")
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
                        print(f"✅ 收到 HEARTBEAT_ACK ← {addr}")
                except Exception as e:
                    print(f"⚠️ 接收 ACK 出错: {e}")
                    break

        threading.Thread(target=_recv_ack, daemon=True).start()

        # ✅ 心跳发送主循环
        while not heartbeat_stop_event.is_set():
            if joined:
                msg = {
                    "type": "HEARTBEAT",
                    "device_id": device.device_id
                }
                try:
                    sock.sendto(json.dumps(msg).encode("utf-8"), (super_ip, super_port))
                    print(f"❤️‍🔥 已发送 HEARTBEAT → {super_ip}:{super_port}")
                except Exception as e:
                    print(f"❌ HEARTBEAT 发送失败: {e}")
            time.sleep(interval)

        sock.close()

    threading.Thread(target=_heartbeat_thread, daemon=True).start()


def listen_heartbeat_ack(self_device: Device, port_offset=100):
    def _listen():
        global last_ack_time
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self_device.host_ip, self_device.conn_port + port_offset))
        print(f"📡 子节点监听 HEARTBEAT_ACK @ {self_device.host_ip}:{self_device.conn_port + port_offset}")

        while joined:
            try:
                data, addr = sock.recvfrom(1024)
                msg = json.loads(data.decode("utf-8"))
                if msg.get("type") == "HEARTBEAT_ACK":
                    last_ack_time = time.time()
                    print(f"✅ 收到超级节点 ACK ← {addr}")
            except Exception as e:
                print(f"⚠️ ACK 接收异常: {e}")
                break

    threading.Thread(target=_listen, daemon=True).start()

def start_super_node_timeout_checker(self_device: Device, timeout=10):
    def _check():
        while joined:
            if time.time() - last_ack_time > timeout:
                print("🛑 检测到超级节点掉线，启动自救")
                reset_child_node_state()
                from lan_comm import start_hello_broadcast
                start_hello_broadcast(self_device, lambda: not joined)
                listen_super_node(self_device)
                break
            time.sleep(3)

    threading.Thread(target=_check, daemon=True).start()



def stop_heartbeat():
    global heartbeat_started
    heartbeat_stop_event.set()
    heartbeat_started = False
    print("🛑 心跳线程已停止")


def stop_listen_super_node():
    global listener_socket, should_stop_listen
    should_stop_listen = True
    if listener_socket:
        try:
            listener_socket.close()
        except Exception as e:
            print(f"🛑 socket 关闭失败：{e}")
        listener_socket = None
        print("🛑 已关闭子节点监听 socket")



def listen_super_node(self_device: Device, on_join_callback=None, auto_join_callback=None):
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
        print(f"📡 子节点监听中: {self_device.host_ip}:{self_device.conn_port}")

        while not should_stop_listen:
            try:
                conn, addr = sock.accept()
                data = conn.recv(65536).decode('utf-8')
                msg = json.loads(data)
                msg_type = msg.get("type")
                print("msg:     ",msg)
                if msg_type == "NEW_MEMBER":
                    super_info = msg.get("super_node")
                    if super_info:
                        super_info["is_full"] = msg.get("is_full", False)
                        print(f"📥 收到超级节点邀请：{super_info['device_name']}")
                        join_candidates.append(super_info)

                    global join_triggered
                    if not joined and not join_triggered:
                        join_triggered = True
                        threading.Thread(target=delayed_choose_and_join, args=[self_device, on_join_callback]).start()

                elif msg_type == "NEW_MEMBER_SYNC":
                    new_dev = msg.get("new_member")
                    print(f"📥 收到新成员同步：{new_dev['device_name']}")
                elif msg_type == "GLOBAL_VIEW_SYNC":
                    names = msg.get("online_device_names", [])
                    print(f"📡 全局在线设备（{len(names)}）：{', '.join(names)}")

            except socket.timeout:
                continue
            except OSError:
                break
            except Exception as e:
                print(f"⚠️ 子节点监听异常：{e}")
                continue

        print("🛑 子节点监听线程退出")

    thread = threading.Thread(target=_listen, daemon=True)
    thread.start()



def choose_and_join(self_device: Device, on_join_callback):
    global joined, super_ip, super_port, heartbeat_started, join_candidates,join_triggered,last_ack_time, first_start# ✅ 统一声明

    print("join_candidates", len(join_candidates))
    print(join_candidates)

    if joined or not join_candidates:
        join_triggered = False
        return

    for chosen in join_candidates:
        if chosen.get("is_full"):
            print(f"⚠️ 超级节点 {chosen['device_name']} 已满，跳过")
            continue

        payload = {
            "type": "JOIN_CONFIRM",
            "device": self_device.to_dict()
        }

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((chosen["host_ip"], chosen["conn_port"]))
            sock.send(json.dumps(payload).encode('utf-8'))

            ack = sock.recv(65536).decode('utf-8')
            ack_msg = json.loads(ack)
            if ack_msg.get("type") != "JOIN_ACK":
                print(f"❌ 未收到 JOIN_ACK，加入失败")
                sock.close()
                continue

            heartbeat_port = ack_msg.get("heartbeat_port", 9999)
            sock.close()

            super_ip = chosen["host_ip"]
            super_port = heartbeat_port

            print(f"📬 发送 JOIN_CONFIRM → {chosen['host_ip']}:{chosen['conn_port']}")
            print(f"✅ 已选择加入超级节点: {chosen['device_name']}，心跳端口：{heartbeat_port}")

            # ✅ 开启心跳
            start_heartbeat(self_device, chosen["host_ip"], heartbeat_port)
            joined = True
            join_triggered = False

            print("child_node joined:", joined)
            #listen_heartbeat_ack(self_device)
            last_ack_time = time.time()
            start_super_node_timeout_checker(self_device)

            if on_join_callback:
                on_join_callback()
            join_event.set()
            return



        except Exception as e:
            print(f"[JOIN_CONFIRM 失败]：{e}")
            continue

    print("❗️所有超级节点都拒绝或连接失败，提升为超级节点")
    # ✅ 不论成功失败都应设置，表示尝试完成
    join_event.set()
    reset_child_node_state()
    first_start=False
    print("⚠️ 子节点内部：未能加入任何超级节点 → 自动晋升为超级节点")
    time.sleep(0.5)  # 等待 socket 彻底释放
    # ⚠️ 使用新的空闲端口，避免和子节点冲突
    from main import find_free_port
    new_port = find_free_port()
    self_device.conn_port = new_port

    print(f"🔁 分配新端口用于超级节点：{new_port}")
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
    global joined, heartbeat_started, join_candidates, should_abort_join,join_triggered
    from lan_comm import stop_hello_broadcast
    joined = False
    join_triggered = False
    heartbeat_started = False
    should_abort_join = False
    join_candidates.clear()
    join_event.clear()
    stop_hello_broadcast()
    stop_listen_super_node()
    stop_heartbeat()  # ✅ 新增
    print("🧹 已重置子节点状态")




def delayed_choose_and_join(self_device, on_join_callback):
    time.sleep(1.5)  # 模拟原来的 Timer 延时

    if should_abort_join:
        print("⛔ 中断：节点已切换身份，跳过 choose_and_join")
        return

    choose_and_join(self_device, on_join_callback)


def request_global_view(self_device,super_ip, super_port):
    payload = {
        "type": "REQUEST_GLOBAL_VIEW",
        "device_id": self_device.device_id
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((super_ip, super_port))
            s.send(json.dumps(payload).encode("utf-8"))

            response = s.recv(65536).decode("utf-8")
            msg = json.loads(response)

            if msg.get("type") == "GLOBAL_VIEW_SYNC":
                names = msg.get("online_device_names", [])
                print(f"🌐 当前在线设备（{len(names)}）：{', '.join(names)}")
    except Exception as e:
        print(f"❌ 获取视图失败：{e}")

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
            else:
                print("❓ 未知命令")

    threading.Thread(target=_input_loop).start()


