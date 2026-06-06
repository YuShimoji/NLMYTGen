#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent_gate import DEFAULT_STATE_PATH, REPO_ROOT, GateInputError, evaluate_report, load_json, resolve_repo_path
from agent_notify_stub import NotifyInputError, write_notification

WORKERS = ("advance", "audit", "fix", "summarize")
PROMPT_ROOT = REPO_ROOT / ".agent" / "prompt_catalog"
SCHEMA_ROOT = REPO_ROOT / ".agent" / "schemas"
REPORT_ROOT = REPO_ROOT / ".agent" / "reports"


@dataclass(frozen=True)
class ExecutionPlan:
    worker: str
    cwd: str
    prompt_path: str
    schema_path: str
    report_path: str
    argv: list[str]
    stdin_source: str
    prompt_input_mode: str
    codex_execution_started: bool
    execution_policy: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _state_string(state: dict[str, Any], key: str, fallback: str) -> str:
    value = state.get(key, fallback)
    return value if isinstance(value, str) else fallback


def _repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _ensure_under(path: Path, parent: Path, label: str) -> Path:
    resolved_parent = parent.resolve()
    try:
        path.relative_to(resolved_parent)
    except ValueError as exc:
        raise GateInputError(f"{label} must stay under {_repo_relative(resolved_parent)}: {path}") from exc
    return path


def execution_policy_from_state(state: dict[str, Any]) -> dict[str, Any]:
    raw_policy = state.get("execution_policy", {})
    if not isinstance(raw_policy, dict):
        raw_policy = {}
    max_steps = raw_policy.get("max_steps")
    timeout_seconds = raw_policy.get("timeout_seconds")
    return {
        "codex_exec_enabled": raw_policy.get("codex_exec_enabled") is True,
        "max_steps": max_steps if isinstance(max_steps, int) and not isinstance(max_steps, bool) else 1,
        "timeout_seconds": (
            timeout_seconds if isinstance(timeout_seconds, int) and not isinstance(timeout_seconds, bool) else 600
        ),
    }


def prompt_path_for_worker(state: dict[str, Any], worker: str) -> Path:
    if worker not in WORKERS:
        raise GateInputError(f"invalid worker: {worker}")
    catalog_dir = _state_string(state, "prompt_catalog_dir", ".agent/prompt_catalog")
    prompt_path = resolve_repo_path(Path(catalog_dir) / f"{worker}.md", must_exist=True)
    return _ensure_under(prompt_path, PROMPT_ROOT, "prompt_path")


def schema_path_from_state(state: dict[str, Any]) -> Path:
    schema_path = _state_string(state, "worker_report_schema", ".agent/schemas/worker_report.schema.json")
    resolved_schema_path = resolve_repo_path(schema_path, must_exist=True)
    return _ensure_under(resolved_schema_path, SCHEMA_ROOT, "schema_path")


def report_path_for_worker(state: dict[str, Any], worker: str, timestamp: str | None = None) -> Path:
    if worker not in WORKERS:
        raise GateInputError(f"invalid worker: {worker}")
    stamp = timestamp or utc_stamp()
    template = _state_string(state, "report_output_template", ".agent/reports/{timestamp}-{worker}.report.json")
    if template:
        report_path = template.format(timestamp=stamp, worker=worker)
    else:
        report_dir = _state_string(state, "report_dir", ".agent/reports")
        report_path = str(Path(report_dir) / f"{stamp}-{worker}.report.json")
    resolved_report_path = resolve_repo_path(report_path)
    return _ensure_under(resolved_report_path, REPORT_ROOT, "report_path")


def powershell_preview(argv: list[str]) -> str:
    def quote(arg: str) -> str:
        if arg and all(char.isalnum() or char in "-_./:\\" for char in arg):
            return arg
        return "'" + arg.replace("'", "''") + "'"

    return " ".join(quote(arg) for arg in argv)


def build_execution_plan(state: dict[str, Any], worker: str, timestamp: str | None = None) -> ExecutionPlan:
    prompt_path = prompt_path_for_worker(state, worker)
    schema_path = schema_path_from_state(state)
    report_path = report_path_for_worker(state, worker, timestamp)
    schema_arg = _repo_relative(schema_path)
    report_arg = _repo_relative(report_path)
    argv = [
        "codex",
        "exec",
        "-",
        "--output-schema",
        schema_arg,
        "-o",
        report_arg,
    ]
    return ExecutionPlan(
        worker=worker,
        cwd=str(REPO_ROOT),
        prompt_path=_repo_relative(prompt_path),
        schema_path=schema_arg,
        report_path=report_arg,
        argv=argv,
        stdin_source=_repo_relative(prompt_path),
        prompt_input_mode="stdin_from_prompt_file",
        codex_execution_started=False,
        execution_policy=execution_policy_from_state(state),
    )


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
        execution_plan = build_execution_plan(state, args.worker).to_dict()
        execution_plan["powershell"] = powershell_preview(execution_plan["argv"])
        result["dry_run"] = execution_plan

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
