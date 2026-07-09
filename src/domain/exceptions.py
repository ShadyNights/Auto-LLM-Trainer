class TravelerException(Exception):
    """Base exception for all domain-specific errors in Traveler LLM."""

    pass


class ProviderUnavailable(TravelerException):
    """Raised when an LLM provider is unreachable or returns an error."""

    pass


class PromptNotFound(TravelerException):
    """Raised when a requested prompt version cannot be located or is empty."""

    pass


class ConfigurationError(TravelerException):
    """Raised when the system configuration is invalid or missing."""

    pass


class EvaluationFailed(TravelerException):
    """Raised when a dataset or generated output fails evaluation checks."""

    pass


class QueueProcessingError(TravelerException):
    """Raised when a background job encounters an unrecoverable queue error."""

    pass
