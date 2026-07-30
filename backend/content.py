"""Content loading helpers for editable LUCERNA 65 JSON files."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SUPPORTED_LOCALES = {"ca", "es", "en"}


@lru_cache(maxsize=32)
def read_json(relative: str):
    path = CONTENT / relative
    return json.loads(path.read_text(encoding="utf-8"))


def locale_or_ca(locale: str) -> str:
    value = (locale or "ca").strip().lower().split("-")[0]
    return value if value in SUPPORTED_LOCALES else "ca"


def localized(item: dict, key: str, locale: str, default: str = "") -> str:
    locale = locale_or_ca(locale)
    direct = item.get(f"{key}_{locale}")
    if direct:
        return str(direct)
    value = item.get(key)
    if isinstance(value, dict):
        return str(value.get(locale) or value.get("ca") or default)
    return str(value or default)
