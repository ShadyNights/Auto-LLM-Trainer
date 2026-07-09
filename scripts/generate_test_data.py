import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import random
import time

from dotenv import load_dotenv

from src.domain.dto.itinerary_request import ItineraryRequest
from src.infrastructure.database.connection import DatabaseConnection
from src.providers.groq_provider import GroqProvider
from src.repositories.config_repository import ConfigRepository
from src.repositories.event_repository import EventRepository
from src.repositories.itinerary_repository import ItineraryRepository
from src.repositories.prompt_repository import PromptRepository
from src.repositories.training_repository import TrainingRepository
from src.repositories.trip_repository import TripRepository
from src.services.event.event_service import EventService
from src.services.planner.planner_service import PlannerService

CITIES = [
    "Kyoto, Japan",
    "Paris, France",
    "New York City, USA",
    "Rome, Italy",
    "Cape Town, South Africa",
    "Sydney, Australia",
    "Bangkok, Thailand",
    "Rio de Janeiro, Brazil",
    "Dubai, UAE",
    "London, UK",
    "Mumbai, India",
    "Barcelona, Spain",
    "Seoul, South Korea",
    "Berlin, Germany",
    "Cairo, Egypt",
]
BUDGETS = ["Budget", "Moderate", "Luxury"]
TRAVEL_STYLES = ["Solo", "Duo", "Family", "Friends", "Business"]
INTERESTS = [
    ["History", "Food"],
    ["Hiking", "Nature"],
    ["Shopping", "Nightlife"],
    ["Art", "Museums"],
    ["Relaxation", "Beaches"],
    ["Adventure", "Sports"],
    ["Photography", "Architecture"],
    ["Local Culture", "Festivals"],
]


def bootstrap_pipeline_metadata(db: DatabaseConnection):
    """Bootstraps the datasets, models, prompts, configs, and audit logs to fully populate the DB Manager."""
    print("Bootstraps pipeline metadata (Datasets, Models, Prompts, Configs, Logs)...")

    queries = [
        "INSERT INTO datasets (version_name, sample_count, average_quality, source) VALUES ('ds-v1', 1500, 92.5, 'feedback') ON CONFLICT (version_name) DO NOTHING",
        "INSERT INTO prompts_metadata (version_name, checksum, is_active) VALUES ('v1', 'abc123hash', true) ON CONFLICT (version_name) DO NOTHING",
        "INSERT INTO model_versions (version_name, provider, provider_model, prompt_version, dataset_version) VALUES ('Custom Model v1', 'Custom Provider', 'custom-llm-1', 'v1', 'ds-v1') ON CONFLICT (version_name) DO NOTHING",
        "INSERT INTO system_config (id, config_version, active_model_id, active_prompt_id, active_dataset_id) VALUES (1, 'prod-1.0', 1, 1, 1) ON CONFLICT (id) DO NOTHING",
        "INSERT INTO config_evaluations (model_version_id, score, passed, structural_metrics, semantic_metrics) VALUES (1, 95.5, true, '{\"format\": 1.0}', '{\"relevance\": 0.95}')",
        'INSERT INTO audit_logs (action, details) VALUES (\'SYSTEM_STARTUP\', \'{"message": "Test data pipeline initialized", "actor": "system"}\')',
        'INSERT INTO audit_logs (action, details) VALUES (\'CONFIG_UPDATED\', \'{"prompt": "v1", "model": "Custom Model v1", "actor": "admin"}\')',
    ]

    for q in queries:
        try:
            with db.get_cursor(commit_on_success=True) as cur:
                cur.execute(q)
        except Exception:
            pass  # Silently skip schema/conflict mismatches


def simulate_dead_queue_failures(db: DatabaseConnection, event_service: EventService, num_failures: int):
    """Simulates pipeline failures to populate the Dead Queue and Error metrics."""
    print(f"Simulating {num_failures} pipeline failures...")
    for _ in range(num_failures):
        conversation_id = event_service.start_conversation()
        corr_id = event_service.log_prompt_submitted(conversation_id, "Unknown", "Budget", 1)
        # Log the generation failure
        event_service.log_generation(conversation_id, corr_id, False, "Simulated 429 API Rate Limit or Timeout")
        # Push a dead item to the training queue
        with db.get_cursor() as cur:
            cur.execute(
                "INSERT INTO training_queue (itinerary_id, status, error_message) VALUES (NULL, 'dead', 'Pipeline crash simulation')"
            )


def generate_test_data(num_itineraries=50):
    load_dotenv()

    # Map local DB vars to PG env vars expected by connection
    if os.getenv("DB_HOST"):
        os.environ["PGHOST"] = os.getenv("DB_HOST")
    if os.getenv("DB_PORT"):
        os.environ["PGPORT"] = os.getenv("DB_PORT")
    if os.getenv("DB_NAME"):
        os.environ["PGDATABASE"] = os.getenv("DB_NAME")
    if os.getenv("DB_USER"):
        os.environ["PGUSER"] = os.getenv("DB_USER")
    if os.getenv("DB_PASSWORD"):
        os.environ["PGPASSWORD"] = os.getenv("DB_PASSWORD")

    print(f"Initializing Comprehensive System Load Test ({num_itineraries} Generations)...")

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
        return

    planner_service = PlannerService(config_repo, prompt_repo, provider)
    event_service = EventService(event_repo)

    # 1. Bootstrap all Pipeline Metadata (Datasets, Models, Prompts, etc.)
    bootstrap_pipeline_metadata(db)

    # 2. Simulate Failures (Creates Dead Queue entries and Failure metrics)
    simulate_dead_queue_failures(db, event_service, 3)

    success_count = 0
    fail_count = 0

    # 3. Main Generation Loop
    for i in range(num_itineraries):
        city = random.choice(CITIES)
        budget = random.choice(BUDGETS)
        travel_style = random.choice(TRAVEL_STYLES)
        interests = random.choice(INTERESTS)
        days = random.randint(1, 7)

        print(f"[{i+1}/{num_itineraries}] Generating {days}-day {budget} {travel_style} trip to {city}...")

        conversation_id = event_service.start_conversation()
        corr_id = event_service.log_prompt_submitted(conversation_id, city, budget, days)

        try:
            # 1. Create Trip Record (Fixes Analytics "Not Available")
            trip_id = trip_repo.create_trip(city, days, budget, [travel_style], interests)

            # 2. Request LLM and Measure Time (Fixes Gen Time "0 ms")
            start_t = time.time()
            req = ItineraryRequest(
                city=city, budget=budget, trip_days=days, interests=interests, travel_style=[travel_style]
            )
            response, config, p_ver, d_ver = planner_service.generate_itinerary(req)
            gen_time_ms = int((time.time() - start_t) * 1000)

            # 3. Save to DB (Linked to trip_id and generation_time_ms)
            itin_id = itinerary_repo.create_itinerary(
                conversation_id=conversation_id,
                itinerary_text=response.text,
                prompt_id=config.active_prompt_id,
                model_version_id=config.active_model_id,
                config_snapshot={"temperature": 0.7, "max_tokens": 2000, "provider": "Custom Provider"},
                word_count=len(response.text.split()),
                trip_id=trip_id,
                generation_time_ms=gen_time_ms,
            )

            # 4. Enqueue for training (Populates Learning Queue)
            training_repo.enqueue(itin_id)

            # 5. Log success
            event_service.log_generation(conversation_id, corr_id, True)

            # 6. Add simulated feedback (Fixes Avg Rating & Quality Score)
            rating = random.randint(3, 5)  # Skew positive for realism
            comments = "Great!" if rating > 3 else "Could be better."
            itinerary_repo.update_rating(itin_id, rating, comments)
            # We must explicitly update quality_score since update_rating doesn't
            with db.get_cursor() as cur:
                cur.execute("UPDATE itineraries SET quality_score = %s WHERE id = %s", (rating * 20.0, itin_id))

            success_count += 1
            print(f"  -> Success! Itinerary ID: {itin_id} | Gen Time: {gen_time_ms}ms | Rating: {rating}/5")

        except Exception as e:
            event_service.log_generation(conversation_id, corr_id, False, str(e))
            fail_count += 1
            if "429" in str(e):
                print("  -> Rate limited by Groq API. Cooling down for 15 seconds...")
                time.sleep(15)
            else:
                print(f"  -> Failed: {e}")

        # Strict sleep to avoid Groq rate limits
        time.sleep(5)

    print(f"\nFinished comprehensive simulation. Success: {success_count}, Failed: {fail_count}")


if __name__ == "__main__":
    generate_test_data(50)
