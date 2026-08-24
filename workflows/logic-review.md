# Workflow: Logic Review

Use when reviewing a specific directory or feature path for logic bugs.

## Goal

Find real behavioral bugs, not style opinions.

## Scope

The target must be explicit. If it is not explicit, identify candidate scopes and ask the user to choose.

## Steps

1. Read project rules.
2. Read the target module docs.
3. Map entry points, core state, and exits.
4. Review edge cases and branch completeness.
5. Trace lifecycle and async paths.
6. Report findings.
7. Wait for confirmation before fixing, unless the user has explicitly authorized direct repair.

## Output

```markdown
## Flow Overview
- Entry:
- Core:
- Exit:

## Findings
| # | Severity | Type | Location | Trigger | Root Cause |
|---|---|---|---|---|---|

## Restraint
- Observations outside this review scope:
```
