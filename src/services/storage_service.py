import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from typing import Dict, Any, List, Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)

class StorageService:
    def __init__(self):
        # Database URL from env
        db_url = os.getenv("DATABASE_URL")
        
        # Local postgres fallback if no neon URL
        if not db_url:
            db_host = os.getenv("DB_HOST", "localhost")
            db_name = os.getenv("DB_NAME", "travel_planner")
            db_user = os.getenv("DB_USER", "postgres")
            db_password = os.getenv("DB_PASSWORD", "")
            
            try:
                self.pool = SimpleConnectionPool(
                    minconn=1,
                    maxconn=10,
                    host=db_host,
                    database=db_name,
                    user=db_user,
                    password=db_password,
                    port=5432,
                    connect_timeout=10
                )
            except Exception as e:
                logger.error(f"Failed to initialize local connection pool: {e}")
                self.pool = None
        else:
            try:
                from urllib.parse import urlparse
                url = urlparse(db_url)
                
                self.pool = SimpleConnectionPool(
                    minconn=1,
                    maxconn=10,
                    host=url.hostname,
                    database=url.path[1:],
                    user=url.username,
                    password=url.password,
                    port=url.port or 5432,
                    connect_timeout=10,
                    sslmode='require' if 'neon.tech' in url.hostname else 'prefer'
                )
            except Exception as e:
                logger.error(f"Failed to initialize Neon connection pool: {e}")
                self.pool = None

    @contextmanager
    def get_connection(self):
        """Yield a database connection from the pool."""
        if not self.pool:
            raise RuntimeError("Database connection pool is not initialized.")
            
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SET statement_timeout = '30s'")
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            self.pool.putconn(conn)

    def execute_query(self, query: str, params: tuple = None, fetch: bool = False, fetch_one: bool = False) -> Any:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    columns = [desc[0] for desc in cursor.description]
                    results = cursor.fetchall()
                    return [dict(zip(columns, row)) for row in results]
                if fetch_one:
                    if cursor.description is None:
                        return None
                    columns = [desc[0] for desc in cursor.description]
                    row = cursor.fetchone()
                    return dict(zip(columns, row)) if row else None
                return None

    def log_event(self, itinerary_id: Optional[int], event_name: str, metadata: dict = None):
        """Log an event for a specific itinerary."""
        import json
        query = """
            INSERT INTO events (itinerary_id, event_name, metadata)
            VALUES (%s, %s, %s)
        """
        self.execute_query(query, (itinerary_id, event_name, json.dumps(metadata) if metadata else None))
        logger.info(f"Event logged: {event_name} for itinerary {itinerary_id}")

    def get_active_config(self) -> dict:
        """Fetch the currently active model, prompt, and dataset."""
        query = """
            SELECT 
                c.id,
                m.id as model_id, m.version_name as model_version, m.provider_model,
                p.id as prompt_id, p.version_name as prompt_version,
                d.id as dataset_id, d.version_name as dataset_version
            FROM system_config c
            LEFT JOIN models m ON c.active_model_id = m.id
            LEFT JOIN prompts_metadata p ON c.active_prompt_id = p.id
            LEFT JOIN datasets d ON c.active_dataset_id = d.id
            WHERE c.id = 1
        """
        return self.execute_query(query, fetch_one=True)

    def get_dashboard_metrics(self) -> dict:
        """Fetch dashboard metrics from the view."""
        query = "SELECT * FROM dashboard_metrics LIMIT 1"
        return self.execute_query(query, fetch_one=True)

    def queue_training(self, itinerary_id: int):
        """Add an itinerary to the training queue."""
        query = """
            INSERT INTO training_queue (itinerary_id, status)
            VALUES (%s, 'pending')
        """
        self.execute_query(query, (itinerary_id,))

    def create_trip(self, user_id: int, destination: str, interests: list, duration: int, budget_level: str, travel_style: list) -> int:
        query = """
            INSERT INTO trips (user_id, destination, interests, duration, budget_level, travel_style)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, destination, interests, duration, budget_level, travel_style))
                return cursor.fetchone()[0]

    def create_itinerary(self, trip_id: int, itinerary_text: str, prompt_id: int, model_id: int, word_count: int = 0) -> int:
        query = """
            INSERT INTO itineraries (trip_id, itinerary_text, prompt_id, model_id, word_count)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (trip_id, itinerary_text, prompt_id, model_id, word_count))
                return cursor.fetchone()[0]

    def record_feedback(self, itinerary_id: int, rating: int, comments: str):
        # Calculate quality score (Rating + export/share would ideally be factored in, but for now we do simple math)
        quality_score = (rating * 16) + 20 # Simple approximation
        
        query = """
            UPDATE itineraries
            SET rating = %s, feedback_comments = %s, rated_at = NOW(), quality_score = %s
            WHERE id = %s
        """
        self.execute_query(query, (rating, comments, quality_score, itinerary_id))
        
        # Log event
        self.log_event(itinerary_id, 'Feedback', {'rating': rating, 'comments': comments, 'quality_score': quality_score})
        
        # Queue for training if rating >= 4
        if rating >= 4:
            self.queue_training(itinerary_id)

    def close(self):
        if self.pool:
            self.pool.closeall()
