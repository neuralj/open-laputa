---
type: layer
domain: computing
subdomain: architecture
---

# CLI → Task → Unit

小型 CLI 应用的最小分层变体。Function 是 Unit 的一种轻量实现形态。

## 三条总原则

1. **Unit 是逻辑能力边界，不等于目录**
2. **Function 是 Unit 的实现形态，不是 Unit 的下一层架构**
3. **funcs/ 是临时的轻量 Function 容器，不是必须长期存在的架构层**

> CLI → Task → Unit 是一种**调用关系**，而不是要求所有项目必须存在三个目录。

## 适用场景

- CLI 工具从单命令扩展到多命令
- 需要复用原子能力
- 支持 Python + Go 双语言

## 目录结构

### 选项 A：小型项目（Function 为主）

```
cli/        # 入口层
tasks/      # 编排层
funcs/      # 临时容器：尚未形成独立边界的 Function Unit
```

> funcs/ 不是架构层，而是"这些 Unit 目前还不值得拥有自己的目录边界"的临时状态。

### 选项 B：业务能力边界清晰（Unit 为主）

```
cli/        # 入口层
tasks/      # 编排层
pack/       # Pack Unit 边界
scan/       # Scan Unit 边界
format/     # Format Unit 边界
```

## 层职责

- **CLI 层**：入口触发器，接收人类输入、构建上下文、触发 Task、统一输出结果
- **Task 层**：流程编排者，调度多个 Unit，控制执行顺序、分支、循环
- **Unit 层**：能力边界，定义明确的输入输出契约。Function 是 Unit 内部的最轻量实现形态，不是独立的架构层

## Unit 组织

### Task 调用多个 Unit

```
Task
 ├── Unit₁ (scan)    → []FileInfo
 ├── Unit₂ (format)  → string
 └── Unit₃ (write)   → error
```

### Unit 之间的协作

Unit 之间通过明确的输入输出契约协作：

```
ScanUnit
  ↓ ([]FileInfo)
FormatUnit
  ↓ (string)
WriteUnit
  ↓ (error)
```

### Unit 类型

| 类型 | 特征 | 示例 |
|------|------|------|
| Function Unit | 无状态、纯计算 | FormatFile, DetectLanguage |
| Domain Unit | 业务状态/规则 | Order, User |
| Execute Unit | IO/副作用 | PostgresClient, HttpClient |

> **Unit 是统一的封装粒度概念，而不是统一的代码形态。**

### Unit ≠ Directory

Unit 是**逻辑能力边界**，目录只是它的一种物理表达。

**单文件 Unit**（能力简单时）：
```go
// pack.go
type Pack struct { ... }
func (p *Pack) Execute(...) (...)
```

**目录 Unit**（能力复杂时）：
```
pack/
├── unit.go
├── scan.go
├── format.go
└── segment.go
```

**选择标准**：代码规模和变化原因决定是否需要目录，而非 Unit 概念本身。

### Function vs Unit 关系

```
Unit（能力边界）
  ├── Function（内部实现）
  ├── Function（内部实现）
  └── Function（内部实现）
```

- **Task** 回答："这次任务要做什么流程？"
- **Unit** 回答："系统有哪些稳定能力？"
- **Function** 回答："这个能力内部具体怎么做？"

Function → Unit 是**包含/实现关系**，不是调用关系。

## 铁律清单

1. 调用链严格遵循 CLI → Task → Unit，无跨层调用
2. Context 分层传递：CLI 传完整 Context 给 Task，Task 传具体参数给 Unit
3. 不存在全局变量
4. 不存在硬编码的文件路径或网络地址
5. 错误向上收敛：Unit 和 Task 不直接输出，CLI 统一处理
6. Logger 统一：CLI 创建，下层通过参数获取，不自行初始化
7. Task 只编排流程，Unit 只实现能力
8. 每个子命令遵循：CLI 子命令文件 → Task 文件 → 多个 Unit 的映射关系

## 演进规则

### 何时从 Function 升级为独立 Unit？

当能力形成稳定边界时，建立独立 Unit。**是否创建目录由代码规模和变化原因决定。**

升级条件：

- 被多个 Task 复用
- 形成稳定的输入输出契约
- 有独立测试价值
- 有明显变化原因

### 目录演进示例

**阶段 1：小型项目**
```
cli/ + tasks/ + funcs/
```

**阶段 2：业务能力边界清晰**
```
cli/ + tasks/ + pack/
```

**阶段 3：多能力独立**
```
cli/ + tasks/ + pack/ + scan/ + format/
```

## 新增功能时的操作指引

1. 判断能力边界：是简单 Function 还是独立 Unit？
2. 在对应层实现能力（funcs/ 或独立目录）
3. 在 tasks/ 层编排调用
4. 在 cli/ 层暴露命令
