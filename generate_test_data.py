import os
import random
import time
from src.infrastructure.database.connection import DatabaseConnection
from src.repositories.config_repository import ConfigRepository
from src.repositories.prompt_repository import PromptRepository
from src.repositories.event_repository import EventRepository
from src.repositories.training_repository import TrainingRepository
from src.repositories.itinerary_repository import ItineraryRepository
from src.providers.groq_provider import GroqProvider
from src.services.planner.planner_service import PlannerService
from src.services.event.event_service import EventService
from src.domain.dto.itinerary_request import ItineraryRequest
from dotenv import load_dotenv

CITIES = ["Kyoto, Japan", "Paris, France", "New York City, USA", "Rome, Italy", "Cape Town, South Africa", "Sydney, Australia", "Bangkok, Thailand", "Rio de Janeiro, Brazil", "Dubai, UAE", "London, UK"]
BUDGETS = ["Budget", "Moderate", "Luxury"]
TRAVEL_STYLES = ["Solo", "Duo", "Family", "Friends", "Business"]
INTERESTS = [["History", "Food"], ["Hiking", "Nature"], ["Shopping", "Nightlife"], ["Art", "Museums"], ["Relaxation", "Beaches"]]

def generate_test_data(num_itineraries=50):
    # Load .env explicitly for local runs
    load_dotenv()
    
    # Map DB_ env vars to PG_ env vars expected by connection.py
    if os.getenv("DB_HOST"): os.environ["PGHOST"] = os.getenv("DB_HOST")
    if os.getenv("DB_PORT"): os.environ["PGPORT"] = os.getenv("DB_PORT")
    if os.getenv("DB_NAME"): os.environ["PGDATABASE"] = os.getenv("DB_NAME")
    if os.getenv("DB_USER"): os.environ["PGUSER"] = os.getenv("DB_USER")
    if os.getenv("DB_PASSWORD"): os.environ["PGPASSWORD"] = os.getenv("DB_PASSWORD")
    
    print(f"Initializing services to generate {num_itineraries} test itineraries...")
    from src.repositories.trip_repository import TripRepository
    db = DatabaseConnection()
    config_repo = ConfigRepository(db)
    prompt_repo = PromptRepository()
    event_repo = EventRepository(db)
    training_repo = TrainingRepository(db)
    itinerary_repo = ItineraryRepository(db)
    trip_repo = TripRepository(db)
    
    try:
        provider = GroqProvider()
    except Exception as e:
        print(f"Failed to initialize GroqProvider: {e}")
        print("Please ensure GROQ_API_KEY is set in your environment.")
        return

    planner_service = PlannerService(config_repo, prompt_repo, provider)
    event_service = EventService(event_repo)

    success_count = 0
    fail_count = 0

    for i in range(num_itineraries):
        city = random.choice(CITIES)
        budget = random.choice(BUDGETS)
        travel_style = random.choice(TRAVEL_STYLES)
        interests = random.choice(INTERESTS)
        days = random.randint(1, 5)
        
        print(f"[{i+1}/{num_itineraries}] Generating {days}-day {budget} {travel_style} trip to {city}...")
        
        conversation_id = event_service.start_conversation()
        corr_id = event_service.log_prompt_submitted(conversation_id, city, budget, days)
        
        try:
            # 1. Create Trip Record
            trip_id = trip_repo.create_trip(city, days, budget, [travel_style], interests)
            
            # 2. Request LLM
            start_t = time.time()
            req = ItineraryRequest(city=city, budget=budget, trip_days=days, interests=interests, travel_style=[travel_style])
            response, config, p_ver, d_ver = planner_service.generate_itinerary(req)
            gen_time_ms = int((time.time() - start_t) * 1000)
            
            # 3. Save to DB
            itin_id = itinerary_repo.create_itinerary(
                conversation_id=conversation_id,
                itinerary_text=response.text,
                prompt_id=config.active_prompt_id,
                model_version_id=config.active_model_id,
                config_snapshot={"temperature": 0.7, "max_tokens": 2000, "provider": "Groq"},
                word_count=len(response.text.split()),
                trip_id=trip_id,
                generation_time_ms=gen_time_ms
            )
            
            # 3. Enqueue for training
            training_repo.enqueue(itin_id)
            
            # 4. Log success
            event_service.log_generation(conversation_id, corr_id, True)
            
            # 5. Add dummy feedback randomly
            rating = random.randint(3, 5) # Skew positive for realism
            comments = "Great!" if rating > 3 else "Could be better."
            itinerary_repo.update_rating(itin_id, rating, comments)
                
            success_count += 1
            print(f"  -> Success! Itinerary ID: {itin_id} (Rating: {rating}/5)")
            
        except Exception as e:
            event_service.log_generation(conversation_id, corr_id, False, str(e))
            fail_count += 1
            if "429" in str(e):
                print(f"  -> Rate limited by Groq API. Cooling down for 15 seconds...")
                time.sleep(15)
            else:
                print(f"  -> Failed: {e}")
            
        # Sleep to avoid Groq rate limits (free tier is strict)
        time.sleep(5)

    print(f"\nFinished generating {num_itineraries} itineraries. Success: {success_count}, Failed: {fail_count}")

if __name__ == "__main__":
    # Ensure env var is loaded if not already in system environment
    generate_test_data(50)
