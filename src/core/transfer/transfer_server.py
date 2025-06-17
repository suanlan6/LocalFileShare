import asyncio
import os
import json
import shutil
import tempfile
import time

from typing import Dict, Any, Optional

from src.common.global_config import CHUNK_SIZE
from src.utils.logger import _logger
from .transfer_config import TransferStatus
from .transfer_utils import compress_folder_to_zst, decompress_zst_to_folder, run_sync


async def upload_chunk(
    file_id: str,
    path: str,
    chunk_index: int,
    total_chunks: int,
    upload_by_other_device: Dict[str, Dict[str, Any]],
    upload_lock: asyncio.Lock,
    content: asyncio.StreamReader,
) -> Dict[str, str]:
    """
    上传单个分片的处理函数。
    Args:
        file_id (str): 文件的唯一标识符。
        path (str): 存储分片的目录路径。
        chunk_index (int): 分片索引，从 0 开始。
        content (asyncio.StreamReader): 异步读取流，用于读取分片内容。

    Returns:
        Dict[str, str]: 包含上传状态和消息的字典。
    """
    save_dir = os.path.join(path, f".{file_id}.chunks")
    os.makedirs(save_dir, exist_ok=True)
    chunk_path = os.path.join(save_dir, f"chunk_{chunk_index}")

    with open(chunk_path, "wb") as f:
        while True:
            chunk = await content.read(CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)

    # 更新来自其他设备的上传进度
    percent = (chunk_index + 1) / total_chunks * 100
    try:
        async with upload_lock:
            upload_by_other_device[file_id]["progress"] = percent
    except KeyError:
        _logger.error(f"[{file_id}] 上传进度更新失败, 可能是因为文件传输取消或被删除")
    except Exception as e:
        _logger.error(f"[{file_id}] 更新上传进度时发生错误: {str(e)}")
    return {"status": "success", "message": "Chunk uploaded successfully"}


async def get_uploaded_chunks(
    from_device_id: str,
    file_id: str,
    filename: str,
    path: str,
    total_chunks: int,
    upload_by_other: Dict[str, Dict[str, Dict[str, str]]],
    upload_lock: asyncio.Lock,
    thumbnail_b64: Optional[str] = None,
    media_type: Optional[str] = None,
) -> Dict[str, str]:
    """
    获取上传的分片信息，并保存略缩图。
    Args:
        file_id (str): 文件的唯一标识符。
        filename (str): 文件名。
        path (str): 存储分片的目录路径。
        thumbnail_b64 (Optional[str]): 略缩图的 Base64 编码字符串。
        media_type (Optional[str]): 媒体类型（如 "image" 或 "video"）。

    Returns:
        Dict[str, str]: 包含上传状态和分片索引的字典。
    """
    # 保存略缩图信息
    if thumbnail_b64 and media_type:
        meta_path = os.path.join(path, f"{filename}.meta.json")
        metadata = {"type": media_type, "thumbnail_b64": thumbnail_b64}
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f)

    save_dir = os.path.join(path, f".{file_id}.chunks")
    if not os.path.exists(save_dir):
        if file_id not in upload_by_other[from_device_id]:
            upload_by_other[from_device_id][file_id] = {
                "filename": filename,
                "status": TransferStatus.RUNNING,
                "uploaded_chunks": [],
                "total_chunks": total_chunks,
                "path": path,
                "media_type": media_type,
                "thumbnail_b64": thumbnail_b64,
            }
        return {"status": "no chunks", "message": "No chunks found"}

    uploaded_chunks = [
        int(fname.replace("chunk_", ""))
        for fname in os.listdir(save_dir)
        if fname.startswith("chunk_")
    ]

    # 3. 并发安全地记录任务
    async with upload_lock:
        if file_id not in upload_by_other[from_device_id]:
            upload_by_other[from_device_id][file_id] = {
                "filename": filename,
                "status": TransferStatus.RUNNING,
                "uploaded_chunks": uploaded_chunks,
                "total_chunks": total_chunks,
                "path": path,
                "media_type": media_type,
                "thumbnail_b64": thumbnail_b64,
            }
        else:
            # 更新进度
            upload_by_other[from_device_id][file_id][
                "uploaded_chunks"
            ] = uploaded_chunks

    return {"status": "success", "chunks": sorted(uploaded_chunks)}


async def merge_chunks(
    file_id: str,
    filename: str,
    path: str,
    total_chunks: int,
    unzip_after_merge: bool = False,
) -> Dict[str, str]:
    """
    合并分片文件。
    Args:
        file_id (str): 文件的唯一标识符。
        filename (str): 合并后的文件名。
        path (str): 存储分片的目录路径。
        total_chunks (int): 分片总数。
        unzip_after_merge (bool): 是否在合并后解压缩文件。
    Returns:
        Dict[str, str]: 包含合并状态和输出文件路径的字典。
    """
    if not all([file_id, filename, path, total_chunks]):
        return {"status": "error", "message": "Missing parameters"}

    chunk_dir = os.path.join(path, f".{file_id}.chunks")
    output_file = os.path.join(path, filename)

    if not os.path.exists(chunk_dir):
        return {"status": "error", "message": "Chunk directory not found"}

    with open(output_file, "wb") as outfile:
        for i in range(total_chunks):
            chunk_path = os.path.join(chunk_dir, f"chunk_{i}")
            if not os.path.exists(chunk_path):
                return {"status": "error", "message": f"Missing chunk {i}"}
            with open(chunk_path, "rb") as infile:
                outfile.write(infile.read())

    # 合并完成后删除分片目录
    shutil.rmtree(chunk_dir)

    # 解压缩逻辑
    try:
        if unzip_after_merge and output_file.endswith(".tar.zst"):
            # extract_dir = os.path.join(
            #     path,
            #     os.path.splitext(os.path.splitext(os.path.basename(output_file))[0])[0],
            # )
            await run_sync(decompress_zst_to_folder, output_file, path)
            os.remove(output_file)

    except Exception as e:
        _logger.error(f"Error during unzipping: {e}")
        return {
            "status": "error",
            "message": f"Failed to unzip file {filename}: {str(e)}",
        }
    return {
        "status": "success",
        "message": f"File {filename} merged successfully",
        "output_path": output_file,
    }


async def remove_cancel_directories_with_retry(paths, max_retries=10, delay=1):
    for path in paths:
        for attempt in range(max_retries):
            try:
                if os.path.exists(path):
                    shutil.rmtree(path)
                    _logger.info(f"[√] 已删除临时分片目录: {path}")
                break
            except PermissionError as e:
                if attempt < max_retries - 1:
                    _logger.warning(
                        f"[!] 删除目录失败({e}),{delay}s后重试...（第{attempt+1}次）"
                    )
                    await asyncio.sleep(delay)
                else:
                    _logger.error(f"[x] 多次重试后仍无法删除目录: {path}，错误: {e}")
            except Exception as e:
                _logger.error(f"[x] 删除目录时发生未知错误: {path}，错误: {e}")
                break


async def download_chunk(file_path: str, chunk_index: int, chunk_size: int) -> bytes:
    """
    下载指定分片的内容。
    Args:
        file_path (str): 文件的完整路径。
        chunk_index (int): 分片索引，从 0 开始。
        chunk_size (int): 每个分片的大小。
    Returns:
        bytes: 分片内容的字节数据。
    """
    try:
        with open(file_path, "rb") as f:
            f.seek(chunk_index * chunk_size)
            data = f.read(chunk_size)
        return data
    except Exception as e:
        raise Exception(
            f"Failed to download chunk {chunk_index} from {file_path}: {str(e)}"
        )


async def prepare_folder_download(folder_path: str) -> Dict[str, str]:
    """
    准备文件夹下载，返回压缩包路径、名称和大小。
    Args:
        folder_path (str): 要压缩的文件夹路径。
    Returns:
        Dict[str, str]: 包含压缩包路径、名称和大小的字典。
    """
    tmp_dir = tempfile.gettempdir()
    base_name = os.path.join(tmp_dir, os.path.basename(folder_path))
    zip_path = await run_sync(compress_folder_to_zst, folder_path, base_name)
    size = os.path.getsize(zip_path)

    return {
        "zip_path": zip_path,
        "zip_name": os.path.basename(zip_path),
        "zip_size": size,
    }
