# 设备连接控制、共享目录管理、权限控制
import aiohttp
import asyncio
import os
import json

from typing import Callable, Dict, Any, Awaitable, List
from aiohttp import web, ClientSession

from src.common.fileConf import ShareType, FileInfo
from src.common.device import Device
from src.common.global_config import CHUNK_SIZE
from .transfer import (
    async_send_files,
    async_download_files,
    my_progress_callback,
    upload_chunk,
    get_uploaded_chunks,
    merge_chunks,
    prepare_folder_download,
    download_chunk,
)
from src.utils.logger import _logger


class ShareManager:
    def __init__(self, device: Device):
        """初始化共享管理器"""
        self.bindDevice = device
        self._devices = {}
        # connections 保存设备连接,key 为 连接设备 deviceId, value 为与该设备通信凭证
        self.connections = {}
        # transfers 保存文件传输任务,key 为 设备 deviceId, value 为传输任务列表
        self.transfers = {}

    # 启动两个简易http服务器监听连接端口和传输端口
    async def start_servers(self):
        # 连接端口，提供/connect接口处理握手请求
        connect_app = web.Application()
        connect_app.add_routes([web.post("/connect", self.handle_connect)])
        self.connect_runner = web.AppRunner(connect_app)
        await self.connect_runner.setup()
        connect_site = web.TCPSite(
            self.connect_runner, "0.0.0.0", self.bindDevice.conn_port
        )
        await connect_site.start()

        # 传输端口，示例简单实现
        transfer_app = web.Application()
        transfer_app.add_routes(
            [
                web.get("/list", self.handle_list),
                web.post("/upload_chunk", self.handle_upload_chunk),  # 新增上传分片接口
                web.get(
                    "/get_uploaded_chunks", self.handle_uploaded_chunks
                ),  # 新增查询已上传分片接口
                web.post("/merge_chunks", self.handle_merge_chunks),  # 新增合并分片接口
                web.get("/download_chunk", self.handle_download_chunk),  # 新增下载接口
                web.get(
                    "/prepare_folder_download", self.handle_prepare_folder_download
                ),  # 新增准备下载文件夹接口
            ]
        )
        self.transfer_runner = web.AppRunner(transfer_app)
        await self.transfer_runner.setup()
        transfer_site = web.TCPSite(
            self.transfer_runner, "0.0.0.0", self.bindDevice.transfer_port
        )
        await transfer_site.start()

        _logger.info(f"Connect server listening on port {self.bindDevice.conn_port}")
        _logger.info(
            f"Transfer server listening on port {self.bindDevice.transfer_port}"
        )

    async def stop_servers(self):
        await self.connect_runner.cleanup()
        await self.transfer_runner.cleanup()

    async def handle_upload_chunk(self, request: web.Request):
        headers = request.headers
        file_id = headers.get("X-File-Id")
        filename = headers.get("X-Filename")
        path = headers.get("X-Path")
        chunk_index = int(headers.get("X-Chunk-Index"))

        result = await upload_chunk(
            file_id=file_id,
            path=path,
            chunk_index=chunk_index,
            content=request.content,
        )

        return web.Response(text=result["message"])

    async def handle_uploaded_chunks(self, request: web.Request):
        file_id = request.query.get("file_id")
        filename = request.query.get("filename")
        path = request.query.get("path")
        thumbnail_b64 = request.query.get("thumbnail_b64")  # 可选
        media_type = request.query.get("media_type")  # 可选

        result = get_uploaded_chunks(file_id, filename, path, thumbnail_b64, media_type)
        if result["status"] == "no chunks":
            return web.json_response([])

        return web.json_response(sorted(result["chunks"]))

    async def handle_merge_chunks(self, request: web.Request):
        data = await request.json()
        file_id = data.get("file_id")
        filename = data.get("filename")
        path = data.get("path")
        total_chunks = data.get("total_chunks")
        unzip_after_merge = data.get("unzip_after_merge", False)

        result = await merge_chunks(
            file_id, filename, path, total_chunks, unzip_after_merge
        )
        if result["status"] == "error":
            _logger.error(
                f"Failed to merge chunks for {filename}, error: {result['message']}"
            )
            return web.Response(status=400, text=result["message"])

        return web.Response(text=result["message"])

    # 服务端：准备压缩文件夹
    async def handle_prepare_folder_download(self, request: web.Request):
        folder_path = request.query.get("path")
        if not folder_path or not os.path.isdir(folder_path):
            return web.Response(status=400, text="Invalid folder path")

        try:
            result = await prepare_folder_download(folder_path)
            return web.json_response(result)
        except Exception as e:
            return web.Response(status=400, text=str(e))

    async def handle_download_chunk(self, request: web.Request):
        file_path = request.query.get("path")
        chunk_index = int(request.query.get("chunk_index", "0"))
        chunk_size = int(request.query.get("chunk_size", str(CHUNK_SIZE)))

        if not file_path or not os.path.exists(file_path):
            return web.Response(status=404, text="File not found")

        try:
            return web.Response(
                body=await download_chunk(file_path, chunk_index, chunk_size)
            )
        except Exception as e:
            return web.Response(status=400, text=str(e))

    # 处理连接请求，返回transfer端口
    async def handle_connect(self, request):
        data = await request.json()
        from_device = data.get("fromDeviceId")
        _logger.info(f"Received connect request from {from_device}")
        # 这里可以加认证、校验逻辑
        # 返回transfer端口信息给请求方
        return web.json_response(
            {"transfer_port": self.bindDevice.transfer_port, "token": "example_token"}
        )

    # 示例目录列表接口（必须建立连接后才能访问，可在此处校验token）
    async def handle_list(self, request):
        """examples: 返回共享文件列表"""
        token = request.headers.get("Authorization")
        if token != "example_token":
            return web.json_response({"error": "Unauthorized"}, status=401)
        # 返回共享文件列表示例
        return web.json_response({"files": ["file1.txt", "file2.jpg"]})

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
        callback: Callable[[Dict[str, str]], Awaitable[Any]] = None,
    ) -> None:
        """
        连接局域网设备。
        Args:
            deviceId (str): 设备ID。
            bindParam (dict): 连接设备相关参数。
            callback (Callable): 连接设备状态异步回调，参数为{'deviceId': str}。
        """
        # 1. 查找设备信息
        device = self._devices.get(deviceId)
        if not device:
            if callback:
                await callback(
                    {
                        "deviceId": deviceId,
                        "status": "failed",
                        "msg": "Device not found",
                    }
                )
            return

        host = device.host_ip
        port = device.conn_port

        connect_url = f"http://{host}:{port}/connect"

        # 2. 发送连接请求，携带本设备ID和bindParam作为请求体
        payload = {"fromDeviceId": self.bindDevice.device_id, "bindParam": bindParam}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(connect_url, json=payload, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        token = data.get("token", None)
                        # 存储连接信息
                        self.connections[deviceId] = {
                            "host": host,
                            "port": data.get("transfer_port"),
                            "token": token,
                            "status": "connected",
                        }
                        if callback:
                            await callback(
                                {
                                    "deviceId": deviceId,
                                    "status": "success",
                                    "msg": "Connected",
                                }
                            )
                    else:
                        text = await resp.text()
                        if callback:
                            await callback(
                                {
                                    "deviceId": deviceId,
                                    "status": "failed",
                                    "msg": f"HTTP {resp.status}: {text}",
                                }
                            )
        except asyncio.TimeoutError:
            if callback:
                await callback(
                    {
                        "deviceId": deviceId,
                        "status": "failed",
                        "msg": "Connection timeout",
                    }
                )
        except Exception as e:
            if callback:
                await callback(
                    {"deviceId": deviceId, "status": "failed", "msg": str(e)}
                )

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

    async def sendFile(
        self, deviceId: str, type: ShareType, dst_path: str, files: List[FileInfo]
    ) -> Any:
        """
        传输文件。
        Args:
            deviceId (str): 设备ID。
            type (ShareType): 分享类型。
            files (List[FileInfo]): 文件信息数组。
        """
        dst_path = f"{self.connections[deviceId]['host']}:{self.connections[deviceId]['port']}/{dst_path}"
        return await async_send_files(
            dst_path=dst_path,
            share_type=type,
            files=files,
            progress_callback=my_progress_callback,  # 可以传入进度回调函数
        )

    async def downloadFile(
        self, deviceId: str, type: ShareType, dst_path: str, files: List[FileInfo]
    ) -> Any:
        """
        获取文件。
        Args:
            deviceId (str): 设备ID。
            type (ShareType): 分享类型。
            files (List[FileInfo]): 文件信息数组。
        """
        return await async_download_files(
            dst_path=dst_path,
            share_type=type,
            files=files,
            progress_callback=my_progress_callback,  # 可以传入进度回调函数
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
