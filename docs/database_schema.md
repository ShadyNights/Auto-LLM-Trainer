# Database Schema

PostgreSQL serves as the single source of truth.

## Core Entities
- **conversations**: Tracks unique user sessions.
- **events**: Strictly-typed user interactions (`event_type`), linked via `correlation_id` and `conversation_id`. Contains a `payload` JSONB column for flexible metric storage.
- **itineraries**: The generated output. Stores a `configuration_snapshot` to freeze the settings (temperature, provider) used during generation.

## Registry & Lineage
- **prompts_metadata**: Tracks prompt file checksums and activation status.
- **datasets**: Records datasets built by the learning pipeline. Tracks lineage via `parent_dataset_id`.
- **model_versions**: Represents inference configurations (Provider + Model + Prompt + Dataset). Tracks history via `previous_version_id`.
- **config_evaluations**: Stores `structural_metrics` and `semantic_metrics` for configurations.

## State Management
- **system_config**: A single-row table managing active configurations, feature flags (`learning_enabled`), and retry schedules.
- **training_queue**: The background job queue. Tracks retries, durations, error messages, and supports a Dead Letter Queue (`status = 'dead'`).
