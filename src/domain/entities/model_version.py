from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ModelVersion:
    id: Optional[int]
    version_name: str
    provider: str
    provider_model: str
    prompt_version: str
    dataset_version: str
    previous_version_id: Optional[int]
    status: str
    release_notes: Optional[str]
    created_at: Optional[datetime] = None
