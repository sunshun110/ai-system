# Workflow: Sync Branch

Use after local commits are ready and the user wants to sync with the remote.

## Goal

Safely fetch, reconcile, and push.

## Rules

- Do not sync with dirty worktree state unless explicitly instructed.
- Do not force push with plain `--force`.
- Prefer `--force-with-lease` only when history was intentionally rewritten.
- Stop on conflicts.

## Steps

1. Check status.
2. Identify current branch.
3. Identify upstream.
4. Fetch with prune.
5. Calculate ahead/behind.
6. Choose fast-forward, push, rebase, or merge.
7. Push safely.
8. Report final HEAD.
