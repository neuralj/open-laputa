---
type: layer
domain: computing
subdomain: architecture
---

# Endpoint → Handler → Adapter

## 适用场景

- Webhook 网关
- 消息队列消费者
- 事件驱动 daemon
- 支持 Python/Node.js/Go 三语言

## 目录结构

```
endpoints/  # 入口层：事件接收、鉴权、脱壳、快速响应
handlers/   # 编排层：业务逻辑编排、错误隔离
adapters/   # 执行层：外部系统交互、超时重试
```

## 层职责

- **Endpoint 层**：系统与外部世界的"触角"，只负责接收事件、鉴权拦截、脱壳，快速响应
- **Handler 层**：Daemon 的"大脑"，调度事件流转，控制执行顺序、分支、状态管理
- **Adapter 层**：系统与外部基础设施的"手脚"，每个 Adapter 是独立的 I/O 执行单元

## 事件流契约

- 对外接口快速响应：Endpoint 接收事件后立即返回 HTTP 200，严禁同步等待
- 内部链路异步编排：事件经 Endpoint 脱壳后，由 Handler 和 Adapter 异步组合处理
- 上下文按需传递：Endpoint 将请求脱壳为 EventDTO 传给 Handler；Handler 仅将 Adapter 需要的参数传给它

## 铁律清单

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

## 两种运行模式

1. **HTTP 网关模式**：Endpoint（HTTP Route） → Handler → Adapter
2. **消息消费模式**：Endpoint（Queue Listener） → Handler → Adapter

Handler 层和 Adapter 层在两种模式下完全复用，只替换上层入口。

## 新增功能时的操作指引

1. 先在 `adapters/` 层实现对接能力
2. 再在 `handlers/` 层编排业务
3. 最后在 `endpoints/` 层暴露路由
