---
type: layer
domain: computing
subdomain: architecture
---

# CLI → Task → Unit

> Unit 是一个具有稳定输入/输出契约、可独立演进、对调用者隐藏内部实现的逻辑能力边界。

CLI → Task → Unit 是一种典型的小型应用调用结构。它不是固定目录模板，而是一种责任分配模型。

## 核心公理

1. **Layer ≠ Directory**：分层是逻辑概念，目录是物理实现
2. **Unit ≠ Directory**：Unit 是能力边界，不是固定目录
3. **Function ⊂ Unit**：Function 是 Unit 的实现形态，不是竞争选项

## 层职责

| 层 | 角色 | 职责 |
|----|------|------|
| CLI | Trigger | 接收外部输入、构建执行请求 |
| Task | Orchestrator | 表达一次完整 Use Case，负责流程编排 |
| Unit | Capability Boundary | 提供稳定的系统能力，隐藏内部实现 |

## 两种编排

**Task 编排**（Use-case orchestration）：
> 用户要求系统完成什么任务？

例如：`TaskA` 代表"用户要求执行某个用例"

**Unit 内部编排**（Capability orchestration）：
> 这个能力内部如何实现？

例如：`UnitX` 内部协调 Step1 → Step2 → Step3 → Step4

## 目录结构示例

**小型 CLI**：
```
internal/
├── cli/
├── tasks/
└── units/
    └── unit-a.go      # 单文件 Unit
```

**中型 CLI**：
```
internal/
├── cli/
├── tasks/
└── units/
    └── unit-x/        # 目录 Unit
        ├── unit-x.go  # 入口
        ├── step-1.go
        └── step-2.go
```

**复杂系统**：
```
internal/
├── cli/
├── tasks/
├── unit-x/            # Unit 可直接在 internal 下
│   ├── unit-x.go
│   └── helper-a.go
└── unit-y/
    ├── unit-y.go
    └── helper-b.go
```

## 演进规则

### Unit Boundary 的形成条件

一个能力应该成为 Unit，当它具备：

1. 明确的能力名称
2. 稳定的输入输出契约
3. 独立的变化原因
4. 内部实现可以独立演进
5. 调用者不应该关心内部步骤

### 决策树

```
是否存在独立能力？
       │
    ┌──┴──┐
    否     是
    │      │
普通代码   Unit
           │
           ├── 一个 Function
           ├── 多个 Function
           ├── Struct + Methods
           └── 多个内部组件
```

## 铁律清单

1. 调用链严格遵循 CLI → Task → Unit，无跨层调用
2. Context 分层传递：CLI 传完整 Context 给 Task，Task 传具体参数给 Unit
3. 不存在全局变量
4. 不存在硬编码的文件路径或网络地址
5. 错误向上收敛：Unit 和 Task 不直接输出，CLI 统一处理
6. Logger 统一：CLI 创建，下层通过参数获取，不自行初始化
7. Task 只编排流程，Unit 只实现能力
8. Unit 对调用者隐藏内部实现细节

## 与其他 Layer 的统一

| 场景 | Trigger | Orchestrator | Capability Boundary |
|------|---------|--------------|---------------------|
| CLI | CLI | Task | Unit |
| HTTP | Endpoint | Handler | Adapter / Unit |
| Daemon | Scheduler | Handler | Adapter / Unit |

统一模型：
```
Trigger → Orchestrator → Capability Boundary → Implementation
```
