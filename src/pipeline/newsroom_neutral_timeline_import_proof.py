"""Neutral timeline import proof for diagnostic newsroom artifacts.

This module turns the existing synthetic capsule, timing plan, caption copy,
and diagnostic transfer proof into a small import-shaped timeline. It does not
write YMM4 projects, create carriers, render output, generate TTS/audio, ingest
real packets, fetch sources, or approve production use.
"""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_caption_copy_refinement import DEFAULT_COPY_REFINEMENT_PATH
from src.pipeline.newsroom_caption_timing_plan import DEFAULT_PLAN_PATH
from src.pipeline.newsroom_diagnostic_transfer_candidate_proof import (
    DEFAULT_DIAGNOSTIC_TRANSFER_PROOF_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import (
    DEFAULT_CAPSULE_PATH,
    load_json_object,
)


NEUTRAL_TIMELINE_SCHEMA_VERSION = "newsroom_neutral_timeline_import_proof.v1"
NEUTRAL_TIMELINE_ID = "newsroom_neutral_timeline_import_proof_v1_2026_06_22"
DEFAULT_NEUTRAL_TIMELINE_PATH = Path(
    "samples/_probe/newsroom_handoff/neutral_timeline_import_proof_v1.json"
)
DEFAULT_CAPTION_IMPORT_CSV_PATH = Path(
    "samples/_probe/newsroom_handoff/caption_import_candidate_v1.csv"
)
DEFAULT_NEUTRAL_TIMELINE_DOC_PATH = Path(
    "docs/verification/NEWSROOM_NEUTRAL_TIMELINE_IMPORT_PROOF_V1_2026-06-22.md"
)

CAPTION_CSV_COLUMNS: tuple[str, ...] = (
    "caption_id",
    "beat_id",
    "start_sec",
    "end_sec",
    "duration_sec",
    "text",
    "diagnostic_only",
    "production_ready",
)


def build_default_newsroom_neutral_timeline_import_proof(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed neutral timeline import proof from default inputs."""
    base = Path(root) if root is not None else Path(".")
    capsule = load_json_object(base / DEFAULT_CAPSULE_PATH)
    timing_plan = load_json_object(base / DEFAULT_PLAN_PATH)
    caption_copy = load_json_object(base / DEFAULT_COPY_REFINEMENT_PATH)
    transfer_proof = load_json_object(base / DEFAULT_DIAGNOSTIC_TRANSFER_PROOF_PATH)
    return build_newsroom_neutral_timeline_import_proof(
        capsule,
        timing_plan,
        caption_copy,
        transfer_proof,
        capsule_path=DEFAULT_CAPSULE_PATH,
        timing_plan_path=DEFAULT_PLAN_PATH,
        caption_copy_path=DEFAULT_COPY_REFINEMENT_PATH,
        transfer_proof_path=DEFAULT_DIAGNOSTIC_TRANSFER_PROOF_PATH,
        caption_csv_path=DEFAULT_CAPTION_IMPORT_CSV_PATH,
    )


def build_newsroom_neutral_timeline_import_proof(
    capsule: dict[str, Any],
    timing_plan: dict[str, Any],
    caption_copy: dict[str, Any],
    transfer_proof: dict[str, Any],
    *,
    capsule_path: str | Path | None = None,
    timing_plan_path: str | Path | None = None,
    caption_copy_path: str | Path | None = None,
    transfer_proof_path: str | Path | None = None,
    caption_csv_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build a deterministic neutral timeline proof for synthetic import tests."""
    episode = _dict(capsule.get("episode"))
    timing_summary = _dict(timing_plan.get("episode_timing_summary"))
    transfer = _dict(transfer_proof.get("decision_split"))
    caption_items = _caption_items(caption_copy)
    visual_items = _visual_placeholder_items(timing_plan)
    marker_items = _marker_items(timing_plan)
    audio_item = _audio_placeholder_item(caption_copy, timing_summary)
    items = caption_items + visual_items + marker_items + [audio_item]

    return {
        "timeline_id": NEUTRAL_TIMELINE_ID,
        "artifact_id": NEUTRAL_TIMELINE_ID,
        "schema_version": NEUTRAL_TIMELINE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "identity": {
            "timeline_id": NEUTRAL_TIMELINE_ID,
            "source_episode_id": episode.get("episode_id"),
            "source_artifacts": _source_artifacts(
                capsule,
                timing_plan,
                caption_copy,
                transfer_proof,
                capsule_path=capsule_path,
                timing_plan_path=timing_plan_path,
                caption_copy_path=caption_copy_path,
                transfer_proof_path=transfer_proof_path,
            ),
            "production_status": "diagnostic_only",
            "import_status": "diagnostic_candidate_with_placeholders",
        },
        "source_episode_id": episode.get("episode_id"),
        "production_status": "diagnostic_only",
        "import_status": "diagnostic_candidate_with_placeholders",
        "review_memory": {
            "prior_user_review_count": 0,
            "accepted_scope": [
                "diagnostic_timing_panel_surface_by_validation",
                "diagnostic_caption_copy_refinement_by_validation",
                "diagnostic_transfer_candidate_classification",
            ],
            "not_accepted_scope": [
                "production subtitle design",
                "production narration",
                "TTS-ready script",
                "YMM4 transfer approval",
                ".ymmp",
                "render",
                "public video",
            ],
            "next_nonredundant_axis": [
                "neutral_timeline_import_proof",
                "import_field_schema",
                "placeholder_policy",
            ],
            "repeated_general_review_allowed": False,
        },
        "global_timing": {
            "total_duration_sec": timing_summary.get("total_duration_sec"),
            "timebase": "seconds",
            "fps_policy": {
                "fps": None,
                "placeholder": False,
                "policy": "not_required_for_neutral_timeline",
            },
            "timing_confidence": "provisional",
            "timing_source": "caption_timing_plan.episode_timing_summary",
        },
        "tracks": [
            _track("track_captions_main", "captions", "refined caption rows"),
            _track("track_visual_placeholders", "visuals", "no-media visual placeholders"),
            _track("track_markers", "markers", "beat boundary markers"),
            _track(
                "track_audio_placeholder",
                "audio_placeholder",
                "explicit no-audio placeholder",
            ),
        ],
        "items": items,
        "caption_csv": {
            "status": "created",
            "path": _path_text(caption_csv_path),
            "derived_from": "items where item_kind=caption",
            "columns": list(CAPTION_CSV_COLUMNS),
            "row_count": len(caption_items),
            "diagnostic_only": True,
            "production_ready": False,
        },
        "blocker_carry_forward": {
            "production_transfer_status": "blocked",
            "diagnostic_import_status": transfer.get(
                "diagnostic_import_status",
                "candidate_with_placeholders",
            ),
            "blocker_summary": _dict(transfer_proof.get("blocker_classification_summary")),
            "YMM4_candidate": False,
            "production_approval": False,
        },
        "placeholder_policy": {
            "visual_media_dependency": "none",
            "audio_media_dependency": "none",
            "real_source_dependency": "none",
            "caption_text_policy": "synthetic_refined_caption_copy_only",
            "visual_policy": "placeholder_metadata_only_no_media_file",
            "marker_policy": "diagnostic_beat_boundaries_only",
        },
        "next_mapping_policy": {
            "recommended_next_slice": "newsroom-caption-csv-import-candidate-v1",
            "allowed_next_artifacts": [
                "neutral timeline JSON",
                "caption CSV",
                "script-import candidate",
            ],
            "prohibited_next_artifacts": [
                "production .ymmp",
                "render output",
                "TTS output",
                "real media",
                "real packet ingest",
                "external fetch",
            ],
            "next_required_decision": (
                "Choose whether the caption CSV remains the next proof target or "
                "whether a script-import candidate should consume the neutral JSON."
            ),
        },
        "review_card": {
            "status": "none",
            "axis_if_needed": "neutral_timeline_import_schema",
            "reason": (
                "No user judgement is required because the slice creates the "
                "validated neutral timeline proof directly."
            ),
            "not_asking": (
                "No repeated timing, caption copy, or blocker classification review "
                "is requested."
            ),
        },
        "boundary_assertions": {
            "diagnostic_only": True,
            "neutral_timeline_json_is_source_of_truth": True,
            "caption_csv_derived_from_json": True,
            "opens_production_transfer": False,
            "opens_YMM4_transfer": False,
            "contains_real_news_claims": False,
            "contains_real_names": False,
            "contains_real_urls": False,
            "real_packet_ingested": False,
            "real_source_fetch_performed": False,
            "rss_inoreader_access_performed": False,
            "external_media_downloaded": False,
            "media_file_dependency": False,
            "tts_generated": False,
            "ymmp_generated": False,
            "ymm4_carrier_generated": False,
            "render_generated": False,
            "production_approval": False,
            "public_video": False,
            "dashboard_governance_freshness_changed": False,
        },
    }


def render_caption_import_candidate_csv(timeline: dict[str, Any]) -> str:
    """Render the optional caption CSV from caption items in the neutral timeline."""
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(CAPTION_CSV_COLUMNS)
    for item in _caption_timeline_items(timeline):
        writer.writerow([
            item.get("caption_id"),
            item.get("beat_id"),
            item.get("start_sec"),
            item.get("end_sec"),
            item.get("duration_sec"),
            item.get("text"),
            str(item.get("diagnostic_only")).lower(),
            str(item.get("production_ready")).lower(),
        ])
    return output.getvalue()


def render_newsroom_neutral_timeline_import_proof_markdown(
    timeline: dict[str, Any],
) -> str:
    """Render a human-readable readback for the neutral timeline proof."""
    identity = _dict(timeline.get("identity"))
    timing = _dict(timeline.get("global_timing"))
    caption_csv = _dict(timeline.get("caption_csv"))
    blockers = _dict(timeline.get("blocker_carry_forward"))
    boundary = _dict(timeline.get("boundary_assertions"))
    items = _list(timeline.get("items"))
    captions = [item for item in items if item.get("item_kind") == "caption"]
    visuals = [item for item in items if item.get("item_kind") == "visual_placeholder"]
    markers = [item for item in items if item.get("item_kind") == "marker"]
    audio = [item for item in items if item.get("item_kind") == "audio_placeholder"]

    lines = [
        "# Newsroom Neutral Timeline Import Proof v1",
        "",
        f"timeline_id: {timeline.get('timeline_id')}",
        f"schema_version: {timeline.get('schema_version')}",
        f"review_status: {timeline.get('review_status')}",
        f"source_episode_id: {identity.get('source_episode_id')}",
        f"production_status: {timeline.get('production_status')}",
        f"import_status: {timeline.get('import_status')}",
        "diagnostic_only: true",
        "",
        "## Purpose",
        "",
        "This artifact is the neutral, synthetic import-shaped timeline for the "
        "diagnostic newsroom episode. It is the source of truth for the optional "
        "caption CSV and keeps production/YMM4 transfer closed.",
        "",
        "## Timing",
        "",
        f"- total_duration_sec: {timing.get('total_duration_sec')}",
        f"- timebase: {timing.get('timebase')}",
        "- fps_policy: not_required_for_neutral_timeline",
        f"- timing_confidence: {timing.get('timing_confidence')}",
        "",
        "## Track Summary",
        "",
        "| track_id | track_kind | production_ready |",
        "|---|---|---|",
    ]
    for track in timeline.get("tracks", []):
        lines.append(
            f"| {track['track_id']} | {track['track_kind']} | "
            f"{str(track['production_ready']).lower()} |"
        )

    lines.extend([
        "",
        "## Item Summary",
        "",
        "| item_kind | count | diagnostic_import_allowed |",
        "|---|---:|---|",
        f"| caption | {len(captions)} | true |",
        f"| visual_placeholder | {len(visuals)} | true |",
        f"| marker | {len(markers)} | true |",
        f"| audio_placeholder | {len(audio)} | true |",
        "",
        "## Caption Items",
        "",
    ])
    for item in captions:
        lines.append(
            f"- {item['caption_id']}: {item['start_sec']}-{item['end_sec']}s "
            f"beat={item['beat_id']} density={item['reading_density']}"
        )
        lines.append(f"  text: {item['text']}")

    lines.extend(["", "## Visual Placeholder Items", ""])
    for item in visuals:
        lines.append(
            f"- {item['visual_id']}: {item['start_sec']}-{item['end_sec']}s "
            f"slot={item['g28_slot']} layout={item['layout_hint']}"
        )
        lines.append(f"  caption_interference_note: {item['caption_interference_note']}")
        lines.append("  media_file_dependency: none")

    lines.extend([
        "",
        "## Audio Placeholder",
        "",
    ])
    for item in audio:
        lines.append(
            f"- {item['item_id']}: voice_status={item['voice_status']}; "
            f"TTS_generated={str(item['TTS_generated']).lower()}; "
            "audio_required_for_this_proof=false"
        )

    lines.extend([
        "",
        "## Caption CSV",
        "",
        f"- status: {caption_csv.get('status')}",
        f"- path: {caption_csv.get('path')}",
        f"- derived_from: {caption_csv.get('derived_from')}",
        f"- row_count: {caption_csv.get('row_count')}",
        "",
        "## Blocker Carry-Forward",
        "",
        f"- production_transfer_status: {blockers.get('production_transfer_status')}",
        f"- diagnostic_import_status: {blockers.get('diagnostic_import_status')}",
        "- YMM4_candidate: false",
        "- production_approval: false",
        "",
        "## Next Mapping Policy",
        "",
        f"- recommended_next_slice: {timeline['next_mapping_policy']['recommended_next_slice']}",
        "- allowed_next_artifacts:",
    ])
    for artifact in timeline["next_mapping_policy"]["allowed_next_artifacts"]:
        lines.append(f"  - {artifact}")
    lines.append("- prohibited_next_artifacts:")
    for artifact in timeline["next_mapping_policy"]["prohibited_next_artifacts"]:
        lines.append(f"  - {artifact}")

    lines.extend([
        "",
        "## Review Card",
        "",
        "Review Card: none. This slice validates the neutral timeline import schema "
        "and does not ask for repeated timing, caption, copy, or blocker review.",
        "",
        "## Boundary",
        "",
        f"neutral_timeline_json_is_source_of_truth: {str(boundary.get('neutral_timeline_json_is_source_of_truth')).lower()}",
        f"caption_csv_derived_from_json: {str(boundary.get('caption_csv_derived_from_json')).lower()}",
        "",
        "This proof does not create `.ymmp`, YMM4 carriers, renders, TTS/audio, "
        "real packet ingestion, external fetches, real source access, media files, "
        "production approvals, rights approvals, public-use approvals, or publishing output.",
        "",
    ])
    return "\n".join(lines)


def _source_artifacts(
    capsule: dict[str, Any],
    timing_plan: dict[str, Any],
    caption_copy: dict[str, Any],
    transfer_proof: dict[str, Any],
    *,
    capsule_path: str | Path | None,
    timing_plan_path: str | Path | None,
    caption_copy_path: str | Path | None,
    transfer_proof_path: str | Path | None,
) -> dict[str, dict[str, Any]]:
    return {
        "episode_capsule": {
            "path": _path_text(capsule_path),
            "artifact_id": capsule.get("artifact_id"),
            "schema_version": capsule.get("schema_version"),
        },
        "caption_timing_plan": {
            "path": _path_text(timing_plan_path),
            "artifact_id": timing_plan.get("artifact_id"),
            "schema_version": timing_plan.get("schema_version"),
        },
        "caption_copy_refinement": {
            "path": _path_text(caption_copy_path),
            "artifact_id": caption_copy.get("artifact_id"),
            "schema_version": caption_copy.get("schema_version"),
        },
        "diagnostic_transfer_candidate_proof": {
            "path": _path_text(transfer_proof_path),
            "artifact_id": transfer_proof.get("artifact_id"),
            "schema_version": transfer_proof.get("schema_version"),
        },
    }


def _track(track_id: str, track_kind: str, note: str) -> dict[str, Any]:
    return {
        "track_id": track_id,
        "track_kind": track_kind,
        "diagnostic_only": True,
        "production_ready": False,
        "notes": [note],
    }


def _caption_items(caption_copy: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for unit in _list(caption_copy.get("refined_caption_units")):
        caption_id = str(unit.get("caption_id") or "")
        items.append({
            "item_id": f"item_caption_{caption_id}",
            "track_id": "track_captions_main",
            "item_kind": "caption",
            "caption_id": caption_id,
            "start_sec": unit.get("start_sec"),
            "end_sec": unit.get("end_sec"),
            "duration_sec": unit.get("duration_sec"),
            "source_ref": f"caption_copy.refined_caption_units.{caption_id}",
            "text": unit.get("refined_caption_text"),
            "beat_id": unit.get("beat_id"),
            "char_count": unit.get("char_count"),
            "reading_density": unit.get("reading_density"),
            "line_count_target": unit.get("line_count_target"),
            "max_chars_target": unit.get("max_chars_target"),
            "contains_real_names": False,
            "contains_real_claims": False,
            "contains_urls": False,
            "diagnostic_only": True,
            "production_ready": False,
            "blocked_for_production": True,
            "diagnostic_import_allowed": True,
            "notes": [
                "Synthetic refined caption copied from diagnostic caption copy.",
                "Timing is inherited unchanged from the caption/timing plan.",
            ],
        })
    return items


def _visual_placeholder_items(timing_plan: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for visual in _list(timing_plan.get("visual_timing")):
        visual_id = str(visual.get("visual_id") or "")
        start = int(visual.get("start_sec") or 0)
        end = int(visual.get("end_sec") or 0)
        items.append({
            "item_id": f"item_visual_placeholder_{visual_id}",
            "track_id": "track_visual_placeholders",
            "item_kind": "visual_placeholder",
            "visual_id": visual_id,
            "start_sec": start,
            "end_sec": end,
            "duration_sec": end - start,
            "source_ref": f"caption_timing_plan.visual_timing.{visual_id}",
            "placeholder_label": f"visual placeholder: {visual.get('layout_hint')}",
            "beat_id": visual.get("beat_id"),
            "g28_slot": visual.get("g28_slot"),
            "layout_hint": visual.get("layout_hint"),
            "caption_interference_note": visual.get("caption_interference_risk"),
            "media_file_dependency": "none",
            "media_required": False,
            "diagnostic_only": True,
            "production_ready": False,
            "blocked_for_production": True,
            "diagnostic_import_allowed": True,
            "notes": [
                "No media file, screenshot, footage, or external source is required.",
                "Geometry remains downstream/YMM4 blocked.",
            ],
        })
    return items


def _marker_items(timing_plan: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for beat in _list(timing_plan.get("beat_timing")):
        beat_id = str(beat.get("beat_id") or "")
        items.append({
            "item_id": f"item_marker_{beat_id}",
            "track_id": "track_markers",
            "item_kind": "marker",
            "start_sec": beat.get("start_sec"),
            "end_sec": beat.get("end_sec"),
            "duration_sec": beat.get("duration_sec"),
            "source_ref": f"caption_timing_plan.beat_timing.{beat_id}",
            "placeholder_label": f"beat marker: {beat_id}",
            "beat_id": beat_id,
            "diagnostic_only": True,
            "production_ready": False,
            "blocked_for_production": True,
            "diagnostic_import_allowed": True,
            "notes": [
                "Marker row preserves beat boundaries only.",
                "Marker row is not a rendered timeline object.",
            ],
        })
    return items


def _audio_placeholder_item(
    caption_copy: dict[str, Any],
    timing_summary: dict[str, Any],
) -> dict[str, Any]:
    audio = _dict(caption_copy.get("audio_readiness"))
    total = int(timing_summary.get("total_duration_sec") or 0)
    return {
        "item_id": "item_audio_placeholder_not_started",
        "track_id": "track_audio_placeholder",
        "item_kind": "audio_placeholder",
        "start_sec": 0,
        "end_sec": total,
        "duration_sec": total,
        "source_ref": "caption_copy.audio_readiness",
        "placeholder_label": "audio placeholder: no TTS generated",
        "beat_id": "all_beats",
        "voice_status": audio.get("voice_status") or "not_started",
        "TTS_generated": False,
        "audio_required_for_this_proof": False,
        "media_file_dependency": "none",
        "diagnostic_only": True,
        "production_ready": False,
        "blocked_for_production": True,
        "diagnostic_import_allowed": True,
        "notes": [
            "Audio is explicitly absent for this proof.",
            "The neutral timeline can be parsed without narration or waveform timing.",
        ],
    }


def _caption_timeline_items(timeline: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in _list(timeline.get("items"))
        if item.get("item_kind") == "caption"
    ]


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None
