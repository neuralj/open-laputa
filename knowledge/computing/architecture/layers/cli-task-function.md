---
type: layer
domain: computing
subdomain: architecture
---

# CLI → Task → Function

## 适用场景

- CLI 工具从单命令扩展到多命令
- 需要复用原子功能
- 支持 Python + Go 双语言

## 目录结构

```
cli/        # 入口层：参数解析、上下文构建、统一输出
tasks/      # 编排层：流程控制、错误处理
funcs/      # 原子层：单一功能、无状态
```

## 层职责

- **CLI 层**：入口触发器，接收人类输入、构建上下文、触发 Task、统一输出结果
- **Task 层**：流程编排者，调度多个 Function，控制执行顺序、分支、循环
- **Function 层**：原子能力提供者，每个 Function 是独立的点状功能，可被任意 Task 复用

## I/O 契约

- 对外接口枯燥固定：CLI 只暴露 `source`（从哪来）和 `destination`（到哪去）
- 内部链路动态生长：Source 到 Destination 之间的处理链路由 Task 和 Function 自由组合

## 铁律清单

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

## 新增功能时的操作指引

1. 先在 `funcs/` 层实现原子函数
2. 再在 `tasks/` 层编排调用
3. 最后在 `cli/` 层暴露命令
