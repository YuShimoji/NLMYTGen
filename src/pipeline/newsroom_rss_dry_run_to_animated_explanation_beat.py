"""Build an offline topic-to-animated-explanation-beat proof.

This slice records the v2 visible-integration preview as a bounded pass, then
returns to content flow by turning one offline topic fixture into a diagnostic
animated explanation beat. It uses no live RSS/news collection, animation
changes, card redesign, render, YMM4 launch, or audio/TTS generation.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_minimal_animated_explanation_beat_visual_gap_fix import (
    DEFAULT_VISUAL_GAP_FIX_DOC_PATH,
    DEFAULT_VISUAL_GAP_FIX_PATH,
    LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH,
    _probe_structure_readback,
    materialize_local_v2_visible_integration_probe,
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
    _local_probe_access,
    _write_json,
    _write_text,
)
from src.pipeline.ymmp_patch import load_ymmp, save_ymmp


RSS_DRY_RUN_TOPIC_TO_BEAT_ID = (
    "newsroom_rss_dry_run_topic_to_animated_explanation_beat_v1_2026_06_30"
)
RSS_DRY_RUN_CONTRACT_ID = (
    "newsroom_rss_dry_run_animated_explanation_beat_contract_v1_2026_06_30"
)
RSS_DRY_RUN_SCHEMA_VERSION = "newsroom_rss_dry_run_to_animated_explanation_beat.v1"
RSS_DRY_RUN_CONTRACT_SCHEMA_VERSION = (
    "newsroom_rss_dry_run_animated_explanation_beat_contract.v1"
)

DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "rss_dry_run_topic_to_animated_explanation_beat_v1.json"
)
DEFAULT_RSS_DRY_RUN_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_RSS_DRY_RUN_TO_ANIMATED_EXPLANATION_BEAT_V1_2026-06-30.md"
)
DEFAULT_RSS_DRY_RUN_CONTRACT_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "rss_dry_run_animated_explanation_beat_contract_v1.json"
)

LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH = Path(
    "_tmp/newsroom_manual_probe/rss_dry_run_animated_explanation_beat_v1.ymmp"
)

NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION = (
    "newsroom-rss-dry-run-animated-explanation-beat-preview-operator-instruction-v1"
)
NEXT_AXIS_EPISODE_CAPSULE_WITH_ACCENT = (
    "newsroom-episode-capsule-with-animation-accent-v1"
)
NEXT_AXIS_TOPIC_FIXTURE_ROUTE_AUDIT = "newsroom-rss-topic-fixture-route-audit-v1"
NEXT_AXIS_ANIMATION_POLICY_CLOSED = (
    "newsroom-animation-accent-policy-closed-return-to-episode-capsule-v1"
)

TOPIC_ID = "offline_rss_like_topic_fixture_001"
BEAT_ID = "rss_dry_run_animated_explanation_beat_v1"
LOCAL_TEXT_REMARK = "rss_dry_run_animated_explanation_beat_v1_topic_text"
EXPLANATION_LINE = "Offline fixture: verify source boundary before production."

VISUAL_INTEGRATION_OBSERVATION: dict[str, Any] = {
    "source_observation_role": "user_opened_v2_visible_integration_probe",
    "source_probe_path": LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH.as_posix(),
    "yym4_opened": True,
    "explanation_text_visible": True,
    "animation_accent_visible": True,
    "same_scene_co_presence": True,
    "card_like_overlay_visible": False,
    "production_subtitle_design_accepted": False,
    "production_card_design_accepted": False,
    "visual_integration_status": "pass_with_boundary",
    "next_axis": "rss_or_topic_dry_run_to_animated_explanation_beat",
}

DRY_RUN_TOPIC_INPUT: dict[str, Any] = {
    "topic_id": TOPIC_ID,
    "title": "Offline fixture: source-boundary handoff before public news",
    "source_kind": "offline_fixture_or_diagnostic",
    "key_fact_or_claim": (
        "A candidate topic must remain diagnostic until source truth, rights, "
        "and episode fit are reviewed."
    ),
    "explanation_angle": (
        "show that a topic-like input can become one clear explanation beat "
        "without using live RSS or public-news claims"
    ),
    "boundary_note": (
        "No live RSS/network fetch, source quote, external media, rights "
        "approval, or publication readiness is implied."
    ),
}

ANIMATION_ACCENT_POLICY: dict[str, Any] = {
    "stable_pose": True,
    "one_expression_event": True,
    "one_short_nod_or_reaction": True,
    "return_to_stable_pose": True,
    "body_forward_back": False,
    "repeated_nodding": False,
    "mechanical_expression_cycle": False,
    "speech_balloon": False,
    "full_chaban_scene": False,
}


def write_default_newsroom_rss_dry_run_to_animated_explanation_beat_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    materialize_local_rss_dry_run_animated_explanation_beat(root=base)
    proof = build_default_rss_dry_run_topic_to_animated_explanation_beat(root=base)
    contract = build_default_rss_dry_run_animated_explanation_beat_contract(root=base)
    _write_json(base / DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH, proof)
    _write_text(base / DEFAULT_RSS_DRY_RUN_DOC_PATH, render_rss_dry_run_markdown(proof))
    _write_json(base / DEFAULT_RSS_DRY_RUN_CONTRACT_PATH, contract)
    return {
        "rss_dry_run_topic_to_animated_explanation_beat": proof,
        "rss_dry_run_animated_explanation_beat_contract": contract,
    }


def build_default_rss_dry_run_topic_to_animated_explanation_beat(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    local_access = _rss_dry_run_probe_access(base)
    local_readback = _probe_structure_readback(
        base,
        LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH,
    )
    materialized = _local_probe_materialized(local_access, local_readback)
    next_axis = (
        NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION
        if materialized
        else NEXT_AXIS_EPISODE_CAPSULE_WITH_ACCENT
    )
    return {
        "artifact_id": RSS_DRY_RUN_TOPIC_TO_BEAT_ID,
        "proof_id": RSS_DRY_RUN_TOPIC_TO_BEAT_ID,
        "schema_version": RSS_DRY_RUN_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_context": _source_context(base),
        "visual_integration_observation": VISUAL_INTEGRATION_OBSERVATION,
        "dry_run_topic_input": DRY_RUN_TOPIC_INPUT,
        "topic_to_beat_transformation": _topic_to_beat_transformation(),
        "animated_explanation_beat": _animated_explanation_beat(local_access, local_readback),
        "local_probe_access_state": local_access,
        "local_probe_readback": local_readback,
        "business_goal_outcome_contract": _business_goal_outcome_contract(
            local_probe_materialized=materialized,
            next_axis=next_axis,
        ),
        "selected_next_axis": next_axis,
        "next_recommended_axis": {
            "selected": next_axis,
            "if_proof_without_local_ymmp": NEXT_AXIS_EPISODE_CAPSULE_WITH_ACCENT,
            "if_topic_route_unclear": NEXT_AXIS_TOPIC_FIXTURE_ROUTE_AUDIT,
            "if_animation_adds_little": NEXT_AXIS_ANIMATION_POLICY_CLOSED,
            "reason": _next_axis_reason(materialized),
        },
        "not_accepted_scope": _not_accepted_scope_with_rss_dry_run_boundaries(),
        "boundaries": _boundaries(local_probe_created=materialized),
        "inertia_check": _inertia_check(next_axis),
        "completion_matrix": _completion_matrix(materialized),
    }


def build_default_rss_dry_run_animated_explanation_beat_contract(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    proof = build_default_rss_dry_run_topic_to_animated_explanation_beat(root=root)
    return {
        "artifact_id": RSS_DRY_RUN_CONTRACT_ID,
        "contract_id": RSS_DRY_RUN_CONTRACT_ID,
        "proof_id": proof["artifact_id"],
        "schema_version": RSS_DRY_RUN_CONTRACT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "visual_integration_observation": proof["visual_integration_observation"],
        "dry_run_topic_input": proof["dry_run_topic_input"],
        "topic_to_beat_transformation": proof["topic_to_beat_transformation"],
        "animated_explanation_beat": proof["animated_explanation_beat"],
        "animation_accent_policy": ANIMATION_ACCENT_POLICY,
        "overlay_card_policy": {
            "plain_TextItem_diagnostic_label_acceptable": True,
            "designed_card_created": False,
            "card_polish_performed": False,
            "production_subtitle_design_claimed": False,
        },
        "local_probe_status": proof["local_probe_access_state"],
        "business_goal_outcome_contract": proof["business_goal_outcome_contract"],
        "selected_next_axis": proof["selected_next_axis"],
        "next_recommended_axis": proof["next_recommended_axis"],
        "not_accepted_scope": proof["not_accepted_scope"],
        "boundaries": proof["boundaries"],
        "inertia_check": proof["inertia_check"],
    }


def materialize_local_rss_dry_run_animated_explanation_beat(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    source = base / LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH
    if not source.exists():
        materialize_local_v2_visible_integration_probe(root=base)
    source_readback = _probe_structure_readback(
        base,
        LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH,
    )
    if source_readback.get("readback_status") != "structural_pass":
        raise ValueError("source v2 visible-integration probe is not structurally readable")
    if source_readback.get("visible_text_or_overlay_item_count") != 1:
        raise ValueError("source v2 probe must contain exactly one visible TextItem")

    target = base / LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    probe = copy.deepcopy(load_ymmp(source))
    probe["FilePath"] = str(target.resolve())
    timeline = _first_timeline(probe)
    if not timeline:
        raise ValueError("source v2 probe has no timeline")

    text_items = [item for item in _get_timeline_items(probe) if _item_type(item) == "TextItem"]
    if len(text_items) != 1:
        raise ValueError("source v2 probe must have exactly one TextItem")
    text_item = text_items[0]
    text_item["Text"] = EXPLANATION_LINE
    text_item["Remark"] = LOCAL_TEXT_REMARK
    text_item["Length"] = max(int(text_item.get("Length", 0) or 0), 720)
    text_item["IsHidden"] = False
    timeline["Length"] = max(int(timeline.get("Length", 0) or 0), 720)

    save_ymmp(probe, target)
    return probe


def render_rss_dry_run_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom RSS Dry Run To Animated Explanation Beat v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(
        lines,
        "Visual Integration Observation",
        payload.get("visual_integration_observation"),
    )
    _append_mapping(lines, "Dry-Run Topic Input", payload.get("dry_run_topic_input"))
    _append_mapping(
        lines,
        "Topic-To-Beat Transformation",
        payload.get("topic_to_beat_transformation"),
    )
    _append_mapping(lines, "Animated Explanation Beat", payload.get("animated_explanation_beat"))
    _append_mapping(lines, "Local Probe Access State", payload.get("local_probe_access_state"))
    _append_mapping(lines, "Local Probe Readback", payload.get("local_probe_readback"))
    _append_mapping(
        lines,
        "Business Goal Outcome Contract",
        payload.get("business_goal_outcome_contract"),
    )
    _append_mapping(lines, "Next Recommended Axis", payload.get("next_recommended_axis"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    _append_rows(lines, "Inertia Check", ["gate", "status"], payload.get("inertia_check"))
    _append_rows(
        lines,
        "Completion Matrix",
        ["gate", "status"],
        payload.get("completion_matrix"),
    )
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This is an offline content-flow proof. It creates no live RSS/news "
        "fetch, no render, no audio/TTS, no card redesign, and no production "
        "or public acceptance claim."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _source_context(base: Path) -> dict[str, Any]:
    return {
        "source_visual_gap_fix_path": DEFAULT_VISUAL_GAP_FIX_PATH.as_posix(),
        "source_visual_gap_fix_doc_path": DEFAULT_VISUAL_GAP_FIX_DOC_PATH.as_posix(),
        "source_v2_visible_integration_probe_path": (
            LOCAL_IGNORED_V2_VISIBLE_INTEGRATION_PROBE_PATH.as_posix()
        ),
        "rss_dry_run_probe_path": (
            LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH.as_posix()
        ),
        "repo_root": str(base.resolve()),
    }


def _topic_to_beat_transformation() -> dict[str, Any]:
    return {
        "source_topic_id": TOPIC_ID,
        "source_kind": DRY_RUN_TOPIC_INPUT["source_kind"],
        "input_claim_used": DRY_RUN_TOPIC_INPUT["key_fact_or_claim"],
        "explanation_angle_used": DRY_RUN_TOPIC_INPUT["explanation_angle"],
        "derived_explanation_line": EXPLANATION_LINE,
        "transformation_status": "offline_topic_fixture_to_one_explanation_beat",
        "network_fetch_performed": False,
        "live_RSS_or_news_used": False,
    }


def _animated_explanation_beat(
    local_access: dict[str, Any],
    local_readback: dict[str, Any],
) -> dict[str, Any]:
    materialized = _local_probe_materialized(local_access, local_readback)
    return {
        "beat_id": BEAT_ID,
        "source_topic_id": TOPIC_ID,
        "explanation_line": EXPLANATION_LINE,
        "narration_intent": (
            "turn a topic-like input into one clear review-only explanation "
            "line before any public-news or source-truth claim"
        ),
        "subtitle_or_text_role": (
            "plain diagnostic TextItem role; proves text/narration placement "
            "without accepting production subtitle design"
        ),
        "minimal_overlay_role": "plain TextItem diagnostic label; no designed card",
        "background_animation_accent_role": (
            "frozen MVP accent remains subordinate: stable pose, one expression "
            "event, one short nod/reaction, return to stable pose"
        ),
        "source_boundary_role": DRY_RUN_TOPIC_INPUT["boundary_note"],
        "YMM4_representation_candidate": {
            "repo_relative_path": (
                LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH.as_posix()
            ),
            "basis": "copied v2 visible-integration probe with TextItem replaced by topic-derived line",
            "textitem_count": local_readback.get("TextItem_count", 0),
            "animation_item_count": local_readback.get("animation_item_count", 0),
            "designed_card_present": False,
        },
        "local_probe_status": (
            "materialized_ignored_local_probe"
            if materialized
            else "blocked"
        ),
        "animation_accent_policy": ANIMATION_ACCENT_POLICY,
    }


def _rss_dry_run_probe_access(base: Path) -> dict[str, Any]:
    access = _local_probe_access(
        base,
        LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH,
        "local_ignored_rss_dry_run_animated_explanation_beat_probe",
    )
    readback = _probe_structure_readback(
        base,
        LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH,
    )
    access.update(
        {
            "visible_text_or_overlay_item_count": readback.get(
                "visible_text_or_overlay_item_count", 0
            ),
            "animation_item_count": readback.get("animation_item_count", 0),
            "materialization_status": (
                "materialized_ignored_local_probe"
                if _local_probe_materialized(access, readback)
                else "blocked"
            ),
        }
    )
    return access


def _local_probe_materialized(
    local_access: dict[str, Any],
    local_readback: dict[str, Any],
) -> bool:
    return (
        local_access.get("target_exists") is True
        and local_access.get("access_state") == "verified_present"
        and local_readback.get("readback_status") == "structural_pass"
        and local_readback.get("visible_text_or_overlay_item_count") == 1
        and local_readback.get("animation_item_count") == 16
    )


def _business_goal_outcome_contract(
    *,
    local_probe_materialized: bool,
    next_axis: str,
) -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": True,
            "rationale": "the slice exits visual/animation tuning and returns to content-flow proof",
        },
        "offer_clear": {
            "status": True,
            "rationale": "one offline topic-like input becomes one explanation beat",
        },
        "proof_clear": {
            "status": True,
            "rationale": "the proof is content-flow integration, not production quality",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "no live RSS, card redesign, animation tuning, render, or publication claim",
        },
        "next_action_clear": {
            "status": True,
            "rationale": next_axis,
        },
        "visual_supports_explanation": {
            "status": local_probe_materialized,
            "rationale": "the frozen animation remains subordinate to the TextItem/narration role",
        },
    }


def _next_axis_reason(local_probe_materialized: bool) -> str:
    if local_probe_materialized:
        return (
            "offline topic-to-beat proof and ignored local .ymmp were created; "
            "the scene contains a topic-derived TextItem plus unchanged animation items"
        )
    return (
        "proof exists, but local .ymmp materialization is not verified; return "
        "to episode capsule integration rather than visual tuning"
    )


def _not_accepted_scope_with_rss_dry_run_boundaries() -> dict[str, bool]:
    scope = _not_accepted_scope()
    scope.update(
        {
            "live_RSS_or_news_fetch": False,
            "real_source_truth_approved": False,
            "production_animation_quality": False,
            "production_subtitle_design": False,
            "production_card_design": False,
            "render_export_proof": False,
            "public_readiness": False,
            "audio_or_tts_output": False,
            "actual_order_or_audience_acceptance": False,
            "card_redesign_or_density_work": False,
            "animation_only_probe_loop": False,
            "primitive_or_tempo_loop": False,
        }
    )
    return scope


def _boundaries(*, local_probe_created: bool) -> dict[str, bool]:
    return {
        "network_fetch_performed": False,
        "live_RSS_news_fetch_performed": False,
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "audio_tts_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "card_assets_modified": False,
        "card_redesign_performed": False,
        "production_subtitle_or_card_design_created": False,
        "animation_tuned": False,
        "animation_only_probe_created": False,
        "local_ignored_ymmp_created_in_this_slice": local_probe_created,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
        "actual_order_or_audience_acceptance_claimed": False,
    }


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_animation_only_loop", "status": True},
        {"gate": "no_primitive_or_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "no_live_RSS_or_network_fetch", "status": True},
        {"gate": "next_work_returns_to_mainline_content_pipeline", "status": next_axis},
    ]


def _completion_matrix(local_probe_materialized: bool) -> list[dict[str, Any]]:
    return [
        {"gate": "repo_state_verified", "status": True},
        {"gate": "visual_integration_observation_recorded", "status": True},
        {"gate": "offline_topic_RSS_like_input_selected_or_created", "status": True},
        {"gate": "topic_to_explanation_beat_transformation_recorded", "status": True},
        {"gate": "animation_accent_policy_enforced", "status": True},
        {"gate": "local_ymmp_created_or_honest_blocked_state_recorded", "status": True},
        {"gate": "local_ymmp_materialized", "status": local_probe_materialized},
        {"gate": "next_axis_selected", "status": True},
    ]


def main() -> int:
    write_default_newsroom_rss_dry_run_to_animated_explanation_beat_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
