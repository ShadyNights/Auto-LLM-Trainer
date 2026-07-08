# Operations & Recovery Guide

> [!NOTE]
> Standardized operational procedures for monitoring platform health, rotating credentials, and managing system queues.

---

## 1. Telemetry & Observability

All operational logs are emitted strictly as structured JSON to `stdout`, optimizing them for ingestion by platforms like Datadog, ELK, or Splunk.

**Critical Indexing Fields:**
- `correlation_id`: The primary key for tracing a single request horizontally from user input ➔ LLM inference ➔ feedback submission.
- `conversation_id`: Tracks the vertical lifecycle of a distinct user session.
- `component`: Identifies the exact origin module (e.g., `PlannerService`, `LearningPipeline`, `GroqProvider`).

## 2. Queue Management & DLQ Recovery

The `training_queue` automatically offloads processing overhead from the UI. If a task fails repeatedly (e.g., due to network timeouts), it transitions to a **Dead Letter Queue (DLQ)** by setting its status to `dead`.

**Recovery Runbook:**
1. **Identify**: Query the DLQ.
   ```sql
   SELECT id, error_message, retry_count FROM training_queue WHERE status = 'dead';
   ```
2. **Investigate**: Cross-reference the `error_message` with your JSON log aggregator.
3. **Resolve**: If the failure was transient (e.g., an LLM provider outage), manually revive the task.
   ```sql
   UPDATE training_queue SET status = 'pending', retry_count = 0 WHERE status = 'dead';
   ```

## 3. Security & Access Control

### Least-Privilege Database User
The application must **never** run under the `postgres` superuser in production. Enforce a least-privilege security model.

```sql
-- Execute as Superuser
CREATE USER traveler_app_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE traveler_db TO traveler_app_user;
GRANT USAGE ON SCHEMA public TO traveler_app_user;

-- Grant strict DML access
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO traveler_app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO traveler_app_user;
```

### Credential Rotation
To rotate external provider keys (e.g., Groq):
1. Generate the new key via the provider's administration console.
2. Update the `.env` file or your encrypted secrets manager.
3. Restart the application process to instantiate the new connection pool. Background tasks currently in the queue will simply utilize the new key upon their next execution cycle.
