"""Utility helpers for making HTTP requests without imposing heavy dependencies."""
from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional dependency
    import httpx  # type: ignore
except Exception:  # pragma: no cover - the fallback path is exercised otherwise
    httpx = None


@dataclass
class HttpClientConfig:
    """Configuration for :class:`AsyncHttpClient`."""

    base_url: str
    headers: Mapping[str, str] = field(default_factory=dict)
    timeout: float = 20.0


class AsyncHttpClient:
    """A very small async HTTP helper supporting httpx when available."""

    def __init__(self, config: HttpClientConfig) -> None:
        self.config = config

    async def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Optional[Mapping[str, Any]] = None,
        params: Optional[Mapping[str, Any]] = None,
    ) -> Any:
        url = self._resolve_url(path, params)
        if httpx:
            return await self._request_httpx(method, url, json_body)
        return await self._request_stdlib(method, url, json_body)

    def _resolve_url(self, path: str, params: Optional[Mapping[str, Any]]) -> str:
        path = path.lstrip("/")
        url = f"{self.config.base_url.rstrip('/')}/{path}"
        if params:
            if httpx:
                query = httpx.QueryParams(params).to_str()
            else:
                query = urlencode(params)
            url = f"{url}?{query}"
        return url

    async def _request_httpx(self, method: str, url: str, json_body: Optional[Mapping[str, Any]]) -> Any:
        assert httpx is not None  # for the type checker
        async with httpx.AsyncClient(timeout=self.config.timeout, headers=self.config.headers) as client:
            response = await client.request(method.upper(), url, json=json_body)
            response.raise_for_status()
            if response.headers.get("content-type", "").startswith("application/json"):
                return response.json()
            return response.text

    async def _request_stdlib(self, method: str, url: str, json_body: Optional[Mapping[str, Any]]) -> Any:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self._blocking_request,
            method,
            url,
            json_body,
        )

    def _blocking_request(self, method: str, url: str, json_body: Optional[Mapping[str, Any]]) -> Any:
        payload: Optional[bytes] = None
        headers = dict(self.config.headers)
        if json_body is not None:
            payload = json.dumps(json_body).encode("utf-8")
            headers.setdefault("Content-Type", "application/json")
        req = urllib_request.Request(url, data=payload, headers=headers, method=method.upper())
        try:
            with urllib_request.urlopen(req, timeout=self.config.timeout) as response:
                charset = response.headers.get_content_charset("utf-8")
                raw = response.read().decode(charset)
                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    return json.loads(raw)
                return raw
        except HTTPError as exc:
            logger.error("HTTP error %s for %s", exc.code, url)
            raise
        except URLError as exc:
            logger.error("URL error for %s: %s", url, exc.reason)
            raise
