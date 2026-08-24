# AI System

[English documentation / 英文说明](README.md)

AI System 是一套可复用的 AI 辅助工程操作系统，用于把零散提示整理为有边界、可验证、可重复执行的规则、知识和流程。它同时保存供应商中立的工程能力，以及同一家公司的共享岗位和业务部门。项目仍处于早期阶段，会随着真实项目的验证持续演进。

## 仓库边界

本仓库是中央事实来源，各目录职责不同：

- `company/`：公司共享岗位、跨部门学习机制和业务部门；业务差异放在 `company/departments/`。
- `core/`：与平台无关且不可随意绕过的推理、风险、上下文和验证规则。
- `docs/`：仅在相关任务中按需加载的可复用知识。
- `workflows/`：带完成标准和验证步骤的通用任务流程。
- `agents/`：用于委派调查或审查的通用工程专员，不是公司岗位。
- `adapters/`：Claude Code、Codex、Cursor 等工具的发现与封装；工具专属语法只放在这里。
- `domains/`：可选技术知识包；当前没有随仓库分发的领域包。
- `templates/`：接入其他项目时使用的模板。
- `bin/`、`tools/`、`tests/`：本地 CLI、仓库维护工具和自动化验证。

完整文档目录见 [DOCUMENTS.md](DOCUMENTS.md)，跨电脑迁移与回滚见 [docs/PORTABILITY.md](docs/PORTABILITY.md)，安全处理见 [SECURITY.md](SECURITY.md)，外部工具评审记录见 [docs/OPEN_SOURCE_REVIEW.md](docs/OPEN_SOURCE_REVIEW.md)。

## 前置条件

只需要：

- Git
- Python 3.10 或更高版本

项目只使用 Python 标准库，不需要安装运行时依赖。

## 克隆和更新中央源码

AI System 必须和业务项目处于同级目录，不能嵌套在任何业务项目中：

```text
workspace/
├── ai-system/
├── business-project-a/
└── business-project-b/
```

首次克隆：

```bash
git clone <private-repository-url> ai-system
cd ai-system
```

以后只做快进更新：

```bash
git pull --ff-only
```

Windows PowerShell 使用相同的 Git 命令：

```powershell
git clone <private-repository-url> ai-system
Set-Location ai-system
git pull --ff-only
```

`git pull` 只更新中央 AI System 源码，不会修改同级业务项目。只有操作人员明确对目标执行 `init`、`install`、`update` 或 `remove` 时，目标项目才会变化。

## 检查和验证源码

在仓库根目录执行。macOS 或 Linux：

```bash
python3 bin/ai-system info
python3 tools/repository_guard.py
python3 -m unittest discover -s tests
python3 bin/ai-system doctor
python3 bin/ai-system validate
```

Windows PowerShell：

```powershell
py -3 .\bin\ai-system info
py -3 .\tools\repository_guard.py
py -3 -m unittest discover -s tests
py -3 .\bin\ai-system doctor
py -3 .\bin\ai-system validate
```

`repository_guard.py` 会根据脚本位置找到本仓库，因此可从任意工作目录运行。需要阻止本地专有词时，在 `.local/forbidden-terms.txt` 中每行填写一个词；`.local/` 不进入版本控制。也可重复传入 `--forbidden-term`，或通过 `--denylist` 指定文件。详细参数使用 `python3 tools/repository_guard.py --help`，Windows 使用对应的 `py -3` 命令。

## 接入同级业务项目

写入前必须先预览。macOS 或 Linux：

```bash
# 预览首次接入
python3 bin/ai-system init --target ../business-project-a --adapter claude --dry-run

# 审查预览后再明确应用
python3 bin/ai-system init --target ../business-project-a --adapter claude
```

Windows PowerShell：

```powershell
# 预览首次接入
py -3 .\bin\ai-system init --target ..\business-project-a --adapter claude --dry-run

# 审查预览后再明确应用
py -3 .\bin\ai-system init --target ..\business-project-a --adapter claude
```

安装器会在目标中写入 `.ai-system/` 和已请求的适配器目录。中央公司模块不会被复制到无关位置；业务项目通过同级 AI System 源码引用公司入口。

## 更新已接入项目

先在本仓库执行 `git pull --ff-only`。然后必须把 `update --dry-run` 作为修改目标前的门禁：

macOS 或 Linux：

```bash
python3 bin/ai-system update --target ../business-project-a --dry-run
python3 bin/ai-system update --target ../business-project-a
python3 bin/ai-system validate --target ../business-project-a
```

Windows PowerShell：

```powershell
py -3 .\bin\ai-system update --target ..\business-project-a --dry-run
py -3 .\bin\ai-system update --target ..\business-project-a
py -3 .\bin\ai-system validate --target ..\business-project-a
```

没有理解预览结果、没有为目标建立可恢复点时，不得执行第二条应用命令。备份和回滚方式见 [docs/PORTABILITY.md](docs/PORTABILITY.md)。

## 常用 CLI 操作

```bash
python3 bin/ai-system list
python3 bin/ai-system list company-roles
python3 bin/ai-system list departments
python3 bin/ai-system show workflows triage-issue
python3 bin/ai-system status --target ../business-project-a
python3 bin/ai-system install --target ../business-project-a --adapter cursor --dry-run
python3 bin/ai-system remove --target ../business-project-a --adapter cursor --dry-run
python3 bin/ai-system export --output ../ai-system-export.tar.gz
```

Windows PowerShell 将入口替换为 `py -3 .\bin\ai-system`，并使用 Windows 路径分隔符。完整接口可运行 `python3 bin/ai-system --help` 或对应子命令的 `--help`。

## 成熟度与变更纪律

AI System 有意保持轻量，目前仍处于早期阶段。规则、部门、适配器和流程会持续演进，但改动必须小、可审查并有证据。新增、移动或删除 Markdown 文档时同步更新 `DOCUMENTS.md`；分享或发布修订前运行全部仓库验证。
