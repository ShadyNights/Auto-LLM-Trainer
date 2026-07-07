# ADR 0003: Repository Pattern

## Context
The initial `StorageService` functioned as a "God Object", containing raw SQL execution, connection handling, and complex business logic (like deciding when to enqueue a training task).

## Decision
We implemented the Repository Pattern to strictly separate infrastructure (SQL) from domain logic. `DatabaseConnection` handles the connection, while specific repositories (`ConfigRepository`, `EventRepository`, etc.) handle SQL queries for specific domain entities.

## Alternatives Considered
- **Active Record (ORM like SQLAlchemy)**: Rejected because raw SQL (via psycopg2) provides absolute clarity, avoids ORM overhead, and matches the portfolio's explicit requirement for explainable data access.
- **Retaining StorageService**: Rejected due to the inability to scale and maintain boundaries.

## Consequences
- **Positive**: Services no longer contain SQL. Repositories only contain CRUD methods. High testability.
- **Negative**: Increases the number of files and boilerplate code.
