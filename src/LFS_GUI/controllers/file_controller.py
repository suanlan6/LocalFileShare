import random
from itertools import count

from src.common.fileConf import FileInfo, ShareType
from src.core.transfer.transfer_config import TransferStatus


class FileController:

    def __init__(self):
        print("FileController init")


    def get_local_file_info(self, path: str = None) -> list[FileInfo]:
        # 模拟数据：若 parent_file_info 存在，则路径为其路径下的子路径
        base_path = path if path else "/"
        sample_types = [ShareType.FILE, ShareType.FOLDER, ShareType.PICTURE]
        infos = []

        nun = random.randint(6, 10)
        for i in range(10):
            info = FileInfo(
                name=f"Item_{i}",
                size=random.randint(1000, 1000000),
                path=f"{random.randint(1,1000)}/Item_{i}",
                host="127.0.0.1:8000",
                file_type=random.choice(sample_types)
            )
            infos.append(info)
        return infos

    def get_sharing_file_info(self, path: str = None) -> list[FileInfo]:
        # 模拟数据：若 parent_file_info 存在，则路径为其路径下的子路径
        base_path = path if path else "/"
        sample_types = [ShareType.FILE, ShareType.FOLDER, ShareType.PICTURE]
        infos = []

        nun = random.randint(6, 10)
        for i in range(10):
            info = FileInfo(
                name=f"Item_{i}",
                size=random.randint(1000, 1000000),
                path=f"{random.randint(1,1000)}/Item_{i}",
                host="127.0.0.1:8000",
                file_type=random.choice(sample_types)
            )
            infos.append(info)
        return infos

    def get_peer_file_info(self,device:str ,path: str = None) -> list[FileInfo]:
        base_path = path if path else "/"
        if device == '':
            return []
        sample_types = [ShareType.FILE, ShareType.FOLDER, ShareType.PICTURE]
        infos = []

        nun = random.randint(6, 10)
        for i in range(10):
            info = FileInfo(
                name=f"Item_{i}",
                size=random.randint(1000, 1000000),
                path=f"{random.randint(1,1000)}/Item_{i}",
                host="127.0.0.1:8000",
                file_type=random.choice(sample_types)
            )
            infos.append(info)
        return infos

    def get_fromSendingData_data(self):
        mock_data = {}
        device_count = 2
        files_per_device = 5
        file_sizes = ["128 KB", "512 KB", "1.2 MB", "2.5 MB", "5.0 MB"]

        for device_index in range(device_count):
            device_id = f"device_{device_index + 1:03d}"
            mock_data[device_id] = {}

            for file_index in range(files_per_device):
                file_id = f"file_{file_index + 1}"
                filename = f"文件{file_index + 1}_{device_id}.txt"
                size = random.choice(file_sizes)
                progress_value = round(random.uniform(0, 100), 2)
                status = random.choice([TransferStatus.RUNNING, TransferStatus.PAUSED])
                mock_data[device_id][file_id] = {
                    "filename": filename,
                    "size": size,
                    "progress_value": progress_value,
                    "status":status
                }
        return mock_data

    def get_toSendingData_list_data(self):
        mock_data = {}
        device_count = 2
        files_per_device = 5
        file_sizes = ["128 KB", "512 KB", "1.2 MB", "2.5 MB", "5.0 MB"]

        for device_index in range(device_count):
            device_id = f"device_{device_index + 1:03d}"
            mock_data[device_id] = {}

            for file_index in range(files_per_device):
                file_id = f"file_{file_index + 1}"
                filename = f"文件{file_index + 1}_{device_id}.txt"
                size = random.choice(file_sizes)
                progress_value = round(random.uniform(0, 100), 2)
                status = random.choice([TransferStatus.RUNNING, TransferStatus.PAUSED])
                mock_data[device_id][file_id] = {
                    "filename": filename,
                    "size": size,
                    "progress_value": progress_value,
                    "status":status
                }

        return mock_data

    def get_ReceivingData_list_data(self):
        mock_data = {}
        device_count = 2
        files_per_device = 5
        file_sizes = ["128 KB", "512 KB", "1.2 MB", "2.5 MB", "5.0 MB"]

        for device_index in range(device_count):
            device_id = f"device_{device_index + 1:03d}"
            mock_data[device_id] = {}

            for file_index in range(files_per_device):
                file_id = f"file_{file_index + 1}"
                filename = f"文件{file_index + 1}_{device_id}.txt"
                size = random.choice(file_sizes)
                progress_value = round(random.uniform(0, 100), 2)
                status = random.choice([TransferStatus.RUNNING, TransferStatus.PAUSED])
                mock_data[device_id][file_id] = {
                    "filename": filename,
                    "size": size,
                    "progress_value": progress_value,
                    "status":status
                }
        return mock_data


    # 拖拽触发的发送和接收事件
    def sending(self, device:str , path:str, info: FileInfo):
        print(f"sending {device} {path} {info.name}")

    def receiving(self, device, path:str, info: FileInfo):
        print(f"receiving {device} {path} {info.name}")

    def get_peer_data(self):
        count = 5
        choices = [
            lambda: f"192.168.0.{random.randint(1, 254)}",
            lambda: f"10.0.0.{random.randint(1, 254)}",
            lambda: f"172.16.{random.randint(0, 31)}.{random.randint(1, 254)}",
            lambda: "127.0.0.1"
        ]
        return random.sample([f() for f in random.choices(choices, k=count)], k=count)

    def sendCode(self,code:int) -> bool:
        print(f"sendCode {code}")
        return True

    def submitConnect(self,ip:str)->None:
        print(f"submitConnect {ip}")

    def stop_continue(self,data,flag:int):

        print(f"stop_continue {data}")
        print("flag:",flag)

    def delete_task(self,data):
        print(f"delete_task {data}")