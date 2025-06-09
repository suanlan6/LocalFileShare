import json
import socket

from lan_comm import start_super_node_listener, send_sync_to_child
from device import Device
import time
import threading


class SuperNode:
    def __init__(self, self_device: Device, group_limit=4):
        self.device = self_device
        self.device.is_super_node = True
        self.sub_nodes = {}           # device_id → device_info
        self.group_limit = group_limit
        self.heartbeat_map = {}       # device_id → last_heartbeat_timestamp
        self.peer_super_nodes = {}  # device_id → { super_node, sub_count, group_limit, last_seen }
        # 添加线程锁
        self.lock = threading.Lock()
        # device_id 正在等待确认
        self.pending_invites = set()
        self.pending_invite_times = {}  # device_id → timestamp
        # 对 peer_super_nodes 的读写加锁
        self.peer_lock = threading.Lock()

    def start(self):
        #用于接收 JOIN_CONFIRM
        self._start_tcp_listener()
        # 启动广播监听（接收子节点HELLO和心跳）
        start_super_node_listener(self.handle_incoming_message)
        # 启动心跳掉线检测
        self.start_offline_checker()
        #打印超级节点视图
        self.start_peer_view_printer()
        #监听心跳
        self.heartbeat_port = self.device.conn_port  # 或者单独指定
        self._start_heartbeat_listener()
        #清理过期邀请名额
        self.start_invite_timeout_checker()
        #定期清理离线的超级节点
        self.start_peer_super_node_timeout_checker()


        from lan_comm import broadcast_super_node_hello  # 确保这一行在顶部或局部导入

        # ✅ 启动 SUPERNODE_HELLO 广播
        broadcast_super_node_hello(
            self.device,
            sub_count=lambda: len(self.sub_nodes),
            group_limit=self.group_limit,
            get_sub_info=lambda: [
                {
                    "device_id": dev["device_id"],
                    "device_name": dev["device_name"]
                } for dev in self.sub_nodes.values()
            ],
            interval=10
        )

    def _start_heartbeat_listener(self):
        def _listen():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.device.host_ip, self.heartbeat_port))
            print(f"📡 超级节点监听 UDP 心跳: {self.device.host_ip}:{self.heartbeat_port}")

            while True:
                try:
                    data, addr = sock.recvfrom(65536)
                    print("data",data)
                    print("addr",addr)
                    msg = json.loads(data.decode('utf-8'))

                    if msg.get("type") == "HEARTBEAT":
                        dev_id = msg.get("device_id")
                        self.heartbeat_map[dev_id] = time.time()
                        print(f"💓 收到心跳：{dev_id}")

                        # 回发 ACK
                        ack = {
                            "type": "HEARTBEAT_ACK"
                        }
                        try:
                            sock.sendto(json.dumps(ack).encode("utf-8"), addr)
                            print(f"🔁 已发送 HEARTBEAT_ACK → {addr}")
                        except Exception as e:
                            print(f"❌ 发送 ACK 失败: {e}")

                except Exception as e:
                    print(f"[UDP心跳监听异常] {e}")

        threading.Thread(target=_listen, daemon=True).start()

    def _start_tcp_listener(self):
        def _listen():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.device.host_ip, self.device.conn_port))
            sock.listen(5)
            print(f"🧲 超级节点监听 JOIN_CONFIRM: {self.device.host_ip}:{self.device.conn_port}")

            while True:
                conn, addr = sock.accept()
                data = conn.recv(65536).decode('utf-8')
                try:
                    msg = json.loads(data)
                    if msg.get("type") == "JOIN_CONFIRM":
                        self.confirm_and_add(msg["device"])
                        # ✅ 发送 JOIN_ACK，附带 heartbeat_port
                        response = {
                            "type": "JOIN_ACK",
                            "heartbeat_port": self.device.conn_port  # ✅ 通常就是当前监听的端口
                        }
                        conn.send(json.dumps(response).encode("utf-8"))
                        print(f"✅ 收到 JOIN_CONFIRM：{msg['device']['device_name']} 加入成功")
                    elif msg.get("type") == "REQUEST_GLOBAL_VIEW":
                        device_id = msg.get("device_id")
                        print(f"📨 收到全局视图请求来自：{device_id}")

                        all_devices = {}  # device_id → device_name
                        all_devices[self.device.device_id] = self.device.device_name

                        for dev in self.sub_nodes.values():
                            all_devices[dev["device_id"]] = dev["device_name"]

                        with self.peer_lock:
                            for peer_data in self.peer_super_nodes.values():
                                peer = peer_data["super_node"]
                                all_devices[peer["device_id"]] = peer["device_name"]
                                for name_pair in peer_data.get("sub_info", []):
                                    all_devices[name_pair["device_id"]] = name_pair["device_name"]
                        #print("self.sub_nodes.values():",self.sub_nodes.values())
                        #print("self.peer_super_nodes.values():",self.peer_super_nodes.values())
                        #print("all_devices",all_devices)
                        response = {
                            "type": "GLOBAL_VIEW_SYNC",
                            "timestamp": time.time(),
                            "online_device_names": list(all_devices.values())  # 显示名称，但基于唯一ID避免冲突
                        }

                        conn.send(json.dumps(response).encode("utf-8"))

                except Exception as e:
                    print(f"[JOIN_CONFIRM 解析失败]：{e}")

        threading.Thread(target=_listen, daemon=True).start()

    def handle_incoming_message(self, msg, addr):
        #print(f"📥 [调试] 收到消息 from {addr} → {msg}")
        msg_type = msg.get("type")

        if msg_type == "HELLO":
            self.handle_new_device(msg.get("device"), addr)
        elif msg_type == "SUPERNODE_HELLO":
            #print("msg", msg)
            info = msg.get("super_node")
            peer_id = info.get("device_id")

            if peer_id == self.device.device_id:
                return  # 忽略自己

            sub_count = msg.get("sub_count", 0)
            group_limit = msg.get("group_limit", 0)
            sub_info = msg.get("sub_info", [])  # ✅ 使用结构化子节点信息
            now = time.time()
            with self.peer_lock:
                is_new = peer_id not in self.peer_super_nodes
                self.peer_super_nodes[peer_id] = {
                    "super_node": info,
                    "sub_count": sub_count,
                    "group_limit": group_limit,
                    "sub_info": sub_info,  # ✅ 替代 sub_names
                    "last_seen": now
                }

            if is_new:
                print(f"🛰️ 发现新超级节点：{peer_id}")
            else:
                print(f"🔄 更新超级节点：{peer_id}（子节点 {sub_count}/{group_limit - 1}）")

            # ✅ 可选：打印子节点列表
            names = ", ".join([dev["device_name"] for dev in sub_info])
            print(f"   子节点列表：[{names}]")

        elif msg_type == "JOIN_CONFIRM":
            self.confirm_and_add(msg.get("device"))
            print(f"✅ 子节点加入成功：",msg.get("device"))


    def confirm_and_add(self, dev_info):
        dev_id = dev_info["device_id"]

        with self.lock:
            if dev_id in self.sub_nodes:
                return

            if len(self.sub_nodes) >= self.group_limit - 1:
                print(f"❌ 加入失败（组满）：{dev_info['device_name']}")
                return

            self.sub_nodes[dev_id] = dev_info

            self.heartbeat_map[dev_id] = time.time()
            self.pending_invites.discard(dev_id)  # ✅ 清除挂起状态
            self.pending_invite_times.pop(dev_id, None)
            print(f"✅ 子节点已确认加入：{dev_info['device_name']} ({dev_id})")

        self.sync_new_member_to_children(dev_info)

    def handle_new_device(self, dev_info, addr):
        with self.lock:
            current_pending = len(self.pending_invites)
            current_total = len(self.sub_nodes)
            is_full = (current_total + current_pending) >= self.group_limit - 1

            dev_id = dev_info["device_id"]

            # 如果组满，或者已经发送过邀请，则不再邀请
            if is_full or dev_id in self.pending_invites or dev_id in self.sub_nodes:
                payload = {
                    "type": "NEW_MEMBER",
                    "super_node": self.device.to_dict(),
                    "is_full": True  # 明确表示组满或不能接受
                }
                print(f"❌ 拒绝或忽略加入请求：{dev_id}")
            else:
                self.pending_invites.add(dev_id)
                self.pending_invite_times[dev_id] = time.time()
                payload = {
                    "type": "NEW_MEMBER",
                    "super_node": self.device.to_dict(),
                    "is_full": False
                }
                print(f"📨 当前容量：{len(self.sub_nodes)} 已邀请：{len(self.pending_invites)}")

                print(f"📨 向 {dev_info['device_name']} 发出加入邀请（挂起确认）")

        send_sync_to_child(dev_info["host_ip"], dev_info["conn_port"], payload)

    def sync_new_member_to_children(self, new_dev):
        for child_id, child_info in self.sub_nodes.items():
            payload = {
                "type": "NEW_MEMBER_SYNC",  # ✅ 改为同步类型
                "new_member": new_dev
            }
            send_sync_to_child(child_info["host_ip"], child_info["conn_port"], payload)

    def start_offline_checker(self, interval=10, timeout=12):
        def _check():
            while True:
                now = time.time()
                offline = []

                for dev_id, last_ts in list(self.heartbeat_map.items()):
                    if now - last_ts > timeout:
                        offline.append(dev_id)

                for dev_id in offline:
                    print(f"❌ 子节点掉线：{dev_id}")
                    self.heartbeat_map.pop(dev_id, None)
                    self.sub_nodes.pop(dev_id, None)
                    # 可扩展：通知其他子节点该设备已掉线

                time.sleep(interval)

        threading.Thread(target=_check, daemon=True).start()

    def start_peer_view_printer(self, interval=10):
        def _print():
            while True:
                print("\n🧭 当前所有超级节点视图：")

                # 打印自己
                self_sub_count = len(self.sub_nodes)
                self_names = ", ".join([dev["device_name"] for dev in self.sub_nodes.values()])
                print(f" - [SELF] {self.device.device_name} ({self.device.device_id[:6]}) "
                      f"{self.device.host_ip}:{self.device.conn_port} | "
                      f"子节点：{self_sub_count}/{self.group_limit - 1} | 状态：在线")
                print(f"   子节点列表：[{self_names}]")

                # 打印其他超级节点
                with self.peer_lock:
                    #print("peer_super_nodes:", self.peer_super_nodes)
                    if not self.peer_super_nodes:
                        print("（暂无其他超级节点）")
                    else:
                        now = time.time()
                        for peer_id, data in self.peer_super_nodes.items():
                            dev = data["super_node"]
                            sub_count = data["sub_count"]
                            limit = data["group_limit"]
                            last_seen = now - data["last_seen"]
                            print(f" - [{dev['device_name']}] ({peer_id[:6]}) {dev['host_ip']}:{dev['conn_port']} | "
                                  f"子节点：{sub_count}/{limit - 1} | 上次看到：{last_seen:.1f}s 前")
                            sub_info = data.get("sub_info", [])
                            names = ", ".join(dev["device_name"] for dev in sub_info)
                            print(f"   子节点列表：[{names}]")

                print("-" * 50)
                time.sleep(interval)

        threading.Thread(target=_print, daemon=True).start()

    def start_invite_timeout_checker(self, interval=5, timeout=10):
        def _check():
            while True:
                now = time.time()
                expired = []
                with self.lock:
                    for dev_id, ts in list(self.pending_invite_times.items()):
                        if now - ts > timeout:
                            expired.append(dev_id)

                    for dev_id in expired:
                        self.pending_invites.discard(dev_id)
                        self.pending_invite_times.pop(dev_id, None)
                        print(f"⏳ 清除过期邀请：{dev_id}")

                time.sleep(interval)

        threading.Thread(target=_check, daemon=True).start()

    def start_peer_super_node_timeout_checker(self, interval=10, timeout=20):
        def _check():
            while True:
                now = time.time()
                offline = []
                with self.peer_lock:
                    for peer_id, info in list(self.peer_super_nodes.items()):
                        last_seen = info.get("last_seen", 0)
                        if now - last_seen > timeout:
                            offline.append(peer_id)
                with self.peer_lock:
                    for peer_id in offline:
                        peer_info = self.peer_super_nodes.pop(peer_id)
                        dev = peer_info["super_node"]
                        print(f"🛑 超级节点掉线：{dev['device_name']} ({peer_id})")

                time.sleep(interval)

        threading.Thread(target=_check, daemon=True).start()



