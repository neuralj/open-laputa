---
type: layer
domain: computing
subdomain: architecture
---

# CLI → Task → Units

CLI 应用的三层宏观分层架构。Function 仅为 Unit 内部最轻量化的代码实现形式，不再作为独立架构概念。

## 三条总原则

1. **Unit 是逻辑能力边界，不等于目录**
2. **Function 是 Unit 的实现形态，不是 Unit 的下一层架构**
3. **units/ 是能力单元的集合目录，内部按职责组织**

> CLI → Task → Units 是一种**调用关系**，而不是要求所有项目必须存在三个目录。

## 适用场景

- CLI 工具从单命令扩展到多命令
- 需要复用原子能力
- 支持 Python + Go + TypeScript 多语言

## 目录结构

### 方案 A：新项目起步（最简结构）

```
cli/        # 入口层
tasks/      # 编排层
units/      # 原子能力层：所有零散能力归集
```

所有代码全部丢在 `units/` 根目录，不用拆分任何子文件夹。

### 方案 B：逻辑增多（按 Unit 职责二次分组）

```
cli/        # 入口层
tasks/      # 编排层
units/
  compute/  # 纯计算逻辑（无状态、无副作用）
  domain/   # 领域实体、业务规则
  execute/  # IO、外部调用适配器
```

这仅为 Unit 内部整理，不上升为 Layer 层级。

### 方案 C：能力边界固化（按业务域拆分）

```
cli/        # 入口层
tasks/      # 编排层
units/
  scanner/  # 扫描 Unit
  formatter/# 格式化 Unit
  exporter/ # 导出 Unit
```

## 层职责

- **CLI 层**：入口触发器，接收人类输入、构建上下文、触发 Task、统一输出结果
- **Task 层**：流程编排者，调度多个 Unit，控制执行顺序、分支、循环
- **Units 层**：原子能力集合，定义明确的输入输出契约

## Unit 类型

| 类型 | 特征 | 示例 |
|------|------|------|
| Compute Unit | 无状态、纯计算 | FormatFile, DetectLanguage |
| Domain Unit | 业务状态/规则 | Order, User |
| Execute Unit | IO/副作用 | PostgresClient, HttpClient |

> **Unit 是统一的封装粒度概念，而不是统一的代码形态。**

## Unit ≠ Directory

Unit 是**逻辑能力边界**，目录只是它的一种物理表达。

**单文件 Unit**（能力简单时）：
```go
// pack.go
type Pack struct { ... }
func (p *Pack) Execute(...) (...)
```

**目录 Unit**（能力复杂时）：
```
units/
└── pack/
    ├── unit.go
    ├── scan.go
    ├── format.go
    └── segment.go
```

**选择标准**：代码规模和变化原因决定是否需要目录，而非 Unit 概念本身。

## Function vs Unit 关系

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

### 何时从临时收纳升级为独立 Unit？

当能力形成稳定边界时，建立独立 Unit。**是否创建目录由代码规模和变化原因决定。**

升级条件：

- 被多个 Task 复用
- 形成稳定的输入输出契约
- 有独立测试价值
- 有明显变化原因

### 演进触发条件

当满足以下任一条件时，应从阶段 1 演进到阶段 2：

| 指标 | 阈值 | 说明 |
|------|------|------|
| `units/` 下文件数量 | > 4 个 | 平铺结构难以维护 |
| 单个 Task 调用的 units 文件 | > 3 个 | 说明存在隐式的能力边界 |
| 某个能力的函数数量 | > 3 个 | 说明该能力已形成独立边界 |
| 文件间存在明显的调用链 | scan → format → segment | 说明存在流程编排需求 |

**示例**：llm-review 当前状态
- `units/` 下有 3 个文件：scan.go, format.go, pack.go
- `pack_task.go` 调用 `units.Pack()`，而 `Pack()` 内部调用 Scan、Format
- 存在隐式调用链：scan → format → segment → write

→ 应演进到 `units/pack/` 结构

### 演进操作步骤

**从阶段 1 到阶段 2 的具体步骤**：

1. **识别能力边界**
   - 分析 Task 调用了哪些 units 文件
   - 找出文件间的调用关系
   - 确定哪些文件属于同一能力

2. **创建子目录**
   ```bash
   mkdir -p internal/units/pack
   ```

3. **移动文件**
   ```bash
   mv internal/units/scan.go internal/units/pack/
   mv internal/units/format.go internal/units/pack/
   mv internal/units/pack.go internal/units/pack/
   ```

4. **调整包名和导入**
   - 所有文件改为 `package pack`
   - Task 层导入改为 `internal/units/pack`

5. **暴露入口函数**
   - 在 `units/pack/` 中创建 `unit.go` 或直接使用 `pack.go` 作为入口
   - 入口函数协调内部 Scan、Format、Segment、Write

### Task 层的演进

| 阶段 | Task 层职责 | 调用方式 |
|------|-------------|----------|
| 阶段 1 | 简单调用 | `units.Pack(opts)` |
| 阶段 2 | 编排 Unit | `pack.Pack(opts)` → 内部协调 |
| 阶段 3 | 编排多个 Unit | `scanner.Scan()` + `formatter.Format()` |

**关键原则**：Task 层不关心 Unit 内部实现，只关心输入输出契约。

### 演进后的代码示例

**Task 层（pack_task.go）**：
```go
func PackTask(rootPath, outputDir string, maxChars int) error {
    // 调用 Pack Unit 的入口函数
    result, err := pack.Pack(pack.Options{
        RootPath:  rootPath,
        OutputDir: outputDir,
        MaxChars:  maxChars,
    })
    // ...
}
```

**Pack Unit 入口（units/pack/pack.go）**：
```go
package pack

func Pack(opts Options) (*Result, error) {
    // 1. 扫描
    files, err := Scan(opts.RootPath)
    
    // 2. 格式化
    formatted := Format(files)
    
    // 3. 分段
    segments := Segment(formatted, opts.MaxChars)
    
    // 4. 写入
    return Write(segments, opts.OutputDir)
}
```

**Pack Unit 内部（units/pack/scan.go, format.go, ...）**：
```go
package pack

func Scan(rootPath string) ([]FileInfo, error) { ... }
func Format(files []FileInfo) []FormattedFile { ... }
func Segment(files []FormattedFile, maxChars int) []Segment { ... }
func Write(segments []Segment, outputDir string) (*Result, error) { ... }
```

### 目录演进示例

**阶段 1：小型项目**
```
cli/ + tasks/ + units/
```

**阶段 2：业务能力边界清晰**
```
cli/ + tasks/ + units/pack/
```

**阶段 3：多能力独立**
```
cli/ + tasks/ + units/scanner/ + units/formatter/
```

## 新增功能时的操作指引

1. 判断能力边界：是简单 Function 还是独立 Unit？
2. 在 `units/` 层实现能力（根目录或独立子目录）
3. 在 `tasks/` 层编排调用
4. 在 `cli/` 层暴露命令

## 与其他 Layer 的统一

| 应用类型 | 分层结构 |
|----------|----------|
| CLI 命令行工具 | CLI → Task → Units |
| Web 同步服务 | Endpoint → Handler → Adapters |
| 后台常驻服务 | Scheduler + Endpoint → Handler → Adapters |

三个变体结构完全同构，只是最外层触发器、最底层能力载体名字不同。
