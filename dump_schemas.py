import json

from dotenv import load_dotenv

from src.infrastructure.database.connection import DatabaseConnection

load_dotenv()
db = DatabaseConnection()

tables = [
    "datasets",
    "prompts_metadata",
    "model_versions",
    "system_config",
    "config_evaluations",
    "audit_logs",
    "training_queue",
]
schema = {}

try:
    with db.get_cursor() as cur:
        for t in tables:
            cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s;", (t,))
            rows = cur.fetchall()
            schema[t] = {r["column_name"]: r["data_type"] for r in rows}

    with open("schema_dump.json", "w") as f:
        json.dump(schema, f, indent=4)
    print("Schema dumped successfully to schema_dump.json")
except Exception as e:
    print(f"Error: {e}")
