import enum

from src.utils import shautil


class TransferStatus(enum.Enum):
    RUNNING = enum.auto()  # 传输中
    PAUSED = enum.auto()  # 暂停中
    COMPLETED = enum.auto()  # 已完成
    FAILED = enum.auto()  # 失败


def get_file_id(file_name: str, file_size: int) -> str:
    return shautil.generate_file_id(file_name, file_size)
