# Architecture

程序架构知识体系 — Logos 的第一个成熟子领域。

## 结构

```
architecture/
├── principles/    # 架构原则 — 依赖方向、关注点分离、领域边界
├── patterns/      # 设计模式 — DDD、六边形、整洁架构、CQRS
├── constraints/   # 约束条件 — 禁止的依赖、不变量
├── templates/     # 架构模板 — 按复杂度分级（simple/standard/enterprise）
├── skeletons/     # 可运行的骨架项目 — 按语言分
│   ├── golang/
│   ├── python/
│   └── typescript/
└── examples/      # 示例代码
```

## 核心理念

架构不是"代码组织"，而是**依赖方向的控制**。

```
         ┌─────────────┐
         │  Interface   │  ← 用户交互
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │ Application  │  ← 用例编排
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │    Domain    │  ← 业务规则（核心）
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │Infrastructure│  ← 技术实现
         └─────────────┘
```

**依赖方向：从上到下，Domain 不依赖任何层。**

## 技术栈

- **Runtime**: Bun
- **Language**: TypeScript
- **Pattern**: DDD (Domain-Driven Design)
- **Structure**: Interface → Application → Domain → Infrastructure

## 使用方式

### 创建新项目

```
1. 选择模板级别（simple/standard/enterprise）
2. 复制 templates/{level}/ 到目标目录
3. 根据 principles/ 调整依赖方向
4. 参考 patterns/ 实现具体模式
```

### 审查现有项目

```
1. 检查 constraints/ 中的禁止依赖
2. 验证 Domain 层是否纯净
3. 确认依赖方向是否正确
```
