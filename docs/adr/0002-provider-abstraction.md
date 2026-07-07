# ADR 0002: Provider Abstraction

## Context
The application originally hardcoded Groq API calls directly into the `PlannerService` (or equivalent orchestration logic). This tightly coupled the business logic to a specific vendor's SDK, making it difficult to swap LLMs.

## Decision
We introduced a strict `ProviderInterface` defining a single `generate(request: ProviderRequest) -> ProviderResponse` method. The `ProviderRequest` is a structured DTO.

## Alternatives Considered
- **LangChain / LlamaIndex Integration**: Rejected to prevent framework bloat and keep the architecture lightweight and understandable.
- **Multi-Method Interface**: `generate_itinerary()`, `evaluate_text()`. Rejected in favor of a single, generic `generate` method that accepts varied prompts.

## Consequences
- **Positive**: Adding a new provider (e.g., OpenAIProvider, GeminiProvider) requires zero changes to the `PlannerService`. Standardized metric reporting (latency, token usage) across all providers.
- **Negative**: Minor initial overhead defining DTOs for standardizing the request/response shapes.
