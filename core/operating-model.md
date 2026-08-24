# Operating Model

The AI system works in five phases.

## 1. Orient

Identify:

- target project
- relevant rules
- task type
- risk level
- success criteria

## 2. Load Context

Read only the context needed for the task:

- project rules
- module index
- relevant README files
- nearby code
- workflow documents
- domain pack documents

## 3. Plan

For non-trivial work, state:

- assumptions
- steps
- verification method
- risk gates

## 4. Execute

Make the smallest direct change that satisfies the task.

Avoid:

- unrelated formatting
- speculative cleanup
- broad rewrites
- silent behavior changes

## 5. Verify and Report

Run the relevant checks. Then report:

- what changed
- where it changed
- what was verified
- remaining risks
