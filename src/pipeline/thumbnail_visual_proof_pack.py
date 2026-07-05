"""Static local/offline thumbnail visual proof package.

The proof uses only current repo-local pilot metadata, abstract SVG shapes, and
text blocks. It does not download media, call image APIs, render a final
thumbnail, or claim production/public readiness.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

from src.pipeline.dashboard_readiness_ingest import STATUS_CATEGORIES

DEFAULT_OUTPUT_DIRNAME = "thumbnail_visual_proof_pack"
DEFAULT_ARTIFACT_ID = "thumbnail_visual_proof_pack_001"

REQUIRED_THUMBNAIL_PROOF_FILES = (
    "thumbnail_proof_manifest.json",
    "thumbnail_concepts.json",
    "title_text_candidates.json",
    "visual_constraints.json",
    "forbidden_claims_and_rights_boundaries.md",
    "thumbnail_proof_panel.html",
    "thumbnail_proof_panel.md",
    "thumbnail_layout_proof.svg",
    "source_artifact_index.json",
    "validation_readback.json",
    "review_checklist.md",
    "limitations.md",
)

REQUIRED_HTML_MARKERS = (
    'data-thumbnail-proof-pack="true"',
    'data-section="layout-proof"',
    'data-section="title-candidates"',
    'data-section="visual-constraints"',
    'data-section="boundary-status"',
    'data-section="source-artifact-index"',
    'data-status="ready"',
    'data-status="partial"',
    'data-status="sample_fixture_not_real"',
    'data-status="draft_offline"',
    'data-status="blocked_by_real_input"',
    'data-status="blocked_by_true_gate"',
    'data-status="deferred"',
    'data-status="missing"',
    'data-status="unknown"',
)

EXTERNAL_MEDIA_PATTERNS = (
    re.compile(r"<image\b", re.IGNORECASE),
    re.compile(r"\b(src|href)\s*=\s*['\"]https?://", re.IGNORECASE),
    re.compile(r"url\(\s*['\"]?https?://", re.IGNORECASE),
)


def build_thumbnail_visual_proof_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a static thumbnail visual proof pack from current pilot artifacts."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)

    repo_root = _find_repo_root(source_root)
    snapshot = _load_snapshot(source_root)
    selected_candidate = _selected_candidate(snapshot)
    thumbnail_profile = selected_candidate.get("thumbnail_profile", {})
    yukkuri_profile = selected_candidate.get("yukkuri_profile", {})
    source_boundary = selected_candidate.get("source_boundary", {})

    title_candidates = _title_text_candidates(selected_candidate, thumbnail_profile)
    concepts = _thumbnail_concepts(selected_candidate, thumbnail_profile, yukkuri_profile)
    visual_constraints = _visual_constraints(thumbnail_profile, source_boundary)
    status_rows = _status_rows(snapshot, source_boundary, repo_root)
    summary = _summary_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        selected_candidate=selected_candidate,
        title_candidates=title_candidates,
        concepts=concepts,
        visual_constraints=visual_constraints,
        status_rows=status_rows,
        snapshot=snapshot,
    )
    svg_text = _render_svg_proof(summary, title_candidates, concepts, visual_constraints)
    panel_html = _render_html_panel(summary, title_candidates, concepts, visual_constraints, status_rows)
    panel_md = _render_markdown_panel(summary, title_candidates, concepts, visual_constraints, status_rows)
    manifest = _manifest_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        selected_candidate=selected_candidate,
        summary=summary,
        snapshot=snapshot,
    )

    _write_json(output_root / "thumbnail_proof_manifest.json", manifest)
    _write_json(output_root / "thumbnail_concepts.json", concepts)
    _write_json(output_root / "title_text_candidates.json", title_candidates)
    _write_json(output_root / "visual_constraints.json", visual_constraints)
    _write_text(output_root / "forbidden_claims_and_rights_boundaries.md", _render_rights_boundaries(summary))
    _write_text(output_root / "thumbnail_proof_panel.html", panel_html)
    _write_text(output_root / "thumbnail_proof_panel.md", panel_md)
    _write_text(output_root / "thumbnail_layout_proof.svg", svg_text)
    _write_text(output_root / "review_checklist.md", _render_review_checklist(summary))
    _write_text(output_root / "limitations.md", _render_limitations(summary))
    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(snapshot, output_root, repo_root))

    readback = validate_thumbnail_visual_proof_pack(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(snapshot, output_root, repo_root))
    final_readback = validate_thumbnail_visual_proof_pack(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    _write_json(output_root / "source_artifact_index.json", _source_artifact_index(snapshot, output_root, repo_root))
    return final_readback


def validate_thumbnail_visual_proof_pack(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate generated thumbnail visual proof files and closed media gates."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_THUMBNAIL_PROOF_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["thumbnail_proof_manifest.json"])
    concepts = _load_json_if_present(files["thumbnail_concepts.json"])
    title_candidates = _load_json_if_present(files["title_text_candidates.json"])
    constraints = _load_json_if_present(files["visual_constraints.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])

    json_payloads = {
        "thumbnail_proof_manifest": manifest,
        "thumbnail_concepts": concepts,
        "title_text_candidates": title_candidates,
        "visual_constraints": constraints,
        "source_artifact_index": source_index,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["thumbnail_proof_manifest"]
    concepts = json_payloads["thumbnail_concepts"]
    title_candidates = json_payloads["title_text_candidates"]
    constraints = json_payloads["visual_constraints"]
    source_index = json_payloads["source_artifact_index"]

    if manifest.get("artifact_kind") != "thumbnail-visual-proof-pack":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if not title_candidates.get("primary_title_candidates"):
        failed_checks.append("primary_title_candidates_missing")
    if not title_candidates.get("short_text_candidates"):
        failed_checks.append("short_text_candidates_missing")
    if not concepts.get("concepts"):
        failed_checks.append("thumbnail_concepts_missing")
    if not constraints.get("rights_boundaries", {}).get("no_external_media"):
        failed_checks.append("external_media_boundary_missing")
    if constraints.get("proof_status") != "static_proof_only_not_final_thumbnail":
        failed_checks.append("proof_status_unexpected")

    html_text = files["thumbnail_proof_panel.html"].read_text(encoding="utf-8") if files["thumbnail_proof_panel.html"].exists() else ""
    markdown_text = files["thumbnail_proof_panel.md"].read_text(encoding="utf-8") if files["thumbnail_proof_panel.md"].exists() else ""
    svg_text = files["thumbnail_layout_proof.svg"].read_text(encoding="utf-8") if files["thumbnail_layout_proof.svg"].exists() else ""
    rights_text = (
        files["forbidden_claims_and_rights_boundaries.md"].read_text(encoding="utf-8")
        if files["forbidden_claims_and_rights_boundaries.md"].exists()
        else ""
    )
    combined_review_text = "\n".join([html_text, markdown_text, svg_text, rights_text])
    external_reference_hits = _external_reference_hits(combined_review_text)
    failed_checks.extend(f"external_reference:{hit}" for hit in external_reference_hits)

    missing_html_markers = [marker for marker in REQUIRED_HTML_MARKERS if marker not in html_text]
    failed_checks.extend(f"missing_html_marker:{marker}" for marker in missing_html_markers)
    for state in _required_visible_states():
        if state not in combined_review_text:
            failed_checks.append(f"status_text_missing:{state}")
    if "<svg" not in svg_text or "</svg>" not in svg_text:
        failed_checks.append("svg_root_missing")
    if "155" not in svg_text or "140" not in svg_text:
        failed_checks.append("speed_delta_not_visible_in_svg")
    if "source_artifact_index" not in html_text:
        failed_checks.append("html_source_artifact_index_missing")
    if not source_index.get("source_inputs"):
        failed_checks.append("source_artifact_index_empty")

    boundary_status = manifest.get("boundary_status", {})
    if boundary_status.get("rights_status") != "sample_only_no_publication":
        failed_checks.append("rights_status_not_preserved")
    if boundary_status.get("public_upload_status") != "blocked_by_true_gate":
        failed_checks.append("public_upload_gate_not_closed")
    if boundary_status.get("external_media_status") != "blocked_by_true_gate":
        failed_checks.append("external_media_gate_not_closed")
    if boundary_status.get("thumbnail_image_status") != "deferred":
        failed_checks.append("thumbnail_generation_not_deferred")
    if boundary_status.get("transcript_status") != "sample_fixture_not_real":
        failed_checks.append("sample_fixture_status_not_preserved")

    return {
        "schema_version": "thumbnail_visual_proof_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
            "title_candidates_present": bool(title_candidates.get("primary_title_candidates")),
            "concepts_present": bool(concepts.get("concepts")),
            "visual_constraints_present": bool(constraints.get("layout_constraints")),
            "html_markers_present": not missing_html_markers,
            "svg_static_proof_present": "<svg" in svg_text and "</svg>" in svg_text,
            "no_external_references": not external_reference_hits,
            "sample_fixture_preserved": boundary_status.get("transcript_status") == "sample_fixture_not_real",
            "rights_gate_closed": boundary_status.get("rights_status") == "sample_only_no_publication",
            "public_upload_gate_closed": boundary_status.get("public_upload_status") == "blocked_by_true_gate",
            "external_media_gate_closed": boundary_status.get("external_media_status") == "blocked_by_true_gate",
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "source_package_dir": manifest.get("source_package_dir"),
        "selected_candidate_id": manifest.get("selected_candidate_id"),
        "primary_title": title_candidates.get("primary_title_candidates", [{}])[0].get("text")
        if title_candidates.get("primary_title_candidates")
        else None,
        "short_text_count": len(title_candidates.get("short_text_candidates", [])),
        "primary_machine_readable": str(root / "thumbnail_proof_manifest.json"),
        "primary_human_review": str(root / "thumbnail_proof_panel.html"),
        "primary_visual_proof": str(root / "thumbnail_layout_proof.svg"),
        "next_action": manifest.get("next_safe_local_action"),
    }


def _load_snapshot(source_root: Path) -> dict[str, Any]:
    dashboard_root = source_root / "dashboard_readiness_ingest"
    gui_root = source_root / "gui_dashboard_panel"
    import_root = source_root / "ymm4_import_preview_pack"
    transcript_root = source_root / "transcript_substitution_readiness"
    files = {
        "content_manifest": source_root / "MANIFEST.json",
        "topic_candidates": source_root / "topic_candidates.json",
        "episode_candidate": source_root / "episode_candidate_001.md",
        "thumbnail_brief": source_root / "thumbnail_brief_001.md",
        "content_dashboard": source_root / "dashboard_status.json",
        "dashboard_summary": dashboard_root / "readiness_summary.json",
        "gui_adapter": gui_root / "gui_dashboard_adapter.json",
        "gui_panel_html": gui_root / "dashboard_panel_preview.html",
        "import_summary": import_root / "import_readiness_summary.json",
        "import_panel_md": import_root / "import_preview_panel.md",
        "import_panel_html": import_root / "import_preview_panel.html",
        "transcript_probe": transcript_root / "transcript_source_probe.json",
    }
    payloads = {
        name: _load_json_if_present(path)
        for name, path in files.items()
        if path.suffix.lower() == ".json"
    }
    return {
        "source_root": source_root,
        "dashboard_root": dashboard_root,
        "gui_root": gui_root,
        "import_root": import_root,
        "transcript_root": transcript_root,
        "files": files,
        "payloads": payloads,
    }


def _selected_candidate(snapshot: dict[str, Any]) -> dict[str, Any]:
    manifest = _payload(snapshot, "content_manifest")
    candidate_id = manifest.get("selected_candidate_id")
    candidates = _payload(snapshot, "topic_candidates").get("candidates", [])
    for candidate in candidates if isinstance(candidates, list) else []:
        if isinstance(candidate, dict) and candidate.get("candidate_id") == candidate_id:
            return candidate
    if isinstance(candidates, list) and candidates and isinstance(candidates[0], dict):
        return candidates[0]
    return {
        "candidate_id": candidate_id or "unknown",
        "title": manifest.get("selected_title") or "unknown",
        "thumbnail_profile": {},
        "source_boundary": {},
        "yukkuri_profile": {},
    }


def _title_text_candidates(candidate: dict[str, Any], thumbnail: dict[str, Any]) -> dict[str, Any]:
    title_hook = str(thumbnail.get("title_hook") or candidate.get("title") or "Untitled")
    full_title = str(candidate.get("title") or title_hook)
    short_candidates = [
        {"text": str(text), "role": "short_overlay", "state": "draft_offline"}
        for text in thumbnail.get("short_text_candidates", [])
        if str(text).strip()
    ]
    if not short_candidates:
        short_candidates.append({"text": title_hook, "role": "short_overlay", "state": "draft_offline"})
    return {
        "schema_version": "thumbnail_title_text_candidates.v1",
        "primary_title_candidates": [
            {
                "text": title_hook,
                "role": "primary_numeric_hook",
                "state": "draft_offline",
                "reason": "uses the existing thumbnail_profile.title_hook",
            },
            {
                "text": full_title,
                "role": "full_episode_title_reference",
                "state": "draft_offline",
                "reason": "too long for final thumbnail unless compressed",
            },
        ],
        "short_text_candidates": short_candidates,
        "composition_pairings": [
            {
                "primary": title_hook,
                "secondary": short_candidates[0]["text"],
                "state": "ready",
                "note": "preferred first-pass proof pairing",
            },
            {
                "primary": title_hook,
                "secondary": short_candidates[min(1, len(short_candidates) - 1)]["text"],
                "state": "draft_offline",
                "note": "alternate emotional hook",
            },
        ],
        "text_constraints": {
            "max_primary_tokens": 4,
            "max_short_text_candidates_on_canvas": 1,
            "avoid_official_names_logos_or_broadcast_framing": True,
        },
    }


def _thumbnail_concepts(
    candidate: dict[str, Any],
    thumbnail: dict[str, Any],
    yukkuri_profile: dict[str, Any],
) -> dict[str, Any]:
    title_hook = str(thumbnail.get("title_hook") or candidate.get("title") or "Untitled")
    short_texts = [str(text) for text in thumbnail.get("short_text_candidates", []) if str(text).strip()]
    preferred_short = short_texts[0] if short_texts else title_hook
    return {
        "schema_version": "thumbnail_concepts.v1",
        "selected_candidate_id": candidate.get("candidate_id"),
        "concepts": [
            {
                "concept_id": "speed_drop_scoreboard",
                "state": "ready",
                "primary_title": title_hook,
                "short_text": preferred_short,
                "hook_rationale": yukkuri_profile.get("hook"),
                "composition": [
                    "top scoreboard strip with inning/count labels",
                    "left pitch card: 155 km/h four-seam",
                    "right pitch card: 140 km/h slider",
                    "large arrow connecting cards",
                    "low-outer strike-zone marker as original abstract graphic",
                ],
                "why_this_is_safe": "uses only original text, boxes, arrows, and abstract strike-zone shapes",
            },
            {
                "concept_id": "low_outer_zone_focus",
                "state": "draft_offline",
                "primary_title": title_hook,
                "short_text": short_texts[min(1, len(short_texts) - 1)] if short_texts else preferred_short,
                "hook_rationale": "make the viewer watch point visible without footage",
                "composition": [
                    "center strike-zone grid",
                    "highlighted low-outer target",
                    "small pitch cards in the corners",
                    "no player, team, league, or broadcast identity",
                ],
                "why_this_is_safe": "abstract zone diagram avoids media rights claims",
            },
            {
                "concept_id": "yukkuri_reaction_data_card",
                "state": "draft_offline",
                "primary_title": title_hook,
                "short_text": short_texts[min(2, len(short_texts) - 1)] if short_texts else preferred_short,
                "hook_rationale": "connects yukkuri reaction framing to a data-first thumbnail",
                "composition": [
                    "two generic circular host placeholders",
                    "oversized numeric speed drop",
                    "small caution chip marking sample-only status",
                ],
                "why_this_is_safe": "host placeholders are abstract shapes, not generated character art",
            },
        ],
        "source_thumbnail_profile": thumbnail,
    }


def _visual_constraints(thumbnail: dict[str, Any], source_boundary: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "thumbnail_visual_constraints.v1",
        "proof_status": "static_proof_only_not_final_thumbnail",
        "layout_constraints": {
            "canvas": "1280x720 SVG static proof",
            "safe_area_px": 48,
            "primary_title_zone": "upper-left to center",
            "secondary_text_zone": "lower-left badge",
            "visual_motif": thumbnail.get("visual_motif"),
            "contrast_target": "large light text on dark field with warm numeric accent",
            "palette": ["#0f1f2e", "#f8fafc", "#f59e0b", "#22c55e", "#ef4444"],
        },
        "rights_boundaries": {
            "source_rights_status": source_boundary.get("rights_status", "unknown"),
            "source_rights_caution": thumbnail.get("source_rights_caution"),
            "no_external_media": True,
            "no_logos_or_player_photos": True,
            "no_broadcast_stills": True,
            "no_public_ready_claim": True,
        },
        "forbidden_avoid_claims": thumbnail.get("forbidden_avoid_claims", []),
        "designer_note": thumbnail.get("designer_note"),
    }


def _status_rows(snapshot: dict[str, Any], source_boundary: dict[str, Any], repo_root: Path) -> list[dict[str, Any]]:
    import_summary = _payload(snapshot, "import_summary")
    import_boundary = import_summary.get("boundary_status", {})
    return [
        _row("content_spine", "Content spine package", "draft_offline", snapshot["files"]["content_manifest"], "current local/offline episode package", repo_root, True),
        _row("thumbnail_brief", "Thumbnail direction brief", "draft_offline", snapshot["files"]["thumbnail_brief"], "text-only direction brief, not an image", repo_root, True),
        _row("episode_candidate", "Episode candidate", "draft_offline", snapshot["files"]["episode_candidate"], "episode hook and beat outline are available", repo_root, True),
        _row("thumbnail_layout_proof", "Static layout proof", "ready", snapshot["source_root"] / DEFAULT_OUTPUT_DIRNAME / "thumbnail_layout_proof.svg", "abstract SVG proof generated locally", repo_root, True),
        _row("transcript_source", "Transcript source reality", "sample_fixture_not_real", snapshot["files"]["transcript_probe"], "current transcript still uses sample fixture", repo_root, False),
        _row("real_transcript_input", "Real transcript input", "blocked_by_real_input", snapshot["transcript_root"] / "real_input", "verified real transcript remains required before production", repo_root, False),
        _row("dashboard_readiness_ingest", "Dashboard readiness ingest", "ready", snapshot["files"]["dashboard_summary"], "read-only readiness summary exists", repo_root, True),
        _row("gui_dashboard_panel", "GUI dashboard panel", "ready", snapshot["files"]["gui_adapter"], "static dashboard panel exists", repo_root, True),
        _row("ymm4_import_preview", "YMM4 import preview pack", "ready", snapshot["files"]["import_summary"], "import preview exists but no actual YMM4 import was run", repo_root, True),
        _row("source_rights_status", "Source rights/public use", "blocked_by_true_gate", snapshot["files"]["topic_candidates"], str(source_boundary.get("rights_status", "unknown")), repo_root, False),
        _row("external_media_download", "External media download", "blocked_by_true_gate", snapshot["files"]["thumbnail_brief"], "no image, logo, screenshot, or sports media download is allowed here", repo_root, False),
        _row("public_upload_status", "Public upload status", "blocked_by_true_gate", snapshot["files"]["dashboard_summary"], "no YouTube upload, scheduling, visibility, or public-ready claim", repo_root, False),
        _row("thumbnail_image_generation", "Final thumbnail image generation", "deferred", snapshot["source_root"] / "thumbnail_output", "static proof only; no PNG/JPG final output generated", repo_root, False),
        _row("production_thumbnail_output", "Production thumbnail output", "missing", snapshot["source_root"] / "thumbnail_output" / "final_thumbnail.png", "no production image output exists", repo_root, False),
        _row("timing_audio_status", "Timing and audio status", "unknown", snapshot["files"]["import_summary"], f"timing={import_boundary.get('timing_status', 'unknown')}; audio={import_boundary.get('audio_status', 'unknown')}", repo_root, False),
        _row("ymm4_gui_render_status", "YMM4 GUI/import/render", "blocked_by_true_gate", snapshot["files"]["import_summary"], "no YMM4 GUI launch, import, or render in this proof", repo_root, False),
        _row("visual_polish", "Designer polish", "partial", snapshot["source_root"] / DEFAULT_OUTPUT_DIRNAME / "thumbnail_proof_panel.html", "composition reviewable, final taste and template transfer still pending", repo_root, True),
    ]


def _summary_payload(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    selected_candidate: dict[str, Any],
    title_candidates: dict[str, Any],
    concepts: dict[str, Any],
    visual_constraints: dict[str, Any],
    status_rows: list[dict[str, Any]],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    import_summary = _payload(snapshot, "import_summary")
    import_boundary = import_summary.get("boundary_status", {})
    source_boundary = selected_candidate.get("source_boundary", {})
    status_groups = {category: [] for category in STATUS_CATEGORIES}
    for row in status_rows:
        status_groups[row["state"]].append(row["capability_id"])
    return {
        "schema_version": "thumbnail_visual_proof_summary.v1",
        "artifact_id": artifact_id,
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": selected_candidate.get("candidate_id"),
        "selected_title": selected_candidate.get("title"),
        "title_hook": title_candidates["primary_title_candidates"][0]["text"],
        "short_text_candidates": [item["text"] for item in title_candidates["short_text_candidates"]],
        "preferred_concept_id": "speed_drop_scoreboard",
        "status_groups": {key: value for key, value in status_groups.items() if value},
        "status_rows": status_rows,
        "boundary_status": {
            "source_status": source_boundary.get("freshness_status", "unknown"),
            "rights_status": source_boundary.get("rights_status", "sample_only_no_publication"),
            "transcript_status": import_boundary.get("transcript_status", "sample_fixture_not_real"),
            "sample_fixture_status": "sample_fixture_not_real",
            "real_transcript_status": "blocked_by_real_input",
            "thumbnail_proof_status": "ready",
            "thumbnail_image_status": "deferred",
            "external_media_status": "blocked_by_true_gate",
            "public_upload_status": "blocked_by_true_gate",
            "yymm4_gui_import_render_status": "blocked_by_true_gate",
            "production_status": "blocked_by_true_gate",
        },
        "closed_gates": [
            "YouTube upload/publication/visibility change",
            "OAuth/API keys/payment",
            "rights/legal/public-ready acceptance",
            "live scraping/media download",
            "external image/media download or embedded copyrighted media",
            "external image generation API",
            "YMM4 GUI launch/import/render",
            "production .ymmp generation",
            "final thumbnail PNG/JPG generation",
            "cross-repo or destructive git",
        ],
        "external_media_policy": visual_constraints["rights_boundaries"],
        "next_safe_local_action": (
            "Open thumbnail_proof_panel.html or thumbnail_layout_proof.svg for offline composition review; "
            "then choose accept_direction, revise_copy, revise_layout, or hold before any real-source, "
            "YMM4, or final thumbnail work."
        ),
        "source_artifacts": {
            "thumbnail_brief": str(snapshot["files"]["thumbnail_brief"]),
            "episode_candidate": str(snapshot["files"]["episode_candidate"]),
            "dashboard_summary": str(snapshot["files"]["dashboard_summary"]),
            "gui_adapter": str(snapshot["files"]["gui_adapter"]),
            "import_summary": str(snapshot["files"]["import_summary"]),
        },
    }


def _manifest_payload(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    selected_candidate: dict[str, Any],
    summary: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "thumbnail_visual_proof_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "thumbnail-visual-proof-pack",
        "status": "generated",
        "source_package_dir": str(source_root),
        "output_dir": str(output_root),
        "selected_candidate_id": selected_candidate.get("candidate_id"),
        "files": {name: str(output_root / name) for name in REQUIRED_THUMBNAIL_PROOF_FILES},
        "source_inputs": {key: str(path) for key, path in snapshot["files"].items()},
        "boundary_status": summary["boundary_status"],
        "boundaries": {
            "local_offline_review_only": True,
            "static_visual_proof_only": True,
            "no_external_media_download": True,
            "no_embedded_external_images": True,
            "no_image_generation_api": True,
            "no_final_thumbnail_image_generation": True,
            "no_youtube_publication": True,
            "no_oauth_or_paid_api": True,
            "no_rights_or_legal_acceptance": True,
            "no_yymm4_gui_launch_import_or_render": True,
            "no_production_ymmp_generation": True,
        },
        "next_safe_local_action": summary["next_safe_local_action"],
    }


def _source_artifact_index(snapshot: dict[str, Any], output_root: Path, repo_root: Path) -> dict[str, Any]:
    source_inputs = []
    for key, path in snapshot["files"].items():
        payload = _payload(snapshot, key)
        source_inputs.append({
            "id": key,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": "ready" if path.exists() else "missing",
            "schema_version": payload.get("schema_version"),
        })
    generated_outputs = []
    for name in REQUIRED_THUMBNAIL_PROOF_FILES:
        path = output_root / name
        generated_outputs.append({
            "id": name,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": "ready" if path.exists() else "missing",
        })
    return {
        "schema_version": "thumbnail_visual_proof_source_artifact_index.v1",
        "source_inputs": source_inputs,
        "generated_outputs": generated_outputs,
        "artifact_counts": {
            "source_total": len(source_inputs),
            "source_present": sum(1 for item in source_inputs if item["exists"]),
            "generated_total": len(generated_outputs),
            "generated_present": sum(1 for item in generated_outputs if item["exists"]),
        },
    }


def _render_svg_proof(
    summary: dict[str, Any],
    title_candidates: dict[str, Any],
    concepts: dict[str, Any],
    visual_constraints: dict[str, Any],
) -> str:
    title = title_candidates["primary_title_candidates"][0]["text"]
    short_text = title_candidates["short_text_candidates"][0]["text"]
    concept = concepts["concepts"][0]
    note = visual_constraints["rights_boundaries"].get("source_rights_status", "unknown")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-labelledby="title desc" data-thumbnail-layout-proof="true">
  <title id="title">{_svg(title)} thumbnail layout proof</title>
  <desc id="desc">Static abstract proof using scoreboard, pitch cards, speed-drop arrow, and low-outer target. No external images.</desc>
  <rect width="1280" height="720" fill="#0f1f2e"/>
  <rect x="44" y="34" width="1192" height="74" rx="10" fill="#17283a" stroke="#9fb3c8" stroke-width="2"/>
  <text x="72" y="80" fill="#dbeafe" font-family="Segoe UI, Noto Sans, Arial" font-size="30" font-weight="700">7回表 1 OUT  B2-S2  RUNNER NONE</text>
  <text x="924" y="82" fill="#fbbf24" font-family="Segoe UI, Noto Sans, Arial" font-size="28" font-weight="700">SAMPLE ONLY</text>

  <rect x="72" y="150" width="454" height="286" rx="18" fill="#f8fafc" stroke="#38bdf8" stroke-width="5"/>
  <text x="104" y="210" fill="#0f172a" font-family="Segoe UI, Noto Sans, Arial" font-size="42" font-weight="800">FOUR-SEAM</text>
  <text x="104" y="334" fill="#ef4444" font-family="Segoe UI, Noto Sans, Arial" font-size="112" font-weight="900">155</text>
  <text x="342" y="334" fill="#0f172a" font-family="Segoe UI, Noto Sans, Arial" font-size="48" font-weight="700">km/h</text>
  <text x="104" y="394" fill="#334155" font-family="Segoe UI, Noto Sans, Arial" font-size="26">{_svg(summary.get("selected_candidate_id"))}</text>

  <rect x="754" y="150" width="454" height="286" rx="18" fill="#f8fafc" stroke="#22c55e" stroke-width="5"/>
  <text x="786" y="210" fill="#0f172a" font-family="Segoe UI, Noto Sans, Arial" font-size="42" font-weight="800">SLIDER</text>
  <text x="786" y="334" fill="#22c55e" font-family="Segoe UI, Noto Sans, Arial" font-size="112" font-weight="900">140</text>
  <text x="1024" y="334" fill="#0f172a" font-family="Segoe UI, Noto Sans, Arial" font-size="48" font-weight="700">km/h</text>
  <text x="786" y="394" fill="#334155" font-family="Segoe UI, Noto Sans, Arial" font-size="26">low-outer watch point</text>

  <path d="M548 290 L706 290" stroke="#f59e0b" stroke-width="20" stroke-linecap="round"/>
  <path d="M700 290 L660 252 M700 290 L660 328" stroke="#f59e0b" stroke-width="20" stroke-linecap="round"/>
  <text x="560" y="248" fill="#fef3c7" font-family="Segoe UI, Noto Sans, Arial" font-size="30" font-weight="800">-15 km/h</text>

  <rect x="820" y="462" width="250" height="170" rx="12" fill="#102235" stroke="#dbeafe" stroke-width="2"/>
  <line x1="903" y1="462" x2="903" y2="632" stroke="#64748b" stroke-width="2"/>
  <line x1="986" y1="462" x2="986" y2="632" stroke="#64748b" stroke-width="2"/>
  <line x1="820" y1="519" x2="1070" y2="519" stroke="#64748b" stroke-width="2"/>
  <line x1="820" y1="576" x2="1070" y2="576" stroke="#64748b" stroke-width="2"/>
  <circle cx="1040" cy="604" r="18" fill="#22c55e" stroke="#dcfce7" stroke-width="4"/>
  <text x="830" y="664" fill="#dbeafe" font-family="Segoe UI, Noto Sans, Arial" font-size="22">abstract strike zone only</text>

  <rect x="72" y="478" width="660" height="128" rx="18" fill="#0b1220" stroke="#f59e0b" stroke-width="4"/>
  <text x="104" y="540" fill="#f8fafc" font-family="Segoe UI, Noto Sans, Arial" font-size="64" font-weight="900">{_svg(title)}</text>
  <text x="108" y="586" fill="#fde68a" font-family="Segoe UI, Noto Sans, Arial" font-size="36" font-weight="800">{_svg(short_text)}</text>

  <text x="72" y="676" fill="#94a3b8" font-family="Segoe UI, Noto Sans, Arial" font-size="22">{_svg(concept.get("concept_id"))} / {_svg(note)} / no external media</text>
</svg>
"""


def _render_html_panel(
    summary: dict[str, Any],
    title_candidates: dict[str, Any],
    concepts: dict[str, Any],
    visual_constraints: dict[str, Any],
    rows: list[dict[str, Any]],
) -> str:
    title_rows = "\n".join(
        f"<tr><td>{_esc(item.get('role'))}</td><td>{_esc(item.get('text'))}</td><td><span class=\"status-pill\" data-status=\"{_esc(item.get('state', 'draft_offline'))}\">{_esc(item.get('state', 'draft_offline'))}</span></td></tr>"
        for item in title_candidates.get("primary_title_candidates", []) + title_candidates.get("short_text_candidates", [])
    )
    cards = "\n".join(_status_card(row) for row in rows)
    concept_cards = "\n".join(_concept_card(concept) for concept in concepts.get("concepts", []))
    boundary_rows = "\n".join(
        f"<tr><th>{_esc(key)}</th><td><span class=\"status-pill\" data-status=\"{_esc(_boundary_state(value))}\">{_esc(value)}</span></td></tr>"
        for key, value in summary["boundary_status"].items()
    )
    palette = "\n".join(
        f"<span class=\"status-pill\" data-status=\"{_esc(state)}\">{_esc(state)}</span>"
        for state in STATUS_CATEGORIES
    )
    constraints = visual_constraints.get("layout_constraints", {})
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Thumbnail Visual Proof Pack</title>
  <style>
    :root {{
      --bg: #f6f8fb;
      --surface: #ffffff;
      --ink: #111827;
      --muted: #64748b;
      --line: #d8e0e8;
      --ready: #0f766e;
      --draft: #8a6116;
      --sample: #a14f16;
      --input: #b42318;
      --gate: #7f1d1d;
      --deferred: #475569;
      --missing: #6b7280;
      --unknown: #4b5563;
      --accent: #f59e0b;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; min-height: 100%; background: var(--bg); color: var(--ink); font-family: "Segoe UI", "Noto Sans", Arial, sans-serif; }}
    body {{ padding: 24px; }}
    .shell {{ max-width: 1320px; margin: 0 auto; }}
    header {{ display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 16px; align-items: end; margin-bottom: 18px; }}
    h1 {{ margin: 0; font-size: 28px; line-height: 1.15; letter-spacing: 0; }}
    h2 {{ margin: 0 0 12px; font-size: 16px; line-height: 1.25; letter-spacing: 0; }}
    p {{ margin: 0; color: var(--muted); line-height: 1.5; }}
    code {{ font-family: Consolas, "SFMono-Regular", monospace; font-size: 12px; overflow-wrap: anywhere; }}
    .topline {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }}
    .layout {{ display: grid; grid-template-columns: minmax(0, 1.45fr) minmax(320px, 0.85fr); gap: 16px; }}
    .panel, .card {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; }}
    .panel {{ padding: 16px; margin-bottom: 16px; }}
    .proof-frame {{ width: 100%; aspect-ratio: 16 / 9; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #0f1f2e; }}
    .proof-frame img {{ display: block; width: 100%; height: 100%; object-fit: contain; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }}
    .status-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }}
    .card {{ padding: 12px; display: grid; gap: 8px; min-height: 132px; }}
    .card-head {{ display: flex; justify-content: space-between; gap: 8px; align-items: flex-start; }}
    .card-title {{ font-size: 14px; font-weight: 700; line-height: 1.25; }}
    .note {{ font-size: 12px; color: var(--muted); line-height: 1.4; }}
    .status-pill {{ display: inline-flex; align-items: center; min-height: 24px; padding: 3px 8px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid currentColor; background: #fff; }}
    [data-status="ready"] {{ color: var(--ready); }}
    [data-status="draft_offline"] {{ color: var(--draft); }}
    [data-status="sample_fixture_not_real"] {{ color: var(--sample); }}
    [data-status="blocked_by_real_input"] {{ color: var(--input); }}
    [data-status="blocked_by_true_gate"] {{ color: var(--gate); }}
    [data-status="deferred"] {{ color: var(--deferred); }}
    [data-status="missing"] {{ color: var(--missing); }}
    [data-status="partial"], [data-status="unknown"] {{ color: var(--unknown); }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ text-align: left; padding: 9px 8px; border-top: 1px solid var(--line); vertical-align: top; }}
    th {{ width: 190px; color: var(--muted); font-weight: 700; }}
    .next {{ border-left: 4px solid var(--accent); padding-left: 12px; }}
    @media (max-width: 980px) {{
      body {{ padding: 14px; }}
      header, .layout {{ grid-template-columns: 1fr; }}
      .status-grid, .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 640px) {{
      .status-grid, .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="shell" data-thumbnail-proof-pack="true">
    <header>
      <div>
        <h1>Thumbnail Visual Proof Pack</h1>
        <p>Static local/offline thumbnail direction for {_esc(summary.get("selected_candidate_id"))}.</p>
        <div class="topline">{palette}</div>
      </div>
      <span class="status-pill" data-status="ready">static proof ready</span>
    </header>

    <section class="layout">
      <div>
        <section class="panel" data-section="layout-proof">
          <h2>Static Layout Proof</h2>
          <div class="proof-frame"><img src="thumbnail_layout_proof.svg" alt="static abstract thumbnail layout proof"></div>
        </section>

        <section class="panel" data-section="visual-constraints">
          <h2>Concepts</h2>
          <div class="grid">{concept_cards}</div>
        </section>

        <section class="panel" data-section="source-artifact-index">
          <h2>Source Artifact Index</h2>
          <p>source_artifact_index: see <code>source_artifact_index.json</code>. All visual material in this proof is abstract SVG/CSS/text.</p>
        </section>
      </div>

      <aside>
        <section class="panel" data-section="title-candidates">
          <h2>Title / Text Candidates</h2>
          <table aria-label="title candidates"><tbody>{title_rows}</tbody></table>
        </section>

        <section class="panel" data-section="visual-constraints">
          <h2>Visual Constraints</h2>
          <table aria-label="visual constraints"><tbody>
            <tr><th>canvas</th><td>{_esc(constraints.get("canvas"))}</td></tr>
            <tr><th>safe_area</th><td>{_esc(constraints.get("safe_area_px"))} px</td></tr>
            <tr><th>motif</th><td>{_esc(constraints.get("visual_motif"))}</td></tr>
            <tr><th>rights</th><td>{_esc(visual_constraints.get("rights_boundaries", {}).get("source_rights_status"))}</td></tr>
          </tbody></table>
        </section>

        <section class="panel" data-section="boundary-status">
          <h2>Boundaries</h2>
          <table aria-label="boundary status"><tbody>{boundary_rows}</tbody></table>
        </section>

        <section class="panel" data-section="readiness-grid">
          <h2>Readiness Grid</h2>
          <div class="status-grid">{cards}</div>
        </section>

        <section class="panel next" data-section="next-action">
          <h2>Next Safe Local Action</h2>
          <p>{_esc(summary.get("next_safe_local_action"))}</p>
        </section>
      </aside>
    </section>
  </main>
</body>
</html>
"""


def _render_markdown_panel(
    summary: dict[str, Any],
    title_candidates: dict[str, Any],
    concepts: dict[str, Any],
    visual_constraints: dict[str, Any],
    rows: list[dict[str, Any]],
) -> str:
    lines = [
        "# Thumbnail Visual Proof Pack",
        "",
        f"- artifact_id: {summary['artifact_id']}",
        f"- selected_candidate_id: {summary.get('selected_candidate_id')}",
        f"- selected_title: {summary.get('selected_title')}",
        f"- primary_visual_proof: `thumbnail_layout_proof.svg`",
        f"- rights_status: {summary['boundary_status'].get('rights_status')}",
        f"- transcript_status: {summary['boundary_status'].get('transcript_status')}",
        "",
        "## Status Palette",
        "",
        ", ".join(STATUS_CATEGORIES),
        "",
        "## Title / Text Candidates",
        "",
    ]
    for item in title_candidates.get("primary_title_candidates", []):
        lines.append(f"- primary: {item.get('text')} ({item.get('state')})")
    for item in title_candidates.get("short_text_candidates", []):
        lines.append(f"- short: {item.get('text')} ({item.get('state')})")
    lines.extend(["", "## Concepts", ""])
    for concept in concepts.get("concepts", []):
        lines.append(f"- {concept.get('concept_id')}: {concept.get('state')} - {concept.get('short_text')}")
    lines.extend([
        "",
        "## Visual Constraints",
        "",
        f"- proof_status: {visual_constraints.get('proof_status')}",
        f"- visual_motif: {visual_constraints.get('layout_constraints', {}).get('visual_motif')}",
        f"- no_external_media: {str(visual_constraints.get('rights_boundaries', {}).get('no_external_media')).lower()}",
        "",
        "## Readiness Grid",
        "",
        "| capability | state | review_ready | path | note |",
        "|---|---|---:|---|---|",
    ])
    for row in rows:
        lines.append(
            f"| {row['capability_id']} | {row['state']} | {str(row['review_ready']).lower()} | "
            f"`{row['repo_relative_path']}` | {row['note']} |"
        )
    lines.extend(["", "## Boundary Status", "", "| boundary | status |", "|---|---|"])
    for key, value in summary["boundary_status"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Next Safe Local Action", "", summary["next_safe_local_action"], ""])
    return "\n".join(lines)


def _render_rights_boundaries(summary: dict[str, Any]) -> str:
    lines = [
        "# Forbidden Claims And Rights Boundaries",
        "",
        "This proof is local/offline and static. It uses only abstract shapes, text, and layout blocks.",
        "",
        "## Closed Gates",
        "",
    ]
    for gate in summary.get("closed_gates", []):
        lines.append(f"- {gate}")
    lines.extend([
        "",
        "## Forbidden Claims",
        "",
        "- Do not imply this is real broadcast analysis.",
        "- Do not use official logos, player photos, or broadcast stills.",
        "- Do not call the pitch sequence a proven strategy outside the sample.",
        "- Do not claim publication readiness or rights clearance.",
        "",
    ])
    return "\n".join(lines)


def _render_review_checklist(summary: dict[str, Any]) -> str:
    return "\n".join([
        "# Thumbnail Visual Proof Review Checklist",
        "",
        "- Open `thumbnail_proof_panel.html` or `thumbnail_layout_proof.svg` locally.",
        "- Confirm the numeric hook `155 -> 140 km/h` is readable at thumbnail scale.",
        "- Confirm the short text candidate is strong enough for a first review.",
        "- Confirm the proof uses only abstract shapes, text, cards, arrows, and labels.",
        "- Confirm no official logos, player photos, broadcast stills, external images, or downloaded media are present.",
        "- Confirm sample fixture, rights, YMM4, render, and publication gates remain closed.",
        "",
        "## Next Move",
        "",
        summary["next_safe_local_action"],
        "",
    ])


def _render_limitations(summary: dict[str, Any]) -> str:
    lines = [
        "# Thumbnail Visual Proof Limitations",
        "",
        "This package is a static composition and messaging proof. It is not a final thumbnail image.",
        "",
        "Not performed:",
        "",
    ]
    for gate in summary.get("closed_gates", []):
        lines.append(f"- {gate}")
    lines.extend([
        "- real transcript rerun",
        "- source, rights, legal, public-ready, or production acceptance",
        "",
        f"Current rights_status: `{summary['boundary_status'].get('rights_status')}`",
        f"Current transcript_status: `{summary['boundary_status'].get('transcript_status')}`",
        "",
    ])
    return "\n".join(lines)


def _status_card(row: dict[str, Any]) -> str:
    state = str(row.get("state", "unknown"))
    return (
        f'<article class="card" data-capability="{_esc(row.get("capability_id", "unknown"))}" data-status="{_esc(state)}">'
        '<div class="card-head">'
        f'<div class="card-title">{_esc(row.get("label", row.get("capability_id", "unknown")))}</div>'
        f'<span class="status-pill" data-status="{_esc(state)}">{_esc(state)}</span>'
        "</div>"
        f'<div class="note">{_esc(row.get("note", ""))}</div>'
        f'<code>{_esc(row.get("repo_relative_path", ""))}</code>'
        "</article>"
    )


def _concept_card(concept: dict[str, Any]) -> str:
    state = str(concept.get("state", "unknown"))
    points = "".join(f"<li>{_esc(item)}</li>" for item in concept.get("composition", [])[:4])
    return (
        f'<article class="card" data-concept="{_esc(concept.get("concept_id", "unknown"))}" data-status="{_esc(state)}">'
        '<div class="card-head">'
        f'<div class="card-title">{_esc(concept.get("concept_id", "unknown"))}</div>'
        f'<span class="status-pill" data-status="{_esc(state)}">{_esc(state)}</span>'
        "</div>"
        f'<div class="note">{_esc(concept.get("hook_rationale", ""))}</div>'
        f"<ul>{points}</ul>"
        "</article>"
    )


def _row(
    capability_id: str,
    label: str,
    state: str,
    path: Path,
    note: str,
    repo_root: Path,
    review_ready: bool,
) -> dict[str, Any]:
    return {
        "capability_id": capability_id,
        "label": label,
        "state": state if state in STATUS_CATEGORIES else "unknown",
        "review_ready": review_ready,
        "repo_relative_path": _relpath(path, repo_root),
        "exists": path.exists(),
        "note": note,
    }


def _required_visible_states() -> tuple[str, ...]:
    return (
        "ready",
        "partial",
        "sample_fixture_not_real",
        "draft_offline",
        "blocked_by_real_input",
        "blocked_by_true_gate",
        "deferred",
        "missing",
        "unknown",
    )


def _external_reference_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in EXTERNAL_MEDIA_PATTERNS:
        match = pattern.search(text)
        if match:
            hits.append(match.group(0))
    return hits


def _payload(snapshot: dict[str, Any], key: str) -> dict[str, Any]:
    payload = snapshot.get("payloads", {}).get(key)
    return payload if isinstance(payload, dict) else {}


def _load_json_if_present(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


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


def _boundary_state(value: Any) -> str:
    text = str(value)
    if text in STATUS_CATEGORIES:
        return text
    if "blocked" in text:
        return "blocked_by_true_gate"
    if "sample" in text:
        return "sample_fixture_not_real"
    if "draft" in text or "offline" in text:
        return "draft_offline"
    if "deferred" in text:
        return "deferred"
    if "missing" in text:
        return "missing"
    if "unknown" in text:
        return "unknown"
    return "ready"


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _svg(value: Any) -> str:
    return html.escape(str(value), quote=False)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
