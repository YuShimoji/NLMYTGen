"""Bridge content spine packages into draft episode/Writer IR inputs.

The bridge is deliberately local and offline. It converts a selected content
planning candidate into machine-readable episode inputs, a draft YMM4 CSV
preview, and readiness reports without fetching sources, launching YMM4, or
claiming production/public acceptance.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from src.pipeline.content_planning_spine import BLOCKED_PUBLIC_ACTIONS

IR_BRIDGE_VERSION = "0.1"
DEFAULT_BRIDGE_DIRNAME = "ir_bridge"

REQUIRED_BRIDGE_FILES = (
    "bridge_manifest.json",
    "episode_bridge.json",
    "writer_ir_candidate.json",
    "cue_packet_candidate.json",
    "cue_packet_candidate.md",
    "draft_yymm4.csv",
    "ymm4_csv_readiness.md",
    "source_content_spine_reference.json",
    "source_artifact_index.json",
    "review_checklist.md",
    "source_to_ir_mapping.md",
    "limitations.md",
    "validation_readback.json",
)

STANDARD_SOURCE_CONTENT_SPINE_FILES = (
    "MANIFEST.json",
    "topic_candidates.json",
    "channel_strategy_proposals.md",
    "episode_candidate_001.md",
    "thumbnail_brief_001.md",
    "dashboard_status.json",
    "dashboard_preview.md",
    "review_checklist.md",
    "limitations.md",
    "content_spine_readback.json",
)

OPTIONAL_SOURCE_CONTENT_SPINE_FILES = (
    "content_spine_dry_run_manifest.json",
    "source_seed_reference.json",
    "source_artifact_index.json",
    "validation_readback.json",
)

EXTERNAL_REFERENCE_PATTERNS = (
    re.compile(r"\b(src|href)\s*=\s*['\"]https?://", re.IGNORECASE),
    re.compile(r"url\(\s*['\"]?https?://", re.IGNORECASE),
    re.compile(r"\bhttps?://", re.IGNORECASE),
    re.compile(r"<image\b", re.IGNORECASE),
    re.compile(r"<img\b", re.IGNORECASE),
)

FORBIDDEN_COMPLETION_CLAIMS = (
    '"render_completion": true',
    '"production_ready": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"video_generation": true',
    '"thumbnail_image_generated": true',
    '"youtube_uploaded": true',
    '"external_media_download_required": true',
    '"media_download_required": true',
    '"oauth_required": true',
    '"payment_required": true',
    '"yymm4_gui_launched": true',
    '"yymm4_import_completed": true',
    '"yymm4_render_completed": true',
    '"public_upload_open": true',
)


def build_content_ir_bridge_package(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = "content_spine_ir_bridge_001",
) -> dict[str, Any]:
    """Build a bridge package from a content spine package."""
    source_root = Path(package_dir)
    bridge_dir = Path(output_dir) if output_dir else source_root / DEFAULT_BRIDGE_DIRNAME
    bridge_dir.mkdir(parents=True, exist_ok=True)

    source = _load_content_spine(source_root)
    selected = source["selected_candidate"]
    dialogue = _draft_dialogue(selected)
    sections = _draft_sections(selected, dialogue)

    episode_bridge = _episode_bridge_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        bridge_dir=bridge_dir,
        source=source,
        dialogue=dialogue,
        sections=sections,
    )
    writer_ir = _writer_ir_candidate_payload(episode_bridge, selected, dialogue, sections)
    cue_packet = _cue_packet_candidate_payload(episode_bridge, selected, dialogue, sections)
    manifest = _bridge_manifest_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        bridge_dir=bridge_dir,
        episode_bridge=episode_bridge,
    )
    source_reference = _source_content_spine_reference(
        artifact_id=artifact_id,
        source_root=source_root,
        bridge_dir=bridge_dir,
        source=source,
        episode_bridge=episode_bridge,
    )
    repo_root = _find_repo_root(source_root)

    _write_json(bridge_dir / "bridge_manifest.json", manifest)
    _write_json(bridge_dir / "episode_bridge.json", episode_bridge)
    _write_json(bridge_dir / "writer_ir_candidate.json", writer_ir)
    _write_json(bridge_dir / "cue_packet_candidate.json", cue_packet)
    _write_text(bridge_dir / "cue_packet_candidate.md", _render_cue_packet_markdown(cue_packet))
    _write_draft_csv(bridge_dir / "draft_yymm4.csv", dialogue)
    _write_text(bridge_dir / "ymm4_csv_readiness.md", _render_yymm4_csv_readiness(episode_bridge))
    _write_json(bridge_dir / "source_content_spine_reference.json", source_reference)
    _write_json(bridge_dir / "source_artifact_index.json", _source_artifact_index(source_root, bridge_dir, repo_root))
    _write_text(bridge_dir / "review_checklist.md", _render_review_checklist(episode_bridge, source_reference))
    _write_text(bridge_dir / "source_to_ir_mapping.md", _render_source_to_ir_mapping(episode_bridge))
    _write_text(bridge_dir / "limitations.md", _render_limitations())

    readback = validate_content_ir_bridge_package(bridge_dir, require_readback=False)
    _write_json(bridge_dir / "validation_readback.json", readback)
    _write_json(bridge_dir / "source_artifact_index.json", _source_artifact_index(source_root, bridge_dir, repo_root))
    final_readback = validate_content_ir_bridge_package(bridge_dir)
    _write_json(bridge_dir / "validation_readback.json", final_readback)
    return final_readback


def validate_content_ir_bridge_package(
    bridge_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate a generated content IR bridge package."""
    root = Path(bridge_dir)
    files = {name: root / name for name in REQUIRED_BRIDGE_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["bridge_manifest.json"])
    episode_bridge = _load_json_if_present(files["episode_bridge.json"])
    writer_ir = _load_json_if_present(files["writer_ir_candidate.json"])
    cue_packet = _load_json_if_present(files["cue_packet_candidate.json"])
    source_reference = _load_json_if_present(files["source_content_spine_reference.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])
    csv_rows = _load_csv_rows_if_present(files["draft_yymm4.csv"])

    if not isinstance(manifest, dict):
        failed_checks.append("bridge_manifest_json_invalid")
        manifest = {}
    if not isinstance(episode_bridge, dict):
        failed_checks.append("episode_bridge_json_invalid")
        episode_bridge = {}
    if not isinstance(writer_ir, dict):
        failed_checks.append("writer_ir_candidate_json_invalid")
        writer_ir = {}
    if not isinstance(cue_packet, dict):
        failed_checks.append("cue_packet_candidate_json_invalid")
        cue_packet = {}
    if not isinstance(source_reference, dict):
        failed_checks.append("source_content_spine_reference_json_invalid")
        source_reference = {}
    if not isinstance(source_index, dict):
        failed_checks.append("source_artifact_index_json_invalid")
        source_index = {}

    source_boundary = episode_bridge.get("source_boundary", {})
    boundary_status = episode_bridge.get("boundary_status", {})
    manifest_boundary_status = manifest.get("boundary_status", {})
    if not source_boundary.get("source_name"):
        failed_checks.append("source_boundary_missing")
    if source_reference.get("schema_version") != "content_ir_bridge_source_content_spine_reference.v1":
        failed_checks.append("source_content_spine_reference_schema_mismatch")
    if source_index.get("schema_version") != "content_ir_bridge_source_artifact_index.v1":
        failed_checks.append("source_artifact_index_schema_mismatch")
    if writer_ir.get("schema_version") != "content_spine_writer_ir_candidate.v1":
        failed_checks.append("writer_ir_schema_mismatch")
    if not writer_ir.get("utterances"):
        failed_checks.append("writer_ir_utterances_empty")
    if cue_packet.get("phase") != "content-spine-bridge-cue-candidate":
        failed_checks.append("cue_packet_phase_mismatch")
    if len(csv_rows) < 2:
        failed_checks.append("draft_csv_too_short")
    if csv_rows and [cell.strip().lower() for cell in csv_rows[0]] == ["speaker", "text"]:
        failed_checks.append("draft_csv_unexpected_header")

    blocked_actions = episode_bridge.get("blocked_public_actions", [])
    if blocked_actions != list(BLOCKED_PUBLIC_ACTIONS):
        failed_checks.append("blocked_public_actions_missing")

    readiness = episode_bridge.get("readiness", {})
    if readiness.get("writer_ir_candidate_status") != "draft_candidate_generated":
        failed_checks.append("writer_ir_readiness_missing")
    if readiness.get("ymm4_csv_status") != "draft_preview_generated_not_production":
        failed_checks.append("csv_readiness_missing")
    if readiness.get("production_status") != "blocked_until_transcript_timing_and_human_review":
        failed_checks.append("production_boundary_missing")

    source_counts = source_index.get("artifact_counts", {})
    if source_counts.get("source_required_present", 0) < 3:
        failed_checks.append("source_artifact_index_too_sparse")
    required_generated_count = len(REQUIRED_BRIDGE_FILES) if require_readback else len(REQUIRED_BRIDGE_FILES) - 1
    if source_counts.get("generated_present", 0) < required_generated_count:
        failed_checks.append("generated_artifact_index_too_sparse")

    generated_outputs = source_reference.get("generated_ir_csv_outputs", {})
    for key in ("episode_bridge", "writer_ir_candidate", "cue_packet_candidate", "draft_yymm4_csv"):
        if not generated_outputs.get(key):
            failed_checks.append(f"generated_ir_csv_output_missing:{key}")

    if source_reference.get("source_seed_reference_present") is True:
        if source_reference.get("manual_copy_of_original_pilot") is not False:
            failed_checks.append("manual_copy_boundary_missing")
        if not source_reference.get("seed_origin_fields"):
            failed_checks.append("seed_origin_fields_missing")
        if not source_reference.get("inherited_template_defaults"):
            failed_checks.append("inherited_template_defaults_missing")
        if not source_reference.get("dry_run_placeholders"):
            failed_checks.append("dry_run_placeholders_missing")
        real_inputs = source_reference.get("required_real_inputs", {})
        if not real_inputs:
            failed_checks.append("required_real_inputs_missing")
        for key, value in real_inputs.items():
            if isinstance(value, dict) and value.get("value") is not None:
                failed_checks.append(f"required_real_input_has_value:{key}")

    dry_run_boundary_required = (
        boundary_status.get("dry_run") is True
        or manifest_boundary_status.get("dry_run") is True
        or source_reference.get("source_seed_reference_present") is True
    )
    if dry_run_boundary_required:
        _check_bridge_boundary_flags(boundary_status, failed_checks, prefix="episode_")
        _check_bridge_boundary_flags(manifest_boundary_status, failed_checks, prefix="manifest_")
        _check_bridge_boundary_flags(source_reference.get("boundary_status", {}), failed_checks, prefix="source_reference_")

    combined_text = _combined_text(
        path
        for name, path in files.items()
        if require_readback or name != "validation_readback.json"
    )
    external_reference_hits = _external_reference_hits(combined_text)
    forbidden_hits = [claim for claim in FORBIDDEN_COMPLETION_CLAIMS if claim in combined_text]
    failed_checks.extend(f"external_reference:{hit}" for hit in external_reference_hits)
    failed_checks.extend(f"forbidden_completion_claim:{claim}" for claim in forbidden_hits)

    return {
        "schema_version": "content_ir_bridge_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "bridge_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "bridge_manifest_json_loads": bool(manifest),
            "episode_bridge_json_loads": bool(episode_bridge),
            "writer_ir_candidate_json_loads": bool(writer_ir),
            "cue_packet_candidate_json_loads": bool(cue_packet),
            "source_content_spine_reference_json_loads": bool(source_reference),
            "source_artifact_index_json_loads": bool(source_index),
            "draft_csv_has_rows": len(csv_rows) >= 2,
            "draft_csv_headerless": bool(csv_rows)
            and [cell.strip().lower() for cell in csv_rows[0]] != ["speaker", "text"],
            "source_boundary_preserved": bool(source_boundary.get("source_name")),
            "blocked_public_actions_preserved": blocked_actions == list(BLOCKED_PUBLIC_ACTIONS),
            "not_production_ready": readiness.get("production_status") == "blocked_until_transcript_timing_and_human_review",
            "source_artifact_index_present": source_counts.get("source_required_present", 0) >= 3,
            "generated_outputs_indexed": source_counts.get("generated_present", 0) >= required_generated_count,
            "source_origin_separated": (
                source_reference.get("source_seed_reference_present") is not True
                or (
                    bool(source_reference.get("seed_origin_fields"))
                    and bool(source_reference.get("inherited_template_defaults"))
                    and bool(source_reference.get("dry_run_placeholders"))
                    and bool(source_reference.get("required_real_inputs"))
                )
            ),
            "dry_run_boundaries_preserved": not dry_run_boundary_required
            or (
                boundary_status.get("dry_run") is True
                and boundary_status.get("sample_fixture_not_real") is True
                and boundary_status.get("no_real_transcript") is True
                and boundary_status.get("no_yymm4_import") is True
                and boundary_status.get("public_upload_closed") is True
                and boundary_status.get("yymm4_render_closed") is True
            ),
            "no_external_references": not external_reference_hits,
            "no_forbidden_completion_claims": not forbidden_hits,
        },
        "failed_checks": failed_checks,
        "selected_candidate_id": episode_bridge.get("selected_candidate_id"),
        "draft_csv_rows": len(csv_rows),
        "next_action": (
            "Review draft_yymm4.csv and writer_ir_candidate.json; if accepted, replace "
            "draft lines with a real transcript before validate-ir/apply-production work."
        ),
    }


def _load_content_spine(root: Path) -> dict[str, Any]:
    manifest = _load_json(root / "MANIFEST.json")
    topics = _load_json(root / "topic_candidates.json")
    dashboard = _load_json(root / "dashboard_status.json")
    content_spine_dry_run_manifest = _load_json_if_present(root / "content_spine_dry_run_manifest.json")
    source_seed_reference = _load_json_if_present(root / "source_seed_reference.json")
    source_artifact_index = _load_json_if_present(root / "source_artifact_index.json")
    validation_readback = _load_json_if_present(root / "validation_readback.json")

    selected_id = manifest.get("selected_candidate_id")
    candidates = topics.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError(f"topic_candidates.json must include candidates[]: {root}")
    selected = next((candidate for candidate in candidates if candidate.get("candidate_id") == selected_id), None)
    if selected is None:
        raise ValueError(f"selected candidate not found in topic_candidates.json: {selected_id}")

    return {
        "manifest": manifest,
        "topics": topics,
        "dashboard": dashboard,
        "content_spine_dry_run_manifest": content_spine_dry_run_manifest if isinstance(content_spine_dry_run_manifest, dict) else {},
        "source_seed_reference": source_seed_reference if isinstance(source_seed_reference, dict) else {},
        "source_artifact_index": source_artifact_index if isinstance(source_artifact_index, dict) else {},
        "validation_readback": validation_readback if isinstance(validation_readback, dict) else {},
        "selected_candidate": selected,
    }


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


def _load_csv_rows_if_present(path: Path) -> list[list[str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as file:
        return [row for row in csv.reader(file) if row]


def _draft_dialogue(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    profile = candidate["yukkuri_profile"]
    thumbnail = candidate["thumbnail_profile"]
    explainer = profile.get("explainer_role", "まりさ")
    listener = profile.get("listener_role", "れいむ")
    title = candidate.get("title", "")
    display_title = thumbnail.get("title_hook") or title
    hook = profile.get("hook", title)
    beats = profile.get("beat_outline", [])

    rows: list[dict[str, Any]] = [
        {
            "index": 1,
            "speaker": listener,
            "text": f"今日は「{display_title}」って、どういう話なの？",
            "purpose": "opening_question",
            "source": "thumbnail_profile.title_hook",
        },
        {
            "index": 2,
            "speaker": explainer,
            "text": hook,
            "purpose": "hook",
            "source": "yukkuri_profile.hook",
        },
    ]

    for beat_index, beat in enumerate(beats, start=1):
        rows.append({
            "index": len(rows) + 1,
            "speaker": explainer,
            "text": _draft_beat_text(beat_index, str(beat)),
            "purpose": "beat_explanation",
            "source": f"yukkuri_profile.beat_outline[{beat_index - 1}]",
        })
        if beat_index in {2, len(beats)}:
            rows.append({
                "index": len(rows) + 1,
                "speaker": listener,
                "text": "なるほど、そこを見れば話の筋が追いやすいんだね。",
                "purpose": "listener_checkpoint",
                "source": "bridge_generated_listener_checkpoint",
            })

    rows.append({
        "index": len(rows) + 1,
        "speaker": explainer,
        "text": "この段階ではローカル企画案なので、本番化には実ソース、台本、タイミング確認が必要だぜ。",
        "purpose": "production_boundary",
        "source": "bridge_boundary_note",
    })
    return rows


def _draft_beat_text(beat_index: int, beat: str) -> str:
    """Convert planning beats into draft yukkuri dialogue without claiming final script quality."""
    known_sports_beats = {
        "Establish inning, count, score, and empty bases.": "まず場面は、7回表、1アウト、カウントB2-S2、走者なしという状況から見るぜ。",
        "Compare the previous 155 km/h four-seam fastball with the current 140 km/h slider.": "直前の155km/hのフォーシームから、今回は140km/hのスライダーに変わっている。",
        "Explain the 15 km/h drop as the main tactical contrast.": "ここで大事なのは15km/hの球速差だ。打者のタイミングをずらす主役になる。",
        "Show the low-outer strike result as the viewer watch point.": "結果は外低めへのストライク。視聴者にはこのコースと変化を見てもらう。",
        "Hand off to CSV/Writer IR only after source and claim review.": "ただし本番化するなら、実ソースと主張確認を済ませてからCSVとWriter IRに進める。",
    }
    if beat in known_sports_beats:
        return known_sports_beats[beat]
    return f"ポイント{beat_index}は、{beat}"


def _draft_sections(candidate: dict[str, Any], dialogue: list[dict[str, Any]]) -> list[dict[str, Any]]:
    title = candidate.get("title", "")
    midpoint = max(3, len(dialogue) // 2)
    return [
        {
            "section_id": "S1",
            "topic": "Opening hook and topic promise",
            "start_index": 1,
            "end_index": min(2, len(dialogue)),
            "default_bg": "studio_blue",
            "default_face": "neutral",
            "bgm": "light_explainer",
            "arc_phase": "intro",
        },
        {
            "section_id": "S2",
            "topic": f"Main explanation: {title}",
            "start_index": 3,
            "end_index": midpoint,
            "default_bg": "diagram",
            "default_face": "serious",
            "bgm": "data_focus",
            "arc_phase": "develop",
        },
        {
            "section_id": "S3",
            "topic": "Viewer watch point and production boundary",
            "start_index": midpoint + 1,
            "end_index": len(dialogue),
            "default_bg": "dark_board",
            "default_face": "thinking",
            "bgm": "closing_light",
            "arc_phase": "closing",
        },
    ]


def _section_for_index(sections: list[dict[str, Any]], index: int) -> dict[str, Any]:
    for section in sections:
        if section["start_index"] <= index <= section["end_index"]:
            return section
    return sections[-1]


def _episode_bridge_payload(
    *,
    artifact_id: str,
    source_root: Path,
    bridge_dir: Path,
    source: dict[str, Any],
    dialogue: list[dict[str, Any]],
    sections: list[dict[str, Any]],
) -> dict[str, Any]:
    selected = source["selected_candidate"]
    profile = selected["yukkuri_profile"]
    thumbnail = selected["thumbnail_profile"]
    boundary = selected["source_boundary"]
    boundary_status = _bridge_boundary_status(source)
    source_seed_reference = source.get("source_seed_reference", {})
    return {
        "schema_version": "content_spine_episode_bridge.v1",
        "artifact_id": artifact_id,
        "source_package_dir": str(source_root),
        "bridge_dir": str(bridge_dir),
        "selected_candidate_id": selected["candidate_id"],
        "selected_title": selected.get("title", ""),
        "source_boundary": boundary,
        "source_origin": {
            "content_spine_artifact_id": source["manifest"].get("artifact_id"),
            "content_spine_source_manifest": source["manifest"].get("source_manifest"),
            "content_spine_package_status": source["manifest"].get("status"),
            "source_seed_reference_present": bool(source_seed_reference),
            "derived_from_seed_instantiation_artifact_id": source_seed_reference.get(
                "derived_from_seed_instantiation_artifact_id"
            ),
            "derived_from_episode_seed_id": source_seed_reference.get("derived_from_episode_seed_id"),
            "manual_copy_of_original_pilot": source_seed_reference.get("manual_copy_of_original_pilot"),
        },
        "boundary_status": boundary_status,
        "yukkuri": {
            "explainer_role": profile.get("explainer_role"),
            "listener_role": profile.get("listener_role"),
            "hook": profile.get("hook"),
            "why_it_matters": profile.get("why_it_matters"),
            "beat_outline": profile.get("beat_outline", []),
            "recommended_tone": profile.get("recommended_tone"),
            "glossary_terms": profile.get("glossary_terms", []),
            "likely_audience": profile.get("likely_audience"),
            "channel_fit": profile.get("channel_fit"),
        },
        "thumbnail": thumbnail,
        "draft_dialogue": dialogue,
        "sections": sections,
        "readiness": {
            "writer_ir_candidate_status": "draft_candidate_generated",
            "cue_packet_status": "draft_candidate_generated",
            "ymm4_csv_status": "draft_preview_generated_not_production",
            "row_range_status": "not_available_until_real_transcript",
            "audio_timing_status": "not_available_until_yymm4_import",
            "maps_status": "not_selected",
            "real_transcript_status": boundary_status.get("real_transcript_status"),
            "yymm4_import_status": boundary_status.get("yymm4_import_status"),
            "no_yymm4_import": boundary_status.get("no_yymm4_import"),
            "production_status": "blocked_until_transcript_timing_and_human_review",
        },
        "missing_for_production": [
            "real transcript or final script",
            "YMM4 CSV import and VoiceItem timing",
            "row_start/row_end annotation",
            "face/bg/slot/overlay/se/motion maps if the episode uses them",
            "human source/rights/publication review",
        ],
        "blocked_public_actions": list(BLOCKED_PUBLIC_ACTIONS),
    }


def _writer_ir_candidate_payload(
    episode_bridge: dict[str, Any],
    candidate: dict[str, Any],
    dialogue: list[dict[str, Any]],
    sections: list[dict[str, Any]],
) -> dict[str, Any]:
    utterances = []
    for row in dialogue:
        section = _section_for_index(sections, row["index"])
        utterances.append({
            "index": row["index"],
            "speaker": row["speaker"],
            "text": row["text"],
            "section_id": section["section_id"],
            "template": "intro" if section["arc_phase"] == "intro" else ("closing" if section["arc_phase"] == "closing" else "data"),
            "face": section["default_face"],
            "bg": section["default_bg"],
            "slot": "left" if row["speaker"] == episode_bridge["yukkuri"]["listener_role"] else "right",
            "bridge_source": row["source"],
        })

    return {
        "schema_version": "content_spine_writer_ir_candidate.v1",
        "production_ir_spec_reference": "docs/PRODUCTION_IR_SPEC.md",
        "compatibility_status": "draft_candidate_not_validate_ir_ready",
        "not_validate_ir_ready_reason": (
            "Content spine package has no final transcript timing, row_start/row_end, "
            "YMM4 base project, or production maps."
        ),
        "video_id": episode_bridge["selected_candidate_id"],
        "ir_version": "1.0-draft",
        "tone": candidate["yukkuri_profile"].get("recommended_tone", ""),
        "pattern_mix": "intro:data:closing = 1:2:1",
        "visual_arc": [
            {"phase": "intro", "primary_pattern": "A", "emotion_flow": "question -> hook"},
            {"phase": "develop", "primary_pattern": "B", "emotion_flow": "fact comparison -> understanding"},
            {"phase": "closing", "primary_pattern": "D", "emotion_flow": "watch point -> production boundary"},
        ],
        "recurring_motif": candidate["thumbnail_profile"].get("visual_motif", ""),
        "default_bgm": "light_explainer",
        "sections": sections,
        "utterances": utterances,
        "source_boundary": episode_bridge["source_boundary"],
        "boundary_status": episode_bridge["boundary_status"],
        "production_boundary": {
            "dry_run": episode_bridge["boundary_status"].get("dry_run"),
            "sample_fixture_not_real": episode_bridge["boundary_status"].get("sample_fixture_not_real"),
            "draft_yymm4_csv_only": True,
            "no_real_transcript": True,
            "no_yymm4_import": True,
            "no_ymmp_generation": True,
            "no_render": True,
            "no_publication": True,
        },
    }


def _cue_packet_candidate_payload(
    episode_bridge: dict[str, Any],
    candidate: dict[str, Any],
    dialogue: list[dict[str, Any]],
    sections: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "packet_version": "content-spine-cue-v1",
        "phase": "content-spine-bridge-cue-candidate",
        "source_name": episode_bridge["selected_candidate_id"],
        "objective": "Turn the content spine draft dialogue into a concise S-6 cue memo candidate.",
        "constraints": [
            "Do not fetch live sources.",
            "Do not rewrite this into a final script without human review.",
            "Do not edit YMM4 projects or .ymmp data.",
            "Do not generate images, audio, or video.",
            "Do not treat dry-run placeholders as real source, transcript, timing, rights, or publication inputs.",
        ],
        "response_preferences": {
            "target_section_count": len(sections),
            "background_density": "One primary background plus at most one supporting visual per section.",
            "sound_policy": "Omit sound cues unless they clearly help.",
            "operator_todos_max": 4,
            "keep_notes_concise": True,
        },
        "context": {
            "candidate_title": candidate.get("title", ""),
            "channel_angle": candidate.get("channel_angle", ""),
            "glossary_terms": candidate["yukkuri_profile"].get("glossary_terms", []),
            "sections": sections,
        },
        "transcript": [
            {
                "index": row["index"],
                "speaker": row["speaker"],
                "mapped_speaker": row["speaker"],
                "text": row["text"],
            }
            for row in dialogue
        ],
    }


def _bridge_manifest_payload(
    *,
    artifact_id: str,
    source_root: Path,
    bridge_dir: Path,
    episode_bridge: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "content_ir_bridge_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "content-spine-to-writer-ir-csv-bridge",
        "status": "generated",
        "source_package_dir": str(source_root),
        "bridge_dir": str(bridge_dir),
        "selected_candidate_id": episode_bridge["selected_candidate_id"],
        "files": {name: str(bridge_dir / name) for name in REQUIRED_BRIDGE_FILES},
        "readiness": episode_bridge["readiness"],
        "boundaries": {
            "local_offline_review_only": True,
            "dry_run": episode_bridge["boundary_status"].get("dry_run"),
            "sample_fixture_not_real": episode_bridge["boundary_status"].get("sample_fixture_not_real"),
            "draft_csv_only": True,
            "no_real_transcript": True,
            "no_live_fetch": True,
            "no_media_download": True,
            "no_youtube_publication": True,
            "no_oauth_or_paid_api": True,
            "no_rights_or_legal_acceptance": True,
            "no_yymm4_import": True,
            "no_ymm4_gui_launch_or_render": True,
            "no_production_ymmp_generation": True,
            "public_upload_closed": True,
            "yymm4_render_closed": True,
        },
        "boundary_status": episode_bridge["boundary_status"],
    }


def _source_content_spine_reference(
    *,
    artifact_id: str,
    source_root: Path,
    bridge_dir: Path,
    source: dict[str, Any],
    episode_bridge: dict[str, Any],
) -> dict[str, Any]:
    source_seed_reference = source.get("source_seed_reference", {})
    content_spine_manifest = source["manifest"]
    content_spine_dry_run_manifest = source.get("content_spine_dry_run_manifest", {})
    selected = source["selected_candidate"]
    return {
        "schema_version": "content_ir_bridge_source_content_spine_reference.v1",
        "artifact_id": artifact_id,
        "source_content_spine_package_dir": str(source_root),
        "bridge_output_dir": str(bridge_dir),
        "content_spine_artifact_id": content_spine_manifest.get("artifact_id"),
        "content_spine_status": content_spine_manifest.get("status"),
        "content_spine_source_manifest": content_spine_manifest.get("source_manifest"),
        "content_spine_dry_run_manifest_present": bool(content_spine_dry_run_manifest),
        "source_seed_reference_present": bool(source_seed_reference),
        "selected_candidate_id": selected.get("candidate_id"),
        "selected_title": selected.get("title"),
        "source_boundary": selected.get("source_boundary", {}),
        "seed_origin_fields": {
            "source_seed_package_dir": source_seed_reference.get("source_seed_package_dir"),
            "derived_from_seed_instantiation_artifact_id": source_seed_reference.get(
                "derived_from_seed_instantiation_artifact_id"
            ),
            "derived_from_episode_seed_id": source_seed_reference.get("derived_from_episode_seed_id"),
            "derived_from_registry_artifact_id": source_seed_reference.get("derived_from_registry_artifact_id"),
            "content_spine_source_file": source_seed_reference.get("content_spine_source_file"),
        },
        "manual_copy_of_original_pilot": source_seed_reference.get("manual_copy_of_original_pilot"),
        "inherited_template_defaults": source_seed_reference.get("inherited_template_defaults", {}),
        "dry_run_placeholders": source_seed_reference.get("dry_run_placeholders", {}),
        "required_real_inputs": source_seed_reference.get("required_real_inputs", {}),
        "generated_content_spine_outputs": source_seed_reference.get("generated_content_spine_outputs", {}),
        "generated_ir_csv_outputs": {
            "bridge_manifest": str(bridge_dir / "bridge_manifest.json"),
            "episode_bridge": str(bridge_dir / "episode_bridge.json"),
            "writer_ir_candidate": str(bridge_dir / "writer_ir_candidate.json"),
            "cue_packet_candidate": str(bridge_dir / "cue_packet_candidate.json"),
            "cue_packet_readable": str(bridge_dir / "cue_packet_candidate.md"),
            "draft_yymm4_csv": str(bridge_dir / "draft_yymm4.csv"),
            "yymm4_csv_readiness": str(bridge_dir / "ymm4_csv_readiness.md"),
            "source_to_ir_mapping": str(bridge_dir / "source_to_ir_mapping.md"),
            "source_artifact_index": str(bridge_dir / "source_artifact_index.json"),
            "review_checklist": str(bridge_dir / "review_checklist.md"),
            "limitations": str(bridge_dir / "limitations.md"),
            "validation_readback": str(bridge_dir / "validation_readback.json"),
        },
        "csv_contract": {
            "header_mode": source_seed_reference.get("inherited_template_defaults", {}).get(
                "csv_header_mode", "headerless_yymm4_csv"
            ),
            "columns": ["speaker", "text"],
            "status": "draft_preview_only_no_yymm4_import",
        },
        "boundary_status": episode_bridge["boundary_status"],
    }


def _source_artifact_index(source_root: Path, bridge_dir: Path, repo_root: Path) -> dict[str, Any]:
    source_inputs = []
    for name in (*STANDARD_SOURCE_CONTENT_SPINE_FILES, *OPTIONAL_SOURCE_CONTENT_SPINE_FILES):
        path = source_root / name
        payload = _load_json_if_present(path) if name.endswith(".json") else None
        required = name in STANDARD_SOURCE_CONTENT_SPINE_FILES
        source_inputs.append({
            "id": name,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "required_for_standard_content_spine": required,
            "state": "ready" if path.exists() else ("missing" if required else "optional_missing"),
            "schema_version": payload.get("schema_version") if isinstance(payload, dict) else None,
        })

    generated_outputs = []
    for name in REQUIRED_BRIDGE_FILES:
        path = bridge_dir / name
        generated_outputs.append({
            "id": name,
            "repo_relative_path": _relpath(path, repo_root),
            "exists": path.exists(),
            "state": "ready" if path.exists() else "missing",
        })

    return {
        "schema_version": "content_ir_bridge_source_artifact_index.v1",
        "source_content_spine_package_dir": str(source_root),
        "bridge_output_dir": str(bridge_dir),
        "source_inputs": source_inputs,
        "generated_outputs": generated_outputs,
        "artifact_counts": {
            "source_total": len(source_inputs),
            "source_present": sum(1 for item in source_inputs if item["exists"]),
            "source_required_total": len(STANDARD_SOURCE_CONTENT_SPINE_FILES),
            "source_required_present": sum(
                1
                for item in source_inputs
                if item["required_for_standard_content_spine"] and item["exists"]
            ),
            "generated_total": len(generated_outputs),
            "generated_present": sum(1 for item in generated_outputs if item["exists"]),
        },
    }


def _bridge_boundary_status(source: dict[str, Any]) -> dict[str, Any]:
    selected_boundary = source["selected_candidate"].get("source_boundary", {})
    seed_boundary = source.get("source_seed_reference", {}).get("boundary_status", {})
    dry_run_boundary = source.get("content_spine_dry_run_manifest", {}).get("boundary_status", {})
    inherited = {**seed_boundary, **dry_run_boundary}
    dry_run = inherited.get("dry_run") is True
    sample_fixture = (
        inherited.get("sample_fixture_not_real") is True
        or selected_boundary.get("freshness_status") == "offline_fixture_not_live"
        or selected_boundary.get("production_status") == "dry_run_only_not_production"
    )
    rights_boundary = inherited.get("rights_boundary") or selected_boundary.get("rights_status")
    yymm4_import_status = inherited.get("yymm4_import_status") or "not_run"
    return {
        **inherited,
        "dry_run": dry_run,
        "sample_fixture_not_real": sample_fixture,
        "rights_boundary": rights_boundary,
        "public_upload_closed": True,
        "yymm4_render_closed": True,
        "no_real_transcript": True,
        "no_yymm4_import": True,
        "ir_csv_bridge_status": "draft_generated_local_offline",
        "writer_ir_status": "draft_candidate_not_validate_ir_ready",
        "draft_csv_status": "draft_preview_only_no_yymm4_import",
        "real_transcript_status": inherited.get("real_transcript_status") or "not_run_required_before_production",
        "public_upload_status": "public_upload_closed",
        "yymm4_render_status": "yymm4_render_closed",
        "yymm4_import_status": yymm4_import_status,
        "external_network_status": "closed",
        "oauth_status": "closed",
        "payment_status": "closed",
        "production_status": "blocked_by_true_gate",
    }


def _write_draft_csv(path: Path, dialogue: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        for row in dialogue:
            writer.writerow([row["speaker"], row["text"]])


def _render_cue_packet_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Cue Packet Candidate",
        "",
        f"- phase: {payload['phase']}",
        f"- source_name: {payload['source_name']}",
        "",
        "## Objective",
        payload["objective"],
        "",
        "## Constraints",
    ]
    for item in payload["constraints"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Transcript"])
    for item in payload["transcript"]:
        lines.append(f"{item['index']}. [{item['mapped_speaker']}] {item['text']}")
    lines.append("")
    return "\n".join(lines)


def _render_yymm4_csv_readiness(episode_bridge: dict[str, Any]) -> str:
    lines = [
        "# YMM4 CSV Readiness",
        "",
        f"- selected_candidate_id: {episode_bridge['selected_candidate_id']}",
        "- generated: `draft_yymm4.csv`",
        "- status: draft_preview_generated_not_production",
        "",
        "## Ready Now",
        "",
        "- Speaker names are mapped to the yukkuri roles from the content spine package.",
        "- Draft dialogue rows are available for review and can be opened as a CSV preview.",
        "- Source boundary and excluded claims are preserved in `episode_bridge.json`.",
        "",
        "## Missing Before Production",
        "",
    ]
    for item in episode_bridge["missing_for_production"]:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "## Boundary",
        "",
        "This CSV is not a NotebookLM transcript, not YMM4-import proof, and not production-ready timing.",
        "",
    ])
    return "\n".join(lines)


def _render_source_to_ir_mapping(episode_bridge: dict[str, Any]) -> str:
    lines = [
        "# Source To IR Mapping",
        "",
        "| Source field | Bridge / IR field | Status |",
        "|---|---|---|",
        "| topic_candidates.selected.candidate_id | episode_bridge.selected_candidate_id / writer_ir.video_id | mapped |",
        "| source_boundary | episode_bridge.source_boundary / writer_ir.source_boundary | preserved |",
        "| content_spine_dry_run_manifest.boundary_status | episode_bridge.boundary_status / bridge_manifest.boundary_status | preserved when present |",
        "| source_seed_reference.seed_origin_fields | source_content_spine_reference.seed_origin_fields | preserved when present |",
        "| source_seed_reference.inherited_template_defaults | source_content_spine_reference.inherited_template_defaults | separated when present |",
        "| source_seed_reference.dry_run_placeholders | source_content_spine_reference.dry_run_placeholders | separated when present |",
        "| source_seed_reference.required_real_inputs | source_content_spine_reference.required_real_inputs | separated and expected null before production |",
        "| yukkuri_profile.explainer_role/listener_role | draft_dialogue.speaker / writer_ir.utterances.speaker | mapped |",
        "| yukkuri_profile.hook | draft_dialogue row 2 / writer_ir utterance 2 | mapped |",
        "| yukkuri_profile.beat_outline | draft_dialogue beat rows / writer_ir utterances | mapped as draft dialogue |",
        "| thumbnail_profile.visual_motif | writer_ir.recurring_motif | mapped as planning cue |",
        "| generated bridge outputs | source_content_spine_reference.generated_ir_csv_outputs / source_artifact_index.generated_outputs | indexed |",
        "| final transcript timing | row_start/row_end | pending |",
        "| YMM4 base project | apply-production input | pending |",
        "",
    ]
    return "\n".join(lines)


def _render_review_checklist(
    episode_bridge: dict[str, Any],
    source_reference: dict[str, Any],
) -> str:
    lines = [
        "# IR Bridge Review Checklist",
        "",
        f"- selected_candidate_id: {episode_bridge['selected_candidate_id']}",
        f"- source_seed_reference_present: {source_reference['source_seed_reference_present']}",
        "- status: dry-run/local review package only",
        "",
        "## Required Checks",
        "",
        "- Confirm `source_content_spine_reference.json` separates seed origin, inherited defaults, dry-run placeholders, required real inputs, and generated IR/CSV outputs.",
        "- Confirm `required_real_inputs` are still null before any real transcript, YMM4 import, rights, render, or publication work.",
        "- Confirm `draft_yymm4.csv` is a headerless two-column draft preview only.",
        "- Confirm `episode_bridge.json`, `writer_ir_candidate.json`, and `cue_packet_candidate.json` all preserve the source boundary.",
        "- Confirm `source_artifact_index.json` lists source content-spine inputs and generated bridge outputs.",
        "",
        "## Closed Gates",
        "",
        "- no real transcript",
        "- no YMM4 GUI/import/render",
        "- no production `.ymmp` generation",
        "- no external media/live fetch/OAuth/payment",
        "- no rights/legal/public-ready acceptance",
        "- no public upload",
        "",
    ]
    return "\n".join(lines)


def _render_limitations() -> str:
    lines = [
        "# Bridge Limitations",
        "",
        "This bridge turns a content spine package into draft production inputs. It is not final video generation.",
        "",
        "Not performed:",
        "",
    ]
    for item in BLOCKED_PUBLIC_ACTIONS:
        lines.append(f"- {item}")
    lines.extend([
        "- production .ymmp generation",
        "- validate-ir/apply-production against a real YMM4 project",
        "- final transcript/timing acceptance",
        "- treating seed-origin or dry-run placeholder fields as real source inputs",
        "- YMM4 CSV import or VoiceItem timing readback",
        "",
    ])
    return "\n".join(lines)


def _check_bridge_boundary_flags(boundary_status: dict[str, Any], failed_checks: list[str], *, prefix: str = "") -> None:
    if boundary_status.get("dry_run") is not True:
        failed_checks.append(f"{prefix}dry_run_not_marked")
    if boundary_status.get("sample_fixture_not_real") is not True:
        failed_checks.append(f"{prefix}sample_fixture_not_real_not_marked")
    if boundary_status.get("no_real_transcript") is not True:
        failed_checks.append(f"{prefix}no_real_transcript_not_marked")
    if boundary_status.get("no_yymm4_import") is not True:
        failed_checks.append(f"{prefix}no_yymm4_import_not_marked")
    if boundary_status.get("rights_boundary") != "sample_only_no_publication":
        failed_checks.append(f"{prefix}rights_boundary_not_preserved")
    if boundary_status.get("public_upload_closed") is not True:
        failed_checks.append(f"{prefix}public_upload_closed_not_marked")
    if boundary_status.get("yymm4_render_closed") is not True:
        failed_checks.append(f"{prefix}yymm4_render_closed_not_marked")
    if boundary_status.get("public_upload_status") != "public_upload_closed":
        failed_checks.append(f"{prefix}public_upload_status_not_closed")
    if boundary_status.get("yymm4_render_status") != "yymm4_render_closed":
        failed_checks.append(f"{prefix}yymm4_render_status_not_closed")
    if boundary_status.get("production_status") != "blocked_by_true_gate":
        failed_checks.append(f"{prefix}production_status_not_blocked")


def _combined_text(paths: Any) -> str:
    chunks = []
    for path in paths:
        if Path(path).is_file():
            chunks.append(Path(path).read_text(encoding="utf-8"))
    return "\n".join(chunks)


def _external_reference_hits(text: str) -> list[str]:
    hits = []
    for pattern in EXTERNAL_REFERENCE_PATTERNS:
        match = pattern.search(text)
        if match:
            hits.append(match.group(0))
    return hits


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


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")
