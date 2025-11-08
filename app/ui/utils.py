"""Helpers for managing UI assets and theming."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List


def discover_anime_art(paths: Iterable[Path]) -> List[str]:
    """Return a list of image paths that can be used as anime themed art."""

    supported_extensions = {".png", ".jpg", ".jpeg", ".gif"}
    discovered: List[str] = []
    for base in paths:
        if not base.exists():
            continue
        if base.is_file() and base.suffix.lower() in supported_extensions:
            discovered.append(str(base.resolve()))
            continue
        for child in base.rglob("*"):
            if child.suffix.lower() in supported_extensions:
                discovered.append(str(child.resolve()))
    return discovered
