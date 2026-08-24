# Workflow: Performance Hunt

Use for broad performance review across a project or selected scope.

## Goal

Find performance problems with evidence, not intuition.

## Scope Rules

- Identify likely hot paths.
- Distinguish measured evidence from static risk.
- Exclude generated, third-party, dependency, cache, and build-output directories unless explicitly included.

## Evidence

Each confirmed finding should include at least one:

- profiler data
- allocation data
- repeated call frequency
- algorithmic complexity
- known hot path
- bundle/build/runtime cost

## Steps

1. Load project rules and active domain packs.
2. Identify performance-sensitive areas.
3. Build a baseline file list.
4. Scan hot paths first, then cold paths.
5. Confirm each candidate with evidence.
6. Apply only small, local, low-risk optimizations.
7. Move larger changes into proposals.
8. Verify and report.

## Gate

Write a proposal instead of editing when:

- change spans modules
- public APIs change
- data structures change broadly
- runtime behavior changes
- expected impact is large but risk is non-trivial

## Output

```markdown
## Confirmed Optimizations
| Location | Issue | Evidence | Expected Benefit | Change |
|---|---|---|---|---|

## Proposals
- ...

## Not Changed
- ...
```
