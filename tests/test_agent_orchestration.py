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
    assert result["dry_run"]["command"][:2] == ["codex", "exec"]
    assert "gate_result" not in result
