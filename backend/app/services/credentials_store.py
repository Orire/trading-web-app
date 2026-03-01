"""
Local credentials storage for tenant-scoped settings.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional
import json


class CredentialsStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._file_path = Path(__file__).resolve().parents[2] / "data" / "etoro_credentials.json"

    def _ensure_parent(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> Optional[Dict[str, Any]]:
        if not self._file_path.exists():
            return None
        with self._file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, payload: Dict[str, Any]) -> None:
        self._ensure_parent()
        with self._file_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    @staticmethod
    def _mask(value: str) -> str:
        if len(value) <= 6:
            return "*" * len(value)
        return f"{value[:4]}...{value[-2:]}"

    def save_etoro_credentials(
        self, api_key: str, api_secret: str, base_url: str, environment: str
    ) -> Dict[str, Any]:
        payload = {
            "api_key": api_key.strip(),
            "api_secret": api_secret.strip(),
            "base_url": base_url.strip(),
            "environment": environment.strip().lower(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        with self._lock:
            self._write(payload)
        return {
            "configured": True,
            "api_key_masked": self._mask(payload["api_key"]),
            "base_url": payload["base_url"],
            "environment": payload["environment"],
            "updated_at": payload["updated_at"],
        }

    def get_etoro_credentials_status(self) -> Dict[str, Any]:
        with self._lock:
            payload = self._read()

        if not payload:
            return {"configured": False}

        return {
            "configured": True,
            "api_key_masked": self._mask(payload.get("api_key", "")),
            "base_url": payload.get("base_url"),
            "environment": payload.get("environment"),
            "updated_at": payload.get("updated_at"),
        }
