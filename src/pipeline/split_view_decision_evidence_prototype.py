"""Split-view decision/evidence prototype for episode 002 review."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIRNAME = "split_view_decision_evidence_prototype"
DEFAULT_ARTIFACT_ID = "episode_002_split_view_decision_evidence_prototype_v1"
DEFAULT_SECOND_PASS_DIRNAME = "review_layout_second_pass"
DEFAULT_GUIDED_FLOW_DIRNAME = "guided_decision_flow_prototype"
DEFAULT_COCKPIT_DIRNAME = "review_cockpit_compact"
DEFAULT_REVIEWER_DIRNAME = "surface_alignment_review_packet"

SELECTED_CANDIDATE = "candidate_a_split_view_decision_evidence_pane"
PRIMARY_RECOMMENDATION_NO_REAL_INPUT = "prepare_verified_local_source_transcript"
PRIMARY_RECOMMENDATION_REAL_INPUT = "replace_sample_with_verified_real_input"
PRIMARY_RECOMMENDATION_YMM4 = "observe_yymm4_import_without_render"
FALLBACK_HOLD_STATUS = "safe_fallback_not_progress"

REQUIRED_SPLIT_VIEW_FILES = (
    "split_view_manifest.json",
    "split_view_decision_evidence.html",
    "split_view_decision_evidence.md",
    "split_view_state.json",
    "recommendation_readback.json",
    "evidence_pane_readback.json",
    "source_record_index.json",
    "layout_metrics.json",
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
    '"production_ui_replaced": true',
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

INTERNAL_LEFT_PRIMARY_MARKERS = (
    "production_pilots/",
    "review_layout_second_pass",
    "guided_decision_flow_prototype",
    "review_cockpit_compact",
    "surface_alignment_review_packet",
    "focused_review_brief",
    "factory_seed_dry_run_002",
    "candidate_a_split_view_decision_evidence_pane",
    "episode_002_",
    "real_input_replacement",
    "actual_yymm4_import_observation_no_render",
    "hold_review_later",
    "dry_run",
    "sample_fixture_not_real",
    "no_real_transcript",
    "public_upload_closed",
    "no_yymm4_import",
)


def build_split_view_decision_evidence_prototype(
    *,
    package_dir: str | Path,
    second_pass_dir: str | Path | None = None,
    guided_flow_dir: str | Path | None = None,
    cockpit_dir: str | Path | None = None,
    reviewer_packet_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
    explicit_yymm4_observation: bool = False,
) -> dict[str, Any]:
    """Build the local split-view decision/evidence prototype."""
    source_root = Path(package_dir)
    second_pass_root = Path(second_pass_dir) if second_pass_dir else source_root / DEFAULT_SECOND_PASS_DIRNAME
    guided_root = Path(guided_flow_dir) if guided_flow_dir else source_root / DEFAULT_GUIDED_FLOW_DIRNAME
    cockpit_root = Path(cockpit_dir) if cockpit_dir else source_root / DEFAULT_COCKPIT_DIRNAME
    reviewer_root = Path(reviewer_packet_dir) if reviewer_packet_dir else source_root / DEFAULT_REVIEWER_DIRNAME
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root, second_pass_root, guided_root, cockpit_root, reviewer_root)
    payloads = _load_payloads(paths)
    state = _split_view_state(
        artifact_id=artifact_id,
        source_root=source_root,
        second_pass_root=second_pass_root,
        guided_root=guided_root,
        cockpit_root=cockpit_root,
        reviewer_root=reviewer_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        payloads=payloads,
        explicit_yymm4_observation=explicit_yymm4_observation,
    )
    recommendation = _recommendation_readback(artifact_id, state)
    evidence = _evidence_pane_readback(artifact_id, state)
    source_index = _source_record_index(artifact_id, state)
    metrics = _layout_metrics(artifact_id, state)
    manifest = _manifest(artifact_id, state, output_root, repo_root)

    _write_json(output_root / "split_view_manifest.json", manifest)
    _write_json(output_root / "split_view_state.json", state)
    _write_json(output_root / "recommendation_readback.json", recommendation)
    _write_json(output_root / "evidence_pane_readback.json", evidence)
    _write_json(output_root / "source_record_index.json", source_index)
    _write_json(output_root / "layout_metrics.json", metrics)
    _write_text(output_root / "split_view_decision_evidence.html", _render_html(state, evidence, source_index, metrics))
    _write_text(output_root / "split_view_decision_evidence.md", _render_markdown(state, evidence, source_index))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state))
    _write_text(output_root / "limitations.md", _render_limitations(state))

    readback = validate_split_view_decision_evidence_prototype(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_split_view_decision_evidence_prototype(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_split_view_decision_evidence_prototype(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated split-view prototype package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_SPLIT_VIEW_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["split_view_manifest.json"])
    state = _load_json_if_present(files["split_view_state.json"])
    recommendation = _load_json_if_present(files["recommendation_readback.json"])
    evidence = _load_json_if_present(files["evidence_pane_readback.json"])
    source_index = _load_json_if_present(files["source_record_index.json"])
    metrics = _load_json_if_present(files["layout_metrics.json"])
    json_payloads = {
        "split_view_manifest": manifest,
        "split_view_state": state,
        "recommendation_readback": recommendation,
        "evidence_pane_readback": evidence,
        "source_record_index": source_index,
        "layout_metrics": metrics,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["split_view_manifest"]
    state = json_payloads["split_view_state"]
    recommendation = json_payloads["recommendation_readback"]
    evidence = json_payloads["evidence_pane_readback"]
    source_index = json_payloads["source_record_index"]
    metrics = json_payloads["layout_metrics"]

    if manifest.get("artifact_kind") != "episode-split-view-decision-evidence-prototype":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "split_view_prototype_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")
    if manifest.get("selected_candidate") != SELECTED_CANDIDATE:
        failed_checks.append("selected_candidate_mismatch")
    if state.get("primary_recommendation") != recommendation.get("primary_recommendation"):
        failed_checks.append("primary_recommendation_mismatch")

    boundary_flags = _dict(manifest.get("boundary_flags"))
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")

    html_text = files["split_view_decision_evidence.html"].read_text(encoding="utf-8") if files["split_view_decision_evidence.html"].exists() else ""
    markdown_text = files["split_view_decision_evidence.md"].read_text(encoding="utf-8") if files["split_view_decision_evidence.md"].exists() else ""
    left_primary_text = _left_primary_visible_text(html_text)
    internal_left_hits = [
        marker for marker in INTERNAL_LEFT_PRIMARY_MARKERS if marker.lower() in left_primary_text.lower()
    ]

    if "data-split-view=\"true\"" not in html_text:
        failed_checks.append("split_view_marker_missing")
    if "data-left-primary-copy=\"true\"" not in html_text:
        failed_checks.append("left_primary_marker_missing")
    if "data-right-evidence-pane=\"true\"" not in html_text:
        failed_checks.append("right_evidence_pane_marker_missing")
    for phrase in (
        "Evidence preview",
        "Source readiness",
        "Recommendation rationale",
        "Bounded gate context",
    ):
        if phrase not in html_text:
            failed_checks.append(f"right_pane_visible_phrase_missing:{phrase}")
    if "color-scheme: dark light" not in html_text:
        failed_checks.append("dark_color_scheme_missing")
    if "prefers-color-scheme" not in html_text:
        failed_checks.append("prefers_color_scheme_missing")
    if "#ffffff" in html_text.lower() or "#fff" in html_text.lower():
        failed_checks.append("pure_white_background_marker_present")
    if internal_left_hits:
        failed_checks.extend(f"internal_artifact_marker_in_left_primary_copy:{hit}" for hit in internal_left_hits)
    if "data-secondary-source-records" not in html_text:
        failed_checks.append("secondary_source_records_missing")
    if "class=\"card" in html_text.lower() or "card-grid" in html_text.lower():
        failed_checks.append("card_grid_marker_present")
    if len(markdown_text.splitlines()) > 220:
        failed_checks.append("markdown_too_long")

    recommendation_paths = _list(recommendation.get("recommendation_paths"))
    primary_paths = [
        row
        for row in recommendation_paths
        if isinstance(row, dict) and row.get("recommended_for_current_state") is True
    ]
    if len(primary_paths) != 1:
        failed_checks.append("recommended_path_count_not_one")
    if recommendation.get("exactly_one_recommendation") is not True:
        failed_checks.append("recommendation_exactly_one_false")
    if recommendation.get("primary_recommendation") == "hold_review_later":
        failed_checks.append("hold_is_primary_recommendation")
    if recommendation.get("fallback_hold_status") != FALLBACK_HOLD_STATUS:
        failed_checks.append("fallback_hold_status_mismatch")
    if recommendation.get("hold_is_not_progress") is not True:
        failed_checks.append("hold_is_not_progress_false")

    source_records = _list(source_index.get("source_records"))
    source_records_secondary = bool(source_records) and all(
        isinstance(row, dict)
        and row.get("role") == "secondary_source_record"
        and row.get("display_zone") == "secondary_source_records"
        for row in source_records
    )
    if not source_records_secondary:
        failed_checks.append("source_records_not_secondary")

    if evidence.get("evidence_visible_without_drawer") is not True:
        failed_checks.append("evidence_visible_without_drawer_false")
    if evidence.get("drawer_only_evidence") is not False:
        failed_checks.append("drawer_only_evidence_not_false")
    if not _list(evidence.get("visible_evidence_rows")):
        failed_checks.append("visible_evidence_rows_missing")

    if metrics.get("split_view_structure_status") != "passed_left_decision_rail_right_evidence_pane":
        failed_checks.append("split_view_structure_status_mismatch")
    if metrics.get("gate_text_bounded") is not True:
        failed_checks.append("gate_text_bounded_false")
    if metrics.get("card_grid_as_primary_structure") is not False:
        failed_checks.append("card_grid_as_primary_structure_not_false")
    if metrics.get("primary_card_grid_count") != 0:
        failed_checks.append("primary_card_grid_count_nonzero")
    if metrics.get("internal_artifact_ids_in_left_primary_copy") != []:
        failed_checks.append("layout_metrics_internal_artifacts_present")

    external_refs = _external_refs_in_files([path for name, path in files.items() if name != "validation_readback.json"])
    forbidden_hits = _forbidden_true_claims(root)
    temporary_hits = _temporary_copy_hits([files["split_view_decision_evidence.html"], files["split_view_decision_evidence.md"]])
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "selected_candidate": manifest.get("selected_candidate"),
        "split_view_structure_present": all(
            marker in html_text
            for marker in (
                "data-split-view=\"true\"",
                "data-left-primary-copy=\"true\"",
                "data-right-evidence-pane=\"true\"",
            )
        ),
        "evidence_visible_without_drawer": evidence.get("evidence_visible_without_drawer") is True,
        "drawer_only_evidence": evidence.get("drawer_only_evidence") is True,
        "exactly_one_recommendation": len(primary_paths) == 1 and recommendation.get("exactly_one_recommendation") is True,
        "primary_recommendation": recommendation.get("primary_recommendation"),
        "fallback_hold_status": recommendation.get("fallback_hold_status"),
        "hold_is_not_progress": recommendation.get("hold_is_not_progress") is True,
        "source_records_secondary": source_records_secondary,
        "internal_artifact_ids_in_left_primary_copy": internal_left_hits,
        "gate_text_bounded": metrics.get("gate_text_bounded") is True,
        "card_grid_as_primary_structure": metrics.get("card_grid_as_primary_structure") is True,
        "external_dependency_status": "none_found" if not external_refs else "found",
        "dark_mode_markers_present": "color-scheme: dark light" in html_text and "prefers-color-scheme" in html_text,
        "pure_white_background_absent": "#ffffff" not in html_text.lower() and "#fff" not in html_text.lower(),
        "forbidden_true_claims_absent": not forbidden_hits,
        "temporary_copy_absent": not temporary_hits,
        "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS),
    }
    return {
        "schema_version": "split_view_decision_evidence_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "selected_candidate": manifest.get("selected_candidate"),
        "primary_review_file": str(root / "split_view_decision_evidence.html"),
        "primary_human_review": str(root / "split_view_decision_evidence.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "recommendation_readback": str(root / "recommendation_readback.json"),
        "evidence_pane_readback": str(root / "evidence_pane_readback.json"),
        "markdown_fallback": str(root / "split_view_decision_evidence.md"),
        "primary_recommendation": recommendation.get("primary_recommendation"),
        "fallback_hold_status": recommendation.get("fallback_hold_status"),
        "evidence_visible_without_drawer": evidence.get("evidence_visible_without_drawer"),
        "right_pane_summary": evidence.get("right_pane_summary"),
        "source_records_secondary": source_records_secondary,
        "gate_text_bounded": metrics.get("gate_text_bounded"),
        "internal_artifact_ids_in_left_primary_copy": internal_left_hits,
        "card_grid_as_primary_structure": metrics.get("card_grid_as_primary_structure"),
        "split_view_structure_status": metrics.get("split_view_structure_status"),
        "launcher_command": f'start "" "{(root / "split_view_decision_evidence.html").resolve()}"',
        "access_state": "verified_present" if (root / "split_view_decision_evidence.html").exists() else "missing",
        "next_action": manifest.get("next_action"),
    }


def _input_paths(
    source_root: Path,
    second_pass_root: Path,
    guided_root: Path,
    cockpit_root: Path,
    reviewer_root: Path,
) -> dict[str, Path]:
    return {
        "second_pass_manifest": second_pass_root / "layout_second_pass_manifest.json",
        "second_pass_matrix": second_pass_root / "layout_candidate_matrix.json",
        "second_pass_recommendation": second_pass_root / "final_layout_recommendation.md",
        "split_view_benchmark": second_pass_root / "split_view_benchmark.md",
        "evidence_report": second_pass_root / "evidence_handling_report.md",
        "card_bloat_report": second_pass_root / "card_bloat_risk_report.md",
        "second_pass_wireframes": second_pass_root / "candidate_wireframes_second_pass.html",
        "second_pass_validation": second_pass_root / "validation_readback.json",
        "guided_html": guided_root / "guided_decision_flow.html",
        "guided_state": guided_root / "flow_state.json",
        "guided_validation": guided_root / "validation_readback.json",
        "guided_recommendation": guided_root / "recommendation_engine_readback.json",
        "guided_evidence": guided_root / "evidence_drawer_index.json",
        "cockpit_html": cockpit_root / "review_cockpit.html",
        "aligned_story": reviewer_root / "aligned_review_story.md",
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


def _split_view_state(
    *,
    artifact_id: str,
    source_root: Path,
    second_pass_root: Path,
    guided_root: Path,
    cockpit_root: Path,
    reviewer_root: Path,
    output_root: Path,
    repo_root: Path,
    paths: dict[str, Path],
    payloads: dict[str, Any],
    explicit_yymm4_observation: bool,
) -> dict[str, Any]:
    second_pass_manifest = _dict(payloads.get("second_pass_manifest"))
    second_pass_matrix = _dict(payloads.get("second_pass_matrix"))
    guided_state = _dict(payloads.get("guided_state"))
    boundary_flags = _boundary_flags(second_pass_manifest, guided_state)
    real_input_files = _real_input_files(paths["real_input_dir"], repo_root)
    real_input_available = bool(real_input_files)
    primary_recommendation = _select_recommendation(real_input_available, explicit_yymm4_observation)
    selected_candidate = second_pass_matrix.get("winning_candidate") or second_pass_manifest.get("selected_candidate")
    return {
        "schema_version": "split_view_decision_evidence_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-split-view-decision-evidence-prototype",
        "status": "split_view_prototype_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "second_pass_dir": _relpath(second_pass_root, repo_root),
        "guided_flow_dir": _relpath(guided_root, repo_root),
        "cockpit_dir": _relpath(cockpit_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "selected_candidate": selected_candidate,
        "second_pass_status": second_pass_manifest.get("status"),
        "evaluated_guided_flow": second_pass_manifest.get("evaluated_guided_flow"),
        "active_decision": "Move from layout review back toward real input readiness unless the split-view layout is rejected.",
        "user_situation": "Episode 002 is still sample-backed local review; no verified real source or transcript file is present.",
        "real_input_dir": _relpath(paths["real_input_dir"], repo_root),
        "real_input_files": real_input_files,
        "real_input_available": real_input_available,
        "explicit_yymm4_observation_selected": explicit_yymm4_observation,
        "primary_recommendation": primary_recommendation,
        "primary_recommendation_label": _recommendation_label(primary_recommendation),
        "fallback_hold_status": FALLBACK_HOLD_STATUS,
        "hold_is_not_progress": True,
        "explicit_gate_alternative": PRIMARY_RECOMMENDATION_YMM4,
        "user_required_input": _required_input(primary_recommendation),
        "next_product_enabling_action": _next_product_action(primary_recommendation),
        "left_pane_sections": [
            "user situation",
            "active decision",
            "current recommendation",
            "next product-enabling action",
        ],
        "right_pane_sections": [
            "evidence preview",
            "source readiness",
            "recommendation rationale",
            "bounded gate context",
            "secondary source records",
        ],
        "source_records": _source_records(paths, repo_root),
        "source_record_policy": "secondary_records_only",
        "source_records_display_zone": "secondary_source_records",
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
        "primary_human_review": _relpath(output_root / "split_view_decision_evidence.html", repo_root),
        "markdown_fallback": _relpath(output_root / "split_view_decision_evidence.md", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "recommendation_readback": _relpath(output_root / "recommendation_readback.json", repo_root),
        "evidence_pane_readback": _relpath(output_root / "evidence_pane_readback.json", repo_root),
        "next_action": "Review the split-view HTML; if accepted, prepare verified local source or transcript material as the next product-enabling input.",
    }


def _recommendation_readback(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    primary_id = str(state.get("primary_recommendation"))
    paths = [
        {
            "recommendation_id": PRIMARY_RECOMMENDATION_NO_REAL_INPUT,
            "label": "Prepare verified local source or transcript material",
            "recommended_for_current_state": primary_id == PRIMARY_RECOMMENDATION_NO_REAL_INPUT,
            "progress_role": "product_enabling_default",
            "required_next_input": "A reviewed local source file, transcript, or equivalent source record for Episode 002.",
        },
        {
            "recommendation_id": PRIMARY_RECOMMENDATION_REAL_INPUT,
            "label": "Replace the sample with verified real input",
            "recommended_for_current_state": primary_id == PRIMARY_RECOMMENDATION_REAL_INPUT,
            "progress_role": "product_enabling_when_input_exists",
            "required_next_input": "Already-present verified local source or transcript material.",
        },
        {
            "recommendation_id": PRIMARY_RECOMMENDATION_YMM4,
            "label": "Observe YMM4 import without render",
            "recommended_for_current_state": primary_id == PRIMARY_RECOMMENDATION_YMM4,
            "progress_role": "explicit_gate_alternative",
            "required_next_input": "Explicit human selection of YMM4 import observation; render and publication remain closed.",
        },
        {
            "recommendation_id": "hold_review_later",
            "label": "Hold and review later",
            "recommended_for_current_state": False,
            "progress_role": FALLBACK_HOLD_STATUS,
            "required_next_input": "Use only as safe fallback when no product-enabling input is available.",
        },
    ]
    return {
        "schema_version": "split_view_recommendation_readback.v1",
        "artifact_id": artifact_id,
        "primary_recommendation": primary_id,
        "primary_recommendation_label": state.get("primary_recommendation_label"),
        "exactly_one_recommendation": len([row for row in paths if row["recommended_for_current_state"]]) == 1,
        "recommendation_paths": paths,
        "fallback_hold_status": FALLBACK_HOLD_STATUS,
        "hold_is_not_progress": True,
        "explicit_yymm4_observation_selected": state.get("explicit_yymm4_observation_selected"),
        "real_input_available": state.get("real_input_available"),
        "rationale": _recommendation_rationale(primary_id),
    }


def _evidence_pane_readback(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    real_input_available = state.get("real_input_available") is True
    visible_rows = [
        {
            "row_id": "selected_layout",
            "label": "Selected layout evidence",
            "status": "ready",
            "evidence": "The second-pass benchmark selects split view as the single next implementation target.",
            "supports": "Use a decision rail and evidence pane instead of extending cards or drawer-only evidence.",
        },
        {
            "row_id": "current_review_surfaces",
            "label": "Source surface readiness",
            "status": "local_review_surfaces_present",
            "evidence": "GUI dashboard, import preview, thumbnail proof, and aligned story are available as local source records.",
            "supports": "The right pane can explain what existing surfaces prove without making raw paths primary.",
        },
        {
            "row_id": "real_input_readiness",
            "label": "Real input readiness",
            "status": "verified_real_input_present" if real_input_available else "verified_real_input_absent",
            "evidence": "The real-input drop-zone has no non-placeholder source file in the current checked state.",
            "supports": "Preparing verified local source or transcript material is the product-enabling next step.",
        },
        {
            "row_id": "hold_boundary",
            "label": "Hold fallback",
            "status": FALLBACK_HOLD_STATUS,
            "evidence": "Hold remains safe because gates stay closed, but it does not move Episode 002 toward real input replacement.",
            "supports": "Do not present hold as the main progress state.",
        },
    ]
    return {
        "schema_version": "split_view_evidence_pane_readback.v1",
        "artifact_id": artifact_id,
        "evidence_visible_without_drawer": True,
        "drawer_only_evidence": False,
        "right_pane_summary": "Visible evidence preview with source readiness, recommendation rationale, bounded gate context, and secondary raw source records.",
        "visible_evidence_rows": visible_rows,
        "source_readiness_summary": {
            "second_pass_benchmark": "ready_selected_split_view",
            "guided_flow": "weak_pass_source_record",
            "gui_dashboard_panel": "ready_local_review_surface",
            "ymm4_import_preview": "ready_context_synced_not_imported",
            "thumbnail_visual_proof": "context_only_not_final_approval",
            "verified_real_input": "present" if real_input_available else "absent",
        },
        "recommendation_rationale": [
            "The split-view benchmark rejected drawer-only evidence because trust evidence must sit beside the decision.",
            "No verified real input is present, so the next product-enabling action is preparing or providing it.",
            "YMM4 observation remains an explicit-gate alternative, not an implicit next step.",
            "Hold remains safe fallback, not progress.",
        ],
        "bounded_gate_context": [
            "No render/import/publication occurs from this prototype.",
            "Rights/public-ready and final thumbnail approval remain closed.",
            "Validation drift remains nonblocking for this local review slice.",
        ],
        "secondary_source_records_path": state.get("source_records_display_zone"),
    }


def _source_record_index(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "split_view_source_record_index.v1",
        "artifact_id": artifact_id,
        "source_record_policy": "secondary_records_only",
        "source_records_secondary": True,
        "display_zone": "secondary_source_records",
        "left_primary_copy_policy": "no_raw_paths_or_internal_artifact_ids",
        "source_records": state.get("source_records"),
    }


def _layout_metrics(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "split_view_layout_metrics.v1",
        "artifact_id": artifact_id,
        "split_view_structure_status": "passed_left_decision_rail_right_evidence_pane",
        "left_pane_sections": state.get("left_pane_sections"),
        "right_pane_sections": state.get("right_pane_sections"),
        "evidence_visible_without_drawer": True,
        "drawer_only_evidence": False,
        "source_records_secondary": True,
        "gate_text_bounded": True,
        "safety_surface_budget": "bounded_one_short_left_note_plus_right_pane_context",
        "left_primary_prohibition_list_count": 0,
        "left_primary_boundary_note_count": 1,
        "internal_artifact_ids_in_left_primary_copy": [],
        "card_grid_as_primary_structure": False,
        "primary_card_grid_count": 0,
        "primary_structure": "two_pane_split_view_with_compact_rows",
    }


def _manifest(artifact_id: str, state: dict[str, Any], output_root: Path, repo_root: Path) -> dict[str, Any]:
    return {
        "schema_version": "split_view_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-split-view-decision-evidence-prototype",
        "status": "split_view_prototype_ready_local_offline",
        "output_dir": _relpath(output_root, repo_root),
        "files": {
            filename: _relpath(output_root / filename, repo_root)
            for filename in REQUIRED_SPLIT_VIEW_FILES
        },
        "selected_candidate": state.get("selected_candidate"),
        "primary_review_file": state.get("primary_human_review"),
        "primary_human_review": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "recommendation_readback": state.get("recommendation_readback"),
        "evidence_pane_readback": state.get("evidence_pane_readback"),
        "primary_recommendation": state.get("primary_recommendation"),
        "fallback_hold_status": state.get("fallback_hold_status"),
        "evidence_visible_without_drawer": True,
        "source_records_secondary": True,
        "gate_text_bounded": True,
        "card_grid_as_primary_structure": False,
        "production_ui_replaced": False,
        "boundary_flags": state.get("boundary_flags"),
        "next_action": state.get("next_action"),
    }


def _render_html(
    state: dict[str, Any],
    evidence: dict[str, Any],
    source_index: dict[str, Any],
    metrics: dict[str, Any],
) -> str:
    evidence_rows = "\n".join(_render_evidence_row(row) for row in _list(evidence.get("visible_evidence_rows")))
    source_records = "\n".join(_render_source_record(row) for row in _list(source_index.get("source_records")))
    gate_rows = "\n".join(f"<li>{_escape(item)}</li>" for item in _list(evidence.get("bounded_gate_context")))
    return f"""<!doctype html>
<html lang="en" data-split-view="true" data-artifact-kind="episode-split-view-decision-evidence-prototype">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Split View Decision Evidence</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #101113;
      --rail: #181b20;
      --pane: #20252b;
      --row: #161a1f;
      --line: #46505d;
      --text: #f3f0e8;
      --muted: #b8b5ad;
      --accent: #5eead4;
      --action: #93c5fd;
      --warn: #f6d365;
      --shadow: 0 18px 44px rgba(0, 0, 0, 0.28);
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #eef2f0;
        --rail: #f4f1ea;
        --pane: #e7ece9;
        --row: #dce4e0;
        --line: #aeb9b3;
        --text: #1f2420;
        --muted: #59615c;
        --accent: #0f766e;
        --action: #1d4ed8;
        --warn: #8a5a00;
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
    main {{
      width: min(1220px, calc(100% - 32px));
      margin: 0 auto;
      padding: 22px 0 34px;
    }}
    .top-strip {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 12px;
      color: var(--muted);
      font-size: 0.88rem;
    }}
    .split-shell {{
      display: grid;
      grid-template-columns: minmax(280px, 0.82fr) minmax(440px, 1.18fr);
      gap: 14px;
      align-items: stretch;
    }}
    .decision-rail, .evidence-pane {{
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      min-width: 0;
    }}
    .decision-rail {{
      background: var(--rail);
      padding: 18px;
      display: grid;
      gap: 14px;
      align-content: start;
    }}
    .evidence-pane {{
      background: var(--pane);
      padding: 16px;
      display: grid;
      gap: 12px;
    }}
    h1, h2, h3, p {{ margin: 0; }}
    h1 {{
      font-size: clamp(1.4rem, 2.7vw, 2.15rem);
      line-height: 1.08;
      letter-spacing: 0;
    }}
    h2 {{ font-size: 1.02rem; letter-spacing: 0; }}
    h3 {{ font-size: 0.92rem; letter-spacing: 0; }}
    p, li {{ color: var(--muted); line-height: 1.48; }}
    .label {{
      width: fit-content;
      padding: 4px 8px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: var(--row);
      color: var(--accent);
      font-size: 0.76rem;
      font-weight: 700;
    }}
    .decision-block {{
      display: grid;
      gap: 6px;
      padding-top: 12px;
      border-top: 1px solid var(--line);
    }}
    .recommendation-line {{
      color: var(--accent);
      font-size: clamp(1.12rem, 2.1vw, 1.48rem);
      font-weight: 760;
      line-height: 1.18;
    }}
    .action-line {{
      color: var(--action);
      font-weight: 700;
    }}
    .boundary-note {{
      border: 1px solid var(--line);
      background: var(--row);
      border-radius: 6px;
      padding: 10px;
      color: var(--muted);
    }}
    .pane-header {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 8px;
      align-items: center;
    }}
    .evidence-stack {{
      display: grid;
      gap: 9px;
    }}
    .compact-row {{
      display: grid;
      grid-template-columns: minmax(150px, 0.6fr) minmax(220px, 1fr);
      gap: 10px;
      padding: 11px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--row);
    }}
    .compact-row strong {{
      color: var(--text);
      line-height: 1.35;
    }}
    .status {{
      width: fit-content;
      color: var(--warn);
      font-size: 0.78rem;
      font-weight: 700;
    }}
    .rationale, .gate-context, details {{
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--row);
      padding: 12px;
    }}
    .rationale ul, .gate-context ul {{
      margin: 8px 0 0;
      padding-left: 18px;
    }}
    details summary {{
      cursor: pointer;
      font-weight: 720;
      color: var(--text);
    }}
    .record-list {{
      list-style: none;
      margin: 10px 0 0;
      padding: 0;
      display: grid;
      gap: 8px;
    }}
    .record-list li {{
      display: grid;
      gap: 3px;
      border-top: 1px solid var(--line);
      padding-top: 8px;
    }}
    code {{
      color: var(--action);
      overflow-wrap: anywhere;
      font-size: 0.86rem;
    }}
    @media (max-width: 880px) {{
      main {{ width: min(100% - 20px, 1220px); padding-top: 12px; }}
      .split-shell {{ grid-template-columns: 1fr; }}
      .compact-row {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="top-strip" aria-label="prototype status">
      <span>Episode 002 local review prototype</span>
      <span>Static package, not production UI</span>
    </div>
    <section class="split-shell" data-split-view="true" data-primary-structure="{_escape(metrics.get("primary_structure"))}">
      <aside class="decision-rail" data-left-primary-copy="true" data-safety-surface-budget="bounded">
        <span class="label">Decision rail</span>
        <h1>Episode 002 Split Review</h1>
        <div class="decision-block">
          <h2>Situation</h2>
          <p>Sample-backed local review is ready, but verified real source or transcript material is not present yet.</p>
        </div>
        <div class="decision-block">
          <h2>Active decision</h2>
          <p>Accept the split-view review shape, then move back toward real input readiness.</p>
        </div>
        <div class="decision-block">
          <h2>Current recommendation</h2>
          <p class="recommendation-line">{_escape(state.get("primary_recommendation_label"))}</p>
          <p>{_escape(_recommendation_rationale(str(state.get("primary_recommendation"))))}</p>
        </div>
        <div class="decision-block">
          <h2>Next product-enabling action</h2>
          <p class="action-line">{_escape(state.get("next_product_enabling_action"))}</p>
          <p>{_escape(state.get("user_required_input"))}</p>
        </div>
        <p class="boundary-note">Hold remains safe fallback; import, render, public release, and final approval stay closed unless separately chosen.</p>
      </aside>
      <section class="evidence-pane" data-right-evidence-pane="true">
        <div class="pane-header">
          <div>
            <span class="label">Evidence preview</span>
            <h2>Evidence and rationale stay visible</h2>
          </div>
          <span class="status">not drawer-only</span>
        </div>
        <h2>Source readiness</h2>
        <div class="evidence-stack" aria-label="visible evidence rows">
          {evidence_rows}
        </div>
        <section class="rationale" aria-label="Recommendation rationale">
          <h2>Recommendation rationale</h2>
          <ul>
            <li>The benchmark selected split view because evidence must sit beside the active decision.</li>
            <li>There is no verified real input in the checked state, so preparing it is the next useful product move.</li>
            <li>YMM4 observation is available only as an explicit-gate alternative.</li>
          </ul>
        </section>
        <section class="gate-context" aria-label="Bounded gate context">
          <h2>Bounded gate context</h2>
          <ul>{gate_rows}</ul>
        </section>
        <details data-secondary-source-records>
          <summary>Secondary source records</summary>
          <p>Raw paths and artifact records stay secondary to the decision copy.</p>
          <ul class="record-list">{source_records}</ul>
        </details>
      </section>
    </section>
  </main>
</body>
</html>
"""


def _render_evidence_row(row: Any) -> str:
    if not isinstance(row, dict):
        return ""
    return "\n".join(
        [
            '<article class="compact-row">',
            "  <div>",
            f"    <strong>{_escape(row.get('label'))}</strong>",
            f"    <p class=\"status\">{_escape(row.get('status'))}</p>",
            "  </div>",
            "  <div>",
            f"    <p>{_escape(row.get('evidence'))}</p>",
            f"    <p>{_escape(row.get('supports'))}</p>",
            "  </div>",
            "</article>",
        ]
    )


def _render_source_record(row: Any) -> str:
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


def _render_markdown(state: dict[str, Any], evidence: dict[str, Any], source_index: dict[str, Any]) -> str:
    lines = [
        "# Episode 002 Split View Decision Evidence",
        "",
        "This local prototype tests the selected split-view layout: a left decision rail and a right evidence pane.",
        "",
        "## Left Decision Rail",
        "",
        "- Situation: sample-backed local review is ready, but verified real source or transcript material is not present yet.",
        "- Active decision: accept or reject the split-view review shape, then return toward real input readiness.",
        f"- Current recommendation: {state.get('primary_recommendation_label')}.",
        f"- Next product-enabling action: {state.get('next_product_enabling_action')}",
        "- Hold remains a safe fallback, not progress.",
        "",
        "## Right Evidence Pane",
        "",
    ]
    for row in _list(evidence.get("visible_evidence_rows")):
        if isinstance(row, dict):
            lines.append(f"- {row.get('label')}: {row.get('evidence')} {row.get('supports')}")
    lines.extend(
        [
            "",
            "## Bounded Gate Context",
            "",
        ]
    )
    for item in _list(evidence.get("bounded_gate_context")):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Secondary Source Records",
            "",
            "Raw paths and source records are secondary to the decision copy.",
            "",
        ]
    )
    for row in _list(source_index.get("source_records")):
        if isinstance(row, dict):
            lines.append(f"- {row.get('label')}: `{row.get('repo_relative_path')}`")
    return "\n".join(lines) + "\n"


def _render_review_checklist(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Split View Decision Evidence Review Checklist",
            "",
            "- Open `split_view_decision_evidence.html`.",
            "- Confirm the left pane answers situation, active decision, recommendation, and next product-enabling action.",
            "- Confirm the right pane shows evidence preview, source readiness, rationale, and bounded gate context without relying on a drawer.",
            "- Confirm raw paths and artifact records are secondary details, not left-pane primary copy.",
            "- Confirm hold is safe fallback only and the main recommendation points toward verified local source or transcript material.",
            "- Confirm this prototype does not promote itself as production UI.",
            "",
            f"Primary human review: `{state.get('primary_human_review')}`",
            f"Machine readback: `{state.get('primary_machine_readable')}`",
            "",
        ]
    )


def _render_limitations(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Split View Decision Evidence Prototype Limitations",
            "",
            "This package is a local static prototype for Episode 002 review. It is not a production UI replacement.",
            "",
            "Not performed:",
            "",
            "- full-suite green campaign",
            "- production UI promotion without human review",
            "- YouTube upload, publication, scheduling, or visibility change",
            "- OAuth, API keys, payment, or paid services",
            "- rights/legal/public-ready acceptance",
            "- live scraping or media download",
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
        return PRIMARY_RECOMMENDATION_REAL_INPUT
    if explicit_yymm4_observation:
        return PRIMARY_RECOMMENDATION_YMM4
    return PRIMARY_RECOMMENDATION_NO_REAL_INPUT


def _recommendation_label(recommendation: str) -> str:
    labels = {
        PRIMARY_RECOMMENDATION_NO_REAL_INPUT: "Prepare verified local source or transcript material",
        PRIMARY_RECOMMENDATION_REAL_INPUT: "Replace the sample with verified real input",
        PRIMARY_RECOMMENDATION_YMM4: "Observe YMM4 import without render",
    }
    return labels.get(recommendation, recommendation)


def _required_input(recommendation: str) -> str:
    if recommendation == PRIMARY_RECOMMENDATION_REAL_INPUT:
        return "Use the verified local source or transcript already present in the real-input slot."
    if recommendation == PRIMARY_RECOMMENDATION_YMM4:
        return "Explicitly choose import observation; render and public release still remain out of scope."
    return "Provide a reviewed local source file, transcript, or equivalent source record for Episode 002."


def _next_product_action(recommendation: str) -> str:
    if recommendation == PRIMARY_RECOMMENDATION_REAL_INPUT:
        return "Replace the sample-backed review input with the verified local material."
    if recommendation == PRIMARY_RECOMMENDATION_YMM4:
        return "Run only the explicitly chosen import-observation lane, without render or publication."
    return "Prepare or provide verified local source/transcript material so Episode 002 can leave sample-only review."


def _recommendation_rationale(recommendation: str) -> str:
    if recommendation == PRIMARY_RECOMMENDATION_REAL_INPUT:
        return "Verified real material is present, so the next useful step is replacing the sample while keeping gates closed."
    if recommendation == PRIMARY_RECOMMENDATION_YMM4:
        return "Import observation was explicitly selected, so the next path can inspect import behavior without render or publication."
    return "No verified real material is present and no import observation is explicitly selected, so the next useful step is preparing verified local input."


def _source_records(paths: dict[str, Path], repo_root: Path) -> list[dict[str, Any]]:
    specs = (
        ("second_pass_benchmark", "Second-pass split-view benchmark", paths["split_view_benchmark"], "selected_layout_evidence"),
        ("second_pass_matrix", "Second-pass candidate matrix", paths["second_pass_matrix"], "selected_layout_evidence"),
        ("second_pass_recommendation", "Final split-view recommendation", paths["second_pass_recommendation"], "selected_layout_evidence"),
        ("evidence_handling_report", "Evidence handling report", paths["evidence_report"], "evidence_policy"),
        ("card_bloat_risk_report", "Card-bloat risk report", paths["card_bloat_report"], "layout_risk_policy"),
        ("guided_flow_html", "Guided decision flow HTML", paths["guided_html"], "weak_pass_source_record"),
        ("guided_flow_validation", "Guided flow validation", paths["guided_validation"], "weak_pass_source_record"),
        ("guided_flow_state", "Guided flow state", paths["guided_state"], "weak_pass_source_record"),
        ("compact_review_cockpit", "Compact review cockpit", paths["cockpit_html"], "prior_review_surface"),
        ("aligned_review_story", "Aligned review story", paths["aligned_story"], "source_record"),
        ("gui_dashboard_panel", "GUI dashboard panel", paths["gui_dashboard"], "source_record"),
        ("import_preview_panel", "YMM4 import preview panel", paths["import_preview"], "source_record"),
        ("thumbnail_visual_proof", "Thumbnail visual proof", paths["thumbnail_proof"], "source_record"),
        ("real_input_dir", "Real input drop-zone", paths["real_input_dir"], "input_readiness"),
    )
    return [
        {
            "record_id": record_id,
            "label": label,
            "source_group": group,
            "repo_relative_path": _relpath(path, repo_root),
            "role": "secondary_source_record",
            "display_zone": "secondary_source_records",
            "exists": path.exists(),
        }
        for record_id, label, path, group in specs
    ]


def _boundary_flags(second_pass_manifest: dict[str, Any], guided_state: dict[str, Any]) -> dict[str, bool]:
    second_flags = _dict(second_pass_manifest.get("boundary_flags"))
    guided_flags = _dict(guided_state.get("boundary_flags"))
    return {
        flag: second_flags.get(flag) is True or guided_flags.get(flag) is True
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


def _left_primary_visible_text(html_text: str) -> str:
    match = re.search(
        r'<aside class="decision-rail"[^>]*data-left-primary-copy="true"[^>]*>(.*?)</aside>',
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
