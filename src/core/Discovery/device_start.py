import time
import uuid
from random import randint
import json
import socket
import threading

import src.core.Discovery.child_node as child_node
from .lan_comm import start_hello_broadcast, stop_hello_broadcast
from .super_node import SuperNode
from src.utils.logger import _logger

# def get_devices():
#   devices = get_all_device_info(self_device)


def get_all_device_info(self_device):
    """
    所有节点统一使用的设备视图获取函数。
    仅传入 self_device，内部自动判断节点类型执行相应逻辑。
    返回格式: {device_id: device_info}
    """

    # 如果是超级节点，从实例中调用收集函数
    if getattr(self_device, "is_super_node", False):
        if not hasattr(self_device, "super_node_ref"):
            raise ValueError(
                "⚠️ 当前为超级节点，但未绑定 super_node 实例（super_node_ref）"
            )
        return self_device.super_node_ref.collect_all_device_info()

    # 否则为子节点，从 self_device 中提取连接超级节点所需信息
    super_ip = getattr(self_device, "super_ip", None)
    super_port = getattr(self_device, "super_port", None)

    if not super_ip or not super_port:
        raise ValueError("⚠️ 当前为子节点，但未设置 super_ip 或 super_port")

    # 发起请求
    payload = {"type": "REQUEST_GLOBAL_VIEW", "device_id": self_device.device_id}

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((super_ip, super_port))
            s.send(json.dumps(payload).encode("utf-8"))
            response = s.recv(65536).decode("utf-8")
            msg = json.loads(response)

            if msg.get("type") == "GLOBAL_VIEW_SYNC":
                return msg.get("online_device_info", {})
            else:
                _logger.warning("⚠️ 未收到正确格式的视图响应")
                return {}

    except Exception as e:
        _logger.error(f"❌ 获取视图失败: {e}")
        return {}


def generate_unique_name(prefix="Node"):
    return f"{prefix}-{uuid.uuid4().hex[:6]}"  # 例如 Node-a1b2c3


def find_free_port():
    """从系统动态获取一个空闲端口"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def node_start(
    device, ready_event: threading.Event, stop_event: threading.Event = None
):
    # 分配空闲端口并创建本机设备对象
    port = find_free_port()
    # device_name = generate_unique_name()
    # device = Device(device_name=device.device_name, conn_port=port)
    device.conn_port = port

    _logger.info(
        f"🚀 启动设备：{device.device_name} @ {device.host_ip}:{device.conn_port}"
    )

    # Step 1: 启动广播 & 子节点监听
    start_hello_broadcast(device, lambda: not child_node.joined)
    child_node.listen_super_node(device)

    # Step 2: 等待加入超级节点
    wait_time = randint(4, 8)
    _logger.info(f"⏳ 等待加入超级节点（最多 {wait_time}s）...")
    child_node.join_event.wait(timeout=wait_time)
    stop_hello_broadcast()
    # 等待之前的hello流程走完
    time.sleep(2)

    # print("main joined:", child_node.joined)
    if not child_node.joined:
        if child_node.first_start:
            child_node.reset_child_node_state()  # ✅ 清理子节点所有线程与状态
            _logger.info("⚠️ main函数外部：未能加入任何超级节点 → 自动晋升为超级节点")
            time.sleep(0.5)  # 等待 socket 彻底释放

            # ⚠️ 使用新的空闲端口，避免和子节点冲突
            new_port = find_free_port()
            device.conn_port = new_port

            # 初始化超级节点信息
            device.is_super_node = True
            device.super_node_id = device.device_id
            device.super_ip = device.host_ip
            device.super_port = device.conn_port
            device.device_type = device.device_type

            _logger.info(f"🔁 分配新端口用于超级节点：{new_port}")
            _logger.info(f"📦 自身设备信息：{device.to_dict()}")
            super_node = SuperNode(device)
            super_node.start()

    else:
        # Step 4: 成功加入 → 开启子节点输入命令监听
        _logger.info("✅ 成功加入某个超级节点，继续作为子节点运行")
        _logger.info(device.to_dict())
        # child_node.start_input_command_listener(device)
    """
    try:
        while not True:
            time.sleep(15)
            print("\n🛰️ [定时获取全网设备信息]")

            device_map = get_all_device_info(device)
            print(f"✅ 当前在线设备总数：{len(device_map)}")

            for dev_id, dev_info in device_map.items():
                print(f"\n🆔 设备ID: {dev_id}")
                print(f"📦 设备信息: {json.dumps(dev_info, indent=2, ensure_ascii=False)}")
    """
    ready_event.set()  # 通知share_manager已准备就绪
    try:
        while stop_event is None or not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        _logger.info("\n🛑 程序已退出")
