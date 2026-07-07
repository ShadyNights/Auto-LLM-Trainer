from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class Itinerary:
    id: Optional[int]
    conversation_id: int
    trip_id: int
    itinerary_text: str
    prompt_id: int
    model_version_id: int
    configuration_snapshot: Dict[str, Any]
    word_count: int
    rating: Optional[int] = None
    feedback_comments: Optional[str] = None
    quality_score: Optional[float] = None
    created_at: Optional[datetime] = None
    rated_at: Optional[datetime] = None
