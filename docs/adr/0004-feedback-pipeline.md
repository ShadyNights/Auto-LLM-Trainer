# ADR 0004: Continuous Feedback Learning Pipeline

## Context
The original system claimed to be a "Self-Training LLM System", which technically implied automatic weight updates (Fine-tuning, LoRA). In reality, it built datasets from feedback and promoted inference configurations (prompts).

## Decision
We formalized this as the **Continuous Feedback Learning Pipeline**. It is implemented via a strict orchestration interface (`LearningPipeline`) divided into independent stages (`Collect`, `Dataset`, `Evaluate`, `Promote`, `Cleanup`).

## Alternatives Considered
- **Actual LoRA/SFT Integration**: Rejected for the current scope.
- **Monolithic Training Script**: Rejected because it prevented independent scaling or testing of the evaluation vs dataset building phases.

## Consequences
- **Positive**: Honest terminology. The pipeline stages are independently testable and idempotent. The interface is ready for a future `TrainerStage` without architectural changes.
- **Negative**: None. Provides a cleaner, scalable operational model.
