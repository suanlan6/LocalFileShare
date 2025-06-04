# 设备连接控制、共享目录管理、权限控制
import aiohttp
import asyncio

from typing import Callable, Dict, Any, Awaitable, List
from aiohttp import web, ClientSession

from common.fileConf import ShareType, FileInfo
from common.device import Device
from file_manager import async_send_files
from utils.logger import _logger

class ShareManager:
    def __init__(self, device: Device):
        """初始化共享管理器"""
        self.bindDevice = device
        self._devices = {}
        # connections 保存设备连接,key 为 连接设备 deviceId, value 为与该设备通信凭证
        self.connections = {}
        # transfers 保存文件传输任务,key 为 设备 deviceId, value 为传输任务列表
        self.transfers = {}

    def startScan(self) -> None:
        """
        扫描当前局域网内的接入设备。
        """
        pass

    def stopScan(self) -> None:
        """
        停止扫描局域网设备。
        """
        pass

    async def connect(
        self,
        deviceId: str,
        bindParam: dict,
        callback: Callable[[Dict[str, str]], Awaitable[Any]]
    ) -> None:
        """
        连接局域网设备。
        Args:
            deviceId (str): 设备ID。
            bindParam (dict): 连接设备相关参数。
            callback (Callable): 连接设备状态异步回调，参数为{'deviceId': str}。
        """
        pass

    def disconnect(self, deviceId: str) -> None:
        """
        关闭设备连接。
        Args:
            deviceId (str): 设备ID。
        """
        pass

    def confirmConnect(self) -> None:
        """
        接受共享连接。
        """
        pass

    def refuseConnect(self) -> None:
        """
        拒绝共享连接。
        """
        pass

    async def sendFile(self, deviceId: str, type: ShareType, files: List[FileInfo]) -> Any:
        """
        传输文件。
        Args:
            deviceId (str): 设备ID。
            type (ShareType): 分享类型。
            files (List[FileInfo]): 文件信息数组。
        """
        return await async_send_files(
            dst_path=f"{self.connections[deviceId]['host']}:{self.connections[deviceId]['port']}",
            share_type=type,
            files=files,
            progress_callback=None  # 可以传入进度回调函数
        )

    async def fetchFile(self, deviceId: str, type: ShareType, files: List[FileInfo]) -> Any:
        """
        获取文件。
        Args:
            deviceId (str): 设备ID。
            type (ShareType): 分享类型。
            files (List[FileInfo]): 文件信息数组。
        """
        return await async_send_files(
            dst_path=f"{self.bindDevice.host_ip}:{self.bindDevice.bind_port}",
            share_type=type,
            files=files,
            progress_callback=None  # 可以传入进度回调函数
        )

    def cancelSendFile(self, deviceId: str) -> None:
        """
        取消所有文件传输。
        Args:
            deviceId (str): 设备ID。
        """
        pass

    def cancelSendFileForFiles(self, deviceId: str, files: List[FileInfo]) -> None:
        """
        取消特定的文件传输。
        Args:
            deviceId (str): 设备ID。
            files (List[FileInfo]): 文件信息数组。
        """
        pass

    def abortReceiveFile(self, deviceId: str) -> None:
        """
        终止对应设备文件接收。
        Args:
            deviceId (str): 设备ID。
        """
        pass

    def abortReceiveFiles(self, deviceId: str, files: List[FileInfo]) -> None:
        """
        终止对应设备文件接收。
        Args:
            deviceId (str): 设备ID。
            files (List[FileInfo]): 文件信息数组。
        """
        pass