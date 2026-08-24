# Workflow: Commit Staged

Use when committing staged changes.

## Goal

Create one or more coherent commits from the staged diff without pulling in unrelated work.

## Rules

- Read the staged diff before writing messages.
- Do not run `git add .`.
- Do not stage additional files unless the user explicitly asks.
- One commit should represent one topic.
- Use explicit file paths in commit commands.

## Steps

1. Check status.
2. Read staged diff stat.
3. Read unstaged diff stat to detect possible missing pieces.
4. Read staged diffs by file.
5. Group by topic.
6. Commit each group.
7. Report commit hashes.

## Gate

Stop when:

- staged changes look incomplete
- secrets or personal files are staged
- generated files and sources appear mismatched
- a commit would mix unrelated work
