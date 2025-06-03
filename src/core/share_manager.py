# 设备连接控制、共享目录管理、权限控制
import asyncio

from typing import Callable, Dict, Any, Awaitable, List

from common.fileConf import ShareType, FileInfo

class ShareManager:
    def __init__(self):
        """初始化共享管理器"""
        self._devices = {}
        self.connections = {}
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

    def sendFile(self, deviceId: str, type: ShareType, files: List[FileInfo]) -> None:
        """
        传输文件。
        Args:
            deviceId (str): 设备ID。
            type (ShareType): 分享类型。
            files (List[FileInfo]): 文件信息数组。
        """
        pass

    def featchFile(self, deviceId: str, type: ShareType, files: List[FileInfo]) -> None:
        """
        获取文件。
        Args:
            deviceId (str): 设备ID。
            type (ShareType): 分享类型。
            files (List[FileInfo]): 文件信息数组。
        """
        pass

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