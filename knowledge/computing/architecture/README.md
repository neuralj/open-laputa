# Architecture

程序架构知识体系 — Logos 的第一个成熟子领域。

## 结构

```
architecture/
├── philosophy.md    # 不可变原则 — 为什么这样做
├── skeletons/       # 项目从哪里开始 — 最小起点模板
│   ├── golang-cmd-internal.md
│   ├── python-minimal.md
│   ├── ts-bun-minimal.md
│   └── ts-bun-svelte-fullstack.md
└── layers/          # 复杂度出现后怎么长 — 分层架构模式
    ├── overview.md
    ├── cli-task-units.md
    ├── endpoint-handler-adapter.md
    └── scheduler-endpoint-handler-adapter.md
```

## 认知模型

```
            Philosophy
                │
      ┌─────────┴─────────┐
      ↓                   ↓
  Skeleton              Layers
      │                   │
   Start here          Grow here
      │                   │
      └─────────┬─────────┘
                ↓
          Actual System
```

- **Philosophy**：不可变的架构原则
- **Skeleton**：新项目从哪里开始？（最小起点，6-8 个文件）
- **Layers**：复杂度出现以后怎么组织？（分层架构模式）

## 使用方式

### 创建新项目

1. 选择 skeleton（按语言和技术栈）
2. 复制 skeleton 到目标目录
3. 开始写代码

### 复杂度增长

当项目复杂度超出 skeleton 最小结构时：

1. 参考 `layers/overview.md` 选择合适的分层架构
2. 按对应 layer 的规范扩展目录结构

### 审查现有项目

1. 检查 `philosophy.md` 中的原则是否被遵守
2. 验证依赖方向是否正确
3. 确认层级职责是否清晰
