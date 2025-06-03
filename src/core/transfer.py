# 文件/文件夹传输主逻辑，含断点续传、多线程支持
from typing import List, Callable

from common.fileConf import ShareType, FileInfo


def send_files(src_device_id: str, dst_device_id: str, share_type: ShareType, files: List[FileInfo]) -> None:
    """
    发送文件或文件夹到目标设备。

    Args:
        src_device_id (str): 接收方设备的唯一标识（如 MAC 或自定义 UUID）。
        dst_device_id (str): 目标设备的唯一标识（如 MAC 或自定义 UUID）。
        share_type (ShareType): 文件类型。
        files (List[FileInfo]): 需要发送的文件/文件夹信息列表，支持递归传输目录结构。

    Raises:
        ConnectionError: 若设备不可达或连接失败。
        FileNotFoundError: 若本地文件不存在。
        TransmissionError: 若传输中出现中断或验证失败。
    """
    pass

def resume_transfer(task_id: str) -> None:
    """
    尝试恢复指定传输任务，支持断点续传。

    Args:
        task_id (str): 原始任务标识符，通常为哈希(device_id + file_path)。

    Raises:
        ValueError: 若任务 ID 不存在或已完成。
        IOError: 恢复失败，可能需要重新开始。
    """
    pass

def register_progress_callback(callback: Callable[[str, float], None]) -> None:
    """
    注册进度回调函数。

    Args:
        callback (Callable[[str, float], None]):
            回调函数，参数为 `task_id` 与 `progress`（0~1）。

    Example:
        register_progress_callback(lambda tid, p: print(f"{tid}: {p*100:.1f}%"))
    """
    pass
