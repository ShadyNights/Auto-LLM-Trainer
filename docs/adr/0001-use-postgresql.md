# ADR 0001: Use PostgreSQL as the Single Source of Truth

## Context
The original architecture relied on a dual-storage system (JSON files for active operations and PostgreSQL for backup/analytics), orchestrated via database triggers. This led to a "God Service" pattern, complex debugging, and race conditions.

## Decision
We will use PostgreSQL as the sole source of truth for all operational data, state, events, and queues. JSON files will no longer be written synchronously during application operation. Database triggers orchestrating ML pipelines are removed.

## Alternatives Considered
- **Dual-Storage Optimization**: Maintaining the JSON active store but removing triggers. Rejected due to inherent synchronization complexity.
- **NoSQL / MongoDB**: Rejected because the data is highly relational (Conversations -> Events -> Itineraries -> Queue).

## Consequences
- **Positive**: Simplified state management. Strong ACID guarantees. Centralized metrics reporting via SQL views.
- **Negative**: Requires robust database connection management in the Python backend (mitigated by introducing a connection pool manager).
