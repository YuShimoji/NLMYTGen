"""Record the yukkuri scene preview stop-loss and integration plan.

This slice turns the user-side scene choreography preview observation into a
planning contract. It does not create another primitive-only probe, launch
YMM4, render, produce audio/TTS output, fetch external media, modify cards, or claim
production quality.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
    _not_accepted_scope,
)
from src.pipeline.newsroom_yukkuri_animation_scene_choreography import (
    DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_PATH,
    DEFAULT_SCENE_CHOREOGRAPHY_PROBE_PATH,
    LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH,
)
from src.pipeline.newsroom_yukkuri_animation_tempo_contract import (
    _local_probe_access,
    _write_json,
    _write_text,
)


SCENE_PREVIEW_OBSERVATION_ID = (
    "newsroom_yukkuri_animation_scene_preview_observation_v1_2026_06_29"
)
BACKGROUND_ANIMATION_MVP_POLICY_ID = (
    "newsroom_background_animation_mvp_policy_v1_2026_06_29"
)
BACKGROUND_ANIMATION_INTEGRATION_PLAN_ID = (
    "newsroom_background_animation_integration_plan_v1_2026_06_29"
)

SCENE_PREVIEW_OBSERVATION_SCHEMA_VERSION = (
    "newsroom_yukkuri_animation_scene_preview_observation.v1"
)
BACKGROUND_ANIMATION_MVP_POLICY_SCHEMA_VERSION = (
    "newsroom_background_animation_mvp_policy.v1"
)
BACKGROUND_ANIMATION_INTEGRATION_PLAN_SCHEMA_VERSION = (
    "newsroom_background_animation_integration_plan.v1"
)

DEFAULT_SCENE_PREVIEW_OBSERVATION_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "yukkuri_animation_scene_preview_observation_v1.json"
)
DEFAULT_SCENE_PREVIEW_OBSERVATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_YUKKURI_ANIMATION_SCENE_PREVIEW_OBSERVATION_V1_2026-06-29.md"
)
DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH = Path(
    "samples/_probe/newsroom_handoff/background_animation_mvp_policy_v1.json"
)
DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_BACKGROUND_ANIMATION_MVP_POLICY_V1_2026-06-29.md"
)
DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_PATH = Path(
    "samples/_probe/newsroom_handoff/background_animation_integration_plan_v1.json"
)
DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_BACKGROUND_ANIMATION_INTEGRATION_PLAN_V1_2026-06-29.md"
)

NEXT_AXIS_MINIMAL_INTEGRATED_SCENE_PROBE = (
    "newsroom-background-animation-minimal-integrated-scene-probe-v1"
)
RETURN_AXIS_RSS_STORY_INTEGRATION = "newsroom-rss-dry-run-integration-plan-v1"

USER_SCENE_PREVIEW_OBSERVATION_NOTES = [
    "The scene choreography probe is not fully incoherent.",
    "Most visible animation is expression changes and nodding.",
    "Earlier forward/back movement is mostly gone.",
    "Unstable movement remains near the angry expression.",
    "Primitive-only tuning is taking too much time.",
]

NORMALIZED_SCENE_PREVIEW_OBSERVATION: dict[str, Any] = {
    "source_observation_role": "user_opened_local_scene_choreography_preview",
    "source_scene_choreography_probe_path": LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH.as_posix(),
    "yym4_opened": True,
    "scene_choreography_probe_observed": True,
    "scene_coherence": "partial",
    "primitive_feasibility": "pass",
    "expression_change_visible": True,
    "nod_visible": True,
    "body_motion_default_should_stop": True,
    "unstable_motion_near_angry_expression": "warning",
    "animation_quality_for_final": "not_accepted",
    "primitive_tuning_loop_risk": "high",
    "render_export_checked": False,
    "render_export_required_now": False,
    "next_axis": "stop_loss_and_integration_plan",
}

STOP_LOSS_POLICY: list[dict[str, Any]] = [
    {
        "rule_id": "no_more_primitive_only_iteration",
        "requirement": (
            "Do not run more primitive-only tempo, angle, or expression iteration "
            "unless an integrated scene proves a specific primitive is blocking."
        ),
        "effect": "moves the bottleneck from isolated motion tuning to one actual explanation beat",
        "default_state": "active",
    },
    {
        "rule_id": "body_forward_back_disabled_by_default",
        "requirement": "Disable body forward/back movement by default.",
        "effect": "prevents the previous unstable depth-like drift from becoming the animation baseline",
        "default_state": "active",
    },
    {
        "rule_id": "expression_changes_are_scene_events",
        "requirement": "Tie expression changes only to a scene event.",
        "effect": "keeps expression swaps from becoming a mechanical cycle",
        "default_state": "active",
    },
    {
        "rule_id": "single_nod_or_reaction_per_short_scene",
        "requirement": "Allow one nod or reaction per short scene.",
        "effect": "keeps the character readable without repeated acknowledgement loops",
        "default_state": "active",
    },
    {
        "rule_id": "speech_balloon_deferred",
        "requirement": "Defer speech balloon work.",
        "effect": "avoids opening a new visual subsystem before the movement layer is useful",
        "default_state": "active",
    },
    {
        "rule_id": "background_animation_support_layer",
        "requirement": "Treat background animation as an accent/support layer, not the main deliverable.",
        "effect": "keeps story clarity and card fatigue reduction ahead of character acting complexity",
        "default_state": "active",
    },
    {
        "rule_id": "next_proof_uses_actual_explanation_beat",
        "requirement": "Use an actual explanation beat for the next proof, not a standalone primitive demo.",
        "effect": "tests whether the animation supports a real newsroom explanation moment",
        "default_state": "active",
    },
    {
        "rule_id": "freeze_animation_if_integrated_scene_fails",
        "requirement": (
            "If the next integrated scene still feels bad, freeze animation as "
            "minimal accent and return to RSS/story integration."
        ),
        "effect": "prevents the background animation track from consuming the mainline",
        "default_state": "active",
    },
]

ALLOWED_DEFAULT_PRIMITIVES: list[dict[str, Any]] = [
    {
        "primitive_id": "stable_pose",
        "allowed_default": True,
        "constraint": "always allowed as the fallback state",
    },
    {
        "primitive_id": "one_expression_event",
        "allowed_default": True,
        "constraint": "exactly one event when the explanation beat changes emotional state",
    },
    {
        "primitive_id": "one_short_nod_or_reaction",
        "allowed_default": True,
        "constraint": "one reaction per short scene; no repeated nodding loop",
    },
    {
        "primitive_id": "small_lateral_emphasis",
        "allowed_default": "optional",
        "constraint": "only when the explanation beat gives a clear reason",
    },
]

DISABLED_BY_DEFAULT: list[dict[str, Any]] = [
    {
        "primitive_id": "repeated_nodding",
        "disabled_by_default": True,
        "reason": "it reads as mechanical agreement rather than explanation support",
    },
    {
        "primitive_id": "mechanical_expression_cycling",
        "disabled_by_default": True,
        "reason": "expression changes must be tied to a scene event",
    },
    {
        "primitive_id": "body_forward_back_movement",
        "disabled_by_default": True,
        "reason": "the latest preview still shows instability around this class of motion",
    },
    {
        "primitive_id": "complex_speech_balloons",
        "disabled_by_default": True,
        "reason": "speech balloon acceptance has not been proven and is not needed for this gate",
    },
    {
        "primitive_id": "full_chaban_scene",
        "disabled_by_default": True,
        "reason": "the product need is an accent/support layer, not a character skit rewrite",
    },
]

REVIEW_GATE: list[dict[str, Any]] = [
    {
        "gate_id": "supports_explanation",
        "question": "Does the animation support the explanation?",
        "pass_condition": "the beat is easier to follow with the accent than without it",
    },
    {
        "gate_id": "does_not_distract",
        "question": "Does it distract?",
        "pass_condition": "viewer attention remains on the newsroom explanation and card context",
    },
    {
        "gate_id": "reduces_card_fatigue",
        "question": "Does it reduce card fatigue?",
        "pass_condition": "the short accent breaks static-card monotony without becoming the subject",
    },
    {
        "gate_id": "introduces_no_confusion",
        "question": "Does it introduce confusion?",
        "pass_condition": "no movement implies the wrong direction, object, speaker, or causal claim",
    },
]

BUSINESS_GOAL_OUTCOME_CONTRACT: dict[str, dict[str, Any]] = {
    "problem_clear": {
        "status": True,
        "rationale": "the problem is over-spending on primitive tuning after partial coherence is already proven",
    },
    "offer_clear": {
        "status": True,
        "rationale": "the offer is a minimal integrated background accent, not a full skit system",
    },
    "proof_clear": {
        "status": True,
        "rationale": "the next proof is one actual explanation beat, 10-20 seconds, one preview only",
    },
    "boundary_clear": {
        "status": True,
        "rationale": "no render, no audio/TTS, no media, no card redesign, and no production claim",
    },
    "next_action_clear": {
        "status": True,
        "rationale": NEXT_AXIS_MINIMAL_INTEGRATED_SCENE_PROBE,
    },
    "visual_supports_explanation": {
        "status": "unknown_until_integrated_preview",
        "rationale": "primitive feasibility passed, but final animation quality is not accepted",
    },
}

INTEGRATED_SCENE_PROBE_SPEC: dict[str, Any] = {
    "probe_id": NEXT_AXIS_MINIMAL_INTEGRATED_SCENE_PROBE,
    "duration_sec_range": {"min": 10, "max": 20},
    "content_rule": "one actual explanation beat, not a primitive demo",
    "review_only_line": (
        "A structural shift can create short-term friction while moving long-term leverage."
    ),
    "line_status": "review_only_diagnostic_line",
    "animation_budget": {
        "stable_pose": "required",
        "expression_event_count": 1,
        "nod_or_reaction_count": 1,
        "body_forward_back_movement": "disabled_by_default",
        "small_lateral_emphasis": "optional_only_if_scene_justified",
        "speech_balloon": "deferred",
    },
    "card_overlay_policy": "minimal existing card or overlay only; no card asset redesign",
    "source_material_policy": "use a small existing diagnostic line or this review-only line",
    "output_policy": {
        "planning_slice_creates_ymmp": False,
        "later_slice_may_create_local_ignored_ymmp": "only if safe and necessary",
        "tracked_ymmp_allowed": False,
        "render_export_required": False,
    },
    "preview_policy": {
        "user_review_mode": "one_freeform_preview_only",
        "do_not_request_repeated_render": True,
        "evaluation_focus": [
            "supports explanation",
            "does not distract",
            "reduces card fatigue",
            "introduces no confusion",
        ],
    },
}


def write_default_newsroom_background_animation_mvp_policy_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    observation = build_default_scene_preview_observation(root=base)
    policy = build_default_background_animation_mvp_policy(root=base)
    plan = build_default_background_animation_integration_plan(root=base)
    _write_json(base / DEFAULT_SCENE_PREVIEW_OBSERVATION_PATH, observation)
    _write_text(
        base / DEFAULT_SCENE_PREVIEW_OBSERVATION_DOC_PATH,
        render_scene_preview_observation_markdown(observation),
    )
    _write_json(base / DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH, policy)
    _write_text(
        base / DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_DOC_PATH,
        render_background_animation_mvp_policy_markdown(policy),
    )
    _write_json(base / DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_PATH, plan)
    _write_text(
        base / DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_DOC_PATH,
        render_background_animation_integration_plan_markdown(plan),
    )
    return {
        "scene_preview_observation": observation,
        "background_animation_mvp_policy": policy,
        "background_animation_integration_plan": plan,
    }


def build_default_scene_preview_observation(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    scene_probe_access = _local_probe_access(
        base,
        LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH,
        "local_ignored_scene_choreography_probe",
    )
    return {
        "artifact_id": SCENE_PREVIEW_OBSERVATION_ID,
        "observation_id": SCENE_PREVIEW_OBSERVATION_ID,
        "schema_version": SCENE_PREVIEW_OBSERVATION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_context": {
            "source_scene_choreography_probe_path": LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH.as_posix(),
            "source_scene_choreography_probe_readback_path": DEFAULT_SCENE_CHOREOGRAPHY_PROBE_PATH.as_posix(),
            "source_scene_choreography_contract_path": DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_PATH.as_posix(),
        },
        "source_scene_choreography_probe_access": scene_probe_access,
        "user_observation_notes": USER_SCENE_PREVIEW_OBSERVATION_NOTES,
        "normalized_user_observation": NORMALIZED_SCENE_PREVIEW_OBSERVATION,
        "stop_loss_trigger": {
            "primitive_tuning_loop_risk": "high",
            "animation_quality_for_final": "not_accepted",
            "body_motion_default_should_stop": True,
            "scene_coherence": "partial",
            "primitive_feasibility": "pass",
            "decision": "stop_primitive_only_tuning_and_plan_integrated_scene",
        },
        "render_export_checked": False,
        "render_export_required_now": False,
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _planning_boundaries(),
    }


def build_default_background_animation_mvp_policy(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    return {
        "artifact_id": BACKGROUND_ANIMATION_MVP_POLICY_ID,
        "policy_id": BACKGROUND_ANIMATION_MVP_POLICY_ID,
        "schema_version": BACKGROUND_ANIMATION_MVP_POLICY_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_context": {
            "source_scene_preview_observation_path": DEFAULT_SCENE_PREVIEW_OBSERVATION_PATH.as_posix(),
            "source_scene_choreography_contract_path": DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_PATH.as_posix(),
            "source_scene_choreography_probe_readback_path": DEFAULT_SCENE_CHOREOGRAPHY_PROBE_PATH.as_posix(),
            "repo_root": str(base.resolve()),
        },
        "stop_loss_policy": STOP_LOSS_POLICY,
        "allowed_default_primitives": ALLOWED_DEFAULT_PRIMITIVES,
        "disabled_by_default": DISABLED_BY_DEFAULT,
        "review_gate": REVIEW_GATE,
        "business_goal_outcome_contract": BUSINESS_GOAL_OUTCOME_CONTRACT,
        "selected_next_axis": NEXT_AXIS_MINIMAL_INTEGRATED_SCENE_PROBE,
        "next_recommended_axis": {
            "selected": NEXT_AXIS_MINIMAL_INTEGRATED_SCENE_PROBE,
            "reason": (
                "Partial scene coherence and primitive feasibility are enough to "
                "stop isolated primitive tuning. The next useful proof is a "
                "minimal integrated explanation beat."
            ),
            "fallback_if_bad": RETURN_AXIS_RSS_STORY_INTEGRATION,
        },
        "freeze_condition": {
            "condition": "next_integrated_scene_still_feels_bad",
            "action": "freeze_animation_as_minimal_accent",
            "return_axis": RETURN_AXIS_RSS_STORY_INTEGRATION,
        },
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _planning_boundaries(),
        "inertia_check": _inertia_check(),
    }


def build_default_background_animation_integration_plan(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    return {
        "artifact_id": BACKGROUND_ANIMATION_INTEGRATION_PLAN_ID,
        "plan_id": BACKGROUND_ANIMATION_INTEGRATION_PLAN_ID,
        "schema_version": BACKGROUND_ANIMATION_INTEGRATION_PLAN_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_context": {
            "source_scene_preview_observation_path": DEFAULT_SCENE_PREVIEW_OBSERVATION_PATH.as_posix(),
            "source_mvp_policy_path": DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH.as_posix(),
            "source_scene_choreography_contract_path": DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_PATH.as_posix(),
            "repo_root": str(base.resolve()),
        },
        "selected_next_axis": NEXT_AXIS_MINIMAL_INTEGRATED_SCENE_PROBE,
        "integrated_scene_probe_spec": INTEGRATED_SCENE_PROBE_SPEC,
        "stop_loss_policy_refs": [row["rule_id"] for row in STOP_LOSS_POLICY],
        "review_gate_refs": [row["gate_id"] for row in REVIEW_GATE],
        "success_signal": {
            "status": "pending_user_freeform_preview",
            "required_readback": (
                "animation supports explanation, does not distract, reduces card "
                "fatigue, and introduces no confusion"
            ),
        },
        "failure_signal": {
            "status": "defined",
            "if_user_reports_bad_integrated_feel": "freeze_animation_as_minimal_accent",
            "return_axis": RETURN_AXIS_RSS_STORY_INTEGRATION,
        },
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _planning_boundaries(),
        "inertia_check": _inertia_check(),
    }


def render_scene_preview_observation_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Yukkuri Animation Scene Preview Observation v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(
        lines,
        "Source Scene Choreography Probe Access",
        payload.get("source_scene_choreography_probe_access"),
    )
    _append_mapping(lines, "Normalized User Observation", payload.get("normalized_user_observation"))
    _append_mapping(lines, "Stop-Loss Trigger", payload.get("stop_loss_trigger"))
    _append_mapping(
        lines,
        "Render Deferral",
        {
            "render_export_checked": payload.get("render_export_checked"),
            "render_export_required_now": payload.get("render_export_required_now"),
        },
    )
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This observation records a user-side preview readback and stop-loss trigger. "
        "It does not create a new probe, render, launch YMM4 from the agent, stage "
        "media, or accept production/public quality."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_background_animation_mvp_policy_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Background Animation MVP Policy v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_rows(
        lines,
        "Stop-Loss Policy",
        ["rule_id", "requirement", "effect", "default_state"],
        payload.get("stop_loss_policy"),
    )
    _append_rows(
        lines,
        "Allowed Default Primitives",
        ["primitive_id", "allowed_default", "constraint"],
        payload.get("allowed_default_primitives"),
    )
    _append_rows(
        lines,
        "Disabled By Default",
        ["primitive_id", "disabled_by_default", "reason"],
        payload.get("disabled_by_default"),
    )
    _append_rows(
        lines,
        "Review Gate",
        ["gate_id", "question", "pass_condition"],
        payload.get("review_gate"),
    )
    _append_mapping(lines, "Business Goal Outcome Contract", payload.get("business_goal_outcome_contract"))
    _append_mapping(lines, "Next Recommended Axis", payload.get("next_recommended_axis"))
    _append_mapping(lines, "Freeze Condition", payload.get("freeze_condition"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This policy makes background animation an explanation support layer. It "
        "does not approve a full chaban scene, speech balloon system, render, "
        "audio/TTS, production quality, or public release."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_background_animation_integration_plan_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Background Animation Integration Plan v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "Integrated Scene Probe Spec", payload.get("integrated_scene_probe_spec"))
    _append_mapping(lines, "Success Signal", payload.get("success_signal"))
    _append_mapping(lines, "Failure Signal", payload.get("failure_signal"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This is a planning artifact for a later minimal integrated scene probe. "
        "It does not create a .ymmp file in this slice and does not request a "
        "render/export pass."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _planning_boundaries() -> dict[str, bool]:
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
    }


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "remote_parity_required_before_work", "status": True},
        {"gate": "no_new_primitive_only_probe", "status": True},
        {"gate": "no_repeated_visual_proof_request", "status": True},
        {"gate": "integrated_scene_before_more_tuning", "status": True},
        {"gate": "return_to_rss_story_integration_if_bad", "status": RETURN_AXIS_RSS_STORY_INTEGRATION},
    ]


def main() -> int:
    write_default_newsroom_background_animation_mvp_policy_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
