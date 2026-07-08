# ADR 0003: Domain Repository Pattern

## Context
The legacy application featured a monolithic `StorageService` that acted as a "God Object." It directly executed raw SQL queries, managed database connections, and leaked complex domain logic (such as deciding when to trigger training events) directly into the infrastructure layer.

## Decision
**Adopt the Repository Pattern to enforce boundary segregation.**
We strictly separated infrastructure access from domain logic. The singleton `DatabaseConnection` now exclusively handles psycopg2 connections and transaction contexts. Meanwhile, domain-specific repositories (e.g., `ConfigRepository`, `EventRepository`, `ItineraryRepository`) encapsulate all SQL execution and return purely typed domain objects.

## Alternatives Considered
- **Active Record / Heavy ORMs (e.g., SQLAlchemy)**: *Rejected*. Raw SQL via psycopg2 guarantees absolute query transparency, avoids N+1 ORM performance traps, and explicitly fulfills the portfolio requirement for explainable data access.
- **Refactoring `StorageService`**: *Rejected*. Attempting to patch the monolith would perpetually blur the line between SQL execution and business rules.

## Consequences
> [!TIP] 
> **Positive Outcomes**
> - **Testability**: Services can now be unit-tested seamlessly by mocking repository interfaces.
> - **Clean Architecture**: Business services orchestrate rules; repositories handle storage. SQL strings no longer leak into business logic.

> [!WARNING]
> **Negative Outcomes**
> - **Code Volume**: Increases boilerplate as SQL queries are explicitly defined within distinct repository classes rather than being dynamically generated.
