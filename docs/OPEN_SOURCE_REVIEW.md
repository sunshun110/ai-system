# Open Source Review

Review date: 2026-08-24

This record captures repository-readiness decisions for selected upstream projects. Star counts and activity observations are point-in-time signals from the review date, not permanent guarantees.

| Upstream | Purpose | Review signal | Decision |
|---|---|---|---|
| [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | Scan working trees and Git history for secrets before publication. | 28,931 stars; MIT; active. | Adopt as a required external pre-publication scan. Do not vendor it and do not make it a repository runtime dependency. |
| [cli/cli](https://github.com/cli/cli) | Perform authenticated GitHub repository, issue, pull-request, and release operations. | 45,963 stars; MIT; active. | Recommend as the official GitHub operations tool when remote work is approved. It is not a repository dependency. |
| [actions/checkout](https://github.com/actions/checkout) | Check out repository content in GitHub Actions. | 8,658 stars; MIT; active. | Adopt v7.0.1 pinned to immutable commit `3d3c42e5aac5ba805825da76410c181273ba90b1`. |
| [actions/setup-python](https://github.com/actions/setup-python) | Provision reviewed Python versions in GitHub Actions. | 2,208 stars; MIT; active. | Adopt v7.0.0 pinned to immutable commit `5fda3b95a4ea91299a34e894583c3862153e4b97`. |
| [github/gitignore](https://github.com/github/gitignore) | Provide community-maintained ignore-pattern references. | 175,437 stars; CC0-1.0; active. | Use as a reference only. Keep this repository's `.gitignore` small and locally reviewed rather than copying a template wholesale. |
| [pre-commit/pre-commit](https://github.com/pre-commit/pre-commit) | Manage repeatable local Git hooks. | 15,528 stars; MIT; active. | Defer to avoid adding a Python package dependency at this stage. Reconsider only when hook consistency justifies the added toolchain. |
| [jdx/mise](https://github.com/jdx/mise) | Manage tool versions, environments, and tasks across machines. | 32,916 stars; MIT; active. | Defer because Git and Python 3.10+ are sufficient for the current repository. |
| [devcontainers/cli](https://github.com/devcontainers/cli) | Create and run development-container environments. | 2,912 stars; MIT; active. | Defer until real projects require container parity that cannot be met by the lightweight workflow. |

Popularity is not approval. Stars and an active repository do not replace code review, threat modeling, maintenance evaluation, or fit testing. Recheck the upstream version, immutable reference, license, maintenance status, security posture, and transitive dependencies before every adoption or upgrade.
