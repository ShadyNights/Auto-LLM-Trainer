import json
import os

from dotenv import load_dotenv

from src.infrastructure.database.connection import DatabaseConnection


def export_dataset():
    print("Initializing Database Connection...")
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

    db = DatabaseConnection()

    export_file = "local_dataset.jsonl"
    count = 0

    print("Extracting itineraries and formatting for LLM Fine-Tuning...")

    try:
        with db.get_cursor() as cur:
            # We join itineraries with trips to get the user's prompt parameters
            query = """
                SELECT i.itinerary_text, t.destination, t.duration, t.budget_level, t.travel_style, t.interests
                FROM itineraries i
                LEFT JOIN trips t ON i.trip_id = t.id
                ORDER BY i.created_at DESC
            """
            cur.execute(query)

            with open(export_file, "w", encoding="utf-8") as f:
                while True:
                    # Stream exactly 1000 records at a time to prevent RAM overload
                    rows = cur.fetchmany(1000)
                    if not rows:
                        break  # All records exported!

                    for row in rows:
                        # Construct the system instruction
                        system_msg = "You are an expert AI travel planner. Create a highly detailed and structured travel itinerary based on the user's request."

                        # Handle missing trip data for older records safely
                        dest = row.get("destination") or "an unknown destination"
                        dur = row.get("duration") or "several"
                        bud = row.get("budget_level") or "flexible"
                        style = row.get("travel_style") or "general"
                        interests = row.get("interests") or ""

                        user_msg = f"Plan a {dur}-day {bud} trip to {dest} for a {style} trip."
                        if interests:
                            user_msg += f" Our interests include: {interests}."

                        # The Assistant's perfect response (the generated itinerary)
                        assistant_msg = row["itinerary_text"]

                        # Format exactly like OpenAI / HuggingFace chat templates
                        jsonl_line = {
                            "messages": [
                                {"role": "system", "content": system_msg},
                                {"role": "user", "content": user_msg},
                                {"role": "assistant", "content": assistant_msg},
                            ]
                        }

                        f.write(json.dumps(jsonl_line) + "\n")
                        count += 1

        print(f"\n✅ Success! Exported {count} high-quality interactions to '{export_file}'.")
        print(f"You can now upload '{export_file}' directly to OpenAI, Unsloth, or HuggingFace for fine-tuning!")

    except Exception as e:
        print(f"Error exporting dataset: {e}")


if __name__ == "__main__":
    export_dataset()
