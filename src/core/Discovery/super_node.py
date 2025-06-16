import json
import socket

import time
import threading

from src.common.device import Device
from .lan_comm import start_super_node_listener, send_sync_to_child
from src.utils.logger import _logger


class SuperNode:
    def __init__(self, self_device: Device, group_limit=4):
        self.device = self_device
        self.device.is_super_node = True
        self.sub_nodes = {}  # device_id → device_info
        # self.all_nodes = {}           # device_id → device_info
        self.group_limit = group_limit
        self.heartbeat_map = {}  # device_id → last_heartbeat_timestamp
        self.peer_super_nodes = (
            {}
        )  # device_id → { super_node, sub_count, group_limit, last_seen }
        # 添加线程锁
        self.lock = threading.Lock()
        # device_id 正在等待确认
        self.pending_invites = set()
        self.pending_invite_times = {}  # device_id → timestamp
        # 对 peer_super_nodes 的读写加锁
        self.peer_lock = threading.Lock()

        self_device.super_node_ref = self  # 在 SuperNode.__init__ 中添加

    def start(self):
        # 用于接收 JOIN_CONFIRM
        self._start_tcp_listener()
        # 启动广播监听（接收子节点HELLO和心跳）
        start_super_node_listener(self.handle_incoming_message)
        # 启动心跳掉线检测
        self.start_offline_checker()
        # 打印超级节点视图
        self.start_peer_view_printer()
        # 监听心跳
        self.heartbeat_port = self.device.discovery_port  # 或者单独指定
        self._start_heartbeat_listener()
        # 清理过期邀请名额
        self.start_invite_timeout_checker()
        # 定期清理离线的超级节点
        self.start_peer_super_node_timeout_checker()

        # 把自己加入self.all_nodes
        # print("self.device")
        # print(self.device)
        # print(Device)
        # self.all_nodes[self.device.device_id] = self.device.to_dict()
        # print("all_nodes")
        # print(self.all_nodes)

        from .lan_comm import broadcast_super_node_hello  # 确保这一行在顶部或局部导入

        # ✅ 启动 SUPERNODE_HELLO 广播
        broadcast_super_node_hello(
            self.device,
            sub_count=lambda: len(self.sub_nodes),
            group_limit=self.group_limit,
            get_sub_info=lambda: list(self.sub_nodes.values()),
            interval=10,
        )

    def _start_heartbeat_listener(self):
        def _listen():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.device.host_ip, self.heartbeat_port))
            _logger.info(
                f"📡 超级节点监听 UDP 心跳: {self.device.host_ip}:{self.heartbeat_port}"
            )

            while True:
                try:
                    data, addr = sock.recvfrom(65536)
                    # print("data",data)
                    # print("addr",addr)
                    msg = json.loads(data.decode("utf-8"))

                    if msg.get("type") == "HEARTBEAT":
                        dev_id = msg.get("device_id")
                        self.heartbeat_map[dev_id] = time.time()
                        # print(f"💓 收到心跳：{dev_id}")

                        # 回发 ACK
                        ack = {"type": "HEARTBEAT_ACK"}
                        try:
                            sock.sendto(json.dumps(ack).encode("utf-8"), addr)
                            # print(f"🔁 已发送 HEARTBEAT_ACK → {addr}")
                        except Exception as e:
                            _logger.error(f"❌ 发送 ACK 失败: {e}")

                except Exception as e:
                    _logger.error(f"[UDP心跳监听异常] {e}")

        threading.Thread(target=_listen, daemon=True).start()

    def _start_tcp_listener(self):
        def _listen():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.device.host_ip, self.device.discovery_port))
            sock.listen(5)
            _logger.info(
                f"🧲 超级节点监听 JOIN_CONFIRM: {self.device.host_ip}:{self.device.discovery_port}"
            )

            while True:
                conn, addr = sock.accept()
                data = conn.recv(65536).decode("utf-8")
                try:
                    msg = json.loads(data)
                    if msg.get("type") == "JOIN_CONFIRM":
                        # print("JOIN_CONFIRM处理1111111111")
                        self.confirm_and_add(msg["device"])
                        # ✅ 发送 JOIN_ACK，附带 heartbeat_port
                        response = {
                            "type": "JOIN_ACK",
                            "heartbeat_port": self.device.discovery_port,  # ✅ 通常就是当前监听的端口
                        }
                        conn.send(json.dumps(response).encode("utf-8"))
                        _logger.info(
                            f"✅ 收到 JOIN_CONFIRM：{msg['device']['device_name']} 加入成功"
                        )
                    elif msg.get("type") == "REQUEST_GLOBAL_VIEW":
                        device_id = msg.get("device_id")
                        _logger.info(f"📨 收到全局视图请求来自：{device_id}")

                        all_devices = {}  # device_id → device_name

                        # 添加自身超级节点的信息
                        all_devices[self.device.device_id] = self.device.to_dict()

                        # 添加本地子节点的信息
                        with self.lock:
                            for dev in self.sub_nodes.values():
                                all_devices[dev["device_id"]] = dev

                        # 添加其他超级节点及其子节点的信息
                        with self.peer_lock:
                            for peer_data in self.peer_super_nodes.values():
                                peer = peer_data["super_node"]
                                all_devices[peer["device_id"]] = peer
                                for dev in peer_data.get("sub_info", []):
                                    all_devices[dev["device_id"]] = dev
                        # print("self.sub_nodes.values():",self.sub_nodes.values())
                        # print("self.peer_super_nodes.values():",self.peer_super_nodes.values())
                        # print("all_devices",all_devices)
                        response = {
                            "type": "GLOBAL_VIEW_SYNC",
                            "timestamp": time.time(),
                            "online_device_info": all_devices,  # 设备ID → 完整信息
                        }

                        conn.send(json.dumps(response).encode("utf-8"))
                    """
                    elif msg.get("type") == "REQUEST_ONE_DEVICE_INFO":
                        device_id = msg.get("device_id")
                        target_device_name = msg.get("target_device_name")
                        print(f"📨 收到的请求来自：{device_id}")
                        print(f"📨 要请求的目标是：{target_device_name}")
                        #定义字典用于存放目标设备的所有信息
                        target_device_info = {
                            "device_name": target_device_name,
                            "is_super_node": False,
                            "super_node_name": None
                        }
                        # 先检查目标设备名是否是当前超级节点的设备名
                        if self.device.device_name == target_device_name:
                            target_device_info["is_super_node"] = True
                            target_device_info["super_node_name"] = self.device.device_name
                            print(f"📡 找到设备 {target_device_name}，设备ID: {self.device.device_id}")

                        # 查找当前超级节点下的子节点
                        for dev in self.sub_nodes.values():
                            if dev["device_name"] == target_device_name:
                                target_device_info["is_super_node"] = False
                                target_device_info["super_node_name"] = self.device.device_name
                                print(f"📡 找到设备 {target_device_name}，设备ID: {dev['device_id']}")
                                break
                        # 查找对等超级节点下的设备
                        with self.peer_lock:
                            for peer_data in self.peer_super_nodes.values():
                                peer = peer_data["super_node"]

                                # 先检查对等超级节点本身
                                if peer["device_name"] == target_device_name:
                                    target_device_info["is_super_node"] = True
                                    target_device_info["super_node_name"] = peer["device_name"]
                                    print(f"📡 找到设备 {target_device_name}，设备ID: {peer['device_id']}")
                                    break
                                else:
                                    # 如果设备在该对等超级节点的子节点中
                                    for name_pair in peer_data.get("sub_info", []):
                                        if name_pair["device_name"] == target_device_name:
                                            target_device_info["is_super_node"] = False
                                            target_device_info["super_node_name"] = peer["device_name"]
                                            print(f"📡 找到设备 {target_device_name}，设备ID: {name_pair['device_id']}")
                                            break
                        if target_device_info["super_node_name"] == None:
                            print("没找到")
                            response = {
                                "type": "TARGET_DEVICE_SYNC",
                                "is_find": False,
                                "target_device_info": target_device_info

                            }
                        else:
                            response = {
                                "type": "TARGET_DEVICE_SYNC",
                                "is_find": True,
                                "target_device_info": target_device_info
                            }

                        conn.send(json.dumps(response).encode("utf-8"))
                    """
                except Exception as e:
                    _logger.error(f"[JOIN_CONFIRM 解析失败]：{e}")

        threading.Thread(target=_listen, daemon=True).start()

    def handle_incoming_message(self, msg, addr):
        # print(f"📥 [调试] 收到消息 from {addr} → {msg}")
        msg_type = msg.get("type")

        if msg_type == "HELLO":
            self.handle_new_device(msg.get("device"), addr)
        elif msg_type == "SUPERNODE_HELLO":
            # print("msg", msg)
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
                    "last_seen": now,
                }
                # print("self.peer_super_nodes[peer_id]")
                # print(self.peer_super_nodes[peer_id])

            # if is_new:
            # print(f"🛰️ 发现新超级节点：{peer_id}")
            # else:
            # print(f"🔄 更新超级节点：{peer_id}（子节点 {sub_count}/{group_limit - 1}）")

            # ✅ 可选：打印子节点列表
            # names = ", ".join([dev["device_name"] for dev in sub_info])
            # print(f"   子节点列表：[{names}]")
        """
        elif msg_type == "JOIN_CONFIRM":
            print("JOIN_CONFIRM处理2222222222")
            self.confirm_and_add(msg.get("device"))
            print(f"✅ 子节点加入成功：",msg.get("device"))
        """

    def confirm_and_add(self, dev_info):
        dev_id = dev_info["device_id"]

        with self.lock:
            if dev_id in self.sub_nodes:
                return

            if len(self.sub_nodes) >= self.group_limit - 1:
                _logger.error(f"❌ 加入失败（组满）：{dev_info['device_name']}")
                return

            # 将当前超级节点的 IP 和端口写入子节点的设备信息
            dev_info["super_node_id"] = self.device.device_id
            dev_info["super_ip"] = self.device.host_ip
            dev_info["super_port"] = self.device.discovery_port

            _logger.info("加入进来的子节点设备信息")
            _logger.info(dev_info)
            self.sub_nodes[dev_id] = dev_info
            # self.all_nodes[dev_id] = dev_info
            # print("all_nodes")
            # print(self.all_nodes)

            self.heartbeat_map[dev_id] = time.time()
            self.pending_invites.discard(dev_id)  # ✅ 清除挂起状态
            self.pending_invite_times.pop(dev_id, None)
            _logger.info(f"✅ 子节点已确认加入：{dev_info['device_name']} ({dev_id})")

        # self.sync_new_member_to_children(dev_info)

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
                    "is_full": True,  # 明确表示组满或不能接受
                }
                _logger.info(f"❌ 拒绝或忽略加入请求：{dev_id}")
            else:
                self.pending_invites.add(dev_id)
                self.pending_invite_times[dev_id] = time.time()
                payload = {
                    "type": "NEW_MEMBER",
                    "super_node": self.device.to_dict(),
                    "is_full": False,
                }
                _logger.info(
                    f"📨 当前容量：{len(self.sub_nodes)} 已邀请：{len(self.pending_invites)}"
                )

                _logger.info(
                    f"📨 {self.device.device_name} 向 {dev_info['device_name']} 发出加入邀请（挂起确认）"
                )

                _logger.info(
                    f"📡 发送邀请到子节点：{dev_info['device_name']} ({dev_info['discovery_port']})"
                )

        send_sync_to_child(dev_info["host_ip"], dev_info["discovery_port"], payload)

    """
    def sync_new_member_to_children(self, new_dev):
        for child_id, child_info in self.sub_nodes.items():
            payload = {
                "type": "NEW_MEMBER_SYNC",  # ✅ 改为同步类型
                "new_member": new_dev
            }
            send_sync_to_child(child_info["host_ip"], child_info["conn_port"], payload)
    """

    def start_offline_checker(self, interval=10, timeout=12):
        def _check():
            while True:
                now = time.time()
                offline = []

                for dev_id, last_ts in list(self.heartbeat_map.items()):
                    if now - last_ts > timeout:
                        offline.append(dev_id)

                for dev_id in offline:
                    _logger.info(f"❌ 子节点掉线：{dev_id}")
                    self.heartbeat_map.pop(dev_id, None)
                    self.sub_nodes.pop(dev_id, None)
                    # self.all_nodes.pop(dev_id, None)
                    # print("all_nodes")
                    # print(self.all_nodes)
                    # 可扩展：通知其他子节点该设备已掉线

                time.sleep(interval)

        threading.Thread(target=_check, daemon=True).start()

    def start_peer_view_printer(self, interval=10):
        def _print():
            while True:

                _logger.info("\n🧭 当前所有超级节点视图：")

                # 打印自己
                self_sub_count = len(self.sub_nodes)
                self_names = ", ".join(
                    [dev["device_name"] for dev in self.sub_nodes.values()]
                )
                _logger.info(
                    f" - [SELF] {self.device.device_name} ({self.device.device_id[:6]}) "
                    f"{self.device.host_ip}:{self.device.discovery_port} | "
                    f"子节点：{self_sub_count}/{self.group_limit - 1} | 状态：在线"
                )
                _logger.info(f"   子节点列表：[{self_names}]")

                # 打印其他超级节点
                with self.peer_lock:
                    # print("peer_super_nodes:", self.peer_super_nodes)
                    if not self.peer_super_nodes:
                        _logger.info("（暂无其他超级节点）")
                    else:
                        now = time.time()
                        for peer_id, data in self.peer_super_nodes.items():
                            dev = data["super_node"]
                            sub_count = data["sub_count"]
                            limit = data["group_limit"]
                            last_seen = now - data["last_seen"]
                            _logger.info(
                                f" - [{dev['device_name']}] ({peer_id[:6]}) {dev['host_ip']}:{dev['discovery_port']} | "
                                f"子节点：{sub_count}/{limit - 1} | 上次看到：{last_seen:.1f}s 前"
                            )
                            sub_info = data.get("sub_info", [])
                            names = ", ".join(dev["device_name"] for dev in sub_info)
                            _logger.info(f"   子节点列表：[{names}]")

                _logger.info("-" * 50)
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
                        _logger.info(f"⏳ 清除过期邀请：{dev_id}")

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
                        _logger.info(
                            f"🛑 超级节点掉线：{dev['device_name']} ({peer_id})"
                        )

                time.sleep(interval)

        threading.Thread(target=_check, daemon=True).start()

    def collect_all_device_info(self):
        """
        动态汇总所有设备的完整信息（不依赖 self.all_nodes）。
        返回值格式: {device_id: device_info}
        """
        all_devices = {}

        # 添加自身超级节点的信息
        all_devices[self.device.device_id] = self.device.to_dict()

        # 添加本地子节点信息
        with self.lock:
            for dev in self.sub_nodes.values():
                all_devices[dev["device_id"]] = dev

        # 添加其他超级节点及其子节点信息
        with self.peer_lock:
            for peer_data in self.peer_super_nodes.values():
                peer = peer_data["super_node"]
                all_devices[peer["device_id"]] = peer

                for dev in peer_data.get("sub_info", []):
                    all_devices[dev["device_id"]] = dev

        return all_devices
