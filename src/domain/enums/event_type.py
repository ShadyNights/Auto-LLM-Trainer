from enum import Enum

class EventType(str, Enum):
    PROMPT_SUBMITTED = 'PromptSubmitted'
    GENERATION_STARTED = 'GenerationStarted'
    GENERATION_COMPLETED = 'GenerationCompleted'
    FEEDBACK = 'Feedback'
    EXPORT = 'Export'
    SHARE = 'Share'
    RETRY = 'Retry'
    FAILURE = 'Failure'
