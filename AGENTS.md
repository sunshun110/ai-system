# AI System Project Rules

## Assumptions

This project is not an application feature. It is a reusable AI operating system for engineering work and the home of one company's shared roles and business departments.

When editing it:

- Keep the core vendor-neutral.
- Put company-wide staff roles and organization workflows under `company/`.
- Put business-line differences under `company/departments/<department>/`; website, H5, and Unity business lines are departments of the same company.
- Put Claude/Codex/Cursor-specific material under `adapters/`.
- Put optional technical knowledge packs under `domains/`; do not model company departments as domains.
- Put reusable task procedures under `workflows/`.
- Put reusable role definitions under `agents/`.
- Put installation scaffolds under `templates/`.

## Working Rules

- State assumptions before changing structure.
- Prefer small, direct documents over broad abstractions.
- Do not duplicate the same rule in many places; link to the source of truth.
- Keep shared job capabilities in `company/roles/`; departments may extend them but must not copy the full role definition.
- Follow the workspace context handoff rule; use this project's `handoff.md` for cross-conversation continuity.
- Preserve legacy material when extracting or generalizing it.
- Every workflow must include success criteria and verification.
- Every risky workflow must define when AI must stop and ask for confirmation.

## Folder Ownership

| Folder | Purpose |
|---|---|
| `company/` | Shared company roles, cross-department learning, and business departments. |
| `core/` | Non-negotiable operating rules and mental model. |
| `docs/` | Reusable, on-demand knowledge documents. |
| `workflows/` | Task procedures. |
| `agents/` | Specialist AI role definitions. |
| `adapters/` | Tool-specific packaging. |
| `domains/` | Optional domain packs. |
| `templates/` | Project onboarding templates. |
