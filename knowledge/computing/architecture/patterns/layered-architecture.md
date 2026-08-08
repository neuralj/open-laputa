---
type: pattern
domain: computing
subdomain: architecture
---

# 分层架构模式

当项目复杂度超出 skeleton 最小结构时，采用分层架构模式。

## 核心原则

1. **单向依赖**：上层 → 下层，无环形依赖、无跨层调用、无反向调用
2. **职责分离**：每层只做一件事，上层只调度不实现，下层只做原子能力不做编排
3. **错误隔离**：下层错误不污染上层，Daemon 类项目必须长青
4. **上下文分层传递**：上层构建完整上下文，下层只接收需要的参数，严禁透传到底
5. **无全局状态**：无全局可变状态、无硬编码路径或密钥
6. **日志统一**：入口处初始化，下层通过参数获取，不自行初始化

## 变体 A：CLI → Task → Function

### 适用场景

- CLI 工具从单命令扩展到多命令
- 需要复用原子功能
- 支持 Python + Go 双语言

### 目录结构

```
cli/        # 入口层：参数解析、上下文构建、统一输出
tasks/      # 编排层：流程控制、错误处理
funcs/      # 原子层：单一功能、无状态
```

### 层职责

- **CLI 层**：入口触发器，接收人类输入、构建上下文、触发 Task、统一输出结果
- **Task 层**：流程编排者，调度多个 Function，控制执行顺序、分支、循环
- **Function 层**：原子能力提供者，每个 Function 是独立的点状功能，可被任意 Task 复用

### I/O 契约

- 对外接口枯燥固定：CLI 只暴露 `source`（从哪来）和 `destination`（到哪去）
- 内部链路动态生长：Source 到 Destination 之间的处理链路由 Task 和 Function 自由组合

### 铁律清单

1. 项目严格使用 `cli/`、`tasks/`、`funcs/` 作为核心骨架目录，命名不可替换
2. 调用链严格遵循 CLI → Task → Function，无跨层调用
3. Context 分层传递：CLI 传完整 Context 给 Task，Task 传具体参数给 Function
4. 不存在全局变量
5. 不存在硬编码的文件路径或网络地址
6. 错误向上收敛：Funcs 和 Tasks 不直接输出，CLI 统一处理
7. Logger 统一：CLI 创建，下层通过参数获取，不自行初始化
8. Task 只编排流程，Function 只实现原子功能
9. 每个子命令遵循：CLI 子命令文件 → Task 文件 → 多个 Function 文件的映射关系
10. 文件命名规范：Function 文件使用纯动词或名词，禁止 `_task`、`_helper`、`_ops` 等后缀

### 新增功能时的操作指引

1. 先在 `funcs/` 层实现原子函数
2. 再在 `tasks/` 层编排调用
3. 最后在 `cli/` 层暴露命令

## 变体 B：Endpoint → Handler → Adapter

### 适用场景

- Webhook 网关
- 消息队列消费者
- 事件驱动 daemon
- 支持 Python/Node.js/Go 三语言

### 目录结构

```
endpoints/  # 入口层：事件接收、鉴权、脱壳、快速响应
handlers/   # 编排层：业务逻辑编排、错误隔离
adapters/   # 执行层：外部系统交互、超时重试
```

### 层职责

- **Endpoint 层**：系统与外部世界的"触角"，只负责接收事件、鉴权拦截、脱壳，快速响应
- **Handler 层**：Daemon 的"大脑"，调度事件流转，控制执行顺序、分支、状态管理
- **Adapter 层**：系统与外部基础设施的"手脚"，每个 Adapter 是独立的 I/O 执行单元

### 事件流契约

- 对外接口快速响应：Endpoint 接收事件后立即返回 HTTP 200，严禁同步等待
- 内部链路异步编排：事件经 Endpoint 脱壳后，由 Handler 和 Adapter 异步组合处理
- 上下文按需传递：Endpoint 将请求脱壳为 EventDTO 传给 Handler；Handler 仅将 Adapter 需要的参数传给它

### 铁律清单

1. 项目严格使用 `endpoints/`、`handlers/`、`adapters/` 作为核心骨架目录，命名不可替换
2. 调用链严格遵循 Endpoint → Handler → Adapter，无跨层调用
3. EventDTO 分层传递：Endpoint 脱壳为 EventDTO 给 Handler，Handler 传具体参数给 Adapter
4. Endpoint 实现异步非阻塞返回（Fast Return）
5. Handler 包含单次事件异常隔离舱（Try/Catch）
6. Adapter 封装外部交互的所有超时和重试逻辑
7. 不存在全局可变状态
8. 不存在硬编码的密钥或网络地址
9. Handler 不直接执行 I/O，Adapter 不感知业务流程
10. 每个端点遵循：Endpoint 文件 → Handler 文件 → 多个 Adapter 文件的映射关系
11. 文件命名规范：Adapter 文件以对接目标命名，禁止 `_handler`、`_endpoint`、`_helper` 等后缀

### 两种运行模式

1. **HTTP 网关模式**：Endpoint（HTTP Route） → Handler → Adapter
2. **消息消费模式**：Endpoint（Queue Listener） → Handler → Adapter

Handler 层和 Adapter 层在两种模式下完全复用，只替换上层入口。

### 新增功能时的操作指引

1. 先在 `adapters/` 层实现对接能力
2. 再在 `handlers/` 层编排业务
3. 最后在 `endpoints/` 层暴露路由

## 变体 C：Scheduler + Endpoint → Handler → Adapter

### 适用场景

- AI Agent 守护进程（监听事件 + 定时清理/探测）
- Sidecar 控制器（监听 API 限流 + 定时恢复 session）
- 监控 daemon（接收告警 + 定时健康检查）
- 消息队列消费者（被动消费 + 主动重试）
- 支持 TypeScript/Go/Python 三语言

### 目录结构

```
scheduler/  # 定时触发层：周期性主动任务
endpoints/  # 事件响应层：被动事件接收
handlers/   # 编排层（共享）：业务逻辑编排
adapters/   # 执行层（共享）：外部系统交互
```

### 层职责

- **Scheduler 层**：系统的"闹钟"，定时触发主动任务（轮询、清理、心跳）
- **Endpoint 层**：系统与外部世界的"触角"，接收事件（SSE、Webhook、插件回调）
- **Handler 层**：Daemon 的"大脑"，编排业务逻辑，调度多个 Adapter，状态管理
- **Adapter 层**：系统与外部基础设施的"手脚"，每个 Adapter 执行独立的 I/O 操作

### 双驱动模型

- **Scheduler 驱动**：定时任务（轮询 API 状态、清理过期数据、心跳检测）
- **Endpoint 驱动**：事件响应（SSE 事件、Webhook 回调、插件通知）
- **共享 Handler**：两种驱动最终都进入 Handler 层，复用业务逻辑
- **共享 Adapter**：Handler 调用 Adapter 执行外部操作
- Handler 不区分事件来源（Scheduler 或 Endpoint），只关心业务逻辑

### 铁律清单

1. 项目严格使用 `scheduler/`、`endpoints/`、`handlers/`、`adapters/` 作为核心骨架目录
2. 调用链严格遵循 Scheduler/Endpoint → Handler → Adapter，无跨层调用
3. Scheduler 只触发定时任务，Endpoint 只接收和脱壳事件
4. Handler 不区分事件来源（Scheduler 或 Endpoint），只关心业务逻辑
5. Endpoint 实现异步非阻塞响应
6. Handler 包含单次任务异常隔离舱
7. Adapter 封装外部交互的所有超时和重试逻辑
8. 不存在全局可变状态
9. 不存在硬编码的密钥或网络地址
10. Handler 不直接执行 I/O，Adapter 不感知业务流程
11. Logger 统一：入口创建，下层通过参数获取

### 新增功能时的操作指引

1. 判断驱动方式：定时任务 → `scheduler/`；事件响应 → `endpoints/`
2. 在 `handlers/` 层创建或修改 Handler，编排 Adapter 调用
3. 在 `adapters/` 层添加 Adapter

## 选择指南

```
项目类型？
├── 人类触发的 CLI 工具 → 变体 A：CLI → Task → Function
├── 外部事件驱动的服务 → 变体 B：Endpoint → Handler → Adapter
└── 定时 + 事件混合驱动 → 变体 C：Scheduler + Endpoint → Handler → Adapter
```

## 与 Skeleton 的关系

Skeleton 是最小起点（6-8 个文件），当项目复杂度到达临界点时，选择合适的分层架构模式演化：

```
Skeleton（最小起点）
    ↓ 复杂度增加
选择合适的分层架构模式
    ↓ 继续演化
按模式规范扩展目录结构
```

Skeleton 提供零架构思考成本的起点，Pattern 提供复杂度到达后的成熟方案。
