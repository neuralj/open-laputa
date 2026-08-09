---
type: skeleton
language: typescript
status: final
domain: computing
subdomain: architecture
---

# TypeScript (Bun) 最小骨架

以最低认知负担为核心目标的 TypeScript 应用骨架。全程基于 Bun 原生能力，零额外构建工具，零预置目录，结构随真实业务需求自然生长。

## 全局规则

1. **Bun 原生全链路**：运行、依赖管理、测试全部使用 Bun 内置能力，不引入 tsc、vitest、tsx 等第三方工具链。
2. **初始 6 文件约束**：项目初始化后仅保留 6 个文件，无任何空目录。
3. **延迟抽象原则**：无真实需求不创建 interface、class、分层目录，不提前做架构设计。
4. **测试就近放置**：测试文件与被测代码同目录，以 `.test.ts` 后缀区分。
5. **禁止预建目录**：不创建 utils、services、config、models 等任何预置目录。

## 目标结构

```text
{package-name}/
├── .gitignore
├── package.json
├── tsconfig.json
├── README.md
└── src/
    ├── index.ts
    └── index.test.ts
```

## 输入参数

| 参数 | 类型 | 命名规则 | 示例 |
|------|------|----------|------|
| package-name | string | 小写短横线命名 | `file-sorter` |

## 初始化步骤

### 1. 创建目录

```bash
mkdir -p {package-name}/src
cd {package-name}
```

### 2. 生成核心文件

#### .gitignore

```gitignore
node_modules/
.env*
dist/
.DS_Store
```

#### package.json

```json
{
  "name": "{package-name}",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "module": "src/index.ts",
  "scripts": {
    "dev": "bun --watch src/index.ts",
    "start": "bun run src/index.ts",
    "test": "bun test"
  },
  "devDependencies": {
    "@types/bun": "latest"
  }
}
```

#### tsconfig.json

```json
{
  "compilerOptions": {
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true
  },
  "include": ["src"]
}
```

#### src/index.ts

```typescript
export async function run(name = "world"): Promise<void> {
  console.log(`Hello, ${name}`);
}

// 直接运行文件时作为入口执行
if (import.meta.main) {
  const arg = Bun.argv[2];
  run(arg).catch((error) => {
    console.error("Fatal error:", error);
    process.exitCode = 1;
  });
}
```

#### src/index.test.ts

```typescript
import { test, expect } from "bun:test";
import { run } from "./index";

test("smoke test", async () => {
  await expect(run()).resolves.toBeUndefined();
});
```

#### README.md

```markdown
# {package-name}

Minimal TypeScript application powered by Bun.

## Commands
- Start: `bun start`
- Dev (watch mode): `bun dev`
- Test: `bun test`
```

### 3. 安装依赖并验证

```bash
bun install
bun test
```

> **注意**：`bun install` 会自动生成 `bun.lock` 文件，该文件应提交到 Git 仓库，用于锁定依赖版本。

## 核心命令

- 运行：`bun start`
- 开发（热重载）：`bun dev`
- 测试：`bun test`
- 安装依赖：`bun add <package>`

## 结构演化

仅当出现真实业务边界时，再拆分文件与目录：

1. 先增加同层级文件（如 `src/backup.ts`）
2. 形成明确模块边界后，再创建对应子目录
3. 入口拆分、配置抽离、分层设计等操作，均按需进行，不提前预设

当项目复杂度进一步增加时，参考 `layers/overview.md` 选择合适的分层架构模式：

- CLI 工具变复杂 → CLI → Task → Function
- 事件驱动服务 → Endpoint → Handler → Adapter
- 混合 daemon → Scheduler + Endpoint → Handler → Adapter

如果需要前端界面，参考 `svelte-fullstack.md` 选择全栈模式。

## 适用边界

- ✅ CLI 工具、自动化脚本、轻量后台服务
- ✅ 个人项目、Homelab 工具、Agent 执行器
- ✅ 快速原型验证、数据处理脚本
- ❌ 前端 UI 项目
- ❌ 面向公众发布的 npm 包
- ❌ 大型 monorepo 项目
