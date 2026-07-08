# ADR 0007: Database Schema Unification and Trigger Removal

## Context
Historically, the PostgreSQL database was built via fragmented initialization scripts (`001_baseline.sql`, `002_architecture_overhaul.sql`, and various manual hotfixes like `fix_triggers.sql`). Additionally, the original architecture relied heavily on PostgreSQL triggers to orchestrate complex domain workflows—such as automatically copying data to a `training_data` table when a rating crossed a certain threshold. This tight coupling between data storage and business logic caused opaque failures, silent errors, and made local testing incredibly difficult.

## Decision
We decided to completely unify the database initialization into a single, cohesive schema (`migrations/001_initial_schema.sql`) and strictly enforce that the database acts **only** as a source of truth for state.
1. **Unification**: All fragmented hotfixes and outdated schemas were permanently deleted.
2. **Trigger Eradication**: All orchestrating database triggers were removed. Business logic and training workflow execution were shifted entirely to the application layer (specifically, the `training_queue` processed by `background_jobs.py`).
3. **Pure Helper Functions**: We introduced pure, side-effect-free SQL functions (like `calculate_quality_score()` and `extract_training_sample()`) to assist the background workers with data formatting, without triggering automated state changes.

## Alternatives Considered
- **Maintaining Incremental Migrations (Flyway/Alembic)**: Rejected at this stage. Given that the prototype was being overhauled into a production baseline, maintaining the messy history of the prototype was unnecessary overhead. A clean `001_initial_schema.sql` establishes a much stronger, documented V1 starting point.
- **Keeping Triggers for "Real-time" ML**: Rejected because database triggers are notoriously difficult to monitor, debug, and scale. Orchestration belongs in the application layer.

## Consequences
- **Positive**: The deployment footprint is simplified to a single initialization file. Eradicating triggers means that when an itinerary is generated or rated, the database merely records it, avoiding silent cascade failures. The architecture is now highly predictable and testable.
- **Negative**: The application layer must now explicitly manage the asynchronous queuing of training events (e.g., manually calling `training_repo.enqueue(itin_id)`). This adds slightly more boilerplate to the Python services but drastically improves system observability.
