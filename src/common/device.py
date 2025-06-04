# 设备相关信息

class Device:
    def __init__(self, device_id: str, device_name: str, device_type: str, host_ip: str, conn_port: int, transfer_port: int):
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type
        self.host_ip = host_ip
        self.conn_port = conn_port
        self.transfer_port = transfer_port

    def __repr__(self):
        return f"Device(id={self.device_id}, name={self.device_name}, type={self.device_type}, host_ip={self.host_ip}, conn_port={self.conn_port}, transfer_port={self.transfer_port})"

    def to_dict(self):
        return {
            "device_id": self.device_id,
            "device_name": self.device_name,
            "device_type": self.device_type,
            "host_ip": self.host_ip,
            "conn_port": self.conn_port,
            "transfer_port": self.transfer_port
        }