from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class ItineraryRequest:
    city: str
    budget: str
    trip_days: int
    interests: List[str]
    travel_style: List[str]
    include_food: bool = True
    include_transport: bool = True
