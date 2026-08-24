# Documentation Writing

Docs in this system exist to give AI reliable project context.

## Good AI-Facing Docs

Good docs include:

- when to read this document
- non-obvious project rules
- dependency direction
- common patterns
- known traps
- verification points

Good docs avoid:

- generic language knowledge
- stale summaries of code
- one-off implementation details
- duplicated rules already owned elsewhere

## Template

```markdown
# <Topic>

> Read when: <keywords and task triggers>.

## Rules

- Must: ...
- Must not: ...
- Default: ...

## Dependencies

<What this depends on and what depends on it.>

## Common Pattern

<Short example or checklist.>

## Traps

| Trap | Correct Approach | Why |
|---|---|---|
| ... | ... | ... |
```
