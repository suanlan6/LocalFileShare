import enum


class ShareType(enum.IntEnum):
    """分享文件类型"""

    FILE = 0
    FOLDER = 1
    PICTURE = 2
    OTHER = 3


class FileInfo:
    """文件信息"""

    def __init__(
        self,
        name: str,
        size: int,
        path: str,
        host: str = None,
        file_type: ShareType = ShareType.OTHER,
    ):
        self.name = name  # 文件名
        self.size = size  # 文件大小（字节）
        self.path = path  # 文件路径
        self.host = host  # 文件所在主机(ip地址+端口)
        self.type = file_type  # 文件类型

    def __repr__(self):
        return f"FileInfo(name={self.name}, size={self.size}, path={self.path}, host={self.host}, type={self.type})"

    def to_dict(self):
        return {
            "name": self.name,
            "size": self.size,
            "path": self.path,
            "host": self.host,
            "type": self.type.value,  # 如果ShareType是枚举
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            size=data["size"],
            path=data["path"],
            host=data["host"],
            file_type=ShareType(data["type"]),  # 如果用的是枚举
        )
