# Code Review

> Read when reviewing code quality, correctness, regressions, maintainability, or risk.

## Review Priorities

1. Correctness
2. Simplicity
3. Safety
4. Maintainability
5. Performance where evidence supports it

## Dimensions

| # | Dimension | Questions |
|---|---|---|
| 0 | Simplicity | Can this be smaller? Is there duplicated logic? Is the abstraction justified? |
| 1 | Design | Are responsibilities clear? Are dependencies pointed the right way? |
| 2 | Readability | Is control flow understandable? Are names useful? Are comments explaining why? |
| 3 | Correctness | Are edge cases, branches, and invariants handled? |
| 4 | Lifecycle | Are setup/teardown, ownership, and cleanup paired? |
| 5 | Performance | Is this a real hotspot? Is there evidence? |
| 6 | Async/Concurrency | Are cancellation, stale writes, and reentrancy handled? |
| 7 | Observability | Are failures diagnosable without noisy logs? |
| 8 | Consistency | Does it match local project patterns? |
| 9 | Compatibility | Does it affect stored data, public APIs, protocols, or generated code? |
| 10 | Data Flow | Do source data and derived views stay in sync? |
| 11 | Platform/Environment | Are platform-specific assumptions explicit? |
| 12 | Domain Rules | Does the active domain pack add extra invariants? |

## Output

Lead with findings. For each finding:

- severity
- file and line
- evidence
- impact
- minimal fix

If there are no findings, say so and name any test gaps.
