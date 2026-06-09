#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent

EXAMPLE_SINGLE_FAKE_FLOW: dict[str, Any] = {
    "mode": "single_fake_execution_flow_for_test",
    "scenario": "needs_human",
    "worker": "audit",
    "status": "completed",
    "preflight": {
        "allowed": True,
        "reasons": [],
        "worker": "audit",
        "prompt_path": ".agent/prompt_catalog/audit.md",
        "schema_path": ".agent/schemas/worker_report.schema.json",
        "report_path": ".agent/reports/example-audit.report.json",
        "max_steps": 1,
        "timeout_seconds": 600,
    },
    "runner_started": True,
    "codex_execution_started": False,
    "real_subprocess_started": False,
    "runner_result": {
        "mode": "fake",
        "scenario": "needs_human",
        "worker": "audit",
        "exit_code": 0,
        "timed_out": False,
        "report_path": ".agent/reports/example-audit.report.json",
        "report_written": True,
        "stdout": "",
        "stderr": "",
        "error_kind": "",
        "codex_execution_started": False,
        "real_subprocess_started": False,
        "artifacts_written": [
            ".agent/reports/example-audit.report.json",
            ".agent/needs_human.json",
            ".agent/logs/notify_stub.log",
        ],
        "fail_closed": True,
        "gate_result": {
            "decision": "needs_human",
            "needs_human": True,
            "reasons": ["status:needs_human"],
            "report_path": ".agent/reports/example-audit.report.json",
            "schema_path": ".agent/schemas/worker_report.schema.json",
            "lane": "audit",
            "status": "needs_human",
            "severity": "none",
            "tests_status": "passed",
            "summary": "fake runner needs_human report",
            "next_recommended_worker": "summarize",
            "human_question": "Fake runner needs human review.",
            "copyable_next_prompt": "",
        },
        "notify_stub": {
            "needs_human_path": ".agent/needs_human.json",
            "notify_stub_log": ".agent/logs/notify_stub.log",
            "payload": {"notification_sent": False},
        },
    },
}


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _text(value: Any, fallback: str = "unknown") -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback


def _yes_no(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "unknown"


def _bullet_list(values: list[str], *, fallback: str) -> list[str]:
    if not values:
        return [f"- {fallback}"]
    return [f"- {value}" for value in values]


def _unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _collect_files(preflight: dict[str, Any], runner: dict[str, Any], gate: dict[str, Any], notify: dict[str, Any]) -> list[str]:
    files: list[str] = []
    for key in ("prompt_path", "schema_path", "report_path"):
        value = preflight.get(key)
        if isinstance(value, str):
            files.append(value)
    for key in ("report_path",):
        value = runner.get(key)
        if isinstance(value, str):
            files.append(value)
    for value in _as_strings(runner.get("artifacts_written")):
        files.append(value)
    for key in ("report_path", "schema_path"):
        value = gate.get(key)
        if isinstance(value, str):
            files.append(value)
    for key in ("needs_human_path", "notify_stub_log"):
        value = notify.get(key)
        if isinstance(value, str):
            files.append(value)
    return _unique_preserve_order(files)


def _human_decision_line(
    preflight: dict[str, Any],
    runner_started: bool,
    gate: dict[str, Any],
    runner: dict[str, Any],
) -> str:
    if preflight.get("allowed") is False:
        return "Human action required: yes, because preflight blocked the worker before any runner output."
    if gate.get("needs_human") is True:
        return "Human action required: yes, because the gate decision is needs_human."
    if runner.get("fail_closed") is True:
        return "Human action required: yes, because the flow failed closed."
    if runner_started and gate:
        return "Human action required: no immediate gate-required action."
    return "Human action required: unknown; no gate result is present."


def _human_action_required(preflight: dict[str, Any], runner_started: bool, gate: dict[str, Any], runner: dict[str, Any]) -> str:
    if preflight.get("allowed") is False:
        return "yes"
    if gate.get("needs_human") is True:
        return "yes"
    if gate.get("needs_human") is False:
        return "no"
    if runner.get("fail_closed") is True:
        return "yes"
    if runner_started and gate:
        return "no"
    return "unknown"


def _next_actions(preflight: dict[str, Any], runner_started: bool, runner: dict[str, Any], gate: dict[str, Any]) -> list[str]:
    if preflight.get("allowed") is False:
        return [
            "Resolve the listed preflight reason before any worker run is considered.",
            "Rerun a dry preflight or render a fresh operator card from the next flow result.",
            "Keep real Codex execution disabled unless a separate boundary-design slice authorizes it.",
        ]
    if gate.get("needs_human") is True:
        return [
            "Open the report and needs-human stub paths listed above.",
            "Answer the human question or choose the next worker after inspecting the gate reasons.",
            "Treat this as a local review stop, not a production or release approval.",
        ]
    if runner.get("error_kind"):
        return [
            "Inspect the runner error kind and report path.",
            "Use a fix or audit worker only after the fail-closed cause is understood.",
        ]
    if runner_started and gate:
        next_worker = _text(gate.get("next_recommended_worker"), "summarize")
        return [
            "Optionally inspect the report path listed above.",
            f"Continue with the gate-recommended worker: {next_worker}.",
            "Move toward real-runner boundary design only after the operator surface is accepted.",
        ]
    return [
        "Render a card from a complete flow result with preflight and gate data.",
        "Do not infer pass/fail from missing runner data.",
    ]


def render_operator_review_card(flow_result: dict[str, Any]) -> str:
    """Render an operator-facing Markdown card from an existing orchestration result."""
    if not isinstance(flow_result, dict):
        raise TypeError("flow_result must be a dict")

    preflight = _as_dict(flow_result.get("preflight"))
    runner = _as_dict(flow_result.get("runner_result"))
    gate = _as_dict(runner.get("gate_result"))
    notify = _as_dict(runner.get("notify_stub"))
    runner_started = flow_result.get("runner_started") is True
    files = _collect_files(preflight, runner, gate, notify)
    preflight_allowed = preflight.get("allowed")
    preflight_state = "passed" if preflight_allowed is True else "blocked" if preflight_allowed is False else "unknown"
    gate_decision = _text(gate.get("decision"), "not_run")
    gate_reasons = _as_strings(gate.get("reasons"))
    preflight_reasons = _as_strings(preflight.get("reasons"))
    runner_report_written = runner.get("report_written") if runner_started else False
    codex_started = flow_result.get("codex_execution_started") is True or runner.get("codex_execution_started") is True
    real_process_started = (
        flow_result.get("real_subprocess_started") is True or runner.get("real_subprocess_started") is True
    )

    lines: list[str] = [
        "# NLMYTGen Operator Review Card",
        "",
        "## Status",
        f"- Flow status: {_text(flow_result.get('status'))}",
        f"- Preflight: {preflight_state}",
        f"- Runner started: {_yes_no(runner_started)}",
        f"- Gate decision: {gate_decision}",
        f"- Human action required: {_human_action_required(preflight, runner_started, gate, runner)}",
        "",
        "## What happened",
        f"- Attempted flow: {_text(flow_result.get('mode'))}",
        f"- Worker / scenario: {_text(flow_result.get('worker'))} / {_text(flow_result.get('scenario'))}",
        f"- Prompt: {_text(preflight.get('prompt_path'))}",
        f"- Schema: {_text(preflight.get('schema_path'))}",
        f"- Planned report: {_text(preflight.get('report_path'))}",
        f"- Runner report written: {_yes_no(runner_report_written)}",
        f"- Runner exit: {_text(runner.get('exit_code'), 'not_run')}",
        f"- Runner timed out: {_yes_no(runner.get('timed_out'))}",
        f"- Runner error kind: {_text(runner.get('error_kind'), 'none')}",
        "",
        "## Human decision needed",
        f"- {_human_decision_line(preflight, runner_started, gate, runner)}",
        f"- Human question: {_text(gate.get('human_question'), 'none')}",
        "- Gate reasons:",
        *_bullet_list(gate_reasons, fallback="none"),
        "- Preflight reasons:",
        *_bullet_list(preflight_reasons, fallback="none"),
        "",
        "## Files to inspect",
        *_bullet_list(files, fallback="No inspectable files were reported."),
        "",
        "## Safety boundary",
        f"- Real Codex execution: {'started' if codex_started else 'not started'}",
        f"- Real subprocess runner: {'started' if real_process_started else 'not started'}",
        "- Codex stdin piping: not implemented",
        "- Runtime worker loop: not implemented",
        "- External notification service: not implemented",
        "- Local notify stub: only written after gate_result.needs_human=true",
        "",
        "## Next safe actions",
        *_bullet_list(_next_actions(preflight, runner_started, runner, gate), fallback="none"),
        "",
        "## Raw identifiers",
        f"- mode: {_text(flow_result.get('mode'))}",
        f"- worker: {_text(flow_result.get('worker'))}",
        f"- scenario: {_text(flow_result.get('scenario'))}",
        f"- preflight_allowed: {_text(preflight.get('allowed'))}",
        f"- runner_started: {_yes_no(runner_started)}",
        f"- gate_decision: {gate_decision}",
        f"- fail_closed: {_yes_no(runner.get('fail_closed'))}",
        f"- report_path: {_text(runner.get('report_path'), _text(preflight.get('report_path')))}",
    ]
    return "\n".join(lines) + "\n"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_absolute():
        path = REPO_ROOT / path
    resolved = path.resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError(f"flow_result must stay inside this repo: {path}") from exc
    if not resolved.exists():
        raise ValueError(f"flow_result does not exist: {path}")

    with open(resolved, encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {resolved}")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a read-only operator review card from an existing orchestration flow JSON."
    )
    parser.add_argument("flow_result", nargs="?", help="Path to an existing flow result JSON.")
    parser.add_argument("--example", action="store_true", help="Print a deterministic example card.")
    args = parser.parse_args(argv)

    try:
        if args.example:
            payload = EXAMPLE_SINGLE_FAKE_FLOW
        elif args.flow_result:
            payload = _load_json(Path(args.flow_result))
        else:
            parser.error("provide a flow_result JSON path or use --example")

        print(render_operator_review_card(payload), end="")
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
