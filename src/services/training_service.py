from src.services.storage_service import StorageService
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TrainingService:
    def __init__(self, storage_service: StorageService):
        self.storage = storage_service

    def process_training_queue(self):
        """Process pending items in the training queue to build a new dataset."""
        logger.info("Starting to process training queue...")
        
        # 1. Get pending queue items
        query_pending = """
            SELECT q.id as queue_id, i.id as itinerary_id, i.rating, i.quality_score,
                   i.trip_id, i.itinerary_text, i.feedback_comments
            FROM training_queue q
            JOIN itineraries i ON q.itinerary_id = i.id
            WHERE q.status = 'pending'
            LIMIT 50
        """
        pending_items = self.storage.execute_query(query_pending, fetch=True)
        
        if not pending_items:
            logger.info("No pending items in training queue.")
            return None

        logger.info(f"Processing {len(pending_items)} pending items.")
        
        # 2. Mark as processing
        queue_ids = [item['queue_id'] for item in pending_items]
        self.storage.execute_query(
            "UPDATE training_queue SET status = 'processing', updated_at = NOW() WHERE id = ANY(%s)",
            (queue_ids,)
        )

        # 3. Calculate metrics for the new dataset
        valid_items = [item for item in pending_items if item['quality_score'] is not None]
        if not valid_items:
            self.storage.execute_query(
                "UPDATE training_queue SET status = 'failed', updated_at = NOW() WHERE id = ANY(%s)",
                (queue_ids,)
            )
            return None

        sample_count = len(valid_items)
        avg_quality = sum(item['quality_score'] for item in valid_items) / sample_count
        
        # 4. Create new Dataset version
        import uuid
        dataset_version = f"dataset-v{uuid.uuid4().hex[:6]}"
        
        insert_dataset_query = """
            INSERT INTO datasets (version_name, sample_count, average_quality)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        dataset_id = None
        with self.storage.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_dataset_query, (dataset_version, sample_count, avg_quality))
                dataset_id = cursor.fetchone()[0]

        # 5. Mark queue items as completed
        self.storage.execute_query(
            "UPDATE training_queue SET status = 'completed', updated_at = NOW() WHERE id = ANY(%s)",
            (queue_ids,)
        )

        logger.info(f"Dataset {dataset_version} created with {sample_count} samples.")
        return dataset_id
