import threading
import socket
import json
import time
import os
from src.utils.logger import get_logger
from file_sharing import FileSharing  # 假设你把代码保存为 file_sharing.py

# ---- SERVER 端：监听请求并交给 FileSharing 处理 ----
def start_server(file_sharing: FileSharing, port: int):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen(5)
    print(f"[Server] Listening on port {port}...")

    while True:
        client_socket, addr = server.accept()
        threading.Thread(
            target=handle_client, args=(file_sharing, client_socket)
        ).start()


def handle_client(file_sharing: FileSharing, client_socket: socket.socket):
    try:
        data = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            data += chunk

        request = json.loads(data.decode())
        file_sharing._handle_file_request(request, client_socket)
    except Exception as e:
        print(f"[Server] Error: {e}")
    finally:
        client_socket.close()


# ---- 测试入口 ----
if __name__ == "__main__":
    logger = get_logger()

    # 模拟设备 A
    fs_a = FileSharing(logger, config_path="shares.json")
    fs_a.add_shared_dir(os.getcwd())  # 共享当前目录
    threading.Thread(target=start_server, args=(fs_a, 9001), daemon=True).start()

    # 模拟设备 B
    fs_b = FileSharing(logger, config_path="shares.json")
    fs_b.add_shared_dir("C:\\") if os.name == "nt" else fs_b.add_shared_dir("/")  # 共享根目录
    threading.Thread(target=start_server, args=(fs_b, 9002), daemon=True).start()

    time.sleep(1)  # 等待服务启动


    fs_a.add_peer_share({
        "device": "B",
        "address": "localhost",
        "port": 9002,
    })
    fs_b.add_peer_share({
        "device": "A",
        "address": "localhost",
        "port": 9001,
    })
    time.sleep(0.2)

    print("\n--- 从 A 请求 B 的 root 目录 ---")
    try:
        result_a_to_b = fs_a.list_peer_dir("B", "C:\\Program Files (x86)")
        for item in result_a_to_b:
            print("  ·", item)
    except Exception as e:
        print(f"Error in fs_a.list_peer_dir('B','root'): {e}")
