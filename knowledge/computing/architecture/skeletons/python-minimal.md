---
type: skeleton
language: python
status: draft
domain: computing
subdomain: architecture
---

# Python 包骨架

标准化的 Python 应用项目结构，使用 UV 管理依赖，flat 布局，支持测试。默认提供 CLI 入口示例，可根据需要添加 Server 或 Daemon 入口。

## 目标结构

```
{package_snake_name}/
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── {package_snake_name}/
│   ├── __init__.py
│   ├── cli.py
│   └── config.py
└── tests/
    ├── conftest.py
    └── test_cli.py
```

## 输入参数

| 参数 | 类型 | 规则 | 示例 |
|------|------|------|------|
| package_snake_name | string | 蛇形命名，仅小写 | `file_sorter` |

派生变量：
- `package_kebab_name`: 蛇形转短横线（用于包名、CLI 命令名）
  - `file_sorter` → `file-sorter`

## 创建步骤

### Step 1: 创建目录结构

```bash
mkdir -p {package_snake_name}/{package_snake_name}
mkdir -p {package_snake_name}/tests
```

### Step 2: 生成文件

#### .gitignore

```gitignore
# UV & Virtual Env
.venv/

# Python Bytecode
__pycache__/
*.pyc
*.pyo
*.pyd

# Env Files
.env
.env.local

# Test Artifacts
.pytest_cache/

# Build & Distribution
dist/
build/
*.egg-info/

# IDE Cache
.vscode/
.idea/
.DS_Store
```

#### README.md

```markdown
# {package_kebab_name}

Minimal UV-managed Python application.

## Quick Start

### 1. Install dependencies
```bash
uv venv
uv sync
```

### 2. Run CLI locally
```bash
uv run {package_kebab_name}
```

### 3. Run test suite

```bash
uv run pytest
```

## Dependencies
- Runtime: typer
- Dev: pytest
```

#### pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{package_kebab_name}"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "typer>=0.12.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0.0",
]

[project.scripts]
{package_kebab_name} = "{package_snake_name}.cli:app"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

#### {package_snake_name}/__init__.py

```python
# Empty package marker
```

#### {package_snake_name}/config.py

```python
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
```

#### 入口类型

当前默认使用命令式入口。根据应用类型，可选择不同模式：

| 模式 | 文件示例 | 启动方式 | 适用场景 |
|------|----------|----------|----------|
| 命令式 | `main.py` | `uv run demo-app` | CLI、Daemon、批处理 |
| 事件驱动 | `server.py` | `uvicorn demo_app.server:app` | Web API |

同一个包可以包含多个入口，按需添加。

#### {package_snake_name}/cli.py

> 这是默认的命令式入口示例。Daemon 只需在函数内添加循环逻辑。

```python
import logging

import typer

from {package_snake_name}.config import LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

app = typer.Typer(help="{package_kebab_name} command line application")

@app.command()
def run(name: str = "system") -> None:
    logger.info("Application started")
    print(f"Hello {name}")
```

#### tests/conftest.py

```python
# Pytest root config placeholder
```

#### tests/test_cli.py

```python
from typer.testing import CliRunner

from {package_snake_name}.cli import app

runner = CliRunner()

def test_cli_run_default_param():
    """Validate run command with default argument"""
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello" in result.output
```

### Step 3: 初始化 UV 环境

```bash
cd {package_snake_name}
uv venv
uv add --dev pytest
uv sync
```

## 设计约束

1. **仅保留 8 个文件**：禁止 `core/`、`utils/`、`scripts/`、`docker/` 等额外目录
2. **入口点必须注册**：命令式入口在 `[project.scripts]` 中定义，禁止 `__main__` 关键词
3. **tests/ 必须保留**：用于 Agent 回归测试
4. **开发依赖隔离**：`dev` 组独立，生产部署可跳过

## 全局安装

```bash
uv tool install -e .
```

安装后可直接运行 `demo-app`。

## 适用边界

- ✅ 独立应用（命令式、事件驱动）
- ✅ 内部自动化工具
- ✅ Agent 迭代维护的项目
- ❌ 可发布的公共库包
- ❌ 需要复杂分层的模块

## 结构演化

当项目复杂度超出最小结构时，参考 `layers/overview.md` 选择合适的分层架构模式：

- CLI 工具变复杂 → CLI → Task → Function
- 事件驱动服务 → Endpoint → Handler → Adapter
- 混合 daemon → Scheduler + Endpoint → Handler → Adapter
