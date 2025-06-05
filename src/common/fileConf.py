import enum


class ShareType(enum.Enum):
    """分享文件类型"""
    FILE = enum.auto()
    FOLDER = enum.auto()
    PICTURE = enum.auto()
    OTHER = enum.auto()

class FileInfo:
    """文件信息"""
    def __init__(self, name: str, size: int, path: str, host: str, file_type: ShareType = ShareType.OTHER):
        self.name = name        # 文件名
        self.size = size        # 文件大小（字节）
        self.path = path        # 文件路径
        self.host = host        # 文件所在主机(ip地址+端口)
        self.type = file_type   # 文件类型

    def __repr__(self):
        return f"FileInfo(name={self.name}, size={self.size}, path={self.path}, host={self.host}, type={self.type})"
