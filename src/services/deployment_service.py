from src.services.storage_service import StorageService
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DeploymentService:
    def __init__(self, storage_service: StorageService):
        self.storage = storage_service

    def promote_candidate(self, model_id: int, dataset_id: int):
        """Promote a candidate model to be the active production model."""
        logger.info(f"Promoting candidate model_id={model_id} to active configuration")
        
        # 1. Update model status to 'approved'
        self.storage.execute_query(
            "UPDATE models SET status = 'approved' WHERE id = %s",
            (model_id,)
        )
        
        # 2. Update system config
        # Get the prompt_id associated with this model
        model_info = self.storage.execute_query("SELECT prompt_id FROM models WHERE id = %s", (model_id,), fetch_one=True)
        prompt_id = model_info['prompt_id'] if model_info else None

        query_config = """
            UPDATE system_config 
            SET active_model_id = %s, active_prompt_id = %s, active_dataset_id = %s, updated_at = NOW()
            WHERE id = 1
        """
        self.storage.execute_query(query_config, (model_id, prompt_id, dataset_id))

        # 3. Write to audit_logs
        import json
        audit_details = {
            "new_model_id": model_id,
            "new_dataset_id": dataset_id,
            "new_prompt_id": prompt_id
        }
        query_audit = """
            INSERT INTO audit_logs (action, details)
            VALUES ('Worker promoted model', %s)
        """
        self.storage.execute_query(query_audit, (json.dumps(audit_details),))

        logger.info(f"Successfully promoted model_id={model_id}. System config updated.")
