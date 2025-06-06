import asyncio
import os
import json
import shutil
import tempfile

from typing import Dict, Optional

from src.common.global_config import CHUNK_SIZE


async def upload_chunk(
    file_id: str,
    path: str,
    chunk_index: int,
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
    return {"status": "success", "message": "Chunk uploaded successfully"}


def get_uploaded_chunks(
    file_id: str,
    filename: str,
    path: str,
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
        return {"status": "no chunks", "message": "No chunks found"}

    chunks = []
    for fname in os.listdir(save_dir):
        if fname.startswith("chunk_"):
            idx = int(fname.replace("chunk_", ""))
            chunks.append(idx)

    return {"status": "success", "chunks": sorted(chunks)}


def merge_chunks(
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
    if unzip_after_merge and output_file.endswith(".zip"):
        extract_dir = os.path.join(
            path, os.path.splitext(os.path.basename(output_file))[0]
        )
        shutil.unpack_archive(output_file, extract_dir)  # 解压到当前 path
        os.remove(output_file)  # 删除 zip 包
    return {
        "status": "success",
        "message": f"File {filename} merged successfully",
        "output_path": output_file,
    }


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


def prepare_folder_download(folder_path: str) -> Dict[str, str]:
    """
    准备文件夹下载，返回压缩包路径、名称和大小。
    Args:
        folder_path (str): 要压缩的文件夹路径。
    Returns:
        Dict[str, str]: 包含压缩包路径、名称和大小的字典。
    """
    tmp_dir = tempfile.gettempdir()
    base_name = os.path.join(tmp_dir, os.path.basename(folder_path))
    zip_path = shutil.make_archive(base_name, "zip", root_dir=folder_path)
    size = os.path.getsize(zip_path)

    return {
        "zip_path": zip_path,
        "zip_name": os.path.basename(zip_path),
        "zip_size": size,
    }
