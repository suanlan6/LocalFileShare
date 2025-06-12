# 设备连接控制、共享目录管理、权限控制
import aiohttp
import asyncio
import os
import json

from typing import Callable, Dict, Optional, Any, Awaitable, List
from collections import defaultdict
from aiohttp import web, ClientSession

from src.common.fileConf import ShareType, FileInfo
from src.common.device import Device
from src.common.global_config import CHUNK_SIZE
from .transfer.transfer_config import TransferStatus
from .transfer.transfer_utils import my_progress_callback
from .transfer.transfer_client import (
    async_send_files,
    async_download_files,
)
from .transfer.transfer_server import (
    upload_chunk,
    get_uploaded_chunks,
    merge_chunks,
    prepare_folder_download,
    download_chunk,
    remove_cancel_directories_with_retry,
)
from .FileSharing.file_sharing import FileSharing
from .Authentication.auth import Authentication
from src.utils.logger import _logger


class ShareManager:
    def __init__(self, device: Device):
        """初始化共享管理器"""
        self.bindDevice = device
        self._devices = {}
        # (客户端)connections 保存设备连接,key 为 连接设备 device_id, value 为与该设备通信凭证
        self.connections = {}
        # (客户端)transfers 保存文件传输任务,key 为 设备 device_id, value 为传输任务列表
        self.transfers = {}
        # (客户端) transfers_locks 用于控制传输任务的并发访问，key 为 device_id
        self.transfers_locks: Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)
        # key 为 device_id，value 为 {file_id: {"status": ..., "event": ...}}
        self.downloads = {}
        self.downloads_locks: Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)
        # (服务端) connections, 保存设备连接信息(host, ip, port, token等)
        self.client_connections: Dict[str, Dict[str, Any]] = {}
        # (服务端)用于记录其他设备上传的文件
        self.upload_by_other: Dict[str, Dict[str, Dict]] = {}
        # 全局上传记录的写锁
        self.upload_lock = asyncio.Lock()
        # 文件相关操作
        self.file_share = FileSharing(device.host_ip)

        # 用于存储所有异步任务(目前用于删除文件)
        self.tasks = []

        # 安全验证模块
        self.auth = Authentication()

    # 启动两个简易http服务器监听连接端口和传输端口
    async def start_servers(self):
        # 连接端口，提供/connect接口处理握手请求
        connect_app = web.Application()
        connect_app.add_routes(
            [
                web.post("/connect", self.handle_connect),
                web.post("/verify_pin", self.handle_verify_pin),
            ]
        )
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
                web.post(
                    "/get_remote_shared_files",
                    self.handle_get_shared_file_of_remote_device,
                ),  # 新增获取远程设备共享文件接口
                web.post(
                    "/cancel_transfer", self.handle_cancel_transfer_client
                ),  # 新增取消传输任务接口(客户端)
                web.post(
                    "/cancel_transfer_server", self.handle_cancel_transfer_server
                ),  # 新增取消传输任务接口(服务端)
                web.post(
                    "/delete_folder_package", self.handle_delete_cancel_folder_package
                ),  # 新增删除取消的文件夹包接口(服务端)
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

        for task in self.tasks:
            await task
        self.tasks.clear()

    async def pause_upload_client(self, device_id: str, file_id: str):
        """如果任务是执行状态，中断上传任务"""
        async with self.transfers_locks[device_id]:
            if (
                device_id in self.transfers
                and file_id in self.transfers[device_id]
                and self.transfers[device_id][file_id]["status"]
                == TransferStatus.RUNNING
            ):
                self.transfers[device_id][file_id]["status"] = TransferStatus.PAUSED

    async def resume_upload_client(self, device_id: str, file_id: str):
        """如果任务是暂停状态，则恢复上传任务"""
        async with self.transfers_locks[device_id]:
            if (
                device_id in self.transfers
                and file_id in self.transfers[device_id]
                and self.transfers[device_id][file_id]["status"]
                == TransferStatus.PAUSED
            ):
                self.transfers[device_id][file_id]["status"] = TransferStatus.RUNNING
                self.transfers[device_id][file_id]["event"].set()

    async def pause_download(self, device_id: str, file_id: str):
        async with self.downloads_locks[device_id]:
            if (
                device_id in self.downloads
                and file_id in self.downloads[device_id]
                and self.downloads[device_id][file_id]["status"]
                == TransferStatus.RUNNING
            ):
                self.downloads[device_id][file_id]["status"] = TransferStatus.PAUSED

    async def resume_download(self, device_id: str, file_id: str):
        async with self.downloads_locks[device_id]:
            if (
                device_id in self.downloads
                and file_id in self.downloads[device_id]
                and self.downloads[device_id][file_id]["status"]
                == TransferStatus.PAUSED
            ):
                self.downloads[device_id][file_id]["status"] = TransferStatus.RUNNING
                self.downloads[device_id][file_id]["event"].set()

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
        from_device_id = request.query.get("from_device_id")
        file_id = request.query.get("file_id")
        filename = request.query.get("filename")
        path = request.query.get("path")
        total_chunks = request.query.get("total_chunks")
        thumbnail_b64 = request.query.get("thumbnail_b64")  # 可选
        media_type = request.query.get("media_type")  # 可选

        result = await get_uploaded_chunks(
            from_device_id,
            file_id,
            filename,
            path,
            total_chunks,
            self.upload_by_other,
            self.upload_lock,
            thumbnail_b64,
            media_type,
        )
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

        result = merge_chunks(file_id, filename, path, total_chunks, unzip_after_merge)
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
            result = prepare_folder_download(folder_path)
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
        device_id: str,
        bindParam: dict,
        callback: Callable[[Dict[str, str]], Awaitable[Any]] = None,
    ) -> Dict[str, Any]:
        """
        连接局域网设备，调用 Authentication 统一完成认证流程（含请求、PIN 输入、token 校验）。
        Args:
            device_id (str): 目标设备 ID。
            bindParam (dict): 连接参数。
            callback (Callable): 状态异步回调。
        """
        # 1. 查找目标设备信息
        device = self._devices.get(device_id)
        if not device:
            if callback:
                await callback(
                    {
                        "device_id": device_id,
                        "status": "failed",
                        "msg": "Device not found",
                    }
                )
            return {"status": "failed", "msg": "Device not found"}

        try:
            # 2. 认证阶段（封装完整交互逻辑）
            connection_info = await self.auth.authenticate(
                from_device=self.bindDevice,
                to_device=device,
                bind_param=bindParam,
            )

            # 认证完成后返回 token 和 transfer_port 信息
            token = connection_info["token"]
            port = connection_info["port"]
            host = device.host_ip

            # 3. 建立连接状态记录
            self.connections[device_id] = {
                "host": host,
                "port": port,
                "token": token,
                "status": "connected",
            }

            # 初始化任务结构
            self.transfers[device_id] = {}
            self.transfers_locks[device_id] = asyncio.Lock()
            self.downloads[device_id] = {}
            self.downloads_locks[device_id] = asyncio.Lock()

            if callback:
                await callback(
                    {
                        "device_id": device_id,
                        "status": "success",
                        "msg": "Connected",
                    }
                )
            return {"status": "success", "msg": f"device {device_id} connected"}

        except asyncio.TimeoutError:
            if callback:
                await callback(
                    {
                        "device_id": device_id,
                        "status": "failed",
                        "msg": "Connection timeout",
                    }
                )
            return {"status": "failed", "msg": "Connection timeout"}
        except Exception as e:
            if callback:
                await callback(
                    {
                        "device_id": device_id,
                        "status": "failed",
                        "msg": str(e),
                    }
                )
            return {"status": "failed", "msg": str(e)}

    def disconnect(self, device_id: str) -> None:
        """
        关闭设备连接。
        Args:
            device_id (str): 设备ID。
        """
        pass

    # 处理连接请求，返回transfer端口
    async def handle_connect(self, request: web.Request):
        try:
            data = await request.json()
            bind_param = data.get("bindParam", {})
            from_device_id = bind_param.get("fromDeviceId")
            _logger.info(f"Received connect request from {from_device_id}")

            # 1. 是否允许连接，由 self.auth 决定
            accept = await self.auth.should_accept_connection(
                from_device_id, bind_param
            )

            if not accept:
                return web.json_response(
                    {"error": "Connection rejected by user"}, status=403
                )

            # 2. 生成 PIN 并设置有效期，例如 120 秒
            pin_code, session_id = self.auth.generate_pin(
                from_device_id=from_device_id, expire_seconds=120
            )

            _logger.info(f"PIN {pin_code} generated for {from_device_id}")

            # # 3. 初始化上传任务
            # self.upload_by_other[from_device_id] = {}
            # # 这里可以加认证、校验逻辑
            # self.client_connections[from_device_id] = {
            #     "host": bind_param.get("host"),
            #     "port": bind_param.get("port"),
            #     "token": "example_token",  # 这里可以生成一个真实的token
            # }
            # 返回transfer端口信息给请求方
            return web.json_response(
                {
                    "transfer_port": self.bindDevice.transfer_port,
                    "pin": pin_code,
                    "session_id": session_id,
                    "expire_seconds": 120,  # PIN 有效期
                }
            )
        except Exception as e:
            _logger.error(f"Error handling connect request: {str(e)}")
            return web.json_response({"error": str(e)}, status=500)

    async def handle_verify_pin(self, request: web.Request):
        """
        处理 PIN 验证请求。
        Args:
            request (web.Request): HTTP 请求对象。
        Returns:
            web.Response: 响应对象，包含验证结果。
        """
        try:
            data = await request.json()
            session_id = data.get("session_id")
            pin = data.get("pin")
            from_device_id = data.get("fromDeviceId")
            host = data.get("host")
            port = data.get("port")

            if not session_id or not pin:
                return web.json_response(
                    {"error": "Missing session_id or pin"}, status=400
                )

            verified = self.auth.verify_pin(session_id, pin)
            if verified:

                # 完成连接流程，返回 token 和 transfer_port
                token, transfer_port = self.auth.finalize_connection(
                    transfer_port=self.bindDevice.transfer_port,
                )
                # 3. 初始化上传任务
                self.upload_by_other[from_device_id] = {}
                # 这里可以加认证、校验逻辑
                self.client_connections[from_device_id] = {
                    "host": host,
                    "port": port,
                    "token": token,  # 这里可以生成一个真实的token
                }
                return web.json_response(
                    {
                        "status": "success",
                        "token": token,
                        "transfer_port": transfer_port,
                    }
                )
            else:
                return web.json_response({"status": "failed"}, status=403)
        except Exception as e:
            _logger.error(f"Error verifying PIN: {str(e)}")
            return web.json_response({"error": str(e)}, status=500)

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
        self, device_id: str, type: ShareType, dst_path: str, files: List[FileInfo]
    ) -> Any:
        """
        传输文件。
        Args:
            device_id (str): 设备ID。
            type (ShareType): 分享类型。
            files (List[FileInfo]): 文件信息数组。
        """
        dst_path = f"{self.connections[device_id]['host']}:{self.connections[device_id]['port']}/{dst_path}"
        return await async_send_files(
            dst_path=dst_path,
            share_type=type,
            device_id=self.bindDevice.device_id,
            files=files,
            transfer_control=self.transfers[device_id],
            transfer_lock=self.transfers_locks[device_id],
            progress_callback=my_progress_callback,  # 可以传入进度回调函数
        )

    async def downloadFile(
        self, device_id: str, type: ShareType, dst_path: str, files: List[FileInfo]
    ) -> Any:
        """
        获取文件。
        Args:
            device_id (str): 设备ID。
            type (ShareType): 分享类型。
            files (List[FileInfo]): 文件信息数组。
        """
        return await async_download_files(
            dst_path=dst_path,
            share_type=type,
            files=files,
            download_control=self.downloads[device_id],
            download_lock=self.downloads_locks[device_id],
            progress_callback=my_progress_callback,  # 可以传入进度回调函数
        )

    def cancelSendFile(self, device_id: str) -> None:
        """
        取消所有文件传输。
        Args:
            device_id (str): 设备ID。
        """
        pass

    async def cancelSendFileForFiles(self, device_id: str, file_ids: List[str]) -> None:
        """
        取消特定的文件传输。
        Args:
            device_id (str): 设备ID。
            files (List[str]): 文件信息数组。
        """
        remove_files = []
        async with self.upload_lock:
            _logger.info(f"[!] 取消设备 {device_id} 的上传任务，文件ID: {file_ids}")
            if device_id in self.upload_by_other:
                for file_id in file_ids:
                    if file_id in self.upload_by_other[device_id]:
                        remove_files.append(
                            os.path.join(
                                self.upload_by_other[device_id][file_id]["path"],
                                f".{file_id}.chunks",
                            )
                        )
                        del self.upload_by_other[device_id][file_id]
                        # 如果该设备下已无记录，也移除设备项
                        if not self.upload_by_other[device_id]:
                            del self.upload_by_other[device_id]
                    else:
                        _logger.error(
                            f"[!] 文件ID {file_id} 不存在于设备 {device_id} 上传任务中"
                        )
                        return
            else:
                _logger.error(f"[!] 未找到设备 {device_id} 的上传任务")
                return

        # 通知客户端
        await asyncio.gather(
            *(self._notify_client_cancel(device_id, file_id) for file_id in file_ids)
        )

        remove_task = asyncio.create_task(
            remove_cancel_directories_with_retry(remove_files)
        )
        self.tasks.append(remove_task)

    async def _notify_client_cancel(self, device_id: str, file_id: str) -> None:
        """
        向客户端发送取消指令，通知其将对应传输任务标记为 TransferStatus.CANCELED_BY_SERVER。
        """
        if device_id not in self.client_connections:
            _logger.warning(f"[!] 未连接设备 {device_id}")
            return

        host = self.client_connections[device_id]["host"]
        port = self.client_connections[device_id]["port"]
        url = f"http://{host}:{port}/cancel_transfer"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json={"file_id": file_id}) as resp:
                    if resp.status == 200:
                        _logger.info(f"[√] 成功通知客户端取消上传任务 {file_id}")
                    else:
                        _logger.error(f"[x] 通知客户端失败: {await resp.text()}")
        except Exception as e:
            _logger.error(f"[x] 通知客户端取消失败: {e}")

    async def handle_cancel_transfer_client(self, request: web.Request) -> web.Response:
        data = await request.json()
        file_id = data.get("file_id")
        if not file_id:
            return web.Response(status=400, text="Missing file_id")

        for device_id, transfers in self.transfers.items():
            for tid, t in transfers.items():
                if tid == file_id:
                    t["status"] = TransferStatus.CANCELED_BY_SERVER
                    t["event"].set()
                    _logger.info(f"[客户端] 接收到服务端取消任务: {file_id}")
                    return web.Response(text="Canceled")

        return web.Response(status=404, text="Transfer not found")

    async def client_cancel_transfer(self, device_id: str, file_ids: List[str]) -> None:
        """
        客户端取消传输任务。
        Args:
            device_id (str): 设备ID。
            file_ids (List[str]): 文件ID列表。
        """
        remove_ids = []
        if device_id in self.transfers:
            async with self.transfers_locks[device_id]:
                for file_id in file_ids:
                    if file_id in self.transfers[device_id]:
                        self.transfers[device_id][file_id][
                            "status"
                        ] = TransferStatus.CANCELED_BY_USER
                        self.transfers[device_id][file_id]["event"].set()
                        # 从传输任务中移除
                        remove_ids.append(file_id)
                        _logger.info(f"[客户端] 已取消传输任务: {file_id}")
                    else:
                        _logger.error(
                            f"[客户端] 未找到传输任务: {file_id} 在设备 {device_id} 上"
                        )
        else:
            _logger.error(f"[客户端] 未找到设备 {device_id} 的传输任务")

        # 通知服务端取消上传任务
        if device_id not in self.connections:
            _logger.warning(f"[!] 未连接设备 {device_id}")
            return

        host = self.connections[device_id]["host"]
        port = self.connections[device_id]["port"]
        url = f"http://{host}:{port}/cancel_transfer_server"

        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "device_id": self.bindDevice.device_id,
                    "file_ids": remove_ids,
                }
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        _logger.info(f"[√] 成功通知服务端取消上传任务 {remove_ids}")
                    else:
                        _logger.error(f"[x] 通知服务端失败: {await resp.text()}")
        except Exception as e:
            _logger.error(f"[x] 通知服务端取消失败: {e}")

    async def handle_cancel_transfer_server(self, request: web.Request) -> web.Response:
        data = await request.json()
        file_ids = data.get("file_ids")
        device_id = data.get("device_id")

        if not file_ids or not device_id:
            return web.Response(status=400, text="Missing file_ids or device_id")

        remove_files = []
        remove_tids = []
        async with self.upload_lock:
            transfers = self.upload_by_other[device_id]
            for tid in file_ids:
                if tid in transfers:
                    transfers[tid]["status"] = TransferStatus.CANCELED_BY_SERVER
                    _logger.info(f"[服务端] 接收到客户端取消任务: {tid}")
                    remove_files.append(
                        os.path.join(transfers[tid]["path"], f".{tid}.chunks")
                    )
                    remove_tids.append(tid)
                else:
                    _logger.warning(
                        f"[服务端] 未找到传输任务: {tid} 在设备 {device_id} 上"
                    )
                    return web.Response(status=404, text=f"Transfer {tid} not found")

            # 删除上传记录
            for tid in remove_tids:
                del transfers[tid]
            if not transfers:
                del self.upload_by_other[device_id]

        # 删除取消的分片目录
        remove_task = asyncio.create_task(
            remove_cancel_directories_with_retry(remove_files)
        )
        self.tasks.append(remove_task)

        return web.Response(status=200, text="成功取消传输任务")

    async def cancel_download_client(self, device_id: str, file_ids: List[str]) -> None:
        """
        客户端取消下载任务。
        Args:
            device_id (str): 设备ID。
            file_ids (List[str]): 文件ID列表。
        """
        if device_id not in self.downloads:
            _logger.error(f"[客户端] 未找到设备 {device_id} 的下载任务")
            return

        async with self.downloads_locks[device_id]:
            for file_id in file_ids:
                if file_id in self.downloads[device_id]:
                    self.downloads[device_id][file_id][
                        "status"
                    ] = TransferStatus.CANCELED_BY_USER
                    self.downloads[device_id][file_id]["event"].set()
                    _logger.info(f"[客户端] 已取消下载任务: {file_id}")
                else:
                    _logger.error(
                        f"[客户端] 未找到下载任务: {file_id} 在设备 {device_id} 上"
                    )

    async def handle_delete_cancel_folder_package(self, request: web.Request):
        """
        删除取消的文件夹包。
        Args:
            request (web.Request): HTTP请求对象。
        Returns:
            web.Response: 响应对象。
        """
        data = await request.json()
        path = data.get("path")
        if not path or not os.path.exists(path):
            return web.Response(status=400, text="Invalid path")

        try:
            await remove_cancel_directories_with_retry([path])
            _logger.info(f"已删除取消的文件夹包: {path}")
            return web.Response(status=200, text="Folder package deleted successfully")
        except Exception as e:
            _logger.error(f"删除文件夹包失败: {str(e)}")
            return web.Response(status=500, text=str(e))

    def abortReceiveFile(self, device_id: str) -> None:
        """
        终止对应设备文件接收。
        Args:
            device_id (str): 设备ID。
        """
        pass

    def abortReceiveFiles(self, device_id: str, files: List[FileInfo]) -> None:
        """
        终止对应设备文件接收。
        Args:
            device_id (str): 设备ID。
            files (List[FileInfo]): 文件信息数组。
        """
        pass

    async def handle_get_shared_file_of_remote_device(self, request: web.Request):
        """
        获取远程设备共享的文件列表。
        Args:
            device_id (str): 设备ID。
        Returns:
            List[FileInfo]: 远程设备共享的文件信息列表。
        """
        try:
            data = await request.json()
            bind_param = data.get("bindParam", {})
            directory = bind_param.get("directory")
            if not directory:
                return web.json_response(
                    {"error": "Missing directory in bindParam"}, status=400
                )

            shared_dir = self.file_share._handle_file_request(directory)

            return web.json_response(
                data=shared_dir,
                dumps=lambda obj: json.dumps(obj, default=lambda x: x.__dict__),
            )
        except Exception as e:
            # 明确返回 application/json 的错误响应，避免客户端报 mimetype 错误
            return web.json_response({"error": f"Server error: {str(e)}"}, status=500)

    async def get_remote_shared_file(
        self,
        device_id: str,
        bindParam: dict,
    ) -> List[FileInfo]:
        """
        获取远程设备共享的文件列表。
        Args:
            device_id (str): 设备ID。
        Returns:
            List[FileInfo]: 远程设备共享的文件信息列表。
        """
        # 这里可以实现获取远程设备共享文件的逻辑
        host, port = (
            self.connections[device_id]["host"],
            self.connections[device_id]["port"],
        )
        connect_url = f"http://{host}:{port}/get_remote_shared_files"

        payload = {"fromDeviceId": self.bindDevice.device_id, "bindParam": bindParam}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(connect_url, json=payload, timeout=5) as resp:
                    if resp.status == 200:
                        return [FileInfo.from_dict(file) for file in await resp.json()]
                    else:
                        _logger.error(
                            f"Failed to get remote shared files: {str(await resp.json())}"
                        )
                        return []
        except Exception as e:
            _logger.error(f"Failed to get remote shared files: {str(e)}")
            return []

    def get_local_directory(self, directory: Optional[str] = None) -> List[FileInfo]:
        """
        获取本地共享目录的文件列表。
        Returns:
            List[FileInfo]: 本地共享目录的文件信息列表。
        """
        # 这里可以实现获取本地共享目录文件的逻辑
        return self.file_share.list_local_dir(path=directory)

    def set_shared_directory(self, directory: str) -> None:
        """
        设置本地共享目录。
        Args:
            directory (str): 共享目录路径。
        """
        # 这里可以实现设置本地共享目录的逻辑
        self.file_share.add_shared_dir(path=directory)

    def cancel_shared_directory(self, directory: str) -> None:
        """
        取消本地共享目录。
        """
        # 这里可以实现取消本地共享目录的逻辑
        self.file_share.remove_shared_dir(path=directory)
