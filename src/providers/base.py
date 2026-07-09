from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProviderRequest:
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderResponse:
    text: str
    latency_ms: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    finish_reason: str
    estimated_cost: float = 0.0


class ProviderInterface(ABC):
    @abstractmethod
    def generate(self, request: ProviderRequest) -> ProviderResponse:
        pass
