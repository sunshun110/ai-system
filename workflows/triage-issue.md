# Workflow: Triage Issue

Use when the user reports a concrete problem.

## Goal

Find the root cause and propose the smallest safe fix.

## Steps

1. Capture the symptom.
2. Locate the entry point.
3. Trace the execution path.
4. Identify why the failure happens.
5. Compare with adjacent working patterns.
6. Propose the minimal fix.
7. Define verification.

## Gate

Stop for confirmation before editing when:

- the fix changes public behavior
- the root cause is uncertain
- the fix spans modules
- verification cannot be run

## Report

```markdown
## Symptom
- Trigger:
- Actual:
- Expected:
- Frequency:

## Root Cause
- Location:
- Mechanism:
- Why this is root cause:

## Fix Plan
- Minimal change:
- Impact:
- Risk:

## Verification
- Test or reproduction:
- Regression points:
```
