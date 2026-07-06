"""Focused dark-mode review brief for episode 002 reviewer packets."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIRNAME = "focused_review_brief"
DEFAULT_ARTIFACT_ID = "episode_002_focused_review_brief_dark_surface_v1"
DEFAULT_REVIEWER_PACKET_DIRNAME = "surface_alignment_review_packet"

REQUIRED_FOCUSED_REVIEW_FILES = (
    "focused_review_manifest.json",
    "focused_review_brief.html",
    "focused_review_brief.md",
    "review_decision_card.json",
    "review_summary.json",
    "detail_source_index.json",
    "review_checklist.md",
    "limitations.md",
    "validation_readback.json",
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
    'data-focused-review-brief="true"',
    'data-section="decision-card"',
    'data-section="three-line-summary"',
    'data-section="next-action-cards"',
    'data-section="evidence-cards"',
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


def build_focused_review_brief(
    *,
    package_dir: str | Path,
    reviewer_packet_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a concise human-facing review brief from the current reviewer packet."""
    source_root = Path(package_dir)
    reviewer_root = Path(reviewer_packet_dir) if reviewer_packet_dir else source_root / DEFAULT_REVIEWER_PACKET_DIRNAME
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root, reviewer_root)
    payloads = _load_payloads(paths)
    summary = _review_summary_payload(
        artifact_id=artifact_id,
        payloads=payloads,
        source_root=source_root,
        reviewer_root=reviewer_root,
        output_root=output_root,
        repo_root=repo_root,
    )
    decision_card = _decision_card_payload(artifact_id, payloads, summary)
    source_index = _detail_source_index(
        artifact_id=artifact_id,
        payloads=payloads,
        paths=paths,
        source_root=source_root,
        reviewer_root=reviewer_root,
        output_root=output_root,
        repo_root=repo_root,
    )
    manifest = _manifest_payload(artifact_id, summary, source_index, source_root, reviewer_root, output_root, repo_root)

    html_text = _render_html(summary, decision_card, source_index)
    markdown_text = _render_markdown(summary, decision_card, source_index)

    _write_json(output_root / "focused_review_manifest.json", manifest)
    _write_json(output_root / "review_summary.json", summary)
    _write_json(output_root / "review_decision_card.json", decision_card)
    _write_json(output_root / "detail_source_index.json", source_index)
    _write_text(output_root / "focused_review_brief.html", html_text)
    _write_text(output_root / "focused_review_brief.md", markdown_text)
    _write_text(output_root / "review_checklist.md", _render_review_checklist(summary, decision_card))
    _write_text(output_root / "limitations.md", _render_limitations(summary))

    readback = validate_focused_review_brief(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_focused_review_brief(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_focused_review_brief(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate the generated focused review brief package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_FOCUSED_REVIEW_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["focused_review_manifest.json"])
    summary = _load_json_if_present(files["review_summary.json"])
    decision_card = _load_json_if_present(files["review_decision_card.json"])
    source_index = _load_json_if_present(files["detail_source_index.json"])

    json_payloads = {
        "focused_review_manifest": manifest,
        "review_summary": summary,
        "review_decision_card": decision_card,
        "detail_source_index": source_index,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["focused_review_manifest"]
    summary = json_payloads["review_summary"]
    decision_card = json_payloads["review_decision_card"]
    source_index = json_payloads["detail_source_index"]

    if manifest.get("artifact_kind") != "episode-focused-review-brief":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if summary.get("status") != "focused_review_brief_ready_local_offline":
        failed_checks.append("summary_status_mismatch")

    primary_questions = decision_card.get("primary_questions")
    if not isinstance(primary_questions, list) or len(primary_questions) != 1 or not primary_questions[0]:
        failed_checks.append("primary_question_count_not_one")
    if decision_card.get("decision_card_count") != 1:
        failed_checks.append("decision_card_count_not_one")

    top_summary_lines = summary.get("top_summary_lines")
    if not isinstance(top_summary_lines, list) or len(top_summary_lines) != 3:
        failed_checks.append("top_summary_not_three_lines")
        top_summary_lines = []
    if any(len(str(line)) > 160 for line in top_summary_lines):
        failed_checks.append("top_summary_line_too_long")

    action_cards = decision_card.get("next_action_cards")
    if not isinstance(action_cards, list) or len(action_cards) != 3:
        failed_checks.append("next_action_card_count_not_three")
    evidence_cards = summary.get("evidence_cards")
    if not isinstance(evidence_cards, list) or len(evidence_cards) != 3:
        failed_checks.append("evidence_card_count_not_three")

    boundary_flags = summary.get("boundary_flags", {})
    if not isinstance(boundary_flags, dict):
        boundary_flags = {}
        failed_checks.append("boundary_flags_invalid")
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary_flags.get(flag) is not True:
            failed_checks.append(f"boundary_flag_missing_or_false:{flag}")

    html_text = files["focused_review_brief.html"].read_text(encoding="utf-8") if files["focused_review_brief.html"].exists() else ""
    markdown_text = files["focused_review_brief.md"].read_text(encoding="utf-8") if files["focused_review_brief.md"].exists() else ""
    missing_html_markers = [marker for marker in REQUIRED_HTML_MARKERS if marker not in html_text]
    failed_checks.extend(f"missing_html_marker:{marker}" for marker in missing_html_markers)
    if "<details" not in html_text:
        failed_checks.append("details_disclosure_missing")
    if "remaining_mismatch_ledger.json" not in html_text:
        failed_checks.append("source_record_marker_missing")
    if "## Details" in markdown_text:
        failed_checks.append("markdown_fallback_too_detail_heavy")
    if len(markdown_text.splitlines()) > 80:
        failed_checks.append("markdown_fallback_too_long")

    forbidden_hits = _forbidden_true_claims(root)
    external_refs = _external_refs(root)
    pure_white_hits = _pure_white_hits(root)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_hits)
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"pure_white_marker:{hit}" for hit in pure_white_hits)

    source_rows = source_index.get("source_artifacts", [])
    if not isinstance(source_rows, list) or len(source_rows) < 6:
        failed_checks.append("source_artifacts_too_small")
    if source_index.get("legacy_story_role") != "source_record":
        failed_checks.append("legacy_story_not_source_record")

    checks = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
        "primary_question_count": len(primary_questions) if isinstance(primary_questions, list) else 0,
        "decision_card_count": decision_card.get("decision_card_count"),
        "top_summary_line_count": len(top_summary_lines),
        "top_summary_short": bool(top_summary_lines) and all(len(str(line)) <= 160 for line in top_summary_lines),
        "next_action_card_count": len(action_cards) if isinstance(action_cards, list) else 0,
        "evidence_card_count": len(evidence_cards) if isinstance(evidence_cards, list) else 0,
        "dark_mode_css_markers_present": not missing_html_markers,
        "details_disclosure_present": "<details" in html_text,
        "boundary_flags_present": all(boundary_flags.get(flag) is True for flag in REQUIRED_BOUNDARY_FLAGS),
        "external_refs_absent": not external_refs,
        "pure_white_background_absent": not pure_white_hits,
        "forbidden_true_claims_absent": not forbidden_hits,
        "markdown_fallback_concise": len(markdown_text.splitlines()) <= 80 and "## Details" not in markdown_text,
        "legacy_story_source_record": source_index.get("legacy_story_role") == "source_record",
    }

    return {
        "schema_version": "focused_review_brief_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": checks,
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "source_artifact_id": summary.get("source_artifact_id"),
        "selected_candidate_id": summary.get("selected_candidate_id"),
        "primary_question": primary_questions[0] if isinstance(primary_questions, list) and primary_questions else None,
        "top_summary_length": len(top_summary_lines),
        "decision_cards": len(action_cards) if isinstance(action_cards, list) else 0,
        "evidence_cards": len(evidence_cards) if isinstance(evidence_cards, list) else 0,
        "dark_mode_support": summary.get("dark_mode_support"),
        "external_dependency_status": "absent" if not external_refs else "present",
        "white_background_status": "absent" if not pure_white_hits else "present",
        "details_policy": summary.get("details_policy"),
        "primary_machine_readable": str(root / "validation_readback.json"),
        "primary_human_review": str(root / "focused_review_brief.html"),
        "markdown_fallback": str(root / "focused_review_brief.md"),
        "next_action": summary.get("next_action"),
    }


def _input_paths(source_root: Path, reviewer_root: Path) -> dict[str, Path]:
    return {
        "reviewer_manifest": reviewer_root / "reviewer_packet_manifest.json",
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


def _review_summary_payload(
    *,
    artifact_id: str,
    payloads: dict[str, Any],
    source_root: Path,
    reviewer_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    repair = payloads["alignment_repair_summary"]
    boundary = payloads["boundary_status_readback"]
    ledger = payloads["remaining_mismatch_ledger"]
    validation = payloads["reviewer_validation"]
    crosswalk = payloads["source_artifact_crosswalk_readback"]

    evidence_cards = _evidence_cards(repair)
    boundary_flags = _dict(boundary.get("boundary_flags"))
    return {
        "schema_version": "focused_review_summary.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-focused-review-brief",
        "status": "focused_review_brief_ready_local_offline",
        "source_artifact_id": repair.get("artifact_id"),
        "source_packet_status": validation.get("status"),
        "source_package_dir": _relpath(source_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "selected_candidate_id": repair.get("selected_candidate_id"),
        "primary_message": (
            "Episode 002 is ready for a focused local review decision, not for production."
        ),
        "top_summary_lines": [
            "GUI, import preview, and thumbnail proof are aligned as local review evidence.",
            "The package is still dry-run and sample-backed: no real transcript, YMM4 import, render, or production claim.",
            "Reviewer should choose real input replacement, gated YMM4 import observation without render, or hold.",
        ],
        "current_state": {
            "review_surface": "focused_dark_html_primary",
            "source_record": _relpath(reviewer_root / "aligned_review_story.md", repo_root),
            "legacy_story_role": "source_record",
            "source_crosswalk_status": crosswalk.get("overall_status"),
            "still_open_mismatch_count": ledger.get("still_open_mismatch_count"),
            "source_surfaces_ready": all(card.get("status") == "ready" for card in evidence_cards),
        },
        "evidence_cards": evidence_cards,
        "boundary_flags": boundary_flags,
        "gate_strip": _gate_strip(boundary_flags),
        "details_policy": (
            "Only decision, summary, next actions, evidence cards, and gate strip are top-level; "
            "ledger and source index are secondary details."
        ),
        "dark_mode_support": {
            "first_party_css": True,
            "color_scheme": "dark light",
            "prefers_color_scheme": True,
            "external_dependencies": False,
            "pure_white_background": False,
        },
        "source_record": _relpath(reviewer_root / "aligned_review_story.md", repo_root),
        "primary_human_review": _relpath(output_root / "focused_review_brief.html", repo_root),
        "markdown_fallback": _relpath(output_root / "focused_review_brief.md", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "next_action": "Open focused_review_brief.html and answer the single primary review question.",
    }


def _decision_card_payload(artifact_id: str, payloads: dict[str, Any], summary: dict[str, Any]) -> dict[str, Any]:
    next_action = payloads["next_action_readback"]
    return {
        "schema_version": "focused_review_decision_card.v1",
        "artifact_id": artifact_id,
        "decision_card_count": 1,
        "primary_questions": [
            "Which next path should episode 002 take after this local dry-run review?"
        ],
        "current_state": "Focused local review is ready; production, YMM4 import/render, and public gates remain closed.",
        "reviewer_decision_prompt": "Pick one path after reading the decision card and evidence cards.",
        "recommended_default": (
            "Choose real_input_replacement if verified local source/transcript material exists; "
            "otherwise hold unless YMM4 observation is explicitly selected."
        ),
        "next_action_cards": [
            {
                "option_id": "real_input_replacement",
                "label": "Real input replacement",
                "status": "advisory_deferred",
                "use_when": "Verified local real source/transcript material is available.",
                "effect": "Moves from sample fixture to production-relevant content without YMM4 or publication gates.",
                "requires": "Human-approved local transcript/source provenance.",
            },
            {
                "option_id": "actual_yymm4_import_observation_no_render",
                "label": "YMM4 observation without render",
                "status": "blocked_by_true_gate",
                "use_when": "Human explicitly chooses to inspect import behavior.",
                "effect": "Observes CSV/VoiceItem/timing behavior only; no render or production .ymmp claim.",
                "requires": "Explicit human decision to launch/import in YMM4.",
            },
            {
                "option_id": "hold_review_later",
                "label": "Hold / review later",
                "status": "safe_hold",
                "use_when": "The brief is insufficient, input is unavailable, or no YMM4 gate is selected.",
                "effect": "Keeps the current local/offline reviewer packet as the record.",
                "requires": "No new action.",
            },
        ],
        "not_claimed": [
            "production readiness",
            "real transcript availability",
            "YMM4 import or render",
            "final thumbnail approval",
            "rights or public-ready acceptance",
            "YouTube upload or visibility change",
        ],
        "source_next_action": next_action.get("next_safe_local_action"),
        "primary_human_review": summary.get("primary_human_review"),
    }


def _detail_source_index(
    *,
    artifact_id: str,
    payloads: dict[str, Any],
    paths: dict[str, Path],
    source_root: Path,
    reviewer_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    crosswalk = payloads["source_artifact_crosswalk_readback"]
    source_rows = []
    for artifact in _list(crosswalk.get("source_artifact_rows")):
        if isinstance(artifact, dict):
            source_rows.append(dict(artifact))
    focused_rows = [
        _source_row("focused_review_html", output_root / "focused_review_brief.html", ["focused_review_brief"], repo_root),
        _source_row("focused_review_markdown", output_root / "focused_review_brief.md", ["focused_review_brief"], repo_root),
        _source_row("review_decision_card", output_root / "review_decision_card.json", ["focused_review_brief"], repo_root),
        _source_row("review_summary", output_root / "review_summary.json", ["focused_review_brief"], repo_root),
        _source_row("legacy_aligned_story", paths["aligned_review_story"], ["surface_alignment_review_packet"], repo_root),
    ]
    return {
        "schema_version": "focused_review_detail_source_index.v1",
        "artifact_id": artifact_id,
        "source_package_dir": _relpath(source_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "legacy_story_role": "source_record",
        "primary_review_surface": _relpath(output_root / "focused_review_brief.html", repo_root),
        "primary_machine_readable": _relpath(output_root / "validation_readback.json", repo_root),
        "source_artifacts": [*source_rows, *focused_rows],
        "source_readbacks": {
            "reviewer_packet": _relpath(paths["reviewer_validation"], repo_root),
            "gui_dashboard_panel": _relpath(paths["gui_readback"], repo_root),
            "yymm4_import_preview_pack": _relpath(paths["import_readback"], repo_root),
            "thumbnail_visual_proof_pack": _relpath(paths["thumbnail_readback"], repo_root),
        },
    }


def _manifest_payload(
    artifact_id: str,
    summary: dict[str, Any],
    source_index: dict[str, Any],
    source_root: Path,
    reviewer_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "focused_review_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "episode-focused-review-brief",
        "status": "generated",
        "source_package_dir": _relpath(source_root, repo_root),
        "reviewer_packet_dir": _relpath(reviewer_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "files": {name: _relpath(output_root / name, repo_root) for name in REQUIRED_FOCUSED_REVIEW_FILES},
        "source_artifact_id": summary.get("source_artifact_id"),
        "primary_review_surface": summary.get("primary_human_review"),
        "primary_machine_readable": summary.get("primary_machine_readable"),
        "markdown_fallback": summary.get("markdown_fallback"),
        "source_artifact_count": len(_list(source_index.get("source_artifacts"))),
        "boundary_flags": summary.get("boundary_flags"),
        "next_action": summary.get("next_action"),
    }


def _render_html(summary: dict[str, Any], decision_card: dict[str, Any], source_index: dict[str, Any]) -> str:
    question = _escape(_list(decision_card.get("primary_questions"))[0])
    summary_items = "\n".join(f"<li>{_escape(line)}</li>" for line in _list(summary.get("top_summary_lines")))
    action_cards = "\n".join(_render_action_card(card) for card in _list(decision_card.get("next_action_cards")))
    evidence_cards = "\n".join(_render_evidence_card(card) for card in _list(summary.get("evidence_cards")))
    gate_chips = "\n".join(f'<span class="chip">{_escape(gate)}</span>' for gate in _list(summary.get("gate_strip")))
    source_paths = "\n".join(
        f"<li><code>{_escape(row.get('repo_relative_path'))}</code></li>"
        for row in _list(source_index.get("source_artifacts"))[:10]
        if isinstance(row, dict)
    )
    not_claimed = "\n".join(f"<li>{_escape(item)}</li>" for item in _list(decision_card.get("not_claimed")))
    return f"""<!doctype html>
<html lang="en" data-focused-review-brief="true">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 Focused Review Brief</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #0b1020;
      --panel: #121a2b;
      --panel-2: #172033;
      --text: #e7edf7;
      --muted: #9fb0c7;
      --line: #334155;
      --accent: #2dd4bf;
      --warn: #facc15;
      --blocked: #fb7185;
      --ok: #86efac;
      --shadow: 0 18px 50px rgba(0, 0, 0, 0.32);
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #eef3f8;
        --panel: #f8fafc;
        --panel-2: #edf2f7;
        --text: #172033;
        --muted: #475569;
        --line: #cbd5e1;
        --accent: #0f766e;
        --warn: #8a5a00;
        --blocked: #be123c;
        --ok: #166534;
        --shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(135deg, var(--bg), #111827 70%);
      color: var(--text);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }}
    main {{ width: min(1120px, calc(100% - 32px)); margin: 0 auto; padding: 28px 0 36px; }}
    .hero {{ display: grid; gap: 16px; grid-template-columns: 1.4fr 0.8fr; align-items: stretch; }}
    .card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; box-shadow: var(--shadow); }}
    .decision {{ padding: 22px; border-color: var(--accent); }}
    .kicker {{ margin: 0 0 8px; color: var(--accent); font-size: 0.82rem; font-weight: 700; text-transform: uppercase; }}
    h1 {{ margin: 0 0 10px; font-size: clamp(1.6rem, 3vw, 2.6rem); line-height: 1.05; letter-spacing: 0; }}
    h2 {{ margin: 0 0 12px; font-size: 1rem; letter-spacing: 0; }}
    p {{ line-height: 1.55; }}
    .question {{ margin: 0; font-size: 1.15rem; font-weight: 700; }}
    .state {{ display: grid; gap: 8px; padding: 18px; }}
    .state strong {{ color: var(--ok); }}
    .summary {{ margin: 18px 0; padding: 16px 18px; }}
    .summary ol {{ margin: 0; padding-left: 22px; line-height: 1.55; }}
    .grid3 {{ display: grid; gap: 14px; grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    .mini {{ padding: 16px; min-height: 190px; }}
    .mini p {{ margin: 8px 0 0; color: var(--muted); font-size: 0.94rem; }}
    .status {{ display: inline-flex; padding: 4px 8px; border-radius: 999px; background: var(--panel-2); color: var(--accent); font-size: 0.8rem; }}
    .gate {{ margin: 18px 0; padding: 14px; display: flex; flex-wrap: wrap; gap: 8px; }}
    .chip {{ padding: 7px 10px; border: 1px solid var(--line); border-radius: 999px; background: var(--panel-2); color: var(--muted); font-size: 0.84rem; }}
    details {{ margin-top: 16px; padding: 14px 16px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; }}
    summary {{ cursor: pointer; font-weight: 700; }}
    code {{ color: var(--accent); overflow-wrap: anywhere; }}
    ul.compact {{ margin: 10px 0 0; padding-left: 20px; color: var(--muted); }}
    @media (max-width: 820px) {{
      .hero, .grid3 {{ grid-template-columns: 1fr; }}
      main {{ width: min(100% - 20px, 1120px); padding-top: 16px; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <article class="card decision" data-section="decision-card">
        <p class="kicker">Episode 002 focused review brief</p>
        <h1>Decide the next path, not the whole project.</h1>
        <p class="question">{question}</p>
        <p>{_escape(decision_card.get("recommended_default"))}</p>
      </article>
      <aside class="card state">
        <h2>Current State</h2>
        <span><strong>Ready:</strong> focused local review surface</span>
        <span><strong>Source record:</strong> <code>{_escape(summary.get("source_record"))}</code></span>
        <span><strong>Still open mismatch:</strong> {_escape(summary.get("current_state", {}).get("still_open_mismatch_count"))}</span>
        <span><strong>Production:</strong> not claimed</span>
      </aside>
    </section>

    <section class="card summary" data-section="three-line-summary">
      <ol>{summary_items}</ol>
    </section>

    <section data-section="next-action-cards">
      <h2>Next Action Choices</h2>
      <div class="grid3">{action_cards}</div>
    </section>

    <section data-section="evidence-cards">
      <h2>Evidence Cards</h2>
      <div class="grid3">{evidence_cards}</div>
    </section>

    <section class="card gate" data-section="gate-strip">{gate_chips}</section>

    <details>
      <summary>Closed claims and not-done boundaries</summary>
      <ul class="compact">{not_claimed}</ul>
    </details>

    <details>
      <summary>Secondary source index</summary>
      <p>The old aligned story remains a source record. The focused HTML is the primary review surface.</p>
      <p>Ledger source: <code>remaining_mismatch_ledger.json</code></p>
      <ul class="compact">{source_paths}</ul>
    </details>
  </main>
</body>
</html>
"""


def _render_markdown(summary: dict[str, Any], decision_card: dict[str, Any], source_index: dict[str, Any]) -> str:
    question = _list(decision_card.get("primary_questions"))[0]
    lines = [
        "# Episode 002 Focused Review Brief",
        "",
        f"Primary question: {question}",
        "",
        "## Current State",
        "",
        "- Focused local review surface is ready.",
        f"- Source record remains `{summary.get('source_record')}`.",
        "- Production, YMM4 import/render, public, rights, and final thumbnail claims remain closed.",
        "",
        "## Three-Line Summary",
        "",
    ]
    lines.extend(f"{index}. {line}" for index, line in enumerate(_list(summary.get("top_summary_lines")), start=1))
    lines.extend(["", "## Next Choices", ""])
    for card in _list(decision_card.get("next_action_cards")):
        lines.append(
            f"- {card.get('label')}: {card.get('use_when')} Effect: {card.get('effect')}"
        )
    lines.extend(["", "## Evidence", ""])
    for card in _list(summary.get("evidence_cards")):
        lines.append(
            f"- {card.get('label')}: {card.get('status')} / {card.get('message')} Review: `{card.get('human_review')}`"
        )
    lines.extend(
        [
            "",
            "## Gates",
            "",
            ", ".join(str(gate) for gate in _list(summary.get("gate_strip"))),
            "",
            "Primary machine readback:",
            "",
            f"`{source_index.get('primary_machine_readable')}`",
            "",
        ]
    )
    return "\n".join(lines)


def _render_action_card(card: dict[str, Any]) -> str:
    return "\n".join(
        [
            '      <article class="card mini">',
            f'        <span class="status">{_escape(card.get("status"))}</span>',
            f"        <h2>{_escape(card.get('label'))}</h2>",
            f"        <p><strong>Use when:</strong> {_escape(card.get('use_when'))}</p>",
            f"        <p><strong>Effect:</strong> {_escape(card.get('effect'))}</p>",
            f"        <p><strong>Requires:</strong> {_escape(card.get('requires'))}</p>",
            "      </article>",
        ]
    )


def _render_evidence_card(card: dict[str, Any]) -> str:
    return "\n".join(
        [
            '      <article class="card mini">',
            f'        <span class="status">{_escape(card.get("status"))}</span>',
            f"        <h2>{_escape(card.get('label'))}</h2>",
            f"        <p>{_escape(card.get('message'))}</p>",
            f"        <p><code>{_escape(card.get('human_review'))}</code></p>",
            "      </article>",
        ]
    )


def _render_review_checklist(summary: dict[str, Any], decision_card: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Focused Review Brief Checklist",
            "",
            "- Open `focused_review_brief.html` first.",
            "- Answer the single primary question before reading secondary details.",
            "- Use `focused_review_brief.md` only as a concise fallback.",
            "- Confirm the gate strip keeps dry-run, sample fixture, no real transcript, rights, publication, YMM4, thumbnail, validation-noise, and production boundaries visible.",
            "- Treat `aligned_review_story.md` as the source record, not the primary review surface.",
            "",
            "Primary question:",
            "",
            str(_list(decision_card.get("primary_questions"))[0]),
            "",
            "Current safe action:",
            "",
            str(summary.get("next_action")),
            "",
        ]
    )


def _render_limitations(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Focused Review Brief Limitations",
            "",
            "This package is a local/offline decision surface over the existing surface alignment reviewer packet.",
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
            str(summary.get("primary_human_review")),
            "",
        ]
    )


def _evidence_cards(repair: dict[str, Any]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    messages = {
        "gui_dashboard_panel": "GUI/dashboard state is already aligned and should be read as evidence, not as the current build target.",
        "yymm4_import_preview_pack": "CSV/import-prep package is locally reviewable; it has not been imported into YMM4.",
        "thumbnail_visual_proof_pack": "Thumbnail proof is context only and is not final thumbnail approval.",
    }
    for surface in _list(repair.get("surfaces")):
        if not isinstance(surface, dict):
            continue
        surface_id = str(surface.get("surface_id"))
        cards.append(
            {
                "surface_id": surface_id,
                "label": surface.get("label"),
                "status": surface.get("status"),
                "role": surface.get("role_in_alignment"),
                "message": messages.get(surface_id, "Local review evidence."),
                "human_review": surface.get("primary_human_review"),
                "machine_readable": surface.get("primary_machine_readable"),
            }
        )
    return cards


def _gate_strip(boundary_flags: dict[str, Any]) -> list[str]:
    ordered = [
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
    ]
    return [flag for flag in ordered if boundary_flags.get(flag) is True]


def _source_row(artifact_id: str, path: Path, surfaces: list[str], repo_root: Path) -> dict[str, Any]:
    generated_output = artifact_id.startswith(("focused_", "review_"))
    return {
        "artifact_id": artifact_id,
        "repo_relative_path": _relpath(path, repo_root),
        "surfaces": surfaces,
        "exists": path.exists() or generated_output,
        "classification": "focused_review_output" if generated_output else "source_record",
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
