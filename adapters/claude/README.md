# Claude Adapter

This adapter maps the vendor-neutral AI system into Claude Code conventions.

## Layout

Claude Code typically expects:

```text
.claude/
  commands/
  agents/
  settings.json
CLAUDE.md
```

The canonical workflow source remains in `../../workflows/`.
Adapter files should be thin wrappers or generated copies.

## Installation Pattern

For a target project:

1. Copy selected commands into `<project>/.claude/commands/`.
2. Copy selected agents into `<project>/.claude/agents/`.
3. Generate or copy a project-specific `CLAUDE.md`.
4. Add a project profile that points to active domain packs.
