"""Second-pass layout benchmark for the episode 002 review UI."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIRNAME = "review_layout_second_pass"
DEFAULT_ARTIFACT_ID = "episode_002_layout_second_pass_split_view_benchmark_v1"
DEFAULT_GUIDED_FLOW_DIRNAME = "guided_decision_flow_prototype"
DEFAULT_LAYOUT_RESEARCH_DIRNAME = "review_layout_research"
DEFAULT_COCKPIT_DIRNAME = "review_cockpit_compact"
DEFAULT_REVIEWER_DIRNAME = "surface_alignment_review_packet"

SELECTED_CANDIDATE = "candidate_a_split_view_decision_evidence_pane"

REQUIRED_LAYOUT_SECOND_PASS_FILES = (
    "layout_second_pass_manifest.json",
    "current_guided_flow_diagnosis.md",
    "split_view_benchmark.md",
    "layout_candidate_matrix.json",
    "evidence_handling_report.md",
    "card_bloat_risk_report.md",
    "candidate_wireframes_second_pass.html",
    "candidate_wireframes_second_pass.md",
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

REQUIRED_CANDIDATES = (
    "candidate_a_split_view_decision_evidence_pane",
    "candidate_b_spine_detail_active_path",
    "candidate_c_service_entry_decision_board",
    "candidate_d_wizard_step_flow",
    "candidate_e_current_card_drawer_guided_flow",
    "candidate_f_command_center_cockpit",
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
    '"production_ui_replaced": true',
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


def build_review_layout_second_pass(
    *,
    package_dir: str | Path,
    guided_flow_dir: str | Path | None = None,
    layout_research_dir: str | Path | None = None,
    cockpit_dir: str | Path | None = None,
    reviewer_packet_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a local second-pass layout benchmark package."""
    source_root = Path(package_dir)
    guided_root = Path(guided_flow_dir) if guided_flow_dir else source_root / DEFAULT_GUIDED_FLOW_DIRNAME
    layout_root = Path(layout_research_dir) if layout_research_dir else source_root / DEFAULT_LAYOUT_RESEARCH_DIRNAME
    cockpit_root = Path(cockpit_dir) if cockpit_dir else source_root / DEFAULT_COCKPIT_DIRNAME
    reviewer_root = Path(reviewer_packet_dir) if reviewer_packet_dir else source_root / DEFAULT_REVIEWER_DIRNAME
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root, guided_root, layout_root, cockpit_root, reviewer_root)
    payloads = _load_payloads(paths)
    state = _second_pass_state(
        artifact_id=artifact_id,
        source_root=source_root,
        guided_root=guided_root,
        layout_root=layout_root,
        cockpit_root=cockpit_root,
        reviewer_root=reviewer_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        payloads=payloads,
    )
    matrix = _layout_candidate_matrix(artifact_id, state)
    evidence = _evidence_handling(state, matrix)
    card_bloat = _card_bloat_risk(state, matrix)
    manifest = _manifest(artifact_id, state, matrix, output_root, repo_root)

    _write_json(output_root / "layout_second_pass_manifest.json", manifest)
    _write_json(output_root / "layout_candidate_matrix.json", matrix)
    _write_text(output_root / "current_guided_flow_diagnosis.md", _render_guided_flow_diagnosis(state))
    _write_text(output_root / "split_view_benchmark.md", _render_split_view_benchmark(state, matrix))
    _write_text(output_root / "evidence_handling_report.md", _render_evidence_handling_report(evidence))
    _write_text(output_root / "card_bloat_risk_report.md", _render_card_bloat_report(card_bloat))
    _write_text(output_root / "candidate_wireframes_second_pass.html", _render_wireframes_html(state, matrix))
    _write_text(output_root / "candidate_wireframes_second_pass.md", _render_wireframes_md(matrix))
    _write_text(output_root / "final_layout_recommendation.md", _render_final_recommendation(state, matrix))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state, matrix))
    _write_text(output_root / "limitations.md", _render_limitations(state))

    readback = validate_review_layout_second_pass(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_review_layout_second_pass(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_review_layout_second_pass(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated second-pass layout benchmark."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_LAYOUT_SECOND_PASS_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["layout_second_pass_manifest.json"])
    matrix = _load_json_if_present(files["layout_candidate_matrix.json"])
    json_payloads = {
        "layout_second_pass_manifest": manifest,
        "layout_candidate_matrix": matrix,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["layout_second_pass_manifest"]
    matrix = json_payloads["layout_candidate_matrix"]

    if manifest.get("artifact_kind") != "episode-review-layout-second-pass":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "layout_second_pass_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")
    if manifest.get("evaluated_guided_flow", {}).get("verdict") != "weak_pass_evaluated_prototype":
        failed_checks.append("guided_flow_verdict_mismatch")

    boundary_flags = _dict(manifest.get("boundary_flags"))
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")

    candidates = _list(matrix.get("candidates"))
    candidate_ids = [row.get("candidate_id") for row in candidates if isinstance(row, dict)]
    selected_ids = _list(matrix.get("selected_candidate_ids"))
    if len(candidates) < 6:
        failed_checks.append("candidate_count_too_small")
    for candidate_id in REQUIRED_CANDIDATES:
        if candidate_id not in candidate_ids:
            failed_checks.append(f"required_candidate_missing:{candidate_id}")
    if len(selected_ids) != 1:
        failed_checks.append("selected_candidate_count_not_one")
    elif selected_ids[0] != SELECTED_CANDIDATE:
        failed_checks.append("selected_candidate_unexpected")
    if matrix.get("winning_candidate") != SELECTED_CANDIDATE:
        failed_checks.append("winning_candidate_unexpected")

    html_text = files["candidate_wireframes_second_pass.html"].read_text(encoding="utf-8") if files["candidate_wireframes_second_pass.html"].exists() else ""
    md_text = files["candidate_wireframes_second_pass.md"].read_text(encoding="utf-8") if files["candidate_wireframes_second_pass.md"].exists() else ""
    recommendation_text = files["final_layout_recommendation.md"].read_text(encoding="utf-8") if files["final_layout_recommendation.md"].exists() else ""
    evidence_text = files["evidence_handling_report.md"].read_text(encoding="utf-8") if files["evidence_handling_report.md"].exists() else ""
    card_text = files["card_bloat_risk_report.md"].read_text(encoding="utf-8") if files["card_bloat_risk_report.md"].exists() else ""
    split_text = files["split_view_benchmark.md"].read_text(encoding="utf-8") if files["split_view_benchmark.md"].exists() else ""

    if f'data-selected-candidate="{SELECTED_CANDIDATE}"' not in html_text:
        failed_checks.append("selected_candidate_marker_missing")
    if "color-scheme: dark light" not in html_text:
        failed_checks.append("wireframe_dark_marker_missing")
    if "prefers-color-scheme" not in html_text:
        failed_checks.append("wireframe_prefers_color_scheme_missing")
    if "data-left-pane" not in html_text or "data-right-pane" not in html_text:
        failed_checks.append("split_view_panes_missing")
    if "Evidence preview pane" not in html_text or "Gate context" not in html_text:
        failed_checks.append("split_view_evidence_context_missing")
    if "Active path spine" not in html_text or "Selected node detail" not in html_text:
        failed_checks.append("spine_detail_wireframe_missing")
    if "Current card/drawer pattern" not in html_text:
        failed_checks.append("current_pattern_critique_missing")
    if len(md_text.splitlines()) > 180:
        failed_checks.append("wireframe_markdown_too_long")

    if f"selected_candidate: {SELECTED_CANDIDATE}" not in recommendation_text:
        failed_checks.append("recommendation_selection_missing")
    for phrase in (
        "user-situation-first",
        "visible active path",
        "evidence is available without becoming a junk drawer",
        "internal artifact IDs are secondary",
        "gate details are bounded",
        "exactly one recommended next step",
        "no external dependencies",
        "no production/YMM4/public overclaims",
    ):
        if phrase not in recommendation_text:
            failed_checks.append(f"test_strategy_phrase_missing:{phrase}")

    if "not a generic drawer" not in evidence_text:
        failed_checks.append("evidence_non_drawer_policy_missing")
    if "card-bloat risk: high" not in card_text:
        failed_checks.append("card_bloat_high_risk_missing")
    if "split view: decision rail + evidence/preview pane" not in split_text:
        failed_checks.append("split_view_benchmark_missing")

    external_refs = _external_refs_in_files([path for name, path in files.items() if name != "validation_readback.json"])
    forbidden_hits = _forbidden_true_claims(root)
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "candidate_count": len(candidates),
        "required_candidates_present": all(candidate_id in candidate_ids for candidate_id in REQUIRED_CANDIDATES),
        "selected_candidate_exactly_one": len(selected_ids) == 1,
        "selected_candidate": selected_ids[0] if len(selected_ids) == 1 else None,
        "split_view_candidate_present": SELECTED_CANDIDATE in candidate_ids,
        "split_view_panes_present": "data-left-pane" in html_text and "data-right-pane" in html_text,
        "spine_detail_candidate_present": "candidate_b_spine_detail_active_path" in candidate_ids,
        "current_pattern_critique_present": "candidate_e_current_card_drawer_guided_flow" in candidate_ids,
        "evidence_not_generic_drawer": "not a generic drawer" in evidence_text,
        "card_bloat_risk_classified": "card-bloat risk: high" in card_text,
        "wireframes_have_no_external_dependencies": not external_refs,
        "forbidden_true_claims_absent": not forbidden_hits,
        "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS),
        "test_strategy_present": "user-situation-first" in recommendation_text and "visible active path" in recommendation_text,
    }
    return {
        "schema_version": "layout_second_pass_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "selected_candidate": selected_ids[0] if len(selected_ids) == 1 else None,
        "primary_human_review": str(root / "split_view_benchmark.md"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "candidate_wireframes": str(root / "candidate_wireframes_second_pass.html"),
        "final_recommendation": str(root / "final_layout_recommendation.md"),
        "launcher_command": f'start "" "{(root / "candidate_wireframes_second_pass.html").resolve()}"',
        "access_state": "verified_present" if (root / "candidate_wireframes_second_pass.html").exists() else "missing",
        "next_action": manifest.get("next_action"),
    }


def _input_paths(
    source_root: Path,
    guided_root: Path,
    layout_root: Path,
    cockpit_root: Path,
    reviewer_root: Path,
) -> dict[str, Path]:
    return {
        "guided_html": guided_root / "guided_decision_flow.html",
        "guided_validation": guided_root / "validation_readback.json",
        "guided_state": guided_root / "flow_state.json",
        "guided_recommendation": guided_root / "recommendation_engine_readback.json",
        "guided_evidence": guided_root / "evidence_drawer_index.json",
        "layout_manifest": layout_root / "layout_research_manifest.json",
        "layout_decision_matrix": layout_root / "layout_decision_matrix.json",
        "layout_principles": layout_root / "layout_principles.json",
        "layout_wireframes": layout_root / "candidate_wireframes.html",
        "layout_recommendation": layout_root / "final_layout_recommendation.md",
        "cockpit_html": cockpit_root / "review_cockpit.html",
        "aligned_story": reviewer_root / "aligned_review_story.md",
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


def _second_pass_state(
    *,
    artifact_id: str,
    source_root: Path,
    guided_root: Path,
    layout_root: Path,
    cockpit_root: Path,
    reviewer_root: Path,
    output_root: Path,
    repo_root: Path,
    paths: dict[str, Path],
    payloads: dict[str, Any],
) -> dict[str, Any]:
    guided_state = _dict(payloads.get("guided_state"))
    guided_validation = _dict(payloads.get("guided_validation"))
    layout_manifest = _dict(payloads.get("layout_manifest"))
    boundary_flags = _boundary_flags(guided_state, layout_manifest)
    return {
        "schema_version": "layout_second_pass_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-review-layout-second-pass",
        "status": "layout_second_pass_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "guided_flow_dir": _relpath(guided_root, repo_root),
        "layout_research_dir": _relpath(layout_root, repo_root),
        "cockpit_dir": _relpath(cockpit_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "evaluated_guided_flow": {
            "artifact_id": guided_validation.get("artifact_id", "episode_002_guided_decision_flow_prototype_v1"),
            "path": _relpath(paths["guided_html"], repo_root),
            "verdict": "weak_pass_evaluated_prototype",
            "reason": "One-screen dark prototype succeeds at situation-first framing but falls back to card rows and a generic evidence drawer.",
        },
        "source_records": [
            _record("guided_flow_html", "Guided decision flow HTML", paths["guided_html"], "evaluated_prototype", repo_root),
            _record("guided_flow_validation", "Guided decision flow validation", paths["guided_validation"], "evaluated_prototype", repo_root),
            _record("guided_flow_evidence", "Guided flow evidence index", paths["guided_evidence"], "evaluated_prototype", repo_root),
            _record("layout_research_matrix", "First-pass layout matrix", paths["layout_decision_matrix"], "first_pass_research", repo_root),
            _record("compact_review_cockpit", "Compact review cockpit", paths["cockpit_html"], "prior_prototype", repo_root),
            _record("aligned_review_story", "Aligned review story", paths["aligned_story"], "source_record", repo_root),
            _record("gui_dashboard_panel", "GUI dashboard panel", paths["gui_dashboard"], "source_record", repo_root),
            _record("import_preview_panel", "YMM4 import preview panel", paths["import_preview"], "source_record", repo_root),
            _record("thumbnail_visual_proof", "Thumbnail visual proof", paths["thumbnail_proof"], "source_record", repo_root),
        ],
        "feedback_drivers": [
            "The guided flow is one screen and dark but still card-based.",
            "The evidence drawer feels like storage rather than decision support.",
            "Needed information may be over-trimmed from the primary view.",
            "Cards and drawers may amplify as later episodes add surfaces.",
            "Split-view and master-detail patterns deserve a direct benchmark.",
        ],
        "research_basis": [
            "Dashboards help monitoring, but this task is choosing a next lane.",
            "Progressive disclosure works only when secondary information is genuinely secondary.",
            "Task lists fit multi-step services, not a single next-lane decision.",
            "Split-view and spine-detail patterns can keep decision and evidence visible together.",
            "Card grids are suspect unless each card is a primary action and dependencies stay visible.",
        ],
        "boundary_flags": boundary_flags,
        "primary_human_review": _relpath(output_root / "split_view_benchmark.md", repo_root),
        "candidate_wireframes": _relpath(output_root / "candidate_wireframes_second_pass.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_action": "Use candidate_a_split_view_decision_evidence_pane as the next implementation target; do not treat this research packet as a production UI replacement.",
    }


def _layout_candidate_matrix(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    criteria = [
        "user_situation_first",
        "visible_active_path",
        "evidence_trust_without_junk_drawer",
        "bounded_gate_context",
        "low_card_bloat_risk",
        "scales_to_future_episode_reviews",
        "supports_real_input_yymm4_hold",
        "internal_artifact_ids_secondary",
        "avoids_production_overclaim",
    ]
    candidates = [
        {
            "candidate_id": "candidate_a_split_view_decision_evidence_pane",
            "label": "Split view: decision rail + evidence/preview pane",
            "pattern_family": "split_view_master_detail",
            "status": "selected",
            "score": 47,
            "primary_strength": "Keeps the active recommendation and the trust evidence visible at the same time without turning evidence into a closet.",
            "primary_weakness": "Needs responsive behavior so the right pane stacks cleanly on narrow screens.",
            "evidence_handling": "evidence_preview_pane",
            "card_bloat_risk": "low",
        },
        {
            "candidate_id": "candidate_b_spine_detail_active_path",
            "label": "Spine + detail: active path and selected node",
            "pattern_family": "spine_detail",
            "status": "runner_up",
            "score": 42,
            "primary_strength": "Shows the route through hold, real input, and YMM4 observation without making every option equal.",
            "primary_weakness": "Can become process-heavy if the user only needs a simple current recommendation.",
            "evidence_handling": "selected_node_detail_with_source_links",
            "card_bloat_risk": "medium",
        },
        {
            "candidate_id": "candidate_c_service_entry_decision_board",
            "label": "Start page / service entry + decision board",
            "pattern_family": "service_entry",
            "status": "rejected",
            "score": 35,
            "primary_strength": "Strong explanation of purpose and first-time user orientation.",
            "primary_weakness": "Still tends to compare choices side by side and can slide back into card-board layout.",
            "evidence_handling": "summary_then_secondary_panel",
            "card_bloat_risk": "medium",
        },
        {
            "candidate_id": "candidate_d_wizard_step_flow",
            "label": "Wizard / step-by-step decision flow",
            "pattern_family": "wizard",
            "status": "rejected_after_weak_pass",
            "score": 34,
            "primary_strength": "Good for novice input gathering and exactly-one outcome.",
            "primary_weakness": "The weak-pass prototype showed that wizard language can over-trim evidence and hide trust checks.",
            "evidence_handling": "deferred_details",
            "card_bloat_risk": "medium",
        },
        {
            "candidate_id": "candidate_e_current_card_drawer_guided_flow",
            "label": "Current card/drawer guided flow",
            "pattern_family": "card_drawer",
            "status": "weak_pass_do_not_extend",
            "score": 26,
            "primary_strength": "Compact, local, dark, and already validates exactly-one recommendation.",
            "primary_weakness": "Cards make options look like equal objects, and the evidence drawer becomes a storage closet.",
            "evidence_handling": "generic_drawer",
            "card_bloat_risk": "high",
        },
        {
            "candidate_id": "candidate_f_command_center_cockpit",
            "label": "Command-center cockpit",
            "pattern_family": "dashboard_cockpit",
            "status": "rejected",
            "score": 24,
            "primary_strength": "Power users can scan many statuses quickly.",
            "primary_weakness": "It centers artifact inventory and repeats the original cockpit weakness for novice decision making.",
            "evidence_handling": "status_rows_and_details",
            "card_bloat_risk": "high",
        },
    ]
    return {
        "schema_version": "layout_second_pass_candidate_matrix.v1",
        "artifact_id": artifact_id,
        "status": "ready",
        "evaluated_guided_flow_verdict": state["evaluated_guided_flow"]["verdict"],
        "criteria": criteria,
        "research_basis": state["research_basis"],
        "candidates": candidates,
        "selected_candidate_ids": [SELECTED_CANDIDATE],
        "winning_candidate": SELECTED_CANDIDATE,
        "decision": "Implement a split-view decision rail plus evidence/preview pane next; do not keep extending the card/drawer guided flow.",
        "test_strategy": [
            "user-situation-first",
            "visible active path",
            "evidence is available without becoming a junk drawer",
            "internal artifact IDs are secondary",
            "gate details are bounded",
            "exactly one recommended next step",
            "no external dependencies",
            "no production/YMM4/public overclaims",
        ],
        "boundary_flags": state["boundary_flags"],
    }


def _evidence_handling(state: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "layout_second_pass_evidence_handling.v1",
        "status": "ready",
        "finding": "Evidence must be visible beside the decision when it explains why the recommended next lane is safe.",
        "current_problem": "The current evidence drawer is not a generic drawer by intent, but in practice it behaves like a storage closet because trust evidence is hidden after the primary recommendation.",
        "recommended_model": "right_side_evidence_preview_pane",
        "required_visible_evidence": [
            "current checked state",
            "one recommendation rationale",
            "source surface readiness summary",
            "closed gate context",
        ],
        "secondary_only_records": [row["record_id"] for row in _list(state.get("source_records"))],
        "boundary_flags": state["boundary_flags"],
    }


def _card_bloat_risk(state: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "layout_second_pass_card_bloat_risk.v1",
        "status": "ready",
        "headline": "card-bloat risk: high for the current card/drawer pattern",
        "risk_drivers": [
            "Each new evidence source becomes either another card or another drawer row.",
            "Cards make gated alternatives look equally actionable.",
            "Drawer-only provenance hides the reason the default recommendation should be trusted.",
            "Future episodes will add more surfaces, which amplifies card rows faster than decision clarity.",
        ],
        "recommended_mitigation": "Use a split view with one decision rail and one evidence pane; add rows inside the pane only when they support the active recommendation.",
        "boundary_flags": state["boundary_flags"],
    }


def _manifest(
    artifact_id: str,
    state: dict[str, Any],
    matrix: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "layout_second_pass_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-review-layout-second-pass",
        "status": "layout_second_pass_ready_local_offline",
        "output_dir": _relpath(output_root, repo_root),
        "files": {name: _relpath(output_root / name, repo_root) for name in REQUIRED_LAYOUT_SECOND_PASS_FILES},
        "evaluated_guided_flow": state["evaluated_guided_flow"],
        "source_records": state["source_records"],
        "primary_human_review": _relpath(output_root / "split_view_benchmark.md", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "candidate_wireframes": _relpath(output_root / "candidate_wireframes_second_pass.html", repo_root),
        "selected_candidate": matrix["winning_candidate"],
        "production_ui_replaced": False,
        "boundary_flags": state["boundary_flags"],
        "next_action": state["next_action"],
    }


def _render_guided_flow_diagnosis(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Current Guided Flow Diagnosis",
            "",
            f"Evaluated prototype: `{state['evaluated_guided_flow']['path']}`",
            "",
            "Verdict: weak_pass_evaluated_prototype.",
            "",
            "## What Improved",
            "",
            "- The page starts from the user's situation instead of a project inventory.",
            "- It keeps one current recommendation and preserves closed gates.",
            "- It is local, dark-mode friendly, and validated without external dependencies.",
            "",
            "## What Still Fails",
            "",
            "- The page is still built from card rows, so alternatives continue to look like peer objects.",
            "- Evidence is available but hidden behind a drawer, which weakens trust in the recommendation.",
            "- The primary view may over-trim the details that explain why hold is the current safe lane.",
            "- The model will amplify as future episodes add source surfaces, gates, and reviewer notes.",
            "",
            "## Second-Pass Requirement",
            "",
            "The next implementation target should keep the active decision and supporting evidence visible together while keeping internal paths and raw records secondary.",
            "",
        ]
    )


def _render_split_view_benchmark(state: dict[str, Any], matrix: dict[str, Any]) -> str:
    rows = [
        "| candidate | score | evidence model | card-bloat risk | verdict |",
        "|---|---:|---|---|---|",
    ]
    for candidate in _list(matrix.get("candidates")):
        if isinstance(candidate, dict):
            rows.append(
                f"| {candidate.get('label')} | {candidate.get('score')} | {candidate.get('evidence_handling')} | {candidate.get('card_bloat_risk')} | {candidate.get('status')} |"
            )
    return "\n".join(
        [
            "# Split-View Benchmark",
            "",
            "split view: decision rail + evidence/preview pane is the strongest next model because it keeps the user's current situation, active recommendation, evidence preview, and closed gate context visible together.",
            "",
            "## Research Basis Applied",
            "",
            "- Dashboard/status-board layouts are useful for monitoring, but this task is choosing a next action.",
            "- Progressive disclosure is useful only when secondary information is genuinely secondary.",
            "- Task lists/checklists are heavier than this single next-lane decision requires.",
            "- Split-view, master-detail, and spine-detail patterns better support simultaneous decision and evidence viewing.",
            "- Card grids are suspect unless each card is a primary actionable object and dependency flow remains visible.",
            "",
            "## Candidate Comparison",
            "",
            *rows,
            "",
            "Selected next implementation target:",
            "",
            f"`{matrix.get('winning_candidate')}`",
            "",
        ]
    )


def _render_evidence_handling_report(evidence: dict[str, Any]) -> str:
    lines = [
        "# Evidence Handling Report",
        "",
        "The evidence model should be not a generic drawer. It should be a visible evidence preview pane that explains why the active recommendation is safe.",
        "",
        "## Current Problem",
        "",
        str(evidence.get("current_problem")),
        "",
        "## Recommended Evidence Model",
        "",
        str(evidence.get("recommended_model")),
        "",
        "## Evidence That Belongs Beside The Decision",
        "",
    ]
    for item in _list(evidence.get("required_visible_evidence")):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Records That Stay Secondary",
            "",
        ]
    )
    for item in _list(evidence.get("secondary_only_records")):
        lines.append(f"- `{item}`")
    return "\n".join(lines) + "\n"


def _render_card_bloat_report(card_bloat: dict[str, Any]) -> str:
    lines = [
        "# Card-Bloat Risk Report",
        "",
        str(card_bloat.get("headline")),
        "",
        "## Risk Drivers",
        "",
    ]
    for item in _list(card_bloat.get("risk_drivers")):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Mitigation",
            "",
            str(card_bloat.get("recommended_mitigation")),
            "",
        ]
    )
    return "\n".join(lines)


def _render_wireframes_html(state: dict[str, Any], matrix: dict[str, Any]) -> str:
    candidates = "\n".join(_render_candidate(candidate) for candidate in _list(matrix.get("candidates")))
    gates = "\n".join(f"<span>{_escape(flag)}</span>" for flag in REQUIRED_BOUNDARY_FLAGS)
    return f"""<!doctype html>
<html lang="en" data-layout-second-pass="true" data-selected-candidate="{SELECTED_CANDIDATE}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Layout Second Pass</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #101113;
      --panel: #1b1d20;
      --panel2: #24282e;
      --panel3: #14171b;
      --text: #f0eee8;
      --muted: #b8b5ad;
      --line: #4b5563;
      --accent: #67e8f9;
      --selected: #a7f3d0;
      --warn: #facc15;
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #eef2f0;
        --panel: #f4f1ea;
        --panel2: #e4e8e6;
        --panel3: #d8dfdc;
        --text: #1f2420;
        --muted: #5f6661;
        --line: #bac3bd;
        --accent: #0e7490;
        --selected: #166534;
        --warn: #8a5a00;
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--text); font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; letter-spacing: 0; }}
    main {{ width: min(1220px, calc(100% - 32px)); margin: 0 auto; padding: 22px 0 34px; }}
    header {{ display: grid; gap: 8px; padding: 16px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; }}
    h1 {{ margin: 0; font-size: clamp(1.35rem, 2.4vw, 2rem); letter-spacing: 0; }}
    h2 {{ margin: 0 0 8px; font-size: 1rem; letter-spacing: 0; }}
    h3 {{ margin: 0; font-size: 0.93rem; letter-spacing: 0; }}
    p {{ margin: 0; color: var(--muted); line-height: 1.45; }}
    .candidate-grid {{ margin-top: 14px; display: grid; gap: 14px; }}
    .candidate {{ display: grid; gap: 10px; padding: 14px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; }}
    .candidate[data-status="selected"] {{ border-color: var(--selected); box-shadow: 0 0 0 2px rgba(167, 243, 208, 0.16); }}
    .candidate-layout {{ display: grid; grid-template-columns: minmax(220px, 0.9fr) minmax(300px, 1.35fr); gap: 10px; }}
    .pane, .block {{ padding: 10px; border: 1px solid var(--line); border-radius: 6px; background: var(--panel2); min-height: 40px; }}
    .pane[data-right-pane] {{ border-color: var(--accent); }}
    .stack {{ display: grid; gap: 8px; }}
    .spine {{ display: grid; grid-template-columns: 16px 1fr; gap: 8px; align-items: start; }}
    .node {{ width: 12px; height: 12px; margin-top: 4px; border-radius: 999px; background: var(--accent); }}
    .tag {{ width: fit-content; padding: 4px 8px; border-radius: 999px; background: var(--panel3); color: var(--accent); font-size: 0.78rem; font-weight: 700; }}
    .gate-strip {{ margin-top: 14px; display: flex; flex-wrap: wrap; gap: 8px; padding: 10px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; }}
    .gate-strip span {{ padding: 5px 8px; border-radius: 999px; background: var(--panel2); color: var(--muted); font-size: 0.78rem; }}
    @media (max-width: 850px) {{
      main {{ width: min(100% - 20px, 1220px); padding-top: 12px; }}
      .candidate-layout {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Episode 002 Layout Second Pass</h1>
      <p>Low-fidelity local wireframes comparing split-view, spine-detail, service entry, wizard, current card/drawer, and cockpit patterns.</p>
    </header>
    <section class="candidate-grid">{candidates}</section>
    <section class="gate-strip" aria-label="closed boundaries">{gates}</section>
  </main>
</body>
</html>
"""


def _render_candidate(candidate: Any) -> str:
    if not isinstance(candidate, dict):
        return ""
    candidate_id = str(candidate.get("candidate_id"))
    status = str(candidate.get("status"))
    if candidate_id == "candidate_a_split_view_decision_evidence_pane":
        layout = "\n".join(
            [
                '<div class="pane stack" data-left-pane>',
                "<h3>Decision rail</h3>",
                '<div class="block">Current user situation</div>',
                '<div class="block">Active decision</div>',
                '<div class="block">Recommended next step</div>',
                "</div>",
                '<div class="pane stack" data-right-pane>',
                "<h3>Evidence preview pane</h3>",
                '<div class="block">Source readiness summary</div>',
                '<div class="block">Gate context</div>',
                '<div class="block">Source index summary</div>',
                "</div>",
            ]
        )
    elif candidate_id == "candidate_b_spine_detail_active_path":
        layout = "\n".join(
            [
                '<div class="pane stack">',
                "<h3>Active path spine</h3>",
                '<div class="spine"><span class="node"></span><span>Hold now</span></div>',
                '<div class="spine"><span class="node"></span><span>Real input later</span></div>',
                '<div class="spine"><span class="node"></span><span>YMM4 observation gate</span></div>',
                "</div>",
                '<div class="pane stack">',
                "<h3>Selected node detail</h3>",
                '<div class="block">Recommendation rationale</div>',
                '<div class="block">Relevant evidence links</div>',
                '<div class="block">Bounded gate notes</div>',
                "</div>",
            ]
        )
    elif candidate_id == "candidate_e_current_card_drawer_guided_flow":
        layout = "\n".join(
            [
                '<div class="pane stack">',
                "<h3>Current card/drawer pattern</h3>",
                '<div class="block">Three situation cards</div>',
                '<div class="block">Three outcome cards</div>',
                "</div>",
                '<div class="pane stack">',
                "<h3>Critique</h3>",
                '<div class="block">Evidence hidden after the decision</div>',
                '<div class="block">Cards multiply as sources grow</div>',
                "</div>",
            ]
        )
    else:
        layout = "\n".join(
            [
                '<div class="pane stack">',
                f"<h3>{_escape(candidate.get('pattern_family'))}</h3>",
                '<div class="block">Primary decision area</div>',
                '<div class="block">Alternative path area</div>',
                "</div>",
                '<div class="pane stack">',
                "<h3>Evidence and gates</h3>",
                '<div class="block">Evidence summary</div>',
                '<div class="block">Boundary summary</div>',
                "</div>",
            ]
        )
    return "\n".join(
        [
            f'<article class="candidate" data-candidate="{_escape(candidate_id)}" data-status="{_escape(status)}">',
            f'  <span class="tag">{_escape(status)}</span>',
            f"  <h2>{_escape(candidate.get('label'))}</h2>",
            f"  <p>{_escape(candidate.get('primary_strength'))}</p>",
            f'  <div class="candidate-layout">{layout}</div>',
            f"  <p>{_escape(candidate.get('primary_weakness'))}</p>",
            "</article>",
        ]
    )


def _render_wireframes_md(matrix: dict[str, Any]) -> str:
    lines = [
        "# Candidate Wireframes Second Pass",
        "",
        f"Selected next implementation target: `{matrix.get('winning_candidate')}`.",
        "",
    ]
    for candidate in _list(matrix.get("candidates")):
        if not isinstance(candidate, dict):
            continue
        lines.extend(
            [
                f"## {candidate.get('label')}",
                "",
                f"- status: {candidate.get('status')}",
                f"- pattern family: {candidate.get('pattern_family')}",
                f"- evidence handling: {candidate.get('evidence_handling')}",
                f"- card-bloat risk: {candidate.get('card_bloat_risk')}",
                f"- strength: {candidate.get('primary_strength')}",
                f"- weakness: {candidate.get('primary_weakness')}",
                "",
            ]
        )
    return "\n".join(lines)


def _render_final_recommendation(state: dict[str, Any], matrix: dict[str, Any]) -> str:
    strategy = "\n".join(f"- {item}" for item in _list(matrix.get("test_strategy")))
    return "\n".join(
        [
            "# Final Layout Recommendation",
            "",
            f"selected_candidate: {SELECTED_CANDIDATE}",
            "",
            "## Why",
            "",
            "Select split view because the current guided flow proved the value of a user-situation-first entry, but the card/drawer structure hides evidence that the user needs in order to trust the recommendation.",
            "",
            "## Next Implementation Target",
            "",
            "Build a split-view prototype with a left decision rail and a right evidence/preview pane. The rail should hold current situation, active decision, and one recommended next step. The pane should hold evidence preview, source readiness, and bounded gate context.",
            "",
            "## Do Not Carry Forward",
            "",
            "- Do not keep a generic evidence drawer as the only source location.",
            "- Do not turn each future source surface into another top-level card.",
            "- Do not return to cockpit inventory as the first screen.",
            "",
            "## Test Strategy",
            "",
            strategy,
            "",
            "This recommendation is a research checkpoint, not a production UI replacement.",
            "",
        ]
    )


def _render_review_checklist(state: dict[str, Any], matrix: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Layout Second-Pass Review Checklist",
            "",
            "- Read `split_view_benchmark.md` for the candidate comparison.",
            "- Open `candidate_wireframes_second_pass.html` for the low-fidelity visual comparison.",
            "- Confirm split view is the single selected next implementation target.",
            "- Confirm the current guided flow is treated as weak-pass evaluated prototype.",
            "- Confirm evidence is visible in the selected model without becoming a generic drawer.",
            "- Confirm this packet does not replace the production UI.",
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
            "# Layout Second-Pass Limitations",
            "",
            "This packet is research and low-fidelity wireframing only.",
            "",
            "Not performed:",
            "",
            "- production UI replacement",
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
            f"Primary research file: `{state.get('primary_human_review')}`",
            "",
        ]
    )


def _record(record_id: str, label: str, path: Path, group: str, repo_root: Path) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "label": label,
        "source_group": group,
        "repo_relative_path": _relpath(path, repo_root),
        "role": "source_record",
        "display_zone": "secondary_source_records",
        "exists": path.exists(),
    }


def _boundary_flags(guided_state: dict[str, Any], layout_manifest: dict[str, Any]) -> dict[str, bool]:
    guided_flags = _dict(guided_state.get("boundary_flags"))
    layout_flags = _dict(layout_manifest.get("boundary_flags"))
    return {
        flag: guided_flags.get(flag) is True or layout_flags.get(flag) is True
        for flag in REQUIRED_BOUNDARY_FLAGS
    }


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


def _forbidden_true_claims(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
            for claim in FORBIDDEN_TRUE_CLAIMS:
                if claim in text:
                    hits.append(f"{path.name}:{claim}")
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
