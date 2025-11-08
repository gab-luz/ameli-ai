"""Simple SQLite-backed configuration store for development use."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Mapping, Optional


class ConfigStore:
    """Persists key/value configuration pairs to a local SQLite database."""

    def __init__(self, db_path: Path) -> None:
        self._path = Path(db_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self._path, detect_types=sqlite3.PARSE_DECLTYPES)
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        cursor = self._connection.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else default

    def set(self, key: str, value: str) -> None:
        with self._connection:
            self._connection.execute(
                "INSERT INTO settings(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, value),
            )

    def ensure_defaults(self, values: Mapping[str, str]) -> None:
        missing: Iterable[str] = [key for key in values if self.get(key) is None]
        if not missing:
            return
        with self._connection:
            self._connection.executemany(
                "INSERT OR IGNORE INTO settings(key, value) VALUES(?, ?)",
                [(key, values[key]) for key in missing],
            )
