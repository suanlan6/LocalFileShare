import ctypes
import os
import platform
from typing import List, Dict

from src.common.fileConf import FileInfo, ShareType


def _is_hidden_or_system_file(entry: os.DirEntry) -> bool:
    """检查文件或目录是否隐藏或系统文件"""
    # 在Windows上使用文件属性
    if platform.system() == "Windows":
        try:
            # 使用ctypes获取文件属性
            attrs = ctypes.windll.kernel32.GetFileAttributesW(entry.path)
            if attrs == -1:  # 错误
                return True

            # 检查隐藏属性 (0x2) 和系统属性 (0x4)
            return attrs & (0x2 | 0x4) != 0
        except:
            # 回退方案：基于名称的过滤
            return entry.name.startswith(".") or entry.name in [
                "$RECYCLE.BIN",
                "System Volume Information",
                "$Recycle.Bin",
                "RECYCLER",
                "RECYCLED",
                "Thumbs.db",
                "desktop.ini",
            ]

    # 在Linux/macOS上，检查以点开头的文件
    return entry.name.startswith(".")


def is_valid_subpath(shared_path, req_path):
    abs_shared = os.path.abspath(shared_path)
    abs_req = os.path.abspath(req_path)

    if os.name == "nt":
        if (
            os.path.splitdrive(abs_shared)[0].lower()
            != os.path.splitdrive(abs_req)[0].lower()
        ):
            return False

    try:
        return os.path.commonpath([abs_shared, abs_req]) == abs_shared
    except ValueError:
        return False


def _get_windows_drives() -> List[FileInfo]:
    """获取Windows所有逻辑驱动器信息"""
    drives = []
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(
                FileInfo(
                    name=f"本地磁盘 ({letter}:)",
                    size=0,
                    path=drive,
                    file_type=ShareType.FOLDER,
                )
            )
    return drives
