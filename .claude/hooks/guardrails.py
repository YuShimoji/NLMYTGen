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

CROSS_PROJECT_SCOPE_PATTERNS = [
    re.compile(r"cross[- ]project", re.IGNORECASE),
    re.compile(r"他\s*repo", re.IGNORECASE),
    re.compile(r"他プロジェクト"),
    re.compile(r"別プロジェクト"),
    re.compile(r"明示範囲"),
    re.compile(r"authority cleanup", re.IGNORECASE),
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

DOC_ROUTE_HANDOFF_PATTERNS = [
    re.compile(
        r"(?:手順の正本|手順.*正本|procedure source of truth|procedure source|source of truth)[^\n]*(?:\.md|README|manifest)(?::\d+)?",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:詳しい手順|詳細手順|手順詳細|詳細は)[^\n]*(?:\.md|README|manifest)[^\n]*(?:参照|見て|確認|従)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:\.md|README|manifest)[^\n]*(?:参照|見て|確認)[^\n]*(?:入力を置く|GUI|YMM4|Build CSV|Validate IR|Apply Production)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:\.md|README|manifest)[^\n]*(?:GUI|YMM4|Build CSV|Validate IR|Apply Production)[^\n]*(?:進め|操作|押|置|実行|press|run|select|open|\?{3,})",
        re.IGNORECASE,
    ),
]

ALLOWED_VISUAL_CONTEXT = [
    re.compile(r"初回\s*E2E"),
    re.compile(r"最終.*品質判断"),
    re.compile(r"最終制作物"),
]


def _read_payload() -> Any:
    raw = sys.stdin.read().lstrip("\ufeff")
    json_starts = [pos for pos in (raw.find("{"), raw.find("[")) if pos >= 0]
    if json_starts:
        raw = raw[min(json_starts) :]
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


def _has_cross_project_scope(strings: list[str]) -> bool:
    return _matches_any("\n".join(strings), CROSS_PROJECT_SCOPE_PATTERNS)


def _check_stop_content(strings: list[str]) -> str | None:
    joined = "\n".join(strings)
    if _matches_any(joined, STOP_PATTERNS):
        return "broad question / user-punt phrase detected"
    if _matches_any(joined, VISUAL_PROOF_PATTERNS) and not _matches_any(
        joined, ALLOWED_VISUAL_CONTEXT
    ):
        return "repeated visual proof request detected"
    if _matches_any(joined, DOC_ROUTE_HANDOFF_PATTERNS):
        return "md/README/manifest handoff laundering detected; inline exact user-operable steps instead"
    return None


def main() -> int:
    payload = _read_payload()
    strings = _collect_strings(payload)
    event = _event_name(payload).lower()

    if "stop" in event or "response" in event:
        forbidden = _contains_forbidden_path(strings)
        if forbidden and not _has_cross_project_scope(strings):
            print(
                "Guardrails rejected repo-external reference without explicit cross-project scope:\n"
                f"{forbidden}"
            )
            return 2

        issue = _check_stop_content(strings)
        if issue:
            print(f"Guardrails rejected assistant output: {issue}")
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
