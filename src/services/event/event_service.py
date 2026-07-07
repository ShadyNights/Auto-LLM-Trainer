import uuid
from typing import Dict, Any
from src.repositories.event_repository import EventRepository
from src.domain.enums.event_type import EventType

class EventService:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def start_conversation(self, user_id: int = 1) -> int:
        return self.event_repo.create_conversation(user_id=user_id)

    def log_prompt_submitted(self, conversation_id: int, city: str, budget: str, trip_days: int) -> str:
        correlation_id = str(uuid.uuid4())
        payload = {
            "city": city,
            "budget": budget,
            "trip_days": trip_days
        }
        self.event_repo.log_event(conversation_id, correlation_id, EventType.PROMPT_SUBMITTED, payload)
        return correlation_id

    def log_generation(self, conversation_id: int, correlation_id: str, success: bool, error: str = None):
        event_type = EventType.GENERATION_COMPLETED if success else EventType.FAILURE
        payload = {"success": success}
        if error:
            payload["error"] = error
        self.event_repo.log_event(conversation_id, correlation_id, event_type, payload)

    def log_feedback(self, conversation_id: int, correlation_id: str, rating: int, comments: str):
        payload = {
            "rating": rating,
            "comments": comments
        }
        self.event_repo.log_event(conversation_id, correlation_id, EventType.FEEDBACK, payload)

    def log_action(self, conversation_id: int, correlation_id: str, action: EventType):
        self.event_repo.log_event(conversation_id, correlation_id, action, {})
