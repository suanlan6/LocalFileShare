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

    def __init__(self, backendConnect):
        print("FileController init")
        device = Device(device_name=get_device_name(), host_ip=get_local_ip())
        self.backendConnect = backendConnect
        # device = Device(
        #     device_id="device1",
        #     device_name="device1",
        #     host_ip=get_local_ip(),
        #     conn_port=19998,
        #     transfer_port=19999,
        # )
        self.share_manager = ShareManager(device, self.backendConnect)
        # self.share_manager._devices["device2"] = Device(
        #     device_id="device2",
        #     device_name="device2",
        #     host_ip="192.168.5.4",
        #     conn_port=19998,
        #     transfer_port=19999,
        # )

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
        result = self.share_manager.get_self_sharing_directory(directory=base_path)
        return result

    async def get_peer_file_info(
        self, device_id: str, path: str = None
    ) -> list[FileInfo]:
        base_path = path if path else "/"
        if device_id == "":
            return []
        # sample_types = [ShareType.FILE, ShareType.FOLDER, ShareType.PICTURE]
        # infos = []

        # nun = random.randint(6, 10)
        # for i in range(10):
        #     info = FileInfo(
        #         name=f"Item_{i}",
        #         size=random.randint(1000, 1000000),
        #         path=f"{random.randint(1,1000)}/Item_{i}",
        #         host="127.0.0.1:8000",
        #         file_type=random.choice(sample_types),
        #     )
        #     infos.append(info)
        # return infos
        return await self.share_manager.get_remote_shared_file(
            device_id, bindParam={"directory": base_path}
        )

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
        result = {}
        for device_id, file_infos in self.share_manager.transfers.items():
            result[device_id] = {}
            for file_id, file in file_infos.items():
                if (
                    file["status"] == TransferStatus.RUNNING
                    or file["status"] == TransferStatus.PAUSED
                ):
                    result[device_id][file_id] = file
        return result

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
        result = {}
        for device_id, file_infos in self.share_manager.upload_by_other.items():
            result[device_id] = {}
            for file_id, file in file_infos.items():
                if (
                    file["status"] == TransferStatus.RUNNING
                    or file["status"] == TransferStatus.PAUSED
                ):
                    result[device_id][file_id] = file
        return result

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
        result = {}
        for device_id, file_infos in self.share_manager.downloads.items():
            result[device_id] = {}
            for file_id, file in file_infos.items():
                if (
                    file["status"] == TransferStatus.RUNNING
                    or file["status"] == TransferStatus.PAUSED
                ):
                    result[device_id][file_id] = file
        return result

    # 拖拽触发的发送和接收事件
    async def sending(
        self, device_id: str, type: ShareType, dst_path: str, info: list[FileInfo]
    ):
        await self.share_manager.sendFile(
            device_id=device_id,
            type=type,
            dst_path=dst_path,
            files=info,
        )

    async def receiving(
        self, device_id: str, type: ShareType, dst_path: str, info: list[FileInfo]
    ):
        await self.share_manager.downloadFile(
            device_id=device_id,
            type=type,
            dst_path=dst_path,
            files=info,
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
        self.share_manager.startScan()
        return [device for device in self.share_manager._devices.values()]

    async def request_connection(
        self, device_id: str, bindParam: dict
    ) -> Dict[str, Any]:
        """
        请求连接到指定设备
        :param device: 设备标识符（IP或设备ID）
        """
        return await self.share_manager.pre_connect(device_id, bindParam)

    async def sendCode(self, device_id: str, bindParam: dict) -> Dict[str, Any]:
        # print(f"sendCode {code}")
        # return True
        _logger.info(f"sendCode {device_id} {bindParam}")
        return await self.share_manager.connect(device_id, bindParam)

    def submitConnect(self, bind_param: dict) -> None:
        # print(f"submitConnect {ip}")
        self.share_manager.handle_connect_latter(
            self.share_manager.bindDevice.device_id, bind_param
        )

    def stop_continue(self, device_id: str, file_id: str):

        # print(f"stop_continue {data}")
        # print("flag:", flag)
        # self.share_manager.pause_upload_client(device_id, file_id)
        pass

    async def pause_client_upload_task(self, device_id: str, file_id: str):
        """
        暂停上传任务
        :param device_id: 设备ID
        :param file_id: 文件ID
        """
        # print(f"pause {device_id} {file_id}")
        await self.share_manager.pause_upload_client(device_id, file_id)

    async def resume_client_upload_task(self, device_id: str, file_id: str):
        """
        恢复上传任务
        :param device_id: 设备ID
        :param file_id: 文件ID
        """
        # print(f"resume {device_id} {file_id}")
        await self.share_manager.resume_upload_client(device_id, file_id)

    async def pause_client_download_task(self, device_id: str, file_id: str):
        """
        暂停下载任务
        :param device_id: 设备ID
        :param file_id: 文件ID
        """
        # print(f"pause {device_id} {file_id}")
        await self.share_manager.pause_download(device_id, file_id)

    async def resume_client_download_task(self, device_id: str, file_id: str):
        """
        恢复下载任务
        :param device_id: 设备ID
        :param file_id: 文件ID
        """
        # print(f"resume {device_id} {file_id}")
        await self.share_manager.resume_download(device_id, file_id)

    async def delete_client_upload_task(self, device_id: str, file_id: list[str]):
        await self.share_manager.client_cancel_transfer(device_id, file_id)

    async def delete_server_upload_task(self, device_id: str, file_id: list[str]):
        # print(f"delete_server_upload_task {data}")
        await self.share_manager.server_cancel_transfer(device_id, file_id)

    async def delete_client_download_task(self, device_id: str, file_id: list[str]):
        # print(f"delete_client_download_task {data}")
        await self.share_manager.client_cancel_download(device_id, file_id)

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

    def get_connections(self):
        return self.share_manager.get_connections()