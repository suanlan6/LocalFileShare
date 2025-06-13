# 🔌 AutoMeshLAN - 自动演化的局域网设备管理系统

AutoMeshLAN 是一个自组织的设备发现与管理系统，专为局域网环境设计。所有节点以子节点身份启动，自动尝试加入现有超级节点组；若未能加入则自动晋升为超级节点，并允许其他设备加入其管理域。

---

## ✨ 功能特点

- 🌐 **自动发现与组建网络**：节点启动后广播寻找可加入的超级节点。
- 🧠 **智能角色演化**：若未找到超级节点，节点将自动晋升为超级节点。
- 🔁 **动态成员同步**：超级节点之间自动同步全局视图。
- 💓 **心跳监测与掉线处理**：子节点定时发送心跳，掉线节点自动剔除。
- 📡 **UDP 广播 & TCP 同步结合**：UDP 发现，TCP 确保数据一致。
- 🛠 **自动命名与端口分配**：无需配置，系统自动生成。
- 📦 **统一设备视图查询接口**：所有节点都可通过 `get_all_device_info()` 获取全局设备信息，角色透明。

---

## 🗂️ 项目结构

```
📁 DIscoverySystem/
│
├── main.py              # 主入口，统一启动流程
├── device.py            # Device类定义，封装节点元数据
├── device_start.py      # 节点启动器（广播、晋升逻辑）
├── child_node.py        # 子节点逻辑（接收邀请、心跳发送）
├── super_node.py        # 超级节点逻辑（组管理、视图同步）
├── lan_comm.py          # 网络通信模块（UDP广播、TCP推送）
├── device_utils.py      # ✅ 全局视图获取函数等通用工具
└── README.md
```

---

## 🚀 启动方式

### 环境要求

- Python 3.8+
- 同一局域网

### 启动命令

```bash
python main.py
```

你将被要求输入设备名，系统将自动广播尝试加入网络：

- 加入成功 → 成为子节点；
- 超时未成功 → 自动晋升为超级节点；
- 全过程对用户透明。

---

## 💻 示例主程序调用

```python
from device import Device
from device_start import node_start, get_all_device_info

name = input("请输入设备名称: ").strip()
device = Device(device_name=name)

node_start(device)  # 自动广播加入或晋升

while True:
    time.sleep(15)
    devices = get_all_device_info(device)
    for dev_id, info in devices.items():
        print(f"{dev_id} → {info}")
```

---

## 🔧 模块说明

### `device.py`

```python
class Device:
    device_id       # UUID 唯一标识
    device_name     # 用户输入名称
    device_type     # 用户自定义类型（可选）
    host_ip         # 本机局域网地址
    conn_port       # 自动分配的监听端口
    is_super_node   # 是否为超级节点
    super_ip        # 所属超级节点IP（子节点）
    super_port      # 所属超级节点端口
```

### `device_utils.py`

```python
get_all_device_info(self_device)
```

该函数统一提供当前网络中的**全部设备视图**，自动判断当前节点角色并选择数据来源（子节点→请求超级节点，超级节点→汇总本地数据）。

---

## 📦 `get_all_device_info()` 返回结构示例

```python
{
  "b4ae9893-2cd4-4f7d-83b4-5051620b8306": {
    "device_id": "b4ae9893-...",
    "device_name": "Node-b4J432",
    "device_type": "printer",
    "host_ip": "10.20.0.180",
    "conn_port": 14363,
    "transfer_port": 0,
    "is_super_node": False,
    "super_node_id": "Node-A123",
    "super_ip": "10.20.0.1",
    "super_port": 8888
  },
  ...
}
```

---

## 🔄 状态同步机制

| 来源 | 目标 | 协议 | 内容 |
|------|------|------|------|
| 子节点 → 超级节点 | UDP 广播 | `HELLO` |
| 超级节点 → 子节点 | TCP | `NEW_MEMBER`, `JOIN_ACK` |
| 子节点 → 超级节点 | TCP | `JOIN_CONFIRM` |
| 子节点 → 超级节点 | UDP | `HEARTBEAT` |
| 超级节点 → 子节点 | TCP | `GLOBAL_VIEW_SYNC`, `NEW_MEMBER_SYNC` |
| 超级节点 → 超级节点 | UDP | `SUPERNODE_HELLO`（带子节点信息）|

---

## 📌 已实现特性

- ✅ 节点角色自动演化（子节点/超级节点转换）
- ✅ 多超级节点全网视图共享
- ✅ 丢包掉线自动修复与剔除
- ✅ 模块间状态共享（引用同步）
- ✅ 多线程安全处理（心跳、输入、通信）

---

## 🧩 可扩展方向

- ✅ 节点日志记录（上线、离线）
- ✅ 多网段桥接、转发支持
- ✅ 文件共享、服务推送模块
- ✅ 图形化可视界面（Web / Tkinter）
- ✅ 加密身份验证支持

---

## 📄 License

MIT License © 2025