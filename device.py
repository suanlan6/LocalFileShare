import socket
import uuid


class Device:
    def __init__(self, device_id: str = None, device_name: str = "", device_type: str = "",
                 host_ip: str = None, conn_port: int = 0, transfer_port: int = 0):
        self.device_id = device_id or str(uuid.uuid4())  # 自动生成唯一标识
        self.device_name = device_name
        self.device_type = device_type

        self.host_ip = host_ip or self._get_local_ip()
        self.conn_port = conn_port
        self.transfer_port = transfer_port
        self.is_super_node = False
        self.super_node_id = None
        self.super_ip = None
        self.super_port = None

    def to_dict(self):
        return {
            "device_id": self.device_id,
            "device_name": self.device_name,
            "device_type": self.device_type,
            "host_ip": self.host_ip,
            "conn_port": self.conn_port,
            "transfer_port": self.transfer_port,
            "is_super_node": self.is_super_node,
            "super_node_id": self.super_node_id,
            "super_ip": self.super_ip,
            "super_port": self.super_port
        }

    @staticmethod
    def _get_local_ip():
        """尝试自动获取本机局域网 IP"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"

    def __repr__(self):
        return f"<Device {self.device_id} @ {self.host_ip}:{self.conn_port}, super={self.is_super_node}>"

