import json
import time
from device_start import node_start, get_all_device_info
from device import Device

if __name__ == "__main__":
    name = input("请输入设备名称: ").strip()
    device = Device(device_name=name)
    node_start(device)


    #调用get_all_device_info示例
    while True:
        time.sleep(15)
        print("\n🛰️ [定时获取全网设备信息]")

        devices = get_all_device_info(device)
        print(f"✅ 当前在线设备总数：{len(devices)}")

        for dev_id, dev_info in devices.items():
            print(f"\n🆔 设备ID: {dev_id}")
            print(f"📦 设备信息: {json.dumps(dev_info, indent=2, ensure_ascii=False)}")
