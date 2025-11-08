"""Unified interface for selecting between LLM providers."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class LLMProviderConfig:
    provider: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None


class LLMRouter:
    """Dispatch LLM requests to OpenRouter, OpenAI, ElevenLabs or local models."""

    def __init__(self) -> None:
        self.configs: Dict[str, LLMProviderConfig] = {}

    def register(self, name: str, config: LLMProviderConfig) -> None:
        self.configs[name] = config

    async def ask(self, message: str, *, provider_name: Optional[str] = None) -> str:
        provider = self._resolve_provider(provider_name)
        # Placeholder: in a real implementation we would send HTTP requests to the provider.
        await asyncio.sleep(0.05)
        if provider.provider == "openrouter":
            return self._format_response("OpenRouter", message, provider)
        if provider.provider == "openai":
            return self._format_response("OpenAI", message, provider)
        if provider.provider == "elevenlabs":
            return self._format_response("ElevenLabs Conversational", message, provider)
        return self._format_response("Local LLaMA", message, provider)

    def _resolve_provider(self, provider_name: Optional[str]) -> LLMProviderConfig:
        if provider_name and provider_name in self.configs:
            return self.configs[provider_name]
        if "default" in self.configs:
            return self.configs["default"]
        if self.configs:
            return next(iter(self.configs.values()))
        # Fallback to a local tiny model configuration
        config = LLMProviderConfig(provider="local", model="llama-1b")
        self.configs["default"] = config
        return config

    def _format_response(self, provider_label: str, prompt: str, config: LLMProviderConfig) -> str:
        return (
            f"[{provider_label} - model={config.model or 'auto'}]\n"
            f"You asked: {prompt}\n"
            "This is a placeholder response demonstrating the chat pipeline."
        )
