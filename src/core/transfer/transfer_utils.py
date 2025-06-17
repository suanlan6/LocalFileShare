import asyncio
import base64
import cv2
import io
import os
import tarfile
import zstandard as zstd

from PIL import Image

from src.utils.logger import _logger


def my_progress_callback(filename: str, percent: float):
    # _logger.info(f"[{filename}] Progress: {percent:.2f}%")
    pass


async def run_sync(func, *args, **kwargs):
    return await asyncio.to_thread(func, *args, **kwargs)


def is_image_or_video(filename: str) -> bool:
    """
    判断文件是否为图像或视频文件。
    """
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
    """
    生成文件的缩略图并返回其 Base64 编码。
    """
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


def compress_folder_to_zst(src_folder: str, out_path: str, level: int = 3):
    """
    将文件夹压缩为 .tar.zst 文件
    """
    tar_path = out_path + ".tmp.tar"

    # 第一步：创建 tar 包
    with tarfile.open(tar_path, "w") as tar:
        tar.add(src_folder, arcname=os.path.basename(src_folder))

    # 第二步：使用 zstd 压缩 tar 包
    cctx = zstd.ZstdCompressor(level=level)
    with open(tar_path, "rb") as f_in, open(out_path, "wb") as f_out:
        cctx.copy_stream(f_in, f_out)

    os.remove(tar_path)  # 删除中间文件
    return out_path


def decompress_zst_to_folder(zst_path: str, out_dir: str):
    """
    解压 .tar.zst 文件到指定目录
    """
    tar_path = zst_path + ".tmp.tar"

    # 第一步：zstd 解压出 tar
    dctx = zstd.ZstdDecompressor()
    with open(zst_path, "rb") as f_in, open(tar_path, "wb") as f_out:
        dctx.copy_stream(f_in, f_out)

    # 第二步：解包 tar 文件
    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(path=out_dir)

    os.remove(tar_path)
