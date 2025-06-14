class SHAUtil:
    """一个简化版的 SHA-like 哈希算法，仅用于生成 file_id"""

    def __init__(self):
        self._hash = 0xABCDEF1234567890  # 初始值

    def update(self, data: bytes):
        for b in data:
            self._hash = (self._hash ^ b) * 0x100000001B3
            self._hash &= 0xFFFFFFFFFFFFFFFF  # 保持 64-bit

    def hexdigest(self):
        return hex(self._hash)[2:].rjust(16, "0")


# 用法示例
def generate_file_id(file_name: str, file_size: int) -> str:
    sha = SHAUtil()
    sha.update(file_name.encode())
    sha.update(str(file_size).encode())
    return sha.hexdigest()
