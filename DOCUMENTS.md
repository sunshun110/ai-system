# AI System 文档索引

本文是 `ai-system` 文档的唯一目录，说明每份文档为什么存在、何时读取。没有出现在“有效文档”中的 Markdown 文件不应新增；确需新增时，必须同时更新本索引。

## 一、根目录

| 文件 | 意义与读取时机 |
|---|---|
| `README.md` | 英文项目总览、目录边界、跨平台安装、更新和验证入口；首次了解或使用 AI System 时读取。 |
| `README.zh-CN.md` | 与英文 README 等价的中文项目介绍和操作指南；需要中文入口时读取。 |
| `SECURITY.md` | 中英双语的私密安全报告、秘密处理和发布前扫描要求；处理泄露或准备发布时读取。 |
| `AGENTS.md` | 维护本仓库时的强制边界和文件归属；编辑任何 `ai-system` 文件前读取。 |
| `DOCUMENTS.md` | 全部文档的用途索引和清理依据；查找规则来源或判断文档是否重复时读取。 |
| `handoff.md` | 只记录 `ai-system` 本身的当前状态、决定、风险和下一步；跨会话维护时读取。 |

## 二、通用核心 `core/`

这些规则与供应商、工具和业务领域无关，会安装到启用 AI System 的项目中。

| 文件 | 意义与读取时机 |
|---|---|
| `core/constitution.md` | 最小改动、证据优先、风险控制等不可变行为原则；非简单任务前读取。 |
| `core/operating-model.md` | 定向、加载上下文、计划、执行、验证五阶段工作模型；组织复杂任务时读取。 |
| `core/context-loading.md` | 决定应该读取哪些规则、代码和领域包；进入陌生项目或模块时读取。 |
| `core/risk-gates.md` | 区分低、中、高风险并规定何时必须停止确认；删除、迁移、外部操作前读取。 |
| `core/verification.md` | 自动化测试到人工检查的验证阶梯与报告要求；完成任何改动前读取。 |

## 三、按需知识 `docs/`

| 文件 | 意义与读取时机 |
|---|---|
| `docs/code-review.md` | 代码审查的优先级、维度和 findings-first 输出格式；执行代码审查时读取。 |
| `docs/doc-writing.md` | 面向 AI 的文档应包含什么、避免什么以及推荐模板；新增或整理规则文档时读取。 |
| `docs/PORTABILITY.md` | 中英双语的中央源码克隆、目标预览/应用、跨平台迁移和回滚流程；接入、更新或换电脑前读取。 |
| `docs/OPEN_SOURCE_REVIEW.md` | 2026-08-24 外部仓库与 GitHub Actions 的许可证、状态和采用/暂缓决定；引入或升级外部工具前读取。 |
| `docs/Figma MCP调用手册.md` | 官方 Figma MCP 的工具选择、Skill 前置、URL 参数解析和 `use_figma` 调用模板；需要让 AI 调用 Figma 时读取。 |

## 四、通用专员 `agents/`

这些是按需使用的通用工程专员，不是公司的策划、程序或测试岗位。

| 文件 | 意义与读取时机 |
|---|---|
| `agents/bug-hunter.md` | 全面追踪真实缺陷的只读调查角色；进行大范围 Bug 扫描时读取。 |
| `agents/code-reviewer.md` | 聚焦回归、风险和缺失验证的只读审查角色；审查差异或目录时读取。 |
| `agents/docs-maintainer.md` | 检查文档缺失、过期、重复和触发条件的角色；维护文档体系时读取。 |
| `agents/perf-reviewer.md` | 只报告有频率、复杂度或测量证据的性能风险；性能审查时读取。 |
| `agents/qa-tester.md` | 独立设计用例、执行验收和回归的通用 QA 角色；需求确认且实现完成后读取。 |

## 五、通用流程 `workflows/`

| 文件 | 意义与读取时机 |
|---|---|
| `workflows/bug-hunt.md` | 带文件覆盖统计的大范围缺陷扫描；用户要求全面找 Bug 时读取。 |
| `workflows/commit-staged.md` | 只处理已暂存内容并按主题提交；用户要求提交 staged changes 时读取。 |
| `workflows/diff-watch.md` | 检查本地未提交差异是否最小、完整和安全；整理当前改动时读取。 |
| `workflows/grill-me.md` | 将无法安全实现的模糊想法逐项问清；关键产品或技术选择缺失时读取。 |
| `workflows/logic-review.md` | 沿入口、状态与出口审查指定功能的逻辑缺陷；目标范围明确时读取。 |
| `workflows/perf-hunt.md` | 按热点和证据进行大范围性能调查；性能扫描或优化请求时读取。 |
| `workflows/shader-review.md` | 依赖渲染领域包的通用 Shader 审查框架；目标项目启用渲染规则时读取。 |
| `workflows/sync-branch.md` | 安全 fetch、reconcile 和 push；用户明确要求同步远端分支时读取。 |
| `workflows/test-acceptance.md` | 从确认需求建立独立用例，并对完整候选执行验收；正式 QA 阶段读取。 |
| `workflows/triage-issue.md` | 从现象、入口和数据流定位根因并给出最小方案；处理明确问题时读取。 |

## 六、安装模板 `templates/`

| 文件 | 意义与读取时机 |
|---|---|
| `templates/module-index.md` | 新项目的目录、必读规则和生成文件索引模板；建立模块导航时使用。 |
| `templates/project-profile.md` | 项目身份、领域包、验证命令和风险概况模板；接入项目时使用。 |
| `templates/proposal.md` | 中高风险改动的目标、范围、风险和验证提案；需要先批准方案时使用。 |
| `templates/review-report.md` | 代码审查结果模板；需要保存正式审查报告时使用。 |
| `templates/triage-report.md` | 问题定位、根因、方案和验证模板；需要保存正式排障记录时使用。 |

## 七、工具适配 `adapters/`

适配器只负责让具体工具发现通用来源，不重新定义规则。

| 文件 | 意义与读取时机 |
|---|---|
| `adapters/claude/README.md` | Claude Code 的安装映射和维护原则；维护 Claude 适配时读取。 |
| `adapters/claude/agents/bug-hunter.md` | 指向通用 Bug Hunter 的 Claude 角色入口。 |
| `adapters/claude/agents/code-reviewer.md` | 指向通用 Code Reviewer 的 Claude 角色入口。 |
| `adapters/claude/agents/docs-maintainer.md` | 指向通用 Docs Maintainer 的 Claude 角色入口。 |
| `adapters/claude/agents/perf-reviewer.md` | 指向通用 Performance Reviewer 的 Claude 角色入口。 |
| `adapters/claude/agents/qa-tester.md` | 指向通用 QA Tester 的 Claude 角色入口。 |
| `adapters/claude/commands/bug-hunt.md` | Claude 的 `bug-hunt` 命令入口。 |
| `adapters/claude/commands/commit-staged.md` | Claude 的 `commit-staged` 命令入口。 |
| `adapters/claude/commands/diff-watch.md` | Claude 的 `diff-watch` 命令入口。 |
| `adapters/claude/commands/grill-me.md` | Claude 的 `grill-me` 命令入口。 |
| `adapters/claude/commands/logic-review.md` | Claude 的 `logic-review` 命令入口。 |
| `adapters/claude/commands/perf-hunt.md` | Claude 的 `perf-hunt` 命令入口。 |
| `adapters/claude/commands/shader-review.md` | Claude 的 `shader-review` 命令入口，要求渲染领域包。 |
| `adapters/claude/commands/sync-branch.md` | Claude 的 `sync-branch` 命令入口。 |
| `adapters/claude/commands/triage-issue.md` | Claude 的 `triage-issue` 命令入口。 |
| `adapters/codex/README.md` | Codex 中 AGENTS、skills、MCP 与项目规则的映射说明；维护 Codex 适配时读取。 |
| `adapters/cursor/README.md` | Cursor rules 与 AI System 的映射说明；维护 Cursor 适配时读取。 |

`adapters/claude/settings.example.json` 是安装配置示例，不是规则文档，但 Claude 适配器会复制它。

## 八、公司共享层 `company/`

公司共享层定义同一家公司的组织入口、跨部门岗位基线和学习机制。业务项目进入公司时先读取这里，再由入口选择部门。

| 文件 | 意义与读取时机 |
|---|---|
| `company/README.md` | 一家公司、多个部门的结构说明；了解公司组织方式时读取。 |
| `company/AGENTS.md` | 公司任务路由、文件归属和跨部门学习规则；处理任何公司业务项目前读取。 |
| `company/handoff.md` | 公司岗位、部门、风险和下一步；维护公司组织或新建部门时读取。 |
| `company/roles/策划.md` | 各部门共享的产品定义、需求、原型和验收标准能力；执行策划任务时读取。 |
| `company/roles/程序.md` | 各部门共享的技术方案、实现、验证和交付能力；执行程序任务时读取。 |
| `company/roles/测试.md` | 各部门共享的独立测试、证据、回归和验收能力；执行测试任务时读取。 |
| `company/roles/运维架构师.md` | 各部门共享的文件结构、环境、自动化脚本、Git/GitHub、跨电脑交付和开源复用评估能力；遇到环境报错、目录重构、GitHub 操作或工程运行保障任务时读取。 |
| `company/workflows/组织改进.md` | 判断项目经验应进入项目、部门、公司岗位还是通用核心；复盘提炼规则时读取。 |

## 九、H5 游戏部门 `company/departments/h5-game/`

H5 部门只保存浏览器游戏特有内容，岗位通用能力仍由公司共享层维护。

| 文件 | 意义与读取时机 |
|---|---|
| `company/departments/h5-game/README.md` | H5 部门定位、目录和使用方式；首次进入该部门时读取。 |
| `company/departments/h5-game/AGENTS.md` | H5 任务路由、部门边界和门禁；处理任何 H5 游戏项目前读取。 |
| `company/departments/h5-game/workflows/项目启动.md` | 使用公司岗位创建全新 H5 项目；启动下一款游戏时读取。 |
| `company/departments/h5-game/workflows/游戏制作流程.md` | H5 游戏从开项到复盘的阶段、负责人和通过条件；跨岗位制作时读取。 |
| `company/departments/h5-game/standards/Figma原型规范.md` | H5 策划原型的正式交付、评论、安全和验证要求；进行 Figma 工作时读取。 |
| `company/departments/h5-game/standards/H5技术与交付规范.md` | H5 技术选型、实现、响应式、构建和试玩交付要求；程序实现与验收时读取。 |
| `company/departments/h5-game/templates/项目开项模板.md` | 新 H5 项目的需求方输入和策划补全项；建立开项文档时使用。 |
| `company/departments/h5-game/templates/项目AGENTS模板.md` | 新 H5 项目指向公司入口的精简规则模板；创建项目规则时使用。 |

## 十、领域包状态

当前没有随 AI System 分发的领域包。只有出现真实项目需求、完成提炼并经过验证后，才在 `domains/<domain>/` 新增领域资料；通用规则继续放在核心、知识文档或工作流中。

## 十一、清理判定

本次删除以下无有效职责的文件：

- `.DS_Store`：macOS 系统元数据，不是项目内容。
- `domains/unity-game/`：当前公司与项目均未使用；通用经验已经提炼，剩余内容是无实际调用的 Unity/UFramework 历史资料。
