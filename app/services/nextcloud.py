"""Nextcloud productivity suite helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional
import base64

from .http_client import AsyncHttpClient, HttpClientConfig


@dataclass
class NextcloudConfig:
    base_url: str
    username: str
    password: str

    def headers(self) -> Mapping[str, str]:
        token = base64.b64encode(f"{self.username}:{self.password}".encode("utf-8")).decode("ascii")
        return {
            "OCS-APIRequest": "true",
            "Authorization": f"Basic {token}",
        }


class NextcloudClient:
    """Wrapper around the Nextcloud OCS API."""

    def __init__(self, config: NextcloudConfig) -> None:
        self.config = config
        self._client = AsyncHttpClient(
            HttpClientConfig(
                base_url=config.base_url,
                headers=config.headers(),
            )
        )

    async def list_contacts(self) -> Any:
        return await self._client.request(
            "GET",
            "/ocs/v2.php/apps/contacts/api/v1/addressbook",
            params={"format": "json"},
        )

    async def list_tasks(self) -> Any:
        return await self._client.request(
            "GET",
            "/ocs/v2.php/apps/tasks/api/v1/tasks",
            params={"format": "json"},
        )

    async def create_todo(self, title: str, due: Optional[str] = None) -> Any:
        payload = {"title": title}
        if due:
            payload["due"] = due
        return await self._client.request(
            "POST",
            "/ocs/v2.php/apps/tasks/api/v1/tasks",
            json_body=payload,
        )
