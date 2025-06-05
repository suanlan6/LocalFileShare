# 文件/文件夹传输主逻辑，含断点续传、多线程支持
import asyncio
import aiohttp
import os
import base64
import cv2
import io
import json
import shutil
import tempfile

from typing import List, Dict, Tuple, Callable, Optional
from PIL import Image

from src.common.fileConf import ShareType, FileInfo
from src.utils import shautil
from src.utils.logger import _logger


CHUNK_SIZE = 1024 * 1024


def my_progress_callback(filename: str, percent: float):
    _logger.info(f"[{filename}] Progress: {percent:.2f}%")


def is_image_or_video(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".gif",
        ".webp",
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
    }


def generate_thumbnail_base64(file_path: str, is_video: bool) -> str:
    if is_video:
        cap = cv2.VideoCapture(file_path)
        success, frame = cap.read()
        cap.release()
        if not success:
            _logger.error(
                f"无法读取视频文件 {file_path},请检查对应文件是否存在或格式是否正确"
            )
            raise RuntimeError("无法读取视频第一帧")
        # 转为 RGB 格式
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
    else:
        img = Image.open(file_path)
        img = img.convert("RGB")

    img.thumbnail((128, 128))  # 可根据需要调整缩略图尺寸

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()


def prepare_upload_targets(files: List[FileInfo]) -> List[Tuple[FileInfo, bool]]:
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
        else:
            upload_targets.append((file, False))
    return upload_targets


async def upload_single_file(
    file: FileInfo,
    remote_dir: str,
    host: str,
    port: str,
    upload_url: str,
    merge_url: str,
    need_unzip: bool,
    progress_callback: Optional[Callable[[str, float], None]] = None,
):
    total = file.size
    total_chunks = (total + CHUNK_SIZE - 1) // CHUNK_SIZE

    file_id = shautil.generate_file_id(file.name, total)

    is_media = is_image_or_video(file.name)
    is_video = file.name.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
    thumbnail_b64 = generate_thumbnail_base64(file.path, is_video) if is_media else None

    async with aiohttp.ClientSession() as session:
        # 先查询服务端已有的分片索引
        params = {"file_id": file_id, "filename": file.name, "path": remote_dir}
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

    # 清理压缩包临时文件
    if need_unzip:
        os.remove(file.path)
        shutil.rmtree(os.path.dirname(file.path), ignore_errors=True)


async def async_send_files(
    dst_path: str,
    share_type: str,
    files: List[FileInfo],
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> str:
    try:
        host_port, remote_dir = dst_path.split("/", 1)
        host, port = host_port.split(":")
    except ValueError:
        raise ValueError("dst_path 格式应为 'ip:port/path'")

    upload_url = f"http://{host}:{port}/upload_chunk"
    merge_url = f"http://{host}:{port}/merge_chunks"

    upload_targets = prepare_upload_targets(files)

    await asyncio.gather(
        *[
            upload_single_file(
                file,
                remote_dir,
                host,
                port,
                upload_url,
                merge_url,
                need_zip,
                progress_callback,
            )
            for file, need_zip in upload_targets
        ]
    )
    return "Transfer complete"


async def upload_chunk(
    file_id: str,
    path: str,
    chunk_index: int,
    content: asyncio.StreamReader,
) -> Dict[str, str]:
    """
    上传单个分片的处理函数。

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


async def merge_chunks(
    file_id: str,
    filename: str,
    path: str,
    total_chunks: int,
    unzip_after_merge: bool = False,
) -> Dict[str, str]:
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


async def download_single_file(
    file: FileInfo,
    dst_path: str,
    progress_callback: Optional[Callable[[str, float], None]] = None,
):
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

        file_id = shautil.generate_file_id(file_name, total_size)
        local_tmp_dir = os.path.join(dst_path, f".{file_id}.chunks")
        os.makedirs(local_tmp_dir, exist_ok=True)

        # 分片下载
        for chunk_index in range(total_chunks):
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
    share_type: str,
    files: List[FileInfo],
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> str:
    # TODO: 下载时暂时没有略缩图
    os.makedirs(dst_path, exist_ok=True)

    await asyncio.gather(
        *[download_single_file(f, dst_path, progress_callback) for f in files]
    )
    return "Download complete"


async def prepare_folder_download(folder_path: str) -> Dict[str, str]:
    """
    准备文件夹下载，返回压缩包路径、名称和大小。
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


async def download_chunk(file_path: str, chunk_index: int, chunk_size: int) -> bytes:
    try:
        with open(file_path, "rb") as f:
            f.seek(chunk_index * chunk_size)
            data = f.read(chunk_size)
        return data
    except Exception as e:
        raise Exception(
            f"Failed to download chunk {chunk_index} from {file_path}: {str(e)}"
        )


def resume_transfer(task_id: str) -> None:
    """
    尝试恢复指定传输任务，支持断点续传。

    Args:
        task_id (str): 原始任务标识符，通常为哈希(device_id + file_path)。

    Raises:
        ValueError: 若任务 ID 不存在或已完成。
        IOError: 恢复失败，可能需要重新开始。
    """
    pass


def register_progress_callback(callback: Callable[[str, float], None]) -> None:
    """
    注册进度回调函数。

    Args:
        callback (Callable[[str, float], None]):
            回调函数，参数为 `task_id` 与 `progress`（0~1）。

    Example:
        register_progress_callback(lambda tid, p: print(f"{tid}: {p*100:.1f}%"))
    """
    pass
