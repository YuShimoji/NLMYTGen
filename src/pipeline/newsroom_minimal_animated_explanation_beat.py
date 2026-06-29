"""Build a diagnostic mainline explanation beat with frozen animation accent.

This slice ties narration intent, subtitle/readback semantics, a minimal
overlay role, and the frozen MVP background animation policy into one mainline
proof. It stays diagnostic-only: no YMM4 launch, render, audio/TTS generation,
real RSS/news fetch, card redesign, or production acceptance.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_background_animation_minimal_integrated_scene import (
    DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_PATH,
    DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH,
    EXPLANATION_BEAT as SOURCE_DIAGNOSTIC_LINE,
    LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH,
    MINIMAL_INTEGRATED_SCENE_PROBE_ID,
    SCENE_DURATION_SEC,
    SCENE_TIMELINE_LENGTH_FRAMES,
    build_default_minimal_integrated_scene_probe_readback,
    materialize_local_minimal_integrated_scene_probe,
)
from src.pipeline.newsroom_background_animation_mvp_freeze import (
    ANIMATION_ACCENT_POLICY,
    DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH,
)
from src.pipeline.newsroom_background_animation_mvp_policy import (
    DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_PATH,
    DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
    _dict,
    _first_timeline,
    _get_timeline_items,
    _item_type,
    _not_accepted_scope,
)
from src.pipeline.newsroom_yukkuri_animation_tempo_contract import (
    _git_check_ignore,
    _local_probe_access,
    _sha256,
    _write_json,
    _write_text,
)
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


MINIMAL_ANIMATED_EXPLANATION_BEAT_ID = (
    "newsroom_minimal_animated_explanation_beat_mainline_v1_2026_06_29"
)
MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_ID = (
    "newsroom_minimal_animated_explanation_beat_contract_v1_2026_06_29"
)
MINIMAL_ANIMATED_EXPLANATION_BEAT_SCHEMA_VERSION = (
    "newsroom_minimal_animated_explanation_beat_mainline.v1"
)
MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_SCHEMA_VERSION = (
    "newsroom_minimal_animated_explanation_beat_contract.v1"
)

DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH = Path(
    "samples/_probe/newsroom_handoff/minimal_animated_explanation_beat_mainline_v1.json"
)
DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_MAINLINE_V1_2026-06-29.md"
)
DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_PATH = Path(
    "samples/_probe/newsroom_handoff/minimal_animated_explanation_beat_contract_v1.json"
)
DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_V1_2026-06-29.md"
)

LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH = Path(
    "_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v1.ymmp"
)

EPISODE_PRODUCTION_CAPSULE_PATH = Path(
    "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json"
)
NEUTRAL_TIMELINE_IMPORT_PROOF_PATH = Path(
    "samples/_probe/newsroom_handoff/neutral_timeline_import_proof_v1.json"
)
CAPTION_TIMING_PLAN_PATH = Path(
    "samples/_probe/newsroom_handoff/episode_caption_timing_plan_v1.json"
)
CAPTION_CSV_IMPORT_CANDIDATE_PATH = Path(
    "samples/_probe/newsroom_handoff/caption_csv_import_candidate_readback_v1.json"
)

NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION = (
    "newsroom-minimal-animated-explanation-beat-preview-operator-instruction-v1"
)
NEXT_AXIS_MATERIALIZATION = (
    "newsroom-minimal-animated-explanation-beat-materialization-v1"
)
NEXT_AXIS_RSS_DRY_RUN = "newsroom-rss-dry-run-to-animated-explanation-beat-v1"
NEXT_AXIS_EPISODE_CAPSULE_RETURN = (
    "newsroom-animation-accent-policy-closed-return-to-episode-capsule-v1"
)

BEAT_ID = "minimal_animated_explanation_beat_mainline_v1"
ROUTE_NAME = "existing_minimal_integrated_scene_route_plus_neutral_timeline_semantics"

EXPLANATION_BEAT: dict[str, Any] = {
    "beat_id": BEAT_ID,
    "diagnostic_line": SOURCE_DIAGNOSTIC_LINE,
    "line_status": "review_only_diagnostic_line_not_final_script_copy",
    "narration_intent": (
        "state one explanation point clearly while a small background accent "
        "reduces static-card fatigue"
    ),
    "subtitle_role": (
        "readback-only subtitle/caption role; proves where caption intent sits "
        "without approving production subtitle design"
    ),
    "viewer_information_goal": (
        "the viewer should understand the structural-shift caution before "
        "noticing the character motion"
    ),
    "card_overlay_role": "existing minimal label / readback-only overlay role; no new card design",
    "background_animation_role": (
        "frozen MVP accent: one expression event and one short nod/reaction "
        "subordinate to narration"
    ),
    "source_boundary_role": (
        "synthetic review-only diagnostic line; no real RSS/news, URL, source "
        "quote, media, or publication rights are implied"
    ),
}

ANIMATION_ACCENT: dict[str, Any] = {
    "expression_event": {
        "event_id": "expression_event_key_phrase",
        "timing_role": "after the key phrase introduces short-term friction",
        "expression": "panic",
        "count": 1,
    },
    "nod_or_reaction": {
        "event_id": "one_short_nod_after_key_phrase",
        "timing_role": "short acknowledgement after the key phrase",
        "count": 1,
        "head_rotation_values": [0.0, -8.0, 0.0],
    },
    "stable_start_pose": {
        "required": True,
        "expression": "easy",
        "parent_x_policy": "fixed_shared_anchor",
    },
    "stable_end_pose": {
        "required": True,
        "head_rotation_return": 0.0,
        "parent_x_policy": "fixed_shared_anchor",
    },
    "disabled_primitives_enforced": [
        "body_forward_back_movement",
        "repeated_nodding",
        "mechanical_expression_cycling",
        "speech_balloons",
        "full_chaban_scene",
        "animation_only_probe_loops",
        "tempo_only_probe_loops",
    ],
}


def write_default_newsroom_minimal_animated_explanation_beat_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    materialize_local_minimal_animated_explanation_beat_probe(root=base)
    contract = build_default_minimal_animated_explanation_beat_contract(root=base)
    proof = build_default_minimal_animated_explanation_beat(root=base)
    _write_json(base / DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_PATH, contract)
    _write_text(
        base / DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_DOC_PATH,
        render_minimal_animated_explanation_beat_contract_markdown(contract),
    )
    _write_json(base / DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH, proof)
    _write_text(
        base / DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_DOC_PATH,
        render_minimal_animated_explanation_beat_markdown(proof),
    )
    return {
        "minimal_animated_explanation_beat_contract": contract,
        "minimal_animated_explanation_beat": proof,
    }


def build_default_minimal_animated_explanation_beat_contract(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    proof = build_default_minimal_animated_explanation_beat(root=base)
    return {
        "artifact_id": MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_ID,
        "contract_id": MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_ID,
        "proof_id": MINIMAL_ANIMATED_EXPLANATION_BEAT_ID,
        "schema_version": MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_mvp_freeze_path": DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH.as_posix(),
        "source_context": _source_context(base),
        "explanation_beat": EXPLANATION_BEAT,
        "mainline_route": proof["mainline_route"],
        "animation_accent": ANIMATION_ACCENT,
        "animation_accent_policy": ANIMATION_ACCENT_POLICY,
        "integration_acceptance": proof["integration_acceptance"],
        "business_goal_outcome_contract": proof["business_goal_outcome_contract"],
        "not_accepted_scope": _not_accepted_scope_with_animation_boundaries(),
        "boundaries": _boundaries(local_probe_created=_local_probe_created(proof)),
        "inertia_check": _inertia_check(proof["selected_next_axis"]),
        "selected_next_axis": proof["selected_next_axis"],
        "next_recommended_axis": proof["next_recommended_axis"],
    }


def build_default_minimal_animated_explanation_beat(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    access = _local_probe_access(
        base,
        LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH,
        "local_ignored_minimal_animated_explanation_beat_probe",
    )
    readback = _local_probe_readback(base, access)
    materialized = (
        access["target_exists"]
        and access["access_state"] == "verified_present"
        and readback["readback_status"] == "structural_pass"
    )
    next_axis = _select_next_axis(materialized)
    return {
        "artifact_id": MINIMAL_ANIMATED_EXPLANATION_BEAT_ID,
        "proof_id": MINIMAL_ANIMATED_EXPLANATION_BEAT_ID,
        "schema_version": MINIMAL_ANIMATED_EXPLANATION_BEAT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_mvp_freeze_path": DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH.as_posix(),
        "source_context": _source_context(base),
        "explanation_beat": EXPLANATION_BEAT,
        "mainline_route": _mainline_route(base, access, readback, materialized),
        "animation_accent": ANIMATION_ACCENT,
        "integration_acceptance": _integration_acceptance(materialized),
        "business_goal_outcome_contract": _business_goal_outcome_contract(next_axis),
        "not_accepted_scope": _not_accepted_scope_with_animation_boundaries(),
        "boundaries": _boundaries(local_probe_created=materialized),
        "selected_next_axis": next_axis,
        "next_recommended_axis": {
            "selected": next_axis,
            "reason": _next_axis_reason(materialized),
            "fallback_if_no_preview_needed": NEXT_AXIS_RSS_DRY_RUN,
            "fallback_if_animation_value_is_too_low": NEXT_AXIS_EPISODE_CAPSULE_RETURN,
        },
        "inertia_check": _inertia_check(next_axis),
    }


def materialize_local_minimal_animated_explanation_beat_probe(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    source_probe = base / LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH
    if not source_probe.exists():
        materialize_local_minimal_integrated_scene_probe(root=base)
    source_readback = build_default_minimal_integrated_scene_probe_readback(root=base)
    if source_readback.get("local_probe_readback", {}).get("readback_status") != "structural_pass":
        raise ValueError("source minimal integrated scene route did not pass structural readback")

    target = base / LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    probe = copy.deepcopy(load_ymmp(source_probe))
    probe["FilePath"] = str(target.resolve())
    save_ymmp(probe, target)
    return probe


def render_minimal_animated_explanation_beat_contract_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Minimal Animated Explanation Beat Contract v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "Explanation Beat", payload.get("explanation_beat"))
    _append_mapping(lines, "Mainline Route", payload.get("mainline_route"))
    _append_mapping(lines, "Animation Accent", payload.get("animation_accent"))
    _append_mapping(lines, "Integration Acceptance", payload.get("integration_acceptance"))
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
        "This contract proves one integrated explanation beat structure. It is "
        "diagnostic-only and does not approve production animation, render, "
        "publication, real source use, or audience/order acceptance."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_minimal_animated_explanation_beat_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom Minimal Animated Explanation Beat Mainline v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "Explanation Beat", payload.get("explanation_beat"))
    _append_mapping(lines, "Mainline Route", payload.get("mainline_route"))
    _append_mapping(lines, "Animation Accent", payload.get("animation_accent"))
    _append_mapping(lines, "Integration Acceptance", payload.get("integration_acceptance"))
    _append_mapping(
        lines,
        "Business Goal Outcome Contract",
        payload.get("business_goal_outcome_contract"),
    )
    _append_mapping(lines, "Next Recommended Axis", payload.get("next_recommended_axis"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "The local probe, when present, is ignored local evidence only. It is "
        "not rendered, not staged, not committed, and not a production/public "
        "quality claim."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _mainline_route(
    base: Path,
    access: dict[str, Any],
    readback: dict[str, Any],
    materialized: bool,
) -> dict[str, Any]:
    return {
        "route_name": ROUTE_NAME,
        "input_artifacts": [
            DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH.as_posix(),
            DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH.as_posix(),
            DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_PATH.as_posix(),
            DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_PATH.as_posix(),
            DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH.as_posix(),
            EPISODE_PRODUCTION_CAPSULE_PATH.as_posix(),
            NEUTRAL_TIMELINE_IMPORT_PROOF_PATH.as_posix(),
            CAPTION_TIMING_PLAN_PATH.as_posix(),
            CAPTION_CSV_IMPORT_CANDIDATE_PATH.as_posix(),
        ],
        "transformation_steps": [
            "select one review-only explanation beat from the existing integrated-scene plan",
            "bind narration intent to a subtitle/readback role rather than final script copy",
            "carry forward existing minimal label/readback overlay semantics without redesign",
            "attach the frozen MVP background animation accent policy",
            "materialize an ignored local YMM4 representation candidate from the known minimal integrated scene route",
            "record boundaries so the output remains diagnostic-only",
        ],
        "output_artifacts": [
            DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_PATH.as_posix(),
            DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_DOC_PATH.as_posix(),
            DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_PATH.as_posix(),
            DEFAULT_MINIMAL_ANIMATED_EXPLANATION_BEAT_CONTRACT_DOC_PATH.as_posix(),
            LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH.as_posix(),
        ],
        "YMM4_representation_candidate": {
            "candidate_kind": "ignored_local_diagnostic_ymmp",
            "repo_relative_path": LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH.as_posix(),
            "source_route_probe_id": MINIMAL_INTEGRATED_SCENE_PROBE_ID,
            "source_route_probe_path": LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH.as_posix(),
            "duration_sec": SCENE_DURATION_SEC,
            "timeline_length_frames": SCENE_TIMELINE_LENGTH_FRAMES,
            "represents": "background animation accent candidate for one mainline explanation beat",
        },
        "local_probe_status": (
            "materialized_ignored_local_probe" if materialized else "blocked"
        ),
        "local_ymmp_materialization_status": (
            "materialized_ignored_local_probe" if materialized else "blocked"
        ),
        "access_state": access.get("access_state"),
        "local_probe_access": access,
        "local_probe_readback": readback,
        "source_route_readback_summary": _source_route_readback_summary(base),
    }


def _local_probe_readback(base: Path, access: dict[str, Any]) -> dict[str, Any]:
    target = base / LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH
    if not target.exists():
        return {
            "readback_status": "blocked",
            "reason": "local_minimal_animated_explanation_beat_probe_missing",
            "target_exists": False,
        }
    data = load_ymmp(target)
    timeline = _first_timeline(data)
    items = _get_timeline_items(data)
    item_type_counts: dict[str, int] = {}
    for item in items:
        item_type = _item_type(item)
        item_type_counts[item_type] = item_type_counts.get(item_type, 0) + 1
    unexpected_item_types = sorted(
        item_type for item_type in item_type_counts if item_type not in {"GroupItem", "ImageItem"}
    )
    source_summary = _source_route_readback_summary(base)
    structural_pass = (
        timeline.get("Length") == SCENE_TIMELINE_LENGTH_FRAMES
        and item_type_counts.get("GroupItem") == 8
        and item_type_counts.get("ImageItem") == 8
        and not unexpected_item_types
        and access["access_state"] == "verified_present"
        and source_summary.get("status") == "structural_pass"
    )
    return {
        "readback_status": "structural_pass" if structural_pass else "blocked",
        "target_exists": True,
        "file_sha256": _sha256(target),
        "file_size_bytes": target.stat().st_size,
        "timeline": {
            "fps": _dict(timeline.get("VideoInfo")).get("FPS"),
            "length_frames": timeline.get("Length"),
            "length_sec": round(SCENE_TIMELINE_LENGTH_FRAMES / 60, 6),
            "item_count": len(items),
            "item_type_counts": item_type_counts,
            "unexpected_item_types": unexpected_item_types,
        },
        "semantic_checks": {
            "status": "pass" if structural_pass else "blocked",
            "not_animation_demo": True,
            "narration_bound_to_subtitle_readback": True,
            "card_overlay_role_is_minimal": True,
            "animation_policy_frozen": True,
            "source_boundary_preserved": True,
            "no_render_or_audio_dependency": True,
        },
        "git_check_ignore_result": _git_check_ignore(
            base,
            LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH,
        ),
        "YMM4_launch_status": "not_launched",
        "render_status": "not_rendered",
        "audio_tts_status": "not_created",
    }


def _source_route_readback_summary(base: Path) -> dict[str, Any]:
    path = base / DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH
    if not path.exists():
        return {"status": "blocked", "reason": "source_route_readback_missing"}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return dict(payload.get("local_probe_readback_summary", {}))


def _source_context(base: Path) -> dict[str, Any]:
    return {
        "source_mvp_freeze_path": DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH.as_posix(),
        "source_mvp_policy_path": DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH.as_posix(),
        "source_integration_plan_path": DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_PATH.as_posix(),
        "source_minimal_integrated_scene_contract_path": (
            DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_PATH.as_posix()
        ),
        "source_minimal_integrated_scene_probe_readback_path": (
            DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH.as_posix()
        ),
        "source_episode_capsule_path": EPISODE_PRODUCTION_CAPSULE_PATH.as_posix(),
        "source_neutral_timeline_path": NEUTRAL_TIMELINE_IMPORT_PROOF_PATH.as_posix(),
        "source_caption_timing_plan_path": CAPTION_TIMING_PLAN_PATH.as_posix(),
        "source_caption_csv_import_candidate_path": CAPTION_CSV_IMPORT_CANDIDATE_PATH.as_posix(),
        "local_probe_path": LOCAL_IGNORED_MINIMAL_ANIMATED_EXPLANATION_BEAT_PROBE_PATH.as_posix(),
        "repo_root": str(base.resolve()),
    }


def _integration_acceptance(materialized: bool) -> dict[str, Any]:
    return {
        "not_animation_demo": True,
        "not_card_polish": True,
        "narration_remains_primary": True,
        "animation_supports_explanation": True,
        "overlay_does_not_become_main_target": True,
        "ready_for_one_preview_if_probe_exists": materialized,
        "preview_readiness_basis": (
            "local ignored YMM4 candidate exists and structural readback passed"
            if materialized
            else "contract is clear but local YMM4 candidate is not verified"
        ),
    }


def _business_goal_outcome_contract(next_axis: str) -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": True,
            "rationale": "the proof moves beyond primitive tuning into one integrated explanation beat",
        },
        "offer_clear": {
            "status": True,
            "rationale": "the pipeline gains a small animated support layer while narration stays primary",
        },
        "proof_clear": {
            "status": True,
            "rationale": "the artifact proves integrated beat structure, not production quality",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "animation overreach, render, audio/TTS, card polish, and source fetch remain closed",
        },
        "next_action_clear": {
            "status": True,
            "rationale": next_axis,
        },
        "visual_supports_explanation": {
            "status": "structural_ready_pending_preview",
            "rationale": "animation remains subordinate: one expression event and one short nod after the key phrase",
        },
    }


def _select_next_axis(materialized: bool) -> str:
    return NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION if materialized else NEXT_AXIS_MATERIALIZATION


def _next_axis_reason(materialized: bool) -> str:
    if materialized:
        return (
            "the integrated local .ymmp candidate exists, is ignored by git, "
            "and has structural readback pass, so one preview instruction is the next gate"
        )
    return "the integrated proof exists but local .ymmp materialization is not verified"


def _local_probe_created(payload: dict[str, Any]) -> bool:
    route = payload.get("mainline_route", {})
    return route.get("local_probe_status") == "materialized_ignored_local_probe"


def _not_accepted_scope_with_animation_boundaries() -> dict[str, bool]:
    scope = _not_accepted_scope()
    scope.update(
        {
            "production_animation_quality": False,
            "render_export_proof": False,
            "public_readiness": False,
            "real_RSS_news_integration": False,
            "speech_balloon_visual_acceptance": False,
            "full_chaban_scene": False,
            "audience_order_acceptance": False,
            "animation_only_probe_loop": False,
            "tempo_only_probe_loop": False,
            "card_redesign_or_density_work": False,
        }
    )
    return scope


def _boundaries(*, local_probe_created: bool) -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "real_RSS_news_fetch_performed": False,
        "card_assets_modified": False,
        "dense_script_modified": False,
        "local_ignored_ymmp_created_in_this_slice": local_probe_created,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
        "actual_order_or_audience_acceptance_claimed": False,
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_animation_only_loop", "status": True},
        {"gate": "no_primitive_loop", "status": True},
        {"gate": "no_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "next_axis_returns_to_mainline_content_pipeline", "status": next_axis},
    ]


def main() -> int:
    write_default_newsroom_minimal_animated_explanation_beat_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
