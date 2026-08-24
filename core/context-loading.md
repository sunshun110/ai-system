# Context Loading

AI should not read a whole repository blindly. It should load context by routing.

## Source Priority

1. User request
2. Project `AGENTS.md` or equivalent
3. Module index
4. Local README or domain rule documents
5. Nearby source files
6. Tests and usage sites
7. Tool-specific adapter instructions

## Module Index Pattern

A module index should answer:

- Which directories exist?
- Which documents must be read before changing each area?
- Which directories are generated, third-party, or build output?
- Which files are safe to edit?

It should not contain long summaries that drift out of date.

## Domain Packs

Domain-specific knowledge belongs in `domains/<domain>/`.

Examples:

- `domains/backend-service/`
- `domains/frontend-app/`
- `domains/data-pipeline/`

Core workflows may call into a domain pack when the target project opts into it.
