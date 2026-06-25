"""Result readback for the newsroom card-placement render smoke.

This module records the user freeform card-placement render observation as
repo evidence. It does not launch YMM4, render, edit .ymmp, generate
audio/TTS, import media, or approve production use.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH,
)
from src.pipeline.newsroom_yym4_card_asset_placement_probe import (
    DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH,
    DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH,
)
from src.pipeline.newsroom_ymmp_timing_patch_render_smoke_result_readback import (
    DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH,
)


CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION = (
    "newsroom_card_placement_render_smoke_result_readback.v1"
)
CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_ID = (
    "newsroom_card_placement_render_smoke_result_readback_v1_2026_06_25"
)
DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "card_placement_render_smoke_result_readback_v1.json"
)
DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_V1_2026-06-25.md"
)
DEFAULT_CARD_PLACEMENT_RENDER_OUTPUT_LOCAL_PATH = Path(
    "_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.mp4"
)

NEXT_DEFAULT_SLICE = "newsroom-internal-review-v0.1-prep"
INTERNAL_REVIEW_RENDER_PACKAGE_SLICE = (
    "newsroom-internal-review-v0.1-render-package-v1"
)
RETENTION_POLICY_SLICE = "newsroom-render-output-retention-policy-v1"
RSS_DRY_RUN_PLAN_SLICE = "newsroom-rss-dry-run-integration-plan-v1"

USER_OBSERVATION_SUMMARY = (
    "The user confirmed the card-placement diagnostic video rendered as "
    "diagnostic_bound_speaker_probe_card_placement_v1.mp4, is about 1 minute "
    "8 seconds long, completed in roughly 30 seconds, and shows no visible "
    "element breakage."
)


def build_default_newsroom_card_placement_render_smoke_result_readback(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed card-placement render smoke result readback."""
    base = Path(root) if root is not None else Path(".")
    card_placement_probe = load_json_object(
        base / DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH
    )
    visual_card_bridge = load_json_object(base / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH)
    timing_render_result = load_json_object(
        base / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    render_output_path = DEFAULT_CARD_PLACEMENT_RENDER_OUTPUT_LOCAL_PATH
    card_placement_ymmp_path = DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH
    return build_newsroom_card_placement_render_smoke_result_readback(
        card_placement_probe,
        visual_card_bridge,
        timing_render_result,
        source_card_placement_probe_path=(
            DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH
        ),
        source_visual_card_bridge_path=DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH,
        source_timing_patch_render_result_path=(
            DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        render_output_path=render_output_path,
        render_output_exists=(base / render_output_path).exists(),
        card_placement_ymmp_path=card_placement_ymmp_path,
        card_placement_ymmp_exists=(base / card_placement_ymmp_path).exists(),
        root=base,
    )


def write_default_newsroom_card_placement_render_smoke_result_readback_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write JSON and human-readable card-placement render smoke readback."""
    base = Path(root) if root is not None else Path(".")
    readback = build_default_newsroom_card_placement_render_smoke_result_readback(
        root=base
    )
    _write_json(
        base / DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH,
        readback,
    )
    _write_text(
        base / DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_DOC_PATH,
        render_newsroom_card_placement_render_smoke_result_readback_markdown(
            readback
        ),
    )
    return readback


def build_newsroom_card_placement_render_smoke_result_readback(
    card_placement_probe: dict[str, Any],
    visual_card_bridge: dict[str, Any],
    timing_render_result: dict[str, Any],
    *,
    source_card_placement_probe_path: str | Path,
    source_visual_card_bridge_path: str | Path,
    source_timing_patch_render_result_path: str | Path,
    render_output_path: str | Path,
    render_output_exists: bool,
    card_placement_ymmp_path: str | Path,
    card_placement_ymmp_exists: bool,
    root: str | Path,
) -> dict[str, Any]:
    """Build a diagnostic-only result readback from the supplied observation."""
    normalized_result = _normalized_render_result()
    source_validation = _source_validation(
        card_placement_probe,
        visual_card_bridge,
        timing_render_result,
        normalized_result,
        render_output_exists=render_output_exists,
        card_placement_ymmp_exists=card_placement_ymmp_exists,
    )
    card_observations = _card_observations(card_placement_probe)

    return {
        "artifact_id": CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_ID,
        "readback_id": CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_ID,
        "schema_version": CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "observation_source": "user_freeform_with_screenshot_support",
        "result_status": "pass",
        "identity": {
            "readback_id": CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_ID,
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
            "observation_source": "user_freeform_with_screenshot_support",
            "production_status": "diagnostic_only",
            "result_status": "pass",
        },
        "source_validation": source_validation,
        "operator_freeform_observation": _operator_freeform_observation(),
        "screenshot_supported_observation": _screenshot_supported_observation(),
        "normalized_render_result": normalized_result,
        "screenshot_supported_card_observations": card_observations,
        "accepted_scope": _accepted_scope(),
        "not_accepted_scope": _not_accepted_scope(),
        "readiness_separation": _readiness_separation(),
        "render_gate_carry_forward": _render_gate_carry_forward(),
        "recommended_next_slices": _recommended_next_slices(),
        "implementation_principle_for_next_lane": (
            _implementation_principle_for_next_lane()
        ),
        "goal_stack": _goal_stack(),
        "completion_matrix": _completion_matrix(),
        "artifact_readiness": _artifact_readiness(),
        "video_readiness": _video_readiness(),
        "visual_readiness": _visual_readiness(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(),
        "local_artifact_status": _local_artifact_status(
            Path(root),
            render_output_path=Path(render_output_path),
            card_placement_ymmp_path=Path(card_placement_ymmp_path),
            render_output_exists=render_output_exists,
            card_placement_ymmp_exists=card_placement_ymmp_exists,
        ),
        "boundaries": _boundaries(),
        "downstream_next_use": _downstream_next_use(),
    }


def render_newsroom_card_placement_render_smoke_result_readback_markdown(
    readback: dict[str, Any],
) -> str:
    """Render a human-readable card-placement render smoke readback."""
    lines = [
        "# Newsroom Card Placement Render Smoke Result Readback v1",
        "",
        f"artifact_id: {readback.get('artifact_id')}",
        f"readback_id: {readback.get('readback_id')}",
        f"schema_version: {readback.get('schema_version')}",
        f"review_status: {readback.get('review_status')}",
        f"production_status: {readback.get('production_status')}",
        f"result_status: {readback.get('result_status')}",
        "diagnostic_only: true",
        "",
        "## Identity",
        "",
    ]
    for key, value in _dict(readback.get("identity")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Source Validation", ""])
    for key, value in _dict(readback.get("source_validation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Operator Observation", ""])
    for key, value in _dict(readback.get("operator_freeform_observation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Screenshot-Supported Observation", ""])
    for key, value in _dict(readback.get("screenshot_supported_observation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Normalized Render Result", ""])
    for key, value in _dict(readback.get("normalized_render_result")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Card Observations",
            "",
            "| card | visible | timing | mapping | integrity |",
            "|---:|---|---|---|---|",
        ]
    )
    for row in readback.get("screenshot_supported_card_observations", []):
        lines.append(
            "| "
            f"{row.get('card_index')} | "
            f"{_display(row.get('visible_status'))} | "
            f"{row.get('observed_time_region')} | "
            f"{row.get('expected_mapping_source')} | "
            f"{row.get('visual_integrity')} |"
        )

    lines.extend(["", "## Accepted Scope", ""])
    for key, value in _dict(readback.get("accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(readback.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Readiness Separation", ""])
    for key, value in _dict(readback.get("readiness_separation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Render Gate Carry-Forward", ""])
    for key, value in _dict(readback.get("render_gate_carry_forward")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Recommended Next Slices",
            "",
            "| slice | timing | reason |",
            "|---|---|---|",
        ]
    )
    for row in readback.get("recommended_next_slices", []):
        lines.append(
            "| "
            f"{row.get('slice')} | "
            f"{row.get('timing')} | "
            f"{row.get('reason')} |"
        )

    lines.extend(
        [
            "",
            "## Goal Stack",
            "",
            "| level | goal | success signal | contribution |",
            "|---|---|---|---|",
        ]
    )
    for row in readback.get("goal_stack", []):
        lines.append(
            "| "
            f"{row.get('level')} | "
            f"{row.get('goal')} | "
            f"{row.get('success_signal')} | "
            f"{row.get('contribution')} |"
        )

    _append_status_table(lines, "Completion Matrix", readback.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", readback.get("artifact_readiness"))
    _append_status_table(lines, "Video Readiness", readback.get("video_readiness"))
    _append_status_table(lines, "Visual Readiness", readback.get("visual_readiness"))
    _append_status_table(
        lines, "Render Gate Hygiene", readback.get("render_gate_hygiene")
    )
    _append_status_table(
        lines, "Human Burden Hygiene", readback.get("human_burden_hygiene")
    )
    _append_status_table(
        lines, "Review Non-Redundancy", readback.get("review_non_redundancy")
    )
    _append_status_table(lines, "Inertia Check", readback.get("inertia_check"))

    lines.extend(["", "## Implementation Principle", ""])
    for item in readback.get("implementation_principle_for_next_lane", []):
        lines.append(f"- {item}")

    lines.extend(["", "## Boundary", ""])
    for key, value in _dict(readback.get("boundaries")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This readback consumes the user card-placement render observation once "
            "and closes the diagnostic visual placement smoke. It does not approve "
            "production visual quality, public use, final packaging, real newsroom "
            "content, or additional render loops for documentation-only changes.",
            "",
        ]
    )
    return "\n".join(lines)


def _normalized_render_result() -> dict[str, Any]:
    return {
        "render_smoke_result": "pass",
        "yym4_opened_card_placement_project": True,
        "render_completed": True,
        "output_video_observed": True,
        "output_filename_observed": (
            "diagnostic_bound_speaker_probe_card_placement_v1.mp4"
        ),
        "output_duration_observed": "00:01:08",
        "output_duration_sec": 68,
        "expected_duration_sec": 68,
        "duration_matches_timing_patch": True,
        "render_time_approx_sec": 30,
        "card_assets_visible": True,
        "card_count_visible": 4,
        "dialogue_items_visible": True,
        "dialogue_item_count_observed": 4,
        "visual_card_integrity": "pass",
        "timing_preservation_regression_reported": False,
        "native_audio_regression_reported": False,
        "card_placement_effective_in_render": True,
        "production_visual_quality_accepted": False,
        "production_pacing_accepted": False,
        "public_video_ready": False,
        "classification": "card_placement_render_smoke_pass",
    }


def _source_validation(
    card_placement_probe: dict[str, Any],
    visual_card_bridge: dict[str, Any],
    timing_render_result: dict[str, Any],
    normalized_result: dict[str, Any],
    *,
    render_output_exists: bool,
    card_placement_ymmp_exists: bool,
) -> dict[str, Any]:
    errors: list[str] = []
    structural_result = _dict(card_placement_probe.get("structural_result"))
    prior_normalized = _dict(timing_render_result.get("normalized_render_result"))
    if card_placement_probe.get("probe_status") != "placed_structurally":
        errors.append("CARD_PLACEMENT_PROBE_NOT_STRUCTURAL_PASS")
    if structural_result.get("placement_structural_readback_status") != "pass":
        errors.append("CARD_PLACEMENT_STRUCTURAL_READBACK_NOT_PASS")
    if visual_card_bridge.get("visual_status") != "asset_bridge_created":
        errors.append("VISUAL_CARD_BRIDGE_NOT_READY")
    if timing_render_result.get("result_status") != "pass":
        errors.append("PRIOR_TIMING_RENDER_RESULT_NOT_PASS")
    if prior_normalized.get("output_duration_sec") != 68:
        errors.append("PRIOR_TIMING_RENDER_NOT_68_SEC")
    if normalized_result.get("output_duration_sec") != 68:
        errors.append("CURRENT_RENDER_NOT_68_SEC")
    if normalized_result.get("card_count_visible") != 4:
        errors.append("VISIBLE_CARD_COUNT_NOT_4")
    if len(_list(card_placement_probe.get("source_assets"))) != 4:
        errors.append("SOURCE_CARD_ASSET_COUNT_NOT_4")
    if not render_output_exists:
        errors.append("LOCAL_RENDER_OUTPUT_NOT_PRESENT_AT_READBACK")
    if not card_placement_ymmp_exists:
        errors.append("LOCAL_CARD_PLACEMENT_YMMP_NOT_PRESENT_AT_READBACK")

    return {
        "status": "passed" if not errors else "blocked",
        "errors": errors,
        "source_card_placement_probe_id": card_placement_probe.get("probe_id"),
        "source_card_placement_probe_status": card_placement_probe.get("probe_status"),
        "source_visual_card_bridge_id": visual_card_bridge.get("bridge_id"),
        "source_timing_patch_render_result_id": timing_render_result.get("readback_id"),
        "source_timing_patch_render_result": timing_render_result.get("result_status"),
        "prior_duration_sec": prior_normalized.get("output_duration_sec"),
        "prior_native_audio_present": prior_normalized.get("native_audio_present"),
        "card_asset_count": len(_list(card_placement_probe.get("source_assets"))),
        "render_output_exists_at_generation": render_output_exists,
        "card_placement_ymmp_exists_at_generation": card_placement_ymmp_exists,
        "canonical_speaker": "yukkuri_reimu",
        "canonical_speaker_unicode_escape": (
            "\\u3086\\u3063\\u304f\\u308a\\u970a\\u5922"
        ),
    }


def _operator_freeform_observation() -> dict[str, Any]:
    return {
        "input_mode": "freeform",
        "summary": USER_OBSERVATION_SUMMARY,
        "reported_duration": "about 1 minute 8 seconds",
        "reported_render_time_approx_sec": 30,
        "reported_output_file": "diagnostic_bound_speaker_probe_card_placement_v1.mp4",
        "reported_visual_breakage": False,
        "fixed_result_template_requested": False,
        "manual_observation_re_requested": False,
    }


def _screenshot_supported_observation() -> dict[str, Any]:
    return {
        "yym4_version_observed": "4.53.0.6",
        "project_name_observed": "diagnostic_bound_speaker_probe_card_placement_v1",
        "yym4_preview_project_duration": "00:01:08.00",
        "dialogue_items_remaining_on_timeline": 4,
        "cards_visible": ["Card 1/4", "Card 2/4", "Card 3/4", "Card 4/4"],
        "card_asset_mode_observed": "external_png_card_asset",
        "preview_surface_elements_observed": [
            "title",
            "chips",
            "source caption",
            "subtitle-safe reserve",
        ],
        "output_file_name": "diagnostic_bound_speaker_probe_card_placement_v1.mp4",
        "render_completed_reported": True,
        "render_time_approx_sec": 30,
        "visible_element_breakage_reported": False,
        "audio_loss_reported": False,
        "subtitle_or_dialogue_loss_reported": False,
        "media_file_committed": False,
    }


def _card_observations(
    card_placement_probe: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, asset in enumerate(_list(card_placement_probe.get("source_assets")), start=1):
        rows.append(
            {
                "card_index": index,
                "visible_status": True,
                "observed_time_region": "unknown",
                "expected_mapping_source": asset.get("card_id"),
                "expected_dialogue_or_caption": asset.get("mapped_dialogue_text"),
                "expected_start_sec": asset.get("intended_start_sec"),
                "expected_end_sec": asset.get("intended_end_sec"),
                "visual_integrity": "pass",
                "notes": [
                    "diagnostic fake/review-only card",
                    "no real brand / URL / production claim",
                ],
            }
        )
    return rows


def _accepted_scope() -> dict[str, bool]:
    return {
        "card_placement_ymmp_can_be_opened_and_rendered_in_current_yym4_environment": True,
        "output_remains_approximately_68_sec": True,
        "four_visual_card_assets_are_visible": True,
        "existing_dialogue_timeline_remains_visible": True,
        "no_obvious_visual_element_breakage_reported": True,
        "diagnostic_visual_placement_smoke_passes": True,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_visual_quality": False,
        "final_design_system": False,
        "final_narration_script_density": False,
        "public_video_readiness": False,
        "real_newsroom_visuals": False,
        "real_content_readiness": False,
        "production_approval": False,
        "final_export_packaging": False,
        "publication_readiness": False,
    }


def _readiness_separation() -> dict[str, Any]:
    return {
        "slice_completion": "pass_for_this_readback",
        "video_readiness_progress": "6/7",
        "video_readiness_current": "card placement render smoke observed",
        "video_readiness_next_missing_gate": "internal review v0.1 milestone",
        "visual_readiness_progress": "7/7",
        "visual_readiness_current": "post-placement render reviewed at diagnostic level",
        "production_readiness": "low_diagnostic_only",
        "production_readiness_reason": (
            "The observation proves diagnostic card visibility only; production "
            "visual quality, real content, packaging, and publication stay outside scope."
        ),
        "next_default_slice": NEXT_DEFAULT_SLICE,
    }


def _render_gate_carry_forward() -> dict[str, Any]:
    return {
        "current_render_observation_consumed_once": True,
        "new_render_in_this_slice": False,
        "YMM4_launched_by_agent": False,
        "render_audio_or_tts_created_by_agent": False,
        "render_gate": "milestone_gated_not_docs_gated",
        "next_render_allowed_after": [
            "internal review v0.1 milestone",
            "material visual/timing/audio surface change",
        ],
        "do_not_render_again_for": [
            "docs changes",
            "readback changes",
            "policy-only changes",
        ],
        "repeated_timing_audio_render_or_card_check_requested": False,
    }


def _recommended_next_slices() -> list[dict[str, str]]:
    return [
        {
            "slice": NEXT_DEFAULT_SLICE,
            "timing": "recommended_next_default",
            "reason": (
                "timing, audio, render, and card placement axes now pass at "
                "diagnostic level; the next value is internal review prep"
            ),
        },
        {
            "slice": INTERNAL_REVIEW_RENDER_PACKAGE_SLICE,
            "timing": "after_internal_review_prep_if_needed",
            "reason": "package the current diagnostic surface as the review milestone",
        },
        {
            "slice": RETENTION_POLICY_SLICE,
            "timing": "only_if_output_artifacts_need_retention",
            "reason": "render outputs remain ignored unless a retention gate opens",
        },
        {
            "slice": RSS_DRY_RUN_PLAN_SLICE,
            "timing": "later_not_immediate",
            "reason": "RSS dry-run planning should wait until internal review direction is set",
        },
    ]


def _implementation_principle_for_next_lane() -> list[str]:
    return [
        "Preserve the YMM4 native audio path.",
        "Preserve the external card asset pipeline.",
        "Avoid direct YMM4 card object graph reconstruction.",
        "Keep .ymmp mutation limited to ignored local copies.",
        "Render only at internal review milestone or material surface change.",
    ]


def _goal_stack() -> list[dict[str, str]]:
    return [
        {
            "level": "Immediate",
            "goal": "Record card placement render smoke result",
            "success_signal": "JSON/doc normalize 68sec render with cards visible and no breakage",
            "contribution": "closes visual placement smoke evidence",
        },
        {
            "level": "Short-term",
            "goal": "Prepare internal review v0.1",
            "success_signal": "current diagnostic video can be packaged as review milestone",
            "contribution": "moves from mechanics proof to reviewable surface",
        },
        {
            "level": "Mid-term",
            "goal": "Stabilize visual card bridge",
            "success_signal": "external assets + YMM4 placement + render evidence are all present",
            "contribution": "avoids fragile direct .ymmp card construction",
        },
        {
            "level": "Long-term",
            "goal": "Support Newsroom-to-video automation",
            "success_signal": (
                "future content packets can drive script/audio/timing/cards/render repeatably"
            ),
            "contribution": "reduces manual assembly",
        },
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "current_repo_state_verified", "status": True},
        {"gate": "card_placement_source_package_inspected", "status": True},
        {"gate": "user_freeform_observation_normalized", "status": True},
        {"gate": "result_readback_json_doc_created", "status": True},
        {"gate": "readiness_separation_updated", "status": True},
        {
            "gate": "narrow_commit_created_and_pushed_if_push_gate_passes",
            "status": "pending_until_git_gate",
        },
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"artifact": "result_readback_json", "status": "present"},
        {"artifact": "human_readback", "status": "present"},
        {"artifact": "normalized_render_result", "status": "present"},
        {"artifact": "accepted_not_accepted_scopes", "status": "present"},
        {"artifact": "render_gate_carry_forward", "status": "present"},
        {"artifact": "downstream_next_use", "status": "present"},
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


def _visual_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "visual_card_concept_selected", "status": True},
        {"gate": "external_card_assets_generated", "status": True},
        {"gate": "preview_contact_sheet_available", "status": True},
        {"gate": "assets_mapped_to_timeline_caption_units", "status": True},
        {"gate": "yym4_placement_contract_defined", "status": True},
        {"gate": "yym4_placement_proof_observed", "status": True},
        {"gate": "post_placement_render_reviewed", "status": True},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "render_performed_by_agent_in_this_slice", "status": False},
        {"gate": "existing_user_render_observation_consumed_once", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {"gate": "next_render_tied_to_internal_review_or_material_change", "status": True},
        {"gate": "no_render_for_docs_readback_changes", "status": True},
        {"gate": "repeated_timing_audio_render_card_check_avoided", "status": True},
    ]


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "user_input", "status": "freeform"},
        {"gate": "template_required", "status": False},
        {"gate": "schema_owner", "status": "Agent"},
        {"gate": "user_side_work", "status": "none"},
        {"gate": "future_look_for_points_max", "status": 3},
        {"gate": "negative_confirmation_checklist", "status": False},
        {"gate": "fixed_form_relapse", "status": False},
    ]


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"gate": "prior_timing_proof_reused", "status": True},
        {"gate": "prior_audio_evidence_reused", "status": True},
        {"gate": "prior_visual_placement_proof_reused", "status": True},
        {"gate": "current_render_observation_consumed_once", "status": True},
        {"gate": "next_axis_stated_as_internal_review_prep", "status": True},
        {"gate": "not_accepted_scope_preserved", "status": True},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "packet_for_packet_drift", "status": False},
        {"gate": "readback_only_stall", "status": False},
        {"gate": "repeated_render_request", "status": False},
        {
            "gate": "product_video_visual_readiness_separated_from_slice_completion",
            "status": True,
        },
        {"gate": "next_concrete_milestone", "status": NEXT_DEFAULT_SLICE},
    ]


def _local_artifact_status(
    root: Path,
    *,
    render_output_path: Path,
    card_placement_ymmp_path: Path,
    render_output_exists: bool,
    card_placement_ymmp_exists: bool,
) -> dict[str, Any]:
    return {
        "render_output_local_path": _path_text(render_output_path),
        "card_placement_ymmp_local_path": _path_text(card_placement_ymmp_path),
        "render_output_exists_at_readback_generation": render_output_exists,
        "card_placement_ymmp_exists_at_readback_generation": card_placement_ymmp_exists,
        "render_output_staged": _git_has_output(
            root, ["diff", "--cached", "--name-only", "--", render_output_path.as_posix()]
        ),
        "render_output_committed": _git_has_output(
            root, ["ls-files", "--", render_output_path.as_posix()]
        ),
        "render_output_ignored": _git_returncode_zero(
            root, ["check-ignore", "-q", "--", render_output_path.as_posix()]
        ),
        "card_placement_ymmp_staged": _git_has_output(
            root,
            ["diff", "--cached", "--name-only", "--", card_placement_ymmp_path.as_posix()],
        ),
        "card_placement_ymmp_committed": _git_has_output(
            root, ["ls-files", "--", card_placement_ymmp_path.as_posix()]
        ),
        "card_placement_ymmp_ignored": _git_returncode_zero(
            root, ["check-ignore", "-q", "--", card_placement_ymmp_path.as_posix()]
        ),
    }


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_created_by_agent": False,
        "video_render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "external_TTS_introduced": False,
        "real_media_imported": False,
        "real_source_fetch_performed": False,
        "ymmp_edited_by_agent": False,
        "ymmp_or_media_staged_or_committed": False,
        "render_output_staged_or_committed": False,
        "production_visual_quality_accepted": False,
        "production_approval": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


def _downstream_next_use() -> dict[str, list[str]]:
    return {
        "use_this_readback_to": [
            "prepare newsroom-internal-review-v0.1-prep",
            "carry diagnostic card placement render evidence without another render loop",
            "preserve the native YMM4 audio and external card asset pipeline",
        ],
        "do_not_use_this_readback_to": [
            "claim production visual quality",
            "claim public video readiness",
            "commit ignored .ymmp or render outputs",
            "introduce external TTS or real media",
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


def _git_has_output(root: Path, args: list[str]) -> bool:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return bool(result.stdout.strip())


def _git_returncode_zero(root: Path, args: list[str]) -> bool:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


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
