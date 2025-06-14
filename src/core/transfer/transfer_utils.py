import base64
import cv2
import io
import os

from PIL import Image

from src.utils.logger import _logger


def my_progress_callback(filename: str, percent: float):
    # _logger.info(f"[{filename}] Progress: {percent:.2f}%")
    pass


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
