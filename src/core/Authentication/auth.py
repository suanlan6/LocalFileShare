import asyncio
import aiohttp
import time
import uuid
from typing import Any, Dict, Tuple

import src.core.Authentication.auth_utils as auth_utils
from src.common.device import Device
from src.utils.logger import _logger


class Authentication:
    def __init__(self):
        self._sessions = {}  # session_id -> {pin, from_device_id, expire_at, verified}

    async def should_accept_connection(
        self, from_device_id: str, bind_param: dict
    ) -> bool:
        # 调用UI弹窗或规则逻辑，是否接受连接
        # TODO(仅供测试使用，实际应调用UI或规则逻辑):
        return True

    async def pre_connect(
        self, from_device: Device, to_device: Device, bind_param: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        预连接阶段，进行一些必要的准备工作。
        """
        connect_url = f"http://{to_device.host_ip}:{to_device.conn_port}/connect"
        payload = {
            "fromDeviceId": from_device.device_id,
            "bindParam": {
                **bind_param,
                "host": from_device.host_ip,
                "port": from_device.conn_port,
            },
        }

        async with aiohttp.ClientSession() as session:
            # 发起连接请求
            async with session.post(connect_url, json=payload, timeout=60) as resp:
                if resp.status != 200:
                    return {
                        "status": "error",
                        "message": f"HTTP {resp.status}: {await resp.text()}",
                    }
                data = await resp.json()
                _logger.info(f"Received connect response: {data}")
        return {
            "status": "success",
            "session_id": data["session_id"],
            "pin_code": data["pin"],
        }
        #         session_id = data["session_id"]
        #         pin_code = data["pin"]
        # return {
        #     "status": "success",
        #     "message": "success",
        #     "session_id": session_id,
        #     "pin_code": pin_code,
        # }

    async def authenticate(
        self,
        from_device: Device,
        to_device: Device,
        bind_param: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        完整认证流程（发起连接请求、接收 PIN、输入 PIN、等待验证、完成连接）。
        Returns:
            {"token": str, "transfer_port": int}
        Raises:
            Exception: 若认证失败
        """

        # expire_seconds = data["expire_seconds"]

        # 提示用户输入 PIN（可以换成自动确认）
        # user_pin = await self.prompt_pin_input(pin_code, timeout=120)

        # 向目标设备发送 PIN 校验请求
        verify_url = f"http://{to_device.host_ip}:{to_device.conn_port}/verify_pin"
        try:
            verify_payload = {
                "session_id": bind_param["session_id"],
                "pin": bind_param["pin_code"],
                "fromDeviceId": from_device.device_id,
                "host": from_device.host_ip,
                "port": from_device.transfer_port,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    verify_url, json=verify_payload, timeout=5
                ) as resp:
                    if resp.status != 200:
                        raise Exception(f"PIN verification failed: HTTP {resp.status}")
                    verify_data = await resp.json()
        except Exception as e:
            _logger.error(f"Authentication error: {e}")
            return {"status": "error", "message": str(e)}

        return {
            "status": "success",
            "token": verify_data["token"],
            "port": verify_data["transfer_port"],
        }

    async def prompt_pin_input(self, pin: str, timeout: int) -> str:
        """
        提示用户输入 PIN（真实场景应为 UI 确认或 CLI 输入）。
        这里为了演示可自动填入。
        """
        # TODO: 你可以替换为 UI 弹窗、console 输入、WebSocket 等方式
        _logger.info(f"请确认PIN码: {pin}")
        await asyncio.sleep(1)  # 模拟用户等待或输入
        return pin  # 自动确认

    def generate_pin(
        self, from_device_id: str, expire_seconds: int = 120
    ) -> Tuple[str, str]:
        pin = auth_utils.generate_pin()
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            "from_device_id": from_device_id,
            "pin": pin,
            "expire_at": time.time() + expire_seconds,
            "verified": False,
        }
        return pin, session_id

    def verify_pin(self, session_id: str, pin: str) -> bool:
        session = self._sessions.get(session_id)
        if not session:
            return False
        if time.time() > session["expire_at"]:
            del self._sessions[session_id]
            return False
        if pin != session["pin"]:
            return False
        session["verified"] = True
        return True

    def finalize_connection(self, transfer_port: str) -> Tuple[str, int]:
        # 生成 token 与返回 transfer_port，确保已验证（目前仅测试使用，后期完善校验）
        token = "example_token"  # 示例值，实际应生成真实的 token
        return token, transfer_port
