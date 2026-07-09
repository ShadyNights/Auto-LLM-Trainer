from typing import Optional, Dict, Any
from src.infrastructure.database.connection import DatabaseConnection
import json

class ItineraryRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def create_itinerary(self, conversation_id: int, itinerary_text: str, prompt_id: int, model_version_id: int, config_snapshot: Dict[str, Any], word_count: int, trip_id: int = None, generation_time_ms: int = 0) -> int:
        with self.db.get_cursor() as cur:
            cur.execute(
                """INSERT INTO itineraries (conversation_id, itinerary_text, prompt_id, model_version_id, configuration_snapshot, word_count, trip_id, generation_time_ms) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (conversation_id, itinerary_text, prompt_id, model_version_id, json.dumps(config_snapshot), word_count, trip_id, generation_time_ms)
            )
            return cur.fetchone()['id']

    def update_rating(self, itinerary_id: int, rating: int, feedback: str):
        with self.db.get_cursor() as cur:
            cur.execute(
                """UPDATE itineraries 
                   SET rating = %s, feedback_comments = %s, rated_at = NOW() 
                   WHERE id = %s""",
                (rating, feedback, itinerary_id)
            )
