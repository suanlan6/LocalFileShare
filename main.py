import socket
import time
from device import Device
import child_node  # ✅ 修改：统一引用整个模块
from lan_comm import (
    start_hello_broadcast,
    stop_hello_broadcast
)
from super_node import SuperNode
import uuid

def generate_unique_name(prefix="Node"):
    return f"{prefix}-{uuid.uuid4().hex[:6]}"  # 例如 Node-a1b2c3


def find_free_port():
    """从系统动态获取一个空闲端口"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def main():
    # 分配空闲端口并创建本机设备对象
    port = find_free_port()
    device_name = generate_unique_name()
    device = Device(device_name=device_name, conn_port=port)

    print(f"🚀 启动设备：{device.device_name} @ {device.host_ip}:{device.conn_port}")

    # Step 1: 启动广播 & 子节点监听
    start_hello_broadcast(device, lambda: not child_node.joined)
    child_node.listen_super_node(device)

    # Step 2: 等待加入超级节点
    wait_time = 5
    print(f"⏳ 等待加入超级节点（最多 {wait_time}s）...")
    child_node.join_event.wait(timeout=wait_time)
    stop_hello_broadcast()
    #等待之前的hello流程走完
    time.sleep(3)

    print("main joined:", child_node.joined)
    if not child_node.joined:
        child_node.reset_child_node_state()  # ✅ 清理子节点所有线程与状态
        print("⚠️ 未能加入任何超级节点 → 自动晋升为超级节点")
        time.sleep(0.5)  # 等待 socket 彻底释放

        # ⚠️ 使用新的空闲端口，避免和子节点冲突
        new_port = find_free_port()
        device.conn_port = new_port

        print(f"🔁 分配新端口用于超级节点：{new_port}")
        super_node = SuperNode(device)
        super_node.start()

    else:
        # Step 4: 成功加入 → 开启子节点输入命令监听
        print("✅ 成功加入某个超级节点，继续作为子节点运行")
        child_node.start_input_command_listener(device)

    # Step 5: 阻止主线程退出
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 程序已退出")


if __name__ == "__main__":
    main()
