"""Compact review cockpit for episode 002 local review packets."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIRNAME = "review_cockpit_compact"
DEFAULT_ARTIFACT_ID = "episode_002_review_cockpit_compact_v1"
DEFAULT_FOCUSED_BRIEF_DIRNAME = "focused_review_brief"
DEFAULT_REVIEWER_PACKET_DIRNAME = "surface_alignment_review_packet"

REQUIRED_REVIEW_COCKPIT_FILES = (
    "review_cockpit_manifest.json",
    "review_cockpit.html",
    "review_cockpit.md",
    "cockpit_state.json",
    "cockpit_layout_readback.json",
    "detail_source_index.json",
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

REQUIRED_HTML_MARKERS = (
    'data-review-cockpit="true"',
    'data-section="header-strip"',
    'data-section="decision-card"',
    'data-section="next-action-row"',
    'data-section="surface-status-row"',
    'data-section="gate-strip"',
    "color-scheme: dark light",
    "prefers-color-scheme",
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

TEMPORARY_NOTE_PHRASES = (
    "only look here",
    "look only here",
    "just read this",
    "only read this",
    "this page is for now",
    "for now",
    "temporary memo",
    "test-passing",
    "note block",
)


def build_review_cockpit_compact(
    *,
    package_dir: str | Path,
    focused_brief_dir: str | Path | None = None,
    reviewer_packet_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a bounded dark review cockpit from the focused brief and source packet."""
    source_root = Path(package_dir)
    focused_root = Path(focused_brief_dir) if focused_brief_dir else source_root / DEFAULT_FOCUSED_BRIEF_DIRNAME
    reviewer_root = Path(reviewer_packet_dir) if reviewer_packet_dir else source_root / DEFAULT_REVIEWER_PACKET_DIRNAME
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root, focused_root, reviewer_root)
    payloads = _load_payloads(paths)
    state = _cockpit_state_payload(
        artifact_id=artifact_id,
        payloads=payloads,
        paths=paths,
        source_root=source_root,
        focused_root=focused_root,
        reviewer_root=reviewer_root,
        output_root=output_root,
        repo_root=repo_root,
    )
    layout = _layout_readback_payload(artifact_id, state, output_root, repo_root)
    source_index = _detail_source_index(
        artifact_id=artifact_id,
        state=state,
        paths=paths,
        source_root=source_root,
        focused_root=focused_root,
        reviewer_root=reviewer_root,
        output_root=output_root,
        repo_root=repo_root,
    )
    manifest = _manifest_payload(artifact_id, state, layout, source_index, source_root, output_root, repo_root)

    _write_json(output_root / "review_cockpit_manifest.json", manifest)
    _write_json(output_root / "cockpit_state.json", state)
    _write_json(output_root / "cockpit_layout_readback.json", layout)
    _write_json(output_root / "detail_source_index.json", source_index)
    _write_text(output_root / "review_cockpit.html", _render_html(state, layout, source_index))
    _write_text(output_root / "review_cockpit.md", _render_markdown(state, source_index))
    _write_text(output_root / "review_checklist.md", _render_review_checklist(state, layout))
    _write_text(output_root / "limitations.md", _render_limitations(state))

    readback = validate_review_cockpit_compact(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_review_cockpit_compact(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_review_cockpit_compact(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated compact review cockpit package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_REVIEW_COCKPIT_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["review_cockpit_manifest.json"])
    state = _load_json_if_present(files["cockpit_state.json"])
    layout = _load_json_if_present(files["cockpit_layout_readback.json"])
    source_index = _load_json_if_present(files["detail_source_index.json"])

    json_payloads = {
        "review_cockpit_manifest": manifest,
        "cockpit_state": state,
        "cockpit_layout_readback": layout,
        "detail_source_index": source_index,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["review_cockpit_manifest"]
    state = json_payloads["cockpit_state"]
    layout = json_payloads["cockpit_layout_readback"]
    source_index = json_payloads["detail_source_index"]

    if manifest.get("artifact_kind") != "episode-review-cockpit-compact":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if state.get("status") != "review_cockpit_ready_local_offline":
        failed_checks.append("state_status_mismatch")
    if state.get("source_record_policy") != "secondary_records_only":
        failed_checks.append("source_record_policy_mismatch")

    decision_options = _list(state.get("decision_options"))
    surface_statuses = _list(state.get("surface_statuses"))
    if len(decision_options) == 0 or len(decision_options) > 3:
        failed_checks.append("next_action_count_out_of_bounds")
    if len(decision_options) != 3:
        failed_checks.append("next_action_count_not_three")
    if len(surface_statuses) != 3:
        failed_checks.append("surface_status_count_not_three")

    boundary_flags = _dict(state.get("boundary_flags"))
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")

    required_layout = {
        "primary_section_count": 5,
        "visible_card_count": 7,
        "detail_section_count": 2,
        "top_level_table_count": 0,
        "temporary_note_count": 0,
    }
    for key, expected in required_layout.items():
        if layout.get(key) != expected:
            failed_checks.append(f"layout_metric_mismatch:{key}")
    if layout.get("ledger_in_primary_body") is not False:
        failed_checks.append("ledger_visible_in_primary_body")
    if layout.get("source_record_display_zone") != "secondary_details":
        failed_checks.append("source_record_display_zone_mismatch")

    secondary_records = _list(source_index.get("secondary_source_records"))
    secondary_record_ids = {str(row.get("record_id")) for row in secondary_records if isinstance(row, dict)}
    for record_id in (
        "surface_alignment_aligned_story",
        "focused_review_html",
        "focused_review_validation",
        "reviewer_packet_validation",
    ):
        if record_id not in secondary_record_ids:
            failed_checks.append(f"secondary_source_record_missing:{record_id}")
    if any(_dict(row).get("display_zone") != "secondary_details" for row in secondary_records):
        failed_checks.append("source_record_not_secondary")

    html_text = files["review_cockpit.html"].read_text(encoding="utf-8") if files["review_cockpit.html"].exists() else ""
    markdown_text = files["review_cockpit.md"].read_text(encoding="utf-8") if files["review_cockpit.md"].exists() else ""
    missing_html_markers = [marker for marker in REQUIRED_HTML_MARKERS if marker not in html_text]
    failed_checks.extend(f"missing_html_marker:{marker}" for marker in missing_html_markers)
    if "<details" not in html_text:
        failed_checks.append("details_disclosure_missing")
    if "<table" in html_text.lower() or "</table" in html_text.lower():
        failed_checks.append("table_markup_present")
    if "surface_alignment_review_packet/aligned_review_story.md" not in html_text:
        failed_checks.append("aligned_story_source_record_missing_from_html")
    if "focused_review_brief/focused_review_brief.html" not in html_text:
        failed_checks.append("focused_html_source_record_missing_from_html")
    if len(markdown_text.splitlines()) > 90:
        failed_checks.append("markdown_fallback_too_long")

    forbidden_hits = _forbidden_true_claims(root)
    external_refs = _external_refs(root)
    pure_white_hits = _pure_white_hits(root)
    phrase_hits = _temporary_phrase_hits(root)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"pure_white_marker:{hit}" for hit in pure_white_hits)
    failed_checks.extend(f"temporary_phrase:{hit}" for hit in phrase_hits)

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "dark_mode_css_markers_present": not missing_html_markers,
        "external_refs_absent": not external_refs,
        "pure_white_background_absent": not pure_white_hits,
        "forbidden_true_claims_absent": not forbidden_hits,
        "temporary_review_copy_absent": not phrase_hits,
        "bounded_primary_layout": not any(check.startswith("layout_metric_mismatch") for check in failed_checks),
        "one_primary_decision_card": layout.get("decision_card_count") == 1,
        "next_action_count_bounded": 0 < len(decision_options) <= 3,
        "three_surface_status_row": len(surface_statuses) == 3,
        "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS),
        "source_records_secondary": source_index.get("source_record_policy") == "secondary_records_only",
        "source_records_linked_secondary": all(
            _dict(row).get("display_zone") == "secondary_details" for row in secondary_records
        ),
        "details_disclosure_present": "<details" in html_text,
        "tables_absent": "<table" not in html_text.lower() and "</table" not in html_text.lower(),
        "markdown_fallback_concise": len(markdown_text.splitlines()) <= 90,
    }

    return {
        "schema_version": "review_cockpit_validation_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "source_artifact_id": state.get("source_artifact_id"),
        "focused_brief_artifact_id": state.get("focused_brief_artifact_id"),
        "primary_decision": state.get("primary_decision"),
        "decision_options": len(decision_options),
        "surface_status_count": len(surface_statuses),
        "primary_section_count": layout.get("primary_section_count"),
        "visible_card_count": layout.get("visible_card_count"),
        "detail_section_count": layout.get("detail_section_count"),
        "layout_bloat_status": layout.get("layout_bloat_status"),
        "source_record_policy": state.get("source_record_policy"),
        "dark_mode_support": state.get("dark_mode_support"),
        "external_dependency_status": "absent" if not external_refs else "present",
        "white_background_status": "absent" if not pure_white_hits else "present",
        "temporary_review_copy_status": "absent" if not phrase_hits else "present",
        "primary_machine_readable": str(root / "validation_readback.json"),
        "primary_human_review": str(root / "review_cockpit.html"),
        "markdown_fallback": str(root / "review_cockpit.md"),
        "access_state": "verified_present" if (root / "review_cockpit.html").exists() else "missing",
        "launcher_command": f'start "" "{(root / "review_cockpit.html").resolve()}"',
        "next_action": state.get("next_action"),
    }


def _input_paths(source_root: Path, focused_root: Path, reviewer_root: Path) -> dict[str, Path]:
    return {
        "focused_manifest": focused_root / "focused_review_manifest.json",
        "focused_validation": focused_root / "validation_readback.json",
        "focused_summary": focused_root / "review_summary.json",
        "focused_decision_card": focused_root / "review_decision_card.json",
        "focused_source_index": focused_root / "detail_source_index.json",
        "focused_html": focused_root / "focused_review_brief.html",
        "focused_markdown": focused_root / "focused_review_brief.md",
        "reviewer_validation": reviewer_root / "validation_readback.json",
        "alignment_repair_summary": reviewer_root / "alignment_repair_summary.json",
        "remaining_mismatch_ledger": reviewer_root / "remaining_mismatch_ledger.json",
        "next_action_readback": reviewer_root / "next_action_readback.json",
        "boundary_status_readback": reviewer_root / "boundary_status_readback.json",
        "source_artifact_crosswalk_readback": reviewer_root / "source_artifact_crosswalk_readback.json",
        "aligned_review_story": reviewer_root / "aligned_review_story.md",
        "gui_readback": source_root / "gui_dashboard_panel" / "validation_readback.json",
        "import_readback": source_root / "ymm4_import_preview_pack" / "validation_readback.json",
        "thumbnail_readback": source_root / "thumbnail_visual_proof_pack" / "readback.json",
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    payloads: dict[str, Any] = {}
    for name, path in paths.items():
        if path.suffix == ".json":
            payloads[name] = _load_json(path)
    return payloads


def _cockpit_state_payload(
    *,
    artifact_id: str,
    payloads: dict[str, Any],
    paths: dict[str, Path],
    source_root: Path,
    focused_root: Path,
    reviewer_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    focused_manifest = payloads["focused_manifest"]
    focused_summary = payloads["focused_summary"]
    focused_decision = payloads["focused_decision_card"]
    focused_validation = payloads["focused_validation"]
    reviewer_validation = payloads["reviewer_validation"]
    repair = payloads["alignment_repair_summary"]
    boundary = payloads["boundary_status_readback"]
    next_action = payloads["next_action_readback"]

    boundary_flags = _dict(boundary.get("boundary_flags")) or _dict(focused_summary.get("boundary_flags"))
    decision_options = _compact_decision_options(_list(focused_decision.get("next_action_cards")))
    surface_statuses = _surface_statuses(repair)
    source_records = _secondary_source_records(paths, repo_root)
    primary_question = _list(focused_decision.get("primary_questions"))[0]
    return {
        "schema_version": "review_cockpit_state.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-review-cockpit-compact",
        "status": "review_cockpit_ready_local_offline",
        "source_package_dir": _relpath(source_root, repo_root),
        "focused_brief_dir": _relpath(focused_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "source_artifact_id": repair.get("artifact_id"),
        "focused_brief_artifact_id": focused_manifest.get("artifact_id"),
        "selected_candidate_id": focused_summary.get("selected_candidate_id"),
        "source_packet_status": reviewer_validation.get("status"),
        "focused_brief_status": focused_validation.get("status"),
        "primary_decision": "Select the next episode 002 review path.",
        "primary_question": primary_question,
        "decision_context": (
            "Episode 002 has aligned local evidence across GUI, import preview, and thumbnail proof; "
            "it remains dry-run and sample-backed."
        ),
        "decision_options": decision_options,
        "recommended_default": focused_decision.get("recommended_default"),
        "surface_statuses": surface_statuses,
        "surface_status_row_count": len(surface_statuses),
        "boundary_flags": boundary_flags,
        "closed_gate_strip": _gate_strip(boundary_flags),
        "closed_gate_status": _dict(boundary.get("closed_gate_status")),
        "not_claimed": _list(focused_decision.get("not_claimed")),
        "source_record_policy": "secondary_records_only",
        "secondary_source_records": source_records,
        "dark_mode_support": {
            "first_party_css": True,
            "color_scheme": "dark light",
            "prefers_color_scheme": True,
            "external_dependencies": False,
            "pure_white_background": False,
        },
        "primary_human_review": _relpath(output_root / "review_cockpit.html", repo_root),
        "markdown_fallback": _relpath(output_root / "review_cockpit.md", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "prior_primary_review_surface": _relpath(paths["focused_html"], repo_root),
        "legacy_aligned_story": _relpath(paths["aligned_review_story"], repo_root),
        "source_next_action": next_action.get("next_safe_local_action"),
        "next_action": "Open review_cockpit.html and choose real input replacement, YMM4 import observation without render, or hold.",
    }


def _layout_readback_payload(
    artifact_id: str,
    state: dict[str, Any],
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    decision_count = 1
    action_count = len(_list(state.get("decision_options")))
    surface_count = len(_list(state.get("surface_statuses")))
    return {
        "schema_version": "review_cockpit_layout_readback.v1",
        "artifact_id": artifact_id,
        "output_dir": _relpath(output_root, repo_root),
        "layout_name": "compact_dark_review_cockpit",
        "primary_sections": [
            "header_strip",
            "decision_card",
            "next_action_row",
            "surface_status_row",
            "closed_gate_strip",
        ],
        "primary_section_count": 5,
        "decision_card_count": decision_count,
        "next_action_option_count": action_count,
        "surface_status_count": surface_count,
        "visible_card_count": decision_count + action_count + surface_count,
        "detail_sections": [
            "secondary_source_index",
            "validation_and_limitations",
        ],
        "detail_section_count": 2,
        "top_level_table_count": 0,
        "temporary_note_count": 0,
        "ledger_in_primary_body": False,
        "source_record_display_zone": "secondary_details",
        "bounded_viewport_strategy": "fixed primary rows with secondary disclosures",
        "one_off_copy_status": "absent",
        "layout_bloat_status": "bounded",
        "primary_review_surface": state.get("primary_human_review"),
    }


def _detail_source_index(
    *,
    artifact_id: str,
    state: dict[str, Any],
    paths: dict[str, Path],
    source_root: Path,
    focused_root: Path,
    reviewer_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "review_cockpit_detail_source_index.v1",
        "artifact_id": artifact_id,
        "source_package_dir": _relpath(source_root, repo_root),
        "focused_brief_dir": _relpath(focused_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "source_record_policy": "secondary_records_only",
        "primary_review_surface": _relpath(output_root / "review_cockpit.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "current_outputs": [
            _output_row("review_cockpit_html", output_root / "review_cockpit.html", repo_root),
            _output_row("review_cockpit_markdown", output_root / "review_cockpit.md", repo_root),
            _output_row("cockpit_state", output_root / "cockpit_state.json", repo_root),
            _output_row("cockpit_layout_readback", output_root / "cockpit_layout_readback.json", repo_root),
            _output_row("validation_readback", output_root / "validation_readback.json", repo_root),
        ],
        "secondary_source_records": state.get("secondary_source_records"),
        "source_readbacks": {
            "focused_review_brief": _relpath(paths["focused_validation"], repo_root),
            "reviewer_packet": _relpath(paths["reviewer_validation"], repo_root),
            "gui_dashboard_panel": _relpath(paths["gui_readback"], repo_root),
            "yymm4_import_preview_pack": _relpath(paths["import_readback"], repo_root),
            "thumbnail_visual_proof_pack": _relpath(paths["thumbnail_readback"], repo_root),
        },
    }


def _manifest_payload(
    artifact_id: str,
    state: dict[str, Any],
    layout: dict[str, Any],
    source_index: dict[str, Any],
    source_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "review_cockpit_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-review-cockpit-compact",
        "status": "generated",
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "files": {name: _relpath(output_root / name, repo_root) for name in REQUIRED_REVIEW_COCKPIT_FILES},
        "source_artifact_id": state.get("source_artifact_id"),
        "focused_brief_artifact_id": state.get("focused_brief_artifact_id"),
        "primary_review_surface": state.get("primary_human_review"),
        "primary_machine_readable": state.get("primary_machine_readable"),
        "markdown_fallback": state.get("markdown_fallback"),
        "source_record_policy": state.get("source_record_policy"),
        "secondary_source_record_count": len(_list(source_index.get("secondary_source_records"))),
        "primary_section_count": layout.get("primary_section_count"),
        "visible_card_count": layout.get("visible_card_count"),
        "boundary_flags": state.get("boundary_flags"),
        "next_action": state.get("next_action"),
    }


def _render_html(state: dict[str, Any], layout: dict[str, Any], source_index: dict[str, Any]) -> str:
    question = _escape(state.get("primary_question"))
    action_cards = "\n".join(_render_action_card(card) for card in _list(state.get("decision_options")))
    surface_cards = "\n".join(_render_surface_card(surface) for surface in _list(state.get("surface_statuses")))
    gate_chips = "\n".join(f'<span class="chip">{_escape(gate)}</span>' for gate in _list(state.get("closed_gate_strip")))
    not_claimed = "\n".join(f"<li>{_escape(item)}</li>" for item in _list(state.get("not_claimed")))
    source_rows = "\n".join(
        f"<li><span>{_escape(row.get('label'))}</span><code>{_escape(row.get('repo_relative_path'))}</code></li>"
        for row in _list(source_index.get("secondary_source_records"))
        if isinstance(row, dict)
    )
    metric_rows = "\n".join(
        [
            f"<li><span>Primary sections</span><strong>{_escape(layout.get('primary_section_count'))}</strong></li>",
            f"<li><span>Visible cards</span><strong>{_escape(layout.get('visible_card_count'))}</strong></li>",
            f"<li><span>Detail sections</span><strong>{_escape(layout.get('detail_section_count'))}</strong></li>",
            f"<li><span>Layout status</span><strong>{_escape(layout.get('layout_bloat_status'))}</strong></li>",
        ]
    )
    return f"""<!doctype html>
<html lang="en" data-review-cockpit="true">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Review Cockpit</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #0a0f1c;
      --panel: #121a27;
      --panel-2: #182235;
      --panel-3: #0f1724;
      --text: #e6edf6;
      --muted: #a7b5c8;
      --line: #33445f;
      --accent: #2dd4bf;
      --action: #93c5fd;
      --warn: #f5c542;
      --closed: #fb7185;
      --ok: #86efac;
      --shadow: 0 18px 46px rgba(0, 0, 0, 0.32);
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #edf4f8;
        --panel: #f7fafc;
        --panel-2: #e8eef5;
        --panel-3: #dde6ef;
        --text: #182235;
        --muted: #475569;
        --line: #bfd0df;
        --accent: #0f766e;
        --action: #1d4ed8;
        --warn: #8a5a00;
        --closed: #be123c;
        --ok: #166534;
        --shadow: 0 16px 36px rgba(15, 23, 42, 0.12);
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(135deg, var(--bg), #111827 68%);
      color: var(--text);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }}
    main {{
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
      padding: 20px 0 28px;
    }}
    .header-strip {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 16px;
      align-items: center;
      padding: 12px 14px;
      background: var(--panel-3);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    .header-strip h1 {{
      margin: 0;
      font-size: clamp(1.2rem, 2.1vw, 1.85rem);
      line-height: 1.1;
      letter-spacing: 0;
    }}
    .header-strip p {{ margin: 4px 0 0; color: var(--muted); }}
    .header-meta {{ display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }}
    .pill {{
      display: inline-flex;
      align-items: center;
      min-height: 28px;
      padding: 5px 9px;
      border-radius: 999px;
      background: var(--panel-2);
      border: 1px solid var(--line);
      color: var(--muted);
      font-size: 0.82rem;
      white-space: nowrap;
    }}
    .decision-card {{
      margin-top: 14px;
      padding: 18px;
      background: var(--panel);
      border: 1px solid var(--accent);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    .eyebrow {{
      margin: 0 0 8px;
      color: var(--accent);
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
    }}
    h2 {{
      margin: 0 0 10px;
      font-size: 0.96rem;
      letter-spacing: 0;
    }}
    .decision-card h2 {{
      font-size: clamp(1.25rem, 2.6vw, 2rem);
      line-height: 1.12;
    }}
    .question {{
      margin: 0;
      font-size: 1.04rem;
      line-height: 1.48;
      color: var(--text);
    }}
    .context {{
      margin: 10px 0 0;
      color: var(--muted);
      line-height: 1.5;
    }}
    .row {{
      margin-top: 14px;
      display: grid;
      gap: 12px;
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }}
    .card {{
      min-height: 154px;
      padding: 14px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .card p {{ margin: 7px 0 0; color: var(--muted); line-height: 1.45; font-size: 0.92rem; }}
    .status {{
      display: inline-flex;
      margin-bottom: 10px;
      padding: 4px 8px;
      border-radius: 999px;
      background: var(--panel-2);
      color: var(--action);
      font-size: 0.78rem;
      font-weight: 700;
    }}
    .surface .status {{ color: var(--ok); }}
    .gate-strip {{
      margin-top: 14px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      padding: 12px;
      background: var(--panel-3);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .chip {{
      padding: 6px 9px;
      border-radius: 999px;
      background: var(--panel-2);
      border: 1px solid var(--line);
      color: var(--muted);
      font-size: 0.79rem;
    }}
    details {{
      margin-top: 12px;
      padding: 12px 14px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    summary {{ cursor: pointer; font-weight: 700; }}
    ul.compact {{ margin: 10px 0 0; padding-left: 20px; color: var(--muted); line-height: 1.5; }}
    ul.records, ul.metrics {{ list-style: none; margin: 10px 0 0; padding: 0; display: grid; gap: 8px; }}
    ul.records li, ul.metrics li {{
      display: grid;
      gap: 4px;
      padding: 9px 10px;
      background: var(--panel-2);
      border-radius: 6px;
      border: 1px solid var(--line);
    }}
    ul.metrics li {{ grid-template-columns: minmax(0, 1fr) auto; align-items: center; }}
    code {{ color: var(--accent); overflow-wrap: anywhere; }}
    @media (max-width: 860px) {{
      main {{ width: min(100% - 20px, 1180px); padding-top: 10px; }}
      .header-strip {{ grid-template-columns: 1fr; }}
      .header-meta {{ justify-content: flex-start; }}
      .row {{ grid-template-columns: 1fr; }}
      .card {{ min-height: auto; }}
    }}
  </style>
</head>
<body>
  <main>
    <header class="header-strip" data-section="header-strip">
      <div>
        <h1>Episode 002 Review Cockpit</h1>
        <p>{_escape(state.get("decision_context"))}</p>
      </div>
      <div class="header-meta">
        <span class="pill">dry_run</span>
        <span class="pill">sample_fixture_not_real</span>
        <span class="pill">gates_closed</span>
      </div>
    </header>

    <article class="decision-card" data-section="decision-card">
      <p class="eyebrow">Primary decision</p>
      <h2>{_escape(state.get("primary_decision"))}</h2>
      <p class="question">{question}</p>
      <p class="context">{_escape(state.get("recommended_default"))}</p>
    </article>

    <section data-section="next-action-row">
      <h2>Next Action Row</h2>
      <div class="row">{action_cards}</div>
    </section>

    <section data-section="surface-status-row">
      <h2>Three-Surface Status Row</h2>
      <div class="row">{surface_cards}</div>
    </section>

    <section class="gate-strip" data-section="gate-strip">{gate_chips}</section>

    <details data-section="secondary-source-index">
      <summary>Secondary Source Records</summary>
      <ul class="records">{source_rows}</ul>
    </details>

    <details data-section="validation-limitations">
      <summary>Validation And Closed Claims</summary>
      <ul class="metrics">{metric_rows}</ul>
      <ul class="compact">{not_claimed}</ul>
    </details>
  </main>
</body>
</html>
"""


def _render_markdown(state: dict[str, Any], source_index: dict[str, Any]) -> str:
    lines = [
        "# Episode 002 Review Cockpit",
        "",
        f"Primary decision: {state.get('primary_decision')}",
        "",
        f"Question: {state.get('primary_question')}",
        "",
        "## Current State",
        "",
        "- GUI, import preview, and thumbnail proof are aligned as local review evidence.",
        "- The package remains dry-run and sample-backed.",
        "- Production, public upload, YMM4 import/render, rights, and final thumbnail claims remain closed.",
        "",
        "## Next Action Row",
        "",
    ]
    for card in _list(state.get("decision_options")):
        lines.append(f"- {card.get('label')}: {card.get('use_when')} Effect: {card.get('effect')}")
    lines.extend(["", "## Surface Status Row", ""])
    for surface in _list(state.get("surface_statuses")):
        lines.append(f"- {surface.get('label')}: {surface.get('status')} / {surface.get('message')}")
    lines.extend(
        [
            "",
            "## Closed Gates",
            "",
            ", ".join(str(gate) for gate in _list(state.get("closed_gate_strip"))),
            "",
            "## Secondary Source Records",
            "",
        ]
    )
    for row in _list(source_index.get("secondary_source_records")):
        if isinstance(row, dict):
            lines.append(f"- {row.get('label')}: `{row.get('repo_relative_path')}`")
    lines.extend(
        [
            "",
            "Primary machine readback:",
            "",
            f"`{state.get('primary_machine_readable')}`",
            "",
        ]
    )
    return "\n".join(lines)


def _render_action_card(card: dict[str, Any]) -> str:
    return "\n".join(
        [
            '        <article class="card">',
            f'          <span class="status">{_escape(card.get("status"))}</span>',
            f"          <h2>{_escape(card.get('label'))}</h2>",
            f"          <p><strong>Use when:</strong> {_escape(card.get('use_when'))}</p>",
            f"          <p><strong>Effect:</strong> {_escape(card.get('effect'))}</p>",
            f"          <p><strong>Requires:</strong> {_escape(card.get('requires'))}</p>",
            "        </article>",
        ]
    )


def _render_surface_card(surface: dict[str, Any]) -> str:
    return "\n".join(
        [
            '        <article class="card surface">',
            f'          <span class="status">{_escape(surface.get("status"))}</span>',
            f"          <h2>{_escape(surface.get('label'))}</h2>",
            f"          <p>{_escape(surface.get('message'))}</p>",
            f"          <p><code>{_escape(surface.get('human_review'))}</code></p>",
            "        </article>",
        ]
    )


def _render_review_checklist(state: dict[str, Any], layout: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Review Cockpit Checklist",
            "",
            "- Open `review_cockpit.html`.",
            "- Confirm the primary decision card is visible before secondary records.",
            "- Confirm the next-action row has three choices: real input replacement, YMM4 import observation without render, and hold.",
            "- Confirm the status row covers GUI, import preview, and thumbnail proof.",
            "- Confirm the closed-gate strip keeps dry-run, sample fixture, no real transcript, rights, publication, YMM4, thumbnail, validation-noise, and production boundaries visible.",
            "- Treat `aligned_review_story.md` and `focused_review_brief.html` as source records.",
            "",
            "Layout readback:",
            "",
            f"- primary_section_count: {layout.get('primary_section_count')}",
            f"- visible_card_count: {layout.get('visible_card_count')}",
            f"- detail_section_count: {layout.get('detail_section_count')}",
            "",
            "Primary question:",
            "",
            str(state.get("primary_question")),
            "",
        ]
    )


def _render_limitations(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Review Cockpit Limitations",
            "",
            "This package is a local/offline decision surface over the existing episode 002 review records.",
            "",
            "It does not change creative assets, GUI dashboard data, import preview content, thumbnail variants, Writer IR, CSV content, source material, or YMM4 files.",
            "",
            "Not performed:",
            "",
            "- real transcript rerun or real source replacement",
            "- YMM4 GUI launch, import, render, or production `.ymmp` generation",
            "- final thumbnail approval",
            "- public upload, publication, scheduling, or visibility change",
            "- rights/legal/public-ready acceptance",
            "- OAuth, API keys, payment, or paid services",
            "- live fetch, scraping, or external media acquisition",
            "- full-suite green campaign or broad fixture regeneration",
            "",
            "Primary review file:",
            "",
            str(state.get("primary_human_review")),
            "",
        ]
    )


def _compact_decision_options(cards: list[Any]) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    for card in cards[:3]:
        if not isinstance(card, dict):
            continue
        compact.append(
            {
                "option_id": card.get("option_id"),
                "label": card.get("label"),
                "status": card.get("status"),
                "use_when": card.get("use_when"),
                "effect": card.get("effect"),
                "requires": card.get("requires"),
            }
        )
    return compact


def _surface_statuses(repair: dict[str, Any]) -> list[dict[str, Any]]:
    messages = {
        "gui_dashboard_panel": "GUI dashboard panel is aligned as local review evidence.",
        "yymm4_import_preview_pack": "Import preview is reviewable without a YMM4 import or render.",
        "thumbnail_visual_proof_pack": "Thumbnail proof is context and not final thumbnail approval.",
    }
    rows: list[dict[str, Any]] = []
    for surface in _list(repair.get("surfaces")):
        if not isinstance(surface, dict):
            continue
        surface_id = str(surface.get("surface_id"))
        rows.append(
            {
                "surface_id": surface_id,
                "label": surface.get("label"),
                "status": surface.get("status"),
                "role": surface.get("role_in_alignment"),
                "message": messages.get(surface_id, "Local review evidence is available."),
                "human_review": surface.get("primary_human_review"),
                "machine_readable": surface.get("primary_machine_readable"),
                "next_action": surface.get("next_action"),
            }
        )
    return rows


def _gate_strip(boundary_flags: dict[str, Any]) -> list[str]:
    return [flag for flag in REQUIRED_BOUNDARY_FLAGS if boundary_flags.get(flag) is True]


def _secondary_source_records(paths: dict[str, Path], repo_root: Path) -> list[dict[str, Any]]:
    rows = [
        ("surface_alignment_aligned_story", "Aligned review story", paths["aligned_review_story"], "surface_alignment_review_packet"),
        ("focused_review_html", "Focused review HTML", paths["focused_html"], "focused_review_brief"),
        ("focused_review_markdown", "Focused review Markdown", paths["focused_markdown"], "focused_review_brief"),
        ("focused_review_validation", "Focused review validation", paths["focused_validation"], "focused_review_brief"),
        ("reviewer_packet_validation", "Reviewer packet validation", paths["reviewer_validation"], "surface_alignment_review_packet"),
        ("remaining_mismatch_ledger", "Remaining mismatch ledger", paths["remaining_mismatch_ledger"], "surface_alignment_review_packet"),
        ("gui_dashboard_validation", "GUI dashboard validation", paths["gui_readback"], "gui_dashboard_panel"),
        ("import_preview_validation", "Import preview validation", paths["import_readback"], "yymm4_import_preview_pack"),
        ("thumbnail_proof_readback", "Thumbnail proof readback", paths["thumbnail_readback"], "thumbnail_visual_proof_pack"),
    ]
    return [
        {
            "record_id": record_id,
            "label": label,
            "repo_relative_path": _relpath(path, repo_root),
            "surface": surface,
            "role": "secondary_source_record",
            "display_zone": "secondary_details",
            "exists": path.exists(),
        }
        for record_id, label, path, surface in rows
    ]


def _output_row(record_id: str, path: Path, repo_root: Path) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "repo_relative_path": _relpath(path, repo_root),
        "role": "review_cockpit_output",
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


def _external_refs(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8-sig", errors="ignore").lower()
            for marker in EXTERNAL_REF_MARKERS:
                if marker in text:
                    hits.append(f"{path.name}:{marker}")
    return hits


def _pure_white_hits(root: Path) -> list[str]:
    hits: list[str] = []
    markers = ("#fff", "#ffffff", "background: white", "background-color: white")
    for path in root.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8-sig", errors="ignore").lower()
            for marker in markers:
                if marker in text:
                    hits.append(f"{path.name}:{marker}")
    return hits


def _temporary_phrase_hits(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8-sig", errors="ignore").lower()
            for phrase in TEMPORARY_NOTE_PHRASES:
                if phrase in text:
                    hits.append(f"{path.name}:{phrase}")
    return hits


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
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
