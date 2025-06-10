# 文件/文件夹传输主逻辑，含断点续传、多线程支持
import asyncio
import aiohttp
import os
import shutil
import tempfile

from typing import List, Dict, Tuple, Callable, Optional, Any

from .transfer_config import TransferStatus, STATUS_MESSAGE, get_file_id
from .transfer_utils import (
    is_image_or_video,
    generate_thumbnail_base64,
)
from src.common.global_config import CHUNK_SIZE
from src.common.fileConf import ShareType, FileInfo
from src.utils.logger import _logger


def prepare_upload_targets(
    files: List[FileInfo], transfer_control: Dict[str, Dict[str, Any]]
) -> List[Tuple[FileInfo, bool]]:
    """
    准备上传目标文件列表,如果文件是文件夹，则先压缩成 zip 文件。
    该函数会遍历传入的文件列表，如果是文件夹，则将其压缩成 zip 文件，并返回一个包含压缩文件信息的元组。
    Args:
        files (List[FileInfo]): 要上传的文件列表。
        transfer_control (Dict[str, Dict[str, Any]]): 传输控制状态字典，用于跟踪文件传输状态。
    Returns:
        List[Tuple[FileInfo, bool]]: 返回一个元组列表，每个元组包含文件信息和是否需要压缩的标志。
    其中元组的第一个元素是 FileInfo 对象，第二个元素是布尔值，表示是否需要压缩。
    """
    upload_targets = []
    for file in files:
        if os.path.isdir(file.path):  # 是文件夹，先压缩
            tmp_dir = tempfile.mkdtemp()
            zip_name = f"{file.name}.zip"
            zip_path = os.path.join(tmp_dir, zip_name)
            shutil.make_archive(zip_path.replace(".zip", ""), "zip", file.path)

            zip_info = FileInfo(
                name=zip_name,
                size=os.path.getsize(zip_path),
                path=zip_path,
                host=file.host,
            )
            upload_targets.append((zip_info, True))

            # 初始化传输控制状态
            transfer_control[get_file_id(zip_name, zip_info.size)] = {
                "status": TransferStatus.RUNNING,
                "event": asyncio.Event(),
            }
        else:
            upload_targets.append((file, False))

            # 初始化传输控制状态
            transfer_control[get_file_id(file.name, file.size)] = {
                "status": TransferStatus.RUNNING,
                "event": asyncio.Event(),
            }
    return upload_targets


async def upload_single_file(
    file: FileInfo,
    remote_dir: str,
    deviceId: str,
    host: str,
    port: str,
    upload_url: str,
    merge_url: str,
    need_unzip: bool,
    transfer_control: Dict[str, Dict[str, Any]],
    transfer_lock: asyncio.Lock,
    progress_callback: Optional[Callable[[str, float], None]] = None,
):
    """
    上传单个文件。
    Args:
        file (FileInfo): 要上传的文件信息。
        remote_dir (str): 远程目录路径。
        host (str): 目标主机地址。
        port (str): 目标端口号。
        upload_url (str): 上传分片的 URL。
        merge_url (str): 合并分片的 URL。
        need_unzip (bool): 是否需要在上传后解压缩文件。
        transfer_control (Dict[str, Dict[str, Any]]): 传输控制状态字典，用于跟踪文件传输状态。
        transfer_lock (asyncio.Lock): 异步锁，用于控制并发上传。
        progress_callback (Optional[Callable[[str, float], None]]): 可选的进度回调函数，接收文件名和进度百分比。
    """
    total = file.size
    total_chunks = (total + CHUNK_SIZE - 1) // CHUNK_SIZE

    file_id = get_file_id(file.name, total)

    is_media = is_image_or_video(file.name)
    is_video = file.name.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
    thumbnail_b64 = generate_thumbnail_base64(file.path, is_video) if is_media else None

    async with aiohttp.ClientSession() as session:
        # 先查询服务端已有的分片索引
        params = {
            "from_device_id": deviceId,
            "file_id": file_id,
            "filename": file.name,
            "path": remote_dir,
            "total_chunks": total_chunks,
        }
        if thumbnail_b64:
            params["thumbnail_b64"] = thumbnail_b64
            params["media_type"] = "video" if is_video else "image"
        async with session.get(
            f"http://{host}:{port}/get_uploaded_chunks",
            params=params,
        ) as resp:
            if resp.status != 200:
                raise Exception(
                    f"Failed to fetch uploaded chunks, error message: {await resp.text()}"
                )
            uploaded_chunks = set(await resp.json())
        with open(file.path, "rb") as f:
            for chunk_index in range(total_chunks):
                # 检查暂停
                async with transfer_lock:
                    if transfer_control:
                        transfer = transfer_control.get(file_id)
                        while transfer and transfer["status"] != TransferStatus.RUNNING:
                            if transfer["status"] >= 2:
                                _logger.info(STATUS_MESSAGE[transfer["status"]])
                                return
                            await transfer["event"].wait()
                            transfer["event"].clear()

                if chunk_index in uploaded_chunks:
                    continue  # 已上传，跳过

                f.seek(chunk_index * CHUNK_SIZE)
                data = f.read(CHUNK_SIZE)

                headers = {
                    "X-Filename": file.name,
                    "X-Chunk-Index": str(chunk_index),
                    "X-Total-Chunks": str(total_chunks),
                    "X-File-Id": file_id,
                    "X-Path": remote_dir,
                }

                async with session.post(upload_url, data=data, headers=headers) as r:
                    if r.status != 200:
                        raise Exception(
                            f"Chunk {chunk_index} upload failed, error message: {await r.text()}"
                        )

                if progress_callback:
                    percent = ((chunk_index + 1) / total_chunks) * 100
                    progress_callback(file.name, percent)

        # 所有分片上传完成后，发起合并请求
        async with session.post(
            merge_url,
            json={
                "file_id": file_id,
                "filename": file.name,
                "path": remote_dir,
                "total_chunks": total_chunks,
                "unzip_after_merge": need_unzip,  # 标记是否需要解压
            },
        ) as merge_resp:
            if merge_resp.status != 200:
                _logger.error(merge_resp)
                raise Exception(
                    f"Failed to merge file {file.name}, error message: {await merge_resp.text()}"
                )

    # 更新传输控制状态
    # _logger.info(transfer_control)
    async with transfer_lock:
        transfer_control[file_id]["status"] = TransferStatus.COMPLETED

    # 清理压缩包临时文件
    if need_unzip:
        os.remove(file.path)
        shutil.rmtree(os.path.dirname(file.path), ignore_errors=True)


async def async_send_files(
    dst_path: str,
    share_type: ShareType,
    deviceId: str,
    files: List[FileInfo],
    transfer_control: Dict[str, Dict[str, Any]],
    transfer_lock: asyncio.Lock,
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> Dict[str, str]:
    """
    发送文件到指定的目标路径。
    Args:
        dst_path (str): 目标路径，格式为 "ip:port/path"。
        share_type (ShareType): 文件共享类型，暂未使用。
        files (List[FileInfo]): 要上传的文件列表。
        transfer_control (Dict[str, Dict[str, Any]]): 传输控制状态字典，用于跟踪文件传输状态。
        progress_callback (Optional[Callable[[str, float], None]]): 可选的进度回调函数，接收文件名和进度百分比。
    Returns:
        Dict[str, str]: 返回一个字典，包含上传状态和消息。
    """
    try:
        host_port, remote_dir = dst_path.split("/", 1)
        host, port = host_port.split(":")
    except ValueError:
        raise ValueError("dst_path 格式应为 'ip:port/path'")

    upload_url = f"http://{host}:{port}/upload_chunk"
    merge_url = f"http://{host}:{port}/merge_chunks"

    upload_targets = prepare_upload_targets(files, transfer_control)

    await asyncio.gather(
        *[
            upload_single_file(
                file,
                remote_dir,
                deviceId,
                host,
                port,
                upload_url,
                merge_url,
                need_zip,
                transfer_control,
                transfer_lock,
                progress_callback,
            )
            for file, need_zip in upload_targets
        ]
    )
    return {"status": "success", "message": "All files uploaded successfully"}


async def download_single_file(
    file: FileInfo,
    dst_path: str,
    download_control: Dict[str, Dict[str, Any]],
    progress_callback: Optional[Callable[[str, float], None]] = None,
):
    """
    下载单个文件。
    Args:
        file (FileInfo): 要下载的文件信息。
        dst_path (str): 下载到的目标路径。
        download_control (Dict[str, Dict[str, Any]]): 传输控制状态字典，用于跟踪文件传输状态。
        progress_callback (Optional[Callable[[str, float], None]]): 可选的进度回调函数，接收文件名和进度百分比。
    """
    download_url = f"http://{file.host}/download_chunk"

    async with aiohttp.ClientSession() as session:
        # 获取文件大小
        if file.type == ShareType.FOLDER:
            async with session.get(
                f"http://{file.host}/prepare_folder_download",
                params={"path": file.path},
            ) as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to prepare folder: {await resp.text()}")
                result = await resp.json()
                file_path = result["zip_path"]
                file_name = result["zip_name"]
                total_size = result["zip_size"]
        else:
            file_path = file.path
            file_name = file.name
            total_size = file.size
        total_chunks = (total_size + CHUNK_SIZE - 1) // CHUNK_SIZE

        file_id = get_file_id(file_name, total_size)
        local_tmp_dir = os.path.join(dst_path, f".{file_id}.chunks")
        os.makedirs(local_tmp_dir, exist_ok=True)

        # 下载之前设置初始状态
        if download_control is not None:
            download_control[file_id] = {
                "status": TransferStatus.RUNNING,
                "event": asyncio.Event(),  # 控制暂停/恢复
            }

        # 分片下载
        for chunk_index in range(total_chunks):
            if download_control:
                transfer = download_control.get(file_id)
                while transfer and transfer["status"] != TransferStatus.RUNNING:
                    if transfer["status"] == TransferStatus.FAILED:
                        return
                    if transfer["status"] == TransferStatus.COMPLETED:
                        return
                    await transfer["event"].wait()
                    transfer["event"].clear()
            chunk_path = os.path.join(local_tmp_dir, f"chunk_{chunk_index}")
            if os.path.exists(chunk_path):
                continue

            async with session.get(
                download_url,
                params={
                    "path": file_path,
                    "chunk_index": chunk_index,
                    "chunk_size": CHUNK_SIZE,
                },
            ) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Chunk {chunk_index} download failed for {file_name}, error: {await resp.text()}"
                    )
                with open(chunk_path, "wb") as f:
                    f.write(await resp.read())

            if progress_callback:
                percent = ((chunk_index + 1) / total_chunks) * 100
                progress_callback(file_name, percent)

        # 合并文件
        local_path = os.path.join(dst_path, file_name)
        with open(local_path, "wb") as outfile:
            for i in range(total_chunks):
                chunk_path = os.path.join(local_tmp_dir, f"chunk_{i}")
                with open(chunk_path, "rb") as cf:
                    outfile.write(cf.read())

        # 删除临时目录
        shutil.rmtree(local_tmp_dir)

        # ✅ 解压缩逻辑（如果是zip文件）
        if file_name.endswith(".zip"):
            extract_dir = os.path.join(dst_path, file_name[:-4])  # 去掉.zip
            shutil.unpack_archive(local_path, extract_dir)
            os.remove(local_path)  # 删除zip包


async def async_download_files(
    dst_path: str,
    share_type: ShareType,
    files: List[FileInfo],
    download_control=Dict[str, Dict[str, Any]],
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> Dict[str, str]:
    # TODO: 下载时暂时没有略缩图
    """
    下载多个文件。
    Args:
        dst_path (str): 下载到的目标路径，格式为 "ip:port/path"。
        share_type (ShareType): 文件共享类型，暂未使用。
        files (List[FileInfo]): 要下载的文件列表。
        download_control (Dict[str, Dict[str, Any]]): 传输控制状态字典，用于跟踪文件传输状态。
        progress_callback (Optional[Callable[[str, float], None]]): 可选的进度回调函数，接收文件名和进度百分比。
    Returns:
        Dict[str, str]: 返回一个字典，包含下载状态和消息。
    """
    os.makedirs(dst_path, exist_ok=True)

    await asyncio.gather(
        *[
            download_single_file(f, dst_path, download_control, progress_callback)
            for f in files
        ]
    )
    return {"status": "success", "message": "All files downloaded successfully"}
