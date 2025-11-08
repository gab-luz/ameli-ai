"""Defines theme colors inspired by Miru and Alexa."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    primary: str = "#1a1f3b"
    accent: str = "#5f7cff"
    background: str = "#0b0e1a"
    surface: str = "#161a2f"
    text_primary: str = "#f4f6ff"
    text_secondary: str = "#b3b9d3"


THEME = Theme()
