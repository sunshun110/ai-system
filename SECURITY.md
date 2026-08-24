# Security / 安全说明

## English

Report suspected vulnerabilities or accidental exposure through a private channel agreed with the repository owner or maintainer. This project does not publish a security email address. Do not put vulnerability details, credentials, private paths, or sensitive reports in public issues.

- Never commit passwords, tokens, private keys, environment files, or real credential examples.
- Put local proprietary names or other repository-specific blocked terms in `.local/forbidden-terms.txt`, one per line. The `.local/` directory is intentionally ignored.
- Before any publication or visibility change, run `python3 tools/repository_guard.py`, the full validation suite, and an external [Gitleaks](https://github.com/gitleaks/gitleaks) scan of the working tree and history.
- If a credential is exposed, rotate or revoke it immediately, remove it from current files and relevant history, and document the incident only through the private reporting channel. Deleting the visible line is not sufficient.
- Repository Guard reduces common disclosure risks but is not a complete secret scanner or a substitute for review.

## 中文

发现疑似漏洞或意外泄露时，使用仓库所有者或维护者事先认可的私密渠道报告。本项目没有对外声明安全邮箱。不要在公开 Issue 中提交漏洞细节、凭据、本地私有路径或敏感报告。

- 绝不提交密码、令牌、私钥、真实环境文件或包含真实凭据的示例。
- 将本地专有名称或其他需要阻止的词逐行写入 `.local/forbidden-terms.txt`；`.local/` 已明确忽略。
- 在任何发布或可见性变更前，运行 `python3 tools/repository_guard.py`、完整验证，以及外部 [Gitleaks](https://github.com/gitleaks/gitleaks) 对工作树和历史的扫描。
- 凭据一旦暴露，立即轮换或吊销，清理当前文件和相关历史，并只通过私密渠道记录事件；仅删除可见行并不足够。
- Repository Guard 只能降低常见泄露风险，不是完整的秘密扫描器，也不能替代人工审查。
