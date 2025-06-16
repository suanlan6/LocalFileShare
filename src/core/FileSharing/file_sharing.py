import ctypes
import os
import socket
import threading
import json
import time
from http.client import responses
from typing import Dict, List, Tuple, Optional, Callable
import platform
import getpass

from src.common.fileConf import ShareType, FileInfo
from src.core.FileSharing.SharingUtils import (
    _is_hidden_or_system_file,
    get_file_type,
    is_valid_subpath,
    _get_windows_drives,
)
from src.utils.logger import _logger


class FileSharing:
    def __init__(self, host: str, config_path: str = "conf/shares.json"):
        """
        初始化文件共享系统
        :param device_name: 本机设备名称
        :param config_path: 共享配置存储路径
        """
        self.host = host  # 主机名或IP地址
        self.os_type = platform.system()
        self.current_user = getpass.getuser()
        self.os_type = platform.system()
        self.root_path = self._get_system_root()  # 初始化根路径
        self.current_path = self.root_path  # 当前浏览路径

        dir_path = os.path.dirname(config_path)

        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.config_path = config_path
        self.shared_dirs: Dict[str, FileInfo] = {}  # {共享路径: 元信息}
        self.peer_shares: Dict[str, dict] = {}  # {设备名: 共享信息(IP、端口、路径)}
        self.load_config()

    # ------------------ 本地目录操作 ------------------
    def _get_system_root(self) -> str:
        """获取系统根目录路径（跨平台）"""
        if self.os_type == "Windows":
            return "/"  # Windows特殊根路径
        else:
            # Linux/macOS: 使用根目录
            return "/"

    def set_current_path(self, path: str):
        """设置当前浏览路径"""
        if self._is_valid_path(path):
            self.current_path = path
        else:
            raise ValueError(f"无效路径: {path}")

    def _is_valid_path(self, path: str) -> bool:
        """检查路径是否有效"""
        if self.os_type == "Windows":
            if path == "/":
                return True
            return os.path.exists(path)
        else:
            return os.path.exists(path)

    def list_local_dir(self, path: Optional[str] = None) -> List[FileInfo]:
        """
        列出本地目录内容
        :param path: 目录路径
        :return: [(文件名, 是否是目录, 文件大小)]
        """
        target_path = path if path else self.current_path
        if self.os_type == "Windows" and target_path == "/":
            return _get_windows_drives()
        if not self._is_valid_path(path) or not os.path.isdir(path):
            return []
        if (
            (self.os_type != "Windows" and path.count("/") <= 1)
            or self.os_type == "Windows"
            and "\\" not in path
            and not path.endswith(":\\")
        ):
            return self.list_local_dir("/")

        items = []
        IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
        # 添加返回上一级选项（除非在根目录）
        if path != self.root_path and (
            self.os_type != "Windows"
            or (self.os_type == "Windows" and "\\" in path and not path.endswith(":\\"))
        ):
            if (
                (self.os_type != "Windows" and path.count("/") <= 1)
                or self.os_type == "Windows"
                and "\\" not in path
                and not path.endswith(":\\")
            ):
                parent = "/"
            else:
                parent = os.path.dirname(path)
            # items.append({"name": "..", "path": parent, "type": ShareType.FOLDER})
            items.append(
                FileInfo(
                    name="..",
                    path=parent,
                    size=0,  # 上级目录没有大小
                    host=f"{self.host}",
                    file_type=ShareType.FOLDER,
                )
            )
        for entry in os.scandir(path):
            try:
                # 跳过隐藏文件和系统文件
                if _is_hidden_or_system_file(entry):
                    continue
                is_dir = entry.is_dir()
                size = entry.stat().st_size if entry.is_file() else 0
                file_type = get_file_type(entry.path)
                # items.append(
                #     {
                #         "name": entry.name,
                #         "path": entry.path,
                #         "type": file_type,
                #         "size": size,
                #     }
                # )
                items.append(
                    FileInfo(
                        name=entry.name,
                        path=entry.path,
                        size=size,
                        host=f"{self.host}",
                        file_type=file_type,
                    )
                )
            except OSError:
                continue
        return items

    # ------------------ 共享目录管理 ------------------
    def add_shared_dir(self, path: str, read_only: bool = True):
        """
        添加共享目录（默认使用当前路径），自动使用路径的文件名作为共享名称
        :param path: 可选目录路径
        """
        target_path = path
        # Windows特殊路径不能共享
        if self.os_type == "Windows" and (
            target_path == "/" or target_path.startswith("Network")
        ):
            raise ValueError("不能共享特殊系统路径")

        if not os.path.isdir(target_path) and not os.path.isfile(target_path):
            raise ValueError(f"目录或文件不存在: {target_path}")

        abs_path = os.path.abspath(target_path)
        name = os.path.basename(abs_path)
        file_type = get_file_type(abs_path)  # 确保路径有效

        size = os.path.getsize(path) if os.path.isfile(path) else 0
        if self.os_type == "Windows" and abs_path.endswith(":\\"):
            name = f"{abs_path[0]}:"
        self.shared_dirs[abs_path] = FileInfo(
            name=name,
            size=size,  # 共享目录不需要大小
            path=abs_path,
            host=f"{self.host}",
            file_type=file_type,
        )
        self.save_config()
        _logger.info(f"已共享目录: {name} ({abs_path})")

    def remove_shared_dir(self, path: str):
        """移除共享目录"""
        abs_path = os.path.abspath(path)
        if abs_path in self.shared_dirs:
            del self.shared_dirs[abs_path]
            self.save_config()

    def get_shared_dirs(self) -> Dict[str, dict]:
        """获取所有共享目录信息"""
        return self.shared_dirs.copy()

    def enter_shared_dir(self, path: str):
        """
        进入共享目录
        :param path: 共享目录路径
        """
        valid = False
        for shared_path in self.shared_dirs:
            if is_valid_subpath(shared_path, path):
                valid = True
                break

        if not valid:
            return list(self.get_shared_dirs().values())
        else:
            return self.list_local_dir(path)

    # peer_logic
    # 1.connect and add to peer_shares
    # 2.get peer_shares
    def add_peer_share(self, peer: Dict[str, any]):
        """
        添加对等设备的共享信息到peer_shares字典
        :param peer: 对等设备信息字典，结构为:
            {
                "device": "设备名",
                "address": "IP地址",
                "port": 端口号,
            }
        """
        # 验证必要字段
        required_fields = ["device", "address", "port"]
        for field in required_fields:
            if field not in peer:
                raise ValueError(f"peer信息缺少必要字段: {field}")

        device_name = peer["device"]
        self.peer_shares[device_name] = {
            "address": peer["address"],
            "port": peer["port"],
            "path": "/",
        }
        shares = self.list_peer_dir(device_name, "/")
        # 创建/更新对等设备信息
        self.peer_shares[device_name]["shares"] = shares

    def get_peer_shares(self, peer_name: str) -> Optional[Dict[str, dict]]:
        """
        获取指定设备的共享目录
        :param peer_name: 设备名称
        :return: 共享目录信息字典 或 None
        """
        peer = self.peer_shares.get(peer_name)
        if not peer:
            return None
        return peer.copy()

    def list_peer_dir(self, peer_name: str, path: str = "/") -> List[Dict[str, any]]:
        """
        列出对等设备共享路径下的文件/文件夹
        :param peer_name: 设备名
        :param path: 要浏览的路径，相对路径或共享根目录名
        :return: 文件/目录列表
        """

        peer = self.peer_shares.get(peer_name)
        # 此处访问并修改路径

        if not peer:
            raise ValueError(f"未找到对等设备: {peer_name}")
        request = {"action": "LIST_PEER_DIR", "path": path}
        try:
            with socket.create_connection(
                (peer["address"], peer["port"]), timeout=5
            ) as s:
                s.sendall(json.dumps(request).encode())
                s.shutdown(socket.SHUT_WR)

                data = b""
                while True:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                response = json.loads(data.decode())
                peer["path"] = response["data"]["path"]
                return response["data"]["data"]
        except Exception as e:
            _logger.error(f"请求共享目录失败: {e}")
            return []

    # ------------------ 内部方法 ------------------
    def load_config(self):
        """加载共享配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    raw_data = json.load(f)
                self.shared_dirs = {
                    k: FileInfo.from_dict(v) for k, v in raw_data.items()
                }
        except Exception as e:
            _logger.error(f"加载配置失败: {str(e)}")

    def save_config(self):
        """保存共享配置"""
        try:
            with open(self.config_path, "w") as f:
                json.dump(
                    self.shared_dirs,
                    f,
                    indent=2,
                    default=lambda o: (
                        o.to_dict() if isinstance(o, FileInfo) else str(o)
                    ),
                )
        except Exception as e:
            _logger.error(f"保存配置失败: {str(e)}")

    # ------------------ 响应核心 ------------------
    def _handle_file_request(self, path: str) -> List[Dict]:
        """处理文件传输请求"""
        try:
            req_path = path
            # / 表示共享根列表
            if req_path == "/":
                return list(self.get_shared_dirs().values())
            else:
                # 找到与请求路径匹配的共享路径（或子路径）
                valid = False
                for shared_path in self.shared_dirs:
                    if is_valid_subpath(shared_path, req_path):
                        valid = True
                        break

                if not valid:
                    return list(self.get_shared_dirs().values())
                else:
                    return self.list_local_dir(req_path)
        except Exception as e:
            _logger.error(f"处理请求出错: {e}")


if __name__ == "__main__":
    # loggers = get_logger()
    fs = FileSharing()
    print(fs.list_local_dir("C:\\Program Files (x86)"))
