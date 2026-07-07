# Operations & Recovery Guide

## Logging & Monitoring
All application logs are emitted as structured JSON to `stdout`.
Key fields to index in your log aggregator (e.g., Datadog, ELK):
- `correlation_id`: Trace a request from prompt submission through generation and feedback.
- `conversation_id`: Track a single user's session.
- `component`: Identify if the log originated in `PlannerService`, `GroqProvider`, or `LearningPipeline`.

## Dead Letter Queue (DLQ) Handling
The `training_queue` automatically transitions tasks to `status = 'dead'` after the maximum retry threshold is reached.
**Recovery Runbook**:
1. Query the database for dead tasks:
   ```sql
   SELECT * FROM training_queue WHERE status = 'dead';
   ```
2. Check the associated `error_message` and structured logs.
3. If the error was transient (e.g., API downtime), manually update the status back to `pending` and reset `retry_count`.

## Secret Rotation (Provider Keys)
To rotate the `GROQ_API_KEY`:
1. Generate a new key in the Groq console.
2. Update the `.env` file (or your secrets manager).
3. Restart the Streamlit application to reload the environment.
*(Note: Active queue tasks do not require the API key unless the pipeline stage requires inference).*

## Least-Privilege PostgreSQL User
Do not run the application as the `postgres` superuser.
```sql
CREATE USER traveler_app_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE traveler_db TO traveler_app_user;
GRANT USAGE ON SCHEMA public TO traveler_app_user;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO traveler_app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO traveler_app_user;
```
