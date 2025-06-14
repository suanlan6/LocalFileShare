import asyncio
from os import path
import random
from itertools import count

from typing import Dict, Any

from src.common.fileConf import FileInfo, ShareType
from src.common.device import Device
from src.core.transfer.transfer_config import TransferStatus
from src.core.share_manager import ShareManager
from src.utils.system_utils import get_device_name, get_local_ip
from src.utils.logger import _logger


class FileController:

    def __init__(self):
        print("FileController init")
        device = Device(device_name=get_device_name(), host_ip=get_local_ip())
        self.share_manager = ShareManager(device)

    async def start_server(self):
        await self.share_manager.start_servers()

    async def stop_server(self):
        await self.share_manager.stop_servers()

    def get_local_file_info(self, path: str = None) -> list[FileInfo]:
        # 模拟数据：若 parent_file_info 存在，则路径为其路径下的子路径
        base_path = path if path else "/"

        return self.share_manager.get_local_directory(directory=base_path)

    def get_sharing_file_info(self, path: str = None) -> list[FileInfo]:
        # 模拟数据：若 parent_file_info 存在，则路径为其路径下的子路径

        # TODO: FIX THE PARAMS
        base_path = path if path else "/"

        return self.share_manager.get_self_sharing_directory(directory=base_path)

    def get_peer_file_info(self, device: str, path: str = None) -> list[FileInfo]:
        base_path = path if path else "/"
        if device == "":
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
                file_type=random.choice(sample_types),
            )
            infos.append(info)
        return infos

    def get_fromSendingData_data(self):
        # mock_data = {}
        # device_count = 2
        # files_per_device = 5
        # file_sizes = ["128 KB", "512 KB", "1.2 MB", "2.5 MB", "5.0 MB"]

        # for device_index in range(device_count):
        #     device_id = f"device_{device_index + 1:03d}"
        #     mock_data[device_id] = {}

        #     for file_index in range(files_per_device):
        #         file_id = f"file_{file_index + 1}"
        #         filename = f"文件{file_index + 1}_{device_id}.txt"
        #         size = random.choice(file_sizes)
        #         progress_value = round(random.uniform(0, 100), 2)
        #         status = random.choice([TransferStatus.RUNNING, TransferStatus.PAUSED])
        #         mock_data[device_id][file_id] = {
        #             "filename": filename,
        #             "size": size,
        #             "progress_value": progress_value,
        #             "status": status,
        #         }
        # return mock_data
        return self.share_manager.transfers

    def get_toSendingData_list_data(self):
        # mock_data = {}
        # device_count = 2
        # files_per_device = 5
        # file_sizes = ["128 KB", "512 KB", "1.2 MB", "2.5 MB", "5.0 MB"]

        # for device_index in range(device_count):
        #     device_id = f"device_{device_index + 1:03d}"
        #     mock_data[device_id] = {}

        #     for file_index in range(files_per_device):
        #         file_id = f"file_{file_index + 1}"
        #         filename = f"文件{file_index + 1}_{device_id}.txt"
        #         size = random.choice(file_sizes)
        #         progress_value = round(random.uniform(0, 100), 2)
        #         status = random.choice([TransferStatus.RUNNING, TransferStatus.PAUSED])
        #         mock_data[device_id][file_id] = {
        #             "filename": filename,
        #             "size": size,
        #             "progress_value": progress_value,
        #             "status": status,
        #         }

        # return mock_data
        return self.share_manager.upload_by_other

    def get_ReceivingData_list_data(self):
        # mock_data = {}
        # device_count = 2
        # files_per_device = 5
        # file_sizes = ["128 KB", "512 KB", "1.2 MB", "2.5 MB", "5.0 MB"]

        # for device_index in range(device_count):
        #     device_id = f"device_{device_index + 1:03d}"
        #     mock_data[device_id] = {}

        #     for file_index in range(files_per_device):
        #         file_id = f"file_{file_index + 1}"
        #         filename = f"文件{file_index + 1}_{device_id}.txt"
        #         size = random.choice(file_sizes)
        #         progress_value = round(random.uniform(0, 100), 2)
        #         status = random.choice([TransferStatus.RUNNING, TransferStatus.PAUSED])
        #         mock_data[device_id][file_id] = {
        #             "filename": filename,
        #             "size": size,
        #             "progress_value": progress_value,
        #             "status": status,
        #         }
        # return mock_data
        return self.share_manager.downloads

    # 拖拽触发的发送和接收事件
    async def sending(self, device: str, path: str, info: FileInfo):
        await self.share_manager.sendFile(
            device=device,
            path=path,
            file_info=info,
        )

    async def receiving(self, device, path: str, info: FileInfo):
        await self.share_manager.downloadFile(
            device=device,
            path=path,
            file_info=info,
        )

    def get_peer_data(self):
        # count = 5
        # choices = [
        #     lambda: f"192.168.0.{random.randint(1, 254)}",
        #     lambda: f"10.0.0.{random.randint(1, 254)}",
        #     lambda: f"172.16.{random.randint(0, 31)}.{random.randint(1, 254)}",
        #     lambda: "127.0.0.1",
        # ]
        # return random.sample([f() for f in random.choices(choices, k=count)], k=count)
        return [device for device in self.share_manager._devices]

    async def request_connection(
        self, device_id: str, bindParam: dict
    ) -> Dict[str, Any]:
        """
        请求连接到指定设备
        :param device: 设备标识符（IP或设备ID）
        """
        return await self.share_manager.pre_connect(device_id, bindParam)

    def sendCode(self, code: int) -> bool:
        # print(f"sendCode {code}")
        # return True
        self.share_manager.connect(code)

    def submitConnect(self, ip: str) -> None:
        print(f"submitConnect {ip}")

    def stop_continue(self, data, flag: int):

        print(f"stop_continue {data}")
        print("flag:", flag)

    def delete_task(self, data):
        print(f"delete_task {data}")

    def set_sharing_file(self, file_info: FileInfo):
        """
        设置文件共享
        :param file_info: 文件信息
        """
        print(f"set_sharing_file {file_info}")
        self.share_manager.set_shared_directory(file_info.path)

    def delete_sharing_file(self, file_info: FileInfo):
        """
        删除文件共享
        :param file_info: 文件信息
        """
        # _logger.info(f"delete_sharing_file {file_info}")
        self.share_manager.cancel_shared_directory(file_info.path)
