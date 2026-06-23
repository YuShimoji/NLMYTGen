"""Timing gap strategy for the diagnostic newsroom YMM4 lane.

This module compares the neutral 68 second planning timeline with the saved
diagnostic .ymmp natural duration. It records strategy only: it does not patch
.ymmp, launch YMM4, render, generate TTS/audio, import real media, fetch
external sources, or approve production use.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.newsroom_diagnostic_ymmp_manual_result import (
    DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH,
)
from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
    DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object


YYM4_TIMING_GAP_STRATEGY_SCHEMA_VERSION = "newsroom_yym4_timing_gap_strategy.v1"
YYM4_TIMING_GAP_STRATEGY_ID = (
    "newsroom_yym4_timing_gap_strategy_v1_2026_06_23"
)
DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH = Path(
    "samples/_probe/newsroom_handoff/yym4_timing_gap_strategy_v1.json"
)
DEFAULT_YYM4_TIMING_GAP_STRATEGY_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YYM4_TIMING_GAP_STRATEGY_V1_2026-06-23.md"
)

RECOMMENDED_DEFAULT = "hybrid_natural_first_then_patch_later"
NEXT_RECOMMENDED_SLICE = "newsroom-tiny-render-smoke-boundary-v1"
AFTER_TINY_RENDER_SMOKE_SLICE = "newsroom-ymmp-timing-patch-strategy-v1"


def build_default_newsroom_yym4_timing_gap_strategy(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed timing gap strategy from source readbacks."""
    base = Path(root) if root is not None else Path(".")
    structure_readback = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
    )
    manual_result = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH
    )
    return build_newsroom_yym4_timing_gap_strategy(
        structure_readback,
        manual_result,
        source_structure_readback_path=DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH,
        source_manual_result_readback_path=DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH,
    )


def build_newsroom_yym4_timing_gap_strategy(
    structure_readback: dict[str, Any],
    manual_result: dict[str, Any],
    *,
    source_structure_readback_path: str | Path,
    source_manual_result_readback_path: str | Path,
) -> dict[str, Any]:
    """Build a diagnostic-only YMM4 timing gap strategy."""
    source_validation = _source_validation(structure_readback, manual_result)
    timing_facts = _timing_facts(structure_readback)
    options = _strategy_options()
    boundary = _boundary()
    not_accepted_scope = _not_accepted_scope()
    strategy_status = (
        "accepted_for_next_tiny_render_smoke"
        if not source_validation["errors"]
        else "blocked"
    )

    return {
        "artifact_id": YYM4_TIMING_GAP_STRATEGY_ID,
        "strategy_id": YYM4_TIMING_GAP_STRATEGY_ID,
        "schema_version": YYM4_TIMING_GAP_STRATEGY_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "strategy_status": strategy_status,
        "identity": {
            "strategy_id": YYM4_TIMING_GAP_STRATEGY_ID,
            "source_structure_readback_path": _path_text(
                source_structure_readback_path
            ),
            "source_structure_readback_id": structure_readback.get("readback_id"),
            "source_manual_result_readback_path": _path_text(
                source_manual_result_readback_path
            ),
            "source_manual_result_id": manual_result.get("result_id"),
            "production_status": "diagnostic_only",
            "strategy_status": strategy_status,
        },
        "source_validation": source_validation,
        "timing_facts": timing_facts,
        "strategy_options": options,
        "recommended_default": {
            "choice": RECOMMENDED_DEFAULT,
            "next_recommended_slice": NEXT_RECOMMENDED_SLICE,
            "after_that": AFTER_TINY_RENDER_SMOKE_SLICE,
            "reasoning": [
                "The first tiny render smoke should isolate YMM4/render tool-chain viability.",
                "Timing patch mechanics should not be mixed with the first render proof.",
                "The neutral 68 second metadata remains valid as production-like planning data.",
                "The saved YMM4 natural duration is valid only for diagnostic smoke evidence.",
            ],
            "what_it_enables_next": [
                "prepare a tiny render smoke boundary using the saved natural duration",
                "defer neutral-timing stretch into a separate patch strategy",
                "keep audio/TTS readiness outside the render smoke decision",
            ],
            "what_it_defers": [
                "production-like 68 second .ymmp timing",
                "audio and narration timing alignment",
                "public video readiness",
            ],
        },
        "next_path": {
            "if_hybrid_chosen": {
                "next_recommended_slice": NEXT_RECOMMENDED_SLICE,
                "after_that": AFTER_TINY_RENDER_SMOKE_SLICE,
            },
            "if_timing_patch_first_chosen": {
                "next_recommended_slice": (
                    "newsroom-ymmp-timing-patch-planning-v1"
                ),
            },
            "if_blocked": {
                "missing_evidence": source_validation["errors"],
            },
        },
        "boundary": boundary,
        "not_accepted_scope": not_accepted_scope,
        "review_memory": {
            "review_source": "diagnostic_ymmp_structure_readback",
            "prior_user_review_count": {
                "manual_import_behavior": 1,
                "bound_speaker_behavior": 1,
                "diagnostic_ymmp_manual_observation": 1,
                "ymmp_structure_readback": 1,
                "timing_gap_strategy": 0,
            },
            "prior_evidence_reused": [
                "diagnostic manual .ymmp save observation",
                "diagnostic .ymmp structure readback",
                "canonical speaker correction v2",
            ],
            "next_nonredundant_axis": [
                NEXT_RECOMMENDED_SLICE,
                AFTER_TINY_RENDER_SMOKE_SLICE,
                "newsroom-audio-tts-boundary-v1",
            ],
            "accepted_scope": {
                "neutral_timeline_and_yym4_duration_gap_compared": True,
                "timing_options_evaluated": True,
                "recommended_default_recorded": True,
            },
            "not_accepted_scope": not_accepted_scope,
            "repeated_general_review_allowed": False,
            "input_mode": "freeform",
        },
        "human_burden_hygiene": {
            "user_input": "freeform",
            "template_required": False,
            "schema_owner": "Agent",
            "max_required_points": 0,
            "screenshot_optional": True,
            "negative_confirmations_required_from_user": False,
            "fixed_form_result_template": False,
            "operator_observation_card": "none",
            "user_side_work_this_slice": "none",
        },
        "downstream_next_use": {
            "use_this_strategy_to": [
                "authorize planning for a tiny render smoke boundary",
                "keep the first render smoke on natural diagnostic timing",
                "open a later neutral timing patch strategy after render smoke evidence",
            ],
            "do_not_use_this_strategy_to": [
                "patch or commit .ymmp files",
                "claim render readiness",
                "claim TTS readiness",
                "claim production readiness",
                "prepare or publish a public video",
            ],
        },
        "review_card": {
            "status": "none",
            "reason": (
                "The required timing evidence is already in repo readbacks; this "
                "strategy does not request manual observation or a fixed form."
            ),
        },
    }


def render_newsroom_yym4_timing_gap_strategy_markdown(
    strategy: dict[str, Any],
) -> str:
    """Render a human-readable timing gap strategy readback."""
    identity = _dict(strategy.get("identity"))
    validation = _dict(strategy.get("source_validation"))
    facts = _dict(strategy.get("timing_facts"))
    recommended = _dict(strategy.get("recommended_default"))
    next_path = _dict(strategy.get("next_path"))
    boundary = _dict(strategy.get("boundary"))
    hygiene = _dict(strategy.get("human_burden_hygiene"))
    review = _dict(strategy.get("review_memory"))

    lines = [
        "# Newsroom YMM4 Timing Gap Strategy v1",
        "",
        f"artifact_id: {strategy.get('artifact_id')}",
        f"strategy_id: {strategy.get('strategy_id')}",
        f"schema_version: {strategy.get('schema_version')}",
        f"review_status: {strategy.get('review_status')}",
        f"production_status: {strategy.get('production_status')}",
        f"strategy_status: {strategy.get('strategy_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
        (
            "- source_structure_readback_path: "
            f"{identity.get('source_structure_readback_path')}"
        ),
        (
            "- source_structure_readback_id: "
            f"{identity.get('source_structure_readback_id')}"
        ),
        (
            "- source_manual_result_readback_path: "
            f"{identity.get('source_manual_result_readback_path')}"
        ),
        (
            "- source_manual_result_id: "
            f"{identity.get('source_manual_result_id')}"
        ),
        "",
        "## Source Validation",
        "",
        f"- status: {validation.get('status')}",
        f"- errors: {_display(validation.get('errors'))}",
        f"- canonical_speaker_value: {validation.get('canonical_speaker_value')}",
        (
            "- canonical_speaker_unicode_escape: "
            f"{validation.get('canonical_speaker_unicode_escape')}"
        ),
        (
            "- accepted_speaker_value_must_not_equal_mojibake: "
            f"{_display(validation.get('accepted_speaker_value_must_not_equal_mojibake'))}"
        ),
        "",
        "## Timing Facts",
        "",
        f"- neutral_timeline_total_sec: {facts.get('neutral_timeline_total_sec')}",
        f"- ymmp_fps: {facts.get('ymmp_fps')}",
        f"- ymmp_total_frames: {facts.get('ymmp_total_frames')}",
        f"- ymmp_total_duration_sec: {facts.get('ymmp_total_duration_sec')}",
        f"- timing_gap_sec: {facts.get('timing_gap_sec')}",
        f"- timing_imported_by_csv: {_display(facts.get('timing_imported_by_csv'))}",
        f"- timing_patch_applied: {_display(facts.get('timing_patch_applied'))}",
        f"- item_frames: {_display(facts.get('item_frames'))}",
        f"- item_lengths: {_display(facts.get('item_lengths'))}",
        "",
        "## Strategy Options",
        "",
        "| option | role | enables | defers | main risk |",
        "|---|---|---|---|---|",
    ]
    for option in strategy.get("strategy_options", []):
        lines.append(
            "| "
            f"{option.get('option_id')} | "
            f"{option.get('decision_role')} | "
            f"{'; '.join(option.get('what_it_enables', []))} | "
            f"{'; '.join(option.get('what_it_blocks_or_defers', []))} | "
            f"{'; '.join(option.get('risks', []))} |"
        )

    lines.extend(
        [
            "",
            "## Recommended Default",
            "",
            f"- choice: {recommended.get('choice')}",
            f"- next_recommended_slice: {recommended.get('next_recommended_slice')}",
            f"- after_that: {recommended.get('after_that')}",
            "- reasoning:",
        ]
    )
    for reason in recommended.get("reasoning", []):
        lines.append(f"  - {reason}")
    lines.append("- what_it_enables_next:")
    for item in recommended.get("what_it_enables_next", []):
        lines.append(f"  - {item}")
    lines.append("- what_it_defers:")
    for item in recommended.get("what_it_defers", []):
        lines.append(f"  - {item}")

    hybrid = _dict(next_path.get("if_hybrid_chosen"))
    patch_first = _dict(next_path.get("if_timing_patch_first_chosen"))
    blocked = _dict(next_path.get("if_blocked"))
    lines.extend(
        [
            "",
            "## Next Path",
            "",
            (
                "- if_hybrid_chosen: "
                f"{hybrid.get('next_recommended_slice')} -> {hybrid.get('after_that')}"
            ),
            (
                "- if_timing_patch_first_chosen: "
                f"{patch_first.get('next_recommended_slice')}"
            ),
            f"- if_blocked_missing_evidence: {_display(blocked.get('missing_evidence'))}",
            "",
            "## Boundary",
            "",
        ]
    )
    for key, value in boundary.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Human Burden Hygiene", ""])
    for key, value in hygiene.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Review Memory",
            "",
            (
                "- prior_user_review_count: "
                f"{_display(review.get('prior_user_review_count'))}"
            ),
            (
                "- next_nonredundant_axis: "
                f"{_display(review.get('next_nonredundant_axis'))}"
            ),
            (
                "- repeated_general_review_allowed: "
                f"{_display(review.get('repeated_general_review_allowed'))}"
            ),
            "",
            "## Boundary Note",
            "",
            "This strategy records a diagnostic timing decision only. It does "
            "not patch `.ymmp`, stage or commit `.ymmp`, launch YMM4, render, "
            "generate TTS/audio, import real media, approve production, or "
            "prepare a public video.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    structure_readback: dict[str, Any],
    manual_result: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    parse_status = _dict(structure_readback.get("parse_status"))
    dialogue = _dict(structure_readback.get("dialogue_structure"))
    timing = _dict(structure_readback.get("timing_structure"))
    manual_normalized = _dict(manual_result.get("normalized_result"))

    if structure_readback.get("production_status") != "diagnostic_only":
        errors.append("STRUCTURE_READBACK_NOT_DIAGNOSTIC_ONLY")
    if parse_status.get("parse_status") != "parsed":
        errors.append("STRUCTURE_READBACK_NOT_PARSED")
    if dialogue.get("dialogue_item_count") != 4:
        errors.append("DIALOGUE_ITEM_COUNT_NOT_4")
    if dialogue.get("canonical_speaker_value") != CANONICAL_UI_OBSERVED_SPEAKER:
        errors.append("CANONICAL_SPEAKER_MISMATCH")
    if dialogue.get("accepted_speaker_value_must_not_equal_mojibake") is not True:
        errors.append("CANONICAL_SPEAKER_MOJIBAKE_GUARD_MISSING")
    if timing.get("neutral_timeline_total_sec") != 68:
        errors.append("NEUTRAL_TIMELINE_TOTAL_SEC_NOT_68")
    if timing.get("observed_project_duration_frames") != 509:
        errors.append("YMMP_TOTAL_FRAMES_NOT_509")
    if timing.get("timing_patch_applied") is not False:
        errors.append("TIMING_PATCH_ALREADY_APPLIED")
    if manual_result.get("result") != "pass":
        errors.append("MANUAL_RESULT_NOT_PASS")
    if manual_normalized.get("timing_observation") != "short_natural_duration":
        errors.append("MANUAL_TIMING_OBSERVATION_NOT_SHORT_NATURAL")

    return {
        "status": "passed" if not errors else "blocked",
        "structure_readback_id": structure_readback.get("readback_id"),
        "manual_result_id": manual_result.get("result_id"),
        "parse_status": parse_status.get("parse_status"),
        "manual_result": manual_result.get("result"),
        "dialogue_item_count": dialogue.get("dialogue_item_count"),
        "canonical_speaker_value": dialogue.get("canonical_speaker_value"),
        "canonical_speaker_unicode_escape": dialogue.get(
            "canonical_speaker_unicode_escape"
        ),
        "accepted_speaker_value_must_not_equal_mojibake": dialogue.get(
            "accepted_speaker_value_must_not_equal_mojibake"
        ),
        "timing_gap_status": timing.get("timing_gap_status"),
        "errors": errors,
    }


def _timing_facts(structure_readback: dict[str, Any]) -> dict[str, Any]:
    timing = _dict(structure_readback.get("timing_structure"))
    item_timings = [
        item
        for item in timing.get("item_timings", [])
        if isinstance(item, dict)
    ]
    neutral_total = _number(timing.get("neutral_timeline_total_sec")) or 68
    ymmp_duration = _number(timing.get("observed_project_duration_sec")) or 0
    item_frames = [_whole_number(item.get("frame")) for item in item_timings]
    item_lengths = [
        _whole_number(item.get("length_frames")) for item in item_timings
    ]
    return {
        "neutral_timeline_total_sec": _whole_number(neutral_total),
        "ymmp_fps": _whole_number(timing.get("fps")),
        "ymmp_total_frames": _whole_number(
            timing.get("observed_project_duration_frames")
        ),
        "ymmp_total_duration_sec": ymmp_duration,
        "item_frames": item_frames,
        "item_lengths": item_lengths,
        "timing_gap_sec": round(neutral_total - ymmp_duration, 6),
        "timing_imported_by_csv": False,
        "timing_patch_applied": False,
        "source_timing_gap_status": timing.get("timing_gap_status"),
        "ymmp_natural_duration_observed": timing.get(
            "ymmp_natural_duration_observed"
        ),
    }


def _strategy_options() -> list[dict[str, Any]]:
    return [
        {
            "option_id": "accept_yym4_natural_duration_for_first_smoke",
            "decision_role": "viable_but_too_short_as_final_strategy",
            "benefits": [
                "isolates render smoke from timing patch mechanics",
                "uses the saved diagnostic .ymmp exactly as observed",
            ],
            "risks": [
                "can be mistaken for production timing if not fenced",
                "does not test the 68 second neutral pacing plan",
            ],
            "what_it_enables": [
                "first tiny render smoke boundary",
                "tool-chain viability check",
            ],
            "what_it_blocks_or_defers": [
                "neutral 68 second timing proof",
                "audio/narration alignment",
            ],
        },
        {
            "option_id": "patch_ymmp_to_neutral_68s_before_render",
            "decision_role": "deferred_not_default",
            "benefits": [
                "tests production-like duration earlier",
                "aligns render timing with neutral planning metadata",
            ],
            "risks": [
                "mixes timing patch behavior with first render smoke",
                "requires a separate .ymmp patch boundary before evidence exists",
            ],
            "what_it_enables": [
                "neutral duration patch planning",
                "later production-like timing proof",
            ],
            "what_it_blocks_or_defers": [
                "smallest render smoke isolation",
                "current diagnostic natural-duration proof reuse",
            ],
        },
        {
            "option_id": RECOMMENDED_DEFAULT,
            "decision_role": "recommended_default",
            "benefits": [
                "keeps first smoke small and diagnostic",
                "preserves neutral metadata for a later dedicated patch slice",
                "keeps audio/TTS boundary separate",
            ],
            "risks": [
                "requires two evidence steps instead of one",
                "natural timing must stay clearly marked diagnostic-only",
            ],
            "what_it_enables": [
                NEXT_RECOMMENDED_SLICE,
                AFTER_TINY_RENDER_SMOKE_SLICE,
            ],
            "what_it_blocks_or_defers": [
                "68 second .ymmp patch in this slice",
                "TTS readiness claims",
                "production approval",
            ],
        },
        {
            "option_id": "keep_timing_external_until_render_path",
            "decision_role": "too_passive_after_structure_readback",
            "benefits": [
                "avoids .ymmp edits entirely",
                "keeps neutral metadata available outside YMM4",
            ],
            "risks": [
                "does not reduce the render smoke decision bottleneck",
                "can leave natural versus neutral timing unresolved too long",
            ],
            "what_it_enables": [
                "docs-only planning",
                "future timing comparison",
            ],
            "what_it_blocks_or_defers": [
                "tiny render smoke boundary",
                "timing patch strategy",
            ],
        },
    ]


def _boundary() -> dict[str, bool]:
    return {
        "ymmp_patched_in_this_slice": False,
        "ymmp_created_in_this_slice": False,
        "ymmp_staged_or_committed": False,
        "ymmp_committed": False,
        "agent_launched_yym4": False,
        "render_created": False,
        "TTS_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "real_newsroom_ingest_performed": False,
        "dashboard_governance_freshness_changed": False,
        "production_approval": False,
        "public_video_ready": False,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_ymmp": False,
        "timing_patch": False,
        "render_readiness": False,
        "TTS_readiness": False,
        "public_video_readiness": False,
        "visual_layout_import": False,
        "production_approval": False,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _number(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _whole_number(value: Any) -> int | float | None:
    number = _number(value)
    if number is None:
        return None
    return int(number) if number.is_integer() else number


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
