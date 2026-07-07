# ADR 0005: Prompt Versioning in Filesystem

## Context
Prompts were originally stored directly in the PostgreSQL database or hardcoded in Python files, making it difficult to track changes via Git or review prompt diffs.

## Decision
Prompt templates are stored in the filesystem (e.g., `prompts/travel/v1.md`). The database (`prompts_metadata` table) stores the `version_name` and a `checksum` (SHA256) of the file contents.

## Alternatives Considered
- **Database-Only Storage**: Rejected because it prevents standard code-review practices for prompts.
- **Python-Only Storage**: Rejected because prompts are configuration/data, not code, and may need to be updated dynamically or moved to S3 eventually.

## Consequences
- **Positive**: Prompts are version-controlled in Git. The database checksum ensures runtime integrity (startup validations fail if the file was modified without a database sync).
- **Negative**: Requires a synchronization step to update the database when a prompt file changes.
