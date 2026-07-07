# System Architecture

## Overview
Traveler LLM is a production-grade AI Travel Planner powered by a **Continuous Feedback Learning Pipeline**. It leverages PostgreSQL as a single source of truth for all operational data, state, events, and background task queues.

## Core Layers
The architecture adheres to strict dependency rules (`UI -> Services -> Providers/Repositories -> Infrastructure`).

### 1. UI Layer (Streamlit)
Located in `app.py` (and potentially `src/ui/`), this layer manages user interactions, renders dashboards, and performs startup health checks (Database, Config, Provider Keys, Prompt Checksums).

### 2. Services Layer
Encapsulates all business logic:
- **PlannerService**: Orchestrates itinerary generation by fetching prompts via `PromptRepository` and calling the `ProviderInterface`.
- **EventService**: Standardizes and logs user interactions as strictly-typed events linked to a `conversation_id`.

### 3. Pipeline Layer
The `LearningPipeline` is divided into independent stages:
- **Collect**: Gathers pending feedback tasks.
- **Dataset**: Builds new dataset iterations.
- **Evaluate**: Performs structural and semantic validation on outputs.
- **Promote**: Updates the `model_versions` registry.
- **Cleanup**: Archives old data and resolves queue tasks.

### 4. Provider Abstraction
The `ProviderInterface` exposes a single `generate(request)` method. `GroqProvider` implements this to interact with LLaMA models, tracking latency, token usage, and cost estimates independently of the business logic.

### 5. Infrastructure Layer
- **PostgreSQL**: Stores all relational data.
- **DatabaseConnection**: A singleton context manager to handle psycopg2 cursors and transactions safely.
- **JSON Logger**: Emits structured logs containing operational metadata (correlation ID, conversation ID, duration).
