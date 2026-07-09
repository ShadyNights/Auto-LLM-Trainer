from typing import Dict, Any, List
from src.infrastructure.database.connection import DatabaseConnection
from src.domain.dto.ui_dtos import AnalyticsDTO, DestinationStat, RatingStat, BudgetStat, PipelineStat

class AnalyticsRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def get_analytics(self) -> AnalyticsDTO:
        dto = AnalyticsDTO(
            recent_conversations=0,
            recent_generations=0,
            destinations=[],
            ratings=[],
            budgets=[],
            pipeline=PipelineStat(0, 0, 0)
        )
        
        try:
            with self.db.get_cursor() as cur:
                # Last 30 Days Usage
                cur.execute("SELECT COUNT(*) as cnt FROM conversations WHERE created_at > NOW() - INTERVAL '30 days'")
                row = cur.fetchone()
                if row: dto.recent_conversations = row['cnt']
                
                cur.execute("SELECT COUNT(*) as cnt FROM itineraries WHERE created_at > NOW() - INTERVAL '30 days'")
                row = cur.fetchone()
                if row: dto.recent_generations = row['cnt']
                
                # Destinations
                cur.execute("SELECT destination, trip_count, avg_rating FROM popular_destinations LIMIT 10")
                for r in cur.fetchall():
                    dto.destinations.append(DestinationStat(r['destination'], r['trip_count'], float(r['avg_rating'] or 0.0)))
                
                # Ratings
                cur.execute("SELECT rating, COUNT(*) as count FROM itineraries WHERE rating > 0 GROUP BY rating ORDER BY rating DESC")
                for r in cur.fetchall():
                    dto.ratings.append(RatingStat(r['rating'], r['count']))
                    
                # Budgets
                cur.execute("SELECT budget_level, COUNT(*) as count FROM trips GROUP BY budget_level ORDER BY count DESC")
                for r in cur.fetchall():
                    dto.budgets.append(BudgetStat(r['budget_level'], r['count']))
                    
                # Pipeline
                cur.execute("SELECT COUNT(*) as cnt FROM datasets")
                d_row = cur.fetchone()
                cur.execute("SELECT COUNT(*) as cnt FROM prompts_metadata")
                p_row = cur.fetchone()
                cur.execute("SELECT COUNT(*) as cnt FROM model_versions")
                m_row = cur.fetchone()
                
                dto.pipeline = PipelineStat(
                    total_datasets=d_row['cnt'] if d_row else 0,
                    total_prompts=p_row['cnt'] if p_row else 0,
                    total_models=m_row['cnt'] if m_row else 0
                )
                
        except Exception:
            pass
            
        return dto
