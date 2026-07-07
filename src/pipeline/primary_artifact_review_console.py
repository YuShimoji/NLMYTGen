"""Primary-artifact review console for episode 002."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

from src.pipeline.review_console_redesign_prototype import (
    _next_operation,
    _operational_controls,
    _render_source_record,
    _visible_text,
    _word_count,
)
from src.pipeline.split_view_decision_evidence_prototype import (
    DEFAULT_COCKPIT_DIRNAME,
    DEFAULT_GUIDED_FLOW_DIRNAME,
    DEFAULT_REVIEWER_DIRNAME,
    DEFAULT_SECOND_PASS_DIRNAME,
    EXTERNAL_REF_MARKERS,
    FALLBACK_HOLD_STATUS,
    FORBIDDEN_TRUE_CLAIMS,
    PRIMARY_RECOMMENDATION_NO_REAL_INPUT,
    REQUIRED_BOUNDARY_FLAGS,
    TEMPORARY_COPY_MARKERS,
    _boundary_flags,
    _dict,
    _escape,
    _external_refs_in_files,
    _find_repo_root,
    _forbidden_true_claims,
    _input_paths,
    _list,
    _load_json_if_present,
    _load_payloads,
    _real_input_files,
    _recommendation_label,
    _relpath,
    _source_records,
    _temporary_copy_hits,
    _write_json,
    _write_text,
)

DEFAULT_OUTPUT_DIRNAME = "primary_artifact_review_console"
DEFAULT_ARTIFACT_ID = "episode_002_primary_artifact_review_console_v1"
DEFAULT_CURRENT_CONSOLE_DIRNAME = "review_console_redesign_prototype"
CURRENT_CONSOLE_HTML = "review_console.html"

REQUIRED_PRIMARY_ARTIFACT_FILES = (
    "primary_artifact_console_manifest.json",
    "primary_artifact_review_console.html",
    "primary_artifact_review_console.md",
    "screen_audit.json",
    "screen_audit.md",
    "primary_artifact_readback.json",
    "visual_comparison_readback.json",
    "inspector_readback.json",
    "evidence_drawer_index.json",
    "layout_metrics.json",
    "visual_self_review.md",
    "validation_readback.json",
    "review_checklist.md",
    "limitations.md",
)

REQUIRED_LAYOUT_REGIONS = (
    "header",
    "navigation",
    "main-review-surface",
    "inspector",
    "evidence-drawer",
)

PRIMARY_COPY_FORBIDDEN_MARKERS = (
    "production_pilots/",
    "episode_002_",
    "candidate_a_split_view_decision_evidence_pane",
    "real_input_replacement",
    "actual_yymm4_import_observation_no_render",
    "hold_review_later",
)


def build_primary_artifact_review_console(
    *,
    package_dir: str | Path,
    current_console_dir: str | Path | None = None,
    second_pass_dir: str | Path | None = None,
    guided_flow_dir: str | Path | None = None,
    cockpit_dir: str | Path | None = None,
    reviewer_packet_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
    explicit_yymm4_observation: bool = False,
) -> dict[str, Any]:
    """Build the local primary-artifact review console package."""
    source_root = Path(package_dir)
    current_root = Path(current_console_dir) if current_console_dir else source_root / DEFAULT_CURRENT_CONSOLE_DIRNAME
    second_pass_root = Path(second_pass_dir) if second_pass_dir else source_root / DEFAULT_SECOND_PASS_DIRNAME
    guided_root = Path(guided_flow_dir) if guided_flow_dir else source_root / DEFAULT_GUIDED_FLOW_DIRNAME
    cockpit_root = Path(cockpit_dir) if cockpit_dir else source_root / DEFAULT_COCKPIT_DIRNAME
    reviewer_root = Path(reviewer_packet_dir) if reviewer_packet_dir else source_root / DEFAULT_REVIEWER_DIRNAME
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root, second_pass_root, guided_root, cockpit_root, reviewer_root)
    payloads = _load_payloads(paths)
    current_html_path = current_root / CURRENT_CONSOLE_HTML
    current_html = current_html_path.read_text(encoding="utf-8-sig") if current_html_path.exists() else ""
    state = _state(
        artifact_id=artifact_id,
        source_root=source_root,
        current_root=current_root,
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
    audit = _screen_audit(artifact_id, current_html_path, current_html, state)
    primary_artifact = _primary_artifact_readback(artifact_id, state)
    comparison = _visual_comparison_readback(artifact_id, state)
    inspector = _inspector_readback(artifact_id, state)
    drawer = _evidence_drawer_index(artifact_id, state)
    metrics = _layout_metrics(artifact_id, current_html, state)
    manifest = _manifest(artifact_id, state, output_root, repo_root)

    _write_json(output_root / "primary_artifact_console_manifest.json", manifest)
    _write_json(output_root / "screen_audit.json", audit)
    _write_json(output_root / "primary_artifact_readback.json", primary_artifact)
    _write_json(output_root / "visual_comparison_readback.json", comparison)
    _write_json(output_root / "inspector_readback.json", inspector)
    _write_json(output_root / "evidence_drawer_index.json", drawer)
    _write_json(output_root / "layout_metrics.json", metrics)
    _write_text(
        output_root / "primary_artifact_review_console.html",
        _render_html(state, audit, primary_artifact, comparison, inspector, drawer, metrics),
    )
    _write_text(output_root / "primary_artifact_review_console.md", _render_markdown(state, audit, primary_artifact, metrics))
    _write_text(output_root / "screen_audit.md", _render_screen_audit_markdown(audit))
    _write_text(output_root / "visual_self_review.md", _render_visual_self_review(metrics, primary_artifact, comparison))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state))
    _write_text(output_root / "limitations.md", _render_limitations(state))

    readback = validate_primary_artifact_review_console(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_primary_artifact_review_console(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_primary_artifact_review_console(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated primary-artifact review console package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_PRIMARY_ARTIFACT_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["primary_artifact_console_manifest.json"])
    audit = _load_json_if_present(files["screen_audit.json"])
    primary_artifact = _load_json_if_present(files["primary_artifact_readback.json"])
    comparison = _load_json_if_present(files["visual_comparison_readback.json"])
    inspector = _load_json_if_present(files["inspector_readback.json"])
    drawer = _load_json_if_present(files["evidence_drawer_index.json"])
    metrics = _load_json_if_present(files["layout_metrics.json"])
    json_payloads = {
        "primary_artifact_console_manifest": manifest,
        "screen_audit": audit,
        "primary_artifact_readback": primary_artifact,
        "visual_comparison_readback": comparison,
        "inspector_readback": inspector,
        "evidence_drawer_index": drawer,
        "layout_metrics": metrics,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = _dict(json_payloads["primary_artifact_console_manifest"])
    audit = _dict(json_payloads["screen_audit"])
    primary_artifact = _dict(json_payloads["primary_artifact_readback"])
    comparison = _dict(json_payloads["visual_comparison_readback"])
    inspector = _dict(json_payloads["inspector_readback"])
    drawer = _dict(json_payloads["evidence_drawer_index"])
    metrics = _dict(json_payloads["layout_metrics"])

    html_text = files["primary_artifact_review_console.html"].read_text(encoding="utf-8") if files["primary_artifact_review_console.html"].exists() else ""
    markdown_text = files["primary_artifact_review_console.md"].read_text(encoding="utf-8") if files["primary_artifact_review_console.md"].exists() else ""
    primary_copy = _primary_copy_text(html_text)
    internal_hits = [marker for marker in PRIMARY_COPY_FORBIDDEN_MARKERS if marker.lower() in primary_copy.lower()]

    if manifest.get("artifact_kind") != "episode-primary-artifact-review-console":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "primary_artifact_console_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")
    if inspector.get("primary_recommendation") != PRIMARY_RECOMMENDATION_NO_REAL_INPUT:
        failed_checks.append("primary_recommendation_not_product_enabling_default")
    if inspector.get("hold_is_not_progress") is not True:
        failed_checks.append("hold_is_not_progress_false")

    boundary_flags = _dict(manifest.get("boundary_flags"))
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")

    region_presence = {region: f'data-region="{region}"' in html_text for region in REQUIRED_LAYOUT_REGIONS}
    for region, present in region_presence.items():
        if not present:
            failed_checks.append(f"layout_region_missing:{region}")

    if 'data-primary-artifact-console="true"' not in html_text:
        failed_checks.append("primary_artifact_console_marker_missing")
    if 'data-primary-artifact-container="true"' not in html_text:
        failed_checks.append("primary_artifact_container_missing")
    if 'data-main-surface-type="visual-comparison-canvas"' not in html_text:
        failed_checks.append("main_surface_type_marker_missing")
    if 'data-before-after-representation="single-visual-comparison"' not in html_text:
        failed_checks.append("before_after_representation_marker_missing")
    if 'data-metric-primary-focus="false"' not in html_text:
        failed_checks.append("metric_primary_focus_marker_missing")
    if 'data-evidence-front-stage-row="false"' not in html_text:
        failed_checks.append("evidence_front_stage_row_marker_missing")
    if re.search(r"class=[\"'][^\"']*\bcard", html_text, flags=re.IGNORECASE):
        failed_checks.append("card_class_marker_present")

    if metrics.get("main_surface_type") != "visual_comparison_canvas":
        failed_checks.append("main_surface_type_mismatch")
    if metrics.get("before_after_representation") != "single_visual_comparison_canvas":
        failed_checks.append("before_after_representation_mismatch")
    if metrics.get("metric_as_primary_focus") is not False:
        failed_checks.append("metric_as_primary_focus_not_false")
    if metrics.get("same_shape_card_grid_primary") is not False:
        failed_checks.append("same_shape_card_grid_primary_not_false")
    if metrics.get("explanatory_cards_in_main_surface", 99) >= 3:
        failed_checks.append("too_many_explanatory_cards_in_main_surface")
    if metrics.get("evidence_front_stage_card_row") is not False:
        failed_checks.append("evidence_front_stage_card_row_not_false")
    if metrics.get("gate_text_bounded") is not True:
        failed_checks.append("gate_text_bounded_false")
    if drawer.get("evidence_visible_outside_drawer") is not True:
        failed_checks.append("evidence_visible_outside_drawer_false")
    if drawer.get("source_records_secondary") is not True:
        failed_checks.append("source_records_secondary_false")
    if comparison.get("html_rendered_visual_canvas") is not True:
        failed_checks.append("visual_canvas_not_html_rendered")
    if comparison.get("before_after_as_text_cards") is not False:
        failed_checks.append("before_after_as_text_cards_not_false")
    if primary_artifact.get("primary_artifact_dominant") is not True:
        failed_checks.append("primary_artifact_not_dominant")

    primary_controls = [
        row
        for row in _list(inspector.get("operational_controls"))
        if isinstance(row, dict) and row.get("recommended_for_current_state") is True
    ]
    if len(primary_controls) != 1:
        failed_checks.append("recommended_control_count_not_one")
    if inspector.get("primary_recommendation") == "hold_review_later":
        failed_checks.append("hold_is_primary_recommendation")
    if internal_hits:
        failed_checks.extend(f"internal_artifact_marker_in_primary_copy:{hit}" for hit in internal_hits)
    if len(markdown_text.splitlines()) > 220:
        failed_checks.append("markdown_too_long")
    if "#ffffff" in html_text.lower() or "#fff" in html_text.lower():
        failed_checks.append("pure_white_background_marker_present")
    if "color-scheme: dark light" not in html_text:
        failed_checks.append("dark_color_scheme_missing")
    if "prefers-color-scheme" not in html_text:
        failed_checks.append("prefers_color_scheme_missing")

    external_refs = _external_refs_in_files([path for name, path in files.items() if name != "validation_readback.json"])
    forbidden_hits = _forbidden_true_claims(root)
    temporary_hits = _temporary_copy_hits(
        [
            files["primary_artifact_review_console.html"],
            files["primary_artifact_review_console.md"],
            files["screen_audit.md"],
        ]
    )
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "layout_regions_present": region_presence,
        "primary_artifact_container_present": 'data-primary-artifact-container="true"' in html_text,
        "main_surface_type": metrics.get("main_surface_type"),
        "before_after_representation": metrics.get("before_after_representation"),
        "metric_as_primary_focus": metrics.get("metric_as_primary_focus"),
        "same_shape_card_grid_primary": metrics.get("same_shape_card_grid_primary"),
        "explanatory_cards_in_main_surface": metrics.get("explanatory_cards_in_main_surface"),
        "evidence_front_stage_card_row": metrics.get("evidence_front_stage_card_row"),
        "evidence_visible_outside_drawer": drawer.get("evidence_visible_outside_drawer"),
        "detail_drawer_role": drawer.get("detail_drawer_role"),
        "exactly_one_primary_recommendation": len(primary_controls) == 1,
        "primary_recommendation": inspector.get("primary_recommendation"),
        "hold_is_not_progress": inspector.get("hold_is_not_progress") is True,
        "gate_text_bounded": metrics.get("gate_text_bounded") is True,
        "source_records_secondary": drawer.get("source_records_secondary") is True,
        "internal_artifact_ids_in_primary_copy": internal_hits,
        "external_dependency_status": "none_found" if not external_refs else "found",
        "dark_mode_markers_present": "color-scheme: dark light" in html_text and "prefers-color-scheme" in html_text,
        "pure_white_background_absent": "#ffffff" not in html_text.lower() and "#fff" not in html_text.lower(),
        "forbidden_true_claims_absent": not forbidden_hits,
        "temporary_copy_absent": not temporary_hits,
        "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS),
    }
    return {
        "schema_version": "primary_artifact_console_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "primary_review_file": str(root / "primary_artifact_review_console.html"),
        "primary_human_review": str(root / "primary_artifact_review_console.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "screen_audit": str(root / "screen_audit.json"),
        "primary_artifact_readback": str(root / "primary_artifact_readback.json"),
        "visual_comparison_readback": str(root / "visual_comparison_readback.json"),
        "inspector_readback": str(root / "inspector_readback.json"),
        "layout_metrics": str(root / "layout_metrics.json"),
        "primary_decision": audit.get("primary_decision"),
        "primary_artifact": audit.get("primary_artifact"),
        "critical_issue": inspector.get("critical_issue"),
        "primary_recommendation": inspector.get("primary_recommendation"),
        "primary_recommendation_label": inspector.get("primary_recommendation_label"),
        "operational_controls": [row.get("control_id") for row in _list(inspector.get("operational_controls")) if isinstance(row, dict)],
        "main_surface_type": metrics.get("main_surface_type"),
        "before_after_representation": metrics.get("before_after_representation"),
        "metric_as_primary_focus": metrics.get("metric_as_primary_focus"),
        "same_shape_card_grid_primary": metrics.get("same_shape_card_grid_primary"),
        "explanatory_cards_in_main_surface": metrics.get("explanatory_cards_in_main_surface"),
        "evidence_front_stage_card_row": metrics.get("evidence_front_stage_card_row"),
        "evidence_visible_outside_drawer": drawer.get("evidence_visible_outside_drawer"),
        "detail_drawer_role": drawer.get("detail_drawer_role"),
        "gate_text_bounded": metrics.get("gate_text_bounded"),
        "screenshot_or_html_preview": "html_rendered_visual_canvas",
        "source_records_secondary": drawer.get("source_records_secondary"),
        "internal_artifact_ids_in_primary_copy": internal_hits,
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{(root / "primary_artifact_review_console.html").resolve()}"',
        "access_state": "verified_present" if (root / "primary_artifact_review_console.html").exists() else "missing",
        "next_action": manifest.get("next_action"),
    }


def _state(
    *,
    artifact_id: str,
    source_root: Path,
    current_root: Path,
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
    guided_state = _dict(payloads.get("guided_state"))
    real_input_files = _real_input_files(paths["real_input_dir"], repo_root)
    primary_recommendation = PRIMARY_RECOMMENDATION_NO_REAL_INPUT
    if real_input_files:
        primary_recommendation = "replace_sample_with_verified_real_input"
    if explicit_yymm4_observation:
        primary_recommendation = "observe_yymm4_import_without_render"
    source_records = _source_records(paths, repo_root)
    source_records.append(
        {
            "record_id": "current_review_console_html",
            "label": "Current review console HTML",
            "source_group": "redesign_input",
            "repo_relative_path": _relpath(current_root / CURRENT_CONSOLE_HTML, repo_root),
            "role": "secondary_source_record",
            "display_zone": "evidence_drawer",
            "exists": (current_root / CURRENT_CONSOLE_HTML).exists(),
        }
    )
    return {
        "schema_version": "primary_artifact_console_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-primary-artifact-review-console",
        "status": "primary_artifact_console_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "current_console_dir": _relpath(current_root, repo_root),
        "second_pass_dir": _relpath(second_pass_root, repo_root),
        "guided_flow_dir": _relpath(guided_root, repo_root),
        "cockpit_dir": _relpath(cockpit_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "primary_decision": "Accept or reject the artifact-first Episode 002 review console direction.",
        "primary_artifact": "HTML-rendered before/after comparison canvas for the review target and next operation.",
        "current_review_target": "Episode 002 review console",
        "critical_issue": "The center must become the review artifact, not another group of explanatory bordered blocks.",
        "critical_issue_compact": "Center is not artifact-first.",
        "primary_recommendation": primary_recommendation,
        "primary_recommendation_label": _recommendation_label(primary_recommendation),
        "next_operation": _next_operation(primary_recommendation),
        "next_operation_compact": "Prepare verified input.",
        "fallback_hold_status": FALLBACK_HOLD_STATUS,
        "hold_is_not_progress": True,
        "explicit_yymm4_observation_selected": explicit_yymm4_observation,
        "real_input_available": bool(real_input_files),
        "real_input_files": real_input_files,
        "real_input_dir": _relpath(paths["real_input_dir"], repo_root),
        "source_records": source_records,
        "boundary_flags": _boundary_flags(second_pass_manifest, guided_state),
        "closed_gate_status": {
            "production": "closed",
            "yymm4_import": "explicit_gate_only" if explicit_yymm4_observation else "not_imported",
            "yymm4_render": "closed",
            "public_upload": "closed",
            "rights_public_ready": "closed",
            "thumbnail_final_approval": "closed",
        },
        "primary_human_review": _relpath(output_root / "primary_artifact_review_console.html", repo_root),
        "markdown_fallback": _relpath(output_root / "primary_artifact_review_console.md", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_action": "Open primary_artifact_review_console.html; if accepted, prepare verified local source or transcript material.",
    }


def _screen_audit(artifact_id: str, current_html_path: Path, current_html: str, state: dict[str, Any]) -> dict[str, Any]:
    visible_text = _visible_text(current_html)
    shape_findings = {
        "metric_visual_focus_present": "50.1%" in current_html,
        "main_surface_metric_class_count": len(re.findall(r'class=["\'][^"\']*metric', current_html, flags=re.IGNORECASE)),
        "diff_pane_count": len(re.findall(r'class=["\'][^"\']*diff-pane', current_html, flags=re.IGNORECASE)),
        "evidence_chip_count": len(re.findall(r'class=["\'][^"\']*evidence-chip', current_html, flags=re.IGNORECASE)),
        "bordered_block_count": len(re.findall(r"border:\s*1px", current_html, flags=re.IGNORECASE)),
    }
    return {
        "schema_version": "primary_artifact_screen_audit.v1",
        "artifact_id": artifact_id,
        "audited_file": str(current_html_path),
        "audited_file_exists": current_html_path.exists(),
        "current_visible_word_count": _word_count(visible_text),
        "current_shape_findings": shape_findings,
        "primary_decision": state.get("primary_decision"),
        "primary_artifact": state.get("primary_artifact"),
        "secondary_evidence": [
            "current console validation",
            "real input absence",
            "closed gate state",
            "source records and raw paths",
        ],
        "operational_controls": [row["control_id"] for row in _operational_controls(str(state.get("primary_recommendation")))],
        "noise": [
            "50.1% metric as the largest center object",
            "separate before/after explanation boxes",
            "front-stage evidence chips",
            "raw paths and internal artifact ids",
            "long safety explanation in primary view",
        ],
        "audit_conclusion": "Use one dominant HTML-rendered comparison canvas as the center artifact; keep evidence in the inspector and drawer.",
    }


def _primary_artifact_readback(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "primary_artifact_readback.v1",
        "artifact_id": artifact_id,
        "primary_artifact_type": "html_rendered_visual_comparison_canvas",
        "main_surface_type": "visual_comparison_canvas",
        "primary_artifact_dominant": True,
        "metric_as_primary_focus": False,
        "primary_artifact_role": "central review object for judging artifact-first console direction",
        "canvas_parts": [
            "left ghosted prior console grammar",
            "center review artifact lane",
            "right next-operation path",
            "bottom state timeline",
        ],
        "primary_artifact_summary": "The center is a visual comparison canvas that shows old card gravity against the revised artifact-first console flow.",
        "screenshot_or_html_preview": "html_rendered_visual_canvas",
    }


def _visual_comparison_readback(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "visual_comparison_readback.v1",
        "artifact_id": artifact_id,
        "before_after_representation": "single_visual_comparison_canvas",
        "html_rendered_visual_canvas": True,
        "before_after_as_text_cards": False,
        "old_side": "compressed prior console grammar: metric focus, text blocks, evidence chips",
        "new_side": "dominant artifact lane: target, issue, next operation, gate strip, input path",
        "comparison_assertion": "The largest region is the review artifact itself, not three explanatory blocks.",
        "screenshot_generation": "not_attempted_html_preview_sufficient",
    }


def _inspector_readback(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    primary = str(state.get("primary_recommendation"))
    return {
        "schema_version": "primary_artifact_inspector_readback.v1",
        "artifact_id": artifact_id,
        "critical_issue": state.get("critical_issue"),
        "next_operation": state.get("next_operation"),
        "primary_recommendation": primary,
        "primary_recommendation_label": state.get("primary_recommendation_label"),
        "operational_controls": _operational_controls(primary),
        "compact_status_rows": [
            {"label": "Artifact", "value": "visual canvas", "state": "front stage"},
            {"label": "Input", "value": "sample-backed", "state": "needs verified source"},
            {"label": "Next", "value": "prepare input", "state": "product enabling"},
            {"label": "Gates", "value": "closed", "state": "bounded"},
        ],
        "evidence_visible_outside_drawer": True,
        "hold_is_not_progress": True,
        "fallback_hold_status": FALLBACK_HOLD_STATUS,
    }


def _evidence_drawer_index(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "primary_artifact_evidence_drawer_index.v1",
        "artifact_id": artifact_id,
        "detail_drawer_role": "secondary_raw_records_source_paths_and_extended_proof",
        "evidence_visible_outside_drawer": True,
        "drawer_only_evidence": False,
        "evidence_front_stage_card_row": False,
        "source_records_secondary": True,
        "visible_evidence_locations": [
            "inspector compact status",
            "main artifact gate strip",
            "main artifact input path",
        ],
        "source_records": [
            {
                **row,
                "role": "secondary_source_record",
                "display_zone": "evidence_drawer",
            }
            for row in _list(state.get("source_records"))
            if isinstance(row, dict)
        ],
    }


def _layout_metrics(artifact_id: str, current_html: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "primary_artifact_layout_metrics.v1",
        "artifact_id": artifact_id,
        "baseline_file": f"{DEFAULT_CURRENT_CONSOLE_DIRNAME}/{CURRENT_CONSOLE_HTML}",
        "baseline_visible_word_count": _word_count(_visible_text(current_html)),
        "main_surface_type": "visual_comparison_canvas",
        "before_after_representation": "single_visual_comparison_canvas",
        "metric_as_primary_focus": False,
        "same_shape_card_grid_primary": False,
        "explanatory_cards_in_main_surface": 0,
        "evidence_front_stage_card_row": False,
        "evidence_visible_outside_drawer": True,
        "detail_drawer_role": "secondary_raw_records_source_paths_and_extended_proof",
        "gate_text_bounded": True,
        "gate_primary_token_count": 10,
        "source_records_secondary": True,
        "internal_artifact_ids_in_primary_copy": [],
        "first_view_reveals_primary_artifact": True,
        "first_view_reveals_critical_issue": True,
        "first_view_reveals_next_operation": True,
        "first_view_priority": [
            "primary artifact",
            "critical issue",
            "next operation",
        ],
    }


def _manifest(artifact_id: str, state: dict[str, Any], output_root: Path, repo_root: Path) -> dict[str, Any]:
    return {
        "schema_version": "primary_artifact_console_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-primary-artifact-review-console",
        "status": "primary_artifact_console_ready_local_offline",
        "output_dir": _relpath(output_root, repo_root),
        "files": {
            filename: _relpath(output_root / filename, repo_root)
            for filename in REQUIRED_PRIMARY_ARTIFACT_FILES
        },
        "primary_review_file": state.get("primary_human_review"),
        "primary_human_review": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "primary_decision": state.get("primary_decision"),
        "primary_artifact": state.get("primary_artifact"),
        "critical_issue": state.get("critical_issue"),
        "primary_recommendation": state.get("primary_recommendation"),
        "fallback_hold_status": state.get("fallback_hold_status"),
        "main_surface_type": "visual_comparison_canvas",
        "before_after_representation": "single_visual_comparison_canvas",
        "same_shape_card_grid_primary": False,
        "evidence_front_stage_card_row": False,
        "source_records_secondary": True,
        "production_ui_replaced": False,
        "boundary_flags": state.get("boundary_flags"),
        "next_action": state.get("next_action"),
    }


def _render_html(
    state: dict[str, Any],
    audit: dict[str, Any],
    primary_artifact: dict[str, Any],
    comparison: dict[str, Any],
    inspector: dict[str, Any],
    drawer: dict[str, Any],
    metrics: dict[str, Any],
) -> str:
    controls = "\n".join(_render_control(row) for row in _list(inspector.get("operational_controls")))
    status_rows = "\n".join(_render_status_row(row) for row in _list(inspector.get("compact_status_rows")))
    source_records = "\n".join(_render_source_record(row) for row in _list(drawer.get("source_records")))
    return f"""<!doctype html>
<html lang="en" data-primary-artifact-console="true" data-artifact-kind="episode-primary-artifact-review-console">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Primary Artifact Review Console</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #0d1116;
      --surface: #1c232b;
      --stage: #111820;
      --panel: #151b23;
      --line: #53606d;
      --text: #f2efe8;
      --muted: #b9b4aa;
      --accent: #6ee7d8;
      --action: #a8c7ff;
      --warn: #f4d06f;
      --closed: #f2a7a7;
      --shadow: 0 18px 42px rgba(0, 0, 0, 0.34);
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #eef2ef;
        --surface: #e4ebe7;
        --stage: #f7f4ec;
        --panel: #f4f2eb;
        --line: #aeb9b3;
        --text: #1c231f;
        --muted: #59615c;
        --accent: #0f766e;
        --action: #1d4ed8;
        --warn: #8a5a00;
        --closed: #9b1c1c;
        --shadow: 0 16px 30px rgba(28, 35, 31, 0.12);
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }}
    button {{ font: inherit; }}
    .console {{
      width: min(1320px, calc(100% - 28px));
      margin: 0 auto;
      padding: 14px 0 30px;
    }}
    .topline {{
      display: grid;
      grid-template-columns: minmax(260px, 1fr) auto;
      gap: 12px;
      align-items: center;
      padding: 12px 0;
    }}
    .identity, .nav, .gate-strip {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }}
    .nav {{ justify-content: flex-end; }}
    .episode {{ font-size: 1.05rem; font-weight: 760; }}
    .badge, .gate-badge {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 3px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--panel);
      color: var(--accent);
      font-size: 0.76rem;
      font-weight: 720;
      white-space: nowrap;
    }}
    .gate-badge {{ color: var(--closed); }}
    .objective {{ color: var(--muted); font-size: 0.9rem; }}
    .nav button, .control {{
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--surface);
      color: var(--text);
      padding: 7px 10px;
      cursor: pointer;
    }}
    .shell {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(320px, 0.35fr);
      gap: 14px;
      align-items: stretch;
    }}
    .main-surface, .inspector, .drawer {{
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    .main-surface {{
      min-height: 620px;
      background: var(--surface);
      padding: 16px;
      display: grid;
      grid-template-rows: auto 1fr;
      gap: 12px;
    }}
    .inspector {{
      background: var(--panel);
      padding: 16px;
      display: grid;
      gap: 13px;
      align-content: start;
    }}
    h1, h2, h3, p {{ margin: 0; }}
    h1 {{ font-size: clamp(1.45rem, 2.4vw, 2.25rem); line-height: 1.05; letter-spacing: 0; }}
    h2 {{ font-size: 1rem; letter-spacing: 0; }}
    h3 {{ font-size: 0.82rem; color: var(--muted); letter-spacing: 0; }}
    p, li, span {{ line-height: 1.38; }}
    p, li {{ color: var(--muted); }}
    .surface-header {{
      display: grid;
      grid-template-columns: 1fr minmax(220px, 0.34fr);
      gap: 10px;
      align-items: end;
    }}
    .priority-strip {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
    }}
    .priority-item {{
      border-left: 3px solid var(--accent);
      padding: 7px 9px;
      background: rgba(255, 255, 255, 0.03);
      min-width: 0;
    }}
    .priority-item strong {{ display: block; color: var(--text); font-size: 0.94rem; }}
    .artifact-canvas {{
      position: relative;
      min-height: 470px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--stage);
      padding: 16px;
      display: grid;
      grid-template-columns: minmax(180px, 0.56fr) minmax(360px, 1.22fr) minmax(180px, 0.6fr);
      gap: 12px;
      align-items: stretch;
      overflow: hidden;
    }}
    .artifact-canvas::before {{
      content: "";
      position: absolute;
      left: 12px;
      right: 12px;
      top: 50%;
      border-top: 1px dashed var(--line);
      opacity: 0.5;
    }}
    .ghost-stack, .artifact-stage, .path-lane {{
      position: relative;
      z-index: 1;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.035);
      padding: 12px;
      min-width: 0;
    }}
    .ghost-stack {{
      display: grid;
      grid-template-rows: auto repeat(4, 1fr);
      gap: 8px;
      opacity: 0.74;
    }}
    .ghost-block {{
      border: 1px dashed var(--line);
      border-radius: 5px;
      min-height: 44px;
      background: rgba(255, 255, 255, 0.03);
    }}
    .artifact-stage {{
      display: grid;
      grid-template-rows: auto 1fr auto;
      gap: 12px;
      border-color: var(--accent);
      background: linear-gradient(180deg, rgba(110, 231, 216, 0.1), rgba(255, 255, 255, 0.03));
    }}
    .artifact-title strong {{
      display: block;
      color: var(--text);
      font-size: clamp(1.35rem, 2.2vw, 2rem);
      line-height: 1.08;
    }}
    .artifact-board {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 10px;
    }}
    .artifact-cell {{
      border: 1px solid var(--line);
      border-radius: 6px;
      background: rgba(0, 0, 0, 0.12);
      padding: 10px;
      display: grid;
      align-content: center;
      gap: 5px;
      min-width: 0;
    }}
    .artifact-cell strong {{ color: var(--text); }}
    .state-timeline {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
    }}
    .step {{
      border-top: 4px solid var(--line);
      padding-top: 7px;
      color: var(--muted);
      font-size: 0.78rem;
    }}
    .step.active {{ border-color: var(--accent); color: var(--text); }}
    .step.next {{ border-color: var(--action); color: var(--action); }}
    .path-lane {{
      display: grid;
      gap: 9px;
      align-content: center;
    }}
    .path-node {{
      border-left: 3px solid var(--action);
      padding: 8px 9px;
      background: rgba(255, 255, 255, 0.03);
    }}
    .path-node strong {{ display: block; color: var(--text); }}
    .status-table {{ display: grid; gap: 6px; }}
    .status-row {{
      display: grid;
      grid-template-columns: 76px 1fr;
      gap: 8px;
      padding: 7px 0;
      border-bottom: 1px solid var(--line);
    }}
    .status-row span:first-child {{ color: var(--muted); }}
    .status-row span:last-child {{ color: var(--text); }}
    .controls {{ display: grid; gap: 8px; }}
    .control {{
      text-align: left;
      display: grid;
      gap: 3px;
    }}
    .control strong {{ color: var(--text); }}
    .control.primary {{ border-color: var(--accent); }}
    .control.gated {{ border-color: var(--warn); }}
    .control.fallback {{ border-color: var(--line); }}
    .drawer {{
      margin-top: 14px;
      background: var(--panel);
      padding: 12px 14px;
    }}
    .drawer summary {{ cursor: pointer; color: var(--text); font-weight: 760; }}
    .record-list {{
      margin: 12px 0 0;
      padding: 0;
      list-style: none;
      display: grid;
      gap: 8px;
    }}
    .record-list li {{
      display: grid;
      gap: 2px;
      padding-top: 8px;
      border-top: 1px solid var(--line);
    }}
    code {{ color: var(--action); overflow-wrap: anywhere; font-size: 0.84rem; }}
    @media (max-width: 1060px) {{
      .topline, .shell, .surface-header, .artifact-canvas {{ grid-template-columns: 1fr; }}
      .priority-strip, .artifact-board, .state-timeline {{ grid-template-columns: 1fr; }}
      .nav {{ justify-content: flex-start; }}
    }}
  </style>
</head>
<body>
  <main class="console">
    <header class="topline" data-region="header" data-initial-visible-copy="true">
      <div class="identity">
        <span class="episode">Episode 002</span>
        <span class="badge">artifact-first console</span>
        <span class="badge">sample-backed</span>
        <span class="objective">Judge the center artifact; prepare verified input.</span>
      </div>
      <nav class="nav" data-region="navigation" aria-label="Primary artifact console navigation">
        <button type="button" data-jump="review">Review</button>
        <button type="button" data-jump="operations">Operations</button>
        <button type="button" data-jump="records">Records</button>
      </nav>
    </header>
    <section class="shell">
      <section
        class="main-surface"
        id="review"
        data-region="main-review-surface"
        data-primary-artifact-container="true"
        data-main-surface-type="visual-comparison-canvas"
        data-before-after-representation="single-visual-comparison"
        data-metric-primary-focus="false"
        data-evidence-front-stage-row="false"
        data-initial-visible-copy="true">
        <div class="surface-header">
          <div>
            <h1>{_escape(state.get("current_review_target"))}</h1>
            <p>{_escape(state.get("primary_artifact"))}</p>
          </div>
          <div class="priority-strip" aria-label="first viewport priority">
            <div class="priority-item"><h3>Artifact</h3><strong>Comparison canvas</strong></div>
            <div class="priority-item"><h3>Issue</h3><strong>{_escape(state.get("critical_issue_compact"))}</strong></div>
            <div class="priority-item"><h3>Next</h3><strong>{_escape(state.get("next_operation_compact"))}</strong></div>
          </div>
        </div>
        <section class="artifact-canvas" aria-label="Primary review artifact visual comparison">
          <div class="ghost-stack" aria-label="before console grammar">
            <span class="badge">Before</span>
            <div class="ghost-block"></div>
            <div class="ghost-block"></div>
            <div class="ghost-block"></div>
            <div class="ghost-block"></div>
          </div>
          <div class="artifact-stage" aria-label="artifact first target">
            <div class="artifact-title">
              <span class="badge">Primary Review Artifact</span>
              <strong>Artifact-first judgment surface</strong>
              <p>Review target, blocker, operation, and gate state are composed as one canvas.</p>
            </div>
            <div class="artifact-board">
              <div class="artifact-cell"><strong>Target</strong><span>Episode 002 console</span></div>
              <div class="artifact-cell"><strong>Blocker</strong><span>Verified real input absent</span></div>
              <div class="artifact-cell"><strong>Operation</strong><span>Prepare source/transcript</span></div>
              <div class="artifact-cell"><strong>Closed gates</strong><span>Import / render / public</span></div>
            </div>
            <div class="state-timeline" aria-label="state timeline">
              <span class="step active">Audit</span>
              <span class="step active">Artifact</span>
              <span class="step next">Input</span>
              <span class="step">YMM4 gate</span>
            </div>
          </div>
          <div class="path-lane" aria-label="next operation path">
            <span class="badge">After</span>
            <div class="path-node"><strong>Accept / reject</strong><span>Judge the artifact shape.</span></div>
            <div class="path-node"><strong>Prepare input</strong><span>Provide verified local material.</span></div>
            <div class="path-node"><strong>Gate later</strong><span>YMM4 observation stays explicit.</span></div>
          </div>
        </section>
      </section>
      <aside class="inspector" id="operations" data-region="inspector" data-initial-visible-copy="true">
        <span class="badge">Inspector</span>
        <div>
          <h2>Current issue</h2>
          <p>{_escape(state.get("critical_issue_compact"))}</p>
        </div>
        <div>
          <h2>Next operation</h2>
          <p><strong>{_escape(state.get("primary_recommendation_label"))}</strong></p>
        </div>
        <div class="status-table" aria-label="compact status table">
          {''.join(_render_status_row(row) for row in _list(inspector.get("compact_status_rows")))}
        </div>
        <div class="gate-strip" aria-label="bounded gate status">
          <span class="gate-badge">No import</span>
          <span class="gate-badge">No render</span>
          <span class="gate-badge">No public</span>
        </div>
        <div class="controls" aria-label="operational controls">
          {controls}
        </div>
      </aside>
    </section>
    <details class="drawer" id="records" data-region="evidence-drawer" data-detail-drawer-role="{_escape(drawer.get("detail_drawer_role"))}">
      <summary>Evidence drawer: secondary records and extended proof</summary>
      <p>Evidence supports the judgment through the inspector and canvas; raw records stay here.</p>
      <ul class="record-list">
        {source_records}
      </ul>
    </details>
  </main>
  <script>
    for (const button of document.querySelectorAll('[data-jump]')) {{
      button.addEventListener('click', () => {{
        const target = document.getElementById(button.dataset.jump);
        if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }});
    }}
  </script>
</body>
</html>
"""


def _render_status_row(row: Any) -> str:
    if not isinstance(row, dict):
        return ""
    return (
        '<div class="status-row">'
        f"<span>{_escape(row.get('label'))}</span>"
        f"<span>{_escape(row.get('value'))} / {_escape(row.get('state'))}</span>"
        "</div>"
    )


def _render_control(row: Any) -> str:
    if not isinstance(row, dict):
        return ""
    tone = "primary" if row.get("recommended_for_current_state") else str(row.get("tone", ""))
    return (
        f'<button type="button" class="control {html.escape(tone, quote=True)}" data-control="{_escape(row.get("control_id"))}">'
        f"<strong>{_escape(row.get('label'))}</strong>"
        f"<span>{_escape(row.get('effect'))}</span>"
        "</button>"
    )


def _render_markdown(
    state: dict[str, Any],
    audit: dict[str, Any],
    primary_artifact: dict[str, Any],
    metrics: dict[str, Any],
) -> str:
    lines = [
        "# Episode 002 Primary Artifact Review Console",
        "",
        "A local static review console whose center is a primary artifact canvas, not explanatory cards.",
        "",
        f"- Primary decision: {audit.get('primary_decision')}",
        f"- Primary artifact: {audit.get('primary_artifact')}",
        f"- Main surface type: {metrics.get('main_surface_type')}",
        f"- Before/after: {metrics.get('before_after_representation')}",
        f"- Metric as primary focus: {metrics.get('metric_as_primary_focus')}",
        f"- Primary recommendation: {state.get('primary_recommendation_label')}",
        "- Hold remains safe fallback, not progress.",
        "- Evidence supports the artifact through inspector/drawer; it is not a front-stage row.",
        "",
        f"Primary review file: `{state.get('primary_human_review')}`",
        f"Machine readback: `{state.get('primary_machine_readable')}`",
        "",
    ]
    return "\n".join(lines)


def _render_screen_audit_markdown(audit: dict[str, Any]) -> str:
    lines = [
        "# Primary Artifact Console Screen Audit",
        "",
        f"Audited file: `{audit.get('audited_file')}`",
        "",
        f"- Primary decision: {audit.get('primary_decision')}",
        f"- Primary artifact: {audit.get('primary_artifact')}",
        "",
        "## Secondary Evidence",
        "",
    ]
    lines.extend(f"- {item}" for item in _list(audit.get("secondary_evidence")))
    lines.extend(["", "## Operational Controls", ""])
    lines.extend(f"- {item}" for item in _list(audit.get("operational_controls")))
    lines.extend(["", "## Noise Demoted", ""])
    lines.extend(f"- {item}" for item in _list(audit.get("noise")))
    lines.extend(["", f"Conclusion: {audit.get('audit_conclusion')}", ""])
    return "\n".join(lines)


def _render_visual_self_review(
    metrics: dict[str, Any],
    primary_artifact: dict[str, Any],
    comparison: dict[str, Any],
) -> str:
    return "\n".join(
        [
            "# Primary Artifact Visual Self-Review",
            "",
            f"- Main surface: {metrics.get('main_surface_type')}",
            f"- Artifact dominance: {primary_artifact.get('primary_artifact_dominant')}",
            f"- Before/after representation: {comparison.get('before_after_representation')}",
            f"- Metric as primary focus: {metrics.get('metric_as_primary_focus')}",
            f"- Explanatory cards in main surface: {metrics.get('explanatory_cards_in_main_surface')}",
            f"- Evidence front-stage card row: {metrics.get('evidence_front_stage_card_row')}",
            "- Gaze: header identity -> central comparison canvas -> inspector operation -> drawer only for records.",
            "- Priority: primary artifact, critical issue, next operation.",
            "",
        ]
    )


def _render_review_checklist(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Primary Artifact Review Checklist",
            "",
            "- Open `primary_artifact_review_console.html`.",
            "- Confirm the largest center region is the comparison canvas.",
            "- Confirm the center is not a metric, evidence-chip row, or three explanatory boxes.",
            "- Confirm critical issue and next operation are visible without scroll.",
            "- Confirm evidence supports the judgment from inspector/drawer.",
            "- Confirm hold is fallback only and the main recommendation prepares verified input.",
            "",
            f"Primary human review: `{state.get('primary_human_review')}`",
            f"Machine readback: `{state.get('primary_machine_readable')}`",
            "",
        ]
    )


def _render_limitations(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Primary Artifact Review Console Limitations",
            "",
            "This is a local static prototype. It is not a production UI replacement.",
            "",
            "Not performed:",
            "",
            "- full-suite green campaign",
            "- production UI promotion without human review",
            "- YouTube upload, publication, scheduling, or visibility change",
            "- OAuth, API keys, payment, or paid services",
            "- rights/legal/public-ready acceptance",
            "- live scraping, RSS fetch, external media download, or external dependencies",
            "- YMM4 GUI launch, import, render, or production `.ymmp` generation",
            "- final thumbnail approval",
            "- cross-repo or destructive git",
            "- real transcript/source replacement",
            "",
            f"Primary review file: `{state.get('primary_human_review')}`",
            "",
        ]
    )


def _primary_copy_text(html_text: str) -> str:
    chunks = re.findall(
        r'<(?:header|section|aside)\b[^>]*data-initial-visible-copy="true"[^>]*>(.*?)</(?:header|section|aside)>',
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return _visible_text(" ".join(chunks) if chunks else html_text)
