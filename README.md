# Logos

> A personal knowledge and practice system for turning understanding into models, methods, and executable systems.

## 定义

Logos 是一套将认知沉淀为模型、方法，并最终转化为可执行系统的个人知识与实践体系。

## 结构

```
                 LOGOS
                   │
       ┌───────────┼───────────┐
       │           │           │
    Computing    Finance    General
       │           │           │
 Architecture   Trading    Thinking
       │           │           │
       └───────────┼───────────┘
                   │
          Knowledge / Models
                   │
                Methods
                   │
               Practices
                   │
              Executable
                Systems
```

## 层级

| 层级 | 目录 | 含义 |
|------|------|------|
| **Knowledge** | `knowledge/` | 知道什么 — 事实、定义、原理 |
| **Models** | `models/` | 如何理解 — 对现实的解释框架 |
| **Methods** | `methods/` | 如何分析 — 验证、研究的方法 |
| **Practices** | `practices/` | 如何行动 — 转化为可执行系统 |

## 领域

| 领域 | 目录 | 内容 |
|------|------|------|
| **Computing** | `knowledge/computing/` | 架构、编程、数据库、分布式、AI |
| **Finance** | `knowledge/finance/` | 经济学、会计、估值、市场理论 |
| **General** | `knowledge/general/` | 思维、决策、研究、方法论 |

## 边界

- 只保存**经过抽象、验证、结构化**的认知
- 不是资料收集箱，是认知操作系统
- Computing/Finance/General 是三个独立领域，共享同一套 Ontology

## 与其他系统的关系

```
                    Logos
                      │
          ┌───────────┼────────────┐
          │           │            │
      Knowledge     Models       Methods
          │           │            │
          └───────────┼────────────┘
                      │
                  Practice
                      │
              ┌───────┴────────┐
              │                │
         neural-base       other projects
              │
        Data / Backtest
        Indicators
        Models
        Experiments
```

- **Logos** 是认知层 — 定义"是什么"和"为什么"
- **neural-base** 是实验层 — 负责"计算"和"验证"
