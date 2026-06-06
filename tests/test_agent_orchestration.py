from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import agent_gate  # noqa: E402
import agent_notify_stub  # noqa: E402
import agent_orchestrator  # noqa: E402

TMP_AGENT_DIR = REPO_ROOT / ".agent" / "reports" / "_tmp_pytest_agent_orchestration"


BASE_REPORT: dict[str, Any] = {
    "status": "pass",
    "lane": "audit",
    "severity": "none",
    "summary": "test report",
    "changed_files": [".agent/state.json"],
    "tests_run": ["pytest tests/test_agent_orchestration.py"],
    "tests_status": "passed",
    "risks": [],
    "next_recommended_worker": "summarize",
    "human_question": "",
    "copyable_next_prompt": "",
}


@pytest.fixture()
def repo_agent_tmp() -> Path:
    if TMP_AGENT_DIR.exists():
        shutil.rmtree(TMP_AGENT_DIR)
    TMP_AGENT_DIR.mkdir(parents=True)
    try:
        yield TMP_AGENT_DIR
    finally:
        shutil.rmtree(TMP_AGENT_DIR, ignore_errors=True)


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def _report(
    tmp_dir: Path,
    name: str,
    *,
    overrides: dict[str, Any] | None = None,
    remove: tuple[str, ...] = (),
) -> Path:
    payload = dict(BASE_REPORT)
    if overrides:
        payload.update(overrides)
    for key in remove:
        payload.pop(key, None)
    return _write_json(tmp_dir / f"{name}.json", payload)


def _evaluate(report_path: Path) -> dict[str, Any]:
    return agent_gate.evaluate_report(report_path, ".agent/state.json")


def _load_state() -> dict[str, Any]:
    with open(REPO_ROOT / ".agent" / "state.json", encoding="utf-8") as handle:
        return json.load(handle)


def _execution_enabled_state() -> dict[str, Any]:
    state = _load_state()
    state["execution_policy"] = {
        "codex_exec_enabled": True,
        "max_steps": 1,
        "timeout_seconds": 600,
    }
    return state


def _clean_repo_status() -> dict[str, Any]:
    return {
        "tracked_dirty": [],
        "staged": [],
        "untracked": [],
        "allowed_untracked": [],
    }


def test_gate_valid_pass_report_allows_continuation(repo_agent_tmp: Path) -> None:
    result = _evaluate(_report(repo_agent_tmp, "pass"))

    assert result["decision"] == "pass"
    assert result["needs_human"] is False
    assert result["reasons"] == []


def test_gate_missing_required_field_escalates(repo_agent_tmp: Path) -> None:
    result = _evaluate(_report(repo_agent_tmp, "missing_required", remove=("tests_run",)))

    assert result["needs_human"] is True
    assert any("missing required field: tests_run" in reason for reason in result["reasons"])


def test_gate_invalid_enum_value_escalates(repo_agent_tmp: Path) -> None:
    result = _evaluate(_report(repo_agent_tmp, "invalid_enum", overrides={"status": "done"}))

    assert result["needs_human"] is True
    assert any("status must be one of" in reason for reason in result["reasons"])


def test_gate_changed_files_wrong_type_escalates(repo_agent_tmp: Path) -> None:
    result = _evaluate(_report(repo_agent_tmp, "changed_files_wrong_type", overrides={"changed_files": ".agent/state.json"}))

    assert result["needs_human"] is True
    assert any("changed_files must be array" in reason for reason in result["reasons"])


@pytest.mark.parametrize("severity", ["P1", "P0"])
def test_gate_high_severity_escalates(repo_agent_tmp: Path, severity: str) -> None:
    result = _evaluate(_report(repo_agent_tmp, f"severity_{severity}", overrides={"severity": severity}))

    assert result["needs_human"] is True
    assert f"severity:{severity}" in result["reasons"]


def test_gate_failed_tests_escalate(repo_agent_tmp: Path) -> None:
    result = _evaluate(_report(repo_agent_tmp, "tests_failed", overrides={"tests_status": "failed"}))

    assert result["needs_human"] is True
    assert "tests_status:failed" in result["reasons"]


@pytest.mark.parametrize(
    "risk_keyword",
    ["format_contract_violation", "completion_report_not_single_code_block"],
)
def test_gate_format_contract_risks_escalate(repo_agent_tmp: Path, risk_keyword: str) -> None:
    result = _evaluate(_report(repo_agent_tmp, risk_keyword, overrides={"risks": [risk_keyword]}))

    assert result["needs_human"] is True
    assert f"risk_keyword:{risk_keyword}" in result["reasons"]


def test_gate_blocked_production_path_escalates(repo_agent_tmp: Path) -> None:
    result = _evaluate(
        _report(
            repo_agent_tmp,
            "blocked_path",
            overrides={"changed_files": ["samples/production.ymmp"]},
        )
    )

    assert result["needs_human"] is True
    assert any("changed_file_blocked_pattern" in reason for reason in result["reasons"])


def test_gate_repo_external_traversal_escalates(repo_agent_tmp: Path) -> None:
    result = _evaluate(
        _report(
            repo_agent_tmp,
            "external_traversal",
            overrides={"changed_files": ["../outside.txt"]},
        )
    )

    assert result["needs_human"] is True
    assert "changed_file_invalid_or_external:../outside.txt" in result["reasons"]


def test_gate_out_of_scope_changed_file_escalates(repo_agent_tmp: Path) -> None:
    result = _evaluate(
        _report(
            repo_agent_tmp,
            "out_of_scope",
            overrides={"changed_files": ["README.md"]},
        )
    )

    assert result["needs_human"] is True
    assert "changed_file_out_of_scope:README.md" in result["reasons"]


def _notify_state(tmp_dir: Path) -> Path:
    with open(REPO_ROOT / ".agent" / "state.json", encoding="utf-8") as handle:
        state = json.load(handle)
    state["needs_human_path"] = ".agent/reports/_tmp_pytest_agent_orchestration/needs_human.json"
    state["notify_stub_log"] = ".agent/reports/_tmp_pytest_agent_orchestration/notify_stub.log"
    return _write_json(tmp_dir / "state.notify.json", state)


def test_notify_stub_writes_only_local_stub_for_needs_human(repo_agent_tmp: Path) -> None:
    report_path = _report(repo_agent_tmp, "notify_report", overrides={"status": "needs_human"})
    state_path = _notify_state(repo_agent_tmp)
    gate_result = {"decision": "needs_human", "needs_human": True, "reasons": ["status:needs_human"]}

    result = agent_notify_stub.write_notification(report_path, gate_result, state_path)

    needs_human_path = REPO_ROOT / result["needs_human_path"]
    notify_log_path = REPO_ROOT / result["notify_stub_log"]
    assert needs_human_path == repo_agent_tmp / "needs_human.json"
    assert notify_log_path == repo_agent_tmp / "notify_stub.log"
    assert needs_human_path.exists()
    assert notify_log_path.exists()
    with open(needs_human_path, encoding="utf-8") as handle:
        payload = json.load(handle)
    assert payload["notification_sent"] is False
    assert payload["gate_reasons"] == ["status:needs_human"]
    assert notify_log_path.read_text(encoding="utf-8").count("\n") == 1


def test_notify_stub_refuses_non_needs_human_without_artifacts(repo_agent_tmp: Path) -> None:
    report_path = _report(repo_agent_tmp, "notify_refused")
    state_path = _notify_state(repo_agent_tmp)
    gate_result = {"decision": "pass", "needs_human": False, "reasons": []}

    with pytest.raises(agent_notify_stub.NotifyInputError):
        agent_notify_stub.write_notification(report_path, gate_result, state_path)

    assert not (repo_agent_tmp / "needs_human.json").exists()
    assert not (repo_agent_tmp / "notify_stub.log").exists()


def test_execution_plan_builds_stdin_based_codex_exec_preview() -> None:
    plan = agent_orchestrator.build_execution_plan(_load_state(), "audit", timestamp="20260606T000000Z")
    payload = plan.to_dict()

    assert payload["worker"] == "audit"
    assert payload["cwd"] == str(REPO_ROOT)
    assert payload["prompt_path"] == ".agent/prompt_catalog/audit.md"
    assert payload["schema_path"] == ".agent/schemas/worker_report.schema.json"
    assert payload["report_path"] == ".agent/reports/20260606T000000Z-audit.report.json"
    assert payload["stdin_source"] == ".agent/prompt_catalog/audit.md"
    assert payload["prompt_input_mode"] == "stdin_from_prompt_file"
    assert payload["codex_execution_started"] is False
    assert payload["argv"] == [
        "codex",
        "exec",
        "-",
        "--output-schema",
        ".agent/schemas/worker_report.schema.json",
        "-o",
        ".agent/reports/20260606T000000Z-audit.report.json",
    ]
    assert "--prompt-file" not in payload["argv"]
    assert "--output" not in payload["argv"]


def test_execution_policy_defaults_are_inert() -> None:
    policy = agent_orchestrator.execution_policy_from_state(_load_state())

    assert policy["codex_exec_enabled"] is False
    assert policy["max_steps"] == 1
    assert policy["timeout_seconds"] == 600


def test_preflight_blocks_default_disabled_execution_policy() -> None:
    result = agent_orchestrator.build_execution_preflight(
        _load_state(),
        "audit",
        repo_status=_clean_repo_status(),
    )

    assert result["allowed"] is False
    assert result["execution_enabled"] is False
    assert "execution_policy.codex_exec_enabled:false" in result["reasons"]
    assert result["worker"] == "audit"
    assert result["prompt_path"] == ".agent/prompt_catalog/audit.md"
    assert result["schema_path"] == ".agent/schemas/worker_report.schema.json"
    assert result["report_path"].startswith(".agent/reports/")
    assert result["max_steps"] == 1
    assert result["timeout_seconds"] == 600
    assert result["repo_status"]["provided"] is True


def test_preflight_rejects_invalid_worker_name() -> None:
    result = agent_orchestrator.build_execution_preflight(
        _execution_enabled_state(),
        "../outside",
        repo_status=_clean_repo_status(),
    )

    assert result["allowed"] is False
    assert any("invalid worker" in reason for reason in result["reasons"])


def test_preflight_rejects_missing_prompt_file() -> None:
    state = _execution_enabled_state()
    state["prompt_catalog_dir"] = ".agent/prompt_catalog/missing"

    result = agent_orchestrator.build_execution_preflight(state, "audit", repo_status=_clean_repo_status())

    assert result["allowed"] is False
    assert any("path does not exist" in reason for reason in result["reasons"])


def test_preflight_rejects_missing_schema_file() -> None:
    state = _execution_enabled_state()
    state["worker_report_schema"] = ".agent/schemas/missing.schema.json"

    result = agent_orchestrator.build_execution_preflight(state, "audit", repo_status=_clean_repo_status())

    assert result["allowed"] is False
    assert any("path does not exist" in reason for reason in result["reasons"])


def test_preflight_rejects_prompt_outside_prompt_catalog(repo_agent_tmp: Path) -> None:
    outside_prompt_dir = repo_agent_tmp / "outside_prompt_catalog"
    outside_prompt_dir.mkdir(parents=True)
    (outside_prompt_dir / "audit.md").write_text("outside prompt\n", encoding="utf-8")
    state = _execution_enabled_state()
    state["prompt_catalog_dir"] = outside_prompt_dir.relative_to(REPO_ROOT).as_posix()

    result = agent_orchestrator.build_execution_preflight(state, "audit", repo_status=_clean_repo_status())

    assert result["allowed"] is False
    assert any("prompt_path must stay under .agent/prompt_catalog" in reason for reason in result["reasons"])


def test_preflight_rejects_schema_outside_schema_dir() -> None:
    state = _execution_enabled_state()
    state["worker_report_schema"] = "docs/AGENT_ORCHESTRATION.md"

    result = agent_orchestrator.build_execution_preflight(state, "audit", repo_status=_clean_repo_status())

    assert result["allowed"] is False
    assert any("schema_path must stay under .agent/schemas" in reason for reason in result["reasons"])


def test_preflight_rejects_report_path_outside_report_dir() -> None:
    state = _execution_enabled_state()
    state["report_output_template"] = "docs/{timestamp}-{worker}.report.json"

    result = agent_orchestrator.build_execution_preflight(state, "audit", repo_status=_clean_repo_status())

    assert result["allowed"] is False
    assert any("report_path must stay under .agent/reports" in reason for reason in result["reasons"])


def test_preflight_rejects_existing_report_output_path(repo_agent_tmp: Path) -> None:
    existing_report = repo_agent_tmp / "existing.report.json"
    existing_report.write_text("{}\n", encoding="utf-8")
    state = _execution_enabled_state()
    state["report_output_template"] = existing_report.relative_to(REPO_ROOT).as_posix()

    result = agent_orchestrator.build_execution_preflight(state, "audit", repo_status=_clean_repo_status())

    assert result["allowed"] is False
    assert f"report_path:already_exists:{existing_report.relative_to(REPO_ROOT).as_posix()}" in result["reasons"]


def test_preflight_rejects_max_steps_greater_than_one() -> None:
    state = _execution_enabled_state()
    state["execution_policy"]["max_steps"] = 2

    result = agent_orchestrator.build_execution_preflight(state, "audit", repo_status=_clean_repo_status())

    assert result["allowed"] is False
    assert "execution_policy.max_steps:greater_than_1" in result["reasons"]


@pytest.mark.parametrize("max_steps", [None, "1", True, 0])
def test_preflight_rejects_missing_invalid_boolean_or_low_max_steps(max_steps: Any) -> None:
    state = _execution_enabled_state()
    if max_steps is None:
        state["execution_policy"].pop("max_steps")
        expected_reason = "execution_policy.max_steps:missing"
    elif max_steps == 0:
        state["execution_policy"]["max_steps"] = max_steps
        expected_reason = "execution_policy.max_steps:less_than_1"
    else:
        state["execution_policy"]["max_steps"] = max_steps
        expected_reason = "execution_policy.max_steps:invalid"

    result = agent_orchestrator.build_execution_preflight(state, "audit", repo_status=_clean_repo_status())

    assert result["allowed"] is False
    assert expected_reason in result["reasons"]


@pytest.mark.parametrize("timeout_seconds", [None, "600", True, 0, -1])
def test_preflight_rejects_missing_invalid_boolean_or_non_positive_timeout(timeout_seconds: Any) -> None:
    state = _execution_enabled_state()
    if timeout_seconds is None:
        state["execution_policy"].pop("timeout_seconds")
        expected_reason = "execution_policy.timeout_seconds:missing"
    elif isinstance(timeout_seconds, int) and timeout_seconds <= 0:
        state["execution_policy"]["timeout_seconds"] = timeout_seconds
        expected_reason = "execution_policy.timeout_seconds:non_positive"
    else:
        state["execution_policy"]["timeout_seconds"] = timeout_seconds
        expected_reason = "execution_policy.timeout_seconds:invalid"

    result = agent_orchestrator.build_execution_preflight(state, "audit", repo_status=_clean_repo_status())

    assert result["allowed"] is False
    assert expected_reason in result["reasons"]


def test_preflight_rejects_staged_files() -> None:
    repo_status = _clean_repo_status()
    repo_status["staged"] = ["scripts/agent_orchestrator.py"]

    result = agent_orchestrator.build_execution_preflight(_execution_enabled_state(), "audit", repo_status=repo_status)

    assert result["allowed"] is False
    assert "repo_status:staged_files_present" in result["reasons"]


def test_preflight_rejects_dirty_tracked_state() -> None:
    repo_status = _clean_repo_status()
    repo_status["tracked_dirty"] = ["docs/AGENT_ORCHESTRATION.md"]

    result = agent_orchestrator.build_execution_preflight(_execution_enabled_state(), "audit", repo_status=repo_status)

    assert result["allowed"] is False
    assert "repo_status:tracked_dirty" in result["reasons"]


def test_preflight_allows_known_untracked_only_with_explicit_allowlist() -> None:
    repo_status = _clean_repo_status()
    repo_status["untracked"] = [".claude/worktrees/example/", "samples/2026-05-16.ymmp"]
    repo_status["allowed_untracked"] = [".claude/worktrees/", "samples/2026-05-16.ymmp"]

    result = agent_orchestrator.build_execution_preflight(_execution_enabled_state(), "audit", repo_status=repo_status)

    assert result["allowed"] is True
    assert result["repo_status"]["unknown_untracked"] == []


def test_preflight_rejects_unknown_untracked_files() -> None:
    repo_status = _clean_repo_status()
    repo_status["untracked"] = ["unexpected.tmp"]

    result = agent_orchestrator.build_execution_preflight(_execution_enabled_state(), "audit", repo_status=repo_status)

    assert result["allowed"] is False
    assert "repo_status:unknown_untracked_files" in result["reasons"]


def test_preflight_only_checks_do_not_write_notification_artifacts(repo_agent_tmp: Path) -> None:
    state = _execution_enabled_state()
    state["needs_human_path"] = (repo_agent_tmp / "needs_human.json").relative_to(REPO_ROOT).as_posix()
    state["notify_stub_log"] = (repo_agent_tmp / "notify_stub.log").relative_to(REPO_ROOT).as_posix()

    result = agent_orchestrator.build_execution_preflight(state, "audit", repo_status=_clean_repo_status())

    assert result["allowed"] is True
    assert not (repo_agent_tmp / "needs_human.json").exists()
    assert not (repo_agent_tmp / "notify_stub.log").exists()


def test_execution_plan_rejects_invalid_worker_name() -> None:
    with pytest.raises(agent_gate.GateInputError):
        agent_orchestrator.build_execution_plan(_load_state(), "../outside", timestamp="20260606T000000Z")


@pytest.mark.parametrize(
    "override",
    [
        {"prompt_catalog_dir": "../outside"},
        {"worker_report_schema": "../outside/schema.json"},
        {"report_output_template": "../outside/{timestamp}-{worker}.json"},
        {"prompt_catalog_dir": "docs"},
        {"worker_report_schema": "docs/AGENT_ORCHESTRATION.md"},
        {"report_output_template": "docs/{timestamp}-{worker}.report.json"},
    ],
)
def test_execution_plan_rejects_repo_external_or_out_of_contract_paths(override: dict[str, Any]) -> None:
    state = _load_state()
    state.update(override)

    with pytest.raises(agent_gate.GateInputError):
        agent_orchestrator.build_execution_plan(state, "audit", timestamp="20260606T000000Z")


def test_orchestrator_dry_run_does_not_start_codex() -> None:
    result = agent_orchestrator.run(
        argparse.Namespace(
            worker="audit",
            dry_run=True,
            report=None,
            state=".agent/state.json",
        )
    )

    assert result["dry_run"]["codex_execution_started"] is False
    assert result["dry_run"]["argv"][:3] == ["codex", "exec", "-"]
    assert result["dry_run"]["prompt_input_mode"] == "stdin_from_prompt_file"
    assert result["dry_run"]["preflight"]["allowed"] is False
    assert "execution_policy.codex_exec_enabled:false" in result["dry_run"]["preflight"]["reasons"]
    assert "gate_result" not in result


def test_orchestrator_without_dry_run_or_report_still_cannot_execute_codex() -> None:
    result = agent_orchestrator.run(
        argparse.Namespace(
            worker="audit",
            dry_run=False,
            report=None,
            state=".agent/state.json",
        )
    )

    assert result["codex_execution_started"] is False
    assert "No Codex execution is performed" in result["message"]
