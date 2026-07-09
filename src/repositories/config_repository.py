from src.domain.entities.system_config import SystemConfig
from src.infrastructure.database.connection import DatabaseConnection


class ConfigRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def get_active_config(self) -> SystemConfig | None:
        with self.db.get_cursor(commit_on_success=False) as cur:
            cur.execute("SELECT * FROM system_config WHERE id = 1")
            row = cur.fetchone()
            if row:
                return SystemConfig(
                    id=row["id"],
                    config_version=row["config_version"],
                    active_model_id=row["active_model_id"],
                    active_prompt_id=row["active_prompt_id"],
                    active_dataset_id=row["active_dataset_id"],
                    retry_schedule=row.get("retry_schedule", {}),
                    learning_enabled=row.get("learning_enabled", True),
                    evaluation_enabled=row.get("evaluation_enabled", True),
                    exports_enabled=row.get("exports_enabled", True),
                    updated_at=row["updated_at"],
                    updated_by=row["updated_by"],
                )
        return None

    def update_config_version(self, new_version: str, updated_by: str = "system"):
        with self.db.get_cursor() as cur:
            cur.execute(
                """
                UPDATE system_config 
                SET config_version = %s, updated_at = NOW(), updated_by = %s
                WHERE id = 1
            """,
                (new_version, updated_by),
            )
