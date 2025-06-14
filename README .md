# 🔌 AutoMeshLAN - 自动演化的局域网设备管理系统

AutoMeshLAN 是一个自组织的设备发现与管理系统，专为局域网环境设计。所有节点以子节点身份启动，自动尝试加入现有超级节点组；若未能加入则自动晋升为超级节点，并允许其他设备加入其管理域。

## ✨ 功能特点

- 🌐 **自动发现与组建网络**：子节点启动后通过广播寻找可加入的超级节点。
- 🧠 **智能角色演化**：若未找到超级节点，节点将自动晋升为超级节点。
- 🔁 **动态成员同步**：超级节点之间自动同步全局视图，子节点可随时查看网络结构。
- 💓 **心跳监测与掉线处理**：子节点定时发送心跳，掉线节点自动剔除。
- 📡 **UDP 广播 & TCP 同步结合**：采用 UDP 进行设备发现，TCP 进行可靠信息传输。
- 🛠 **完全自动端口与设备命名**：无需手动分配端口与 ID，系统自适应生成。

## 🗂️ 项目结构

```
📁 DIscoverySystem/
│
├── main.py              # 主入口，统一启动流程
├── device.py            # Device类定义，封装节点元数据
├── child_node.py        # 子节点逻辑（接收邀请、发送心跳、请求全局视图）
├── super_node.py        # 超级节点逻辑（广播、心跳监听、组管理、同步）
├── lan_comm.py          # 广播通信模块（HELLO / SUPERNODE_HELLO）
└── README.md            # 本说明文档
```

## 🚀 启动方式

### 前提依赖

- Python 3.8+
- 局域网环境（允许广播）

### 启动命令

```bash
python main.py
```

每个设备会自动分配端口和名称，作为子节点启动，系统将自动决定其是否成为超级节点。

## 🔧 模块说明

### `main.py`

- 自动端口选择
- 唯一设备名生成（如 `Node-27A5`）
- 启动广播 + 子节点监听
- 超时未加入 → 自动晋升为超级节点

### `device.py`

```python
class Device:
    device_id       # UUID 唯一标识
    device_name     # 系统自动命名（可定制）
    host_ip         # 本机局域网地址
    conn_port       # 监听端口
    ...
```

### `child_node.py`

- 监听超级节点邀请 (`NEW_MEMBER`)
- 向目标节点发送 `JOIN_CONFIRM`
- 接收 `JOIN_ACK` 启动心跳
- 请求 `REQUEST_GLOBAL_VIEW` 以获取全网设备

### `super_node.py`

- 处理 HELLO 请求（决定是否邀请）
- 管理 `pending_invites` / `sub_nodes`
- TCP 接收 `JOIN_CONFIRM` 并回复 `JOIN_ACK`
- 定期发送 `SUPERNODE_HELLO`，同步全局视图
- 自动检测子节点掉线（心跳机制）

### `lan_comm.py`

- `start_hello_broadcast`: 子节点广播
- `broadcast_super_node_hello`: 超级节点广播状态
- `start_super_node_listener`: 所有广播统一入口
- `send_sync_to_child`: TCP 推送（如成员同步）

## 🔍 指令支持

子节点输入 `view` 可查看整个网络中的所有设备：

```
view
→ 🌐 在线设备列表：
 - Node-1234
 - Node-5678
 - Node-89AB
```

超级节点定期输出网络拓扑图，包括其他超级节点信息：

```
🧭 当前所有超级节点视图：
 - [SELF] Node-89AB | 子节点：2/3
   子节点列表：[Node-1234, Node-5678]
 - [Node-ACDF] | 上次看到：5s前
   子节点列表：[Node-EFGH, Node-IJKL]
```

## 🔄 状态同步机制

| 来源 | 目标 | 协议 | 内容 |
|------|------|------|------|
| 子节点 → 超级节点 | UDP 广播 | `HELLO` |
| 超级节点 → 子节点 | TCP 单播 | `NEW_MEMBER` |
| 子节点 → 超级节点 | TCP 确认 | `JOIN_CONFIRM` + `JOIN_ACK` |
| 子节点 → 超级节点 | UDP 心跳 | `HEARTBEAT` |
| 超级节点 → 所有子节点 | TCP 同步 | `NEW_MEMBER_SYNC`、`GLOBAL_VIEW_SYNC` |
| 超级节点 → 其他超级节点 | UDP 广播 | `SUPERNODE_HELLO`（附带子节点名） |

## 📌 设计约束与扩展建议

### 已实现的设计

- 自动设备角色演化
- 线程安全的连接管理（加锁）
- 掉线检测与视图修正
- 多超级节点互知与视图共享

### 后续可拓展

- 支持节点上线/掉线日志记录
- 支持跨网段或多网卡
- 可视化界面（Web 或桌面）
- 数据转发/文件传输模块
- 加密/身份认证机制

## 📄 License

MIT License © 2025
