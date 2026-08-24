# Portability Guide / 跨平台迁移指南

This guide defines the safe clone, update, apply, and rollback workflow for macOS, Linux, and Windows. AI System is early-stage and evolves continuously, so every target mutation must be previewed.

本文规定 macOS、Linux 和 Windows 上安全的克隆、更新、应用和回滚流程。AI System 仍处于早期阶段并持续演进，因此每次修改目标前都必须预览。

## 1. Keep the central clone separate / 保持中央源码独立

Use one workspace whose children are the AI System clone and real business projects. Never clone AI System inside a real project, and never place a real project inside AI System.

使用一个工作区，将 AI System 中央源码和真实业务项目作为同级目录。不要把 AI System 克隆到真实项目内部，也不要把真实项目放进 AI System。

```text
workspace/
├── ai-system/
├── business-project-a/
└── business-project-b/
```

This separation makes source updates inert: `git pull --ff-only` changes only `ai-system/`. No business project changes until an explicit CLI command targets it.

这种分离保证源码更新本身没有外部副作用：`git pull --ff-only` 只改变 `ai-system/`。只有 CLI 明确指定目标后，业务项目才会变化。

## 2. Clone and verify / 克隆与验证

Prerequisites are Git and Python 3.10 or newer. No package installation is required.

前置条件只有 Git 和 Python 3.10 或更高版本，不需要安装 Python 包。

macOS or Linux:

```bash
cd workspace
git clone <private-repository-url> ai-system
cd ai-system
python3 tools/repository_guard.py
python3 -m unittest discover -s tests
python3 bin/ai-system doctor
python3 bin/ai-system validate
```

Windows PowerShell:

```powershell
Set-Location workspace
git clone <private-repository-url> ai-system
Set-Location ai-system
py -3 .\tools\repository_guard.py
py -3 -m unittest discover -s tests
py -3 .\bin\ai-system doctor
py -3 .\bin\ai-system validate
```

Stop if any command returns nonzero. Resolve source validation before integrating a project.

任何命令返回非零状态时都要停止；先修复源码验证，再接入项目。

## 3. Preview, then apply initial integration / 先预览，再首次应用

macOS or Linux:

```bash
python3 bin/ai-system init --target ../business-project-a --adapter claude --dry-run
# Review every planned path, then explicitly apply:
python3 bin/ai-system init --target ../business-project-a --adapter claude
python3 bin/ai-system validate --target ../business-project-a
```

Windows PowerShell:

```powershell
py -3 .\bin\ai-system init --target ..\business-project-a --adapter claude --dry-run
# 审查全部计划路径后，再明确应用：
py -3 .\bin\ai-system init --target ..\business-project-a --adapter claude
py -3 .\bin\ai-system validate --target ..\business-project-a
```

The dry run is a review artifact, not authorization to write. Confirm the target path, adapter/domain selection, overwrite behavior, and recovery point before applying.

Dry-run 只是审查材料，不等于已经授权写入。应用前必须确认目标路径、适配器/领域选择、覆盖行为和恢复点。

## 4. Update workflow / 更新流程

1. Ensure the target project has no unexplained local changes and create a recovery point using its normal version-control or backup policy.
2. Update only the central source with `git pull --ff-only`.
3. Run the source validations.
4. Run `update --dry-run` against exactly one target and review the planned writes.
5. Only after approval, run `update` without `--dry-run`.
6. Validate and test the target project using both AI System validation and the project's own checks.

1. 确认目标项目没有无法解释的本地改动，并按该项目的版本控制或备份策略建立恢复点。
2. 使用 `git pull --ff-only` 只更新中央源码。
3. 运行源码验证。
4. 对一个明确目标运行 `update --dry-run` 并审查计划写入。
5. 获得确认后，才运行不带 `--dry-run` 的 `update`。
6. 同时使用 AI System 验证和目标项目自身检查完成验证。

**`update --dry-run` is the mandatory gate before mutation. If the preview is unexpected, stop; do not run the apply command.**

**`update --dry-run` 是修改目标前的强制门禁。预览不符合预期时立即停止，不得执行应用命令。**

macOS or Linux:

```bash
git pull --ff-only
python3 tools/repository_guard.py
python3 -m unittest discover -s tests
python3 bin/ai-system update --target ../business-project-a --dry-run
python3 bin/ai-system update --target ../business-project-a
python3 bin/ai-system validate --target ../business-project-a
```

Windows PowerShell:

```powershell
git pull --ff-only
py -3 .\tools\repository_guard.py
py -3 -m unittest discover -s tests
py -3 .\bin\ai-system update --target ..\business-project-a --dry-run
py -3 .\bin\ai-system update --target ..\business-project-a
py -3 .\bin\ai-system validate --target ..\business-project-a
```

## 5. Rollback / 回滚

If validation fails after applying an update:

1. Stop further AI System operations on that target.
2. Save the dry-run output and validation errors without copying credentials or private data.
3. Restore target files from the recovery point created before mutation. Prefer the target project's reviewed version-control restore procedure; otherwise restore its verified backup.
4. Run the target project's tests and `validate` again.
5. Keep the central AI System clone unchanged for diagnosis, or use a separate clean clone of the previously approved revision. Do not solve a target rollback by nesting or copying the central repository into the target.
6. Re-run `update --dry-run` before any retry.

应用后验证失败时：

1. 停止对该目标继续执行 AI System 操作。
2. 保存 dry-run 输出和验证错误，但不要复制凭据或私有数据。
3. 从修改前建立的恢复点还原目标文件；优先使用目标项目经过审查的版本控制恢复流程，否则还原已验证备份。
4. 重新运行目标项目测试和 `validate`。
5. 保持中央 AI System 源码不变以便排查，或另建上一批准版本的干净克隆。不要通过把中央仓库嵌套或复制进目标来回滚。
6. 任何重试前再次执行 `update --dry-run`。

The `remove` command also supports `--dry-run`, but it is not a substitute for a backup because it removes tracked installation files rather than reconstructing overwritten target content.

`remove` 命令同样支持 `--dry-run`，但它只删除受跟踪的安装文件，不能重建被覆盖的目标内容，因此不能代替备份。

## 6. Cross-machine handoff / 跨电脑交接

Record only portable facts: approved source revision, Python version, operating system, selected adapters/domains, exact validation commands, target-relative paths, and remaining risks. Never record credentials or machine-specific user paths. On the new machine, clone the central source as a sibling, validate it, preview the target update, and only then apply.

只记录可迁移事实：已批准的源码版本、Python 版本、操作系统、适配器/领域选择、准确验证命令、目标相对路径和剩余风险。不要记录凭据或机器专属用户路径。在新电脑上把中央源码克隆为同级目录，先验证源码，再预览目标更新，最后才应用。
