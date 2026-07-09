from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Event:
    id: int | None
    conversation_id: int
    correlation_id: str
    event_type: str
    occurred_at: datetime
    actor: str
    payload: dict[str, Any]
    version: str = "1.0"
