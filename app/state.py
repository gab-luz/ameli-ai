"""Application state containers used by the Kivy interface."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class IntegrationStatus:
    """Represents the online/offline state of a backend integration."""

    name: str
    is_connected: bool = False
    last_error: Optional[str] = None
    last_updated: Optional[str] = None

    @property
    def status_label(self) -> str:
        if self.is_connected:
            return "Connected"
        if self.last_error:
            return f"Error: {self.last_error}"
        return "Disconnected"


@dataclass
class ChatMessage:
    """A message that appears in the chat view."""

    author: str
    content: str
    is_user: bool = False
    avatar_hint: Optional[str] = None


@dataclass
class AppState:
    """Global state shared between UI components and service layers."""

    integrations: Dict[str, IntegrationStatus] = field(default_factory=dict)
    chat_history: List[ChatMessage] = field(default_factory=list)
    anime_art_paths: List[str] = field(default_factory=list)

    def ensure_integration(self, name: str) -> IntegrationStatus:
        if name not in self.integrations:
            self.integrations[name] = IntegrationStatus(name=name)
        return self.integrations[name]

    def push_message(self, message: ChatMessage) -> None:
        self.chat_history.append(message)
