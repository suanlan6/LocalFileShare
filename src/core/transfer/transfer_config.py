import enum

from src.utils import shautil


class TransferStatus(enum.IntEnum):
    RUNNING = 0  # 传输中
    PAUSED = 1  # 暂停中
    COMPLETED = 2  # 已完成
    FAILED = 3  # 失败
    CANCELED_BY_USER = 4  # 已被用户取消
    CANCELED_BY_SERVER = 5  # 已被服务端取消
    ZST_COMPRESSING = 6  # ZST 压缩中


STATUS_MESSAGE = {
    TransferStatus.RUNNING: "文件传输中",
    TransferStatus.PAUSED: "文件传输已暂停",
    TransferStatus.FAILED: "文件传输失败",
    TransferStatus.COMPLETED: "文件传输已完成",
    TransferStatus.CANCELED_BY_USER: "文件传输已被用户取消",
    TransferStatus.CANCELED_BY_SERVER: "文件传输已被服务端取消",
    TransferStatus.ZST_COMPRESSING: "正在压缩文件",
}


def get_file_id(file_name: str, file_size: int) -> str:
    return shautil.generate_file_id(file_name, file_size)
