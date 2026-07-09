from dataclasses import dataclass


@dataclass
class ItineraryRequest:
    city: str
    budget: str
    trip_days: int
    interests: list[str]
    travel_style: list[str]
    include_food: bool = True
    include_transport: bool = True
