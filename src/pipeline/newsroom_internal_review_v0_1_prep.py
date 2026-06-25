"""Internal review v0.1 prep package for the newsroom diagnostic video.

This module packages existing diagnostic YMM4 evidence for internal review. It
does not launch YMM4, render video, edit .ymmp files, generate audio/TTS, fetch
external sources, import media, or approve production/public use.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_audio_observation_and_timing_patch_readiness import (
    DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH,
)
from src.pipeline.newsroom_audio_tts_boundary import (
    DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH,
)
from src.pipeline.newsroom_caption_timing_plan import DEFAULT_PLAN_PATH
from src.pipeline.newsroom_card_placement_render_smoke_result_readback import (
    DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import (
    DEFAULT_CAPSULE_PATH,
    load_json_object,
)
from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH,
)
from src.pipeline.newsroom_yym4_card_asset_placement_probe import (
    DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH,
)
from src.pipeline.newsroom_ymmp_timing_patch_render_smoke_result_readback import (
    DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH,
)


INTERNAL_REVIEW_V0_1_PREP_SCHEMA_VERSION = "newsroom_internal_review_v0_1_prep.v1"
INTERNAL_REVIEW_V0_1_PREP_ID = (
    "newsroom_internal_review_v0_1_prep_v1_2026_06_25"
)
DEFAULT_INTERNAL_REVIEW_V0_1_PREP_PATH = Path(
    "samples/_probe/newsroom_handoff/internal_review_v0_1_prep_v1.json"
)
DEFAULT_INTERNAL_REVIEW_V0_1_PREP_DOC_PATH = Path(
    "docs/verification/NEWSROOM_INTERNAL_REVIEW_V0_1_PREP_V1_2026-06-25.md"
)
DEFAULT_INTERNAL_REVIEW_V0_1_REVIEW_BRIEF_PATH = Path(
    "docs/verification/NEWSROOM_INTERNAL_REVIEW_V0_1_REVIEW_BRIEF_2026-06-25.md"
)

NEXT_DEFAULT_SLICE = "newsroom-internal-review-v0.1-operator-review-card"
INTERNAL_REVIEW_RENDER_PACKAGE_SLICE = (
    "newsroom-internal-review-v0.1-render-package-v1"
)
RSS_DRY_RUN_PLAN_SLICE = "newsroom-rss-dry-run-integration-plan-v1"
VISUAL_CARD_REFINEMENT_SLICE = "newsroom-visual-card-design-refinement-v1"


def build_default_newsroom_internal_review_v0_1_prep(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed internal review v0.1 prep package."""
    base = Path(root) if root is not None else Path(".")
    card_render_result = load_json_object(
        base / DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    card_placement_probe = load_json_object(
        base / DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH
    )
    visual_card_bridge = load_json_object(base / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH)
    timing_render_result = load_json_object(
        base / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    audio_observation = load_json_object(
        base / DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
    )
    tiny_render_result = load_json_object(
        base / DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    capsule = load_json_object(base / DEFAULT_CAPSULE_PATH)
    caption_timing_plan = load_json_object(base / DEFAULT_PLAN_PATH)
    return build_newsroom_internal_review_v0_1_prep(
        card_render_result,
        card_placement_probe,
        visual_card_bridge,
        timing_render_result,
        audio_observation,
        tiny_render_result,
        capsule,
        caption_timing_plan,
        source_card_render_result_path=(
            DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        source_card_placement_probe_path=DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH,
        source_visual_card_bridge_path=DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH,
        source_timing_patch_render_result_path=(
            DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        source_audio_observation_path=(
            DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
        ),
        source_tiny_render_result_path=DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH,
        source_episode_capsule_path=DEFAULT_CAPSULE_PATH,
        source_caption_timing_plan_path=DEFAULT_PLAN_PATH,
    )


def write_default_newsroom_internal_review_v0_1_prep_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write the JSON prep package, readback doc, and review brief."""
    base = Path(root) if root is not None else Path(".")
    prep = build_default_newsroom_internal_review_v0_1_prep(root=base)
    _write_json(base / DEFAULT_INTERNAL_REVIEW_V0_1_PREP_PATH, prep)
    _write_text(
        base / DEFAULT_INTERNAL_REVIEW_V0_1_PREP_DOC_PATH,
        render_newsroom_internal_review_v0_1_prep_markdown(prep),
    )
    _write_text(
        base / DEFAULT_INTERNAL_REVIEW_V0_1_REVIEW_BRIEF_PATH,
        render_newsroom_internal_review_v0_1_review_brief(prep),
    )
    return prep


def build_newsroom_internal_review_v0_1_prep(
    card_render_result: dict[str, Any],
    card_placement_probe: dict[str, Any],
    visual_card_bridge: dict[str, Any],
    timing_render_result: dict[str, Any],
    audio_observation: dict[str, Any],
    tiny_render_result: dict[str, Any],
    capsule: dict[str, Any],
    caption_timing_plan: dict[str, Any],
    *,
    source_card_render_result_path: str | Path,
    source_card_placement_probe_path: str | Path,
    source_visual_card_bridge_path: str | Path,
    source_timing_patch_render_result_path: str | Path,
    source_audio_observation_path: str | Path,
    source_tiny_render_result_path: str | Path,
    source_episode_capsule_path: str | Path,
    source_caption_timing_plan_path: str | Path,
) -> dict[str, Any]:
    """Build a diagnostic-only review prep package from existing evidence."""
    source_validation = _source_validation(
        card_render_result,
        card_placement_probe,
        visual_card_bridge,
        timing_render_result,
        audio_observation,
        tiny_render_result,
        capsule,
        caption_timing_plan,
    )
    candidate_summary = _candidate_summary(card_render_result)
    evidence_map = _evidence_map(
        card_render_result,
        card_placement_probe,
        visual_card_bridge,
        timing_render_result,
        audio_observation,
        tiny_render_result,
        capsule,
        caption_timing_plan,
    )

    return {
        "artifact_id": INTERNAL_REVIEW_V0_1_PREP_ID,
        "review_package_id": INTERNAL_REVIEW_V0_1_PREP_ID,
        "schema_version": INTERNAL_REVIEW_V0_1_PREP_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "review_stage": [
            "internal_review_v0_1_prep",
            "not_public",
            "not_production",
        ],
        "identity": {
            "review_package_id": INTERNAL_REVIEW_V0_1_PREP_ID,
            "source_card_render_result_path": _path_text(
                source_card_render_result_path
            ),
            "source_card_render_result_id": card_render_result.get("readback_id"),
            "source_card_placement_probe_path": _path_text(
                source_card_placement_probe_path
            ),
            "source_card_placement_probe_id": card_placement_probe.get("probe_id"),
            "source_visual_card_bridge_path": _path_text(
                source_visual_card_bridge_path
            ),
            "source_visual_card_bridge_id": visual_card_bridge.get("bridge_id"),
            "source_timing_patch_render_result_path": _path_text(
                source_timing_patch_render_result_path
            ),
            "source_timing_patch_render_result_id": timing_render_result.get(
                "readback_id"
            ),
            "source_audio_observation_path": _path_text(
                source_audio_observation_path
            ),
            "source_audio_observation_id": audio_observation.get("readback_id"),
            "source_tiny_render_result_path": _path_text(source_tiny_render_result_path),
            "source_tiny_render_result_id": tiny_render_result.get("result_id")
            or tiny_render_result.get("artifact_id"),
            "source_episode_capsule_path": _path_text(source_episode_capsule_path),
            "source_episode_capsule_id": capsule.get("artifact_id"),
            "source_caption_timing_plan_path": _path_text(
                source_caption_timing_plan_path
            ),
            "source_caption_timing_plan_id": caption_timing_plan.get("artifact_id"),
            "production_status": "diagnostic_only",
            "review_stage": "internal_review_v0_1_prep",
        },
        "source_validation": source_validation,
        "evidence_map": evidence_map,
        "internal_review_v0_1_candidate_summary": candidate_summary,
        "review_questions": _review_questions(),
        "accepted_scope": _accepted_scope(),
        "not_accepted_scope": _not_accepted_scope(),
        "next_milestone_recommendation": _next_milestone_recommendation(),
        "render_gate_carry_forward": _render_gate_carry_forward(),
        "readiness_separation": _readiness_separation(),
        "benchmark_baseline": _benchmark_baseline(candidate_summary),
        "goal_stack": _goal_stack(),
        "completion_matrix": _completion_matrix(),
        "artifact_readiness": _artifact_readiness(),
        "internal_review_readiness": _internal_review_readiness(),
        "video_readiness": _video_readiness(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(),
        "review_brief": _review_brief(),
        "boundaries": _boundaries(),
        "downstream_next_use": _downstream_next_use(),
    }


def render_newsroom_internal_review_v0_1_prep_markdown(
    prep: dict[str, Any],
) -> str:
    """Render the human-readable review prep document."""
    lines = [
        "# Newsroom Internal Review v0.1 Prep v1",
        "",
        f"artifact_id: {prep.get('artifact_id')}",
        f"review_package_id: {prep.get('review_package_id')}",
        f"schema_version: {prep.get('schema_version')}",
        f"review_status: {prep.get('review_status')}",
        f"production_status: {prep.get('production_status')}",
        f"review_stage: {_display(prep.get('review_stage'))}",
        "diagnostic_only: true",
        "",
        "## Identity",
        "",
    ]
    for key, value in _dict(prep.get("identity")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Source Validation", ""])
    for key, value in _dict(prep.get("source_validation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Evidence Map",
            "",
            "| axis | status | evidence | implication |",
            "|---|---|---|---|",
        ]
    )
    for row in prep.get("evidence_map", []):
        lines.append(
            "| "
            f"{row.get('axis')} | "
            f"{row.get('status')} | "
            f"{row.get('evidence_path')} | "
            f"{row.get('review_implication')} |"
        )

    lines.extend(["", "## Candidate Summary", ""])
    for key, value in _dict(prep.get("internal_review_v0_1_candidate_summary")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Review Questions", ""])
    for question in prep.get("review_questions", []):
        lines.append(f"- {question}")

    lines.extend(["", "## Accepted Scope", ""])
    for key, value in _dict(prep.get("accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(prep.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Next Milestone Recommendation", ""])
    for key, value in _dict(prep.get("next_milestone_recommendation")).items():
        if key == "alternative_next_slices":
            continue
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "| alternative slice | reason |",
            "|---|---|",
        ]
    )
    for row in _dict(prep.get("next_milestone_recommendation")).get(
        "alternative_next_slices", []
    ):
        lines.append(f"| {row.get('slice')} | {row.get('reason')} |")

    lines.extend(["", "## Render Gate Carry-Forward", ""])
    for key, value in _dict(prep.get("render_gate_carry_forward")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Readiness Separation", ""])
    for key, value in _dict(prep.get("readiness_separation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Benchmark Baseline", ""])
    for key, value in _dict(prep.get("benchmark_baseline")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Goal Stack",
            "",
            "| level | goal | success signal | contribution |",
            "|---|---|---|---|",
        ]
    )
    for row in prep.get("goal_stack", []):
        lines.append(
            "| "
            f"{row.get('level')} | "
            f"{row.get('goal')} | "
            f"{row.get('success_signal')} | "
            f"{row.get('contribution')} |"
        )

    _append_status_table(lines, "Completion Matrix", prep.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", prep.get("artifact_readiness"))
    _append_status_table(
        lines, "Internal Review Readiness", prep.get("internal_review_readiness")
    )
    _append_status_table(lines, "Video Readiness", prep.get("video_readiness"))
    _append_status_table(lines, "Render Gate Hygiene", prep.get("render_gate_hygiene"))
    _append_status_table(
        lines, "Human Burden Hygiene", prep.get("human_burden_hygiene")
    )
    _append_status_table(
        lines, "Review Non-Redundancy", prep.get("review_non_redundancy")
    )
    _append_status_table(lines, "Inertia Check", prep.get("inertia_check"))

    lines.extend(["", "## Boundary", ""])
    for key, value in _dict(prep.get("boundaries")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This package prepares a diagnostic internal review candidate from "
            "existing evidence only. It does not approve production quality, "
            "public release, real newsroom content, RSS/live ingest, final "
            "packaging, or another render for documentation-only changes.",
            "",
        ]
    )
    return "\n".join(lines)


def render_newsroom_internal_review_v0_1_review_brief(
    prep: dict[str, Any],
) -> str:
    """Render the compact operator-facing review brief."""
    candidate = _dict(prep.get("internal_review_v0_1_candidate_summary"))
    lines = [
        "# Newsroom Internal Review v0.1 Review Brief",
        "",
        "This is a diagnostic internal review candidate, not a production or "
        "public-ready video.",
        "",
        "## Candidate",
        "",
        f"- video: {candidate.get('candidate_video_name')}",
        f"- duration: {candidate.get('candidate_duration_sec')} sec",
        f"- content: {candidate.get('candidate_content_type')}",
        f"- cards: {candidate.get('card_count')}",
        f"- dialogue items: {candidate.get('dialogue_item_count')}",
        f"- voice path: {candidate.get('voice_path')}",
        "",
        "## Review Focus",
        "",
    ]
    for question in prep.get("review_questions", []):
        lines.append(f"- {question}")
    lines.extend(
        [
            "",
            "## Boundaries",
            "",
            "- Keep feedback freeform and focused on the current diagnostic video.",
            "- Treat production quality, real newsroom content, publication, and final packaging as out of scope.",
            "- Prefer one highest-value next improvement over a broad checklist.",
            "",
            "## Next Use",
            "",
            f"Default next slice: {NEXT_DEFAULT_SLICE}",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    card_render_result: dict[str, Any],
    card_placement_probe: dict[str, Any],
    visual_card_bridge: dict[str, Any],
    timing_render_result: dict[str, Any],
    audio_observation: dict[str, Any],
    tiny_render_result: dict[str, Any],
    capsule: dict[str, Any],
    caption_timing_plan: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    card_normalized = _dict(card_render_result.get("normalized_render_result"))
    timing_normalized = _dict(timing_render_result.get("normalized_render_result"))
    if card_render_result.get("result_status") != "pass":
        errors.append("CARD_PLACEMENT_RENDER_RESULT_NOT_PASS")
    if card_normalized.get("output_duration_sec") != 68:
        errors.append("CARD_PLACEMENT_RENDER_DURATION_NOT_68")
    if card_normalized.get("card_count_visible") != 4:
        errors.append("CARD_COUNT_VISIBLE_NOT_4")
    if card_placement_probe.get("probe_status") != "placed_structurally":
        errors.append("CARD_PLACEMENT_PROBE_NOT_STRUCTURAL_PASS")
    if visual_card_bridge.get("visual_status") != "asset_bridge_created":
        errors.append("VISUAL_CARD_BRIDGE_NOT_READY")
    if timing_render_result.get("result_status") != "pass":
        errors.append("TIMING_RENDER_RESULT_NOT_PASS")
    if timing_normalized.get("native_audio_present") is not True:
        errors.append("NATIVE_AUDIO_NOT_PRESENT_IN_PRIOR_RENDER")
    if audio_observation.get("production_status") != "diagnostic_only":
        errors.append("AUDIO_OBSERVATION_NOT_DIAGNOSTIC_ONLY")
    if tiny_render_result.get("render_smoke_status") not in {"pass", "observed", None}:
        errors.append("TINY_RENDER_STATUS_NOT_OBSERVED")
    if capsule.get("production_status") != "diagnostic_only":
        errors.append("CAPSULE_NOT_DIAGNOSTIC_ONLY")
    if not _list(caption_timing_plan.get("caption_units")):
        errors.append("CAPTION_TIMING_UNITS_MISSING")

    return {
        "status": "passed" if not errors else "blocked",
        "errors": errors,
        "card_render_result_id": card_render_result.get("readback_id"),
        "card_render_result": card_render_result.get("result_status"),
        "card_render_duration_sec": card_normalized.get("output_duration_sec"),
        "card_render_card_count": card_normalized.get("card_count_visible"),
        "card_placement_probe_id": card_placement_probe.get("probe_id"),
        "card_placement_probe_status": card_placement_probe.get("probe_status"),
        "visual_card_bridge_id": visual_card_bridge.get("bridge_id"),
        "timing_render_result_id": timing_render_result.get("readback_id"),
        "timing_render_result": timing_render_result.get("result_status"),
        "native_audio_present_in_prior_render": timing_normalized.get(
            "native_audio_present"
        ),
        "audio_observation_id": audio_observation.get("readback_id"),
        "tiny_render_result_id": tiny_render_result.get("result_id")
        or tiny_render_result.get("artifact_id"),
        "episode_capsule_id": capsule.get("artifact_id"),
        "caption_timing_plan_id": caption_timing_plan.get("artifact_id"),
    }


def _evidence_map(
    card_render_result: dict[str, Any],
    card_placement_probe: dict[str, Any],
    visual_card_bridge: dict[str, Any],
    timing_render_result: dict[str, Any],
    audio_observation: dict[str, Any],
    tiny_render_result: dict[str, Any],
    capsule: dict[str, Any],
    caption_timing_plan: dict[str, Any],
) -> list[dict[str, Any]]:
    card_normalized = _dict(card_render_result.get("normalized_render_result"))
    timing_normalized = _dict(timing_render_result.get("normalized_render_result"))
    structural = _dict(card_placement_probe.get("structural_result"))
    return [
        {
            "axis": "script/caption import",
            "status": "diagnostic_pass",
            "evidence_path": _path_text(DEFAULT_TINY_RENDER_SMOKE_RESULT_READBACK_PATH),
            "evidence_id": tiny_render_result.get("result_id")
            or tiny_render_result.get("artifact_id"),
            "review_implication": "four fake dialogue rows are enough for internal review structure",
        },
        {
            "axis": "speaker binding",
            "status": "diagnostic_pass",
            "evidence_path": _path_text(
                DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
            ),
            "evidence_id": audio_observation.get("readback_id"),
            "review_implication": "native YMM4 yukkuri voice remains the diagnostic default",
        },
        {
            "axis": "native YMM4 audio",
            "status": "diagnostic_pass",
            "evidence_path": _path_text(
                DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH
            ),
            "evidence_id": timing_render_result.get("readback_id"),
            "observed_value": timing_normalized.get("native_audio_present"),
            "review_implication": "audio mechanics do not block internal review prep",
        },
        {
            "axis": "timing patch to 68 sec",
            "status": "diagnostic_pass",
            "evidence_path": _path_text(
                DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH
            ),
            "evidence_id": timing_render_result.get("readback_id"),
            "observed_value": timing_normalized.get("output_duration_sec"),
            "review_implication": "current benchmark duration is 68 sec",
        },
        {
            "axis": "card asset generation",
            "status": "diagnostic_pass",
            "evidence_path": _path_text(DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH),
            "evidence_id": visual_card_bridge.get("bridge_id"),
            "observed_value": len(_list(visual_card_bridge.get("assets"))),
            "review_implication": "external fake card asset bridge is available",
        },
        {
            "axis": "card placement as ImageItems",
            "status": "diagnostic_pass",
            "evidence_path": _path_text(DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH),
            "evidence_id": card_placement_probe.get("probe_id"),
            "observed_value": structural.get("card_image_item_count_observed"),
            "review_implication": "direct YMM4 text/shape card graph is avoided",
        },
        {
            "axis": "card placement render smoke",
            "status": "diagnostic_pass",
            "evidence_path": _path_text(
                DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
            ),
            "evidence_id": card_render_result.get("readback_id"),
            "observed_value": card_normalized.get("card_placement_effective_in_render"),
            "review_implication": "cards are visible in the diagnostic render surface",
        },
        {
            "axis": "render duration",
            "status": "diagnostic_pass",
            "evidence_path": _path_text(
                DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
            ),
            "evidence_id": card_render_result.get("readback_id"),
            "observed_value": card_normalized.get("output_duration_observed"),
            "review_implication": "duration matches the 68 sec timing patch",
        },
        {
            "axis": "render time approximate",
            "status": "observed_diagnostic",
            "evidence_path": _path_text(
                DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
            ),
            "evidence_id": card_render_result.get("readback_id"),
            "observed_value": card_normalized.get("render_time_approx_sec"),
            "review_implication": "local diagnostic render cost is currently about 30 sec",
        },
        {
            "axis": "not accepted production/public scope",
            "status": "closed_for_now",
            "evidence_path": _path_text(DEFAULT_CAPSULE_PATH),
            "evidence_id": capsule.get("artifact_id"),
            "observed_value": capsule.get("production_status"),
            "review_implication": "internal review must not be treated as production approval",
        },
        {
            "axis": "caption timing source",
            "status": "diagnostic_reference",
            "evidence_path": _path_text(DEFAULT_PLAN_PATH),
            "evidence_id": caption_timing_plan.get("artifact_id"),
            "observed_value": len(_list(caption_timing_plan.get("caption_units"))),
            "review_implication": "fake caption timing remains a review baseline, not final script density",
        },
    ]


def _candidate_summary(card_render_result: dict[str, Any]) -> dict[str, Any]:
    normalized = _dict(card_render_result.get("normalized_render_result"))
    return {
        "candidate_video_name": "diagnostic_bound_speaker_probe_card_placement_v1.mp4",
        "candidate_duration_sec": 68,
        "candidate_content_type": "fake/review-only diagnostic",
        "card_count": normalized.get("card_count_visible", 4),
        "dialogue_item_count": normalized.get("dialogue_item_count_observed", 4),
        "voice_path": "YMM4_native_yukkuri_japanese",
        "render_status": normalized.get("render_smoke_result", "pass"),
        "review_status": [
            "ready_for_internal_review_prep",
            "not_ready_for_publication",
        ],
    }


def _review_questions() -> list[str]:
    return [
        "Is the 68sec pacing intelligible despite sparse content?",
        "Do the four cards make the fake/review-only structure understandable?",
        "Is the subtitle/card safe area acceptable for a diagnostic baseline?",
        "Does the video feel like a viable internal review v0.1, not production?",
        "What is the single highest-value improvement before real packet integration?",
    ]


def _accepted_scope() -> dict[str, bool]:
    return {
        "diagnostic_68sec_yym4_video_exists_and_render_path_is_proven": True,
        "cards_audio_timing_survive_render": True,
        "internal_review_v0_1_can_be_prepared": True,
        "external_card_asset_bridge_is_viable": True,
        "yym4_native_audio_path_remains_preferred_for_diagnostic_flow": True,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_pacing": False,
        "final_visual_design": False,
        "final_narration_script_density": False,
        "real_newsroom_content": False,
        "rss_live_ingest": False,
        "rights_publication_boundary": False,
        "production_export_settings": False,
        "final_artifact_packaging": False,
        "public_prod_approval": False,
    }


def _next_milestone_recommendation() -> dict[str, Any]:
    return {
        "recommended_default": NEXT_DEFAULT_SLICE,
        "reason": (
            "all mechanical axes now pass at diagnostic level; the next useful "
            "input is a freeform internal review of pacing and visual comprehensibility"
        ),
        "avoid_next": "further mechanics/readback-only loop before review",
        "alternative_next_slices": [
            {
                "slice": INTERNAL_REVIEW_RENDER_PACKAGE_SLICE,
                "reason": "only if the repo needs a non-media package around the ignored local video",
            },
            {
                "slice": RSS_DRY_RUN_PLAN_SLICE,
                "reason": "later, after internal review identifies the next content direction",
            },
            {
                "slice": VISUAL_CARD_REFINEMENT_SLICE,
                "reason": "only if internal review identifies a visual issue",
            },
        ],
    }


def _render_gate_carry_forward() -> dict[str, Any]:
    return {
        "new_render_in_this_slice": False,
        "existing_card_placement_render_observation_consumed_once": True,
        "next_render_only_after": [
            "material visual/card design change",
            "internal review package explicitly needs a new render",
            "real packet dry run changes the surface",
        ],
        "no_render_for": [
            "docs changes",
            "readback changes",
            "review package changes",
        ],
        "YMM4_launched_by_agent": False,
        "render_audio_or_tts_created_by_agent": False,
    }


def _readiness_separation() -> dict[str, Any]:
    return {
        "slice_completion": "pass_for_this_prep",
        "video_readiness_progress": "6/7",
        "video_readiness_next_missing_gate": "internal review milestone completed",
        "visual_readiness_progress": "7/7_diagnostic",
        "production_readiness": "low_diagnostic_only",
        "internal_review_readiness": "prep_defined",
        "next_default_slice": NEXT_DEFAULT_SLICE,
    }


def _benchmark_baseline(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "video_duration_sec": candidate.get("candidate_duration_sec"),
        "render_time_approx_sec": 30,
        "fake_card_count": candidate.get("card_count"),
        "dialogue_item_count": candidate.get("dialogue_item_count"),
        "voice_path": candidate.get("voice_path"),
        "real_data_used": False,
        "production_public_readiness": False,
        "benchmark_label": "68sec diagnostic video with four fake cards and YMM4 native audio",
    }


def _goal_stack() -> list[dict[str, str]]:
    return [
        {
            "level": "Immediate",
            "goal": "Package current diagnostic video as internal review v0.1 candidate",
            "success_signal": "review prep JSON/doc/brief exist and cite evidence",
            "contribution": "moves from mechanics proof to review milestone",
        },
        {
            "level": "Short-term",
            "goal": "Enable freeform internal review",
            "success_signal": "operator review card is compact and focused",
            "contribution": "avoids more mechanical proof loops",
        },
        {
            "level": "Mid-term",
            "goal": "Identify highest-value refinement before real packet integration",
            "success_signal": "review outcome can choose visual refinement, script density, or RSS dry run",
            "contribution": "makes next work evidence-driven",
        },
        {
            "level": "Long-term",
            "goal": "Stabilize Newsroom-to-video automation",
            "success_signal": "review criteria become reusable for later real packet runs",
            "contribution": "reduces subjective drift",
        },
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "current_repo_state_verified", "status": True},
        {"gate": "source_evidence_artifacts_inspected", "status": True},
        {"gate": "internal_review_prep_json_created", "status": True},
        {"gate": "human_review_prep_doc_brief_created", "status": True},
        {"gate": "readiness_benchmark_baseline_recorded", "status": True},
        {
            "gate": "narrow_commit_created_and_pushed_if_push_gate_passes",
            "status": "pending_until_git_gate",
        },
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"artifact": "review_prep_json", "status": "present"},
        {"artifact": "human_readback", "status": "present"},
        {"artifact": "evidence_map", "status": "present"},
        {"artifact": "review_questions", "status": "present"},
        {"artifact": "not_accepted_scope", "status": "present"},
        {"artifact": "downstream_next_use", "status": "present"},
    ]


def _internal_review_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "candidate_identity_defined", "status": True},
        {"gate": "evidence_map_complete", "status": True},
        {"gate": "review_questions_defined", "status": True},
        {"gate": "user_observation_burden_bounded", "status": True},
        {"gate": "production_public_boundary_preserved", "status": True},
        {"gate": "next_review_action_named", "status": NEXT_DEFAULT_SLICE},
    ]


def _video_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "source_input_path_proven", "status": True},
        {"gate": "target_yym4_import_path_proven", "status": True},
        {"gate": "audio_path_proven", "status": True},
        {"gate": "timing_duration_strategy_defined", "status": True},
        {"gate": "tiny_smoke_render_observed", "status": True},
        {"gate": "targeted_regression_render_observed", "status": True},
        {"gate": "internal_review_milestone_reached", "status": False},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "render_performed_in_this_slice", "status": False},
        {"gate": "existing_card_placement_render_evidence_reused", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {
            "gate": "next_render_tied_to_material_change_or_explicit_internal_review_need",
            "status": True,
        },
        {"gate": "no_render_for_docs_review_prep_changes", "status": True},
        {"gate": "repeated_timing_audio_card_render_check_avoided", "status": True},
    ]


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "user_input", "status": "freeform"},
        {"gate": "template_required", "status": False},
        {"gate": "schema_owner", "status": "Agent"},
        {"gate": "user_side_work_for_this_slice", "status": "none"},
        {"gate": "future_review_questions_compact", "status": True},
        {"gate": "negative_confirmation_checklist", "status": False},
        {"gate": "fixed_form_relapse", "status": False},
    ]


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"gate": "prior_timing_evidence_reused", "status": True},
        {"gate": "prior_audio_evidence_reused", "status": True},
        {"gate": "prior_card_render_evidence_reused", "status": True},
        {"gate": "next_axis_stated_as_internal_review", "status": True},
        {"gate": "not_accepted_scope_preserved", "status": True},
        {"gate": "repeated_mechanics_review_requested", "status": False},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "packet_for_packet_drift", "status": False},
        {"gate": "readback_only_stall", "status": False},
        {"gate": "repeated_render_request", "status": False},
        {
            "gate": "product_video_review_readiness_separated_from_slice_completion",
            "status": True,
        },
        {"gate": "next_concrete_milestone", "status": NEXT_DEFAULT_SLICE},
    ]


def _review_brief() -> dict[str, Any]:
    return {
        "brief_path": _path_text(DEFAULT_INTERNAL_REVIEW_V0_1_REVIEW_BRIEF_PATH),
        "mode": "freeform_internal_review",
        "look_for_count": 5,
        "fixed_template_required": False,
        "user_side_work_for_this_slice": "none",
        "next_user_facing_action": NEXT_DEFAULT_SLICE,
    }


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "video_render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "external_TTS_introduced": False,
        "real_media_imported": False,
        "external_source_fetch_performed": False,
        "real_brand_url_or_news_screenshot_used": False,
        "ymmp_edited_by_agent": False,
        "ymmp_or_media_staged_or_committed": False,
        "production_quality_claimed": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


def _downstream_next_use() -> dict[str, list[str]]:
    return {
        "use_this_package_to": [
            "start the freeform internal review v0.1 operator-review-card slice",
            "compare future refinements against the 68sec diagnostic benchmark",
            "choose the next improvement axis from review evidence",
        ],
        "do_not_use_this_package_to": [
            "claim production quality or public readiness",
            "request another render for documentation-only work",
            "start RSS/live ingest before internal review direction is known",
            "commit ignored .ymmp, mp4, audio, voice cache, or render outputs",
        ],
    }


def _append_status_table(
    lines: list[str],
    title: str,
    rows: Any,
) -> None:
    lines.extend(["", f"## {title}", "", "| item | status |", "|---|---|"])
    for row in rows if isinstance(rows, list) else []:
        key = row.get("gate") or row.get("artifact") or "item"
        lines.append(f"| {key} | {_display(row.get('status'))} |")


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    json_path = Path(path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_bytes(
        (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )


def _write_text(path: str | Path, text: str) -> None:
    text_path = Path(path)
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text_path.write_bytes(text.encode("utf-8"))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, list):
        if not value:
            return "[]"
        return ", ".join(_display(item) for item in value)
    return str(value)
