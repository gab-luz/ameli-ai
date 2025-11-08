"""Grocy ERP-style household management helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .http_client import AsyncHttpClient, HttpClientConfig


@dataclass
class GrocyConfig:
    base_url: str
    api_key: str

    def headers(self) -> Mapping[str, str]:
        return {
            "GROCY-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }


class GrocyClient:
    """Interact with the Grocy REST API."""

    def __init__(self, config: GrocyConfig) -> None:
        self.config = config
        self._client = AsyncHttpClient(
            HttpClientConfig(base_url=config.base_url, headers=config.headers())
        )

    async def stock(self) -> Any:
        return await self._client.request("GET", "/api/stock")

    async def chores(self) -> Any:
        return await self._client.request("GET", "/api/chores")

    async def add_product(self, payload: Mapping[str, Any]) -> Any:
        return await self._client.request("POST", "/api/stock/products", json_body=payload)
