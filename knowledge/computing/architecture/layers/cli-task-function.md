---
type: layer
domain: computing
subdomain: architecture
---

# CLI → Task → Unit

小型 CLI 应用的最小分层变体。Function 是 Unit 的一种轻量实现形态。

## 适用场景

- CLI 工具从单命令扩展到多命令
- 需要复用原子能力
- 支持 Python + Go 双语言

## 目录结构

### 选项 A：小型项目（Function 为主）

```
cli/        # 入口层：参数解析、上下文构建、统一输出
tasks/      # 编排层：流程控制、错误处理
funcs/      # 原子层：单一功能、无状态
```

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
- **Unit 层**：能力边界，定义明确的输入输出契约。Function 是 Unit 的最轻量形态

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

### 何时从 Function 升级为 Unit Boundary？

当 Function 满足以下条件时，升级为独立 Unit：

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
