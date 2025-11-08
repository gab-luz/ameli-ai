"""Home Assistant client helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from .http_client import AsyncHttpClient, HttpClientConfig


@dataclass
class HomeAssistantConfig:
    base_url: str
    token: str

    def headers(self) -> Mapping[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }


class HomeAssistantClient:
    """Tiny wrapper around the Home Assistant REST API."""

    def __init__(self, config: HomeAssistantConfig) -> None:
        self.config = config
        self._client = AsyncHttpClient(
            HttpClientConfig(base_url=config.base_url, headers=config.headers(), timeout=15.0)
        )

    async def fetch_states(self) -> Any:
        """Retrieve the entity states from Home Assistant."""
        return await self._client.request("GET", "/api/states")

    async def call_service(self, domain: str, service: str, payload: Optional[Mapping[str, Any]] = None) -> Any:
        """Trigger an action within Home Assistant."""
        path = f"/api/services/{domain}/{service}"
        return await self._client.request("POST", path, json_body=payload)

    async def create_event(self, event_type: str, data: Optional[Mapping[str, Any]] = None) -> Any:
        path = f"/api/events/{event_type}"
        return await self._client.request("POST", path, json_body=data)

    async def ping(self) -> bool:
        try:
            await self._client.request("GET", "/api/", params=None)
            return True
        except Exception:
            return False
