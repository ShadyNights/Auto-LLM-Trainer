# ADR 0005: Filesystem Prompt Versioning

## Context
System prompts were historically either stored entirely within the PostgreSQL database or hardcoded randomly across Python files. This fragmentation made it impossible to track prompt evolution via Git, conduct rigorous peer reviews on prompt diffs, or maintain consistency across environments.

## Decision
**Prompts are version-controlled in the filesystem; integrity is guaranteed by the database.**
All prompt templates are stored as Markdown files (e.g., `prompts/travel/v1.md`). The database (`prompts_metadata` table) acts as the registry, storing the active `version_name` alongside a strict **SHA256 checksum** of the expected file contents.

## Alternatives Considered
- **Database-Only Storage**: *Rejected* as it bypasses Git version control, preventing standard CI/CD code-review workflows for prompt engineering.
- **Python-Only Storage**: *Rejected*. Prompts represent data/configuration, not application code. Tightly coupling them to Python files complicates dynamic updates and future migrations to block storage (S3).

## Consequences
> [!TIP] 
> **Positive Outcomes**
> - **Git Ops**: Prompts are rigorously version-controlled.
> - **Runtime Integrity**: Application startup validations actively hash the filesystem prompt. If the file was modified without a corresponding database registry update, the system halts, preventing silent divergence.

> [!WARNING]
> **Negative Outcomes**
> - **Synchronization**: Introducing or modifying a prompt requires a strict two-step process: commit the file, then execute a database sync to update the checksum registry.
