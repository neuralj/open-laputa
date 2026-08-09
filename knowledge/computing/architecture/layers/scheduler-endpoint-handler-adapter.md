---
type: layer
domain: computing
subdomain: architecture
---

# Scheduler + Endpoint → Handler → Adapter

## 适用场景

- AI Agent 守护进程（监听事件 + 定时清理/探测）
- Sidecar 控制器（监听 API 限流 + 定时恢复 session）
- 监控 daemon（接收告警 + 定时健康检查）
- 消息队列消费者（被动消费 + 主动重试）
- 支持 TypeScript/Go/Python 三语言

## 目录结构

```
scheduler/  # 定时触发层：周期性主动任务
endpoints/  # 事件响应层：被动事件接收
handlers/   # 编排层（共享）：业务逻辑编排
adapters/   # 执行层（共享）：外部系统交互
```

## 层职责

- **Scheduler 层**：系统的"闹钟"，定时触发主动任务（轮询、清理、心跳）
- **Endpoint 层**：系统与外部世界的"触角"，接收事件（SSE、Webhook、插件回调）
- **Handler 层**：Daemon 的"大脑"，编排业务逻辑，调度多个 Adapter，状态管理
- **Adapter 层**：系统与外部基础设施的"手脚"，每个 Adapter 执行独立的 I/O 操作

## 双驱动模型

- **Scheduler 驱动**：定时任务（轮询 API 状态、清理过期数据、心跳检测）
- **Endpoint 驱动**：事件响应（SSE 事件、Webhook 回调、插件通知）
- **共享 Handler**：两种驱动最终都进入 Handler 层，复用业务逻辑
- **共享 Adapter**：Handler 调用 Adapter 执行外部操作
- Handler 不区分事件来源（Scheduler 或 Endpoint），只关心业务逻辑

## 目录组织

> **adapters/ 是 Unit 的集合**，内部组织方式由项目规模决定，不强制统一。

### 方案 A：扁平结构（小型项目）

```
scheduler/
endpoints/
handlers/
adapters/
  ├── postgres.go
  ├── redis.go
  └── http_client.go
```

### 方案 B：按职责分组（中型项目）

```
scheduler/
endpoints/
handlers/
adapters/
  ├── database/
  ├── messaging/
  └── external/
```

### 方案 C：按业务域分组（大型项目）

```
scheduler/
endpoints/
handlers/
adapters/
  ├── user/
  ├── order/
  └── notification/
```

## 铁律清单

1. 调用链严格遵循 Scheduler/Endpoint → Handler → Adapter，无跨层调用
2. Scheduler 只触发定时任务，Endpoint 只接收和脱壳事件
3. Handler 不区分事件来源（Scheduler 或 Endpoint），只关心业务逻辑
4. Endpoint 实现异步非阻塞响应
5. Handler 包含单次任务异常隔离舱
6. Adapter 封装外部交互的所有超时和重试逻辑
7. 不存在全局可变状态
8. 不存在硬编码的密钥或网络地址
9. Handler 不直接执行 I/O，Adapter 不感知业务流程
10. Logger 统一：入口创建，下层通过参数获取

## 新增功能时的操作指引

1. 判断驱动方式：定时任务 → `scheduler/`；事件响应 → `endpoints/`
2. 在 `handlers/` 层创建或修改 Handler，编排 Adapter 调用
3. 在 `adapters/` 层添加 Adapter
