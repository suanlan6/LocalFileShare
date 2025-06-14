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


# 示例用法
if __name__ == "__main__":
    print(get_device_name())
