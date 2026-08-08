# Logos

面向 Agent 的个人认知基础设施。将认知沉淀为可组合、可执行的认知资产。

## 认知资产类型

| 层 | 核心问题 | 定义 | 目录 |
|---|---|---|---|
| Knowledge | What is true? | 世界的事实、规则、原理 | `knowledge/` |
| Models | How do we represent? | 对现实的压缩与解释 | `models/` |
| Methods | How do we reason? | 可执行的推理过程 | `methods/` |
| Practices | How do we act? | 面向行动的操作规程 | `practices/` |

## 目录结构

```
knowledge/
├── computing/architecture/    # principles/ patterns/ constraints/ templates/ skeletons/ examples/
├── finance/                   # economics/ accounting/ valuation/ markets/
└── (general/ 已迁移至 methods/)

models/                        # 按领域：computing/ finance/ general/
methods/                       # 按推理类型：reasoning/ research/ analysis/ decision/
practices/                     # 按领域：computing/ finance/ general/
schemas/                       # 认知产物元数据定义
```

## 导航逻辑

```
用户需求 → 定位资产类型 → 定位领域 → 获取认知产物
```

## 边界规则

1. **Knowledge** 描述外部世界，不含主观解释
2. **Models** 是对现实的压缩，必须明确假设和边界
3. **Methods** 必须可执行，有明确输入输出
4. **Practices** 必须经过验证，有验收标准

## 不变量

- 每个文件以 `# 标题` 开头，紧跟一句话定义
- 引用使用路径格式：`knowledge/computing/architecture/patterns/ddd.md`
- 文件命名：小写英文 + 短横线分隔
- 不创建空文件，没有内容就不建文件
- 只保存经过抽象、验证、结构化的认知

## 新增认知产物

1. 确定资产类型（Knowledge / Model / Method / Practice）
2. 查看 `schemas/` 对应元数据定义
3. 按元数据格式创建文件
4. 建立跨层引用（如 Practice 引用 Knowledge + Method）

## 禁止事项

- 禁止将 Knowledge 与 Model 混放
- 禁止创建无元数据的认知产物
- 禁止在 AGENTS.md 中堆积知识内容
