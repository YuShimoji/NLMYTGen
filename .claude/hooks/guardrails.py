from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = str(Path(__file__).resolve().parents[2]).lower()

FORBIDDEN_PATTERNS = [
    re.compile(r"holosync", re.IGNORECASE),
    re.compile(r"nlmandslidevideogenerator", re.IGNORECASE),
    re.compile(r"narrativegen", re.IGNORECASE),
    re.compile(r"vastcore", re.IGNORECASE),
    re.compile(r"[\\/]\.claude[\\/]+projects[\\/]", re.IGNORECASE),
]

STOP_PATTERNS = [
    re.compile(r"判断をお願いします"),
    re.compile(r"何が足りないか教えてください"),
    re.compile(r"何をすべきか教えてください"),
    re.compile(r"どこに pain があるか教えてください", re.IGNORECASE),
    re.compile(r"クローズすべき", re.IGNORECASE),
]

VISUAL_PROOF_PATTERNS = [
    re.compile(r"YMM4\s*で確認してください"),
    re.compile(r"visual\s+proof", re.IGNORECASE),
    re.compile(r"開いて確認"),
]

ALLOWED_VISUAL_CONTEXT = [
    re.compile(r"初回\s*E2E"),
    re.compile(r"最終.*品質判断"),
    re.compile(r"最終制作物"),
]


def _read_payload() -> Any:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def _collect_strings(value: Any) -> list[str]:
    results: list[str] = []
    if isinstance(value, str):
        results.append(value)
    elif isinstance(value, dict):
        for k, v in value.items():
            results.extend(_collect_strings(k))
            results.extend(_collect_strings(v))
    elif isinstance(value, list):
        for item in value:
            results.extend(_collect_strings(item))
    return results


def _event_name(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    for key in ("event", "event_name", "hook_event_name", "type"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    return ""


def _contains_forbidden_path(strings: list[str]) -> str | None:
    for text in strings:
        lowered = text.lower()
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(lowered):
                return text
        if lowered.startswith(("c:\\", "d:\\", "/")) and REPO_ROOT not in lowered:
            if any(token in lowered for token in ("media contents projects", ".claude\\projects", ".claude/projects")):
                return text
    return None


def _matches_any(text: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def _check_stop_content(strings: list[str]) -> str | None:
    joined = "\n".join(strings)
    if _matches_any(joined, STOP_PATTERNS):
        return "broad question / user-punt phrase detected"
    if _matches_any(joined, VISUAL_PROOF_PATTERNS) and not _matches_any(
        joined, ALLOWED_VISUAL_CONTEXT
    ):
        return "repeated visual proof request detected"
    return None


def main() -> int:
    payload = _read_payload()
    strings = _collect_strings(payload)
    event = _event_name(payload).lower()

    forbidden = _contains_forbidden_path(strings)
    if forbidden:
        print(
            "Guardrails rejected repo-external or forbidden project reference:\n"
            f"{forbidden}"
        )
        return 2

    if "stop" in event or "response" in event:
        issue = _check_stop_content(strings)
        if issue:
            print(f"Guardrails rejected assistant output: {issue}")
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
