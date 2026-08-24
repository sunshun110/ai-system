# Workflow: Shader Review

This is a domain-sensitive workflow. It should be activated only when the target project has a rendering or shader domain pack.

## Goal

Review shader code for correctness, compatibility, and performance using the active rendering domain rules.

## Inputs

- shader file path
- shader code
- rendering pipeline rules from the active domain pack

## Steps

1. Confirm target shader or shader code.
2. Load rendering domain rules.
3. Identify passes and variants.
4. Review performance, correctness, compatibility, and maintainability.
5. Provide specific before/after suggestions.
6. Wait for confirmation before editing unless direct fixes were requested.

## Output

```markdown
## Summary
| Dimension | Verdict | Reason |
|---|---|---|

## Findings
### 1. <title>
- Dimension:
- Location:
- Impact:
- Before:
- After:

## Restraint
- ...
```
