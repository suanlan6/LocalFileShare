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



def start_heartbeat(device, super_ip, super_port, interval=5):
    global heartbeat_started
    with heartbeat_lock:
        if heartbeat_started:
            return
        heartbeat_started = True
    def _send():
        while True:
            if joined:
                msg = {
                    "type": "HEARTBEAT",
                    "device_id": device.device_id
                }
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                        s.sendto(json.dumps(msg).encode("utf-8"), (super_ip, super_port))
                        print(f"❤️‍🔥 发送心跳成功")
                except Exception as e:
                    print(f"❤️‍🔥 发送心跳失败: {e}")
            time.sleep(interval)

    threading.Thread(target=_send, daemon=True).start()

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

                    if not joined:
                        threading.Timer(1.5, choose_and_join, args=[self_device, on_join_callback]).start()

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
    print("join_candidates", len(join_candidates))
    print(join_candidates)
    global joined, super_ip, super_port
    if joined or not join_candidates:
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
            print("child_node joined:",joined)

            if on_join_callback:
                on_join_callback()
            return

        except Exception as e:
            print(f"[JOIN_CONFIRM 失败]：{e}")
            continue

    print("❗️所有超级节点都拒绝或连接失败，提升为超级节点")
    from lan_comm import stop_hello_broadcast
    stop_hello_broadcast()
    from super_node import SuperNode
    stop_listen_super_node()
    super_node = SuperNode(self_device)
    super_node.start()




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


