from enum import Enum

class TableType(Enum):
    ITINERARIES = "itineraries"
    CONVERSATIONS = "conversations"
    EVENTS = "events"
    DATASETS = "datasets"
    MODEL_VERSIONS = "model_versions"
    PROMPTS_METADATA = "prompts_metadata"
    CONFIG_EVALUATIONS = "config_evaluations"
    TRAINING_QUEUE = "training_queue"
    AUDIT_LOGS = "audit_logs"
    SYSTEM_CONFIG = "system_config"
    TRIPS = "trips"
    USERS = "users"
    TRAINING_DATA = "training_data"
