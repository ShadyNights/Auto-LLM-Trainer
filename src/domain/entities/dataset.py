from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Dataset:
    id: Optional[int]
    version_name: str
    sample_count: int
    average_quality: float
    parent_dataset_id: Optional[int]
    created_by_pipeline_version: str
    language: str = 'en'
    source: str = 'feedback'
    created_at: Optional[datetime] = None
