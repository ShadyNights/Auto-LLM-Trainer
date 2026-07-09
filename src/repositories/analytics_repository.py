from typing import Dict, Any, List
from src.infrastructure.database.connection import DatabaseConnection

class AnalyticsRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def get_ai_metrics(self) -> Dict[str, Any]:
        """Fetches high-level metrics for the AI Metrics dashboard."""
        metrics = {
            'data_points': 0,
            'training_cycles': 0,
            'average_rating': 0.0
        }
        
        try:
            with self.db.get_cursor() as cur:
                # Total Data Points (Itineraries generated)
                cur.execute("SELECT COUNT(*) as count FROM itineraries")
                row = cur.fetchone()
                if row: metrics['data_points'] = row['count']
                
                # Training Cycles
                cur.execute("SELECT COUNT(*) as count FROM training_queue WHERE status = 'completed'")
                row = cur.fetchone()
                if row: metrics['training_cycles'] = row['count']
                
                # Average Rating
                cur.execute("SELECT AVG(rating) as avg_rating FROM itineraries WHERE rating > 0")
                row = cur.fetchone()
                if row and row['avg_rating'] is not None:
                    metrics['average_rating'] = round(row['avg_rating'], 1)
        except Exception:
            pass
            
        return metrics

    def get_popular_destinations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetches popular destinations from the SQL view."""
        try:
            with self.db.get_cursor() as cur:
                cur.execute("SELECT destination, trip_count, avg_rating FROM popular_destinations LIMIT %s", (limit,))
                return cur.fetchall()
        except Exception:
            return []

    def get_rating_distribution(self) -> List[Dict[str, Any]]:
        """Fetches the distribution of user ratings."""
        try:
            with self.db.get_cursor() as cur:
                cur.execute("""
                    SELECT rating, COUNT(*) as count 
                    FROM itineraries 
                    WHERE rating > 0 
                    GROUP BY rating 
                    ORDER BY rating DESC
                """)
                return cur.fetchall()
        except Exception:
            return []

    def get_recent_records(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetches flat list of recent generated trips for the Database Manager."""
        try:
            with self.db.get_cursor() as cur:
                cur.execute("""
                    SELECT 
                        i.id as itinerary_id, 
                        t.destination, 
                        t.duration, 
                        t.budget_level, 
                        i.rating, 
                        i.created_at
                    FROM itineraries i
                    JOIN trips t ON i.trip_id = t.id
                    ORDER BY i.id DESC
                    LIMIT %s
                """, (limit,))
                return cur.fetchall()
        except Exception:
            return []
