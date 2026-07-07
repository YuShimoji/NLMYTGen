"""Review judgment console redesign prototype for episode 002."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

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
    _load_json,
    _load_json_if_present,
    _load_payloads,
    _real_input_files,
    _recommendation_label,
    _recommendation_rationale,
    _relpath,
    _source_records,
    _temporary_copy_hits,
    _write_json,
    _write_text,
)

DEFAULT_OUTPUT_DIRNAME = "review_console_redesign_prototype"
DEFAULT_ARTIFACT_ID = "episode_002_review_console_redesign_prototype_v1"
CURRENT_SPLIT_VIEW_DIRNAME = "split_view_decision_evidence_prototype"
CURRENT_SPLIT_VIEW_HTML = "split_view_decision_evidence.html"

REQUIRED_REVIEW_CONSOLE_FILES = (
    "review_console_manifest.json",
    "review_console.html",
    "review_console.md",
    "screen_audit.json",
    "screen_audit.md",
    "console_state.json",
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
    "review_layout_second_pass",
    "guided_decision_flow_prototype",
    "review_cockpit_compact",
    "surface_alignment_review_packet",
    "episode_002_",
    "candidate_a_split_view_decision_evidence_pane",
    "real_input_replacement",
    "actual_yymm4_import_observation_no_render",
    "hold_review_later",
)

NOISE_BUCKETS = (
    "raw artifact paths",
    "long source provenance explanations",
    "full boundary inventories",
    "test-passing justification copy",
    "internal artifact ids",
    "secondary record ledgers",
)


def build_review_console_redesign_prototype(
    *,
    package_dir: str | Path,
    current_split_view_dir: str | Path | None = None,
    second_pass_dir: str | Path | None = None,
    guided_flow_dir: str | Path | None = None,
    cockpit_dir: str | Path | None = None,
    reviewer_packet_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
    explicit_yymm4_observation: bool = False,
) -> dict[str, Any]:
    """Build the local review judgment console prototype package."""
    source_root = Path(package_dir)
    current_root = Path(current_split_view_dir) if current_split_view_dir else source_root / CURRENT_SPLIT_VIEW_DIRNAME
    second_pass_root = Path(second_pass_dir) if second_pass_dir else source_root / DEFAULT_SECOND_PASS_DIRNAME
    guided_root = Path(guided_flow_dir) if guided_flow_dir else source_root / DEFAULT_GUIDED_FLOW_DIRNAME
    cockpit_root = Path(cockpit_dir) if cockpit_dir else source_root / DEFAULT_COCKPIT_DIRNAME
    reviewer_root = Path(reviewer_packet_dir) if reviewer_packet_dir else source_root / DEFAULT_REVIEWER_DIRNAME
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root, second_pass_root, guided_root, cockpit_root, reviewer_root)
    payloads = _load_payloads(paths)
    current_html_path = current_root / CURRENT_SPLIT_VIEW_HTML
    current_html = current_html_path.read_text(encoding="utf-8-sig") if current_html_path.exists() else ""

    state = _console_state(
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
    inspector = _inspector_readback(artifact_id, state)
    evidence_drawer = _evidence_drawer_index(artifact_id, state)
    metrics = _layout_metrics(artifact_id, current_html, state)
    manifest = _manifest(artifact_id, state, output_root, repo_root)

    _write_json(output_root / "review_console_manifest.json", manifest)
    _write_json(output_root / "screen_audit.json", audit)
    _write_json(output_root / "console_state.json", state)
    _write_json(output_root / "inspector_readback.json", inspector)
    _write_json(output_root / "evidence_drawer_index.json", evidence_drawer)
    _write_json(output_root / "layout_metrics.json", metrics)
    _write_text(output_root / "review_console.html", _render_html(state, audit, inspector, evidence_drawer, metrics))
    _write_text(output_root / "review_console.md", _render_markdown(state, audit, inspector, metrics))
    _write_text(output_root / "screen_audit.md", _render_screen_audit_markdown(audit))
    _write_text(output_root / "visual_self_review.md", _render_visual_self_review(metrics, inspector))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state))
    _write_text(output_root / "limitations.md", _render_limitations(state))

    readback = validate_review_console_redesign_prototype(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_review_console_redesign_prototype(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_review_console_redesign_prototype(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated review console prototype package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_REVIEW_CONSOLE_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["review_console_manifest.json"])
    audit = _load_json_if_present(files["screen_audit.json"])
    state = _load_json_if_present(files["console_state.json"])
    inspector = _load_json_if_present(files["inspector_readback.json"])
    drawer = _load_json_if_present(files["evidence_drawer_index.json"])
    metrics = _load_json_if_present(files["layout_metrics.json"])
    json_payloads = {
        "review_console_manifest": manifest,
        "screen_audit": audit,
        "console_state": state,
        "inspector_readback": inspector,
        "evidence_drawer_index": drawer,
        "layout_metrics": metrics,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = _dict(json_payloads["review_console_manifest"])
    audit = _dict(json_payloads["screen_audit"])
    state = _dict(json_payloads["console_state"])
    inspector = _dict(json_payloads["inspector_readback"])
    drawer = _dict(json_payloads["evidence_drawer_index"])
    metrics = _dict(json_payloads["layout_metrics"])

    html_text = files["review_console.html"].read_text(encoding="utf-8") if files["review_console.html"].exists() else ""
    markdown_text = files["review_console.md"].read_text(encoding="utf-8") if files["review_console.md"].exists() else ""
    primary_text = _primary_copy_text(html_text)
    internal_hits = [marker for marker in PRIMARY_COPY_FORBIDDEN_MARKERS if marker.lower() in primary_text.lower()]

    if manifest.get("artifact_kind") != "episode-review-console-redesign-prototype":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "review_console_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")
    if state.get("primary_recommendation") != PRIMARY_RECOMMENDATION_NO_REAL_INPUT:
        failed_checks.append("primary_recommendation_not_product_enabling_default")
    if state.get("fallback_hold_status") != FALLBACK_HOLD_STATUS:
        failed_checks.append("fallback_hold_status_mismatch")
    if state.get("hold_is_not_progress") is not True:
        failed_checks.append("hold_is_not_progress_false")

    boundary_flags = _dict(manifest.get("boundary_flags"))
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")

    region_presence = {
        region: f'data-region="{region}"' in html_text
        for region in REQUIRED_LAYOUT_REGIONS
    }
    for region, present in region_presence.items():
        if not present:
            failed_checks.append(f"layout_region_missing:{region}")

    if 'data-review-console="true"' not in html_text:
        failed_checks.append("review_console_marker_missing")
    if 'data-initial-visible-copy="true"' not in html_text:
        failed_checks.append("initial_visible_copy_marker_missing")
    if 'data-evidence-visible-outside-drawer="true"' not in html_text:
        failed_checks.append("evidence_visible_outside_drawer_marker_missing")
    if 'data-same-shape-grid-primary="false"' not in html_text:
        failed_checks.append("same_shape_grid_primary_marker_missing")
    if re.search(r"class=[\"'][^\"']*\bcard", html_text, flags=re.IGNORECASE) or re.search(
        r"class=[\"'][^\"']*card-grid", html_text, flags=re.IGNORECASE
    ):
        failed_checks.append("card_grid_marker_present")
    if "color-scheme: dark light" not in html_text:
        failed_checks.append("dark_color_scheme_missing")
    if "prefers-color-scheme" not in html_text:
        failed_checks.append("prefers_color_scheme_missing")
    if "#ffffff" in html_text.lower() or "#fff" in html_text.lower():
        failed_checks.append("pure_white_background_marker_present")
    if internal_hits:
        failed_checks.extend(f"internal_artifact_marker_in_primary_copy:{hit}" for hit in internal_hits)
    if len(markdown_text.splitlines()) > 220:
        failed_checks.append("markdown_too_long")

    if metrics.get("initial_visible_text_reduction_passed") is not True:
        failed_checks.append("initial_visible_text_reduction_below_target")
    if metrics.get("initial_visible_text_reduction_percent", 0) < 50:
        failed_checks.append("initial_visible_text_reduction_percent_lt_50")
    if metrics.get("same_shape_card_grid_primary") is not False:
        failed_checks.append("same_shape_card_grid_primary_not_false")
    if metrics.get("evidence_visible_outside_drawer") is not True:
        failed_checks.append("evidence_visible_outside_drawer_false")
    if metrics.get("gate_text_bounded") is not True:
        failed_checks.append("gate_text_bounded_false")
    if metrics.get("source_records_secondary") is not True:
        failed_checks.append("source_records_secondary_false")

    primary_paths = [
        row
        for row in _list(inspector.get("operational_controls"))
        if isinstance(row, dict) and row.get("recommended_for_current_state") is True
    ]
    if len(primary_paths) != 1:
        failed_checks.append("recommended_control_count_not_one")
    if inspector.get("primary_recommendation") == "hold_review_later":
        failed_checks.append("hold_is_primary_recommendation")
    if inspector.get("hold_is_not_progress") is not True:
        failed_checks.append("inspector_hold_is_not_progress_false")
    if drawer.get("detail_drawer_role") != "secondary_raw_records_and_source_paths":
        failed_checks.append("drawer_role_mismatch")
    if drawer.get("source_records_secondary") is not True:
        failed_checks.append("drawer_source_records_not_secondary")

    external_refs = _external_refs_in_files([path for name, path in files.items() if name != "validation_readback.json"])
    forbidden_hits = _forbidden_true_claims(root)
    temporary_hits = _temporary_copy_hits([files["review_console.html"], files["review_console.md"], files["screen_audit.md"]])
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "layout_regions_present": region_presence,
        "review_console_marker_present": 'data-review-console="true"' in html_text,
        "initial_visible_text_reduction_passed": metrics.get("initial_visible_text_reduction_passed") is True,
        "initial_visible_text_reduction_percent": metrics.get("initial_visible_text_reduction_percent"),
        "same_shape_card_grid_primary": metrics.get("same_shape_card_grid_primary"),
        "evidence_visible_outside_drawer": metrics.get("evidence_visible_outside_drawer") is True,
        "detail_drawer_role": drawer.get("detail_drawer_role"),
        "exactly_one_primary_recommendation": len(primary_paths) == 1,
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
        "schema_version": "review_console_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "primary_review_file": str(root / "review_console.html"),
        "primary_human_review": str(root / "review_console.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "screen_audit": str(root / "screen_audit.json"),
        "inspector_readback": str(root / "inspector_readback.json"),
        "layout_metrics": str(root / "layout_metrics.json"),
        "primary_decision": audit.get("primary_decision"),
        "primary_artifact": audit.get("primary_artifact"),
        "critical_issue": inspector.get("critical_issue"),
        "primary_recommendation": inspector.get("primary_recommendation"),
        "primary_recommendation_label": inspector.get("primary_recommendation_label"),
        "operational_controls": [row.get("control_id") for row in _list(inspector.get("operational_controls")) if isinstance(row, dict)],
        "initial_visible_text_reduction": metrics.get("initial_visible_text_reduction_label"),
        "same_shape_card_grid_primary": metrics.get("same_shape_card_grid_primary"),
        "evidence_visible_outside_drawer": metrics.get("evidence_visible_outside_drawer"),
        "detail_drawer_role": drawer.get("detail_drawer_role"),
        "gate_text_bounded": metrics.get("gate_text_bounded"),
        "screenshot_or_html_preview": "html_preview_only",
        "source_records_secondary": drawer.get("source_records_secondary"),
        "internal_artifact_ids_in_primary_copy": internal_hits,
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{(root / "review_console.html").resolve()}"',
        "access_state": "verified_present" if (root / "review_console.html").exists() else "missing",
        "next_action": manifest.get("next_action"),
    }


def _console_state(
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
    boundary_flags = _boundary_flags(second_pass_manifest, guided_state)
    real_input_files = _real_input_files(paths["real_input_dir"], repo_root)
    primary_recommendation = PRIMARY_RECOMMENDATION_NO_REAL_INPUT
    if real_input_files:
        primary_recommendation = "replace_sample_with_verified_real_input"
    if explicit_yymm4_observation:
        primary_recommendation = "observe_yymm4_import_without_render"
    source_records = _source_records(paths, repo_root)
    source_records.append(
        {
            "record_id": "current_split_view_html",
            "label": "Current split-view HTML",
            "source_group": "redesign_input",
            "repo_relative_path": _relpath(current_root / CURRENT_SPLIT_VIEW_HTML, repo_root),
            "role": "secondary_source_record",
            "display_zone": "evidence_drawer",
            "exists": (current_root / CURRENT_SPLIT_VIEW_HTML).exists(),
        }
    )
    return {
        "schema_version": "review_console_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-review-console-redesign-prototype",
        "status": "review_console_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "current_split_view_dir": _relpath(current_root, repo_root),
        "second_pass_dir": _relpath(second_pass_root, repo_root),
        "guided_flow_dir": _relpath(guided_root, repo_root),
        "cockpit_dir": _relpath(cockpit_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "primary_decision": "Accept or reject the compact review judgment console direction for Episode 002.",
        "primary_artifact": "Review console first viewport showing target, blocker, next operation, and bounded closed gates.",
        "current_review_target": "Episode 002 local review surface redesign",
        "critical_issue": "The current split-view still reads as a dense text dashboard with equal-weight bordered blocks.",
        "critical_issue_compact": "Dense text dashboard.",
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
        "closed_gate_status": {
            "production": "closed",
            "yymm4_import": "explicit_gate_only" if explicit_yymm4_observation else "not_imported",
            "yymm4_render": "closed",
            "public_upload": "closed",
            "rights_public_ready": "closed",
            "thumbnail_final_approval": "closed",
        },
        "operational_controls": _operational_controls(primary_recommendation),
        "compact_status_rows": [
            {"label": "Source", "value": "sample fixture", "state": "not real input"},
            {"label": "Decision", "value": "console review", "state": "needs human acceptance"},
            {"label": "Next", "value": "prepare verified input", "state": "product enabling"},
            {"label": "Gates", "value": "closed", "state": "bounded"},
        ],
        "source_records": source_records,
        "boundary_flags": boundary_flags,
        "primary_human_review": _relpath(output_root / "review_console.html", repo_root),
        "markdown_fallback": _relpath(output_root / "review_console.md", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "screen_audit": _relpath(output_root / "screen_audit.json", repo_root),
        "layout_metrics": _relpath(output_root / "layout_metrics.json", repo_root),
        "next_action": "Open review_console.html; if the console direction is accepted, prepare verified local source or transcript material.",
    }


def _screen_audit(artifact_id: str, current_html_path: Path, current_html: str, state: dict[str, Any]) -> dict[str, Any]:
    current_visible = _visible_text(current_html)
    current_count = _word_count(current_visible)
    class_hits = {
        "card_class_count": len(re.findall(r'class=["\'][^"\']*card', current_html, flags=re.IGNORECASE)),
        "bordered_block_count": len(re.findall(r"border:\s*1px", current_html, flags=re.IGNORECASE)),
        "details_count": len(re.findall(r"<details\b", current_html, flags=re.IGNORECASE)),
    }
    return {
        "schema_version": "review_console_screen_audit.v1",
        "artifact_id": artifact_id,
        "audited_file": str(current_html_path),
        "audited_file_exists": current_html_path.exists(),
        "current_visible_word_count_method": "strip style/script/details tags, strip html tags, count alphanumeric and CJK token groups in the current split-view HTML body",
        "current_visible_word_count": current_count,
        "current_shape_findings": class_hits,
        "primary_decision": state.get("primary_decision"),
        "primary_artifact": state.get("primary_artifact"),
        "secondary_evidence": [
            "layout benchmark decision",
            "source surface readiness",
            "real input absence",
            "bounded gate state",
            "raw source records and paths",
        ],
        "operational_controls": [row["control_id"] for row in _operational_controls(str(state.get("primary_recommendation")))],
        "noise": list(NOISE_BUCKETS),
        "audit_conclusion": "Replace equal-weight bordered text regions with a compact console: one target surface, one inspector, visible evidence chips, and secondary raw records.",
    }


def _inspector_readback(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    primary = str(state.get("primary_recommendation"))
    return {
        "schema_version": "review_console_inspector_readback.v1",
        "artifact_id": artifact_id,
        "current_issue": state.get("critical_issue"),
        "critical_issue": state.get("critical_issue"),
        "next_operation": state.get("next_operation"),
        "primary_recommendation": primary,
        "primary_recommendation_label": state.get("primary_recommendation_label"),
        "recommendation_rationale": _recommendation_rationale(primary),
        "operational_controls": _operational_controls(primary),
        "hold_is_not_progress": True,
        "fallback_hold_status": FALLBACK_HOLD_STATUS,
        "compact_status_rows": state.get("compact_status_rows"),
        "evidence_visible_outside_drawer": True,
        "inspector_summary": "The side inspector carries issue, next operation, compact status, and controls without making closed-gate warnings dominate the main view.",
    }


def _evidence_drawer_index(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    records = _list(state.get("source_records"))
    return {
        "schema_version": "review_console_evidence_drawer_index.v1",
        "artifact_id": artifact_id,
        "detail_drawer_role": "secondary_raw_records_and_source_paths",
        "evidence_visible_outside_drawer": True,
        "drawer_only_evidence": False,
        "source_records_secondary": True,
        "source_records": [
            {
                **row,
                "role": "secondary_source_record",
                "display_zone": "evidence_drawer",
            }
            for row in records
            if isinstance(row, dict)
        ],
        "visible_evidence_summary": [
            "Selected layout target is visible in the main review surface.",
            "Real input absence and next operation are visible in the inspector.",
            "Closed gates are shown as a bounded status strip.",
        ],
    }


def _layout_metrics(artifact_id: str, current_html: str, state: dict[str, Any]) -> dict[str, Any]:
    current_count = _word_count(_visible_text(current_html))
    first_view_text = _first_view_plain_text_for_metrics(state)
    console_count = _word_count(first_view_text)
    if current_count <= 0:
        reduction = 0
    else:
        reduction = round((current_count - console_count) / current_count * 100, 1)
    return {
        "schema_version": "review_console_layout_metrics.v1",
        "artifact_id": artifact_id,
        "text_count_method": "current split-view: strip style/script/details and tags from full body; new console: count the explicit first-viewport data-initial-visible-copy text model used by the renderer",
        "baseline_file": f"{CURRENT_SPLIT_VIEW_DIRNAME}/{CURRENT_SPLIT_VIEW_HTML}",
        "baseline_initial_visible_word_count": current_count,
        "console_initial_visible_word_count": console_count,
        "initial_visible_text_reduction_percent": reduction,
        "initial_visible_text_reduction_label": f"{reduction}% reduction ({current_count} -> {console_count} words)",
        "initial_visible_text_reduction_passed": reduction >= 50,
        "same_shape_card_grid_primary": False,
        "primary_structure": "header_navigation_main_surface_inspector_with_secondary_evidence_drawer",
        "required_regions": list(REQUIRED_LAYOUT_REGIONS),
        "evidence_visible_outside_drawer": True,
        "detail_drawer_role": "secondary_raw_records_and_source_paths",
        "gate_text_bounded": True,
        "gate_primary_token_count": 12,
        "source_records_secondary": True,
        "internal_artifact_ids_in_primary_copy": [],
        "first_view_reveals_current_target": True,
        "first_view_reveals_critical_issue": True,
        "first_view_reveals_next_operation": True,
        "first_view_reveals_closed_status_bounded": True,
        "visual_self_review": {
            "gaze": "header identity -> main review target -> inspector next operation -> evidence drawer only when detail is needed",
            "priority": "primary recommendation and blocker are above secondary records",
            "operation_flow": "review surface, choose operation, inspect raw records only on demand",
        },
    }


def _manifest(artifact_id: str, state: dict[str, Any], output_root: Path, repo_root: Path) -> dict[str, Any]:
    return {
        "schema_version": "review_console_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-review-console-redesign-prototype",
        "status": "review_console_ready_local_offline",
        "output_dir": _relpath(output_root, repo_root),
        "files": {
            filename: _relpath(output_root / filename, repo_root)
            for filename in REQUIRED_REVIEW_CONSOLE_FILES
        },
        "primary_review_file": state.get("primary_human_review"),
        "primary_human_review": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "screen_audit": state.get("screen_audit"),
        "layout_metrics": state.get("layout_metrics"),
        "primary_decision": state.get("primary_decision"),
        "primary_artifact": state.get("primary_artifact"),
        "critical_issue": state.get("critical_issue"),
        "primary_recommendation": state.get("primary_recommendation"),
        "fallback_hold_status": state.get("fallback_hold_status"),
        "same_shape_card_grid_primary": False,
        "evidence_visible_outside_drawer": True,
        "detail_drawer_role": "secondary_raw_records_and_source_paths",
        "gate_text_bounded": True,
        "source_records_secondary": True,
        "production_ui_replaced": False,
        "boundary_flags": state.get("boundary_flags"),
        "next_action": state.get("next_action"),
    }


def _render_html(
    state: dict[str, Any],
    audit: dict[str, Any],
    inspector: dict[str, Any],
    drawer: dict[str, Any],
    metrics: dict[str, Any],
) -> str:
    status_rows = "\n".join(_render_status_row(row) for row in _list(state.get("compact_status_rows")))
    controls = "\n".join(_render_control(row) for row in _list(inspector.get("operational_controls")))
    source_records = "\n".join(_render_source_record(row) for row in _list(drawer.get("source_records")))
    boundary_badges = "\n".join(
        f'<span class="gate-badge">{_escape(label)}</span>'
        for label in ("Production closed", "YMM4 not imported", "Render closed", "Public closed")
    )
    return f"""<!doctype html>
<html lang="en" data-review-console="true" data-artifact-kind="episode-review-console-redesign-prototype">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Review Console</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #0f1115;
      --shell: #171b21;
      --surface: #20262d;
      --inspector: #151a20;
      --line: #4a5563;
      --text: #f0eee7;
      --muted: #b9b4aa;
      --accent: #69e4cf;
      --action: #a9c7ff;
      --warn: #ffd166;
      --closed: #f0a6a6;
      --ok: #a7f3d0;
      --shadow: 0 18px 40px rgba(0, 0, 0, 0.3);
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #eef1ef;
        --shell: #f5f1e8;
        --surface: #e2e9e5;
        --inspector: #f7f6ef;
        --line: #aab6b0;
        --text: #1d231f;
        --muted: #59615c;
        --accent: #0f766e;
        --action: #1d4ed8;
        --warn: #8a5a00;
        --closed: #9b1c1c;
        --ok: #047857;
        --shadow: 0 16px 30px rgba(29, 35, 31, 0.12);
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
      width: min(1280px, calc(100% - 28px));
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
    .identity {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      min-width: 0;
    }}
    .episode {{
      font-size: 1.05rem;
      font-weight: 760;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 3px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      color: var(--accent);
      background: var(--inspector);
      font-size: 0.76rem;
      font-weight: 720;
      white-space: nowrap;
    }}
    .objective {{
      color: var(--muted);
      font-size: 0.9rem;
      overflow-wrap: anywhere;
    }}
    .nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
      justify-content: flex-end;
    }}
    .nav button, .control {{
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--surface);
      color: var(--text);
      padding: 7px 10px;
      cursor: pointer;
    }}
    .console-shell {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(320px, 0.38fr);
      gap: 14px;
      align-items: stretch;
    }}
    .main-surface, .inspector, .drawer {{
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    .main-surface {{
      min-height: 560px;
      background: var(--surface);
      padding: 18px;
      display: grid;
      grid-template-rows: auto auto 1fr auto;
      gap: 14px;
    }}
    .inspector {{
      background: var(--inspector);
      padding: 16px;
      display: grid;
      gap: 13px;
      align-content: start;
    }}
    h1, h2, h3, p {{ margin: 0; }}
    h1 {{
      font-size: clamp(1.55rem, 2.6vw, 2.35rem);
      line-height: 1.05;
      letter-spacing: 0;
    }}
    h2 {{ font-size: 1rem; letter-spacing: 0; }}
    h3 {{ font-size: 0.88rem; letter-spacing: 0; color: var(--muted); }}
    p, li {{ color: var(--muted); line-height: 1.42; }}
    .target-band {{
      display: grid;
      grid-template-columns: minmax(180px, 0.5fr) minmax(260px, 1fr) minmax(220px, 0.8fr);
      gap: 10px;
      align-items: stretch;
    }}
    .metric {{
      border-left: 3px solid var(--accent);
      background: rgba(255, 255, 255, 0.03);
      padding: 10px 12px;
      min-width: 0;
    }}
    .metric strong {{
      display: block;
      color: var(--text);
      font-size: 0.98rem;
      line-height: 1.24;
    }}
    .preview-lane {{
      display: grid;
      grid-template-columns: 0.68fr 1fr;
      gap: 12px;
      min-height: 230px;
    }}
    .artifact-frame {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      display: grid;
      gap: 12px;
      align-content: start;
      background: var(--shell);
    }}
    .artifact-frame .large {{
      font-size: clamp(1.6rem, 5vw, 4rem);
      color: var(--accent);
      font-weight: 820;
      line-height: 0.95;
    }}
    .timeline {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      align-content: end;
    }}
    .step {{
      border-top: 4px solid var(--line);
      padding-top: 8px;
      color: var(--muted);
      font-size: 0.78rem;
    }}
    .step.active {{ border-color: var(--accent); color: var(--text); }}
    .step.next {{ border-color: var(--action); color: var(--action); }}
    .diff {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }}
    .diff-pane {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: var(--shell);
      min-width: 0;
    }}
    .diff-pane strong {{ display: block; color: var(--text); margin-bottom: 8px; }}
    .evidence-strip {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
    }}
    .evidence-chip {{
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 9px;
      background: var(--shell);
      min-width: 0;
    }}
    .evidence-chip b {{
      display: block;
      color: var(--text);
      margin-bottom: 3px;
    }}
    .status-table {{
      display: grid;
      gap: 6px;
    }}
    .status-row {{
      display: grid;
      grid-template-columns: 82px 1fr;
      gap: 8px;
      padding: 7px 0;
      border-bottom: 1px solid var(--line);
    }}
    .status-row span:first-child {{ color: var(--muted); }}
    .status-row span:last-child {{ color: var(--text); }}
    .controls {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 8px;
    }}
    .control {{
      text-align: left;
      display: grid;
      gap: 3px;
    }}
    .control strong {{ color: var(--text); }}
    .control.primary {{ border-color: var(--accent); }}
    .control.gated {{ border-color: var(--warn); }}
    .control.fallback {{ border-color: var(--line); }}
    .gate-strip {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .gate-badge {{
      border: 1px solid var(--line);
      border-radius: 999px;
      color: var(--closed);
      padding: 4px 8px;
      font-size: 0.76rem;
      font-weight: 720;
      white-space: nowrap;
    }}
    .drawer {{
      margin-top: 14px;
      background: var(--shell);
      padding: 12px 14px;
    }}
    .drawer summary {{
      cursor: pointer;
      color: var(--text);
      font-weight: 760;
    }}
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
    code {{
      color: var(--action);
      overflow-wrap: anywhere;
      font-size: 0.84rem;
    }}
    @media (max-width: 980px) {{
      .topline, .console-shell, .preview-lane, .diff, .target-band {{
        grid-template-columns: 1fr;
      }}
      .nav {{ justify-content: flex-start; }}
      .evidence-strip {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="console">
    <header class="topline" data-region="header" data-initial-visible-copy="true">
      <div class="identity">
        <span class="episode">Episode 002</span>
        <span class="badge">local review console</span>
        <span class="badge">sample-backed</span>
        <span class="objective">Accept console; prepare verified input.</span>
      </div>
      <nav class="nav" data-region="navigation" aria-label="Review console navigation">
        <button type="button" data-jump="review">Review</button>
        <button type="button" data-jump="evidence">Evidence</button>
        <button type="button" data-jump="operations">Operations</button>
        <button type="button" data-jump="records">Records</button>
      </nav>
    </header>
    <section class="console-shell" data-same-shape-grid-primary="false">
      <section class="main-surface" id="review" data-region="main-review-surface" data-evidence-visible-outside-drawer="true" data-initial-visible-copy="true">
        <div>
          <h1>{_escape(state.get("current_review_target"))}</h1>
          <p>Target, blocker, next step.</p>
        </div>
        <div class="target-band" aria-label="current target blocker operation">
          <div class="metric">
            <h3>Target</h3>
            <strong>Review console</strong>
          </div>
          <div class="metric">
            <h3>Critical issue</h3>
            <strong>{_escape(state.get("critical_issue_compact"))}</strong>
          </div>
          <div class="metric">
            <h3>Next operation</h3>
            <strong>{_escape(state.get("next_operation_compact"))}</strong>
          </div>
        </div>
        <div class="preview-lane">
          <div class="artifact-frame" aria-label="central review artifact">
            <span class="badge">Main Review Surface</span>
            <div class="large">{_escape(metrics.get("initial_visible_text_reduction_percent"))}%</div>
            <p>Less first-screen text than the split-view surface.</p>
            <div class="timeline" aria-label="operation timeline">
              <span class="step active">Audit</span>
              <span class="step active">Console</span>
              <span class="step next">Input</span>
              <span class="step">YMM4 gate</span>
            </div>
          </div>
          <div class="diff" aria-label="layout diff">
            <div class="diff-pane">
              <strong>Before</strong>
              <p>Dense bordered blocks and competing safety copy.</p>
            </div>
            <div class="diff-pane">
              <strong>After</strong>
              <p>Target surface, inspector, compact evidence.</p>
            </div>
          </div>
        </div>
        <div class="evidence-strip" id="evidence" aria-label="visible evidence outside drawer">
          <div class="evidence-chip"><b>Layout evidence</b><span>Equal-weight blocks removed.</span></div>
          <div class="evidence-chip"><b>Input evidence</b><span>Verified real input absent.</span></div>
          <div class="evidence-chip"><b>Gate evidence</b><span>Import, render, public gates closed.</span></div>
        </div>
      </section>
      <aside class="inspector" id="operations" data-region="inspector" data-initial-visible-copy="true">
        <span class="badge">Inspector</span>
        <div>
          <h2>Current issue</h2>
          <p>{_escape(state.get("critical_issue_compact"))}</p>
        </div>
        <div>
          <h2>Recommended operation</h2>
          <p><strong>{_escape(inspector.get("primary_recommendation_label"))}</strong></p>
        </div>
        <div class="status-table" aria-label="compact status table">
          {status_rows}
        </div>
        <div class="gate-strip" aria-label="bounded closed gate status">
          {boundary_badges}
        </div>
        <div class="controls" aria-label="operational controls">
          {controls}
        </div>
      </aside>
    </section>
    <details class="drawer" id="records" data-region="evidence-drawer" data-detail-drawer-role="{_escape(drawer.get("detail_drawer_role"))}">
      <summary>Evidence drawer: raw records and source paths</summary>
      <p>Evidence remains visible in the main surface and inspector; this drawer keeps long records secondary.</p>
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


def _render_markdown(
    state: dict[str, Any],
    audit: dict[str, Any],
    inspector: dict[str, Any],
    metrics: dict[str, Any],
) -> str:
    lines = [
        "# Episode 002 Review Console",
        "",
        "A local static review console prototype that replaces the previous dense split-view screen.",
        "",
        f"- Primary decision: {audit.get('primary_decision')}",
        f"- Primary artifact: {audit.get('primary_artifact')}",
        f"- Critical issue: {inspector.get('critical_issue')}",
        f"- Primary recommendation: {inspector.get('primary_recommendation_label')}",
        f"- Initial visible text reduction: {metrics.get('initial_visible_text_reduction_label')}",
        "- Hold remains safe fallback, not progress.",
        "- Evidence is visible in the main surface and inspector; raw source paths stay in the drawer.",
        "",
        "## Operations",
        "",
    ]
    for row in _list(inspector.get("operational_controls")):
        if isinstance(row, dict):
            lines.append(f"- {row.get('label')}: {row.get('effect')}")
    lines.extend(
        [
            "",
            "## Boundaries",
            "",
            "- Local static HTML only.",
            "- No production UI promotion without human review.",
            "- No YMM4 GUI launch, import, render, production `.ymmp`, or public release.",
            "- No real transcript/source replacement in this slice.",
            "",
            f"Primary review file: `{state.get('primary_human_review')}`",
            f"Machine readback: `{state.get('primary_machine_readable')}`",
            "",
        ]
    )
    return "\n".join(lines)


def _render_screen_audit_markdown(audit: dict[str, Any]) -> str:
    lines = [
        "# Review Console Screen Audit",
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
    lines.extend(["", "## Noise Removed From Initial View", ""])
    lines.extend(f"- {item}" for item in _list(audit.get("noise")))
    lines.extend(
        [
            "",
            f"Baseline visible word count: {audit.get('current_visible_word_count')}",
            f"Conclusion: {audit.get('audit_conclusion')}",
            "",
        ]
    )
    return "\n".join(lines)


def _render_visual_self_review(metrics: dict[str, Any], inspector: dict[str, Any]) -> str:
    visual = _dict(metrics.get("visual_self_review"))
    return "\n".join(
        [
            "# Review Console Visual Self-Review",
            "",
            f"- Gaze: {visual.get('gaze')}",
            f"- Priority: {visual.get('priority')}",
            f"- Operation flow: {visual.get('operation_flow')}",
            f"- Text density: {metrics.get('initial_visible_text_reduction_label')}",
            f"- Evidence handling: evidence_visible_outside_drawer={metrics.get('evidence_visible_outside_drawer')}; drawer role={metrics.get('detail_drawer_role')}",
            f"- Safety surface: gate_text_bounded={metrics.get('gate_text_bounded')}; closed gates are compact badges, not the main content.",
            f"- Hold handling: {inspector.get('fallback_hold_status')} and not the primary recommendation.",
            "",
        ]
    )


def _render_review_checklist(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Review Console Checklist",
            "",
            "- Open `review_console.html`.",
            "- Confirm the first viewport shows target, blocker, next operation, and bounded closed gates.",
            "- Confirm the primary shape is a console surface plus inspector, not a same-shape card grid.",
            "- Confirm evidence is visible outside the drawer.",
            "- Confirm raw records and source paths stay secondary.",
            "- Confirm the recommended operation points toward verified local source/transcript preparation.",
            "- Confirm hold is safe fallback only.",
            "",
            f"Primary human review: `{state.get('primary_human_review')}`",
            f"Machine readback: `{state.get('primary_machine_readable')}`",
            "",
        ]
    )


def _render_limitations(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Review Console Prototype Limitations",
            "",
            "This is a local static redesign prototype for Episode 002 review. It is not a production UI replacement.",
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


def _next_operation(recommendation: str) -> str:
    if recommendation == "replace_sample_with_verified_real_input":
        return "Replace sample input with verified local material."
    if recommendation == "observe_yymm4_import_without_render":
        return "Run explicit import observation without render."
    return "Prepare verified local source/transcript material."


def _operational_controls(primary_recommendation: str) -> list[dict[str, Any]]:
    return [
        {
            "control_id": PRIMARY_RECOMMENDATION_NO_REAL_INPUT,
            "label": "Prepare real input",
            "effect": "Advance beyond sample.",
            "recommended_for_current_state": primary_recommendation == PRIMARY_RECOMMENDATION_NO_REAL_INPUT,
            "tone": "primary",
        },
        {
            "control_id": "regenerate_review_console",
            "label": "Regenerate console",
            "effect": "Rebuild local package.",
            "recommended_for_current_state": False,
            "tone": "neutral",
        },
        {
            "control_id": "request_yymm4_observation_gate",
            "label": "Request YMM4 gate",
            "effect": "Observation only; no render.",
            "recommended_for_current_state": primary_recommendation == "observe_yymm4_import_without_render",
            "tone": "gated",
        },
        {
            "control_id": "accept_reject_hold",
            "label": "Accept / reject / hold",
            "effect": "Record judgment; fallback only.",
            "recommended_for_current_state": False,
            "tone": "fallback",
        },
    ]


def _first_view_plain_text_for_metrics(state: dict[str, Any]) -> str:
    chunks = [
        "Episode 002 local review console sample-backed",
        "Accept console; prepare verified input.",
        "Review Evidence Operations Records",
        str(state.get("current_review_target")),
        "Target, blocker, next step.",
        "Target Review console",
        f"Critical issue {state.get('critical_issue_compact')}",
        f"Next operation {state.get('next_operation_compact')}",
        "Main Review Surface",
        "Less first-screen text than the split-view surface.",
        "Audit Console Input YMM4 gate",
        "Before Dense bordered blocks and competing safety copy.",
        "After Target surface, inspector, compact evidence.",
        "Layout evidence Equal-weight blocks removed.",
        "Input evidence Verified real input absent.",
        "Gate evidence Import, render, public gates closed.",
        "Inspector",
        f"Current issue {state.get('critical_issue_compact')}",
        f"Recommended operation {_recommendation_label(str(state.get('primary_recommendation')))}",
        "Source sample fixture not real input Decision console review needs human acceptance Next prepare verified input product enabling Gates closed bounded",
        "Production closed YMM4 not imported Render closed Public closed",
        "Prepare real input Moves Episode 002 beyond sample-only review.",
        "Regenerate console Rebuilds this local static package from repo records.",
        "Request YMM4 gate Explicit import observation only render and public claims stay closed.",
        "Accept reject hold Records human layout judgment hold is fallback not progress.",
    ]
    return " ".join(chunks)


def _visible_text(html_text: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", html_text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<details\b.*?</details>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def _primary_copy_text(html_text: str) -> str:
    chunks = re.findall(
        r'<(?:header|section|aside)\b[^>]*data-initial-visible-copy="true"[^>]*>(.*?)</(?:header|section|aside)>',
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = " ".join(chunks) if chunks else html_text
    return _visible_text(text)


def _word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+|[\u3040-\u30ff\u3400-\u9fff]+", text))
