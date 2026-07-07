from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Conversation:
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
