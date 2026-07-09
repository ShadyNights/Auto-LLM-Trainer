from typing import Any

from src.infrastructure.database.connection import DatabaseConnection


class TrainingRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def enqueue(self, itinerary_id: int) -> int:
        with self.db.get_cursor() as cur:
            cur.execute("INSERT INTO training_queue (itinerary_id) VALUES (%s) RETURNING id", (itinerary_id,))
            return cur.fetchone()["id"]

    def get_pending_tasks(self, limit: int = 10) -> list[dict[str, Any]]:
        with self.db.get_cursor(commit_on_success=False) as cur:
            cur.execute(
                "SELECT * FROM training_queue WHERE status = 'pending' ORDER BY created_at ASC LIMIT %s", (limit,)
            )
            return cur.fetchall()

    def update_status(
        self,
        task_id: int,
        status: str,
        error_message: str | None = None,
        duration: int | None = None,
        increment_retry: bool = False,
    ):
        with self.db.get_cursor() as cur:
            updates = ["status = %s", "updated_at = NOW()"]
            params = [status]

            if error_message is not None:
                updates.append("error_message = %s")
                params.append(error_message)

            if duration is not None:
                updates.append("duration = %s")
                updates.append("finished_at = NOW()")
                params.append(duration)

            if increment_retry:
                updates.append("retry_count = retry_count + 1")

            params.append(task_id)

            query = f"UPDATE training_queue SET {', '.join(updates)} WHERE id = %s"
            cur.execute(query, tuple(params))
