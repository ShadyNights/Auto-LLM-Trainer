from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class Event:
    id: Optional[int]
    conversation_id: int
    correlation_id: str
    event_type: str
    occurred_at: datetime
    actor: str
    payload: Dict[str, Any]
    version: str = "1.0"
