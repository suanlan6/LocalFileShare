import socket
import json
import threading
import time

from src.utils.system_utils import get_broadcast_ip
from src.utils.logger import _logger

BROADCAST_PORT = 9999
BROADCAST_ADDR = get_broadcast_ip()
ENCODING = "utf-8"
# 添加状态控制变量
_hello_broadcast_should_stop = False
_hello_broadcast_thread = None


def start_hello_broadcast(device, should_continue, interval=5):
    """
    启动子节点的HELLO广播线程，当 should_continue() 返回 True 且未被外部强制停止时持续广播
    """
    global _hello_broadcast_should_stop, _hello_broadcast_thread
    _hello_broadcast_should_stop = False

    def _broadcast():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while should_continue() and not _hello_broadcast_should_stop:
            payload = {"type": "HELLO", "device": device.to_dict()}
            data = json.dumps(payload).encode(ENCODING)
            sock.sendto(data, (BROADCAST_ADDR, BROADCAST_PORT))
            _logger.info(f"📡 广播 HELLO：{device.device_name}")
            time.sleep(interval)

        sock.close()
        _logger.info(
            f"🛑 停止子节点{device.device_name} HELLO 广播, 原因: should_stop: {_hello_broadcast_should_stop}, should_coutinue: {should_continue()}"
        )

    _hello_broadcast_thread = threading.Thread(target=_broadcast, daemon=True)
    _hello_broadcast_thread.start()


def stop_hello_broadcast():
    global _hello_broadcast_should_stop
    _hello_broadcast_should_stop = True


def start_super_node_listener(on_msg):
    def _listen():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", BROADCAST_PORT))
        _logger.info(f"📡 超级节点监听 UDP 已启动 (port {BROADCAST_PORT})")

        while True:
            try:
                data, addr = sock.recvfrom(65536)
                msg = json.loads(data.decode(ENCODING))
                on_msg(msg, addr)
            except Exception as e:
                _logger.error(f"[UDP监听错误] {e}")

    threading.Thread(target=_listen, daemon=True).start()


def send_sync_to_child(child_ip, child_port, sync_payload):
    """
    超级节点通过 TCP 向子节点推送同步信息（如 NEW_MEMBER）
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((child_ip, child_port))
            sock.send(json.dumps(sync_payload).encode(ENCODING))
    except Exception as e:
        _logger.error(f"[同步失败] → {child_ip}:{child_port} ：{e}")


def broadcast_super_node_hello(
    super_device, sub_count, group_limit, get_sub_info, interval=10
):

    def _broadcast():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            payload = {
                "type": "SUPERNODE_HELLO",
                "super_node": super_device.to_dict(),
                "sub_count": sub_count(),
                "group_limit": group_limit,
                "sub_info": get_sub_info(),  # 用结构化数据替换 sub_names
            }
            data = json.dumps(payload).encode("utf-8")
            # print("data:",data)
            sock.sendto(data, ("<broadcast>", BROADCAST_PORT))
            # print(f"📢 广播 SUPERNODE_HELLO: {super_device.device_id}")
            time.sleep(interval)

    threading.Thread(target=_broadcast, daemon=True).start()
