from dataclasses import dataclass
from datetime import datetime


@dataclass
class SystemConfig:
    id: int
    config_version: str
    active_model_id: int
    active_prompt_id: int
    active_dataset_id: int
    retry_schedule: dict[str, int]
    learning_enabled: bool
    evaluation_enabled: bool
    exports_enabled: bool
    updated_at: datetime
    updated_by: str
