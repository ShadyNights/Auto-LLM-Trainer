from typing import Optional, Dict, Any, Tuple
import json
from src.domain.dto.itinerary_request import ItineraryRequest
from src.domain.entities.system_config import SystemConfig
from src.repositories.config_repository import ConfigRepository
from src.repositories.prompt_repository import PromptRepository
from src.providers.base import ProviderInterface, ProviderRequest, ProviderResponse
from src.domain.exceptions import ConfigurationError, PromptNotFound

class PlannerService:
    def __init__(self, config_repo: ConfigRepository, prompt_repo: PromptRepository, provider: ProviderInterface):
        self.config_repo = config_repo
        self.prompt_repo = prompt_repo
        self.provider = provider
        
        # Simple cache for system config
        self._cached_config = None
        self._cached_at = 0
        self.CACHE_TTL = 300 # 5 minutes

    def _get_active_config(self) -> SystemConfig:
        import time
        now = time.time()
        
        if self._cached_config and (now - self._cached_at) < self.CACHE_TTL:
            return self._cached_config
            
        config = self.config_repo.get_active_config()
        if not config:
            raise ConfigurationError("No active configuration found in database.")
            
        self._cached_config = config
        self._cached_at = now
        return config

    def generate_itinerary(self, request: ItineraryRequest) -> Tuple[ProviderResponse, SystemConfig, str, str]:
        config = self._get_active_config()
        
        # We need the prompt version string. Since config stores IDs, we'd normally join.
        # For simplicity in this iteration, we assume the PromptRepository can handle IDs or we fetch the name.
        # We'll assume the prompt version is 'v1' for now, or we'd need a method to get prompt name by ID.
        # Let's fetch prompt text directly assuming prompt_repo has a default fallback or we hardcode 'v1'.
        # In a complete implementation we'd fetch the metadata from a repository.
        prompt_template = self.prompt_repo.get_prompt_text("v1")
        if not prompt_template:
            raise PromptNotFound("Failed to load active prompt.")
            
        # Format the prompt
        prompt = prompt_template.format(
            city=request.city,
            trip_days=request.trip_days,
            budget=request.budget,
            interests=", ".join(request.interests)
        )
        
        # Build provider request
        provider_request = ProviderRequest(
            prompt=prompt,
            temperature=0.7,
            max_tokens=2000,
            system_prompt="You are an expert AI Travel Planner.",
            metadata={"city": request.city}
        )
        
        response = self.provider.generate(provider_request)
        
        # Also return config and active versions so we can snapshot them
        return response, config, "v1", "v1" # (response, config, prompt_version, dataset_version)
