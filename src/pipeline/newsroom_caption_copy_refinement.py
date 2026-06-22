"""Diagnostic caption copy refinement for newsroom timing plans.

This module consumes the existing diagnostic caption/timing plan and produces a
copy-readability layer. It does not change timing, fetch sources, generate TTS,
write YMM4 projects, render output, or approve production use.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_caption_timing_plan import DEFAULT_PLAN_PATH
from src.pipeline.newsroom_episode_production_capsule import load_json_object


COPY_REFINEMENT_SCHEMA_VERSION = "newsroom_caption_copy_refinement.v1"
COPY_REFINEMENT_ARTIFACT_ID = "newsroom_caption_copy_refinement_v1_2026_06_22"
DEFAULT_COPY_REFINEMENT_PATH = Path(
    "samples/_probe/newsroom_handoff/episode_caption_copy_refinement_v1.json"
)
DEFAULT_COPY_REFINEMENT_DOC_PATH = Path(
    "docs/verification/NEWSROOM_CAPTION_COPY_REFINEMENT_V1_2026-06-22.md"
)

REFINED_CAPTION_TEXT: dict[str, str] = {
    "cap_beat_fake_intro_001_01": "Fake topic, review only.",
    "cap_beat_fake_intro_001_02": "Review-only handoff stays.",
    "cap_beat_fake_claim_001_01": "A fake claim is shown.",
    "cap_beat_fake_claim_001_02": "Fake source checks are noted.",
}


def build_default_newsroom_caption_copy_refinement(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed caption copy refinement from the default plan."""
    base = Path(root) if root is not None else Path(".")
    plan = load_json_object(base / DEFAULT_PLAN_PATH)
    return build_newsroom_caption_copy_refinement(plan, plan_path=DEFAULT_PLAN_PATH)


def build_newsroom_caption_copy_refinement(
    plan: dict[str, Any],
    *,
    plan_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build a deterministic, diagnostic caption copy refinement artifact."""
    units = [_refined_unit(plan, unit) for unit in _list(plan.get("caption_units"))]
    transfer = _dict(plan.get("transfer_status"))
    audio = _dict(plan.get("audio_readiness"))
    summary = _dict(plan.get("episode_timing_summary"))
    source = _dict(plan.get("source"))
    return {
        "artifact_id": COPY_REFINEMENT_ARTIFACT_ID,
        "schema_version": COPY_REFINEMENT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "review_axis": "caption_copy_readability",
        "diagnostic_only": True,
        "production_status": "diagnostic_caption_copy_only",
        "source": {
            "caption_timing_plan_path": _path_text(plan_path),
            "caption_timing_plan_artifact_id": plan.get("artifact_id"),
            "caption_timing_plan_schema_version": plan.get("schema_version"),
            "episode_id": source.get("episode_id"),
        },
        "review_memory": {
            "prior_user_review_count": 0,
            "accepted_scope": "diagnostic_timing_panel_surface_by_validation",
            "not_accepted_scope": [
                "production subtitle design",
                "production narration",
                "YMM4 transfer",
                "render",
                "public video",
            ],
            "next_nonredundant_axis": "caption_copy_readability",
            "repeated_general_timing_review_allowed": False,
        },
        "caption_copy_summary": {
            "total_duration_sec": summary.get("total_duration_sec"),
            "beat_count": summary.get("beat_count"),
            "caption_unit_count": len(units),
            "visual_count": summary.get("visual_count"),
            "timing_changed": False,
            "copy_status": "refined_diagnostic_placeholders",
            "max_chars_target": 34,
            "line_count_target": 2,
            "density_band_counts": _density_band_counts(units),
            "notes": [
                "Copy is synthetic and generic.",
                "Copy is not final narration and is not TTS-ready.",
                "Timing values are inherited unchanged from the caption/timing plan.",
            ],
        },
        "refined_caption_units": units,
        "audio_readiness": {
            "voice_status": audio.get("voice_status") or "not_started",
            "TTS_generated": False,
            "copy_tts_status": "not_TTS_ready",
        },
        "transfer_status": {
            "transfer_status": "blocked",
            "YMM4_candidate": False,
            "blocker_count": transfer.get("blocker_count"),
            "unlock_requirement_count": transfer.get("unlock_requirement_count"),
        },
        "next_allowed_steps": [
            "supervisor caption readability review",
            "Review Console refined-copy display only if requested",
            "YMM4 transfer candidate proof only after blockers are resolved",
        ],
        "prohibited_next_actions": [
            ".ymmp generation",
            "YMM4 carrier generation",
            "render generation",
            "TTS generation",
            "production approval",
            "real source fetch",
            "real URL access",
            "media download",
            "external fetch",
            "publishing",
        ],
        "review_card": {
            "status": "none",
            "reason": "No user judgement is required to create the diagnostic copy artifact.",
            "not_asking": "No repeated general timing panel review is requested.",
        },
        "boundary_assertions": {
            "diagnostic_only": True,
            "timing_changed": False,
            "contains_real_news_claims": False,
            "contains_real_names": False,
            "contains_real_urls": False,
            "real_source_fetch_performed": False,
            "external_media_downloaded": False,
            "tts_generated": False,
            "ymmp_generated": False,
            "ymm4_carrier_generated": False,
            "render_generated": False,
            "production_approval": False,
            "public_video": False,
        },
    }


def render_newsroom_caption_copy_refinement_markdown(refinement: dict[str, Any]) -> str:
    """Render a human-readable readback for the caption copy refinement."""
    summary = _dict(refinement.get("caption_copy_summary"))
    audio = _dict(refinement.get("audio_readiness"))
    transfer = _dict(refinement.get("transfer_status"))
    review_memory = _dict(refinement.get("review_memory"))
    lines = [
        "# Newsroom Caption Copy Refinement v1",
        "",
        f"artifact_id: {refinement.get('artifact_id')}",
        f"schema_version: {refinement.get('schema_version')}",
        f"review_status: {refinement.get('review_status')}",
        f"review_axis: {refinement.get('review_axis')}",
        f"production_status: {refinement.get('production_status')}",
        "diagnostic_only: true",
        "",
        "## Purpose",
        "",
        "This artifact refines the four diagnostic caption placeholders into short, "
        "synthetic caption copy. It preserves timing and keeps transfer blocked.",
        "",
        "## Review Memory",
        "",
        f"- prior_user_review_count: {review_memory.get('prior_user_review_count')}",
        f"- accepted_scope: {review_memory.get('accepted_scope')}",
        f"- next_nonredundant_axis: {review_memory.get('next_nonredundant_axis')}",
        "- repeated_general_timing_review_allowed: false",
        "",
        "## Caption Copy Summary",
        "",
        f"- total_duration_sec: {summary.get('total_duration_sec')}",
        f"- beat_count: {summary.get('beat_count')}",
        f"- caption_unit_count: {summary.get('caption_unit_count')}",
        f"- visual_count: {summary.get('visual_count')}",
        f"- timing_changed: {str(summary.get('timing_changed')).lower()}",
        f"- copy_status: {summary.get('copy_status')}",
        "",
        "## Video Readiness Matrix",
        "",
        "| area | status | note |",
        "|---|---|---|",
        "| timing | unchanged | inherits the existing 68 second plan |",
        "| caption copy | refined_diagnostic_placeholders | readable but not final narration |",
        f"| audio | {audio.get('voice_status')} | TTS_generated=false |",
        f"| transfer | {transfer.get('transfer_status')} | YMM4_candidate=false |",
        "",
        "## Refined Caption Units",
        "",
    ]
    for unit in refinement.get("refined_caption_units", []):
        lines.append(
            f"- {unit['caption_id']}: {unit['start_sec']}-{unit['end_sec']}s "
            f"beat={unit['beat_id']} chars={unit['char_count']} "
            f"density={unit['reading_density']}"
        )
        lines.append(f"  original: {unit['original_placeholder']}")
        lines.append(f"  refined: {unit['refined_caption_text']}")
        lines.append(f"  readability: {unit['readability_note']}")
        lines.append(f"  beat alignment: {unit['beat_alignment_note']}")
        lines.append(f"  visual interference: {unit['visual_interference_note']}")

    lines.extend([
        "",
        "## Review Card",
        "",
        "Review Card: none. This slice does not ask for a repeated general timing "
        "panel review; the next useful human axis is caption copy readability.",
        "",
        "## Transfer And Boundary",
        "",
        f"transfer_status: {transfer.get('transfer_status')}",
        f"YMM4_candidate: {str(transfer.get('YMM4_candidate')).lower()}",
        f"TTS_generated: {str(audio.get('TTS_generated')).lower()}",
        "",
        "Prohibited next actions:",
    ])
    for action in refinement.get("prohibited_next_actions", []):
        lines.append(f"- {action}")

    lines.extend(["", "Next allowed steps:"])
    for step in refinement.get("next_allowed_steps", []):
        lines.append(f"- {step}")

    lines.extend([
        "",
        "## Boundary",
        "",
        "This readback is diagnostic-only. It is not final narration, not TTS-ready, "
        "not a public video, not an importable proof, and not production approval.",
        "",
    ])
    return "\n".join(lines)


def _refined_unit(plan: dict[str, Any], unit: dict[str, Any]) -> dict[str, Any]:
    caption_id = str(unit.get("caption_id") or "")
    refined_text = REFINED_CAPTION_TEXT.get(caption_id, str(unit.get("text_placeholder") or ""))
    duration = int(unit.get("end_sec") or 0) - int(unit.get("start_sec") or 0)
    char_count = len(refined_text)
    visual_note = _visual_interference_note(plan, str(unit.get("beat_id") or ""))
    return {
        "caption_id": caption_id,
        "beat_id": unit.get("beat_id"),
        "original_placeholder": unit.get("text_placeholder"),
        "refined_caption_text": refined_text,
        "start_sec": unit.get("start_sec"),
        "end_sec": unit.get("end_sec"),
        "duration_sec": duration,
        "char_count": char_count,
        "line_count_target": unit.get("line_count_target"),
        "max_chars_target": unit.get("max_chars_target"),
        "reading_density": _reading_density(char_count, duration),
        "readability_note": _readability_note(char_count, duration),
        "beat_alignment_note": _beat_alignment_note(str(unit.get("beat_id") or "")),
        "visual_interference_note": visual_note,
        "production_status": [
            "diagnostic_only",
            "not_final_script",
            "not_TTS_ready",
        ],
        "transfer_status": "blocked",
    }


def _reading_density(char_count: int, duration_sec: int) -> str:
    if duration_sec <= 0:
        return "high"
    chars_per_sec = char_count / duration_sec
    if chars_per_sec <= 1.5:
        return "low"
    if chars_per_sec <= 2.5:
        return "medium"
    return "high"


def _readability_note(char_count: int, duration_sec: int) -> str:
    density = _reading_density(char_count, duration_sec)
    if density == "low":
        return "Short enough for relaxed diagnostic caption reading."
    if density == "medium":
        return "Readable as a short diagnostic caption; keep under review before narration."
    return "Dense for the current duration; revise before any downstream transfer review."


def _beat_alignment_note(beat_id: str) -> str:
    if beat_id == "beat_fake_intro_001":
        return "Keeps the intro limited to a fake topic and review-only handoff."
    if beat_id == "beat_fake_claim_001":
        return "Keeps the claim beat synthetic and source-check oriented."
    return "Keeps the caption aligned to its source beat."


def _visual_interference_note(plan: dict[str, Any], beat_id: str) -> str:
    visuals = [
        visual
        for visual in _list(plan.get("visual_timing"))
        if visual.get("beat_id") == beat_id
    ]
    if not visuals:
        return "No visual timing row is linked to this caption beat."
    risks = [str(visual.get("caption_interference_risk") or "unknown") for visual in visuals]
    if any("medium" in risk for risk in risks):
        return "Use concise copy because the linked visual has a caption reserve warning."
    return "Linked visual has low caption interference in the diagnostic plan."


def _density_band_counts(units: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"low": 0, "medium": 0, "high": 0}
    for unit in units:
        density = unit.get("reading_density")
        if density in counts:
            counts[density] += 1
    return counts


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None
