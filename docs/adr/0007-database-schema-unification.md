# ADR 0007: Database Schema Unification

## Context
Historically, the PostgreSQL database was assembled via heavily fragmented initialization scripts and manual hotfixes. Worse, the architecture heavily abused PostgreSQL triggers to orchestrate complex domain workflows—such as automatically copying data to training tables based on rating thresholds. This tight coupling between data storage and business logic caused opaque failures, silent errors, and made local testing nearly impossible.

## Decision
**Unify the schema and strictly eradicate business logic triggers.**
We collapsed the entire database initialization into a single, cohesive schema (`migrations/001_initial_schema.sql`). 
1. **Trigger Eradication**: All orchestrating database triggers were permanently deleted. Workflow execution was shifted entirely to the application layer (specifically via the `training_queue` and `background_jobs.py`).
2. **Pure Helper Functions**: We introduced pure, side-effect-free SQL functions (`calculate_quality_score()`, `extract_training_sample()`) to handle data formatting for the background workers *without* triggering automated state changes.

## Alternatives Considered
- **Incremental Migration Systems (Flyway/Alembic)**: *Rejected* at this specific milestone. Because we were overhauling a fragmented prototype into a clean production baseline, maintaining the messy history of the prototype was unnecessary overhead.
- **Retaining "Real-time" Database Triggers**: *Rejected* because database triggers are notoriously difficult to monitor, debug, scale, and version control. 

## Consequences
> [!TIP] 
> **Positive Outcomes**
> - **Deployment Simplicity**: The entire platform database spins up from a single initialization script.
> - **Predictability**: Eradicating triggers means the database acts strictly as a passive ledger. When an event occurs, it is recorded without causing unpredictable, cascading background mutations.

> [!WARNING]
> **Negative Outcomes**
> - **Application Overhead**: The application layer must now explicitly manage the asynchronous queuing of training events (e.g., executing `training_repo.enqueue()`). This adds slight boilerplate but drastically improves system observability.
