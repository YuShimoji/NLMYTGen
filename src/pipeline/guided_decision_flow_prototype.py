"""Guided decision flow prototype for episode 002 review."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIRNAME = "guided_decision_flow_prototype"
DEFAULT_ARTIFACT_ID = "episode_002_guided_decision_flow_prototype_v1"
DEFAULT_LAYOUT_RESEARCH_DIRNAME = "review_layout_research"
DEFAULT_COCKPIT_DIRNAME = "review_cockpit_compact"
DEFAULT_REVIEWER_DIRNAME = "surface_alignment_review_packet"

REQUIRED_GUIDED_DECISION_FILES = (
    "guided_flow_manifest.json",
    "guided_decision_flow.html",
    "guided_decision_flow.md",
    "flow_state.json",
    "recommendation_engine_readback.json",
    "evidence_drawer_index.json",
    "decision_outcomes.json",
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
    '"real_transcript_exists": true',
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

TEMPORARY_COPY_MARKERS = (
    "only look here",
    "just read this",
    "this is only for now",
    "temporary note",
)

INTERNAL_PRIMARY_MARKERS = (
    "production_pilots/",
    "review_layout_research",
    "review_cockpit_compact",
    "surface_alignment_review_packet",
    "focused_review_brief",
    "factory_seed_dry_run_002",
    "candidate_b_guided_decision_flow",
    "episode_002_",
    "real_input_replacement",
    "actual_yymm4_import_observation_no_render",
    "hold_review_later",
    "dry_run",
    "sample_fixture_not_real",
)


def build_guided_decision_flow_prototype(
    *,
    package_dir: str | Path,
    layout_research_dir: str | Path | None = None,
    cockpit_dir: str | Path | None = None,
    reviewer_packet_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
    explicit_yymm4_observation: bool = False,
) -> dict[str, Any]:
    """Build the local guided decision flow prototype."""
    source_root = Path(package_dir)
    layout_root = Path(layout_research_dir) if layout_research_dir else source_root / DEFAULT_LAYOUT_RESEARCH_DIRNAME
    cockpit_root = Path(cockpit_dir) if cockpit_dir else source_root / DEFAULT_COCKPIT_DIRNAME
    reviewer_root = Path(reviewer_packet_dir) if reviewer_packet_dir else source_root / DEFAULT_REVIEWER_DIRNAME
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root, layout_root, cockpit_root, reviewer_root)
    payloads = _load_payloads(paths)
    state = _flow_state(
        artifact_id=artifact_id,
        source_root=source_root,
        layout_root=layout_root,
        cockpit_root=cockpit_root,
        reviewer_root=reviewer_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        payloads=payloads,
        explicit_yymm4_observation=explicit_yymm4_observation,
    )
    outcomes = _decision_outcomes(artifact_id, state)
    recommendation = _recommendation_readback(artifact_id, state, outcomes)
    evidence = _evidence_drawer_index(artifact_id, state, paths, repo_root)
    manifest = _manifest(artifact_id, state, outcomes, output_root, repo_root)

    _write_json(output_root / "guided_flow_manifest.json", manifest)
    _write_json(output_root / "flow_state.json", state)
    _write_json(output_root / "decision_outcomes.json", outcomes)
    _write_json(output_root / "recommendation_engine_readback.json", recommendation)
    _write_json(output_root / "evidence_drawer_index.json", evidence)
    _write_text(output_root / "guided_decision_flow.html", _render_html(state, outcomes, evidence))
    _write_text(output_root / "guided_decision_flow.md", _render_markdown(state, outcomes, evidence))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state))
    _write_text(output_root / "limitations.md", _render_limitations(state))

    readback = validate_guided_decision_flow_prototype(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_guided_decision_flow_prototype(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_guided_decision_flow_prototype(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated guided decision flow prototype."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_GUIDED_DECISION_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["guided_flow_manifest.json"])
    flow_state = _load_json_if_present(files["flow_state.json"])
    recommendation = _load_json_if_present(files["recommendation_engine_readback.json"])
    evidence = _load_json_if_present(files["evidence_drawer_index.json"])
    outcomes = _load_json_if_present(files["decision_outcomes.json"])
    json_payloads = {
        "guided_flow_manifest": manifest,
        "flow_state": flow_state,
        "recommendation_engine_readback": recommendation,
        "evidence_drawer_index": evidence,
        "decision_outcomes": outcomes,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["guided_flow_manifest"]
    flow_state = json_payloads["flow_state"]
    recommendation = json_payloads["recommendation_engine_readback"]
    evidence = json_payloads["evidence_drawer_index"]
    outcomes = json_payloads["decision_outcomes"]

    if manifest.get("artifact_kind") != "episode-guided-decision-flow-prototype":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "guided_decision_flow_prototype_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")
    if manifest.get("selected_candidate") != "candidate_b_guided_decision_flow":
        failed_checks.append("selected_candidate_mismatch")

    boundary_flags = _dict(manifest.get("boundary_flags"))
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")

    recommended = [
        row
        for row in _list(outcomes.get("outcomes"))
        if isinstance(row, dict) and row.get("recommended_for_current_state") is True
    ]
    if len(recommended) != 1:
        failed_checks.append("recommended_outcome_count_not_one")
    elif recommended[0].get("outcome_id") != flow_state.get("default_recommendation"):
        failed_checks.append("recommended_outcome_mismatch")

    if recommendation.get("exactly_one_recommendation") is not True:
        failed_checks.append("recommendation_exactly_one_false")
    if recommendation.get("default_recommendation") != flow_state.get("default_recommendation"):
        failed_checks.append("recommendation_default_mismatch")
    if flow_state.get("default_recommendation") != "hold_review_later" and flow_state.get("real_input_available") is not True and flow_state.get("explicit_yymm4_observation_selected") is not True:
        failed_checks.append("dry_run_default_recommendation_unexpected")
    if not flow_state.get("primary_user_question"):
        failed_checks.append("primary_user_question_missing")

    source_records = _list(evidence.get("source_records"))
    source_records_secondary = bool(source_records) and all(
        isinstance(row, dict)
        and row.get("role") == "secondary_source_record"
        and row.get("display_zone") == "evidence_drawer"
        for row in source_records
    )
    if not source_records_secondary:
        failed_checks.append("source_records_not_secondary")

    html_text = files["guided_decision_flow.html"].read_text(encoding="utf-8") if files["guided_decision_flow.html"].exists() else ""
    markdown_text = files["guided_decision_flow.md"].read_text(encoding="utf-8") if files["guided_decision_flow.md"].exists() else ""
    primary_text = _primary_visible_text(html_text)
    internal_primary_hits = [
        marker for marker in INTERNAL_PRIMARY_MARKERS if marker.lower() in primary_text.lower()
    ]
    if internal_primary_hits:
        failed_checks.extend(f"internal_artifact_marker_in_primary_copy:{hit}" for hit in internal_primary_hits)
    if "color-scheme: dark light" not in html_text:
        failed_checks.append("dark_color_scheme_missing")
    if "prefers-color-scheme" not in html_text:
        failed_checks.append("prefers_color_scheme_missing")
    if "#ffffff" in html_text.lower() or "#fff" in html_text.lower():
        failed_checks.append("pure_white_background_marker_present")
    if "data-default-recommendation=\"hold_review_later\"" not in html_text and flow_state.get("default_recommendation") == "hold_review_later":
        failed_checks.append("default_recommendation_marker_missing")
    if "data-secondary-records" not in html_text:
        failed_checks.append("secondary_records_drawer_missing")
    if "Hold and review later" not in html_text:
        failed_checks.append("hold_recommendation_visible_label_missing")
    if len(markdown_text.splitlines()) > 180:
        failed_checks.append("markdown_too_long")

    external_refs = _external_refs_in_files([path for name, path in files.items() if name != "validation_readback.json"])
    forbidden_hits = _forbidden_true_claims(root)
    temporary_hits = _temporary_copy_hits([files["guided_decision_flow.html"], files["guided_decision_flow.md"]])
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "exactly_one_recommendation": len(recommended) == 1 and recommendation.get("exactly_one_recommendation") is True,
        "default_recommendation": flow_state.get("default_recommendation"),
        "source_records_secondary": source_records_secondary,
        "internal_artifact_ids_in_primary_copy": internal_primary_hits,
        "external_dependency_status": "none_found" if not external_refs else "found",
        "dark_mode_markers_present": "color-scheme: dark light" in html_text and "prefers-color-scheme" in html_text,
        "pure_white_background_absent": "#ffffff" not in html_text.lower() and "#fff" not in html_text.lower(),
        "forbidden_true_claims_absent": not forbidden_hits,
        "temporary_copy_absent": not temporary_hits,
        "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS),
        "primary_question_present": bool(flow_state.get("primary_user_question")),
    }
    return {
        "schema_version": "guided_decision_flow_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "primary_user_question": flow_state.get("primary_user_question"),
        "default_recommendation": flow_state.get("default_recommendation"),
        "alternatives": flow_state.get("alternative_paths"),
        "exactly_one_recommendation": checks["exactly_one_recommendation"],
        "source_records_secondary": source_records_secondary,
        "internal_artifact_ids_in_primary_copy": internal_primary_hits,
        "gate_integrity_status": "closed_preserved" if checks["boundary_flags_present"] and checks["forbidden_true_claims_absent"] else "needs_review",
        "primary_human_review": str(root / "guided_decision_flow.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "recommendation_engine_readback": str(root / "recommendation_engine_readback.json"),
        "markdown_fallback": str(root / "guided_decision_flow.md"),
        "launcher_command": f'start "" "{(root / "guided_decision_flow.html").resolve()}"',
        "access_state": "verified_present" if (root / "guided_decision_flow.html").exists() else "missing",
        "next_action": manifest.get("next_action"),
    }


def _input_paths(source_root: Path, layout_root: Path, cockpit_root: Path, reviewer_root: Path) -> dict[str, Path]:
    return {
        "layout_manifest": layout_root / "layout_research_manifest.json",
        "layout_decision_matrix": layout_root / "layout_decision_matrix.json",
        "layout_principles": layout_root / "layout_principles.json",
        "layout_recommendation": layout_root / "final_layout_recommendation.md",
        "layout_wireframes": layout_root / "candidate_wireframes.html",
        "layout_validation": layout_root / "validation_readback.json",
        "cockpit_html": cockpit_root / "review_cockpit.html",
        "cockpit_state": cockpit_root / "cockpit_state.json",
        "cockpit_validation": cockpit_root / "validation_readback.json",
        "aligned_story": reviewer_root / "aligned_review_story.md",
        "reviewer_validation": reviewer_root / "validation_readback.json",
        "gui_dashboard": source_root / "gui_dashboard_panel" / "dashboard_panel_preview.html",
        "import_preview": source_root / "ymm4_import_preview_pack" / "import_preview_panel.md",
        "thumbnail_proof": source_root / "thumbnail_visual_proof_pack" / "thumbnail_visual_proof.html",
        "real_input_dir": source_root / "transcript_substitution_readiness" / "real_input",
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    payloads: dict[str, Any] = {}
    for name, path in paths.items():
        if path.suffix == ".json" and path.exists():
            payloads[name] = _load_json(path)
    return payloads


def _flow_state(
    *,
    artifact_id: str,
    source_root: Path,
    layout_root: Path,
    cockpit_root: Path,
    reviewer_root: Path,
    output_root: Path,
    repo_root: Path,
    paths: dict[str, Path],
    payloads: dict[str, Any],
    explicit_yymm4_observation: bool,
) -> dict[str, Any]:
    layout_manifest = _dict(payloads.get("layout_manifest"))
    layout_matrix = _dict(payloads.get("layout_decision_matrix"))
    cockpit_state = _dict(payloads.get("cockpit_state"))
    boundary_flags = _boundary_flags(layout_manifest, cockpit_state)
    real_input_files = _real_input_files(paths["real_input_dir"], repo_root)
    real_input_available = bool(real_input_files)
    default_recommendation = _select_recommendation(real_input_available, explicit_yymm4_observation)
    selected_candidate = (
        layout_matrix.get("winning_candidate")
        or layout_manifest.get("selected_candidate")
        or "candidate_b_guided_decision_flow"
    )
    return {
        "schema_version": "guided_decision_flow_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-guided-decision-flow-prototype",
        "status": "guided_decision_flow_prototype_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "layout_research_dir": _relpath(layout_root, repo_root),
        "cockpit_dir": _relpath(cockpit_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "selected_candidate": selected_candidate,
        "layout_research_status": layout_manifest.get("status"),
        "evaluated_prior_prototype": layout_manifest.get("evaluated_prototype"),
        "primary_user_question": "What situation are you in right now?",
        "user_situation_checks": [
            {
                "check_id": "reviewed_local_source_or_transcript",
                "question": "Do you have reviewed local source or transcript material for this episode?",
                "current_checked_answer": real_input_available,
                "current_answer_label": "Yes" if real_input_available else "No",
                "if_yes_recommendation": "real_input_replacement",
            },
            {
                "check_id": "explicit_yymm4_import_observation",
                "question": "Do you need to inspect YMM4 import behavior now without rendering or publishing?",
                "current_checked_answer": explicit_yymm4_observation,
                "current_answer_label": "Yes" if explicit_yymm4_observation else "No",
                "if_yes_recommendation": "actual_yymm4_import_observation_no_render",
            },
            {
                "check_id": "current_story_understanding_check",
                "question": "Are you only checking whether the current sample story is understandable?",
                "current_checked_answer": not real_input_available and not explicit_yymm4_observation,
                "current_answer_label": "Yes" if not real_input_available and not explicit_yymm4_observation else "No",
                "if_yes_recommendation": "hold_review_later",
            },
        ],
        "real_input_dir": _relpath(paths["real_input_dir"], repo_root),
        "real_input_files": real_input_files,
        "real_input_available": real_input_available,
        "explicit_yymm4_observation_selected": explicit_yymm4_observation,
        "default_recommendation": default_recommendation,
        "alternative_paths": [
            "real_input_replacement",
            "actual_yymm4_import_observation_no_render",
            "hold_review_later",
        ],
        "default_reason": _default_reason(default_recommendation, real_input_available, explicit_yymm4_observation),
        "source_record_policy": "secondary_records_only",
        "source_records_display_zone": "evidence_drawer",
        "boundary_flags": boundary_flags,
        "closed_gate_status": {
            "real_transcript_status": "available" if real_input_available else "blocked_by_real_input",
            "yymm4_import_status": "explicit_observation_selected_no_render" if explicit_yymm4_observation else "no_yymm4_import",
            "yymm4_render_status": "yymm4_render_closed",
            "public_upload_status": "public_upload_closed",
            "rights_public_ready_status": "rights_boundary",
            "thumbnail_approval_status": "thumbnail_context_only",
            "production_status": "not_production_ready",
        },
        "primary_human_review": _relpath(output_root / "guided_decision_flow.html", repo_root),
        "markdown_fallback": _relpath(output_root / "guided_decision_flow.md", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "recommendation_engine_readback": _relpath(output_root / "recommendation_engine_readback.json", repo_root),
        "next_action": "Open guided_decision_flow.html and review the single default recommendation before choosing a gated next path.",
    }


def _decision_outcomes(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    default_id = str(state.get("default_recommendation"))
    outcomes = [
        {
            "outcome_id": "real_input_replacement",
            "label": "Real input replacement",
            "status": "gated_until_reviewed_local_material_exists"
            if not state.get("real_input_available")
            else "recommended",
            "recommended_for_current_state": default_id == "real_input_replacement",
            "use_when": "Reviewed local source or transcript material is available for this episode.",
            "effect": "Moves the episode from sample review toward real content while keeping YMM4 and public gates closed.",
            "required_next_input": "Verified local source/transcript material with provenance.",
        },
        {
            "outcome_id": "actual_yymm4_import_observation_no_render",
            "label": "YMM4 import observation without render",
            "status": "gated_until_explicit_observation_is_selected"
            if not state.get("explicit_yymm4_observation_selected")
            else "recommended",
            "recommended_for_current_state": default_id == "actual_yymm4_import_observation_no_render",
            "use_when": "A human explicitly chooses to inspect import behavior now.",
            "effect": "Allows a manual import observation only; it does not render, publish, or create a production project claim.",
            "required_next_input": "Explicit human decision to perform the YMM4 observation outside this prototype.",
        },
        {
            "outcome_id": "hold_review_later",
            "label": "Hold and review later",
            "status": "recommended" if default_id == "hold_review_later" else "available_hold",
            "recommended_for_current_state": default_id == "hold_review_later",
            "use_when": "No reviewed local real material is available and no import observation has been selected.",
            "effect": "Keeps the current sample-backed review as a local record without crossing any production gate.",
            "required_next_input": "None.",
        },
    ]
    return {
        "schema_version": "guided_decision_outcomes.v1",
        "artifact_id": artifact_id,
        "status": "ready",
        "current_state": {
            "real_input_available": state.get("real_input_available"),
            "explicit_yymm4_observation_selected": state.get("explicit_yymm4_observation_selected"),
            "default_recommendation": default_id,
        },
        "outcomes": outcomes,
        "recommended_outcome_ids": [row["outcome_id"] for row in outcomes if row["recommended_for_current_state"]],
        "boundary_flags": state.get("boundary_flags"),
    }


def _recommendation_readback(
    artifact_id: str,
    state: dict[str, Any],
    outcomes: dict[str, Any],
) -> dict[str, Any]:
    recommended_ids = _list(outcomes.get("recommended_outcome_ids"))
    return {
        "schema_version": "guided_recommendation_engine_readback.v1",
        "artifact_id": artifact_id,
        "status": "passed" if len(recommended_ids) == 1 else "failed",
        "primary_user_question": state.get("primary_user_question"),
        "default_recommendation": state.get("default_recommendation"),
        "recommended_outcome_ids": recommended_ids,
        "exactly_one_recommendation": len(recommended_ids) == 1,
        "default_reason": state.get("default_reason"),
        "current_inputs": {
            "real_input_available": state.get("real_input_available"),
            "real_input_files": state.get("real_input_files"),
            "explicit_yymm4_observation_selected": state.get("explicit_yymm4_observation_selected"),
            "selected_candidate": state.get("selected_candidate"),
            "source_record_policy": state.get("source_record_policy"),
        },
        "alternatives": [
            row.get("outcome_id")
            for row in _list(outcomes.get("outcomes"))
            if isinstance(row, dict) and row.get("recommended_for_current_state") is not True
        ],
        "gate_integrity_status": "closed_preserved",
    }


def _evidence_drawer_index(
    artifact_id: str,
    state: dict[str, Any],
    paths: dict[str, Path],
    repo_root: Path,
) -> dict[str, Any]:
    records = [
        _record("layout_research_manifest", "Layout research manifest", paths["layout_manifest"], "layout_research", repo_root),
        _record("layout_decision_matrix", "Layout decision matrix", paths["layout_decision_matrix"], "layout_research", repo_root),
        _record("layout_principles", "Layout principles", paths["layout_principles"], "layout_research", repo_root),
        _record("layout_final_recommendation", "Layout final recommendation", paths["layout_recommendation"], "layout_research", repo_root),
        _record("layout_wireframes", "Layout wireframes", paths["layout_wireframes"], "layout_research", repo_root),
        _record("compact_review_cockpit", "Compact review cockpit", paths["cockpit_html"], "prior_prototype", repo_root),
        _record("aligned_review_story", "Aligned review story", paths["aligned_story"], "reviewer_packet", repo_root),
        _record("gui_dashboard_panel", "GUI dashboard panel", paths["gui_dashboard"], "episode_surface", repo_root),
        _record("import_preview_panel", "YMM4 import preview panel", paths["import_preview"], "episode_surface", repo_root),
        _record("thumbnail_visual_proof", "Thumbnail visual proof", paths["thumbnail_proof"], "episode_surface", repo_root),
    ]
    return {
        "schema_version": "guided_evidence_drawer_index.v1",
        "artifact_id": artifact_id,
        "status": "ready",
        "source_record_policy": state.get("source_record_policy"),
        "primary_surface": state.get("primary_human_review"),
        "source_records": records,
        "boundary_flags": state.get("boundary_flags"),
    }


def _manifest(
    artifact_id: str,
    state: dict[str, Any],
    outcomes: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "guided_flow_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-guided-decision-flow-prototype",
        "status": "guided_decision_flow_prototype_ready_local_offline",
        "output_dir": _relpath(output_root, repo_root),
        "files": {name: _relpath(output_root / name, repo_root) for name in REQUIRED_GUIDED_DECISION_FILES},
        "selected_candidate": state.get("selected_candidate"),
        "primary_user_question": state.get("primary_user_question"),
        "default_recommendation": state.get("default_recommendation"),
        "recommended_outcome_ids": outcomes.get("recommended_outcome_ids"),
        "source_record_policy": state.get("source_record_policy"),
        "primary_human_review": _relpath(output_root / "guided_decision_flow.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "recommendation_engine_readback": _relpath(output_root / "recommendation_engine_readback.json", repo_root),
        "markdown_fallback": _relpath(output_root / "guided_decision_flow.md", repo_root),
        "boundary_flags": state.get("boundary_flags"),
        "next_action": state.get("next_action"),
    }


def _render_html(state: dict[str, Any], outcomes: dict[str, Any], evidence: dict[str, Any]) -> str:
    default_id = str(state.get("default_recommendation"))
    default_label = _outcome_label(outcomes, default_id)
    checks = "\n".join(_render_check_card(row) for row in _list(state.get("user_situation_checks")))
    outcome_cards = "\n".join(_render_outcome_card(row) for row in _list(outcomes.get("outcomes")))
    evidence_records = "\n".join(_render_record(row) for row in _list(evidence.get("source_records")))
    gate_chips = "\n".join(f"<span>{_escape(flag)}</span>" for flag in REQUIRED_BOUNDARY_FLAGS)
    js_outcomes = json.dumps(
        {
            "real": "Real input replacement",
            "yymm4": "YMM4 import observation without render",
            "hold": "Hold and review later",
        },
        ensure_ascii=False,
    )
    return f"""<!doctype html>
<html lang="en" data-guided-decision-flow="true" data-default-recommendation="{_escape(default_id)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Guided Decision Flow</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #11100e;
      --panel: #1b1d20;
      --panel-2: #242830;
      --panel-3: #15181d;
      --text: #f3f0e8;
      --muted: #bab7ae;
      --line: #4b5563;
      --accent: #4ade80;
      --action: #8ab4f8;
      --warn: #f7c948;
      --closed: #f97373;
      --shadow: 0 18px 44px rgba(0, 0, 0, 0.28);
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #edf1ee;
        --panel: #f3f0e8;
        --panel-2: #e4e8e4;
        --panel-3: #d9dfdc;
        --text: #1f2420;
        --muted: #5b625d;
        --line: #bac3bd;
        --accent: #166534;
        --action: #1d4ed8;
        --warn: #8a5a00;
        --closed: #be123c;
        --shadow: 0 16px 34px rgba(31, 36, 32, 0.12);
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }}
    main {{ width: min(1080px, calc(100% - 32px)); margin: 0 auto; padding: 22px 0 32px; }}
    header, section, details {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    header {{ display: grid; gap: 10px; padding: 18px; }}
    h1 {{ margin: 0; font-size: clamp(1.35rem, 2.5vw, 2rem); line-height: 1.12; letter-spacing: 0; }}
    h2 {{ margin: 0 0 10px; font-size: 1.05rem; letter-spacing: 0; }}
    h3 {{ margin: 0; font-size: 0.98rem; letter-spacing: 0; }}
    p {{ margin: 0; color: var(--muted); line-height: 1.5; }}
    .primary-flow {{ margin-top: 14px; padding: 16px; display: grid; gap: 14px; }}
    .question-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }}
    .question-card, .outcome-card {{
      min-height: 142px;
      padding: 13px;
      border-radius: 8px;
      background: var(--panel-2);
      border: 1px solid var(--line);
      display: grid;
      gap: 8px;
      align-content: start;
    }}
    .answer {{ width: fit-content; padding: 4px 8px; border-radius: 999px; color: var(--text); background: var(--panel-3); border: 1px solid var(--line); font-size: 0.82rem; font-weight: 700; }}
    .recommendation {{
      padding: 16px;
      border-radius: 8px;
      background: var(--panel-3);
      border: 1px solid var(--accent);
      display: grid;
      gap: 8px;
    }}
    .recommendation strong {{ color: var(--accent); font-size: clamp(1.15rem, 2.2vw, 1.55rem); }}
    .form-row {{ display: grid; gap: 10px; grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    fieldset {{ margin: 0; padding: 12px; border: 1px solid var(--line); border-radius: 8px; display: grid; gap: 8px; }}
    legend {{ padding: 0 4px; font-weight: 700; }}
    label {{ display: flex; gap: 8px; align-items: center; color: var(--muted); line-height: 1.4; }}
    input {{ accent-color: var(--accent); }}
    .outcome-row {{ display: grid; gap: 12px; grid-template-columns: 1.25fr 0.9fr 0.9fr; }}
    .outcome-card[data-selected="true"] {{ border-color: var(--accent); box-shadow: 0 0 0 2px rgba(74, 222, 128, 0.16); }}
    .outcome-card[data-selected="false"] {{ opacity: 0.86; }}
    .status {{ width: fit-content; padding: 4px 8px; border-radius: 999px; background: var(--panel-3); color: var(--action); font-size: 0.78rem; font-weight: 700; }}
    .status.recommended {{ color: var(--accent); }}
    .status.gated {{ color: var(--warn); }}
    details {{ margin-top: 12px; padding: 13px 15px; }}
    summary {{ cursor: pointer; font-weight: 700; }}
    .record-list {{ list-style: none; padding: 0; margin: 12px 0 0; display: grid; gap: 8px; }}
    .record-list li {{ padding: 9px 10px; background: var(--panel-2); border: 1px solid var(--line); border-radius: 6px; display: grid; gap: 4px; }}
    code {{ color: var(--action); overflow-wrap: anywhere; }}
    .gate-strip {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
    .gate-strip span {{ padding: 5px 8px; border-radius: 999px; background: var(--panel-2); border: 1px solid var(--line); color: var(--muted); font-size: 0.78rem; }}
    @media (max-width: 880px) {{
      main {{ width: min(100% - 20px, 1080px); padding-top: 12px; }}
      .question-grid, .form-row, .outcome-row {{ grid-template-columns: 1fr; }}
      .question-card, .outcome-card {{ min-height: auto; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Episode 002 Decision Flow</h1>
      <p>Start with the situation you are in, then use one safe recommendation for the current sample review.</p>
    </header>

    <section class="primary-flow" data-primary-copy="true">
      <div>
        <h2>{_escape(state.get("primary_user_question"))}</h2>
        <p>Answer these checks before choosing any next work.</p>
      </div>
      <div class="question-grid">{checks}</div>
      <article class="recommendation" aria-live="polite">
        <span class="answer">Recommended now</span>
        <strong id="liveRecommendation">{_escape(default_label)}</strong>
        <p id="liveReason">{_escape(state.get("default_reason"))}</p>
      </article>
      <div class="form-row" data-interactive-prototype="true">
        <fieldset>
          <legend>Reviewed material</legend>
          <label><input type="radio" name="realInput" value="yes"> Yes</label>
          <label><input type="radio" name="realInput" value="no" checked> No</label>
        </fieldset>
        <fieldset>
          <legend>Import observation</legend>
          <label><input type="radio" name="yymm4" value="yes"> Yes</label>
          <label><input type="radio" name="yymm4" value="no" checked> No</label>
        </fieldset>
        <fieldset>
          <legend>Current intent</legend>
          <label><input type="radio" name="intent" value="story" checked> Check story only</label>
          <label><input type="radio" name="intent" value="move"> Move forward</label>
        </fieldset>
      </div>
      <div class="outcome-row">{outcome_cards}</div>
    </section>

    <details data-secondary-records>
      <summary>Evidence drawer</summary>
      <p>Source records stay here so the first screen remains about the decision.</p>
      <ul class="record-list">{evidence_records}</ul>
    </details>

    <details>
      <summary>Closed gates and boundaries</summary>
      <p>This prototype does not perform import, render, publication, rights approval, or production acceptance.</p>
      <div class="gate-strip">{gate_chips}</div>
    </details>
  </main>
  <script>
    const outcomeLabels = {js_outcomes};
    const recommendation = document.getElementById("liveRecommendation");
    const reason = document.getElementById("liveReason");
    function checked(name) {{
      const node = document.querySelector(`input[name="${{name}}"]:checked`);
      return node ? node.value : "no";
    }}
    function updateRecommendation() {{
      const real = checked("realInput") === "yes";
      const importCheck = checked("yymm4") === "yes";
      if (real) {{
        recommendation.textContent = outcomeLabels.real;
        reason.textContent = "Use this when reviewed local material exists; YMM4 and public gates still remain closed.";
      }} else if (importCheck) {{
        recommendation.textContent = outcomeLabels.yymm4;
        reason.textContent = "Use this only when import observation is explicitly selected; no render or publication follows from this page.";
      }} else {{
        recommendation.textContent = outcomeLabels.hold;
        reason.textContent = "No reviewed real material is detected and no import observation is selected, so keep this as a local review record.";
      }}
    }}
    document.querySelectorAll("input").forEach((node) => node.addEventListener("change", updateRecommendation));
  </script>
</body>
</html>
"""


def _render_check_card(row: Any) -> str:
    if not isinstance(row, dict):
        return ""
    return "\n".join(
        [
            '<article class="question-card">',
            f"  <span class=\"answer\">Current answer: {_escape(row.get('current_answer_label'))}</span>",
            f"  <h3>{_escape(row.get('question'))}</h3>",
            "</article>",
        ]
    )


def _render_outcome_card(row: Any) -> str:
    if not isinstance(row, dict):
        return ""
    selected = row.get("recommended_for_current_state") is True
    status_class = "recommended" if selected else "gated"
    return "\n".join(
        [
            f'<article class="outcome-card" data-selected="{str(selected).lower()}">',
            f'  <span class="status {status_class}">{_escape("recommended" if selected else "gated")}</span>',
            f"  <h3>{_escape(row.get('label'))}</h3>",
            f"  <p>{_escape(row.get('use_when'))}</p>",
            f"  <p>{_escape(row.get('effect'))}</p>",
            "</article>",
        ]
    )


def _render_record(row: Any) -> str:
    if not isinstance(row, dict):
        return ""
    exists = "present" if row.get("exists") else "missing"
    return "\n".join(
        [
            "<li>",
            f"  <span>{_escape(row.get('label'))} ({_escape(exists)})</span>",
            f"  <code>{_escape(row.get('repo_relative_path'))}</code>",
            "</li>",
        ]
    )


def _render_markdown(state: dict[str, Any], outcomes: dict[str, Any], evidence: dict[str, Any]) -> str:
    default_id = str(state.get("default_recommendation"))
    default_label = _outcome_label(outcomes, default_id)
    lines = [
        "# Episode 002 Guided Decision Flow",
        "",
        "This local prototype starts with the user's situation and then gives one safe recommendation.",
        "",
        f"Primary question: {state.get('primary_user_question')}",
        "",
        "## Current Checked Answers",
        "",
    ]
    for row in _list(state.get("user_situation_checks")):
        if isinstance(row, dict):
            lines.append(f"- {row.get('question')} {row.get('current_answer_label')}.")
    lines.extend(
        [
            "",
            "## Recommended Now",
            "",
            f"{default_label}.",
            "",
            str(state.get("default_reason")),
            "",
            "## Other Paths",
            "",
        ]
    )
    for row in _list(outcomes.get("outcomes")):
        if isinstance(row, dict) and row.get("outcome_id") != default_id:
            lines.append(f"- {row.get('label')}: {row.get('required_next_input')}")
    lines.extend(
        [
            "",
            "## Evidence Drawer",
            "",
            "Source records stay secondary to the decision.",
            "",
        ]
    )
    for row in _list(evidence.get("source_records")):
        if isinstance(row, dict):
            lines.append(f"- {row.get('label')}: `{row.get('repo_relative_path')}`")
    lines.extend(
        [
            "",
            "## Closed Gates",
            "",
            "- No production readiness claim.",
            "- No YMM4 import, render, or production project creation.",
            "- No public upload, publication, rights acceptance, or final thumbnail approval.",
            "",
        ]
    )
    return "\n".join(lines)


def _render_review_checklist(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Guided Decision Flow Review Checklist",
            "",
            "- Open `guided_decision_flow.html`.",
            "- Confirm the first screen asks about the user's situation before evidence paths.",
            "- Confirm exactly one recommendation is selected for the current checked state.",
            "- Confirm evidence and source paths stay in the evidence drawer.",
            "- Confirm closed gates remain visible and unchanged.",
            "",
            f"Primary human review: `{state.get('primary_human_review')}`",
            f"Machine readback: `{state.get('primary_machine_readable')}`",
            "",
        ]
    )


def _render_limitations(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Guided Decision Flow Prototype Limitations",
            "",
            "This package is a local static prototype and recommendation readback for the current sample-backed episode review state.",
            "",
            "Not performed:",
            "",
            "- full-suite green campaign",
            "- repeated full pytest loops",
            "- broad fixture regeneration",
            "- production UI promotion without human review",
            "- YouTube upload, publication, scheduling, or visibility change",
            "- OAuth, API keys, payment, or paid services",
            "- rights/legal/public-ready acceptance",
            "- live scraping or media download",
            "- external image/media download or embedded copyrighted media",
            "- external CSS, JavaScript, font, image, media, or CDN dependency",
            "- YMM4 GUI launch, import, render, or production `.ymmp` generation",
            "- final thumbnail approval",
            "- cross-repo or destructive git",
            "- real transcript/source replacement",
            "",
            f"Primary review file: `{state.get('primary_human_review')}`",
            "",
        ]
    )


def _select_recommendation(real_input_available: bool, explicit_yymm4_observation: bool) -> str:
    if real_input_available:
        return "real_input_replacement"
    if explicit_yymm4_observation:
        return "actual_yymm4_import_observation_no_render"
    return "hold_review_later"


def _default_reason(recommendation: str, real_input_available: bool, explicit_yymm4_observation: bool) -> str:
    if recommendation == "real_input_replacement":
        return "Reviewed local material was detected, so the next safe path is replacing the sample input while keeping production gates closed."
    if recommendation == "actual_yymm4_import_observation_no_render":
        return "Import observation has been explicitly selected, so the next path is a manual observation without render or publication."
    if not real_input_available and not explicit_yymm4_observation:
        return "No reviewed real material is detected and no import observation is selected, so keep this as a local review record."
    return "Keep this as a local review record until a higher-confidence path is selected."


def _outcome_label(outcomes: dict[str, Any], outcome_id: str) -> str:
    for row in _list(outcomes.get("outcomes")):
        if isinstance(row, dict) and row.get("outcome_id") == outcome_id:
            return str(row.get("label"))
    return outcome_id


def _boundary_flags(layout_manifest: dict[str, Any], cockpit_state: dict[str, Any]) -> dict[str, bool]:
    layout_flags = _dict(layout_manifest.get("boundary_flags"))
    cockpit_flags = _dict(cockpit_state.get("boundary_flags"))
    return {
        flag: layout_flags.get(flag) is True or cockpit_flags.get(flag) is True
        for flag in REQUIRED_BOUNDARY_FLAGS
    }


def _real_input_files(real_input_dir: Path, repo_root: Path) -> list[str]:
    if not real_input_dir.exists() or not real_input_dir.is_dir():
        return []
    ignored = {"readme.md", ".gitkeep", "placeholder.txt"}
    files: list[str] = []
    for path in sorted(real_input_dir.iterdir()):
        if not path.is_file():
            continue
        if path.name.lower() in ignored or path.name.startswith("."):
            continue
        if path.stat().st_size <= 0:
            continue
        files.append(_relpath(path, repo_root))
    return files


def _record(record_id: str, label: str, path: Path, source_group: str, repo_root: Path) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "label": label,
        "source_group": source_group,
        "repo_relative_path": _relpath(path, repo_root),
        "role": "secondary_source_record",
        "display_zone": "evidence_drawer",
        "exists": path.exists(),
    }


def _primary_visible_text(html_text: str) -> str:
    match = re.search(
        r'<section class="primary-flow"[^>]*data-primary-copy="true"[^>]*>(.*?)</section>',
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    primary = match.group(1) if match else html_text
    primary = re.sub(r"<script\b.*?</script>", " ", primary, flags=re.IGNORECASE | re.DOTALL)
    primary = re.sub(r"<style\b.*?</style>", " ", primary, flags=re.IGNORECASE | re.DOTALL)
    primary = re.sub(r"<[^>]+>", " ", primary)
    return html.unescape(re.sub(r"\s+", " ", primary)).strip()


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


def _temporary_copy_hits(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8-sig", errors="ignore").lower()
        for marker in TEMPORARY_COPY_MARKERS:
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
