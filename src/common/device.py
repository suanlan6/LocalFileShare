# 设备相关信息

class Device:
    def __init__(self, device_id: str, device_name: str, device_type: str):
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type

    def __repr__(self):
        return f"Device(id={self.device_id}, name={self.device_name}, type={self.device_type})"
    
    def to_dict(self):
        return {
            "device_id": self.device_id,
            "device_name": self.device_name,
            "device_type": self.device_type
        }