"""Layout research packet for the episode 002 review cockpit."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIRNAME = "review_layout_research"
DEFAULT_ARTIFACT_ID = "episode_002_review_layout_research_and_pattern_benchmark_v1"
DEFAULT_COCKPIT_DIRNAME = "review_cockpit_compact"
DEFAULT_FOCUSED_DIRNAME = "focused_review_brief"
DEFAULT_REVIEWER_DIRNAME = "surface_alignment_review_packet"

REQUIRED_LAYOUT_RESEARCH_FILES = (
    "layout_research_manifest.json",
    "layout_research_report.md",
    "current_ui_diagnosis.md",
    "layout_principles.json",
    "pattern_benchmark.md",
    "candidate_wireframes.html",
    "candidate_wireframes.md",
    "layout_decision_matrix.json",
    "final_layout_recommendation.md",
    "validation_readback.json",
    "review_checklist.md",
    "limitations.md",
)

REQUIRED_BOUNDARY_FLAGS = (
    "dry_run",
    "sample_fixture_not_real",
    "no_real_transcript",
    "rights_boundary",
    "public_upload_closed",
    "yymm4_render_closed",
    "no_yymm4_import",
    "thumbnail_context_only",
    "validation_noise_nonblocking",
    "not_production_ready",
)

FORBIDDEN_TRUE_CLAIMS = (
    '"youtube_uploaded": true',
    '"production_ready": true',
    '"production_thumbnail_ready": true',
    '"public_ready": true',
    '"rights_accepted": true',
    '"render_completion": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"actual_yymm4_import": true',
    '"yymm4_rendered": true',
    '"thumbnail_image_generated": true',
)

EXTERNAL_REF_MARKERS = (
    "http://",
    "https://",
    "src=\"",
    "src='",
    "href=\"",
    "href='",
    "@import",
    "url(",
)

RESEARCH_SOURCES = (
    {
        "source_id": "nng_dashboard",
        "label": "NN/g dashboard guidance",
        "url": "https://www.nngroup.com/articles/dashboards-preattentive/",
        "used_for": "dashboard/status-board benchmark",
        "finding": "Dashboards are useful when a single page supports quick action from at-a-glance information.",
    },
    {
        "source_id": "nng_progressive_disclosure",
        "label": "NN/g progressive disclosure",
        "url": "https://www.nngroup.com/articles/progressive-disclosure/",
        "used_for": "detail deferral and novice support",
        "finding": "Advanced or rare detail belongs behind a secondary step so the primary choice stays learnable.",
    },
    {
        "source_id": "nng_cognitive_load",
        "label": "NN/g cognitive-load form principles",
        "url": "https://www.nngroup.com/articles/4-principles-reduce-cognitive-load/",
        "used_for": "structure, transparency, clarity, and support",
        "finding": "Structure, transparency, clarity, and support reduce the mental effort of deciding what to do.",
    },
    {
        "source_id": "nng_cards",
        "label": "NN/g card component definition",
        "url": "https://www.nngroup.com/articles/cards-component/",
        "used_for": "card-board benchmark",
        "finding": "Cards work when each card has one subject and can be scanned as a unit.",
    },
    {
        "source_id": "govuk_task_list",
        "label": "GOV.UK task list component",
        "url": "https://design-system.service.gov.uk/components/task-list/",
        "used_for": "task-list benchmark",
        "finding": "Task lists are for multi-step services and should not be used merely to show answers.",
    },
    {
        "source_id": "govuk_complete_multiple_tasks",
        "label": "GOV.UK complete multiple tasks pattern",
        "url": "https://design-system.service.gov.uk/patterns/complete-multiple-tasks/",
        "used_for": "multi-step service benchmark",
        "finding": "A task list helps when users must understand tasks, order, and completion state.",
    },
)


def build_review_layout_research(
    *,
    package_dir: str | Path,
    cockpit_dir: str | Path | None = None,
    focused_brief_dir: str | Path | None = None,
    reviewer_packet_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build the local layout research packet for the episode 002 review cockpit."""
    source_root = Path(package_dir)
    cockpit_root = Path(cockpit_dir) if cockpit_dir else source_root / DEFAULT_COCKPIT_DIRNAME
    focused_root = Path(focused_brief_dir) if focused_brief_dir else source_root / DEFAULT_FOCUSED_DIRNAME
    reviewer_root = Path(reviewer_packet_dir) if reviewer_packet_dir else source_root / DEFAULT_REVIEWER_DIRNAME
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root, cockpit_root, focused_root, reviewer_root)
    payloads = _load_payloads(paths)
    state = _research_state(
        artifact_id=artifact_id,
        source_root=source_root,
        cockpit_root=cockpit_root,
        focused_root=focused_root,
        reviewer_root=reviewer_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        payloads=payloads,
    )
    principles = _layout_principles(artifact_id, state)
    matrix = _decision_matrix(artifact_id, state)
    manifest = _manifest(artifact_id, state, matrix, output_root, repo_root)

    _write_json(output_root / "layout_research_manifest.json", manifest)
    _write_json(output_root / "layout_principles.json", principles)
    _write_json(output_root / "layout_decision_matrix.json", matrix)
    _write_text(output_root / "layout_research_report.md", _render_research_report(state, principles, matrix))
    _write_text(output_root / "current_ui_diagnosis.md", _render_current_ui_diagnosis(state))
    _write_text(output_root / "pattern_benchmark.md", _render_pattern_benchmark(matrix))
    _write_text(output_root / "candidate_wireframes.html", _render_wireframes_html(state, matrix))
    _write_text(output_root / "candidate_wireframes.md", _render_wireframes_md(matrix))
    _write_text(output_root / "final_layout_recommendation.md", _render_final_recommendation(state, matrix))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state, matrix))
    _write_text(output_root / "limitations.md", _render_limitations(state))

    readback = validate_review_layout_research(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_review_layout_research(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_review_layout_research(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated layout research packet."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_LAYOUT_RESEARCH_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["layout_research_manifest.json"])
    principles = _load_json_if_present(files["layout_principles.json"])
    matrix = _load_json_if_present(files["layout_decision_matrix.json"])
    json_payloads = {
        "layout_research_manifest": manifest,
        "layout_principles": principles,
        "layout_decision_matrix": matrix,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["layout_research_manifest"]
    principles = json_payloads["layout_principles"]
    matrix = json_payloads["layout_decision_matrix"]

    if manifest.get("artifact_kind") != "episode-review-layout-research":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "layout_research_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")

    boundary_flags = _dict(manifest.get("boundary_flags"))
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")

    candidates = _list(matrix.get("candidate_wireframes"))
    selected = _list(matrix.get("selected_candidate_ids"))
    patterns = _list(matrix.get("pattern_benchmark"))
    if len(patterns) < 6:
        failed_checks.append("pattern_benchmark_too_small")
    if len(candidates) != 3:
        failed_checks.append("candidate_wireframe_count_not_three")
    if len(selected) != 1:
        failed_checks.append("selected_candidate_count_not_one")
    elif selected[0] != "candidate_b_guided_decision_flow":
        failed_checks.append("selected_candidate_unexpected")

    if len(_list(principles.get("principles"))) < 6:
        failed_checks.append("principles_too_small")

    wireframe_html = files["candidate_wireframes.html"].read_text(encoding="utf-8") if files["candidate_wireframes.html"].exists() else ""
    wireframe_md = files["candidate_wireframes.md"].read_text(encoding="utf-8") if files["candidate_wireframes.md"].exists() else ""
    if "color-scheme: dark light" not in wireframe_html:
        failed_checks.append("wireframe_dark_marker_missing")
    if "prefers-color-scheme" not in wireframe_html:
        failed_checks.append("wireframe_prefers_color_scheme_missing")
    if "data-selected-candidate=\"candidate_b_guided_decision_flow\"" not in wireframe_html:
        failed_checks.append("selected_candidate_marker_missing")
    if "Candidate A" not in wireframe_html or "Candidate B" not in wireframe_html or "Candidate C" not in wireframe_html:
        failed_checks.append("wireframe_candidate_labels_missing")
    if len(wireframe_md.splitlines()) > 140:
        failed_checks.append("wireframe_markdown_too_long")

    wireframe_external_refs = _external_refs_in_files([files["candidate_wireframes.html"], files["candidate_wireframes.md"]])
    forbidden_hits = _forbidden_true_claims(root)
    failed_checks.extend(f"wireframe_external_ref:{hit}" for hit in wireframe_external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)

    recommendation_text = files["final_layout_recommendation.md"].read_text(encoding="utf-8") if files["final_layout_recommendation.md"].exists() else ""
    if "selected_candidate: candidate_b_guided_decision_flow" not in recommendation_text:
        failed_checks.append("recommendation_selection_missing")
    if "## Test Anti-Goals" not in recommendation_text:
        failed_checks.append("test_anti_goals_missing")

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "pattern_count": len(patterns),
        "candidate_wireframe_count": len(candidates),
        "selected_candidate_count": len(selected),
        "selected_candidate_exactly_one": len(selected) == 1,
        "selected_candidate": selected[0] if len(selected) == 1 else None,
        "wireframes_have_no_external_dependencies": not wireframe_external_refs,
        "forbidden_true_claims_absent": not forbidden_hits,
        "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS),
        "test_anti_goals_present": "## Test Anti-Goals" in recommendation_text,
    }
    return {
        "schema_version": "review_layout_research_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "primary_human_review": str(root / "layout_research_report.md"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "candidate_wireframes": str(root / "candidate_wireframes.html"),
        "final_recommendation": str(root / "final_layout_recommendation.md"),
        "launcher_command": f'start "" "{(root / "candidate_wireframes.html").resolve()}"',
        "access_state": "verified_present" if (root / "candidate_wireframes.html").exists() else "missing",
        "selected_candidate": selected[0] if len(selected) == 1 else None,
        "next_action": manifest.get("next_action"),
    }


def _input_paths(source_root: Path, cockpit_root: Path, focused_root: Path, reviewer_root: Path) -> dict[str, Path]:
    return {
        "cockpit_html": cockpit_root / "review_cockpit.html",
        "cockpit_validation": cockpit_root / "validation_readback.json",
        "cockpit_state": cockpit_root / "cockpit_state.json",
        "focused_html": focused_root / "focused_review_brief.html",
        "focused_validation": focused_root / "validation_readback.json",
        "aligned_story": reviewer_root / "aligned_review_story.md",
        "reviewer_validation": reviewer_root / "validation_readback.json",
        "gui_dashboard": source_root / "gui_dashboard_panel" / "dashboard_panel_preview.html",
        "import_preview": source_root / "ymm4_import_preview_pack" / "import_preview_panel.md",
        "thumbnail_proof": source_root / "thumbnail_visual_proof_pack" / "thumbnail_visual_proof.html",
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    payloads: dict[str, Any] = {}
    for name, path in paths.items():
        if path.suffix == ".json" and path.exists():
            payloads[name] = _load_json(path)
    return payloads


def _research_state(
    *,
    artifact_id: str,
    source_root: Path,
    cockpit_root: Path,
    focused_root: Path,
    reviewer_root: Path,
    output_root: Path,
    repo_root: Path,
    paths: dict[str, Path],
    payloads: dict[str, Any],
) -> dict[str, Any]:
    cockpit_state = _dict(payloads.get("cockpit_state"))
    cockpit_validation = _dict(payloads.get("cockpit_validation"))
    boundary_flags = _dict(cockpit_state.get("boundary_flags"))
    return {
        "schema_version": "review_layout_research_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-review-layout-research",
        "status": "layout_research_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "cockpit_dir": _relpath(cockpit_root, repo_root),
        "focused_brief_dir": _relpath(focused_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "evaluated_prototype": {
            "artifact_id": cockpit_validation.get("artifact_id", "episode_002_review_cockpit_compact_v1"),
            "path": _relpath(paths["cockpit_html"], repo_root),
            "verdict": "weak_pass_evaluated_prototype",
            "keep_as": "source_record_for_next_layout",
        },
        "source_records": [
            _record("compact_review_cockpit", paths["cockpit_html"], repo_root),
            _record("focused_review_brief", paths["focused_html"], repo_root),
            _record("aligned_review_story", paths["aligned_story"], repo_root),
            _record("gui_dashboard_panel", paths["gui_dashboard"], repo_root),
            _record("import_preview_panel", paths["import_preview"], repo_root),
            _record("thumbnail_visual_proof", paths["thumbnail_proof"], repo_root),
        ],
        "boundary_flags": {flag: boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS},
        "user_feedback": [
            "The current page still assumes prior project knowledge.",
            "The user has to search for what matters.",
            "The UI shows internal artifact state more than it guides discovery.",
            "Text density remains too high.",
            "Test-passing guidance and one-off wording are not durable.",
        ],
        "research_scope": {
            "web_sources_used": True,
            "web_source_count": len(RESEARCH_SOURCES),
            "external_dependencies_added": False,
            "production_ui_replacement": False,
        },
        "primary_human_review": _relpath(output_root / "layout_research_report.md", repo_root),
        "candidate_wireframes": _relpath(output_root / "candidate_wireframes.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_action": "Use candidate_b_guided_decision_flow as the next implementation target after human review.",
    }


def _layout_principles(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    principles = [
        {
            "principle_id": "novice_start_point",
            "name": "Explain the job before artifact state",
            "rule": "First screen should answer what this page is for, whether it fits the user's situation, and the next action.",
            "source_basis": ["supervisor_start_point", "govuk_task_list"],
        },
        {
            "principle_id": "guided_choice",
            "name": "One decision path, not equal artifact panels",
            "rule": "The layout should guide the user through the real input, YMM4 observation, or hold decision.",
            "source_basis": ["nng_cognitive_load", "nng_progressive_disclosure"],
        },
        {
            "principle_id": "progressive_records",
            "name": "Source records stay secondary",
            "rule": "Show provenance after the user understands the decision, not before.",
            "source_basis": ["nng_progressive_disclosure"],
        },
        {
            "principle_id": "plain_language",
            "name": "Use durable user language",
            "rule": "Prefer user task labels over internal enum-like labels in the primary surface.",
            "source_basis": ["supervisor_feedback"],
        },
        {
            "principle_id": "bounded_growth",
            "name": "Layout should absorb more evidence without becoming an audit log",
            "rule": "Add source records to a secondary evidence drawer, not to the first screen.",
            "source_basis": ["nng_dashboard", "nng_cards"],
        },
        {
            "principle_id": "gate_integrity",
            "name": "Safety gates are visible but not the main task",
            "rule": "Closed gates should reassure and constrain, not dominate the primary action.",
            "source_basis": ["supervisor_safety_gate_scope"],
        },
        {
            "principle_id": "semantic_validation",
            "name": "Tests should validate meaning, not exact layout counts",
            "rule": "Future checks should assert task hierarchy, selected recommendation, source records secondary, dependency absence, and gate integrity.",
            "source_basis": ["supervisor_test_anti_goals"],
        },
    ]
    return {
        "schema_version": "layout_principles.v1",
        "artifact_id": artifact_id,
        "status": "ready",
        "principles": principles,
        "research_sources": list(RESEARCH_SOURCES),
        "boundary_flags": state.get("boundary_flags"),
    }


def _decision_matrix(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    patterns = [
        _pattern("dashboard_status_board", "Dashboard / status board", 3, 2, "Good for at-a-glance monitoring, weak for novice decision discovery."),
        _pattern("start_page_service_entry", "Start page / service entry", 5, 4, "Strong at explaining purpose and first action, but needs a decision mechanism."),
        _pattern("task_list_checklist", "Task list / checklist", 3, 3, "Useful for multi-step completion, but this slice is one decision with optional evidence."),
        _pattern("command_center_cockpit", "Command center / cockpit", 2, 3, "Power-user friendly but repeats the current weakness: internal state can dominate."),
        _pattern("wizard_decision_flow", "Wizard / step-by-step decision flow", 5, 5, "Best fit for helping a novice discover the correct next action while deferring evidence."),
        _pattern("card_board_kanban", "Card board / kanban-like review surface", 3, 3, "Scannable but risks making all options look equal and board-like."),
    ]
    candidates = [
        {
            "candidate_id": "candidate_a_start_page_decision_board",
            "label": "Candidate A: start page plus decision board",
            "pattern_mix": ["start_page_service_entry", "card_board_kanban"],
            "score": 34,
            "status": "runner_up",
            "strength": "Best introductory frame and low-friction first screen.",
            "weakness": "Still asks the user to compare choices side by side.",
        },
        {
            "candidate_id": "candidate_b_guided_decision_flow",
            "label": "Candidate B: guided decision flow",
            "pattern_mix": ["start_page_service_entry", "wizard_decision_flow", "progressive_records"],
            "score": 41,
            "status": "selected",
            "strength": "Turns the review into a small sequence of situation checks and recommends one next action.",
            "weakness": "Needs careful copy so it feels like guidance, not automation deciding for the user.",
        },
        {
            "candidate_id": "candidate_c_novice_command_center",
            "label": "Candidate C: novice-friendly command center",
            "pattern_mix": ["command_center_cockpit", "dashboard_status_board"],
            "score": 27,
            "status": "rejected",
            "strength": "Preserves cockpit continuity and compact status visibility.",
            "weakness": "Closest to the weak_pass prototype and most likely to keep project jargon on top.",
        },
    ]
    criteria = [
        "usable_without_prior_project_knowledge",
        "clear_first_action",
        "low_text_density",
        "durable_language",
        "dark_mode_suitability",
        "bounded_growth",
        "supports_real_input_yymm4_hold",
        "source_records_secondary",
        "avoids_gate_overclaims",
    ]
    return {
        "schema_version": "layout_decision_matrix.v1",
        "artifact_id": artifact_id,
        "status": "ready",
        "criteria": criteria,
        "pattern_benchmark": patterns,
        "candidate_wireframes": candidates,
        "selected_candidate_ids": ["candidate_b_guided_decision_flow"],
        "winning_candidate": "candidate_b_guided_decision_flow",
        "evaluated_prototype_verdict": state["evaluated_prototype"]["verdict"],
        "decision": "Implement a guided decision flow next; do not continue polishing the command-center cockpit pattern first.",
        "boundary_flags": state.get("boundary_flags"),
    }


def _pattern(pattern_id: str, label: str, novice_score: int, action_score: int, verdict: str) -> dict[str, Any]:
    return {
        "pattern_id": pattern_id,
        "label": label,
        "novice_support_score": novice_score,
        "action_clarity_score": action_score,
        "verdict": verdict,
    }


def _manifest(
    artifact_id: str,
    state: dict[str, Any],
    matrix: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "layout_research_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-review-layout-research",
        "status": "layout_research_ready_local_offline",
        "output_dir": _relpath(output_root, repo_root),
        "files": {name: _relpath(output_root / name, repo_root) for name in REQUIRED_LAYOUT_RESEARCH_FILES},
        "evaluated_prototype": state.get("evaluated_prototype"),
        "primary_human_review": _relpath(output_root / "layout_research_report.md", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "candidate_wireframes": _relpath(output_root / "candidate_wireframes.html", repo_root),
        "selected_candidate": matrix.get("winning_candidate"),
        "boundary_flags": state.get("boundary_flags"),
        "next_action": state.get("next_action"),
    }


def _render_research_report(state: dict[str, Any], principles: dict[str, Any], matrix: dict[str, Any]) -> str:
    source_lines = [
        f"- {source['label']}: {source['finding']} Source: {source['url']}"
        for source in RESEARCH_SOURCES
    ]
    return "\n".join(
        [
            "# Episode 002 Review Layout Research",
            "",
            "This packet evaluates the current compact review cockpit as a weak-pass prototype and benchmarks better layout patterns before another UI implementation.",
            "",
            "## Current UI Failure Modes",
            "",
            "- The top screen still assumes the reader understands project vocabulary and internal artifact names.",
            "- The three choices are visible, but the page does not help a novice decide which one applies.",
            "- Status rows and gate chips explain what the tool knows before the user understands the job.",
            "- Source records are correctly secondary, but the first screen still feels like an audit cockpit.",
            "- Tests currently reward structure counts more than user-task semantics.",
            "",
            "## Research Basis",
            "",
            *source_lines,
            "",
            "## Reusable Design Principles",
            "",
            *[
                f"- {item['name']}: {item['rule']}"
                for item in _list(principles.get("principles"))
                if isinstance(item, dict)
            ],
            "",
            "## Pattern Benchmark Result",
            "",
            "The guided decision flow wins because the work is not broad monitoring; it is one human decision that must be made safely by someone who may not know the project history.",
            "",
            f"Selected candidate: `{matrix.get('winning_candidate')}`.",
            "",
            "Primary wireframe file:",
            "",
            f"`{state.get('candidate_wireframes')}`",
            "",
        ]
    )


def _render_current_ui_diagnosis(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Current UI Diagnosis",
            "",
            f"Evaluated prototype: `{state['evaluated_prototype']['path']}`",
            "",
            "Verdict: weak_pass_evaluated_prototype.",
            "",
            "## User Feedback Mapping",
            "",
            "- Prior-project knowledge burden: internal names such as GUI dashboard panel, import preview pack, and thumbnail visual proof pack are primary labels.",
            "- Search burden: the user must infer whether real input, YMM4 observation, or hold is the right path.",
            "- Tool-centric framing: the surface lists known artifacts and gates before it explains the user's situation.",
            "- Text density: each action card carries use/effect/requires text and competes with the surface status row.",
            "- Durability issue: a cockpit built around episode-specific artifact names will not scale to repeated review surfaces.",
            "",
            "## Design Requirement",
            "",
            "The replacement direction should open with a plain-language situation check, produce one recommended next action, and keep source records and gates secondary but available.",
            "",
        ]
    )


def _render_pattern_benchmark(matrix: dict[str, Any]) -> str:
    lines = [
        "# Pattern Benchmark",
        "",
        "| pattern | novice support | action clarity | verdict |",
        "|---|---:|---:|---|",
    ]
    for row in _list(matrix.get("pattern_benchmark")):
        if isinstance(row, dict):
            lines.append(
                f"| {row.get('label')} | {row.get('novice_support_score')} | {row.get('action_clarity_score')} | {row.get('verdict')} |"
            )
    lines.extend(
        [
            "",
            "## Candidate Comparison",
            "",
            "| candidate | status | score | key reason |",
            "|---|---|---:|---|",
        ]
    )
    for row in _list(matrix.get("candidate_wireframes")):
        if isinstance(row, dict):
            lines.append(f"| {row.get('label')} | {row.get('status')} | {row.get('score')} | {row.get('strength')} |")
    return "\n".join(lines) + "\n"


def _render_wireframes_html(state: dict[str, Any], matrix: dict[str, Any]) -> str:
    cards = "\n".join(_render_candidate_card(candidate) for candidate in _list(matrix.get("candidate_wireframes")))
    gates = "\n".join(f"<span>{_escape(flag)}</span>" for flag in REQUIRED_BOUNDARY_FLAGS)
    return f"""<!doctype html>
<html lang="en" data-layout-research="true" data-selected-candidate="candidate_b_guided_decision_flow">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Layout Wireframes</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #080d17;
      --panel: #111827;
      --panel2: #162033;
      --text: #e6edf6;
      --muted: #a7b5c8;
      --line: #33445f;
      --accent: #2dd4bf;
      --selected: #93c5fd;
      --warn: #f5c542;
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #edf4f8;
        --panel: #f7fafc;
        --panel2: #e8eef5;
        --text: #182235;
        --muted: #475569;
        --line: #bfd0df;
        --accent: #0f766e;
        --selected: #1d4ed8;
        --warn: #8a5a00;
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--text); font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; letter-spacing: 0; }}
    main {{ width: min(1180px, calc(100% - 32px)); margin: 0 auto; padding: 24px 0 32px; }}
    header {{ display: grid; gap: 8px; padding: 16px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; }}
    h1 {{ margin: 0; font-size: clamp(1.35rem, 2.4vw, 2rem); letter-spacing: 0; }}
    h2 {{ margin: 0 0 8px; font-size: 1rem; letter-spacing: 0; }}
    p {{ margin: 0; color: var(--muted); line-height: 1.45; }}
    .grid {{ display: grid; gap: 14px; grid-template-columns: repeat(3, minmax(0, 1fr)); margin-top: 14px; }}
    .candidate {{ min-height: 390px; display: grid; gap: 12px; align-content: start; padding: 14px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; }}
    .candidate[data-status="selected"] {{ border-color: var(--selected); box-shadow: 0 0 0 2px rgba(147, 197, 253, 0.18); }}
    .tag {{ display: inline-flex; width: fit-content; padding: 4px 8px; border-radius: 999px; background: var(--panel2); color: var(--accent); font-size: 0.78rem; font-weight: 700; }}
    .screen {{ display: grid; gap: 8px; padding: 12px; background: var(--panel2); border: 1px dashed var(--line); border-radius: 6px; }}
    .block {{ min-height: 34px; padding: 8px; border: 1px solid var(--line); border-radius: 5px; color: var(--muted); }}
    .primary {{ border-color: var(--selected); color: var(--text); }}
    .choice {{ display: grid; grid-template-columns: 22px 1fr; gap: 8px; align-items: center; }}
    .dot {{ width: 18px; height: 18px; border-radius: 999px; border: 2px solid var(--accent); }}
    .gate-strip {{ margin-top: 14px; display: flex; flex-wrap: wrap; gap: 8px; padding: 10px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; }}
    .gate-strip span {{ padding: 5px 8px; border-radius: 999px; background: var(--panel2); color: var(--muted); font-size: 0.78rem; }}
    @media (max-width: 880px) {{ main {{ width: min(100% - 20px, 1180px); padding-top: 12px; }} .grid {{ grid-template-columns: 1fr; }} .candidate {{ min-height: auto; }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Layout Wireframe Candidates</h1>
      <p>Low-fidelity dark-mode candidates for the next Episode 002 review surface. The selected implementation target is Candidate B.</p>
    </header>
    <section class="grid">{cards}</section>
    <section class="gate-strip" aria-label="closed boundaries">{gates}</section>
  </main>
</body>
</html>
"""


def _render_candidate_card(candidate: Any) -> str:
    if not isinstance(candidate, dict):
        return ""
    cid = str(candidate.get("candidate_id"))
    status = str(candidate.get("status"))
    if cid == "candidate_a_start_page_decision_board":
        blocks = [
            ("primary", "What this review is for"),
            ("", "Do you have verified real input?"),
            ("", "Choose: real input / YMM4 observation / hold"),
            ("", "Evidence drawer"),
        ]
    elif cid == "candidate_b_guided_decision_flow":
        blocks = [
            ("primary", "Start: What situation are you in?"),
            ("choice", "1. Real source or transcript is available"),
            ("choice", "2. YMM4 import observation is explicitly selected"),
            ("choice", "3. Neither is true"),
            ("primary", "Recommended next action"),
            ("", "Source records and gates drawer"),
        ]
    else:
        blocks = [
            ("primary", "Decision status"),
            ("", "Three compact action tiles"),
            ("", "Evidence health row"),
            ("", "Gate strip"),
            ("", "Records drawer"),
        ]
    screen = "\n".join(_wire_block(kind, label) for kind, label in blocks)
    return "\n".join(
        [
            f'      <article class="candidate" data-candidate="{_escape(cid)}" data-status="{_escape(status)}">',
            f'        <span class="tag">{_escape(status)}</span>',
            f"        <h2>{_escape(candidate.get('label'))}</h2>",
            f"        <p>{_escape(candidate.get('strength'))}</p>",
            f'        <div class="screen">{screen}</div>',
            f"        <p>{_escape(candidate.get('weakness'))}</p>",
            "      </article>",
        ]
    )


def _wire_block(kind: str, label: str) -> str:
    if kind == "choice":
        return f'<div class="block choice"><span class="dot"></span><span>{_escape(label)}</span></div>'
    class_name = "block primary" if kind == "primary" else "block"
    return f'<div class="{class_name}">{_escape(label)}</div>'


def _render_wireframes_md(matrix: dict[str, Any]) -> str:
    lines = [
        "# Candidate Wireframes",
        "",
        "Selected implementation target: `candidate_b_guided_decision_flow`.",
        "",
    ]
    for candidate in _list(matrix.get("candidate_wireframes")):
        if not isinstance(candidate, dict):
            continue
        lines.extend(
            [
                f"## {candidate.get('label')}",
                "",
                f"- status: {candidate.get('status')}",
                f"- pattern mix: {', '.join(str(item) for item in _list(candidate.get('pattern_mix')))}",
                f"- strength: {candidate.get('strength')}",
                f"- weakness: {candidate.get('weakness')}",
                "",
            ]
        )
    return "\n".join(lines)


def _render_final_recommendation(state: dict[str, Any], matrix: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Final Layout Recommendation",
            "",
            "selected_candidate: candidate_b_guided_decision_flow",
            "",
            "## Why",
            "",
            "Candidate B is the next implementation target because the core job is not monitoring. The user needs to identify which situation applies, then receive one safe next action while provenance remains available on demand.",
            "",
            "## Next Implementation Target",
            "",
            "Build a guided start-to-decision flow: first explain the review purpose in plain language, then ask the minimum situation checks, then show one recommended action and a secondary evidence/gate drawer.",
            "",
            "## Known Risks",
            "",
            "- If the flow hides too much evidence, expert reviewers may feel slowed down.",
            "- If copy is too assertive, it may look like the tool is approving real input or YMM4 work.",
            "- If tests keep asserting exact card counts, the better layout may be blocked for the wrong reason.",
            "",
            "## Test Anti-Goals",
            "",
            "Avoid testing exact card counts, exact strings, enum labels in primary copy, and fixed visual section names as success criteria.",
            "",
            "Prefer testing that the primary user question exists, the action hierarchy is clear, exactly one final recommendation is selected, source records remain secondary, external dependencies are absent, and all closed gates stay intact.",
            "",
            "Copy policy: primary copy should use durable user language, with internal artifact IDs limited to details or machine-readable files.",
            "",
            "Layout policy: validate meaning and containment, not one specific grid.",
            "",
        ]
    )


def _render_review_checklist(state: dict[str, Any], matrix: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Layout Research Review Checklist",
            "",
            "- Read `layout_research_report.md` for the benchmark conclusion.",
            "- Open `candidate_wireframes.html` to compare A, B, and C.",
            "- Confirm Candidate B is the single selected next implementation target.",
            "- Confirm current `review_cockpit.html` is treated as weak-pass evaluated prototype, not replaced here.",
            "- Confirm source records and safety gates remain secondary and intact.",
            "",
            f"Selected candidate: `{matrix.get('winning_candidate')}`",
            "",
            f"Candidate wireframes: `{state.get('candidate_wireframes')}`",
            "",
        ]
    )


def _render_limitations(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Layout Research Limitations",
            "",
            "This packet is research and low-fidelity wireframing only.",
            "",
            "Not performed:",
            "",
            "- production review cockpit replacement",
            "- real transcript rerun or real source replacement",
            "- YMM4 GUI launch, import, render, or production `.ymmp` generation",
            "- final thumbnail approval",
            "- public upload, publication, scheduling, or visibility change",
            "- rights/legal/public-ready acceptance",
            "- OAuth, API keys, payment, or paid services",
            "- live scraping or media download",
            "- external CSS, JavaScript, font, image, media, or CDN dependency",
            "- full-suite green campaign or broad fixture regeneration",
            "",
            "Primary research report:",
            "",
            f"`{state.get('primary_human_review')}`",
            "",
        ]
    )


def _record(record_id: str, path: Path, repo_root: Path) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "repo_relative_path": _relpath(path, repo_root),
        "role": "source_record",
        "exists": path.exists(),
    }


def _forbidden_true_claims(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
            for claim in FORBIDDEN_TRUE_CLAIMS:
                if claim in text:
                    hits.append(f"{path.name}:{claim}")
    return hits


def _external_refs_in_files(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8-sig", errors="ignore").lower()
        for marker in EXTERNAL_REF_MARKERS:
            if marker in text:
                hits.append(f"{path.name}:{marker}")
    return hits


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON input must be an object: {path}")
    return data


def _load_json_if_present(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def _find_repo_root(path: Path) -> Path:
    resolved = path.resolve()
    for candidate in (resolved, *resolved.parents):
        if (candidate / "pyproject.toml").exists() or (candidate / "AGENTS.md").exists():
            return candidate
    return Path.cwd()


def _relpath(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def _escape(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}
