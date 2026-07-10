#!/usr/bin/env python3
"""Claude hook that enforces only the repository's cross-project boundary."""

from __future__ import annotations

import json
import re
import sys
from typing import Any


HOOK_METADATA_KEYS = {
    "cwd",
    "event",
    "event_name",
    "hook_event_name",
    "model",
    "session_id",
    "transcript_path",
    "type",
}

FORBIDDEN_PATTERNS = [
    re.compile(r"holosync", re.IGNORECASE),
    re.compile(r"nlmandslidevideogenerator", re.IGNORECASE),
    re.compile(r"narrativegen", re.IGNORECASE),
    re.compile(r"vastcore", re.IGNORECASE),
    re.compile(r"[\\/]\.claude[\\/]+projects[\\/]", re.IGNORECASE),
]

CROSS_PROJECT_SCOPE_PATTERNS = [
    re.compile(r"cross[- ]project", re.IGNORECASE),
    re.compile(r"cross[- ]repo", re.IGNORECASE),
    re.compile(r"他\s*repo", re.IGNORECASE),
    re.compile(r"別\s*repo", re.IGNORECASE),
    re.compile(r"他プロジェクト"),
    re.compile(r"別プロジェクト"),
    re.compile(r"明示範囲"),
    re.compile(r"authority cleanup", re.IGNORECASE),
]


def _read_payload() -> Any:
    try:
        return json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}


def _collect_strings(value: Any, *, key: str | None = None) -> list[str]:
    """Collect content strings while ignoring hook metadata such as cwd paths."""

    if key in HOOK_METADATA_KEYS:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for child_key, child_value in value.items():
            strings.extend(_collect_strings(child_value, key=str(child_key)))
        return strings
    if isinstance(value, (list, tuple)):
        strings = []
        for child_value in value:
            strings.extend(_collect_strings(child_value))
        return strings
    return []


def _event_name(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    for key in ("hook_event_name", "event_name", "event", "type"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    return ""


def _contains_forbidden_path(strings: list[str]) -> str | None:
    for value in strings:
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(value):
                return value
    return None


def _has_cross_project_scope(strings: list[str]) -> bool:
    text = "\n".join(strings)
    return any(pattern.search(text) for pattern in CROSS_PROJECT_SCOPE_PATTERNS)


def _reject(message: str) -> int:
    print(message, file=sys.stderr)
    return 2


def main() -> int:
    payload = _read_payload()
    if _event_name(payload).lower() not in {"stop", "response"}:
        return 0

    strings = _collect_strings(payload)
    forbidden = _contains_forbidden_path(strings)
    if forbidden and not _has_cross_project_scope(strings):
        return _reject(
            "Guardrails rejected a repo-external reference without explicit "
            f"cross-project scope:\n{forbidden}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
