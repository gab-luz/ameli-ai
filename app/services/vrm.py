"""Basic utilities for referencing VRM avatar models."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class VRMAvatar:
    """Metadata describing a VRM model on disk."""

    path: Path
    display_name: Optional[str] = None
    description: Optional[str] = None

    def exists(self) -> bool:
        return self.path.is_file()


class VRMRegistry:
    """Keeps track of Vtuber-style avatars for use within the UI."""

    def __init__(self) -> None:
        self._avatars: list[VRMAvatar] = []

    def add_avatar(self, avatar: VRMAvatar) -> None:
        self._avatars.append(avatar)

    def list_avatars(self) -> list[VRMAvatar]:
        return list(self._avatars)

    def first_available(self) -> Optional[VRMAvatar]:
        for avatar in self._avatars:
            if avatar.exists():
                return avatar
        return None
