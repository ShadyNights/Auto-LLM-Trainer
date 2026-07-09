import argparse
import logging
import sys

from src.infrastructure.database.connection import DatabaseConnection
from src.pipelines.learning_pipeline import (
    CleanupStage,
    CollectStage,
    DatasetStage,
    EvaluationStage,
    LearningPipeline,
    PromotionStage,
)
from src.repositories.training_repository import TrainingRepository

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("background_jobs")


def run_train():
    logger.info("Starting Dataset Builder (train) job")
    db = DatabaseConnection()
    training_repo = TrainingRepository(db)

    # In a real distributed system, we would just run Collect + Dataset
    pipeline = LearningPipeline([CollectStage(training_repo), DatasetStage()])
    pipeline.run()


def run_evaluate():
    logger.info("Starting Evaluation job")
    # In reality, this would evaluate a built dataset/model version
    pipeline = LearningPipeline([EvaluationStage()])
    pipeline.run()


def run_promote():
    logger.info("Starting Promotion job")
    db = DatabaseConnection()
    training_repo = TrainingRepository(db)

    # We might run the full pipeline in a single script for simplicity, or just Promote + Cleanup
    pipeline = LearningPipeline([PromotionStage(), CleanupStage(training_repo)])
    pipeline.run()


import os

from dotenv import load_dotenv


def main():
    load_dotenv()

    # Map local DB vars to PG env vars expected by connection
    if os.getenv("DB_HOST"):
        os.environ["PGHOST"] = os.getenv("DB_HOST")
    if os.getenv("DB_PORT"):
        os.environ["PGPORT"] = os.getenv("DB_PORT")
    if os.getenv("DB_NAME"):
        os.environ["PGDATABASE"] = os.getenv("DB_NAME")
    if os.getenv("DB_USER"):
        os.environ["PGUSER"] = os.getenv("DB_USER")
    if os.getenv("DB_PASSWORD"):
        os.environ["PGPASSWORD"] = os.getenv("DB_PASSWORD")

    parser = argparse.ArgumentParser(description="Background Jobs CLI for Traveler LLM")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("train", help="Run the dataset building stage")
    subparsers.add_parser("evaluate", help="Run the evaluation stage")
    subparsers.add_parser("promote", help="Run the promotion and cleanup stages")
    subparsers.add_parser("pipeline", help="Run the full Learning Pipeline end-to-end")

    args = parser.parse_args()

    try:
        if args.command == "train":
            run_train()
        elif args.command == "evaluate":
            run_evaluate()
        elif args.command == "promote":
            run_promote()
        elif args.command == "pipeline":
            db = DatabaseConnection()
            training_repo = TrainingRepository(db)
            pipeline = LearningPipeline(
                [
                    CollectStage(training_repo),
                    DatasetStage(),
                    EvaluationStage(),
                    PromotionStage(),
                    CleanupStage(training_repo),
                ]
            )
            pipeline.run()
    except Exception as e:
        logger.error(f"Job execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
