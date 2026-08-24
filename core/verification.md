# Verification

Every workflow should define how success is checked.

## Verification Ladder

Use the strongest practical check:

1. Automated tests
2. Typecheck / lint / build
3. Targeted command output
4. Reproduction steps
5. Manual inspection checklist

## Report Format

At completion, report:

- files changed
- checks run
- checks skipped
- residual risk

## Coverage Accounting

For scanning workflows, report:

- baseline file count
- files scanned
- excluded files and reasons
- gaps that require follow-up
