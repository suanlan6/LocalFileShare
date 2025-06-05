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

from src.common.fileConf import ShareType
from src.core.FileSharing.SharingUtils import _is_hidden_or_system_file, is_valid_subpath, _get_windows_drives
from src.utils.logger import CustomFormatter, get_logger


class FileSharing:
    def __init__(self, logger: CustomFormatter, config_path: str = "shares.json"):
        """
        初始化文件共享系统
        :param device_name: 本机设备名称
        :param config_path: 共享配置存储路径
        """
        self.logger = logger
        self.os_type = platform.system()
        self.current_user = getpass.getuser()
        self.os_type = platform.system()
        self.root_path = self._get_system_root()  # 初始化根路径
        self.current_path = self.root_path  # 当前浏览路径

        self.config_path = config_path
        self.shared_dirs: Dict[str, dict] = {}  # {共享路径: 元信息}
        self.peer_shares: Dict[str, dict] = {}  # {设备名: 共享信息(IP、端口、路径)}
        self.load_config()
    # ------------------ 本地目录操作 ------------------
    def _get_system_root(self) -> str:
        """获取系统根目录路径（跨平台）"""
        if self.os_type == "Windows":
            return "baseroot"  # Windows特殊根路径
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
            if path == "baseroot":
                return True
            return os.path.exists(path)
        else:
            return os.path.exists(path)



    def list_local_dir(self, path: Optional[str] = None) -> List[Dict[str, any]]:
        """
        列出本地目录内容
        :param path: 目录路径
        :return: [(文件名, 是否是目录, 文件大小)]
        """
        target_path = path if path else self.current_path
        if self.os_type == "Windows" and target_path == "baseroot":
            return _get_windows_drives()
        if not self._is_valid_path(path) or not os.path.isdir(path):
            return []

        items = []
        IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        # 添加返回上一级选项（除非在根目录）
        if path != self.root_path and (self.os_type != "Windows" or
                                       (self.os_type == "Windows" and "\\" in path and not path.endswith(":\\")) or
                                       (self.os_type == "Windows" and "//" in path and not path.endswith("://"))):
            parent = os.path.dirname(path)
            items.append({
                "name": "..",
                "path": parent,
                "type": ShareType.FOLDER
            })
        if self.os_type == "Windows" and (path.endswith(":\\") or path.endswith("://")):
            parent = self.root_path
            items.append({
                "name": "..",
                "path": parent,
                "type": ShareType.FOLDER
            })
        for entry in os.scandir(path):
            try:
                # 跳过隐藏文件和系统文件
                if _is_hidden_or_system_file(entry):
                    continue
                is_dir = entry.is_dir()
                size = entry.stat().st_size if entry.is_file() else 0
                if is_dir:
                    file_type = ShareType.FOLDER
                else:
                    # 检查图片扩展名
                    ext = os.path.splitext(entry.name)[1].lower()
                    file_type = ShareType.PICTURE if ext in IMAGE_EXTENSIONS else ShareType.FILE
                items.append({
                    "name": entry.name,
                    "path": entry.path,
                    "type": file_type,
                    "size": size,
                })
            except OSError:
                continue
        return items



    # ------------------ 共享目录管理 ------------------
    def add_shared_dir(self, path: Optional[str] = None, read_only: bool = True):
        """
        添加共享目录（默认使用当前路径），自动使用路径的文件名作为共享名称
        :param path: 可选目录路径
        """
        target_path = path if path else self.current_path
        # Windows特殊路径不能共享
        if self.os_type == "Windows" and (target_path == "baseroot" or target_path.startswith("Network")):
            raise ValueError("不能共享特殊系统路径")

        if not os.path.isdir(target_path):
            raise ValueError(f"目录不存在: {target_path}")

        abs_path = os.path.abspath(target_path)
        name = os.path.basename(abs_path)
        if self.os_type == "Windows" and abs_path.endswith(":\\"):
            name = f"{abs_path[0]}:"
        self.shared_dirs[abs_path] = {
            'name': name,
            'path': abs_path,
            'read_only': read_only,
        }
        self.save_config()
        self.logger.info(f"已共享目录: {name} ({abs_path})")

    def remove_shared_dir(self, path: str):
        """移除共享目录"""
        abs_path = os.path.abspath(path)
        if abs_path in self.shared_dirs:
            del self.shared_dirs[abs_path]
            self.save_config()

    def get_shared_dirs(self) -> Dict[str, dict]:
        """获取所有共享目录信息"""
        return self.shared_dirs.copy()


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
                "shares": {共享目录信息列表},
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

            "path": "baseroot",
        }
        shares = self.list_peer_dir(device_name,"baseroot")
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

    def list_peer_dir(self, peer_name: str, path: str = "baseroot") -> List[Dict[str, any]]:
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
        request = {
            "action": "LIST_PEER_DIR",
            "path": path
        }
        try:
            with socket.create_connection((peer["address"], peer["port"]), timeout=5) as s:
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
            self.logger.error(f"请求共享目录失败: {e}")
            return []

    # ------------------ 文件操作接口 ------------------
    def download_file(self, peer_name: str, share_path: str,
                      remote_path: str, local_path: str,
                      progress_callback: Optional[Callable] = None):
        """
        从其他设备下载文件
        :param peer_name: 设备名称
        :param share_path: 共享目录路径
        :param remote_path: 远程文件路径(相对共享目录)
        :param local_path: 本地保存路径
        :param progress_callback: 进度回调函数(bytes_downloaded, total_size)
        """
        # 实现细节留空
        raise NotImplementedError("下载功能需要具体实现")

    def upload_file(self, peer_name: str, share_path: str,
                    local_path: str, remote_path: str,
                    progress_callback: Optional[Callable] = None):
        """
        上传文件到其他设备
        :param peer_name: 设备名称
        :param share_path: 共享目录路径
        :param local_path: 本地文件路径
        :param remote_path: 远程保存路径(相对共享目录)
        :param progress_callback: 进度回调函数(bytes_uploaded, total_size)
        """
        # 实现细节留空
        raise NotImplementedError("上传功能需要具体实现")

    # ------------------ 内部方法 ------------------
    def load_config(self):
        """加载共享配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.shared_dirs = json.load(f)
        except Exception as e:
            self.logger.error(f"加载配置失败: {str(e)}")

    def save_config(self):
        """保存共享配置"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.shared_dirs, f, indent=2)
        except Exception as e:
            self.logger.error(f"保存配置失败: {str(e)}")




    # ------------------ 响应核心 ------------------
    def _handle_file_request(self, request: dict, client_socket: socket.socket):
        """处理文件传输请求"""
        try:
            if request['action'] == 'LIST_PEER_DIR':
                req_path = request.get("path", "baseroot")

                # baseroot 表示共享根列表
                if req_path == "baseroot":
                    response = {
                        "data": {
                            "path": "baseroot",
                            "data": list(self.get_shared_dirs().values()),
                        }}
                else:
                    # 找到与请求路径匹配的共享路径（或子路径）
                    valid = False
                    for shared_path in self.shared_dirs:
                        if is_valid_subpath(shared_path, req_path):
                            valid = True
                            break

                    if not valid:
                        response = {
                            "data":{
                                "path": "baseroot",
                                "data":list(self.get_shared_dirs().values()),
                            }}
                    else:
                        response = {
                            "data":{
                                "path": req_path,
                                "data":self.list_local_dir(),
                            }}
                client_socket.sendall(json.dumps(response).encode())

            elif request['action'] == 'DOWNLOAD':
                # 实现文件下载逻辑
                pass
        except Exception as e:
            self.logger.error(f"处理请求出错: {e}")
            client_socket.sendall(json.dumps({"error": str(e)}).encode())

if __name__ == '__main__':
    loggers = get_logger()
    fs = FileSharing(loggers)
    print(fs.list_local_dir("C:\\Program Files (x86)"))