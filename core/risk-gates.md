# Risk Gates

Risk gates decide whether AI may act directly or must stop for confirmation.

## Low Risk

AI may proceed after local context is loaded.

Examples:

- documentation edits
- small typo fixes
- adding focused tests
- small local bug fixes with clear verification
- moving files inside an explicitly approved restructure

## Medium Risk

AI should state a short plan before editing.

Examples:

- behavior changes
- edits across multiple modules
- changing workflow documents
- changing adapter behavior
- migrations with reversible file moves

## High Risk

AI must stop and ask before execution.

Examples:

- deleting user work
- rewriting public history
- destructive shell commands
- broad refactors
- schema or protocol changes
- changing project boundaries
- moving files outside the approved workspace plan

## Stop Conditions

Stop when:

- the target is ambiguous
- required context is missing
- verification is impossible and risk is high
- the same blocker repeats after reasonable investigation
