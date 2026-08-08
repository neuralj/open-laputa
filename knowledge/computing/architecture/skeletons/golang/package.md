---
type: skeleton
language: golang
status: final
domain: computing
subdomain: architecture
---

# Go 包骨架

Go 项目结构，仅使用标准库，`cmd + internal` 单模式，最小可演化架构。

## 全局规则

1. **仅使用标准库**：不引入第三方依赖（zap/fx/wire/viper 等不自动生成）
2. **Context 首参**：IO、数据库、HTTP 等阻塞函数首参必须为 `context.Context`，纯计算函数无需 ctx
3. **错误包装**：统一用 `fmt.Errorf("xxx: %w", err)` 嵌套，仅初始化致命场景允许 `panic`
4. **测试就近**：单元测试在同包内创建 `*_test.go`，不新建独立 `tests` 顶层目录
5. **延迟抽象**：单个实现直接用结构体，多套实现时才抽 `interface`；手动构造函数注入依赖，禁用 DI 框架
6. **禁止空目录**：`utils/core/common/model/config/pkg` 不预先创建，结构跟随业务生长
7. **main 职责**：`main()` 仅处理启动、上下文设置和顶层错误退出，不写业务逻辑
8. **结构生长**：目录结构只在真实业务需求出现时才扩展

## 目标结构

```
{module-path}/
├── .gitignore
├── go.mod
├── README.md
├── cmd/
│   └── {binary-name}/
│       └── main.go
└── internal/
    └── app/
        ├── app.go
        └── app_test.go
```

## 输入参数

| 参数 | 类型 | 规则 | 示例 |
|------|------|------|------|
| module-path | string | Go module 路径 | `my-service` |
| binary-name | string | 小写短横线命名 | `server`、`worker` |

## 创建步骤

### Step 1: 初始化目录

```bash
mkdir -p cmd/{binary-name} internal/app
go mod init {module-path}
```

### Step 2: 生成文件

#### .gitignore

```gitignore
bin/
*.exe *.so *.dylib *.dll
*.test coverage.out
.env .env.local
.vscode/ .idea/ .DS_Store
```

#### go.mod

```go
module {module-path}

go 1.24
```

#### cmd/{binary-name}/main.go

```go
package main

import (
	"context"
	"log"

	"{module-path}/internal/app"
)

func main() {
	ctx := context.Background()
	if err := app.Run(ctx); err != nil {
		log.Fatalf("exit error: %v", err)
	}
}
```

#### internal/app/app.go

```go
package app

import (
	"context"
	"log/slog"
)

func Run(ctx context.Context) error {
	slog.Info("service started")
	return nil
}
```

#### internal/app/app_test.go

```go
package app

import (
	"context"
	"testing"
)

func TestRun_Smoke(t *testing.T) {
	if err := Run(context.Background()); err != nil {
		t.Fatal(err)
	}
}
```

#### README.md

````markdown
# {module-path}

Go service, stdlib only.

## Build

```bash
go build -o bin/{binary-name} ./cmd/{binary-name}
```

## Run

```bash
go run ./cmd/{binary-name}
```

## Test

```bash
go test -v ./...
go test -race ./...
```
````

## 附录：扩展指南

### A. 内部包扩展

当实际业务边界出现时，在 `internal/` 下创建对应 package。
优先按 capability / domain 组织，而不是按 MVC 或技术角色组织。

例如：

```
internal/
├── app/
├── backup/
├── media/
└── monitoring/
```

如果某个基础设施形成稳定的跨领域边界，再创建：

```
internal/
└── infra/
    ├── postgres/
    └── minio/
```

### B. 多二进制扩展

需要多个独立进程时，在 `cmd` 下新增子目录：

```
cmd/
├── api/
│   └── main.go
└── worker/
    └── main.go
```

编译示例：

```bash
go build -o bin/api ./cmd/api
go build -o bin/worker ./cmd/worker
```

### C. 适用边界

- ✅ CLI 工具、定时脚本、数据处理
- ✅ HTTP 自托管服务、常驻后台 Daemon
- ✅ 多二进制组合（API + Worker + 迁移）
- ❌ 团队协作项目
- ❌ 公共 Library/SDK（需独立设计 public package API）
