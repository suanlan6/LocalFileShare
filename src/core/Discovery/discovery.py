# 设备发现与管理(分组选举)
import socket
import threading
import time
import random
import json
from typing import Dict, List, Tuple, Optional

from src.utils.logger import _logger


class Discovery:
    def __init__(self, device_ip: str, is_supernode_candidate: bool = False):
        """
        初始化发现服务
        :param device_ip: 本设备IP地址
        :param is_supernode_candidate: 是否可作为超级节点候选
        """
        self.device_ip = device_ip
        self.is_supernode = False
        self.supernodes: List[str] = []  # 已知超级节点列表
        self.device_cache: Dict[str, float] = {}  # 设备缓存 {ip: 最后活跃时间}
        self.heartbeat_target: Optional[str] = None  # 当前心跳目标超级节点

        # 网络配置
        self.multicast_group = "239.255.0.1"
        self.multicast_port = 5353
        self.unicast_port = 5354

        # 状态控制
        self.running = False
        self.threads: List[threading.Thread] = []

        # 如果是候选节点且符合条件，自动成为超级节点
        if is_supernode_candidate and self._elected_as_supernode():
            self._promote_to_supernode()

    def start(self) -> None:
        """启动发现服务"""
        if self.running:
            return

        self.running = True

        # 启动组播监听线程
        multicast_thread = threading.Thread(target=self._listen_multicast)
        multicast_thread.daemon = True
        self.threads.append(multicast_thread)

        # 启动单播监听线程
        unicast_thread = threading.Thread(target=self._listen_unicast)
        unicast_thread.daemon = True
        self.threads.append(unicast_thread)

        # 启动心跳线程
        heartbeat_thread = threading.Thread(target=self._heartbeat_loop)
        heartbeat_thread.daemon = True
        self.threads.append(heartbeat_thread)

        # 启动离线检测线程（仅超级节点）
        if self.is_supernode:
            cleanup_thread = threading.Thread(target=self._cleanup_offline_devices)
            cleanup_thread.daemon = True
            self.threads.append(cleanup_thread)

        for t in self.threads:
            t.start()

        # 新设备加入网络
        self.join_network()

    def stop(self) -> None:
        """停止发现服务"""
        self.running = False
        # 发送下线通知
        self.leave_network()

    def join_network(self) -> None:
        """新设备加入网络流程"""
        # 发送组播发现请求
        self._send_multicast("DISCOVERY_REQUEST")

    def leave_network(self) -> None:
        """设备离开网络"""
        if self.is_supernode:
            # 超级节点下线前转移职责
            self._transfer_supernode_duty()
        else:
            # 普通设备发送下线通知
            self._notify_offline(self.device_ip)

    def get_online_devices(self) -> List[str]:
        """
        获取当前在线设备列表
        :return: 在线设备IP列表
        """
        now = time.time()
        return [
            ip for ip, last_seen in self.device_cache.items() if now - last_seen < 600
        ]  # 10分钟内活跃

    def _elected_as_supernode(self) -> bool:
        """检查是否被选为超级节点（简化选举逻辑）"""
        # 实际实现应基于IP/MAC等属性进行选举
        return random.random() < 0.05  # 5%概率当选

    def _promote_to_supernode(self) -> None:
        """提升为超级节点"""
        self.is_supernode = True
        _logger.info(f"[SUPERNODE] {self.device_ip} promoted to supernode")

    def _send_multicast(self, message_type: str, payload: dict = None) -> None:
        """发送组播消息"""
        # 实现组播发送逻辑
        pass

    def _send_unicast(self, target_ip: str, message: dict) -> None:
        """发送单播消息"""
        # 实现单播发送逻辑
        pass

    def _listen_multicast(self) -> None:
        """监听组播消息"""
        while self.running:
            # 实现组播接收逻辑
            # 处理 DISCOVERY_REQUEST 等消息
            pass

    def _listen_unicast(self) -> None:
        """监听单播消息"""
        while self.running:
            # 实现单播接收逻辑
            # 处理 HEARTBEAT, FULL_LIST_REQUEST 等消息
            pass

    def _heartbeat_loop(self) -> None:
        """心跳循环（普通设备）"""
        while self.running and not self.is_supernode:
            if self.heartbeat_target:
                self._send_heartbeat()
            time.sleep(300)  # 5分钟心跳间隔

    def _send_heartbeat(self) -> None:
        """发送心跳到超级节点"""
        self._send_unicast(
            self.heartbeat_target, {"type": "HEARTBEAT", "source": self.device_ip}
        )

    def _handle_heartbeat(self, source_ip: str) -> None:
        """处理心跳（超级节点）"""
        if self.is_supernode:
            self.device_cache[source_ip] = time.time()

    def _handle_discovery_request(self, source_ip: str) -> None:
        """
        处理发现请求
        :param source_ip: 请求来源IP
        """
        # 30%概率响应
        if random.random() < 0.3:
            response = {
                "type": "DISCOVERY_RESPONSE",
                "supernodes": self.supernodes,
                "self": self.device_ip,
            }
            self._send_unicast(source_ip, response)

    def _request_full_list(self) -> None:
        """向超级节点请求完整设备列表"""
        if self.supernodes:
            target = random.choice(self.supernodes)
            self._send_unicast(target, {"type": "FULL_LIST_REQUEST"})

    def _handle_full_list_request(self, source_ip: str) -> None:
        """处理全量列表请求（超级节点）"""
        if self.is_supernode:
            response = {
                "type": "FULL_LIST_RESPONSE",
                "devices": list(self.device_cache.keys()),
            }
            self._send_unicast(source_ip, response)

    def _cleanup_offline_devices(self) -> None:
        """清理离线设备（超级节点定时任务）"""
        while self.running and self.is_supernode:
            now = time.time()
            offline_devices = []

            for ip, last_seen in self.device_cache.items():
                if now - last_seen > 600:  # 10分钟无心跳
                    offline_devices.append(ip)

            for ip in offline_devices:
                self._notify_offline(ip)
                del self.device_cache[ip]

            time.sleep(60)  # 每分钟检查一次

    def _notify_offline(self, device_ip: str) -> None:
        """通知设备离线"""
        if self.is_supernode:
            # 广播离线通知
            self._send_multicast("DEVICE_OFFLINE", {"ip": device_ip})
            _logger.info(f"[OFFLINE] Device {device_ip} marked offline")

    def _transfer_supernode_duty(self) -> None:
        """转移超级节点职责"""
        # 在实际实现中，应选择新的超级节点并同步状态
        pass


# 使用示例
if __name__ == "__main__":
    # 获取本机IP（简化实现）
    local_ip = "192.168.1.100"

    # 初始化发现服务（5%概率成为超级节点候选）
    discovery = Discovery(local_ip, is_supernode_candidate=True)

    try:
        discovery.start()
        _logger.info("Discovery service started")

        # 模拟主程序运行
        while True:
            # 每30秒打印一次在线设备
            _logger.info("Online devices: %s", discovery.get_online_devices())
            time.sleep(30)

    except KeyboardInterrupt:
        discovery.stop()
        _logger.info("Discovery service stopped")
