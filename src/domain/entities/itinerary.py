from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Itinerary:
    id: int | None
    conversation_id: int
    trip_id: int
    itinerary_text: str
    prompt_id: int
    model_version_id: int
    configuration_snapshot: dict[str, Any]
    word_count: int
    rating: int | None = None
    feedback_comments: str | None = None
    quality_score: float | None = None
    created_at: datetime | None = None
    rated_at: datetime | None = None
