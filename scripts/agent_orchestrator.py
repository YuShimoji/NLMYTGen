#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent_gate import DEFAULT_STATE_PATH, REPO_ROOT, GateInputError, evaluate_report, load_json, resolve_repo_path
from agent_notify_stub import NotifyInputError, write_notification

WORKERS = ("advance", "audit", "fix", "summarize")


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _state_string(state: dict[str, Any], key: str, fallback: str) -> str:
    value = state.get(key, fallback)
    return value if isinstance(value, str) else fallback


def prompt_path_for_worker(state: dict[str, Any], worker: str) -> Path:
    catalog_dir = _state_string(state, "prompt_catalog_dir", ".agent/prompt_catalog")
    return resolve_repo_path(Path(catalog_dir) / f"{worker}.md", must_exist=True)


def build_dry_run_command(state: dict[str, Any], worker: str, prompt_path: Path) -> dict[str, Any]:
    schema_path = _state_string(state, "worker_report_schema", ".agent/schemas/worker_report.schema.json")
    template = _state_string(state, "report_output_template", ".agent/reports/{timestamp}-{worker}.report.json")
    report_path = template.format(timestamp=utc_stamp(), worker=worker)
    command = [
        "codex",
        "exec",
        "--output-schema",
        schema_path,
        "--prompt-file",
        prompt_path.relative_to(REPO_ROOT).as_posix(),
        "--output",
        report_path,
    ]
    return {
        "codex_execution_started": False,
        "worker": worker,
        "prompt": prompt_path.relative_to(REPO_ROOT).as_posix(),
        "expected_report": report_path,
        "command": command,
        "powershell": subprocess.list2cmdline(command),
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    state_path = resolve_repo_path(args.state, must_exist=True)
    state = load_json(state_path)
    prompt_path = prompt_path_for_worker(state, args.worker)

    result: dict[str, Any] = {
        "worker": args.worker,
        "state": state_path.relative_to(REPO_ROOT).as_posix(),
        "prompt": prompt_path.relative_to(REPO_ROOT).as_posix(),
    }

    if args.dry_run:
        result["dry_run"] = build_dry_run_command(state, args.worker, prompt_path)

    if args.report:
        gate_result = evaluate_report(args.report, state_path)
        result["gate_result"] = gate_result
        if gate_result["needs_human"]:
            result["notify_stub"] = write_notification(args.report, gate_result, state_path)

    if not args.dry_run and not args.report:
        result["codex_execution_started"] = False
        result["message"] = "No Codex execution is performed by the v0 orchestrator. Use --dry-run or --report."

    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Minimal Codex worker orchestration for NLMYTGen.")
    parser.add_argument("--worker", required=True, choices=WORKERS, help="Worker prompt to select.")
    parser.add_argument("--dry-run", action="store_true", help="Print the planned codex exec command.")
    parser.add_argument("--report", help="Evaluate an existing worker report JSON inside this repo.")
    parser.add_argument(
        "--state",
        default=str(DEFAULT_STATE_PATH.relative_to(REPO_ROOT)),
        help="Agent state JSON path inside this repo.",
    )
    args = parser.parse_args(argv)

    try:
        result = run(args)
    except (GateInputError, NotifyInputError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
