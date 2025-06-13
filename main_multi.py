# device_node.py
import sys
from device import Device
from device_start import node_start, get_all_device_info
import time
import json
import threading

if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = input("请输入设备名称: ").strip()

    device = Device(device_name=name)

    t = threading.Thread(target=node_start, args=(device,), daemon=True)
    t.start()

    while True:
        time.sleep(15)
        devices = get_all_device_info(device)
        print(f"\n🛰️ {name} 在线设备总数：{len(devices)}")
