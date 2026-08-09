---
type: layer
domain: computing
subdomain: architecture
---

# 分层架构概览

当项目复杂度超出 skeleton 最小结构时，选择合适的分层架构模式。

## 核心原则

1. **单向依赖**：上层 → 下层，无环形依赖、无跨层调用、无反向调用
2. **职责分离**：每层只做一件事，上层只调度不实现，下层只做原子能力不做编排
3. **错误隔离**：下层错误不污染上层，Daemon 类项目必须长青
4. **上下文分层传递**：上层构建完整上下文，下层只接收需要的参数，严禁透传到底
5. **无全局状态**：无全局可变状态、无硬编码路径或密钥
6. **日志统一**：入口处初始化，下层通过参数获取，不自行初始化

## 三种变体

| 变体 | 适用场景 | 驱动方式 |
|------|----------|----------|
| [CLI → Task → Units](cli-task-units.md) | CLI 工具、多命令 | 人类输入 |
| [Endpoint → Handler → Adapters](endpoint-handler-adapter.md) | 事件驱动服务 | 外部事件 |
| [Scheduler + Endpoint → Handler → Adapters](scheduler-endpoint-handler-adapter.md) | 混合 daemon | 定时 + 事件 |

## 统一性

| 应用类型 | 分层结构 | 能力层目录 |
|----------|----------|------------|
| CLI 命令行工具 | CLI → Task → Units | units/ |
| Web 同步服务 | Endpoint → Handler → Adapters | adapters/ |
| 后台常驻服务 | Scheduler + Endpoint → Handler → Adapters | adapters/ |

**adapters/ 是 units/ 在 HTTP/Daemon 场景下的具体化**，表达"外部系统适配器"的语义。

## 选择指南

```
项目类型？
├── 人类触发的 CLI 工具 → CLI → Task → Units
├── 外部事件驱动的服务 → Endpoint → Handler → Adapters
└── 定时 + 事件混合驱动 → Scheduler + Endpoint → Handler → Adapters
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

Skeleton 提供零架构思考成本的起点，Layer 提供复杂度到达后的成熟方案。
