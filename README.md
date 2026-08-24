# AI System

[中文说明 / Chinese documentation](README.zh-CN.md)

AI System is a reusable operating system for structured AI-assisted engineering. It combines vendor-neutral operating rules, on-demand knowledge, repeatable workflows, tool adapters, and one company's shared roles and business departments. It is early-stage software and evolves continuously as real projects validate or disprove its rules.

## Repository boundaries

This repository is the central source of truth. Its major areas have distinct owners:

- `company/`: shared company staff roles, cross-department learning, and business departments. Business-specific differences belong in `company/departments/`.
- `core/`: non-negotiable, platform-independent reasoning, risk, context, and verification rules.
- `docs/`: reusable knowledge loaded only when relevant.
- `workflows/`: repeatable task procedures with success criteria and verification.
- `agents/`: generic engineering specialists for delegated investigation or review; they are not company staff positions.
- `adapters/`: discovery and packaging for tools such as Claude Code, Codex, and Cursor. Tool-specific syntax stays here.
- `domains/`: optional technical knowledge packs. No domain pack is currently bundled.
- `templates/`: scaffolds installed into another project.
- `bin/`, `tools/`, and `tests/`: the local CLI, repository-maintenance tools, and automated verification.

See [DOCUMENTS.md](DOCUMENTS.md) for the complete document catalog, [docs/PORTABILITY.md](docs/PORTABILITY.md) for migration and rollback procedures, [SECURITY.md](SECURITY.md) for security handling, and [docs/OPEN_SOURCE_REVIEW.md](docs/OPEN_SOURCE_REVIEW.md) for reviewed external tooling decisions.

## Prerequisites

Only these tools are required:

- Git
- Python 3.10 or newer

The project uses the Python standard library and has no runtime package installation step.

## Clone and update the central source

Keep the AI System clone beside business projects, never inside one of them:

```text
workspace/
├── ai-system/
├── business-project-a/
└── business-project-b/
```

Clone once:

```bash
git clone <private-repository-url> ai-system
cd ai-system
```

Update with a fast-forward-only pull:

```bash
git pull --ff-only
```

On Windows PowerShell, the Git commands are the same:

```powershell
git clone <private-repository-url> ai-system
Set-Location ai-system
git pull --ff-only
```

A pull changes only this central source clone. It never mutates sibling business projects. Project integration changes only when an operator explicitly runs `init`, `install`, `update`, or `remove` against a target.

## Inspect and validate the source

From the repository root on macOS or Linux:

```bash
python3 bin/ai-system info
python3 tools/repository_guard.py
python3 -m unittest discover -s tests
python3 bin/ai-system doctor
python3 bin/ai-system validate
```

On Windows PowerShell:

```powershell
py -3 .\bin\ai-system info
py -3 .\tools\repository_guard.py
py -3 -m unittest discover -s tests
py -3 .\bin\ai-system doctor
py -3 .\bin\ai-system validate
```

The repository guard can run from any working directory because it locates this repository from its own file. Add local forbidden terms, one per line, to `.local/forbidden-terms.txt`; `.local/` is intentionally untracked. Terms can also be supplied with repeatable `--forbidden-term` options or an explicit `--denylist` file. Run `python3 tools/repository_guard.py --help` (or the Windows equivalent) for details.

## Integrate AI System into a sibling project

Always preview before writing. On macOS or Linux:

```bash
# Preview initial integration
python3 bin/ai-system init --target ../business-project-a --adapter claude --dry-run

# Apply only after reviewing the preview
python3 bin/ai-system init --target ../business-project-a --adapter claude
```

On Windows PowerShell:

```powershell
# Preview initial integration
py -3 .\bin\ai-system init --target ..\business-project-a --adapter claude --dry-run

# Apply only after reviewing the preview
py -3 .\bin\ai-system init --target ..\business-project-a --adapter claude
```

The installer writes `.ai-system/` and requested adapter folders into the target. It does not copy the central company source into unrelated locations; business projects reference the company module from the sibling AI System clone.

## Update an integrated project

First update this source clone with `git pull --ff-only`. Then treat `update --dry-run` as the required gate before any target mutation:

macOS or Linux:

```bash
python3 bin/ai-system update --target ../business-project-a --dry-run
python3 bin/ai-system update --target ../business-project-a
python3 bin/ai-system validate --target ../business-project-a
```

Windows PowerShell:

```powershell
py -3 .\bin\ai-system update --target ..\business-project-a --dry-run
py -3 .\bin\ai-system update --target ..\business-project-a
py -3 .\bin\ai-system validate --target ..\business-project-a
```

Do not run the apply command until the preview is understood and the target has a clean recovery point. Detailed backup and rollback options are in [docs/PORTABILITY.md](docs/PORTABILITY.md).

## Common CLI operations

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

Use `py -3 .\bin\ai-system` and Windows path separators for the corresponding PowerShell commands. Run `python3 bin/ai-system --help` or a subcommand with `--help` for the full interface.

## Maturity and change discipline

AI System is intentionally lightweight and early-stage. Rules, departments, adapters, and workflows evolve continuously, but changes should remain small, reviewable, and evidence-based. Update `DOCUMENTS.md` whenever Markdown documents are added, moved, or removed, and run all repository validations before sharing or publishing a revision.
