#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent

EXAMPLE_SINGLE_FAKE_FLOW: dict[str, Any] = {
    "card_mode": "example",
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
            "human_question": (
                "Review the example report shape and decide whether the next real "
                "worker result should be summarized, fixed, or held for more human input."
            ),
            "copyable_next_prompt": "",
        },
        "notify_stub": {
            "needs_human_path": ".agent/needs_human.json",
            "notify_stub_log": ".agent/logs/notify_stub.log",
            "payload": {"notification_sent": False},
        },
    },
}


EXAMPLE_PREFLIGHT_RESULT: dict[str, Any] = {
    "allowed": False,
    "mode": "real_runner",
    "worker": "audit",
    "reasons": [
        "execution_policy.codex_exec_enabled:false",
        "missing_explicit_human_authority",
    ],
    "safe_to_start_real_runner": False,
    "codex_execution_started": False,
    "real_subprocess_started": False,
    "report_path": ".agent/reports/example-audit.report.json",
    "inspected_paths": [
        ".agent/prompt_catalog/audit.md",
        ".agent/schemas/worker_report.schema.json",
        ".agent/reports/example-audit.report.json",
    ],
    "authority_summary": {
        "execution_policy_enabled": False,
        "human_real_execution_authority": False,
        "notification_policy": "ambiguous",
        "environment_policy": "not_inspected",
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


def _has_credential_marker(value: str) -> bool:
    token_markers = (
        "s" + "k-",
        "g" + "hp_",
        "github" + "_pat_",
        "A" + "KIA",
        "xox" + "b-",
        "xox" + "p-",
        "xox" + "a-",
        "xox" + "r-",
        "AI" + "za",
    )
    return any(marker in value for marker in token_markers)


def _safe_text(value: Any, fallback: str = "unknown") -> str:
    text = _text(value, fallback)
    if _has_credential_marker(text):
        return "[redacted credential-like value]"
    return text


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


def _safe_bullet_list(values: list[str], *, fallback: str) -> list[str]:
    if not values:
        return [f"- {fallback}"]
    return [f"- {_safe_text(value)}" for value in values]


def _card_mode(flow_result: dict[str, Any]) -> str:
    return "example" if flow_result.get("card_mode") == "example" else "real result"


def _worker_label(worker: Any) -> str:
    labels = {
        "advance": "Advance worker",
        "audit": "Audit worker",
        "fix": "Fix worker",
        "summarize": "Summarize worker",
        "escalate": "Escalation lane",
    }
    text = _text(worker)
    return labels.get(text, text)


def _scenario_label(scenario: Any) -> str:
    labels = {
        "pass": "No human stop",
        "needs_human": "Needs human review",
        "blocked": "Blocked",
        "invalid_json": "Invalid report JSON",
        "missing_report": "Missing report",
        "nonzero_exit": "Runner returned an error",
        "timeout": "Timed out",
    }
    text = _text(scenario)
    return labels.get(text, text)


def _flow_label(mode: Any) -> str:
    labels = {
        "single_fake_execution_flow_for_test": "Review an existing local simulation result",
    }
    text = _text(mode)
    return labels.get(text, text)


def _gate_label(decision: str) -> str:
    labels = {
        "needs_human": "needs human review",
        "pass": "passed",
        "blocked": "blocked",
        "not_run": "not run",
    }
    return labels.get(decision, decision)


def _plain_result(
    worker: Any,
    preflight: dict[str, Any],
    runner_started: bool,
    gate: dict[str, Any],
    runner: dict[str, Any],
    gate_decision: str,
) -> str:
    worker_label = _worker_label(worker)
    if preflight.get("allowed") is False:
        return f"{worker_label} stopped at preflight before any runner output."
    if gate.get("needs_human") is True:
        return f"{worker_label} reached a human-review stop."
    if runner.get("error_kind"):
        return f"{worker_label} produced an abnormal runner result."
    if runner_started and gate:
        return f"{worker_label} completed with gate result: {_gate_label(gate_decision)}."
    return f"{worker_label} has no complete gate result to review."


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
        return "Human action required: yes. Decide whether to fix the preflight reason before trying again."
    if gate.get("needs_human") is True:
        return (
            "Human action required: yes. Decide whether to continue with the suggested next worker, "
            "send the result back for a fix, or keep the run stopped for more human input."
        )
    if runner.get("fail_closed") is True:
        return "Human action required: yes. Decide how to handle the abnormal runner result before continuing."
    if runner_started and gate:
        return "Human action required: no immediate gate-required action."
    return "Human action required: unknown; no gate result is present."


def _decision_to_make(preflight: dict[str, Any], gate: dict[str, Any], runner: dict[str, Any]) -> str:
    if preflight.get("allowed") is False:
        return "Fix or intentionally leave the preflight block; do not proceed until it is understood."
    if gate.get("needs_human") is True:
        next_worker = _text(gate.get("next_recommended_worker"), "the next worker")
        return f"Inspect the listed artifacts, then choose whether to run {next_worker}, request a fix, or stop."
    if runner.get("error_kind"):
        return "Inspect the runner error and choose a fix or audit path before any continuation."
    if gate:
        next_worker = _text(gate.get("next_recommended_worker"), "the next worker")
        return f"No required stop is shown; the safe continuation is {next_worker} after optional review."
    return "No decision can be made from this card alone because gate data is missing."


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
            "Open the listed report and local needs-human artifacts if this is a real result.",
            "Choose whether to continue with the suggested worker, request a fix, or keep the run stopped.",
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
    card_mode = _card_mode(flow_result)
    is_example = card_mode == "example"
    human_action = _human_action_required(preflight, runner_started, gate, runner)
    codex_started = flow_result.get("codex_execution_started") is True or runner.get("codex_execution_started") is True
    real_process_started = (
        flow_result.get("real_subprocess_started") is True or runner.get("real_subprocess_started") is True
    )
    file_note = (
        "Example paths only; this example command does not check whether these files exist."
        if is_example
        else "Paths reported by the flow result; open them before making the decision."
    )

    summary_lines = [
        f"- Card mode: {card_mode}",
        f"- Plain-language result: {_plain_result(flow_result.get('worker'), preflight, runner_started, gate, runner, gate_decision)}",
        f"- Human action required: {human_action}",
        f"- Decision to make: {_decision_to_make(preflight, gate, runner)}",
    ]
    if is_example:
        summary_lines.append("- This is a deterministic sample card; it did not run or verify any worker artifacts.")

    raw_lines = [
        f"- mode: {_text(flow_result.get('mode'))}",
        f"- worker: {_text(flow_result.get('worker'))}",
        f"- scenario: {_text(flow_result.get('scenario'))}",
        f"- preflight_allowed: {_text(preflight.get('allowed'))}",
        f"- runner_started: {_yes_no(runner_started)}",
        f"- gate_decision: {gate_decision}",
        f"- report_path: {_text(runner.get('report_path'), _text(preflight.get('report_path')))}",
    ]
    abnormal_runner = bool(runner.get("error_kind")) or runner.get("timed_out") is True or runner.get("exit_code") not in (0, None)
    if preflight.get("allowed") is False or abnormal_runner:
        raw_lines.append(f"- fail_closed: {_yes_no(runner.get('fail_closed'))}")

    lines: list[str] = [
        "# NLMYTGen Operator Review Card",
        "",
        "## Summary",
        *summary_lines,
        "",
        "## Status",
        f"- Flow status: {_text(flow_result.get('status'))}",
        f"- Preflight check: {preflight_state}",
        f"- Local simulation runner started: {_yes_no(runner_started)}",
        f"- Gate result: {_gate_label(gate_decision)}",
        f"- Human action required: {human_action}",
        "",
        "## What happened",
        f"- Attempted work: {_flow_label(flow_result.get('mode'))}",
        f"- Worker / scenario: {_worker_label(flow_result.get('worker'))} / {_scenario_label(flow_result.get('scenario'))}",
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
        f"- Decision to make: {_decision_to_make(preflight, gate, runner)}",
        f"- Report note: {_text(gate.get('human_question'), 'none')}",
        "- Gate reasons:",
        *_bullet_list(gate_reasons, fallback="none"),
        "- Preflight reasons:",
        *_bullet_list(preflight_reasons, fallback="none"),
        "",
        "## Files to inspect",
        f"- Note: {file_note}",
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
        *raw_lines,
    ]
    return "\n".join(lines) + "\n"


def _preflight_state(preflight: dict[str, Any]) -> str:
    allowed = preflight.get("allowed")
    if allowed is True:
        return "allowed"
    if allowed is False:
        return "blocked"
    return "unknown"


def _preflight_paths(preflight: dict[str, Any]) -> list[str]:
    paths = _as_strings(preflight.get("inspected_paths"))
    for key in ("prompt_path", "schema_path", "report_path"):
        value = preflight.get(key)
        if isinstance(value, str):
            paths.append(value)
    return _unique_preserve_order(paths)


def _authority_summary_lines(preflight: dict[str, Any]) -> list[str]:
    authority = _as_dict(preflight.get("authority_summary"))
    if not authority:
        return ["- none"]
    preferred_order = [
        "execution_policy_enabled",
        "human_real_execution_authority",
        "notification_policy",
        "environment_policy",
    ]
    keys = [key for key in preferred_order if key in authority]
    keys.extend(sorted(key for key in authority if key not in keys))
    return [f"- {key}: {_safe_text(authority.get(key))}" for key in keys]


def _preflight_next_actions(preflight: dict[str, Any]) -> list[str]:
    if preflight.get("allowed") is False:
        return [
            "Compare the listed reasons against authority, path, and repo-state inputs before rerunning preflight.",
            "Keep this as a preview card; do not infer execution authority from the card.",
        ]
    if preflight.get("safe_to_start_real_runner") is True:
        return [
            "Verify the authority summary, inspected paths, and clean execution boundary before a separate runner step.",
            "Treat this as start permission only for a separately authorized real-runner slice.",
        ]
    if preflight.get("allowed") is True:
        return [
            "Use this as a read-only preview; dry-run and fake-helper allows still cannot start a real runner.",
            "Inspect the paths and authority summary before deciding the next adapter or review step.",
        ]
    return [
        "Regenerate the preflight result with complete mode, worker, authority, path, and safety fields.",
        "Do not start any runner from an unknown preflight state.",
    ]


def render_preflight_preview_card(preflight_result: dict[str, Any]) -> str:
    """Render a read-only Markdown preview card from a raw preflight result."""
    if not isinstance(preflight_result, dict):
        raise TypeError("preflight_result must be a dict")

    state = _preflight_state(preflight_result)
    reasons = _as_strings(preflight_result.get("reasons"))
    inspected_paths = _preflight_paths(preflight_result)
    codex_started = preflight_result.get("codex_execution_started") is True
    real_process_started = preflight_result.get("real_subprocess_started") is True
    safe_to_start = preflight_result.get("safe_to_start_real_runner")
    human_action = "yes" if preflight_result.get("allowed") is False else "review"
    if safe_to_start is True:
        human_next_action = "Confirm explicit authority and hand this to a separate real-runner slice only if that slice is authorized."
    elif preflight_result.get("allowed") is True:
        human_next_action = "Inspect the preview and keep real runner start disabled for this card."
    else:
        human_next_action = "Fix or intentionally hold the listed block reasons before any runner step."

    lines: list[str] = [
        "# NLMYTGen Preflight Preview Card",
        "",
        "## Summary",
        f"- Preflight status: {state}",
        f"- Mode / worker: {_safe_text(preflight_result.get('mode'))} / {_safe_text(preflight_result.get('worker'))}",
        f"- Allowed: {_yes_no(preflight_result.get('allowed'))}",
        f"- Safe to start real runner: {_yes_no(safe_to_start)}",
        f"- Human action required: {human_action}",
        "- This card is read-only; it did not start a runner or validate a worker report.",
        "",
        "## Reasons",
        *_safe_bullet_list(reasons, fallback="none"),
        "",
        "## Files / Paths Inspected",
        *_safe_bullet_list(inspected_paths, fallback="No inspected paths were reported."),
        "",
        "## Authority Summary",
        *_authority_summary_lines(preflight_result),
        "",
        "## Execution Boundary",
        f"- Real Codex execution: {'started' if codex_started else 'not started'}",
        f"- Real subprocess runner: {'started' if real_process_started else 'not started'}",
        "- Codex stdin piping: not implemented",
        "- Runtime worker loop: not implemented",
        "- External notification service: not implemented",
        "- Runtime artifacts: not written by preflight preview",
        "",
        "## Human Next Action",
        f"- {human_next_action}",
        *_safe_bullet_list(_preflight_next_actions(preflight_result), fallback="none"),
        "",
        "## Raw Identifiers",
        f"- mode: {_safe_text(preflight_result.get('mode'))}",
        f"- worker: {_safe_text(preflight_result.get('worker'))}",
        f"- preflight_allowed: {_yes_no(preflight_result.get('allowed'))}",
        f"- safe_to_start_real_runner: {_yes_no(safe_to_start)}",
        f"- report_path: {_safe_text(preflight_result.get('report_path'))}",
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
    parser.add_argument("--preflight-example", action="store_true", help="Print a deterministic preflight preview card.")
    args = parser.parse_args(argv)

    try:
        selected_inputs = sum(1 for selected in (args.example, args.preflight_example, bool(args.flow_result)) if selected)
        if selected_inputs != 1:
            parser.error("provide one of flow_result, --example, or --preflight-example")

        if args.preflight_example:
            print(render_preflight_preview_card(EXAMPLE_PREFLIGHT_RESULT), end="")
            return 0
        if args.example:
            payload = EXAMPLE_SINGLE_FAKE_FLOW
        else:
            payload = _load_json(Path(args.flow_result))

        print(render_operator_review_card(payload), end="")
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
