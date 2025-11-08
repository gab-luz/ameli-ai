"""Background asyncio runner for the Kivy app."""
from __future__ import annotations

import asyncio
import threading
from typing import Awaitable, Callable, Optional

from kivy.clock import Clock


class AsyncExecutor:
    """Runs an asyncio loop on a dedicated background thread."""

    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def _run_loop(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def submit(self, coro: Awaitable, callback: Optional[Callable[[object], None]] = None) -> None:
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        if callback:
            def _cb(fut):
                try:
                    result = fut.result()
                except Exception as exc:  # pragma: no cover - UI side handles logging
                    Clock.schedule_once(lambda _dt: callback(exc))
                    return
                Clock.schedule_once(lambda _dt: callback(result))
            future.add_done_callback(_cb)

    def shutdown(self) -> None:
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join(timeout=1.0)
