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
import agent_operator_surface  # noqa: E402

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


def _load_adapter() -> dict[str, Any]:
    with open(REPO_ROOT / ".agent" / "repo_adapter.json", encoding="utf-8") as handle:
        return json.load(handle)


def _load_gitignore_lines() -> list[str]:
    with open(REPO_ROOT / ".gitignore", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip() and not line.lstrip().startswith("#")]


def _agent_runtime_gitignore_decision(path: str) -> bool:
    ignored = False
    for pattern in _load_gitignore_lines():
        if pattern == ".agent/reports/*" and path.startswith(".agent/reports/"):
            ignored = True
        elif pattern == ".agent/logs/*" and path.startswith(".agent/logs/"):
            ignored = True
        elif pattern == ".agent/needs_human.json" and path == ".agent/needs_human.json":
            ignored = True
        elif pattern == "!.agent/reports/.gitkeep" and path == ".agent/reports/.gitkeep":
            ignored = False
        elif pattern == "!.agent/logs/.gitkeep" and path == ".agent/logs/.gitkeep":
            ignored = False
    return ignored


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


def _fake_runner_state(tmp_dir: Path) -> tuple[dict[str, Any], Path]:
    state = _execution_enabled_state()
    state["report_output_template"] = (
        f"{tmp_dir.relative_to(REPO_ROOT).as_posix()}/{{timestamp}}-{{worker}}.report.json"
    )
    state["needs_human_path"] = (tmp_dir / "needs_human.json").relative_to(REPO_ROOT).as_posix()
    state["notify_stub_log"] = (tmp_dir / "notify_stub.log").relative_to(REPO_ROOT).as_posix()
    state_path = _write_json(tmp_dir / "state.fake.json", state)
    return state, state_path


def _fake_plan(tmp_dir: Path, scenario: str = "pass") -> tuple[dict[str, Any], Path, agent_orchestrator.ExecutionPlan]:
    state, state_path = _fake_runner_state(tmp_dir)
    plan = agent_orchestrator.build_execution_plan(state, "audit", timestamp=f"fake-{scenario}")
    preflight = agent_orchestrator.build_execution_preflight(
        state,
        "audit",
        plan,
        repo_status=_clean_repo_status(),
        mode="fake_runner_helper",
    )
    assert preflight["allowed"] is True
    assert preflight["safe_to_start_real_runner"] is False
    return state, state_path, plan


def test_repo_adapter_exists_and_identifies_reference_host() -> None:
    adapter_path = REPO_ROOT / ".agent" / "repo_adapter.json"

    assert adapter_path.exists()
    adapter = _load_adapter()
    assert adapter["adapter_version"] == 1
    assert adapter["repo_id"] == "nlmytgen"
    assert adapter["repo_kind"]


def test_repo_adapter_records_authority_docs_and_known_untracked_allowlist() -> None:
    adapter = _load_adapter()

    assert adapter["authority_docs"] == [
        "AGENTS.md",
        "docs/REPO_LOCAL_RULES.md",
        "docs/runtime-state.md",
    ]
    assert ".claude/worktrees/" in adapter["known_untracked_allowlist"]
    assert "samples/2026-05-16.ymmp" in adapter["known_untracked_allowlist"]


def test_repo_adapter_records_scope_and_forbidden_domains() -> None:
    adapter = _load_adapter()
    state = _load_state()

    assert adapter["allowed_change_roots"]
    assert adapter["blocked_change_roots"]
    assert adapter["allowed_change_roots"] == state["gate_policy"]["allowed_changed_path_prefixes"]
    assert adapter["blocked_change_roots"] == state["gate_policy"]["blocked_changed_path_prefixes"]
    for domain in (
        "publish",
        "release",
        "rights_status",
        "production_candidate",
        "external_notification",
    ):
        assert domain in adapter["forbidden_automation_domains"]


def test_repo_adapter_worker_groups_and_report_artifacts_are_inert() -> None:
    adapter = _load_adapter()

    assert adapter["worker_groups"]["default"] == ["advance", "audit", "fix", "summarize"]
    assert adapter["worker_groups"]["inert"] is True
    report_policy = adapter["report_artifact_policy"]
    assert report_policy["runtime_report_glob"] == ".agent/reports/*.report.json"
    assert report_policy["local_runtime_artifacts"] is True
    assert report_policy["commit_by_default"] is False
    assert report_policy["external_notification"] is False


def test_repo_adapter_does_not_enable_execution_or_migrate_policy() -> None:
    adapter = _load_adapter()

    assert adapter["runtime_effect"]["inert"] is True
    assert adapter["runtime_effect"]["runtime_policy_source"] == ".agent/state.json"
    assert adapter["runtime_effect"]["enables_codex_exec"] is False
    assert adapter["runtime_effect"]["migrates_gate_policy"] is False
    assert "execution_policy" not in adapter


def test_repo_adapter_does_not_resume_mainline_or_implement_clippipegen() -> None:
    adapter = _load_adapter()

    assert adapter["mainline_resume_contract"]["does_not_resume_mainline"] is True
    assert adapter["mainline_resume_contract"]["reference_host_only"] is True
    assert adapter["portability_notes"]["clip_pipe_gen_implemented"] is False
    assert "ClipPipeGen adapter should supply its own" in adapter["portability_notes"]["clip_pipe_gen_design_goal"]


def test_repo_adapter_keeps_nlmytgen_artifact_terms_out_of_common_runtime() -> None:
    adapter = _load_adapter()

    vocabulary = adapter["portability_notes"]["nlmytgen_specific_vocabulary"]
    for term in ("YMM4", "ymmp", "rights_status", "production_candidate", "diagnostic proof", "visual proof"):
        assert term in vocabulary
    for term in ("YMM4", "ymmp", "G-28", "production_candidate"):
        assert term in adapter["portability_notes"]["common_core_should_not_assume"]


def test_agent_runtime_artifacts_are_gitignored_by_policy() -> None:
    lines = _load_gitignore_lines()

    for pattern in (
        ".agent/reports/*",
        ".agent/logs/*",
        ".agent/needs_human.json",
    ):
        assert pattern in lines


def test_agent_runtime_gitkeep_files_remain_trackable() -> None:
    lines = _load_gitignore_lines()

    assert "!.agent/reports/.gitkeep" in lines
    assert "!.agent/logs/.gitkeep" in lines
    assert (REPO_ROOT / ".agent" / "reports" / ".gitkeep").exists()
    assert (REPO_ROOT / ".agent" / "logs" / ".gitkeep").exists()
    assert _agent_runtime_gitignore_decision(".agent/reports/.gitkeep") is False
    assert _agent_runtime_gitignore_decision(".agent/logs/.gitkeep") is False


def test_report_artifact_policy_keeps_generated_outputs_local() -> None:
    adapter = _load_adapter()
    report_policy = adapter["report_artifact_policy"]
    ignored_runtime_paths = {
        ".agent/reports/example.report.json",
        ".agent/needs_human.json",
        ".agent/logs/notify_stub.log",
    }

    assert report_policy["commit_by_default"] is False
    assert report_policy["local_runtime_artifacts"] is True
    assert report_policy["runtime_report_glob"] == ".agent/reports/*.report.json"
    assert all(_agent_runtime_gitignore_decision(path) for path in ignored_runtime_paths)


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
        human_real_execution_authority=True,
        notification_policy="local_stub_only",
    )

    assert result["allowed"] is False
    assert result["safe_to_start_real_runner"] is False
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False
    assert result["execution_enabled"] is False
    assert "execution_policy.codex_exec_enabled:false" in result["reasons"]
    assert result["mode"] == "real_runner"
    assert result["worker"] == "audit"
    assert result["prompt_path"] == ".agent/prompt_catalog/audit.md"
    assert result["schema_path"] == ".agent/schemas/worker_report.schema.json"
    assert result["report_path"].startswith(".agent/reports/")
    assert result["inspected_paths"] == [
        ".agent/prompt_catalog/audit.md",
        ".agent/schemas/worker_report.schema.json",
        result["report_path"],
    ]
    assert result["authority_summary"]["execution_policy_enabled"] is False
    assert result["authority_summary"]["human_real_execution_authority"] is True
    assert result["authority_summary"]["notification_policy"] == "local_stub_only"
    assert result["max_steps"] == 1
    assert result["timeout_seconds"] == 600
    assert result["repo_status"]["provided"] is True


def test_preflight_blocks_real_runner_without_explicit_human_authority() -> None:
    result = agent_orchestrator.build_execution_preflight(
        _execution_enabled_state(),
        "audit",
        repo_status=_clean_repo_status(),
        notification_policy="local_stub_only",
    )

    assert result["allowed"] is False
    assert result["safe_to_start_real_runner"] is False
    assert "missing_explicit_human_authority" in result["reasons"]
    assert result["authority_summary"]["human_real_execution_authority"] is False
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False


def test_preflight_dry_run_preview_allows_without_real_runner_start() -> None:
    result = agent_orchestrator.build_execution_preflight(
        _load_state(),
        "audit",
        repo_status=_clean_repo_status(),
        mode="dry_run_preview",
    )

    assert result["allowed"] is True
    assert result["safe_to_start_real_runner"] is False
    assert result["mode"] == "dry_run_preview"
    assert result["authority_summary"]["execution_policy_enabled"] is False
    assert result["authority_summary"]["human_real_execution_authority"] is False
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False


def test_preflight_fake_runner_helper_allows_without_real_runner_start() -> None:
    result = agent_orchestrator.build_execution_preflight(
        _execution_enabled_state(),
        "audit",
        repo_status=_clean_repo_status(),
        mode="fake_runner_helper",
    )

    assert result["allowed"] is True
    assert result["safe_to_start_real_runner"] is False
    assert result["mode"] == "fake_runner_helper"
    assert result["authority_summary"]["human_real_execution_authority"] is False
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False


def test_preflight_authorized_future_real_runner_can_start_only_after_all_gates_pass() -> None:
    result = agent_orchestrator.build_execution_preflight(
        _execution_enabled_state(),
        "audit",
        repo_status=_clean_repo_status(),
        human_real_execution_authority=True,
        notification_policy="local_stub_only",
    )

    assert result["allowed"] is True
    assert result["safe_to_start_real_runner"] is True
    assert result["mode"] == "real_runner"
    assert result["reasons"] == []
    assert result["authority_summary"] == {
        "execution_policy_enabled": True,
        "human_real_execution_authority": True,
        "notification_policy": "local_stub_only",
        "environment_policy": "not_inspected",
    }
    assert result["inspected_paths"] == [
        ".agent/prompt_catalog/audit.md",
        ".agent/schemas/worker_report.schema.json",
        result["report_path"],
    ]
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False


def test_preflight_rejects_shell_command_string_shape() -> None:
    plan = agent_orchestrator.build_execution_plan(
        _execution_enabled_state(),
        "audit",
        timestamp="shell-shape",
    )
    unsafe_plan = agent_orchestrator.ExecutionPlan(
        worker=plan.worker,
        cwd=plan.cwd,
        prompt_path=plan.prompt_path,
        schema_path=plan.schema_path,
        report_path=plan.report_path,
        argv="codex exec - --output-schema schema -o report",  # type: ignore[arg-type]
        stdin_source=plan.stdin_source,
        prompt_input_mode=plan.prompt_input_mode,
        codex_execution_started=False,
        execution_policy=plan.execution_policy,
    )

    result = agent_orchestrator.build_execution_preflight(
        _execution_enabled_state(),
        "audit",
        unsafe_plan,
        repo_status=_clean_repo_status(),
        human_real_execution_authority=True,
        notification_policy="local_stub_only",
    )

    assert result["allowed"] is False
    assert result["safe_to_start_real_runner"] is False
    assert "command_shape:shell_string" in result["reasons"]


def test_preflight_rejects_prompt_source_ambiguity() -> None:
    plan = agent_orchestrator.build_execution_plan(
        _execution_enabled_state(),
        "audit",
        timestamp="ambiguous-prompt",
    )
    ambiguous_plan = agent_orchestrator.ExecutionPlan(
        worker=plan.worker,
        cwd=plan.cwd,
        prompt_path=plan.prompt_path,
        schema_path=plan.schema_path,
        report_path=plan.report_path,
        argv=plan.argv,
        stdin_source="",
        prompt_input_mode="",
        codex_execution_started=False,
        execution_policy=plan.execution_policy,
    )

    result = agent_orchestrator.build_execution_preflight(
        _execution_enabled_state(),
        "audit",
        ambiguous_plan,
        repo_status=_clean_repo_status(),
        human_real_execution_authority=True,
        notification_policy="local_stub_only",
    )

    assert result["allowed"] is False
    assert result["safe_to_start_real_runner"] is False
    assert "prompt_source:ambiguous" in result["reasons"]


def test_preflight_rejects_notification_ambiguity_for_real_runner() -> None:
    result = agent_orchestrator.build_execution_preflight(
        _execution_enabled_state(),
        "audit",
        repo_status=_clean_repo_status(),
        human_real_execution_authority=True,
    )

    assert result["allowed"] is False
    assert result["safe_to_start_real_runner"] is False
    assert "notification_policy:ambiguous" in result["reasons"]


def test_preflight_rejects_credential_like_metadata_without_echoing_secret() -> None:
    secret_value = "s" + "k-test-secret-value"

    result = agent_orchestrator.build_execution_preflight(
        _execution_enabled_state(),
        "audit",
        repo_status=_clean_repo_status(),
        human_real_execution_authority=True,
        notification_policy="local_stub_only",
        credential_like_values={"environment.OPENAI_API_KEY": secret_value},
    )

    assert result["allowed"] is False
    assert result["safe_to_start_real_runner"] is False
    assert "credential_like_value:environment.OPENAI_API_KEY" in result["reasons"]
    assert secret_value not in json.dumps(result)


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

    result = agent_orchestrator.build_execution_preflight(
        _execution_enabled_state(),
        "audit",
        repo_status=repo_status,
        human_real_execution_authority=True,
        notification_policy="local_stub_only",
    )

    assert result["allowed"] is True
    assert result["safe_to_start_real_runner"] is True
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

    result = agent_orchestrator.build_execution_preflight(
        state,
        "audit",
        repo_status=_clean_repo_status(),
        human_real_execution_authority=True,
        notification_policy="local_stub_only",
    )

    assert result["allowed"] is True
    assert result["safe_to_start_real_runner"] is True
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


def test_fake_runner_pass_report_flows_through_gate_without_notify(repo_agent_tmp: Path) -> None:
    _, state_path, plan = _fake_plan(repo_agent_tmp, "pass")

    result = agent_orchestrator.run_fake_runner(plan, "pass", state_path).to_dict()

    assert result["mode"] == "fake"
    assert result["scenario"] == "pass"
    assert result["report_written"] is True
    assert result["report_path"].startswith(".agent/reports/_tmp_pytest_agent_orchestration/")
    assert result["gate_result"]["decision"] == "pass"
    assert result["gate_result"]["needs_human"] is False
    assert result["notify_stub"] is None
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False
    assert not (repo_agent_tmp / "needs_human.json").exists()
    assert not (repo_agent_tmp / "notify_stub.log").exists()


def test_fake_runner_needs_human_report_writes_only_local_notify_stub(repo_agent_tmp: Path) -> None:
    _, state_path, plan = _fake_plan(repo_agent_tmp, "needs-human")

    result = agent_orchestrator.run_fake_runner(plan, "needs_human", state_path).to_dict()

    assert result["gate_result"]["needs_human"] is True
    assert "status:needs_human" in result["gate_result"]["reasons"]
    assert result["notify_stub"]["payload"]["notification_sent"] is False
    assert result["notify_stub"]["needs_human_path"] == (
        repo_agent_tmp / "needs_human.json"
    ).relative_to(REPO_ROOT).as_posix()
    assert result["notify_stub"]["notify_stub_log"] == (
        repo_agent_tmp / "notify_stub.log"
    ).relative_to(REPO_ROOT).as_posix()
    assert (repo_agent_tmp / "needs_human.json").exists()
    assert (repo_agent_tmp / "notify_stub.log").exists()


def test_fake_runner_blocked_report_escalates_through_gate(repo_agent_tmp: Path) -> None:
    _, state_path, plan = _fake_plan(repo_agent_tmp, "blocked")

    result = agent_orchestrator.run_fake_runner(plan, "blocked", state_path).to_dict()

    assert result["gate_result"]["needs_human"] is True
    assert "status:blocked" in result["gate_result"]["reasons"]
    assert result["notify_stub"]["payload"]["notification_sent"] is False


@pytest.mark.parametrize(
    ("scenario", "expected_error_kind", "expected_exit_code", "expected_timed_out"),
    [
        ("invalid_json", "invalid_json", 0, False),
        ("missing_report", "missing_report", 0, False),
        ("nonzero_exit", "nonzero_exit", 2, False),
        ("timeout", "timeout", None, True),
    ],
)
def test_fake_runner_failure_scenarios_fail_closed(
    repo_agent_tmp: Path,
    scenario: str,
    expected_error_kind: str,
    expected_exit_code: int | None,
    expected_timed_out: bool,
) -> None:
    _, state_path, plan = _fake_plan(repo_agent_tmp, scenario)

    result = agent_orchestrator.run_fake_runner(plan, scenario, state_path).to_dict()

    assert result["gate_result"]["needs_human"] is True
    assert result["fail_closed"] is True
    assert result["error_kind"] == expected_error_kind
    assert result["exit_code"] == expected_exit_code
    assert result["timed_out"] is expected_timed_out
    assert result["notify_stub"] is None
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False
    assert not (repo_agent_tmp / "needs_human.json").exists()
    assert not (repo_agent_tmp / "notify_stub.log").exists()


def test_fake_runner_uses_repo_local_tmp_artifacts_and_cleanup_removes_them(repo_agent_tmp: Path) -> None:
    _, state_path, plan = _fake_plan(repo_agent_tmp, "cleanup")

    result = agent_orchestrator.run_fake_runner(plan, "needs_human", state_path).to_dict()

    for artifact in result["artifacts_written"]:
        assert artifact.startswith(".agent/reports/_tmp_pytest_agent_orchestration/")
        assert (REPO_ROOT / artifact).exists()

    shutil.rmtree(repo_agent_tmp)
    assert not repo_agent_tmp.exists()
    repo_agent_tmp.mkdir(parents=True)


def test_single_fake_execution_flow_pass_builds_plan_preflights_runs_gate_without_notify(
    repo_agent_tmp: Path,
) -> None:
    state, state_path = _fake_runner_state(repo_agent_tmp)

    result = agent_orchestrator.run_single_fake_execution_flow_for_test(
        state,
        "audit",
        "pass",
        repo_status=_clean_repo_status(),
        state_path=state_path,
        timestamp="single-pass",
    )

    assert result["status"] == "completed"
    assert result["preflight"]["allowed"] is True
    assert result["preflight"]["report_path"].startswith(
        ".agent/reports/_tmp_pytest_agent_orchestration/"
    )
    assert result["runner_started"] is True
    assert result["runner_result"]["gate_result"]["decision"] == "pass"
    assert result["runner_result"]["notify_stub"] is None
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False
    assert not (repo_agent_tmp / "needs_human.json").exists()
    assert not (repo_agent_tmp / "notify_stub.log").exists()


def test_single_fake_execution_flow_needs_human_writes_only_local_notify_stub(
    repo_agent_tmp: Path,
) -> None:
    state, state_path = _fake_runner_state(repo_agent_tmp)

    result = agent_orchestrator.run_single_fake_execution_flow_for_test(
        state,
        "audit",
        "needs_human",
        repo_status=_clean_repo_status(),
        state_path=state_path,
        timestamp="single-needs-human",
    )

    runner = result["runner_result"]
    assert result["status"] == "completed"
    assert runner["gate_result"]["needs_human"] is True
    assert "status:needs_human" in runner["gate_result"]["reasons"]
    assert runner["notify_stub"]["payload"]["notification_sent"] is False
    assert runner["notify_stub"]["needs_human_path"] == (
        repo_agent_tmp / "needs_human.json"
    ).relative_to(REPO_ROOT).as_posix()
    assert runner["notify_stub"]["notify_stub_log"] == (
        repo_agent_tmp / "notify_stub.log"
    ).relative_to(REPO_ROOT).as_posix()
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False


def test_operator_review_card_summarizes_needs_human_single_fake_flow(
    repo_agent_tmp: Path,
) -> None:
    state, state_path = _fake_runner_state(repo_agent_tmp)

    result = agent_orchestrator.run_single_fake_execution_flow_for_test(
        state,
        "audit",
        "needs_human",
        repo_status=_clean_repo_status(),
        state_path=state_path,
        timestamp="single-needs-human-card",
    )

    card = agent_operator_surface.render_operator_review_card(result)

    for section in (
        "## Summary",
        "## Status",
        "## What happened",
        "## Human decision needed",
        "## Files to inspect",
        "## Safety boundary",
        "## Next safe actions",
        "## Raw identifiers",
    ):
        assert section in card
    assert card.index("## Summary") < card.index("## Status")
    assert "- Human action required: yes" in card
    assert "- Card mode: real result" in card
    assert "- Attempted work: Review an existing local simulation result" in card
    assert "- Worker / scenario: Audit worker / Needs human review" in card
    assert "- Gate result: needs human review" in card
    assert "- Decision to make: Inspect the listed artifacts" in card
    assert "- status:needs_human" in card
    assert ".agent/reports/_tmp_pytest_agent_orchestration/single-needs-human-card-audit.report.json" in card
    assert ".agent/reports/_tmp_pytest_agent_orchestration/needs_human.json" in card
    assert "- Real Codex execution: not started" in card
    assert "- External notification service: not implemented" in card
    assert "- fail_closed:" not in card


def test_operator_review_card_marks_example_paths_as_illustrative() -> None:
    card = agent_operator_surface.render_operator_review_card(
        agent_operator_surface.EXAMPLE_SINGLE_FAKE_FLOW
    )

    assert "- Card mode: example" in card
    assert "This is a deterministic sample card" in card
    assert "Example paths only; this example command does not check whether these files exist." in card
    assert "single_fake_execution_flow_for_test" in card.split("## Raw identifiers", 1)[1]


def test_operator_review_card_surfaces_preflight_block_without_runner(
    repo_agent_tmp: Path,
) -> None:
    state = _load_state()
    state["report_output_template"] = (
        f"{repo_agent_tmp.relative_to(REPO_ROOT).as_posix()}/{{timestamp}}-{{worker}}.report.json"
    )

    result = agent_orchestrator.run_single_fake_execution_flow_for_test(
        state,
        "audit",
        "pass",
        repo_status={
            "tracked_dirty": ["scripts/agent_orchestrator.py"],
            "staged": [],
            "untracked": [],
        },
        timestamp="single-preflight-card",
    )

    card = agent_operator_surface.render_operator_review_card(result)

    assert "- Preflight check: blocked" in card
    assert "- Local simulation runner started: no" in card
    assert "- Runner report written: no" in card
    assert "- Human action required: yes" in card
    assert "- repo_status:tracked_dirty" in card
    assert "Resolve the listed preflight reason" in card
    assert not any(repo_agent_tmp.glob("*.report.json"))


def test_preflight_preview_card_surfaces_blocked_raw_result() -> None:
    preflight = agent_orchestrator.build_execution_preflight(
        _load_state(),
        "audit",
        repo_status=_clean_repo_status(),
        notification_policy="local_stub_only",
    )

    card = agent_operator_surface.render_preflight_preview_card(preflight)

    assert "# NLMYTGen Preflight Preview Card" in card
    assert "- Preflight status: blocked" in card
    assert "- Mode / worker: real_runner / audit" in card
    assert "- Allowed: no" in card
    assert "- Safe to start real runner: no" in card
    assert "- execution_policy.codex_exec_enabled:false" in card
    assert "- missing_explicit_human_authority" in card
    assert ".agent/prompt_catalog/audit.md" in card
    assert ".agent/schemas/worker_report.schema.json" in card
    assert "- execution_policy_enabled: no" in card
    assert "- human_real_execution_authority: no" in card
    assert "- notification_policy: local_stub_only" in card
    assert "- Real Codex execution: not started" in card
    assert "- Real subprocess runner: not started" in card
    assert "- Runtime artifacts: not written by preflight preview" in card


def test_preflight_preview_card_surfaces_allowed_dry_run_without_real_runner() -> None:
    preflight = agent_orchestrator.build_execution_preflight(
        _load_state(),
        "audit",
        repo_status=_clean_repo_status(),
        mode="dry_run_preview",
    )

    card = agent_operator_surface.render_preflight_preview_card(preflight)

    assert "- Preflight status: allowed" in card
    assert "- Mode / worker: dry_run_preview / audit" in card
    assert "- Allowed: yes" in card
    assert "- Safe to start real runner: no" in card
    assert "dry-run and fake-helper allows still cannot start a real runner" in card
    assert "- Real Codex execution: not started" in card
    assert "- Real subprocess runner: not started" in card


def test_preflight_preview_card_surfaces_authorized_real_runner_preview() -> None:
    preflight = agent_orchestrator.build_execution_preflight(
        _execution_enabled_state(),
        "audit",
        repo_status=_clean_repo_status(),
        human_real_execution_authority=True,
        notification_policy="local_stub_only",
    )

    card = agent_operator_surface.render_preflight_preview_card(preflight)

    assert "- Preflight status: allowed" in card
    assert "- Safe to start real runner: yes" in card
    assert "- execution_policy_enabled: yes" in card
    assert "- human_real_execution_authority: yes" in card
    assert "separate real-runner slice" in card
    assert "- Real Codex execution: not started" in card
    assert "- Real subprocess runner: not started" in card


def test_preflight_preview_card_redacts_credential_like_raw_values() -> None:
    secret_value = "s" + "k-preview-secret-value"
    preflight = {
        "allowed": False,
        "mode": "real_runner",
        "worker": "audit",
        "reasons": [f"credential_like_value:{secret_value}"],
        "safe_to_start_real_runner": False,
        "codex_execution_started": False,
        "real_subprocess_started": False,
        "report_path": ".agent/reports/example-audit.report.json",
        "inspected_paths": [f".agent/reports/{secret_value}.report.json"],
        "authority_summary": {"notification_policy": secret_value},
    }

    card = agent_operator_surface.render_preflight_preview_card(preflight)

    assert secret_value not in card
    assert "[redacted credential-like value]" in card


def test_operator_surface_cli_preflight_example_outputs_markdown(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = agent_operator_surface.main(["--preflight-example"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "# NLMYTGen Preflight Preview Card" in captured.out
    assert "- Preflight status: blocked" in captured.out
    assert "- Safe to start real runner: no" in captured.out
    assert "- Real Codex execution: not started" in captured.out
    assert "- Runtime artifacts: not written by preflight preview" in captured.out
    assert captured.err == ""


def test_operator_surface_cli_refuses_repo_external_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    outside_flow = tmp_path / "flow.json"
    outside_flow.write_text("{}\n", encoding="utf-8")

    exit_code = agent_operator_surface.main([str(outside_flow)])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "flow_result must stay inside this repo" in captured.err


def test_single_fake_execution_flow_blocked_escalates_through_gate_only(
    repo_agent_tmp: Path,
) -> None:
    state, state_path = _fake_runner_state(repo_agent_tmp)

    result = agent_orchestrator.run_single_fake_execution_flow_for_test(
        state,
        "audit",
        "blocked",
        repo_status=_clean_repo_status(),
        state_path=state_path,
        timestamp="single-blocked",
    )

    runner = result["runner_result"]
    assert result["status"] == "completed"
    assert runner["gate_result"]["needs_human"] is True
    assert "status:blocked" in runner["gate_result"]["reasons"]
    assert runner["notify_stub"]["payload"]["notification_sent"] is False
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False


@pytest.mark.parametrize(
    ("scenario", "expected_error_kind"),
    [
        ("invalid_json", "invalid_json"),
        ("missing_report", "missing_report"),
        ("nonzero_exit", "nonzero_exit"),
        ("timeout", "timeout"),
    ],
)
def test_single_fake_execution_flow_failure_scenarios_fail_closed_without_real_execution(
    repo_agent_tmp: Path,
    scenario: str,
    expected_error_kind: str,
) -> None:
    state, state_path = _fake_runner_state(repo_agent_tmp)

    result = agent_orchestrator.run_single_fake_execution_flow_for_test(
        state,
        "audit",
        scenario,
        repo_status=_clean_repo_status(),
        state_path=state_path,
        timestamp=f"single-{scenario}",
    )

    runner = result["runner_result"]
    assert result["status"] == "completed"
    assert runner["gate_result"]["needs_human"] is True
    assert runner["fail_closed"] is True
    assert runner["error_kind"] == expected_error_kind
    assert runner["notify_stub"] is None
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False
    assert not (repo_agent_tmp / "needs_human.json").exists()
    assert not (repo_agent_tmp / "notify_stub.log").exists()


def test_single_fake_execution_flow_allows_default_disabled_execution_policy_without_real_runner(
    repo_agent_tmp: Path,
) -> None:
    state = _load_state()
    state["report_output_template"] = (
        f"{repo_agent_tmp.relative_to(REPO_ROOT).as_posix()}/{{timestamp}}-{{worker}}.report.json"
    )

    result = agent_orchestrator.run_single_fake_execution_flow_for_test(
        state,
        "audit",
        "pass",
        repo_status=_clean_repo_status(),
        timestamp="single-disabled-policy",
    )

    assert result["status"] == "completed"
    assert result["preflight"]["allowed"] is True
    assert result["preflight"]["safe_to_start_real_runner"] is False
    assert result["preflight"]["mode"] == "fake_runner_helper"
    assert result["runner_started"] is True
    assert result["runner_result"]["gate_result"]["decision"] == "pass"
    assert result["codex_execution_started"] is False
    assert result["real_subprocess_started"] is False


@pytest.mark.parametrize(
    ("repo_status", "expected_reason"),
    [
        (
            {"tracked_dirty": ["scripts/agent_orchestrator.py"], "staged": [], "untracked": []},
            "repo_status:tracked_dirty",
        ),
        (
            {"tracked_dirty": [], "staged": ["scripts/agent_orchestrator.py"], "untracked": []},
            "repo_status:staged_files_present",
        ),
        (
            {"tracked_dirty": [], "staged": [], "untracked": ["unexpected.tmp"]},
            "repo_status:unknown_untracked_files",
        ),
    ],
)
def test_single_fake_execution_flow_refuses_dirty_or_staged_repo_status(
    repo_agent_tmp: Path,
    repo_status: dict[str, Any],
    expected_reason: str,
) -> None:
    state, state_path, plan = _fake_plan(repo_agent_tmp, "blocked-preflight")

    result = agent_orchestrator.run_single_fake_execution_flow_for_test(
        state,
        "audit",
        "pass",
        repo_status=repo_status,
        state_path=state_path,
        plan=plan,
    )

    assert result["status"] == "preflight_blocked"
    assert result["runner_started"] is False
    assert expected_reason in result["preflight"]["reasons"]
    assert not (REPO_ROOT / plan.report_path).exists()


def test_single_fake_execution_flow_refuses_existing_report_path(repo_agent_tmp: Path) -> None:
    state, state_path, plan = _fake_plan(repo_agent_tmp, "existing-report")
    _write_json(REPO_ROOT / plan.report_path, BASE_REPORT)

    result = agent_orchestrator.run_single_fake_execution_flow_for_test(
        state,
        "audit",
        "pass",
        repo_status=_clean_repo_status(),
        state_path=state_path,
        plan=plan,
    )

    assert result["status"] == "preflight_blocked"
    assert result["runner_started"] is False
    assert f"report_path:already_exists:{plan.report_path}" in result["preflight"]["reasons"]


def test_single_fake_execution_flow_refuses_invalid_report_path_policy(
    repo_agent_tmp: Path,
) -> None:
    state, state_path = _fake_runner_state(repo_agent_tmp)
    state["report_output_template"] = "docs/{timestamp}-{worker}.report.json"

    result = agent_orchestrator.run_single_fake_execution_flow_for_test(
        state,
        "audit",
        "pass",
        repo_status=_clean_repo_status(),
        state_path=state_path,
        timestamp="single-invalid-path",
    )

    assert result["status"] == "preflight_blocked"
    assert result["runner_started"] is False
    assert any(
        "report_path must stay under .agent/reports" in reason
        for reason in result["preflight"]["reasons"]
    )
    assert not (REPO_ROOT / "docs" / "single-invalid-path-audit.report.json").exists()


def test_fake_runner_is_not_reachable_from_default_orchestrator_path() -> None:
    result = agent_orchestrator.run(
        argparse.Namespace(
            worker="audit",
            dry_run=False,
            report=None,
            state=".agent/state.json",
        )
    )

    assert "fake_runner" not in result
    assert "single_fake_execution_flow" not in result
    assert result["codex_execution_started"] is False
    assert "No Codex execution is performed" in result["message"]


def test_no_cli_flag_exposes_single_fake_execution_flow() -> None:
    with pytest.raises(SystemExit):
        agent_orchestrator.main(["--worker", "audit", "--single-fake-flow"])


def test_common_orchestration_scripts_do_not_use_real_execution_or_notification_sentinels() -> None:
    for path in (
        REPO_ROOT / "scripts" / "agent_gate.py",
        REPO_ROOT / "scripts" / "agent_notify_stub.py",
        REPO_ROOT / "scripts" / "agent_orchestrator.py",
        REPO_ROOT / "scripts" / "agent_operator_surface.py",
    ):
        text = path.read_text(encoding="utf-8")
        assert "subprocess.run" not in text
        assert "codex_execution_started=True" not in text
        assert "real_subprocess_started=True" not in text
        assert "notification_sent=True" not in text


def test_orchestrator_dry_run_does_not_start_codex() -> None:
    result = agent_orchestrator.run(
        argparse.Namespace(
            worker="audit",
            dry_run=True,
            pre_execution_dry_run=False,
            report=None,
            timestamp=None,
            repo_status_clean=False,
            repo_status_json=None,
            state=".agent/state.json",
        )
    )

    assert result["dry_run"]["codex_execution_started"] is False
    assert result["dry_run"]["argv"][:3] == ["codex", "exec", "-"]
    assert result["dry_run"]["prompt_input_mode"] == "stdin_from_prompt_file"
    assert result["dry_run"]["preflight"]["allowed"] is True
    assert result["dry_run"]["preflight"]["safe_to_start_real_runner"] is False
    assert result["dry_run"]["preflight"]["mode"] == "dry_run_preview"
    assert "gate_result" not in result


def test_pre_execution_dry_run_preview_renders_plan_preflight_card_without_artifacts() -> None:
    report_path = REPO_ROOT / ".agent" / "reports" / "preview-mvp-audit.report.json"
    assert not report_path.exists()

    preview = agent_orchestrator.build_pre_execution_dry_run_preview(
        _load_state(),
        "audit",
        timestamp="preview-mvp",
        repo_status=_clean_repo_status(),
    )
    card = agent_orchestrator.render_pre_execution_dry_run_preview(preview)

    assert preview["preflight"]["allowed"] is True
    assert preview["preflight"]["safe_to_start_real_runner"] is False
    assert preview["runtime_artifacts_written"] == []
    assert "# NLMYTGen Pre-execution Dry-run Preview" in card
    assert "- Worker: audit" in card
    assert "- Prompt source: .agent/prompt_catalog/audit.md" in card
    assert "- Schema path: .agent/schemas/worker_report.schema.json" in card
    assert "- Planned report path: .agent/reports/preview-mvp-audit.report.json" in card
    assert "- codex" in card
    assert "- exec" in card
    assert "- This argv is shown only for review; it was not executed." in card
    assert "- Source: operator-provided" in card
    assert "- Preflight: passed for this preview" in card
    assert "- safe_to_start_real_runner: no; eligibility only, not execution permission" in card
    assert "# NLMYTGen Preflight Preview Card" in card
    assert "- subprocess.run: not implemented" in card
    assert "- runtime artifacts: not written" in card
    assert "gate result from a real run: not evaluated" in card
    assert not report_path.exists()


def test_pre_execution_dry_run_preview_surfaces_blocked_repo_status() -> None:
    repo_status = _clean_repo_status()
    repo_status["tracked_dirty"] = ["scripts/agent_orchestrator.py"]

    preview = agent_orchestrator.build_pre_execution_dry_run_preview(
        _load_state(),
        "audit",
        timestamp="preview-blocked",
        repo_status=repo_status,
    )
    card = agent_orchestrator.render_pre_execution_dry_run_preview(preview)

    assert preview["preflight"]["allowed"] is False
    assert "repo_status:tracked_dirty" in preview["preflight"]["reasons"]
    assert "- Preflight: blocked this preview" in card
    assert "- Tracked dirty: scripts/agent_orchestrator.py" in card
    assert "- repo_status:tracked_dirty" in card
    assert "Resolve or intentionally hold the listed preflight reasons" in card
    assert "- real codex exec: not started" in card


def test_orchestrator_cli_pre_execution_dry_run_outputs_markdown(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = agent_orchestrator.main(
        [
            "--worker",
            "audit",
            "--pre-execution-dry-run",
            "--timestamp",
            "cli-preview",
            "--repo-status-clean",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.err == ""
    assert captured.out.startswith("# NLMYTGen Pre-execution Dry-run Preview")
    assert ".agent/reports/cli-preview-audit.report.json" in captured.out
    assert "# NLMYTGen Preflight Preview Card" in captured.out
    assert "safe_to_start_real_runner: no; eligibility only, not execution permission" in captured.out
    assert "- codex_execution_started: no" in captured.out
    assert "- real_subprocess_started: no" in captured.out


def test_orchestrator_without_dry_run_or_report_still_cannot_execute_codex() -> None:
    result = agent_orchestrator.run(
        argparse.Namespace(
            worker="audit",
            dry_run=False,
            pre_execution_dry_run=False,
            report=None,
            timestamp=None,
            repo_status_clean=False,
            repo_status_json=None,
            state=".agent/state.json",
        )
    )

    assert result["codex_execution_started"] is False
    assert "No Codex execution is performed" in result["message"]
