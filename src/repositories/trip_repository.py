from typing import Optional
from src.infrastructure.database.connection import DatabaseConnection
from src.domain.dto.ui_dtos import TripSummaryDTO

class TripRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def create_trip(self, destination: str, duration: int, budget_level: str, travel_style: list, interests: list) -> int:
        with self.db.get_cursor() as cur:
            cur.execute("""
                INSERT INTO trips (destination, duration, budget_level, travel_style, interests)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (destination, duration, budget_level, travel_style, interests))
            return cur.fetchone()['id']

    def get_trip_summary(self, itinerary_id: int) -> Optional[TripSummaryDTO]:
        try:
            with self.db.get_cursor() as cur:
                cur.execute("""
                    SELECT 
                        t.destination, t.duration, t.budget_level, t.travel_style, t.interests,
                        i.itinerary_text, i.generation_time_ms, i.rating, i.quality_score, i.conversation_id, i.created_at,
                        m.provider, p.version_name as prompt_version, m.version_name as model_version
                    FROM itineraries i
                    JOIN trips t ON i.trip_id = t.id
                    LEFT JOIN model_versions m ON i.model_version_id = m.id
                    LEFT JOIN prompts_metadata p ON i.prompt_id = p.id
                    WHERE i.id = %s
                """, (itinerary_id,))
                
                row = cur.fetchone()
                if not row:
                    return None
                    
                complexity = len(row['interests'] if row['interests'] else []) * row['duration']
                
                return TripSummaryDTO(
                    destination=row['destination'],
                    duration=row['duration'],
                    budget=row['budget_level'],
                    travel_style=row['travel_style'] or [],
                    interests=row['interests'] or [],
                    trip_complexity=complexity,
                    generation_time_ms=row['generation_time_ms'],
                    itinerary_text=row['itinerary_text'],
                    provider=row['provider'] or "Unknown",
                    prompt_version=row['prompt_version'] or "Unknown",
                    model_version=row['model_version'] or "Unknown",
                    conversation_id=row['conversation_id'],
                    created_at=row['created_at'],
                    quality_score=row['quality_score'],
                    rating=row['rating']
                )
        except Exception:
            return None

    def get_recent_trip_summaries(self, limit: int = 10) -> list[TripSummaryDTO]:
        try:
            with self.db.get_cursor() as cur:
                cur.execute("""
                    SELECT 
                        t.destination, t.duration, t.budget_level, t.travel_style, t.interests,
                        i.itinerary_text, i.generation_time_ms, i.rating, i.quality_score, i.conversation_id, i.created_at,
                        m.provider, p.version_name as prompt_version, m.version_name as model_version
                    FROM itineraries i
                    JOIN trips t ON i.trip_id = t.id
                    LEFT JOIN model_versions m ON i.model_version_id = m.id
                    LEFT JOIN prompts_metadata p ON i.prompt_id = p.id
                    ORDER BY i.created_at DESC
                    LIMIT %s
                """, (limit,))
                
                rows = cur.fetchall()
                results = []
                for row in rows:
                    complexity = len(row['interests'] if row['interests'] else []) * row['duration']
                    results.append(TripSummaryDTO(
                        destination=row['destination'],
                        duration=row['duration'],
                        budget=row['budget_level'],
                        travel_style=row['travel_style'] or [],
                        interests=row['interests'] or [],
                        trip_complexity=complexity,
                        generation_time_ms=row['generation_time_ms'],
                        itinerary_text=row['itinerary_text'],
                        provider=row['provider'] or "Unknown",
                        prompt_version=row['prompt_version'] or "Unknown",
                        model_version=row['model_version'] or "Unknown",
                        conversation_id=row['conversation_id'],
                        created_at=row['created_at'],
                        quality_score=row['quality_score'],
                        rating=row['rating']
                    ))
                return results
        except Exception:
            return []
