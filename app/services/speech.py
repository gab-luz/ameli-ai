"""Speech-to-text and text-to-speech abstractions."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Optional


@dataclass
class WhisperConfig:
    model_path: str = "tiny"
    language: Optional[str] = None


@dataclass
class TTSConfig:
    engine: str = "kokoro"  # kokoro, piper, builtin
    voice: Optional[str] = None


class SpeechOrchestrator:
    """Coordinates STT and TTS pipelines."""

    def __init__(self) -> None:
        self.whisper_config = WhisperConfig()
        self.tts_config = TTSConfig()

    async def transcribe(self, audio_path: str) -> str:
        await asyncio.sleep(0.05)
        return f"[Whisper:{self.whisper_config.model_path}] Transcript placeholder for {audio_path}"

    async def synthesize(self, text: str, *, engine: Optional[str] = None) -> bytes:
        await asyncio.sleep(0.05)
        engine = engine or self.tts_config.engine
        sample = f"[{engine} voice={self.tts_config.voice or 'default'}] {text}".encode("utf-8")
        return sample

    def set_whisper_model(self, model_path: str, language: Optional[str] = None) -> None:
        self.whisper_config.model_path = model_path
        self.whisper_config.language = language

    def set_tts_engine(self, engine: str, voice: Optional[str] = None) -> None:
        self.tts_config.engine = engine
        self.tts_config.voice = voice
