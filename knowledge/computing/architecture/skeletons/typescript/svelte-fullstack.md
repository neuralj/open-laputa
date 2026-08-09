---
type: skeleton
language: typescript+svelte
status: final
domain: computing
subdomain: architecture
---

# TypeScript (Bun) + Svelte 全栈骨架

Bun 原生 HTTP API + Svelte SPA，单进程生产部署，Bun 统一管控依赖、运行、测试。

## 全局规则

1. **Bun 原生全链路**：运行、依赖管理、测试全部使用 Bun 内置能力，不引入 tsc、vitest、tsx 等第三方工具链
2. **初始文件最小约束**：初始化仅 10 个文件，无任何预置空目录
3. **延迟抽象原则**：无真实需求不创建 interface、class、分层目录，不提前做架构设计
4. **测试就近放置**：测试文件与被测代码同目录，以 `.test.ts` 后缀区分
5. **禁止预建目录**：不创建 utils、services、config、components、stores 等任何预置目录

## 目标结构

```text
{package-name}/
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts
├── svelte.config.js
├── README.md
├── src/server/
│   ├── index.ts
│   └── index.test.ts
└── src/client/
    ├── app.svelte
    └── main.ts
```

## 输入参数

| 参数 | 类型 | 命名规则 | 示例 |
|------|------|----------|------|
| package-name | string | 小写短横线 kebab-case | `homelab-control-panel` |

## 初始化步骤

### 1. 创建目录

```bash
mkdir -p {package-name}/src/server {package-name}/src/client
cd {package-name}
```

### 2. 生成核心文件

#### .gitignore

```gitignore
node_modules/
.env*
dist/
build/
.DS_Store
.vscode/
.idea/
bun.lockb
```

#### package.json

```json
{
  "name": "{package-name}",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev:server": "bun --watch src/server/index.ts",
    "dev:client": "vite",
    "dev": "bun dev:server & bun dev:client",
    "build": "vite build",
    "start": "bun run src/server/index.ts",
    "test": "bun test"
  },
  "devDependencies": {
    "@sveltejs/vite-plugin-svelte": "^3.2.0",
    "@types/bun": "latest",
    "svelte": "^4.2.19",
    "typescript": "^5.6.0",
    "vite": "^5.4.0"
  }
}
```

#### tsconfig.json

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

#### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  root: 'src/client',
  build: {
    outDir: '../../dist/client',
    emptyOutDir: true
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true
      }
    }
  }
});
```

#### svelte.config.js

```javascript
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
  preprocess: vitePreprocess()
};
```

#### src/server/index.ts

```typescript
import { existsSync } from 'fs';
import { resolve } from 'path';

export async function startServer(): Promise<void> {
  const staticDir = resolve('./dist/client');
  const serveStatic = existsSync(staticDir);

  Bun.serve({
    port: 3000,
    async fetch(req) {
      const url = new URL(req.url);

      // API 路由
      if (url.pathname === '/api/hello') {
        return Response.json({ msg: 'Bun backend service running' });
      }

      // 生产环境托管 Svelte 打包后的静态页面
      if (serveStatic) {
        if (url.pathname === '/' || !url.pathname.includes('.')) {
          return Bun.file(`${staticDir}/index.html`);
        }
        return Bun.file(`${staticDir}${url.pathname}`);
      }

      return new Response('Not Found', { status: 404 });
    }
  });

  console.log('Backend running on http://localhost:3000');
  if (serveStatic) console.log('Frontend static assets served by Bun');
}

if (import.meta.main) {
  startServer().catch((error) => {
    console.error('Fatal error:', error);
    process.exitCode = 1;
  });
}
```

#### src/server/index.test.ts

```typescript
import { test, expect } from "bun:test";
import { startServer } from "./index";

test("server entry function valid", async () => {
  await expect(startServer).toBeInstanceOf(Function);
});
```

#### src/client/main.ts

```typescript
import App from './app.svelte';

const app = new App({
  target: document.getElementById('app')!
});

export default app;
```

#### src/client/app.svelte

```svelte
<script lang="ts">
  let message = '';

  async function fetchBackend() {
    const res = await fetch('/api/hello');
    const data = await res.json();
    message = data.msg;
  }
</script>

<main>
  <h1>Bun Fullstack + Svelte Minimal Skeleton</h1>
  <button on:click={fetchBackend}>Request Backend API</button>
  <p>{message}</p>
</main>

<style>
main {
  text-align: center;
  padding: 3rem;
}
button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>
```

#### README.md

```markdown
# {package-name}

Bun TS Fullstack Minimal Skeleton

- Backend: Bun native HTTP
- Frontend: Svelte SPA (Vite only for build tool)

## Core Commands

1. Full development (backend + frontend hot reload):
   ```bash
   bun dev
   ```

2. Start backend service only:
   ```bash
   bun start
   ```

3. Build frontend static files to /dist/client:
   ```bash
   bun build
   ```

4. Run all unit tests:
   ```bash
   bun test
   ```

## Production Deploy Flow

1. `bun build` compile frontend
2. `bun start` launch backend, Bun automatically serve static page on port 3000
```

### 3. 安装依赖并验证

```bash
bun install
bun test
```

> **注意**：`bun.lockb` 提交至 Git，锁定依赖版本。

## 核心命令

- `bun dev`：前后端并行热更新开发
- `bun dev:server`：仅后端热重载
- `bun dev:client`：仅前端 Vite 开发服务
- `bun build`：编译前端静态产物
- `bun start`：生产启动后端，自动托管打包后的前端页面
- `bun test`：全项目统一测试入口
- `bun add xxx`：安装依赖

## 生产部署流程

1. `bun build` 编译前端静态资源到 `dist/client`
2. `bun start` 启动后端服务，自动托管前端静态页面

单进程、单端口（3000），无需 Nginx 反向代理。

## 结构演化

仅当出现真实业务边界时，再拆分文件与目录：

1. **平级优先**：`server/`、`client/` 内部先新增同级文件，禁止初次创建子文件夹
2. **边界后置拆分**：单一目录文件数量过多、业务模块完全清晰后，再手动建立子目录
3. **超大规模解耦**：系统复杂度飙升后，直接将 `src/server`、`src/client` 拆分两个独立仓库

**永久禁止**：初始化自动生成 `controllers`、`repositories`、`stores`、`routes`、`components` 等空架构目录。

## 适用边界

- ✅ 单人 Code Agent 驱动私有复杂系统、Homelab 运维控制面板
- ✅ 内网工具、CLI 配套可视化后台、长期迭代全栈项目
- ✅ 追求最小打包体积、最低框架心智负担、AI 低出错率的前端场景
- ❌ 需要 SvelteKit SSR/SSG 全站渲染的公网官网
- ❌ 多人团队协作、重度依赖海量 Vue 生态 UI 组件的中台系统
- ❌ 超大型企业级分布式微服务架构

## 与纯后端 skeleton 的关系

| 维度 | 纯后端 (`package.md`) | 全栈 (`svelte-fullstack.md`) |
|------|----------------------|------------------------------|
| 文件数 | 6 个 | 10 个 |
| 额外依赖 | 无 | Svelte、Vite |
| 构建工具 | Bun 原生 | Vite（仅前端） |
| 部署方式 | 单进程 | 单进程托管静态资源 |
| 适用场景 | CLI、脚本、API | 控制面板、运维工具 |

选择原则：
- 纯后端逻辑 → `package.md`
- 需要前端界面 → `svelte-fullstack.md`
