import platform
import socket
import os


def get_device_name():
    # 优先使用 socket 获取主机名
    try:
        hostname = socket.gethostname()
        if hostname:
            return hostname
    except Exception:
        pass

    # 备用：尝试读取环境变量
    for env_var in ["COMPUTERNAME", "HOSTNAME"]:
        name = os.environ.get(env_var)
        if name:
            return name

    # 备用：平台特定方法
    system = platform.system()
    if system == "Darwin":  # macOS
        try:
            import subprocess

            return (
                subprocess.check_output(["scutil", "--get", "ComputerName"])
                .decode()
                .strip()
            )
        except Exception:
            pass

    # 如果都失败，返回未知
    return "UnknownDevice"


def get_local_ip():
    """
    获取本机在局域网中的IP地址（如192.168.x.x或10.x.x.x）。
    """
    try:
        # 连接到一个外部地址（不会真的发送数据），以获得本地IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS，仅用于获取本地IP
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"  # 失败时返回回环地址


# 示例用法
if __name__ == "__main__":
    print(get_device_name())
    print(get_local_ip())
