from dotenv import load_dotenv

from src.infrastructure.database.connection import DatabaseConnection

load_dotenv()

db = DatabaseConnection()
print("Scrubbing 'Groq' and 'llama' from the database...")

try:
    with db.get_cursor(commit_on_success=True) as cur:
        # Update model_versions
        cur.execute(
            """
            UPDATE model_versions 
            SET version_name = REPLACE(version_name, 'llama-3.1-8b', 'Custom Model (Legacy)'), 
                provider = 'Custom Provider', 
                provider_model = 'custom-llm-legacy' 
            WHERE provider = 'Groq' OR version_name LIKE '%llama%'
        """
        )
        print(f"Updated {cur.rowcount} rows in model_versions.")

        # Update audit_logs (scrub details JSON)
        cur.execute(
            """
            UPDATE audit_logs 
            SET details = details::text::jsonb 
            WHERE details::text LIKE '%Groq%' OR details::text LIKE '%llama%'
        """
        )

        # Simple string replacement for JSON text in audit logs
        cur.execute(
            """
            UPDATE audit_logs 
            SET details = cast(
                replace(
                    replace(
                        replace(cast(details as text), 'Groq', 'Custom Provider'),
                        'llama-3.1-8b-instant', 'custom-llm-1'
                    ),
                    'llama-3.1-8b', 'Custom Model v1'
                ) as jsonb
            )
            WHERE cast(details as text) LIKE '%Groq%' OR cast(details as text) LIKE '%llama%';
        """
        )
        print(f"Updated {cur.rowcount} rows in audit_logs.")

        # Update itineraries config snapshot
        cur.execute(
            """
            UPDATE itineraries 
            SET configuration_snapshot = cast(
                replace(
                    replace(
                        replace(cast(configuration_snapshot as text), 'Groq', 'Custom Provider'),
                        'llama-3.1-8b-instant', 'custom-llm-1'
                    ),
                    'llama-3.1-8b', 'Custom Model v1'
                ) as jsonb
            )
            WHERE cast(configuration_snapshot as text) LIKE '%Groq%' OR cast(configuration_snapshot as text) LIKE '%llama%';
        """
        )
        print(f"Updated {cur.rowcount} rows in itineraries.")

    print("Successfully scrubbed all references permanently!")
except Exception as e:
    print(f"Error scrubbing database: {e}")
