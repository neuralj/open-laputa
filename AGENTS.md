# Logos Agent Guide

## 导航逻辑

```
用户需求 → 定位领域 → 定位层级 → 获取知识/方法/模板
```

## 层级含义

| 层级 | 问题 | 示例 |
|------|------|------|
| **Knowledge** | "这是什么？" | 涨停制度、DDD 分层 |
| **Models** | "如何理解？" | 涨停 = 价格发现约束 |
| **Methods** | "如何验证？" | 统计涨停后 N 日收益分布 |
| **Practices** | "如何行动？" | 构建涨停策略 |

## 领域导航

### Computing
```
knowledge/computing/architecture/
├── principles/    # 架构原则
├── patterns/      # 设计模式
├── constraints/   # 约束条件
├── templates/     # 项目模板
└── examples/      # 示例代码
```

### Finance
```
knowledge/finance/
├── economics/     # 经济学
├── accounting/    # 会计
├── valuation/     # 估值
└── markets/       # 市场理论
```

### General
```
knowledge/general/
├── thinking/      # 思维模型
├── decision/      # 决策框架
├── research/      # 研究方法
└── methodology/   # 方法论
```

## 任务路由

### "帮我创建一个新的 TypeScript 服务"
```
Computing → Architecture → templates/standard/
```

### "帮我分析这个股票策略"
```
Trading → Models → Research Methods → neural-base
```

### "帮我理解这个概念"
```
定位领域 → Knowledge → 返回定义和原理
```

## 输出规范

当基于 Logos 生成代码或分析时：
1. 引用具体知识来源（路径）
2. 说明使用的模型/方法
3. 给出可执行的下一步
