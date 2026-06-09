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
PREFLIGHT_MODES = ("dry_run_preview", "fake_runner_helper", "real_runner")
LOCAL_NOTIFICATION_POLICY = "local_stub_only"
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


@dataclass(frozen=True)
class FakeRunnerResult:
    mode: str
    scenario: str
    worker: str
    plan: dict[str, Any]
    exit_code: int | None
    timed_out: bool
    report_path: str
    report_written: bool
    stdout: str
    stderr: str
    error_kind: str
    codex_execution_started: bool
    real_subprocess_started: bool
    artifacts_written: list[str]
    fail_closed: bool
    gate_result: dict[str, Any] | None = None
    notify_stub: dict[str, Any] | None = None

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


def _preflight_mode_reasons(mode: str) -> list[str]:
    if mode in PREFLIGHT_MODES:
        return []
    return [f"mode:invalid:{mode}"]


def _command_shape_reasons(plan: ExecutionPlan) -> list[str]:
    argv = plan.argv
    if isinstance(argv, str):
        return ["command_shape:shell_string"]
    if not isinstance(argv, list) or any(not isinstance(arg, str) for arg in argv):
        return ["command_shape:invalid_argv"]
    if len(argv) < 3 or argv[:3] != ["codex", "exec", "-"]:
        return ["command_shape:invalid_argv"]
    shell_markers = ("|", "&&", "||", ";", ">", "<")
    if any(any(marker in arg for marker in shell_markers) for arg in argv):
        return ["command_shape:shell_dependent_argument"]
    return []


def _prompt_source_reasons(plan: ExecutionPlan) -> list[str]:
    if not isinstance(plan.stdin_source, str) or not plan.stdin_source:
        return ["prompt_source:ambiguous"]
    if not isinstance(plan.prompt_input_mode, str) or not plan.prompt_input_mode:
        return ["prompt_source:ambiguous"]
    if plan.prompt_input_mode != "stdin_from_prompt_file":
        return [f"prompt_source:unsupported_mode:{plan.prompt_input_mode}"]
    if plan.stdin_source != plan.prompt_path:
        return ["prompt_source:mismatch"]
    return []


def _notification_policy_reason(mode: str, notification_policy: str | None) -> str | None:
    if mode != "real_runner":
        return None
    if notification_policy != LOCAL_NOTIFICATION_POLICY:
        return "notification_policy:ambiguous"
    return None


def _credential_like_reason(value: str) -> bool:
    token_markers = (
        "sk-",
        "ghp_",
        "github_pat_",
        "AKIA",
        "xoxb-",
        "xoxp-",
        "xoxa-",
        "xoxr-",
        "AIza",
    )
    return any(marker in value for marker in token_markers)


def _credential_reasons(credential_like_values: Any) -> list[str]:
    if credential_like_values is None:
        return []
    if isinstance(credential_like_values, dict):
        items = credential_like_values.items()
    elif isinstance(credential_like_values, list):
        items = ((f"value_{index}", value) for index, value in enumerate(credential_like_values))
    else:
        items = (("value", credential_like_values),)
    reasons: list[str] = []
    for label, value in items:
        if isinstance(value, str) and _credential_like_reason(value):
            reasons.append(f"credential_like_value:{label}")
    return reasons


def _preflight_inspected_paths(plan: ExecutionPlan | None) -> list[str]:
    if plan is None:
        return []
    values = [plan.prompt_path, plan.schema_path, plan.report_path]
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def build_execution_preflight(
    state: dict[str, Any],
    worker: str,
    plan: ExecutionPlan | None = None,
    repo_status: dict[str, Any] | None = None,
    *,
    mode: str = "real_runner",
    human_real_execution_authority: bool = False,
    notification_policy: str | None = None,
    environment_policy: str = "not_inspected",
    credential_like_values: Any = None,
) -> dict[str, Any]:
    reasons: list[str] = []
    mode_reasons = _preflight_mode_reasons(mode)
    reasons.extend(mode_reasons)
    policy_reasons, execution_enabled, max_steps, timeout_seconds = _execution_policy_reasons(state)
    if mode == "real_runner":
        reasons.extend(policy_reasons)
        if not human_real_execution_authority:
            reasons.append("missing_explicit_human_authority")
    else:
        reasons.extend(reason for reason in policy_reasons if reason != "execution_policy.codex_exec_enabled:false")

    effective_notification_policy = notification_policy
    if effective_notification_policy is None and mode in {"dry_run_preview", "fake_runner_helper"}:
        effective_notification_policy = LOCAL_NOTIFICATION_POLICY
    notification_reason = _notification_policy_reason(mode, effective_notification_policy)
    if notification_reason:
        reasons.append(notification_reason)
    reasons.extend(_credential_reasons(credential_like_values))

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
        reasons.extend(_command_shape_reasons(plan))
        reasons.extend(_prompt_source_reasons(plan))
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

    if not repo_status_result["provided"] and mode != "dry_run_preview":
        reasons.append("repo_status:not_provided")
    if repo_status_result["tracked_dirty"]:
        reasons.append("repo_status:tracked_dirty")
    if repo_status_result["staged"]:
        reasons.append("repo_status:staged_files_present")
    if repo_status_result["unknown_untracked"]:
        reasons.append("repo_status:unknown_untracked_files")

    allowed = not reasons
    safe_to_start_real_runner = allowed and mode == "real_runner"
    return {
        "allowed": allowed,
        "mode": mode,
        "reasons": reasons,
        "safe_to_start_real_runner": safe_to_start_real_runner,
        "codex_execution_started": False,
        "real_subprocess_started": False,
        "execution_enabled": execution_enabled,
        "worker": worker,
        "prompt_path": prompt_path,
        "schema_path": schema_path,
        "report_path": report_path,
        "inspected_paths": _preflight_inspected_paths(plan),
        "authority_summary": {
            "execution_policy_enabled": execution_enabled,
            "human_real_execution_authority": human_real_execution_authority,
            "notification_policy": effective_notification_policy or "ambiguous",
            "environment_policy": environment_policy,
        },
        "max_steps": max_steps,
        "timeout_seconds": timeout_seconds,
        "repo_status": repo_status_result,
        "plan_error": plan_error,
    }


def _fake_report_payload(worker: str, scenario: str) -> dict[str, Any]:
    status = "pass"
    summary = f"fake runner {scenario} report"
    human_question = ""
    if scenario == "needs_human":
        status = "needs_human"
        human_question = "Fake runner needs human review."
    elif scenario == "blocked":
        status = "blocked"
        human_question = "Fake runner blocked the worker."

    return {
        "status": status,
        "lane": worker,
        "severity": "none",
        "summary": summary,
        "changed_files": [".agent/state.json"],
        "tests_run": ["fake runner synthetic report"],
        "tests_status": "passed",
        "risks": [],
        "next_recommended_worker": "summarize",
        "human_question": human_question,
        "copyable_next_prompt": "",
    }


def _write_fake_report(report_path: Path, payload: dict[str, Any]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _fail_closed_gate_result(report_path: str, reason: str) -> dict[str, Any]:
    return {
        "decision": "needs_human",
        "needs_human": True,
        "reasons": [reason],
        "report_path": report_path,
        "schema_path": "",
        "lane": "",
        "status": "",
        "severity": "",
        "tests_status": "",
        "summary": "",
        "next_recommended_worker": "",
        "human_question": "",
        "copyable_next_prompt": "",
    }


def run_fake_runner(
    plan: ExecutionPlan,
    scenario: str,
    state_path: str | Path = DEFAULT_STATE_PATH,
) -> FakeRunnerResult:
    if scenario not in {"pass", "needs_human", "blocked", "invalid_json", "missing_report", "nonzero_exit", "timeout"}:
        raise GateInputError(f"invalid fake runner scenario: {scenario}")

    report_path = resolve_repo_path(plan.report_path)
    artifacts_written: list[str] = []
    report_written = False
    exit_code: int | None = 0
    timed_out = False
    stdout = ""
    stderr = ""
    error_kind = ""
    gate_result: dict[str, Any] | None = None
    notify_stub: dict[str, Any] | None = None

    if scenario in {"pass", "needs_human", "blocked"}:
        _write_fake_report(report_path, _fake_report_payload(plan.worker, scenario))
        report_written = True
        artifacts_written.append(plan.report_path)
        gate_result = evaluate_report(report_path, state_path)
        if gate_result["needs_human"]:
            notify_stub = write_notification(report_path, gate_result, state_path)
            artifacts_written.extend(
                [notify_stub["needs_human_path"], notify_stub["notify_stub_log"]]
            )
    elif scenario == "invalid_json":
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write("{ invalid json\n")
        report_written = True
        artifacts_written.append(plan.report_path)
        error_kind = "invalid_json"
        stderr = "fake runner wrote invalid JSON"
        try:
            gate_result = evaluate_report(report_path, state_path)
        except json.JSONDecodeError as exc:
            gate_result = _fail_closed_gate_result(plan.report_path, f"invalid_json:{exc.msg}")
    elif scenario == "missing_report":
        error_kind = "missing_report"
        stderr = "fake runner did not write a report"
        gate_result = _fail_closed_gate_result(plan.report_path, "missing_report")
    elif scenario == "nonzero_exit":
        exit_code = 2
        error_kind = "nonzero_exit"
        stderr = "fake runner simulated nonzero exit"
        gate_result = _fail_closed_gate_result(plan.report_path, "nonzero_exit")
    elif scenario == "timeout":
        exit_code = None
        timed_out = True
        error_kind = "timeout"
        stderr = "fake runner simulated timeout"
        gate_result = _fail_closed_gate_result(plan.report_path, "timeout")

    fail_closed = bool(gate_result and gate_result.get("needs_human") is True)
    return FakeRunnerResult(
        mode="fake",
        scenario=scenario,
        worker=plan.worker,
        plan=plan.to_dict(),
        exit_code=exit_code,
        timed_out=timed_out,
        report_path=plan.report_path,
        report_written=report_written,
        stdout=stdout,
        stderr=stderr,
        error_kind=error_kind,
        codex_execution_started=False,
        real_subprocess_started=False,
        artifacts_written=artifacts_written,
        fail_closed=fail_closed,
        gate_result=gate_result,
        notify_stub=notify_stub,
    )


def run_single_fake_execution_flow_for_test(
    state: dict[str, Any],
    worker: str,
    scenario: str,
    *,
    repo_status: dict[str, Any],
    state_path: str | Path = DEFAULT_STATE_PATH,
    plan: ExecutionPlan | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    if plan is None:
        try:
            plan = build_execution_plan(state, worker, timestamp)
        except GateInputError:
            plan = None

    preflight = build_execution_preflight(
        state,
        worker,
        plan,
        repo_status=repo_status,
        mode="fake_runner_helper",
    )
    result: dict[str, Any] = {
        "mode": "single_fake_execution_flow_for_test",
        "scenario": scenario,
        "worker": worker,
        "preflight": preflight,
        "runner_started": False,
        "runner_result": None,
        "codex_execution_started": False,
        "real_subprocess_started": False,
    }

    if not preflight["allowed"]:
        result["status"] = "preflight_blocked"
        return result

    if plan is None:
        raise GateInputError("preflight unexpectedly allowed without an execution plan")

    runner_result = run_fake_runner(plan, scenario, state_path).to_dict()
    result.update(
        {
            "status": "completed",
            "runner_started": True,
            "runner_result": runner_result,
            "codex_execution_started": runner_result["codex_execution_started"],
            "real_subprocess_started": runner_result["real_subprocess_started"],
        }
    )
    return result


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
        execution_plan["preflight"] = build_execution_preflight(
            state,
            args.worker,
            execution_plan_obj,
            mode="dry_run_preview",
        )
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
