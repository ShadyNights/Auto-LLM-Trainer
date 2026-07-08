# ADR 0004: Continuous Feedback Learning Pipeline

## Context
The platform's original premise marketed a "Self-Training LLM System." This misleadingly implied active, automated neural network weight updates (Fine-tuning, LoRA) occurring in real-time. In reality, the system merely aggregated user feedback, curated datasets, and promoted distinct inference configurations via prompts.

## Decision
**Formalize the architecture as the "Continuous Feedback Learning Pipeline."**
We established a strict, modular orchestration interface (`LearningPipeline`) that divides the process into independent, asynchronous stages: 
1. **Collect** (Gathering pending feedback)
2. **Dataset** (Building curated training subsets)
3. **Evaluate** (Benchmarking configuration performance)
4. **Promote** (Updating the active `model_versions` registry)
5. **Cleanup** (Resolving task queues)

## Alternatives Considered
- **Real-time LoRA / SFT Integration**: *Rejected* for the current MVP scope due to the immense infrastructure complexity and cost of automated hardware fine-tuning.
- **Monolithic Training Script**: *Rejected* because a single massive script prevents independent staging, isolated testing, and precise failure recovery.

## Consequences
> [!TIP] 
> **Positive Outcomes**
> - **Honest Architecture**: Terminology now accurately reflects the system's capabilities.
> - **Scalability**: Because stages are modular and idempotent, we can easily inject an actual `TrainerStage` (for API-based fine-tuning) in the future without altering the pipeline architecture.

> [!WARNING]
> **Negative Outcomes**
> - None. This decision provides a definitively cleaner and more scalable operational model.
