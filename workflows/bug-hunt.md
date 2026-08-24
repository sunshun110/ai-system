# Workflow: Bug Hunt

Use for broad defect discovery across a project or explicitly selected scope.

## Goal

Find real defects with coverage accounting and minimal recommended fixes.

## Scope Rules

- Define the baseline file set before scanning.
- Exclude generated, third-party, dependency, cache, and build-output directories.
- Split the scan into non-overlapping slices.
- The union of slices must equal the baseline.

## Steps

1. Load project rules and active domain packs.
2. Build the baseline file list.
3. Slice by ownership, language, or risk area.
4. Scan every file in each slice.
5. Record findings with evidence.
6. Re-check each candidate against call sites and data flow.
7. Fix only confirmed, low-risk issues or produce a review list.
8. Verify and report coverage.

## Finding Standard

A finding needs:

- concrete location
- plausible trigger
- observable impact
- code evidence
- minimal fix

## Output

```markdown
## Coverage
| Slice | Target Files | Scanned Files | Status |
|---|---:|---:|---|

## Confirmed Findings
| Severity | Location | Trigger | Evidence | Minimal Fix |
|---|---|---|---|---|

## Needs Review
- ...

## Exclusions
- ...
```
