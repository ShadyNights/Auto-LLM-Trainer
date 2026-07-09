from dataclasses import dataclass
from datetime import datetime


@dataclass
class TripSummaryDTO:
    destination: str
    duration: int
    budget: str
    travel_style: list[str]
    interests: list[str]
    trip_complexity: int
    generation_time_ms: int | None
    itinerary_text: str
    provider: str
    prompt_version: str
    model_version: str
    conversation_id: int
    created_at: datetime
    quality_score: float | None
    rating: int | None


@dataclass
class AIOverviewDTO:
    total_conversations: int
    successful_generations: int
    failed_generations: int
    success_rate: float
    average_rating: float
    average_quality_score: float
    average_generation_time_ms: float
    provider_latency: float
    learning_queue_size: int
    dead_letter_queue_size: int
    promotions: int
    evaluations: int


@dataclass
class DestinationStat:
    destination: str
    count: int
    avg_rating: float


@dataclass
class RatingStat:
    rating: int
    count: int


@dataclass
class BudgetStat:
    budget_level: str
    count: int


@dataclass
class PipelineStat:
    total_datasets: int
    total_prompts: int
    total_models: int


@dataclass
class AnalyticsDTO:
    recent_conversations: int
    recent_generations: int
    destinations: list[DestinationStat]
    ratings: list[RatingStat]
    budgets: list[BudgetStat]
    pipeline: PipelineStat
