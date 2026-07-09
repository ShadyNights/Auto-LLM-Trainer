import os
import time
from groq import Groq
from src.providers.base import ProviderInterface, ProviderRequest, ProviderResponse
from src.domain.exceptions import ProviderUnavailable

class GroqProvider(ProviderInterface):
    def __init__(self, api_key: str = None, model: str = "llama-3.1-8b-instant"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        if not self.client:
            raise ProviderUnavailable("GROQ_API_KEY is not set.")

        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})

        start_time = time.time()
        
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        latency = int((time.time() - start_time) * 1000)
        
        choice = response.choices[0]
        usage = response.usage
        
        # Estimate cost (approximate LLaMA 3 8B pricing on Groq)
        # Assuming $0.05 per 1M input tokens and $0.08 per 1M output tokens
        estimated_cost = (usage.prompt_tokens / 1000000.0 * 0.05) + (usage.completion_tokens / 1000000.0 * 0.08)

        return ProviderResponse(
            text=choice.message.content,
            latency_ms=latency,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            finish_reason=choice.finish_reason,
            estimated_cost=estimated_cost
        )
