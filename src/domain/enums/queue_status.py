from enum import Enum


class QueueStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "completed"
    DEAD = "dead"
