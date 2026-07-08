# ADR 0001: PostgreSQL as Single Source of Truth

## Context
The legacy architecture utilized a fragile dual-storage system: synchronous JSON files for active session operations, combined with PostgreSQL for asynchronous backup and analytics. This dual-write pattern necessitated complex database triggers, caused severe race conditions, and created an unmaintainable "God Service" bottleneck.

## Decision
**PostgreSQL is now the exclusive, single source of truth.**
We have entirely eradicated synchronous JSON storage and database triggers. All operational data, session state, telemetry events, and background learning queues are managed strictly within relational PostgreSQL tables. 

## Alternatives Considered
- **Optimized Dual-Storage**: Maintaining the JSON active store but removing triggers. *Rejected* due to the inherent complexity of eventual consistency and synchronization overhead.
- **NoSQL / MongoDB Migration**: *Rejected* because the platform's core data model (Conversations ➔ Events ➔ Itineraries ➔ Queues) is inherently relational and benefits from strict ACID guarantees.

## Consequences
> [!TIP] 
> **Positive Outcomes**
> - **Absolute Data Integrity**: ACID guarantees eliminate race conditions.
> - **Simplified State Management**: The application layer no longer attempts to synchronize multiple data stores.
> - **Observability**: Centralized metrics reporting via simple SQL views.

> [!WARNING]
> **Negative Outcomes**
> - **Connection Overhead**: Requires robust connection pool management in the Python backend (mitigated by our singleton `DatabaseConnection` manager).
