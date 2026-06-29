"""Record minimal integrated scene preview readback and freeze MVP animation.

This slice accepts the user-side preview as enough for a bounded background
animation accent layer. The animation-only loop stays closed here; the module
does not launch YMM4, render, produce audio/TTS output, fetch external media,
modify cards, or claim production quality.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_background_animation_minimal_integrated_scene import (
    DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_PATH,
    DEFAULT_MINIMAL_INTEGRATED_SCENE_OPERATOR_INSTRUCTION_PATH,
    DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH,
    LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH,
    MINIMAL_INTEGRATED_SCENE_PROBE_ID,
)
from src.pipeline.newsroom_background_animation_mvp_policy import (
    DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
    _not_accepted_scope,
)
from src.pipeline.newsroom_yukkuri_animation_tempo_contract import (
    _local_probe_access,
    _write_json,
    _write_text,
)


MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_ID = (
    "newsroom_background_animation_minimal_integrated_scene_preview_observation_v1_2026_06_29"
)
BACKGROUND_ANIMATION_MVP_FREEZE_ID = (
    "newsroom_background_animation_mvp_freeze_v1_2026_06_29"
)
MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_SCHEMA_VERSION = (
    "newsroom_background_animation_minimal_integrated_scene_preview_observation.v1"
)
BACKGROUND_ANIMATION_MVP_FREEZE_SCHEMA_VERSION = (
    "newsroom_background_animation_mvp_freeze.v1"
)

DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "background_animation_minimal_integrated_scene_preview_observation_v1.json"
)
DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_BACKGROUND_ANIMATION_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_V1_2026-06-29.md"
)
DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH = Path(
    "samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json"
)
DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_DOC_PATH = Path(
    "docs/verification/NEWSROOM_BACKGROUND_ANIMATION_MVP_FREEZE_V1_2026-06-29.md"
)

NEXT_AXIS_MAINLINE_PIPELINE = (
    "newsroom-minimal-animated-explanation-beat-in-mainline-pipeline-v1"
)
NEXT_AXIS_RSS_DRY_RUN_TO_ANIMATED_BEAT = (
    "newsroom-rss-dry-run-to-animated-explanation-beat-v1"
)
NEXT_AXIS_EPISODE_CAPSULE_RETURN = (
    "newsroom-animation-accent-policy-closed-return-to-episode-capsule-v1"
)

NORMALIZED_USER_OBSERVATION: dict[str, Any] = {
    "source_observation_role": "user_opened_minimal_integrated_scene_probe_preview",
    "source_probe_path": LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH.as_posix(),
    "yym4_opened": True,
    "minimal_integrated_scene_preview_observed": True,
    "expression_event_visible": True,
    "nod_after_expression_visible": True,
    "stable_pose_context": "not_negatively_reported",
    "body_forward_back_problem": "not_dominant_in_this_probe",
    "mvp_accent_layer_status": "accepted_with_boundary",
    "production_animation_quality": "not_accepted",
    "render_export_required_now": False,
    "next_axis": "animation_mvp_freeze_and_mainline_return",
}

USER_OBSERVATION_NOTES = [
    "The minimal integrated scene probe file opened successfully.",
    "The scene showed an expression change.",
    "After the expression change, the character performed a nod-like motion.",
    "This is sufficient for MVP accent-layer acceptance with boundaries.",
]

ANIMATION_ACCENT_POLICY: dict[str, Any] = {
    "policy_status": "frozen_for_mvp_accent_layer",
    "background_animation_role": "accent_support_layer",
    "may_reduce_static_card_fatigue": True,
    "must_not_become_main_deliverable": True,
    "future_change_rule": (
        "Future animation changes require an integrated scene or production "
        "blocker, not primitive preference."
    ),
    "allowed": [
        "stable_pose",
        "one_expression_event_tied_to_scene_beat",
        "one_short_nod_or_reaction_after_expression_event",
        "return_to_stable_pose",
    ],
    "disabled_by_default": [
        "body_forward_back_movement",
        "repeated_nodding",
        "mechanical_expression_cycling",
        "speech_balloons",
        "full_chaban_scene",
        "animation_only_probe_loops",
        "tempo_only_probe_loops",
    ],
}

MAINLINE_RETURN_PLAN: dict[str, Any] = {
    "selected_next_axis": NEXT_AXIS_MAINLINE_PIPELINE,
    "preferred_default": NEXT_AXIS_MAINLINE_PIPELINE,
    "reason": (
        "The minimal accent layer is accepted with boundary, so the next value "
        "proof should attach this policy to a real explanation beat or YMM4 "
        "scene route instead of tuning primitives."
    ),
    "alternates": [
        {
            "axis": NEXT_AXIS_RSS_DRY_RUN_TO_ANIMATED_BEAT,
            "use_when": "the project needs topic/RSS dry-run material before scene attachment",
        },
        {
            "axis": NEXT_AXIS_EPISODE_CAPSULE_RETURN,
            "use_when": "animation should be treated as closed documentation while episode production resumes",
        },
    ],
}


def write_default_newsroom_background_animation_mvp_freeze_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    observation = build_default_minimal_integrated_scene_preview_observation(root=base)
    freeze = build_default_background_animation_mvp_freeze(root=base)
    _write_json(base / DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_PATH, observation)
    _write_text(
        base / DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_DOC_PATH,
        render_minimal_integrated_scene_preview_observation_markdown(observation),
    )
    _write_json(base / DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH, freeze)
    _write_text(
        base / DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_DOC_PATH,
        render_background_animation_mvp_freeze_markdown(freeze),
    )
    return {
        "minimal_integrated_scene_preview_observation": observation,
        "background_animation_mvp_freeze": freeze,
    }


def build_default_minimal_integrated_scene_preview_observation(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    access = _local_probe_access(
        base,
        LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH,
        "local_ignored_minimal_integrated_scene_probe",
    )
    return {
        "artifact_id": MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_ID,
        "observation_id": MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_ID,
        "schema_version": MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_context": _source_context(base),
        "local_probe_access": access,
        "user_observation_notes": USER_OBSERVATION_NOTES,
        "normalized_user_observation": NORMALIZED_USER_OBSERVATION,
        "mvp_acceptance_judgment": {
            "status": "accepted_with_boundary",
            "reason": (
                "The user saw the integrated expression event and the following "
                "nod-like motion in the actual minimal scene probe."
            ),
            "not_production_quality": True,
            "no_more_primitive_tuning": True,
        },
        "render_export_required_now": False,
        "not_accepted_scope": _not_accepted_scope_with_full_chaban(),
        "boundaries": _boundaries(),
    }


def build_default_background_animation_mvp_freeze(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    observation = build_default_minimal_integrated_scene_preview_observation(root=base)
    return {
        "artifact_id": BACKGROUND_ANIMATION_MVP_FREEZE_ID,
        "freeze_id": BACKGROUND_ANIMATION_MVP_FREEZE_ID,
        "schema_version": BACKGROUND_ANIMATION_MVP_FREEZE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_context": _source_context(base),
        "source_preview_observation_path": DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_PATH.as_posix(),
        "mvp_freeze_decision": {
            "status": "freeze_mvp_accent_layer",
            "mvp_accent_layer_status": "accepted_with_boundary",
            "primitive_loop_status": "closed",
            "animation_only_probe_loop_status": "closed",
            "tempo_only_probe_loop_status": "closed",
            "mainline_return_required": True,
        },
        "animation_accent_policy": ANIMATION_ACCENT_POLICY,
        "mainline_return_plan": MAINLINE_RETURN_PLAN,
        "business_goal_outcome_contract": _business_goal_outcome_contract(observation),
        "not_accepted_scope": _not_accepted_scope_with_full_chaban(),
        "boundaries": _boundaries(),
        "inertia_check": _inertia_check(),
    }


def render_minimal_integrated_scene_preview_observation_markdown(
    payload: dict[str, Any],
) -> str:
    lines = [
        "# Newsroom Background Animation Minimal Integrated Scene Preview Observation v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "Local Probe Access", payload.get("local_probe_access"))
    _append_mapping(lines, "Normalized User Observation", payload.get("normalized_user_observation"))
    _append_mapping(lines, "MVP Acceptance Judgment", payload.get("mvp_acceptance_judgment"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This readback records a user-side preview observation only. It freezes "
        "the MVP accent layer but does not render, launch YMM4 from the agent, "
        "stage media, or accept production/public quality."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_background_animation_mvp_freeze_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Background Animation MVP Freeze v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "MVP Freeze Decision", payload.get("mvp_freeze_decision"))
    _append_mapping(lines, "Animation Accent Policy", payload.get("animation_accent_policy"))
    _append_mapping(lines, "Mainline Return Plan", payload.get("mainline_return_plan"))
    _append_mapping(
        lines,
        "Business Goal Outcome Contract",
        payload.get("business_goal_outcome_contract"),
    )
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "The MVP animation accent policy is closed for now. Future work should "
        "attach it to mainline video integration, not reopen primitive-only "
        "animation preference loops."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _source_context(base: Path) -> dict[str, Any]:
    return {
        "source_mvp_policy_path": DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH.as_posix(),
        "source_minimal_integrated_scene_contract_path": (
            DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_PATH.as_posix()
        ),
        "source_minimal_integrated_scene_probe_readback_path": (
            DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH.as_posix()
        ),
        "source_operator_instruction_path": (
            DEFAULT_MINIMAL_INTEGRATED_SCENE_OPERATOR_INSTRUCTION_PATH.as_posix()
        ),
        "source_probe_id": MINIMAL_INTEGRATED_SCENE_PROBE_ID,
        "source_probe_path": LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH.as_posix(),
        "repo_root": str(base.resolve()),
    }


def _business_goal_outcome_contract(observation: dict[str, Any]) -> dict[str, Any]:
    accepted = observation["normalized_user_observation"]["mvp_accent_layer_status"] == (
        "accepted_with_boundary"
    )
    return {
        "problem_clear": {
            "status": True,
            "rationale": "this closes primitive-only animation tuning after an integrated preview passed the MVP accent signal",
        },
        "offer_clear": {
            "status": True,
            "rationale": "animation adds a small support accent: expression event plus nod after the scene beat",
        },
        "proof_clear": {
            "status": True,
            "rationale": "MVP accent acceptance is separated from production animation quality and render proof",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "production/public/order/audience acceptance and render/export proof remain false",
        },
        "next_action_clear": {
            "status": True,
            "rationale": NEXT_AXIS_MAINLINE_PIPELINE,
        },
        "visual_supports_explanation": {
            "status": "accepted_with_boundary" if accepted else "not_accepted",
            "rationale": "the visible expression event and following nod are enough for a subordinate accent layer",
        },
    }


def _not_accepted_scope_with_full_chaban() -> dict[str, bool]:
    scope = _not_accepted_scope()
    scope.update(
        {
            "full_chaban_scene": False,
            "animation_only_probe_loop": False,
            "tempo_only_probe_loop": False,
        }
    )
    return scope


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "dense_script_modified": False,
        "local_ignored_ymmp_created_in_this_slice": False,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
        "actual_order_or_audience_acceptance_claimed": False,
    }


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "no_primitive_only_animation_work", "status": True},
        {"gate": "no_animation_only_probe_loop", "status": True},
        {"gate": "no_tempo_only_probe_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "next_value_proof_returns_to_mainline", "status": NEXT_AXIS_MAINLINE_PIPELINE},
    ]


def main() -> int:
    write_default_newsroom_background_animation_mvp_freeze_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
