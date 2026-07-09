import json
from typing import Any

from src.infrastructure.database.connection import DatabaseConnection


class EventRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def create_conversation(self, user_id: int = 1) -> int:
        with self.db.get_cursor() as cur:
            cur.execute("INSERT INTO conversations (user_id) VALUES (%s) RETURNING id", (user_id,))
            return cur.fetchone()["id"]

    def log_event(
        self,
        conversation_id: int,
        correlation_id: str,
        event_type: str,
        payload: dict[str, Any],
        actor: str = "system",
        version: str = "1.0",
    ) -> int:
        with self.db.get_cursor() as cur:
            cur.execute(
                """INSERT INTO events (conversation_id, correlation_id, event_type, payload, actor, version) 
                   VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
                (conversation_id, correlation_id, event_type, json.dumps(payload), actor, version),
            )
            return cur.fetchone()["id"]
