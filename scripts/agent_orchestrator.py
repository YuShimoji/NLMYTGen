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
DEFAULT_REPO_STATUS = {
    "provided": False,
    "tracked_dirty": [],
    "staged": [],
    "untracked": [],
    "allowed_untracked": [],
    "unknown_untracked": [],
}


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


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


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


def _path_allowed_by_prefix(path_value: str, allowed_values: list[str]) -> bool:
    normalized = path_value.replace("\\", "/")
    for allowed_value in allowed_values:
        allowed = allowed_value.replace("\\", "/")
        if allowed.endswith("/"):
            if normalized.startswith(allowed):
                return True
        elif normalized == allowed:
            return True
    return False


def repo_status_policy_result(repo_status: dict[str, Any] | None) -> dict[str, Any]:
    if repo_status is None:
        return dict(DEFAULT_REPO_STATUS)

    tracked_dirty = _string_list(repo_status.get("tracked_dirty", repo_status.get("dirty_tracked", [])))
    staged = _string_list(repo_status.get("staged", repo_status.get("staged_files", [])))
    untracked = _string_list(repo_status.get("untracked", repo_status.get("untracked_files", [])))
    allowed_untracked = _string_list(
        repo_status.get("allowed_untracked", repo_status.get("allowed_untracked_paths", []))
    )
    unknown_untracked = [
        path_value for path_value in untracked if not _path_allowed_by_prefix(path_value, allowed_untracked)
    ]
    return {
        "provided": True,
        "tracked_dirty": tracked_dirty,
        "staged": staged,
        "untracked": untracked,
        "allowed_untracked": allowed_untracked,
        "unknown_untracked": unknown_untracked,
    }


def _preflight_path_reason(path_value: str, parent: Path, label: str, *, must_exist: bool = False) -> str | None:
    try:
        path = resolve_repo_path(path_value, must_exist=must_exist)
        _ensure_under(path, parent, label)
    except GateInputError as exc:
        return f"{label}:{exc}"
    return None


def _execution_policy_reasons(state: dict[str, Any]) -> tuple[list[str], bool, Any, Any]:
    reasons: list[str] = []
    raw_policy = state.get("execution_policy")
    if not isinstance(raw_policy, dict):
        reasons.append("execution_policy:missing_or_invalid")
        raw_policy = {}

    execution_enabled = raw_policy.get("codex_exec_enabled") is True
    if not execution_enabled:
        reasons.append("execution_policy.codex_exec_enabled:false")

    max_steps = raw_policy.get("max_steps")
    if "max_steps" not in raw_policy:
        reasons.append("execution_policy.max_steps:missing")
    elif isinstance(max_steps, bool) or not isinstance(max_steps, int):
        reasons.append("execution_policy.max_steps:invalid")
    elif max_steps < 1:
        reasons.append("execution_policy.max_steps:less_than_1")
    elif max_steps > 1:
        reasons.append("execution_policy.max_steps:greater_than_1")

    timeout_seconds = raw_policy.get("timeout_seconds")
    if "timeout_seconds" not in raw_policy:
        reasons.append("execution_policy.timeout_seconds:missing")
    elif isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, int):
        reasons.append("execution_policy.timeout_seconds:invalid")
    elif timeout_seconds <= 0:
        reasons.append("execution_policy.timeout_seconds:non_positive")

    return reasons, execution_enabled, max_steps, timeout_seconds


def build_execution_preflight(
    state: dict[str, Any],
    worker: str,
    plan: ExecutionPlan | None = None,
    repo_status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    reasons, execution_enabled, max_steps, timeout_seconds = _execution_policy_reasons(state)
    repo_status_result = repo_status_policy_result(repo_status)
    plan_error = ""

    if plan is None:
        try:
            plan = build_execution_plan(state, worker)
        except GateInputError as exc:
            plan_error = str(exc)
            reasons.append(f"execution_plan:{plan_error}")

    prompt_path = plan.prompt_path if plan else ""
    schema_path = plan.schema_path if plan else ""
    report_path = plan.report_path if plan else ""

    if plan is not None:
        for maybe_reason in (
            _preflight_path_reason(plan.prompt_path, PROMPT_ROOT, "prompt_path", must_exist=True),
            _preflight_path_reason(plan.schema_path, SCHEMA_ROOT, "schema_path", must_exist=True),
            _preflight_path_reason(plan.report_path, REPORT_ROOT, "report_path"),
        ):
            if maybe_reason:
                reasons.append(maybe_reason)
        try:
            report_exists = resolve_repo_path(plan.report_path).exists()
        except GateInputError:
            report_exists = False
        if report_exists:
            reasons.append(f"report_path:already_exists:{plan.report_path}")

    if not repo_status_result["provided"]:
        reasons.append("repo_status:not_provided")
    if repo_status_result["tracked_dirty"]:
        reasons.append("repo_status:tracked_dirty")
    if repo_status_result["staged"]:
        reasons.append("repo_status:staged_files_present")
    if repo_status_result["unknown_untracked"]:
        reasons.append("repo_status:unknown_untracked_files")

    return {
        "allowed": not reasons,
        "reasons": reasons,
        "execution_enabled": execution_enabled,
        "worker": worker,
        "prompt_path": prompt_path,
        "schema_path": schema_path,
        "report_path": report_path,
        "max_steps": max_steps,
        "timeout_seconds": timeout_seconds,
        "repo_status": repo_status_result,
        "plan_error": plan_error,
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
        execution_plan_obj = build_execution_plan(state, args.worker)
        execution_plan = execution_plan_obj.to_dict()
        execution_plan["powershell"] = powershell_preview(execution_plan["argv"])
        execution_plan["preflight"] = build_execution_preflight(state, args.worker, execution_plan_obj)
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
