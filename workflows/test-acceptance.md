# Workflow: Test Acceptance

Use when a confirmed product specification must be converted into independent test cases and a completed implementation must be accepted against them.

## Inputs

- explicitly confirmed requirements baseline
- approved interaction and visual assets, when applicable
- acceptance candidate from the programmer
- implementation notes and supported environments

## Procedure

### 1. Confirm the planning gate

Check that product logic, scope, edge cases, and version identifiers are complete and explicitly confirmed.

If the baseline is incomplete or ambiguous, stop. The requirements owner resolves product logic; planning does not participate in test design or execution.

### 2. Design independent test cases

The QA tester creates versioned cases that include:

- case identifier and requirement trace
- priority
- preconditions and test data
- steps
- expected observable result
- automation status
- evidence required during execution

Cover normal flows, invalid actions, boundaries, state transitions, compatibility, and regressions. Freeze the applicable case version before acceptance execution.

### 3. Wait for implementation completion

Do not execute acceptance against an unfinished feature set. The programmer must declare all in-scope functionality complete and provide one identifiable candidate.

Build, typecheck, lint, or developer smoke checks may support implementation, but they do not replace QA acceptance.

### 4. Execute acceptance

Run every applicable frozen case against the completed candidate. Record the environment, result, evidence, and defect identifier for each failure.

Do not change expected results to match observed behavior.

### 5. Route defects and retest

- Implementation defects return to the programmer.
- Requirement ambiguity returns to the requirements owner for a product decision, then affected cases are revised and versioned by QA.
- Visual asset defects return to the responsible design role.

After a fix, retest the defect and run the affected regression set.

### 6. Issue the acceptance report

Report:

- candidate identifier
- test-case version
- environment
- pass, fail, blocked, and not-applicable counts
- unresolved defects by severity
- regression result
- final decision: passed or failed

## Success Criteria

- Test cases were created only from an explicitly confirmed planning baseline.
- Planning did not author, review, execute, or maintain test content.
- Acceptance ran only after the programmer declared the in-scope implementation complete.
- Every applicable case has a result and evidence.
- No release-blocking defect remains open.
- The final decision identifies both the candidate and test-case version.

## Verification

- Check the confirmation record and baseline version.
- Check test-case traceability against the confirmed requirements.
- Check the programmer's completion handoff and candidate identifier.
- Check that execution counts reconcile with the frozen case inventory.
- Check that every failed case links to a defect and every closed defect has a retest result.

## Stop Conditions

Stop and request resolution when:

- planning logic or scope is not explicitly confirmed
- a requirement has no determinate expected behavior
- the programmer has not declared the scoped implementation complete
- the acceptance candidate changes during execution
- required evidence or a required test environment is unavailable
