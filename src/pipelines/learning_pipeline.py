from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.repositories.training_repository import TrainingRepository
import logging

logger = logging.getLogger(__name__)

class PipelineStage(ABC):
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass

class CollectStage(PipelineStage):
    def __init__(self, training_repo: TrainingRepository):
        self.training_repo = training_repo

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Executing CollectStage")
        # Collect pending items from the queue
        pending = self.training_repo.get_pending_tasks(limit=1000)
        context["pending_tasks"] = pending
        return context

class DatasetStage(PipelineStage):
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Executing DatasetStage")
        # In a full implementation, we'd build a JSONL dataset here using high quality items
        # from context["pending_tasks"].
        # For now, we simulate dataset building.
        context["new_dataset_version"] = "ds-v2"
        context["sample_count"] = len(context.get("pending_tasks", []))
        return context

class EvaluationStage(PipelineStage):
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Executing EvaluationStage")
        # Simulate deterministic evaluation of the dataset
        context["evaluation_passed"] = True
        context["structural_metrics"] = {"format": 100, "word_count": 90}
        context["semantic_metrics"] = {"destination_match": 100}
        return context

class PromotionStage(PipelineStage):
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Executing PromotionStage")
        if context.get("evaluation_passed"):
            # Promote the configuration
            context["new_model_version"] = "mv-v2"
            logger.info("Configuration promoted to production.")
        return context

class CleanupStage(PipelineStage):
    def __init__(self, training_repo: TrainingRepository):
        self.training_repo = training_repo
        
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Executing CleanupStage")
        # Mark tasks as completed
        for task in context.get("pending_tasks", []):
            self.training_repo.update_status(task['id'], 'completed')
        # Here we'd also archive datasets, remove temp exports, etc.
        return context

class LearningPipeline:
    def __init__(self, stages: List[PipelineStage]):
        self.stages = stages

    def run(self) -> Dict[str, Any]:
        context = {}
        logger.info("Starting LearningPipeline")
        try:
            for stage in self.stages:
                context = stage.execute(context)
            logger.info("LearningPipeline completed successfully")
        except Exception as e:
            logger.error(f"LearningPipeline failed: {e}")
            context["error"] = str(e)
        return context
