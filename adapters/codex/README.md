# Codex Adapter

This adapter maps the AI system into Codex-style project instructions.

## Common Targets

- `AGENTS.md`
- skill instructions
- tool-specific workflow docs
- MCP-backed resources

## Installation Pattern

1. Generate a project `AGENTS.md` from `templates/project-profile.md`.
2. Reference core rules from `core/`.
3. Add domain packs only when the project needs them.
4. Keep project-specific rules in the target project, not in the global core.
