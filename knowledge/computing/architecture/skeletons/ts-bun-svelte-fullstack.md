---
type: skeleton
language: typescript+svelte
status: final
domain: computing
subdomain: architecture
---

# TypeScript (Bun) + Svelte 全栈骨架

Bun + Svelte SPA 的最小全栈应用骨架。Bun 负责 runtime、依赖管理和测试；Vite 仅负责 Svelte 前端开发与构建。生产环境由 Bun 单进程托管 API 和静态文件。

## 全局规则

1. **Bun 优先**：运行、依赖管理、测试统一使用 Bun
2. **Vite 单一职责**：仅用于 Svelte 前端开发和构建
3. **延迟抽象**：没有真实需求不创建 interface、class 或分层目录
4. **测试就近**：测试文件与被测代码放在一起，使用 `.test.ts`
5. **禁止预建目录**：不提前创建 utils、services、components、stores 等目录
6. **结构随业务增长**：需要什么再创建什么

## 目标结构

```text
{package-name}/
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts
├── README.md
└── src/
    ├── server/
    │   ├── index.ts
    │   └── index.test.ts
    └── client/
        ├── main.ts
        └── app.svelte
```

## 输入参数

| 参数 | 类型 | 规则 | 示例 |
|------|------|------|------|
| package-name | string | kebab-case | `homelab-control-panel` |

## 创建

```bash
mkdir -p {package-name}/src/server {package-name}/src/client
cd {package-name}

bun init -y
bun add svelte
bun add -d vite @sveltejs/vite-plugin-svelte typescript @types/bun
```

## package.json

```json
{
  "name": "{package-name}",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "bun run dev:server & bun run dev:client",
    "dev:server": "bun --watch src/server/index.ts",
    "dev:client": "vite --config vite.config.ts",
    "build": "vite build",
    "start": "bun run src/server/index.ts",
    "test": "bun test"
  }
}
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

## vite.config.ts

```typescript
import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

export default defineConfig({
  plugins: [svelte()],
  root: "src/client",
  build: {
    outDir: "../../dist/client",
    emptyOutDir: true
  },
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:3000"
    }
  }
});
```

## src/server/index.ts

```typescript
const staticDir = "./dist/client";

export function startServer(): void {
  Bun.serve({
    port: 3000,

    async fetch(req) {
      const url = new URL(req.url);

      if (url.pathname === "/api/hello") {
        return Response.json({ message: "hello" });
      }

      const path =
        url.pathname === "/"
          ? `${staticDir}/index.html`
          : `${staticDir}${url.pathname}`;

      const file = Bun.file(path);

      if (await file.exists()) {
        return new Response(file);
      }

      return new Response("Not Found", { status: 404 });
    }
  });

  console.log("Server: http://localhost:3000");
}

if (import.meta.main) {
  try {
    startServer();
  } catch (error) {
    console.error(error);
    process.exitCode = 1;
  }
}
```

## src/server/index.test.ts

```typescript
import { test } from "bun:test";
import { startServer } from "./index";

test("server entry exists", () => {
  if (typeof startServer !== "function") {
    throw new Error("startServer is not a function");
  }
});
```

## src/client/main.ts

```typescript
import App from "./app.svelte";

new App({
  target: document.getElementById("app")!
});
```

## src/client/app.svelte

```svelte
<script lang="ts">
  let message = "";

  async function hello() {
    const response = await fetch("/api/hello");
    const data = await response.json();
    message = data.message;
  }
</script>

<main>
  <h1>{package-name}</h1>
  <button onclick={hello}>Hello</button>
  <p>{message}</p>
</main>
```

## README.md

````markdown
# {package-name}

Minimal Bun + Svelte full-stack application.

## Development

```bash
bun run dev
```

* Client: http://localhost:5173
* Server: http://localhost:3000

## Build

```bash
bun run build
```

## Production

```bash
bun run start
```

## Test

```bash
bun test
```
````

## 结构演化

初始结构保持简单。

需要新功能时直接增加文件：

```text
src/
├── server/
│   ├── index.ts
│   ├── backup.ts
│   └── backup.test.ts
└── client/
    ├── main.ts
    ├── app.svelte
    └── backup.svelte
```

只有出现明确业务边界时才创建目录。

不要预先创建：

```text
controllers/
services/
repositories/
models/
routes/
components/
stores/
utils/
```

## 适用边界

- ✅ Homelab 控制面板
- ✅ 内网工具
- ✅ Agent 管理 UI
- ✅ CLI 配套 Web UI
- ✅ 小型全栈应用
- ❌ SvelteKit SSR / SSG
- ❌ 公共 npm Library
- ❌ 大型团队前端平台

## 与纯后端 skeleton 的关系

| 维度 | 纯后端 (`package.md`) | 全栈 (`svelte-fullstack.md`) |
|------|----------------------|------------------------------|
| 文件数 | 6 个 | 9 个 |
| 额外依赖 | 无 | Svelte、Vite |
| 构建工具 | Bun 原生 | Vite（仅前端） |
| 部署方式 | 单进程 | 单进程托管静态资源 |
| 适用场景 | CLI、脚本、API | 控制面板、运维工具 |

选择原则：
- 纯后端逻辑 → `package.md`
- 需要前端界面 → `svelte-fullstack.md`
