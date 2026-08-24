# Workflow: Diff Watch

Use when reviewing local uncommitted changes.

## Goal

Keep the diff minimal, coherent, and safe.

## Steps

1. Inspect status.
2. Read staged and unstaged diffs separately.
3. Group changes by intent.
4. Identify unrelated edits.
5. Identify over-defensive or duplicated code.
6. Identify risky partial changes.
7. Recommend or apply only safe cleanup.

## Rules

- Do not touch staged changes unless the workflow explicitly allows it.
- Do not revert user work unless clearly requested.
- Do not mix unrelated cleanup into a fix.
- Preserve work that is risky to judge.

## Output

```markdown
## Diff Summary
- Files:
- Themes:

## Safe Cleanup
- ...

## Needs Review
- ...

## Left Untouched
- ...
```
