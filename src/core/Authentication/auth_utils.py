import os
import hashlib
import time


def generate_pin() -> str:
    """Generate a random 6-digit PIN."""
    # 获取高熵输入（时间戳 + 进程ID + os.urandom）
    entropy = (
        str(time.time()).encode("utf-8")
        + str(os.getpid()).encode("utf-8")
        + os.urandom(16)
    )
    # 使用哈希生成伪唯一值
    hash_digest = hashlib.sha256(entropy).hexdigest()

    # 取前面的十六进制字符，转成整数，再模 900000 + 100000 保证6位
    pin = int(hash_digest[:12], 16) % 900000 + 100000
    return f"{pin:06d}"
