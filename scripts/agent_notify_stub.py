#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE_PATH = REPO_ROOT / ".agent" / "state.json"


class NotifyInputError(RuntimeError):
    pass


def resolve_repo_path(path_value: str | Path, *, must_exist: bool = False) -> Path:
    path = Path(path_value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    resolved = path.resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise NotifyInputError(f"path is outside this repo: {path_value}") from exc
    if must_exist and not resolved.exists():
        raise NotifyInputError(f"path does not exist: {path_value}")
    return resolved


def load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise NotifyInputError(f"JSON root must be an object: {path}")
    return data


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _state_repo_path(state: dict[str, Any], key: str, fallback: str) -> Path:
    value = state.get(key, fallback)
    if not isinstance(value, str):
        value = fallback
    return resolve_repo_path(value)


def write_notification(
    report_path: str | Path,
    gate_result: dict[str, Any],
    state_path: str | Path = DEFAULT_STATE_PATH,
) -> dict[str, Any]:
    if gate_result.get("needs_human") is not True:
        raise NotifyInputError("notify stub only writes for needs_human gate results")

    resolved_state_path = resolve_repo_path(state_path, must_exist=True)
    resolved_report_path = resolve_repo_path(report_path, must_exist=True)
    state = load_json(resolved_state_path)
    report = load_json(resolved_report_path)

    needs_human_path = _state_repo_path(state, "needs_human_path", ".agent/needs_human.json")
    notify_log_path = _state_repo_path(state, "notify_stub_log", ".agent/logs/notify_stub.log")
    created_at = utc_now()

    payload = {
        "created_at": created_at,
        "notification_sent": False,
        "reason": "stub_only_no_external_notification",
        "report_path": resolved_report_path.relative_to(REPO_ROOT).as_posix(),
        "gate_decision": gate_result.get("decision", ""),
        "gate_reasons": gate_result.get("reasons", []),
        "lane": report.get("lane", ""),
        "status": report.get("status", ""),
        "severity": report.get("severity", ""),
        "summary": report.get("summary", ""),
        "human_question": report.get("human_question", ""),
        "copyable_next_prompt": report.get("copyable_next_prompt", ""),
    }

    needs_human_path.parent.mkdir(parents=True, exist_ok=True)
    notify_log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(needs_human_path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    with open(notify_log_path, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
        handle.write("\n")

    return {
        "needs_human_path": needs_human_path.relative_to(REPO_ROOT).as_posix(),
        "notify_stub_log": notify_log_path.relative_to(REPO_ROOT).as_posix(),
        "payload": payload,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write a local needs-human notification stub.")
    parser.add_argument("--report", required=True, help="Worker report JSON path inside this repo.")
    parser.add_argument("--gate-result", required=True, help="Gate result JSON path inside this repo.")
    parser.add_argument(
        "--state",
        default=str(DEFAULT_STATE_PATH.relative_to(REPO_ROOT)),
        help="Agent state JSON path inside this repo.",
    )
    args = parser.parse_args(argv)

    try:
        gate_result = load_json(resolve_repo_path(args.gate_result, must_exist=True))
        result = write_notification(args.report, gate_result, args.state)
    except (NotifyInputError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
