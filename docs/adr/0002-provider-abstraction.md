# ADR 0002: Strict Provider Abstraction

## Context
In previous iterations, Groq SDK API calls were hardcoded directly into the orchestration layer (`PlannerService`). This tight coupling bound the platform's business logic to a single vendor's specific SDK shape, making model evaluation, vendor swapping, or hybrid-routing architecturally impossible.

## Decision
**Implement a strict `ProviderInterface` contract.**
We introduced a decoupled interface defining a solitary `generate(request: ProviderRequest) -> ProviderResponse` contract using strictly-typed Data Transfer Objects (DTOs). The core business logic now interacts exclusively with this interface. The `GroqProvider` is merely one concrete implementation of this contract.

## Alternatives Considered
- **LangChain / LlamaIndex**: *Rejected*. While these frameworks offer provider abstraction, they introduce immense dependency bloat and obscure the execution trace. A lightweight, native interface keeps our architecture transparent.
- **Multi-Method Interfaces**: Creating separate methods like `generate_itinerary()` and `evaluate_text()`. *Rejected*. A single, generic `generate` method accepting varied prompt payloads is vastly more scalable.

## Consequences
> [!TIP] 
> **Positive Outcomes**
> - **Vendor Agnosticism**: Introducing new LLM providers (e.g., OpenAI, Anthropic, Gemini) requires zero modifications to the core `PlannerService`.
> - **Standardized Telemetry**: Latency, token usage, and cost estimates are captured uniformly across all providers via the interface layer.

> [!WARNING]
> **Negative Outcomes**
> - **Mapping Overhead**: Requires explicit DTO mapping between the application's domain model and the specific vendor's expected JSON schema.
