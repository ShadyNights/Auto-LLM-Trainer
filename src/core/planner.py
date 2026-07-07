"""
Enhanced TravelPlanner with trip_days and budget support.
"""

import os
from groq import Groq
from src.services.storage_service import StorageService

logger = get_logger(__name__)

MAX_TOKENS = 8000

class TravelPlanner:
    """Travel planner with proper trip_days and budget handling."""
    
    def __init__(
        self, 
        city: str, 
        interests: list, 
        trip_days: int = 1, 
        budget: str = "Moderate",
        storage_service: StorageService = None
    ):
        """
        Initialize TravelPlanner.
        
        Args:
            city: Destination city
            interests: List of interests
            trip_days: Number of days for the trip (CRITICAL!)
            budget: Budget level (Budget/Moderate/Luxury)
        """
        self.city = city
        self.interests = interests if isinstance(interests, list) else [interests]
        
        # ✅ FIX: Validate trip_days range
        self.trip_days = max(1, min(trip_days, 30))
        if trip_days != self.trip_days:
            logger.warning(f"Trip days adjusted from {trip_days} to {self.trip_days}")
        
        self.budget = budget
        self.storage = storage_service or StorageService()
        self.client = self._initialize_client()
        
        logger.info(
            f"Initialized TravelPlanner for {city=}, {trip_days=}, {budget=}, "
            f"interests={self.interests[:3]}"
        )
    
    def _initialize_client(self) -> Groq:
        """
        Initialize Groq client.
        
        Returns:
            Groq: Configured Groq client
            
        Raises:
            ValueError: If GROQ_API_KEY not found
        """
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        return Groq(api_key=api_key)
    
    def create_itinerary(self) -> dict:
        """
        Generate complete itinerary for ALL trip days.
        
        Returns:
            Dict containing itinerary, prompt_id, and model_id
            
        Raises:
            RuntimeError: If generation fails
        """
        try:
            logger.info(
                f"Generating itinerary for city={self.city}, "
                f"trip_days={self.trip_days}, budget={self.budget}"
            )
            
            # Format interests
            interests_str = ", ".join(self.interests)
            
            # Fetch active configuration
            config = self.storage.get_active_config()
            model_name = config.get('provider_model') if config and config.get('provider_model') else "llama-3.3-70b-versatile"
            prompt_id = config.get('prompt_id') if config else None
            model_id = config.get('model_id') if config else None
            
            # Load active prompt version
            prompt_template = ""
            prompt_version_name = config.get('prompt_version') if config else "travel_v1"
            prompt_file = f"prompts/{prompt_version_name}.md"
            
            if os.path.exists(prompt_file):
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    prompt_template = f.read()
            else:
                # Fallback template
                prompt_template = "You are an expert travel planner. Create a COMPLETE {trip_days}-day itinerary for {city}. Cover {interests_str} with {budget} budget."
            
            # Format the prompt
            prompt = prompt_template.format(
                city=self.city,
                trip_days=self.trip_days,
                budget=self.budget,
                interests_str=interests_str
            )
            
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=MAX_TOKENS,
                top_p=0.9,
                stream=False
            )
            
            itinerary = response.choices[0].message.content.strip()
            
            # ✅ FIX: Better validation for empty response
            if not itinerary or len(itinerary) < 100:
                raise RuntimeError(
                    f"Generated itinerary is too short or empty (length: {len(itinerary)})"
                )
            
            logger.info(
                f"Itinerary generated successfully - {len(itinerary)} chars, "
                f"{len(itinerary.split())} words"
            )
            
            # ✅ FIX: More robust validation
            days_found = sum(
                1 for i in range(1, self.trip_days + 1)
                if f"Day {i}" in itinerary or f"**Day {i}**" in itinerary
            )
            
            if days_found < self.trip_days:
                logger.warning(
                    f"⚠️  Only {days_found}/{self.trip_days} days found in itinerary - "
                    "may be truncated"
                )
            else:
                logger.info(f"✅ All {self.trip_days} days generated successfully!")
            
            return {
                "itinerary_text": itinerary,
                "prompt_id": prompt_id,
                "model_id": model_id
            }
            
        except Exception as e:
            logger.error(f"Error generating itinerary: {e}", exc_info=True)
            # ✅ FIX: Raise exception instead of returning error string
            raise RuntimeError(f"Unable to generate itinerary: {str(e)}") from e
