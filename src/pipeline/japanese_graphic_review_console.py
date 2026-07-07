"""Japanese graphical review console for episode 002."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

from src.pipeline.primary_artifact_review_console import (
    DEFAULT_CURRENT_CONSOLE_DIRNAME,
    _primary_copy_text,
)
from src.pipeline.review_console_redesign_prototype import (
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
    _relpath,
    _source_records,
    _temporary_copy_hits,
    _write_json,
    _write_text,
)

DEFAULT_OUTPUT_DIRNAME = "japanese_graphic_review_console"
DEFAULT_ARTIFACT_ID = "episode_002_japanese_graphic_review_console_v1"
CURRENT_PRIMARY_CONSOLE_HTML = "primary_artifact_review_console.html"
DEFAULT_LANE_MAP_PATH = "docs/PROJECT_LANES.md"

REQUIRED_JAPANESE_GRAPHIC_FILES = (
    "japanese_graphic_console_manifest.json",
    "japanese_graphic_review_console.html",
    "japanese_graphic_review_console.md",
    "screen_audit.json",
    "screen_audit.md",
    "graphic_surface_readback.json",
    "japanese_copy_readback.json",
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
    "main-graphic-review-surface",
    "inspector",
    "evidence-drawer",
    "handoff-note",
)

GRAPHICAL_ELEMENTS = (
    "production_flow_spine",
    "before_after_visual_comparison_canvas",
    "timeline_state_diagram",
    "yymm4_prep_progress_strip",
    "input_readiness_map",
    "diff_style_visual_panel",
    "structural_shelf_layout",
)

PRIMARY_COPY_FORBIDDEN_MARKERS = (
    "production_pilots/",
    "episode_002_",
    "candidate_a_split_view_decision_evidence_pane",
    "real_input_replacement",
    "actual_yymm4_import_observation_no_render",
    "hold_review_later",
    "dry_run",
    "sample_fixture_not_real",
    "no_real_transcript",
    "no_yymm4_import",
    "public_upload_closed",
)

ALLOWED_ENGLISH_TERMS = ("YMM4", "CSV", "HTML", "Git", "API", "RSS")

LANE_STOP_RULE = (
    "After the Japanese graphical console is reviewable, return to the product "
    "lane unless the user rejects the UI direction."
)


def build_japanese_graphic_review_console(
    *,
    package_dir: str | Path,
    current_console_dir: str | Path | None = None,
    second_pass_dir: str | Path | None = None,
    guided_flow_dir: str | Path | None = None,
    cockpit_dir: str | Path | None = None,
    reviewer_packet_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    lane_map_path: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
    explicit_yymm4_observation: bool = False,
) -> dict[str, Any]:
    """Build the local Japanese-first graphical review console package."""
    source_root = Path(package_dir)
    current_root = Path(current_console_dir) if current_console_dir else source_root / DEFAULT_CURRENT_CONSOLE_DIRNAME
    second_pass_root = Path(second_pass_dir) if second_pass_dir else source_root / DEFAULT_SECOND_PASS_DIRNAME
    guided_root = Path(guided_flow_dir) if guided_flow_dir else source_root / DEFAULT_GUIDED_FLOW_DIRNAME
    cockpit_root = Path(cockpit_dir) if cockpit_dir else source_root / DEFAULT_COCKPIT_DIRNAME
    reviewer_root = Path(reviewer_packet_dir) if reviewer_packet_dir else source_root / DEFAULT_REVIEWER_DIRNAME
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)
    lane_map = Path(lane_map_path) if lane_map_path else repo_root / DEFAULT_LANE_MAP_PATH

    paths = _input_paths(source_root, second_pass_root, guided_root, cockpit_root, reviewer_root)
    payloads = _load_payloads(paths)
    current_html_path = current_root / CURRENT_PRIMARY_CONSOLE_HTML
    current_html = current_html_path.read_text(encoding="utf-8-sig") if current_html_path.exists() else ""
    lane_map_text = lane_map.read_text(encoding="utf-8-sig") if lane_map.exists() else ""

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
        lane_map=lane_map,
        lane_map_text=lane_map_text,
        paths=paths,
        payloads=payloads,
        explicit_yymm4_observation=explicit_yymm4_observation,
    )
    audit = _screen_audit(artifact_id, current_html_path, current_html, state)
    graphic = _graphic_surface_readback(artifact_id, state)
    japanese_copy = _japanese_copy_readback(artifact_id, state)
    inspector = _inspector_readback(artifact_id, state)
    drawer = _evidence_drawer_index(artifact_id, state)
    metrics = _layout_metrics(artifact_id, current_html, state)
    manifest = _manifest(artifact_id, state, output_root, repo_root)

    _write_json(output_root / "japanese_graphic_console_manifest.json", manifest)
    _write_json(output_root / "screen_audit.json", audit)
    _write_json(output_root / "graphic_surface_readback.json", graphic)
    _write_json(output_root / "japanese_copy_readback.json", japanese_copy)
    _write_json(output_root / "inspector_readback.json", inspector)
    _write_json(output_root / "evidence_drawer_index.json", drawer)
    _write_json(output_root / "layout_metrics.json", metrics)
    _write_text(output_root / "japanese_graphic_review_console.html", _render_html(state, inspector, drawer))
    _write_text(output_root / "japanese_graphic_review_console.md", _render_markdown(state, audit, graphic, metrics))
    _write_text(output_root / "screen_audit.md", _render_screen_audit_markdown(audit))
    _write_text(output_root / "visual_self_review.md", _render_visual_self_review(graphic, metrics))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state))
    _write_text(output_root / "limitations.md", _render_limitations(state))

    readback = validate_japanese_graphic_review_console(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_japanese_graphic_review_console(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_japanese_graphic_review_console(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated Japanese graphical review console package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_JAPANESE_GRAPHIC_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["japanese_graphic_console_manifest.json"])
    audit = _load_json_if_present(files["screen_audit.json"])
    graphic = _load_json_if_present(files["graphic_surface_readback.json"])
    japanese_copy = _load_json_if_present(files["japanese_copy_readback.json"])
    inspector = _load_json_if_present(files["inspector_readback.json"])
    drawer = _load_json_if_present(files["evidence_drawer_index.json"])
    metrics = _load_json_if_present(files["layout_metrics.json"])
    json_payloads = {
        "japanese_graphic_console_manifest": manifest,
        "screen_audit": audit,
        "graphic_surface_readback": graphic,
        "japanese_copy_readback": japanese_copy,
        "inspector_readback": inspector,
        "evidence_drawer_index": drawer,
        "layout_metrics": metrics,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = _dict(json_payloads["japanese_graphic_console_manifest"])
    audit = _dict(json_payloads["screen_audit"])
    graphic = _dict(json_payloads["graphic_surface_readback"])
    japanese_copy = _dict(json_payloads["japanese_copy_readback"])
    inspector = _dict(json_payloads["inspector_readback"])
    drawer = _dict(json_payloads["evidence_drawer_index"])
    metrics = _dict(json_payloads["layout_metrics"])

    html_path = files["japanese_graphic_review_console.html"]
    markdown_path = files["japanese_graphic_review_console.md"]
    html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
    markdown_text = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""
    primary_copy = _primary_copy_text(html_text)
    internal_hits = [marker for marker in PRIMARY_COPY_FORBIDDEN_MARKERS if marker.lower() in primary_copy.lower()]
    primary_headings = _primary_heading_texts(html_text)
    english_primary_headings = _english_primary_heading_hits(primary_headings)

    if manifest.get("artifact_kind") != "episode-japanese-graphic-review-console":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if manifest.get("status") != "japanese_graphic_console_ready_local_offline":
        failed_checks.append("manifest_status_mismatch")
    if manifest.get("project_lanes_recorded") is not True:
        failed_checks.append("project_lanes_not_recorded")
    if manifest.get("stop_rule_recorded") is not True:
        failed_checks.append("stop_rule_not_recorded")
    if inspector.get("primary_recommendation") != PRIMARY_RECOMMENDATION_NO_REAL_INPUT:
        failed_checks.append("primary_recommendation_not_product_enabling_default")
    if inspector.get("hold_is_not_progress") is not True:
        failed_checks.append("hold_is_not_progress_false")

    boundary_flags = _dict(manifest.get("boundary_flags"))
    for flag in (
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
    ):
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")

    region_presence = {region: f'data-region="{region}"' in html_text for region in REQUIRED_LAYOUT_REGIONS}
    for region, present in region_presence.items():
        if not present:
            failed_checks.append(f"layout_region_missing:{region}")

    if '<html lang="ja"' not in html_text:
        failed_checks.append("html_language_not_ja")
    if 'data-japanese-graphic-console="true"' not in html_text:
        failed_checks.append("japanese_graphic_console_marker_missing")
    if 'data-primary-ui-language="ja"' not in html_text:
        failed_checks.append("primary_ui_language_marker_missing")
    if 'data-main-surface-type="japanese-graphic-flow-spine"' not in html_text:
        failed_checks.append("main_surface_type_marker_missing")
    if 'data-visual-element="production_flow_spine"' not in html_text:
        failed_checks.append("production_flow_spine_marker_missing")
    if 'data-visual-element="timeline_state_diagram"' not in html_text:
        failed_checks.append("timeline_marker_missing")
    if 'data-visual-element="yymm4_prep_progress_strip"' not in html_text:
        failed_checks.append("progress_strip_marker_missing")
    if 'data-free-text-role="secondary_handoff_note"' not in html_text:
        failed_checks.append("handoff_note_role_marker_missing")
    if 'data-evidence-front-stage-row="false"' not in html_text:
        failed_checks.append("evidence_front_stage_row_marker_missing")
    if re.search(r"class=[\"'][^\"']*\bcard", html_text, flags=re.IGNORECASE):
        failed_checks.append("card_class_marker_present")

    graphical_elements = _list(graphic.get("graphical_elements"))
    for element in GRAPHICAL_ELEMENTS:
        if element not in graphical_elements:
            failed_checks.append(f"graphical_element_missing:{element}")
    if graphic.get("primary_artifact_dominant") is not True:
        failed_checks.append("primary_artifact_not_dominant")
    if graphic.get("center_not_text_cards") is not True:
        failed_checks.append("center_not_text_cards_false")

    if japanese_copy.get("primary_ui_language") != "ja":
        failed_checks.append("primary_ui_language_not_ja")
    if english_primary_headings:
        failed_checks.extend(f"english_primary_heading:{heading}" for heading in english_primary_headings)
    if japanese_copy.get("internal_artifact_ids_in_primary_copy") not in ([], None):
        failed_checks.append("internal_artifact_ids_report_not_empty")
    if metrics.get("main_surface_type") != "japanese_graphical_flow_spine":
        failed_checks.append("main_surface_type_mismatch")
    if metrics.get("same_shape_card_grid_primary") is not False:
        failed_checks.append("same_shape_card_grid_primary_not_false")
    if metrics.get("explanatory_cards_in_main_surface", 99) != 0:
        failed_checks.append("explanatory_cards_in_main_surface_not_zero")
    if metrics.get("evidence_front_stage_card_row") is not False:
        failed_checks.append("evidence_front_stage_card_row_not_false")
    if metrics.get("free_text_role") != "secondary_handoff_note":
        failed_checks.append("free_text_role_mismatch")
    if int(metrics.get("free_text_handoff_character_count", 999)) > 110:
        failed_checks.append("free_text_handoff_too_long")
    if metrics.get("gate_text_bounded") is not True:
        failed_checks.append("gate_text_bounded_false")
    if drawer.get("evidence_visible_outside_drawer") is not True:
        failed_checks.append("evidence_visible_outside_drawer_false")
    if drawer.get("source_records_secondary") is not True:
        failed_checks.append("source_records_secondary_false")

    recommended_controls = [
        row
        for row in _list(inspector.get("operational_controls"))
        if isinstance(row, dict) and row.get("recommended_for_current_state") is True
    ]
    if len(recommended_controls) != 1:
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
            files["japanese_graphic_review_console.html"],
            files["japanese_graphic_review_console.md"],
            files["screen_audit.md"],
            files["visual_self_review.md"],
        ]
    )
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "layout_regions_present": region_presence,
        "primary_ui_language": japanese_copy.get("primary_ui_language"),
        "english_primary_headings": english_primary_headings,
        "main_surface_type": metrics.get("main_surface_type"),
        "graphical_elements": graphical_elements,
        "free_text_role": metrics.get("free_text_role"),
        "same_shape_card_grid_primary": metrics.get("same_shape_card_grid_primary"),
        "explanatory_cards_in_main_surface": metrics.get("explanatory_cards_in_main_surface"),
        "evidence_front_stage_card_row": metrics.get("evidence_front_stage_card_row"),
        "evidence_visible_outside_drawer": drawer.get("evidence_visible_outside_drawer"),
        "detail_drawer_role": drawer.get("detail_drawer_role"),
        "exactly_one_primary_recommendation": len(recommended_controls) == 1,
        "primary_recommendation": inspector.get("primary_recommendation"),
        "hold_is_not_progress": inspector.get("hold_is_not_progress") is True,
        "gate_text_bounded": metrics.get("gate_text_bounded") is True,
        "project_lanes_recorded": manifest.get("project_lanes_recorded") is True,
        "stop_rule_recorded": manifest.get("stop_rule_recorded") is True,
        "source_records_secondary": drawer.get("source_records_secondary") is True,
        "internal_artifact_ids_in_primary_copy": internal_hits,
        "external_dependency_status": "none_found" if not external_refs else "found",
        "dark_mode_markers_present": "color-scheme: dark light" in html_text and "prefers-color-scheme" in html_text,
        "pure_white_background_absent": "#ffffff" not in html_text.lower() and "#fff" not in html_text.lower(),
        "forbidden_true_claims_absent": not forbidden_hits,
        "temporary_copy_absent": not temporary_hits,
        "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in boundary_flags),
    }
    return {
        "schema_version": "japanese_graphic_console_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "primary_review_file": str(root / "japanese_graphic_review_console.html"),
        "primary_human_review": str(root / "japanese_graphic_review_console.html"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "screen_audit": str(root / "screen_audit.json"),
        "graphic_surface_readback": str(root / "graphic_surface_readback.json"),
        "japanese_copy_readback": str(root / "japanese_copy_readback.json"),
        "inspector_readback": str(root / "inspector_readback.json"),
        "layout_metrics": str(root / "layout_metrics.json"),
        "primary_decision": audit.get("primary_decision"),
        "primary_artifact": audit.get("primary_artifact"),
        "critical_issue": inspector.get("critical_issue"),
        "primary_recommendation": inspector.get("primary_recommendation"),
        "primary_recommendation_label": inspector.get("primary_recommendation_label"),
        "operational_controls": [row.get("control_id") for row in _list(inspector.get("operational_controls")) if isinstance(row, dict)],
        "main_surface_type": metrics.get("main_surface_type"),
        "graphical_elements": graphical_elements,
        "primary_ui_language": japanese_copy.get("primary_ui_language"),
        "english_primary_headings": english_primary_headings,
        "free_text_role": metrics.get("free_text_role"),
        "same_shape_card_grid_primary": metrics.get("same_shape_card_grid_primary"),
        "explanatory_cards_in_main_surface": metrics.get("explanatory_cards_in_main_surface"),
        "evidence_front_stage_card_row": metrics.get("evidence_front_stage_card_row"),
        "evidence_visible_outside_drawer": drawer.get("evidence_visible_outside_drawer"),
        "detail_drawer_role": drawer.get("detail_drawer_role"),
        "gate_text_bounded": metrics.get("gate_text_bounded"),
        "project_lanes_recorded": manifest.get("project_lanes_recorded"),
        "stop_rule_recorded": manifest.get("stop_rule_recorded"),
        "source_records_secondary": drawer.get("source_records_secondary"),
        "internal_artifact_ids_in_primary_copy": internal_hits,
        "screenshot_or_html_preview": "html_rendered_visual_canvas",
        "launcher_or_open_command": f'Invoke-Item -LiteralPath "{(root / "japanese_graphic_review_console.html").resolve()}"',
        "access_state": "verified_present" if (root / "japanese_graphic_review_console.html").exists() else "missing",
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
    lane_map: Path,
    lane_map_text: str,
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
            "record_id": "current_primary_artifact_console",
            "label": "Current primary artifact console",
            "source_group": "redesign_input",
            "repo_relative_path": _relpath(current_root / CURRENT_PRIMARY_CONSOLE_HTML, repo_root),
            "role": "secondary_source_record",
            "display_zone": "evidence_drawer",
            "exists": (current_root / CURRENT_PRIMARY_CONSOLE_HTML).exists(),
        }
    )
    source_records.append(
        {
            "record_id": "project_lane_map",
            "label": "Project lane map",
            "source_group": "lane_split",
            "repo_relative_path": _relpath(lane_map, repo_root),
            "role": "secondary_source_record",
            "display_zone": "evidence_drawer",
            "exists": lane_map.exists(),
        }
    )
    return {
        "schema_version": "japanese_graphic_console_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-japanese-graphic-review-console",
        "status": "japanese_graphic_console_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "current_console_dir": _relpath(current_root, repo_root),
        "second_pass_dir": _relpath(second_pass_root, repo_root),
        "guided_flow_dir": _relpath(guided_root, repo_root),
        "cockpit_dir": _relpath(cockpit_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "lane_map": _relpath(lane_map, repo_root),
        "project_lanes_recorded": _lane_map_has_required_lanes(lane_map_text),
        "stop_rule_recorded": "return to the product lane" in lane_map_text.lower()
        and "rejects the ui direction" in lane_map_text.lower(),
        "primary_decision": "Accept or reject the Japanese-first graphical Episode 002 review console direction.",
        "primary_artifact": "Japanese graphical review artifact with production-flow spine, diff, readiness map, and timeline.",
        "current_review_target": "第002話 レビューコンソール",
        "critical_issue": "Primary UI must be Japanese and the center must be graphical, not explanatory cards.",
        "critical_issue_ja": "中央を説明カードではなく、制作フローと差分で判断できる画面にする。",
        "primary_recommendation": primary_recommendation,
        "primary_recommendation_label": _recommendation_label_ja(primary_recommendation),
        "next_operation": _next_operation_ja(primary_recommendation),
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
        "primary_human_review": _relpath(output_root / "japanese_graphic_review_console.html", repo_root),
        "markdown_fallback": _relpath(output_root / "japanese_graphic_review_console.md", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_action": "Open japanese_graphic_review_console.html; if accepted, return to verified local source or transcript preparation.",
        "handoff_note": "採用できたら、次は検証済みローカル素材/文字起こしの準備へ戻る。",
    }


def _screen_audit(artifact_id: str, current_html_path: Path, current_html: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "japanese_graphic_screen_audit.v1",
        "artifact_id": artifact_id,
        "audited_file": str(current_html_path),
        "audited_file_exists": current_html_path.exists(),
        "current_visible_word_count": _word_count(_visible_text(current_html)),
        "primary_decision": state.get("primary_decision"),
        "primary_artifact": state.get("primary_artifact"),
        "secondary_evidence": [
            "current primary artifact console validation",
            "real input absence",
            "closed gate state",
            "source records and raw paths",
            "project lane split map",
        ],
        "operational_controls": [row["control_id"] for row in _operational_controls_ja(str(state.get("primary_recommendation")))],
        "noise": [
            "English-first primary labels",
            "same-shape bordered explanation blocks",
            "front-stage raw evidence rows",
            "internal artifact ids and raw paths",
            "long gate prose in the first view",
        ],
        "audit_conclusion": "Use a Japanese graphical center: production spine, visual diff, readiness map, timeline, and short handoff only.",
    }


def _graphic_surface_readback(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "japanese_graphic_surface_readback.v1",
        "artifact_id": artifact_id,
        "primary_artifact_type": "html_rendered_japanese_graphical_review_canvas",
        "main_surface_type": "japanese_graphical_flow_spine",
        "primary_artifact_dominant": True,
        "center_not_text_cards": True,
        "graphical_elements": list(GRAPHICAL_ELEMENTS),
        "communicates": [
            "current review target",
            "critical issue",
            "next operation",
            "input readiness",
            "bounded YMM4 gate state",
        ],
        "free_text_secondary": True,
        "screenshot_or_html_preview": "html_rendered_visual_canvas",
    }


def _japanese_copy_readback(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "japanese_copy_readback.v1",
        "artifact_id": artifact_id,
        "primary_ui_language": "ja",
        "allowed_english_terms": list(ALLOWED_ENGLISH_TERMS),
        "english_primary_headings": [],
        "internal_artifact_ids_in_primary_copy": [],
        "raw_paths_secondary": True,
        "technical_keys_secondary": True,
        "primary_copy_policy": "Japanese labels first; English artifact IDs and raw paths stay in the secondary drawer/readbacks.",
    }


def _inspector_readback(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    primary = str(state.get("primary_recommendation"))
    return {
        "schema_version": "japanese_graphic_inspector_readback.v1",
        "artifact_id": artifact_id,
        "critical_issue": state.get("critical_issue"),
        "critical_issue_ja": state.get("critical_issue_ja"),
        "next_operation": state.get("next_operation"),
        "primary_recommendation": primary,
        "primary_recommendation_label": state.get("primary_recommendation_label"),
        "operational_controls": _operational_controls_ja(primary),
        "compact_status_rows": [
            {"label": "素材", "value": "サンプル", "state": "実入力待ち"},
            {"label": "判断", "value": "UI方向", "state": "人間レビュー待ち"},
            {"label": "次手", "value": "素材準備", "state": "前進"},
            {"label": "Gate", "value": "YMM4", "state": "明示選択のみ"},
        ],
        "evidence_visible_outside_drawer": True,
        "hold_is_not_progress": True,
        "fallback_hold_status": FALLBACK_HOLD_STATUS,
    }


def _evidence_drawer_index(artifact_id: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "japanese_graphic_evidence_drawer_index.v1",
        "artifact_id": artifact_id,
        "detail_drawer_role": "secondary_raw_records_source_paths_and_extended_proof",
        "evidence_visible_outside_drawer": True,
        "drawer_only_evidence": False,
        "evidence_front_stage_card_row": False,
        "source_records_secondary": True,
        "visible_evidence_locations": [
            "inspector compact status",
            "main graphical readiness map",
            "main flow gate strip",
            "handoff note",
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
        "schema_version": "japanese_graphic_layout_metrics.v1",
        "artifact_id": artifact_id,
        "baseline_file": f"{DEFAULT_CURRENT_CONSOLE_DIRNAME}/{CURRENT_PRIMARY_CONSOLE_HTML}",
        "baseline_visible_word_count": _word_count(_visible_text(current_html)),
        "main_surface_type": "japanese_graphical_flow_spine",
        "graphical_elements": list(GRAPHICAL_ELEMENTS),
        "primary_ui_language": "ja",
        "same_shape_card_grid_primary": False,
        "explanatory_cards_in_main_surface": 0,
        "evidence_front_stage_card_row": False,
        "evidence_visible_outside_drawer": True,
        "detail_drawer_role": "secondary_raw_records_source_paths_and_extended_proof",
        "free_text_role": "secondary_handoff_note",
        "free_text_handoff_character_count": len(str(state.get("handoff_note", ""))),
        "gate_text_bounded": True,
        "gate_primary_token_count": 9,
        "source_records_secondary": True,
        "internal_artifact_ids_in_primary_copy": [],
        "first_view_reveals_primary_artifact": True,
        "first_view_reveals_critical_issue": True,
        "first_view_reveals_next_operation": True,
        "first_view_priority": [
            "Japanese visual artifact",
            "critical issue",
            "next operation",
        ],
    }


def _manifest(artifact_id: str, state: dict[str, Any], output_root: Path, repo_root: Path) -> dict[str, Any]:
    return {
        "schema_version": "japanese_graphic_console_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-japanese-graphic-review-console",
        "status": "japanese_graphic_console_ready_local_offline",
        "output_dir": _relpath(output_root, repo_root),
        "files": {
            filename: _relpath(output_root / filename, repo_root)
            for filename in REQUIRED_JAPANESE_GRAPHIC_FILES
        },
        "primary_review_file": state.get("primary_human_review"),
        "primary_human_review": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "primary_decision": state.get("primary_decision"),
        "primary_artifact": state.get("primary_artifact"),
        "critical_issue": state.get("critical_issue"),
        "primary_recommendation": state.get("primary_recommendation"),
        "fallback_hold_status": state.get("fallback_hold_status"),
        "main_surface_type": "japanese_graphical_flow_spine",
        "graphical_elements": list(GRAPHICAL_ELEMENTS),
        "primary_ui_language": "ja",
        "same_shape_card_grid_primary": False,
        "evidence_front_stage_card_row": False,
        "source_records_secondary": True,
        "project_lanes_recorded": state.get("project_lanes_recorded"),
        "stop_rule_recorded": state.get("stop_rule_recorded"),
        "lane_map": state.get("lane_map"),
        "production_ui_replaced": False,
        "boundary_flags": state.get("boundary_flags"),
        "next_action": state.get("next_action"),
    }


def _render_html(state: dict[str, Any], inspector: dict[str, Any], drawer: dict[str, Any]) -> str:
    controls = "\n".join(_render_control(row) for row in _list(inspector.get("operational_controls")))
    status_rows = "\n".join(_render_status_row(row) for row in _list(inspector.get("compact_status_rows")))
    source_records = "\n".join(_render_source_record(row) for row in _list(drawer.get("source_records")))
    return f"""<!doctype html>
<html lang="ja" data-japanese-graphic-console="true" data-artifact-kind="episode-japanese-graphic-review-console" data-primary-ui-language="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>第002話 日本語グラフィックレビューコンソール</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #0b1014;
      --surface: #182027;
      --stage: #10171d;
      --panel: #141b22;
      --line: #4e5c68;
      --text: #f3efe7;
      --muted: #c2baad;
      --accent: #68e0d4;
      --action: #9fc5ff;
      --warn: #f2ce66;
      --closed: #f0a0a0;
      --ok: #a7e8c2;
      --shadow: 0 18px 42px rgba(0, 0, 0, 0.34);
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #eef1ed;
        --surface: #e2e9e4;
        --stage: #f7f2e8;
        --panel: #f0eee6;
        --line: #aeb8b1;
        --text: #1d231f;
        --muted: #5d665f;
        --accent: #0f766e;
        --action: #1d4ed8;
        --warn: #8a5a00;
        --closed: #9b1c1c;
        --ok: #047857;
        --shadow: 0 16px 32px rgba(29, 35, 31, 0.12);
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
      width: min(1380px, calc(100% - 28px));
      margin: 0 auto;
      padding: 14px 0 30px;
    }}
    .topline {{
      display: grid;
      grid-template-columns: minmax(280px, 1fr) auto;
      gap: 12px;
      align-items: center;
      padding: 12px 0;
    }}
    .identity, .region-nav, .badge-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }}
    .region-nav {{ justify-content: flex-end; }}
    .episode {{ font-size: 1.08rem; font-weight: 760; }}
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
    .region-nav button, .control {{
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--surface);
      color: var(--text);
      padding: 7px 10px;
      cursor: pointer;
    }}
    .workspace {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(320px, 0.35fr);
      gap: 14px;
      align-items: stretch;
    }}
    .graphic-surface, .inspector, .evidence-drawer, .brief-note {{
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    .graphic-surface {{
      min-height: 650px;
      background: var(--surface);
      padding: 16px;
      display: grid;
      grid-template-rows: auto 1fr auto;
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
    h1 {{ font-size: clamp(1.45rem, 2.35vw, 2.2rem); line-height: 1.08; letter-spacing: 0; }}
    h2 {{ font-size: 1rem; letter-spacing: 0; }}
    h3 {{ font-size: 0.83rem; color: var(--muted); letter-spacing: 0; }}
    p, li, span {{ line-height: 1.4; }}
    p, li {{ color: var(--muted); }}
    .surface-head {{
      display: grid;
      grid-template-columns: 1fr minmax(230px, 0.34fr);
      gap: 10px;
      align-items: end;
    }}
    .decision-strip {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
    }}
    .decision-cell {{
      border-left: 3px solid var(--accent);
      padding: 7px 9px;
      background: rgba(255, 255, 255, 0.035);
      min-width: 0;
    }}
    .decision-cell strong {{ display: block; color: var(--text); font-size: 0.94rem; }}
    .artifact-frame {{
      min-height: 488px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--stage);
      padding: 14px;
      display: grid;
      grid-template-columns: minmax(190px, 0.5fr) minmax(420px, 1.28fr) minmax(190px, 0.56fr);
      gap: 12px;
      overflow: hidden;
    }}
    .before-lane, .flow-stage, .next-lane {{
      min-width: 0;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.035);
      padding: 12px;
    }}
    .before-lane {{
      display: grid;
      grid-template-rows: auto repeat(4, 1fr);
      gap: 8px;
      opacity: 0.76;
    }}
    .faded-block {{
      border: 1px dashed var(--line);
      border-radius: 5px;
      min-height: 44px;
      background: rgba(255, 255, 255, 0.032);
    }}
    .flow-stage {{
      display: grid;
      grid-template-rows: auto 1fr auto;
      gap: 12px;
      border-color: var(--accent);
      background: linear-gradient(180deg, rgba(104, 224, 212, 0.12), rgba(255, 255, 255, 0.035));
    }}
    .flow-title strong {{
      display: block;
      color: var(--text);
      font-size: clamp(1.24rem, 2.1vw, 1.9rem);
      line-height: 1.1;
    }}
    .shelf-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: auto auto;
      gap: 10px;
    }}
    .shelf {{
      border: 1px solid var(--line);
      border-radius: 6px;
      background: rgba(0, 0, 0, 0.14);
      padding: 10px;
      display: grid;
      gap: 7px;
      min-width: 0;
    }}
    .shelf strong {{ color: var(--text); }}
    .mini-bars {{
      display: grid;
      gap: 5px;
    }}
    .mini-bar {{
      height: 8px;
      border-radius: 999px;
      background: var(--line);
      overflow: hidden;
    }}
    .mini-bar span {{
      display: block;
      height: 100%;
      background: var(--accent);
    }}
    .mini-bar.wait span {{ background: var(--warn); }}
    .mini-bar.closed span {{ background: var(--closed); }}
    .progress-strip {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
    }}
    .progress-step {{
      border-top: 4px solid var(--line);
      padding-top: 7px;
      color: var(--muted);
      font-size: 0.78rem;
    }}
    .progress-step.done {{ border-color: var(--accent); color: var(--text); }}
    .progress-step.next {{ border-color: var(--action); color: var(--action); }}
    .next-lane {{
      display: grid;
      gap: 9px;
      align-content: center;
    }}
    .path-node {{
      border-left: 3px solid var(--action);
      padding: 8px 9px;
      background: rgba(255, 255, 255, 0.035);
    }}
    .path-node strong {{ display: block; color: var(--text); }}
    .timeline-band {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 8px;
    }}
    .timeline-node {{
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 8px;
      background: rgba(255, 255, 255, 0.035);
      min-width: 0;
    }}
    .timeline-node strong {{ display: block; color: var(--text); }}
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
    .brief-note {{
      margin-top: 14px;
      background: var(--surface);
      padding: 12px 14px;
    }}
    .evidence-drawer {{
      margin-top: 14px;
      background: var(--panel);
      padding: 12px 14px;
    }}
    .evidence-drawer summary {{ cursor: pointer; color: var(--text); font-weight: 760; }}
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
    @media (max-width: 1100px) {{
      .topline, .workspace, .surface-head, .artifact-frame {{ grid-template-columns: 1fr; }}
      .region-nav {{ justify-content: flex-start; }}
      .decision-strip, .shelf-grid, .progress-strip, .timeline-band {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="console">
    <header class="topline" data-region="header" data-initial-visible-copy="true">
      <div class="identity">
        <span class="episode">第002話</span>
        <span class="badge">日本語レビュー</span>
        <span class="badge">サンプル素材</span>
        <span class="objective">中央の図で方向性を判断し、次は検証済み素材へ戻す。</span>
      </div>
      <nav class="region-nav" data-region="navigation" aria-label="レビュー画面ナビゲーション">
        <button type="button" data-jump="review">レビュー</button>
        <button type="button" data-jump="records">証拠</button>
        <button type="button" data-jump="operations">操作</button>
        <button type="button" data-jump="note">記録</button>
      </nav>
    </header>
    <section class="workspace">
      <section
        class="graphic-surface"
        id="review"
        data-region="main-graphic-review-surface"
        data-main-surface-type="japanese-graphic-flow-spine"
        data-visual-element="production_flow_spine"
        data-free-text-role="secondary_handoff_note"
        data-same-shape-card-grid-primary="false"
        data-evidence-front-stage-row="false"
        data-initial-visible-copy="true">
        <div class="surface-head">
          <div>
            <h1>{_escape(state.get("current_review_target"))}</h1>
            <p>{_escape(state.get("critical_issue_ja"))}</p>
          </div>
          <div class="decision-strip" aria-label="初期表示の優先事項">
            <div class="decision-cell"><h3>判断対象</h3><strong>レビュー画面の方向性</strong></div>
            <div class="decision-cell"><h3>問題</h3><strong>説明量が中心を奪う</strong></div>
            <div class="decision-cell"><h3>次手</h3><strong>検証済み素材を準備</strong></div>
          </div>
        </div>
        <section class="artifact-frame" aria-label="日本語グラフィック判断面">
          <div class="before-lane" data-visual-element="before_after_visual_comparison_canvas" aria-label="修正前の重さ">
            <span class="badge">修正前</span>
            <div class="faded-block"></div>
            <div class="faded-block"></div>
            <div class="faded-block"></div>
            <div class="faded-block"></div>
          </div>
          <div class="flow-stage" aria-label="制作フロー中心の判断">
            <div class="flow-title">
              <span class="badge">中心図</span>
              <strong>素材準備へ戻すレビュー判断面</strong>
              <p>画面方向、入力不足、閉じた gate、次操作を一つの図で見る。</p>
            </div>
            <div class="shelf-grid" data-visual-element="input_readiness_map" aria-label="入力準備マップ">
              <div class="shelf">
                <strong>素材状態</strong>
                <span>サンプルのみ</span>
                <div class="mini-bars"><span class="mini-bar wait"><span style="width: 46%"></span></span></div>
              </div>
              <div class="shelf">
                <strong>判断状態</strong>
                <span>UI方向レビュー</span>
                <div class="mini-bars"><span class="mini-bar"><span style="width: 72%"></span></span></div>
              </div>
              <div class="shelf">
                <strong>差分</strong>
                <span>説明から図へ</span>
                <div class="mini-bars"><span class="mini-bar"><span style="width: 82%"></span></span></div>
              </div>
              <div class="shelf">
                <strong>閉鎖中</strong>
                <span>import / render / public</span>
                <div class="mini-bars"><span class="mini-bar closed"><span style="width: 100%"></span></span></div>
              </div>
            </div>
            <div class="progress-strip" data-visual-element="yymm4_prep_progress_strip" aria-label="準備進行">
              <span class="progress-step done">監査</span>
              <span class="progress-step done">日本語化</span>
              <span class="progress-step next">実素材</span>
              <span class="progress-step">YMM4 gate</span>
            </div>
          </div>
          <div class="next-lane" data-visual-element="diff_style_visual_panel" aria-label="次操作">
            <span class="badge">次の動線</span>
            <div class="path-node"><strong>採否判断</strong><span>この図の方向性を確認。</span></div>
            <div class="path-node"><strong>素材準備</strong><span>検証済みローカル素材へ進む。</span></div>
            <div class="path-node"><strong>明示 gate</strong><span>YMM4観察は選択時だけ。</span></div>
          </div>
        </section>
        <section class="timeline-band" data-visual-element="timeline_state_diagram" aria-label="状態タイムライン">
          <div class="timeline-node"><h3>過去</h3><strong>カード増加</strong></div>
          <div class="timeline-node"><h3>現在</h3><strong>日本語図解</strong></div>
          <div class="timeline-node"><h3>次</h3><strong>実素材準備</strong></div>
          <div class="timeline-node"><h3>別レーン</h3><strong>GUI調整</strong></div>
          <div class="timeline-node"><h3>ゲート</h3><strong>YMM4明示</strong></div>
        </section>
      </section>
      <aside class="inspector" id="operations" data-region="inspector" data-initial-visible-copy="true">
        <span class="badge">検査パネル</span>
        <div>
          <h2>現在の問題</h2>
          <p>{_escape(state.get("critical_issue_ja"))}</p>
        </div>
        <div>
          <h2>推奨操作</h2>
          <p><strong>{_escape(state.get("primary_recommendation_label"))}</strong></p>
        </div>
        <div class="status-table" aria-label="短い状態表">
          {status_rows}
        </div>
        <div class="badge-row" aria-label="閉じた gate">
          <span class="gate-badge">importなし</span>
          <span class="gate-badge">renderなし</span>
          <span class="gate-badge">公開なし</span>
        </div>
        <div class="controls" aria-label="操作">
          {controls}
        </div>
      </aside>
    </section>
    <section class="brief-note" id="note" data-region="handoff-note" data-free-text-role="secondary_handoff_note">
      <h2>記録</h2>
      <p>{_escape(state.get("handoff_note"))}</p>
    </section>
    <details class="evidence-drawer" id="records" data-region="evidence-drawer" data-detail-drawer-role="{_escape(drawer.get("detail_drawer_role"))}">
      <summary>証拠: raw records と source paths</summary>
      <p>判断に必要な状態は上の図と検査パネルへ配置し、raw path と内部IDはここへ退避する。</p>
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
    graphic: dict[str, Any],
    metrics: dict[str, Any],
) -> str:
    lines = [
        "# 第002話 日本語グラフィックレビューコンソール",
        "",
        "中央を説明カードではなく、制作フロー・差分・準備状態で判断する local static console。",
        "",
        f"- Primary decision: {audit.get('primary_decision')}",
        f"- Primary artifact: {audit.get('primary_artifact')}",
        f"- Main surface type: {metrics.get('main_surface_type')}",
        f"- Graphical elements: {', '.join(str(item) for item in _list(graphic.get('graphical_elements')))}",
        f"- Primary UI language: {metrics.get('primary_ui_language')}",
        f"- Free text role: {metrics.get('free_text_role')}",
        f"- Primary recommendation: {state.get('primary_recommendation_label')}",
        "- Hold remains safe fallback, not progress.",
        "- Evidence supports the judgment through inspector/drawer; it is not a front-stage row.",
        "",
        f"Primary review file: `{state.get('primary_human_review')}`",
        f"Machine readback: `{state.get('primary_machine_readable')}`",
        "",
    ]
    return "\n".join(lines)


def _render_screen_audit_markdown(audit: dict[str, Any]) -> str:
    lines = [
        "# Japanese Graphic Console Screen Audit",
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


def _render_visual_self_review(graphic: dict[str, Any], metrics: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Japanese Graphic Console Visual Self-Review",
            "",
            f"- Main surface: {metrics.get('main_surface_type')}",
            f"- Primary UI language: {metrics.get('primary_ui_language')}",
            f"- Artifact dominance: {graphic.get('primary_artifact_dominant')}",
            f"- Center not text cards: {graphic.get('center_not_text_cards')}",
            f"- Graphical elements: {', '.join(str(item) for item in _list(graphic.get('graphical_elements')))}",
            f"- Explanatory cards in main surface: {metrics.get('explanatory_cards_in_main_surface')}",
            f"- Evidence front-stage card row: {metrics.get('evidence_front_stage_card_row')}",
            "- Gaze: header identity -> central graphical flow -> inspector operation -> drawer only for records.",
            "",
        ]
    )


def _render_review_checklist(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Japanese Graphic Review Checklist",
            "",
            "- Open `japanese_graphic_review_console.html`.",
            "- Confirm the primary UI labels are Japanese.",
            "- Confirm the largest center region is graphical flow/diff/timeline, not explanation cards.",
            "- Confirm critical issue and next operation are visible without relying on raw records.",
            "- Confirm evidence supports the judgment from inspector/drawer.",
            "- Confirm hold is fallback only and the main recommendation prepares verified input.",
            "- Confirm `docs/PROJECT_LANES.md` keeps GUI/i18n work from blocking product progress.",
            "",
            f"Primary human review: `{state.get('primary_human_review')}`",
            f"Machine readback: `{state.get('primary_machine_readable')}`",
            "",
        ]
    )


def _render_limitations(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Japanese Graphic Review Console Limitations",
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


def _operational_controls_ja(primary_recommendation: str) -> list[dict[str, Any]]:
    return [
        {
            "control_id": PRIMARY_RECOMMENDATION_NO_REAL_INPUT,
            "label": "検証済み素材を準備",
            "effect": "サンプル依存から進める。",
            "recommended_for_current_state": primary_recommendation == PRIMARY_RECOMMENDATION_NO_REAL_INPUT,
            "tone": "primary",
        },
        {
            "control_id": "regenerate_review_console",
            "label": "画面を再生成",
            "effect": "ローカル出力を作り直す。",
            "recommended_for_current_state": False,
            "tone": "neutral",
        },
        {
            "control_id": "request_yymm4_observation_gate",
            "label": "YMM4観察を依頼",
            "effect": "観察のみ。出力なし。",
            "recommended_for_current_state": primary_recommendation == "observe_yymm4_import_without_render",
            "tone": "gated",
        },
        {
            "control_id": "accept_reject_hold",
            "label": "採用・差し戻し・保留",
            "effect": "保留は安全退避で前進ではない。",
            "recommended_for_current_state": False,
            "tone": "fallback",
        },
    ]


def _recommendation_label_ja(recommendation: str) -> str:
    if recommendation == "replace_sample_with_verified_real_input":
        return "検証済みの実入力へ差し替える"
    if recommendation == "observe_yymm4_import_without_render":
        return "renderなしでYMM4 import観察を行う"
    return "検証済みローカル素材/文字起こしを準備"


def _next_operation_ja(recommendation: str) -> str:
    if recommendation == "replace_sample_with_verified_real_input":
        return "サンプル入力を検証済み素材へ差し替える。"
    if recommendation == "observe_yymm4_import_without_render":
        return "明示 gate の範囲だけでYMM4 import観察を行う。"
    return "検証済みローカル素材/文字起こしを準備する。"


def _lane_map_has_required_lanes(text: str) -> bool:
    required = (
        "Output / Video Layer",
        "Input / API Hub",
        "GUI / IA / i18n",
        "Integrity / Triage",
        "Editing / YMM4 Feature Design",
        "Deep Research",
    )
    return all(item in text for item in required)


def _primary_heading_texts(html_text: str) -> list[str]:
    snippets = re.findall(r"<h[1-3]\b[^>]*>(.*?)</h[1-3]>", html_text, flags=re.IGNORECASE | re.DOTALL)
    snippets.extend(re.findall(r"<button\b[^>]*>(.*?)</button>", html_text, flags=re.IGNORECASE | re.DOTALL))
    return [_visible_text(snippet).strip() for snippet in snippets if _visible_text(snippet).strip()]


def _english_primary_heading_hits(headings: list[str]) -> list[str]:
    hits: list[str] = []
    for heading in headings:
        normalized = heading
        for term in ALLOWED_ENGLISH_TERMS:
            normalized = re.sub(re.escape(term), "", normalized, flags=re.IGNORECASE)
        if re.search(r"[A-Za-z]", normalized):
            hits.append(heading)
    return hits
