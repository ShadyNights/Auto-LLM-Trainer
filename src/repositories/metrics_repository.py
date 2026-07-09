from typing import Optional, List
from src.infrastructure.database.connection import DatabaseConnection
from src.domain.dto.ui_dtos import AIOverviewDTO

class MetricsRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def get_ai_metrics(self) -> AIOverviewDTO:
        dto = AIOverviewDTO(
            total_conversations=0,
            successful_generations=0,
            failed_generations=0,
            success_rate=0.0,
            average_rating=0.0,
            average_quality_score=0.0,
            average_generation_time_ms=0.0,
            provider_latency=0.0,
            learning_queue_size=0,
            dead_letter_queue_size=0,
            promotions=0,
            evaluations=0
        )
        
        try:
            with self.db.get_cursor() as cur:
                cur.execute("SELECT COUNT(*) as cnt FROM conversations")
                row = cur.fetchone()
                if row: dto.total_conversations = row['cnt']
                
                cur.execute("SELECT COUNT(*) as cnt FROM events WHERE event_type = 'GenerationCompleted'")
                row = cur.fetchone()
                if row: dto.successful_generations = row['cnt']
                
                cur.execute("SELECT COUNT(*) as cnt FROM events WHERE event_type = 'Failure'")
                row = cur.fetchone()
                if row: dto.failed_generations = row['cnt']
                
                total_gens = dto.successful_generations + dto.failed_generations
                if total_gens > 0:
                    dto.success_rate = (dto.successful_generations / total_gens) * 100.0
                
                cur.execute("SELECT AVG(rating) as avg_rtg, AVG(quality_score) as avg_qs, AVG(generation_time_ms) as avg_time FROM itineraries")
                row = cur.fetchone()
                if row:
                    dto.average_rating = float(row['avg_rtg'] or 0.0)
                    dto.average_quality_score = float(row['avg_qs'] or 0.0)
                    dto.average_generation_time_ms = float(row['avg_time'] or 0.0)
                    dto.provider_latency = float(row['avg_time'] or 0.0) # Approximation if API latency not tracked separately
                
                cur.execute("SELECT COUNT(*) as cnt FROM training_queue WHERE status = 'pending'")
                row = cur.fetchone()
                if row: dto.learning_queue_size = row['cnt']
                
                cur.execute("SELECT COUNT(*) as cnt FROM training_queue WHERE status = 'dead'")
                row = cur.fetchone()
                if row: dto.dead_letter_queue_size = row['cnt']
                
                cur.execute("SELECT COUNT(*) as cnt FROM config_evaluations")
                row = cur.fetchone()
                if row: dto.evaluations = row['cnt']
                
        except Exception:
            pass
            
        return dto
