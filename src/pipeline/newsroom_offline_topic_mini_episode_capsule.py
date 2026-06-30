"""Create a diagnostic mini episode capsule from the offline topic bridge.

This slice advances the prior bridge into a concrete 5-beat capsule contract.
It intentionally does not create a YMM4 project, launch YMM4, render, fetch live
RSS/news, redesign cards, tune animation, or generate audio/TTS.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_offline_topic_mini_episode_capsule_bridge import (
    ANIMATION_ACCENT_DISABLED,
    DEFAULT_BRIDGE_PATH,
    DEFAULT_PREVIEW_OBSERVATION_PATH,
)
from src.pipeline.newsroom_rss_dry_run_to_animated_explanation_beat import (
    DEFAULT_RSS_DRY_RUN_CONTRACT_PATH,
    DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH,
    DRY_RUN_TOPIC_INPUT,
    EXPLANATION_LINE,
    TOPIC_ID,
)
from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    _append_mapping,
    _append_rows,
)
from src.pipeline.newsroom_yukkuri_animation_tempo_contract import (
    _write_json,
    _write_text,
)


CAPSULE_ID = "newsroom_offline_topic_mini_episode_capsule_with_animation_accent_v1_2026_06_30"
CONTRACT_ID = "newsroom_offline_topic_mini_episode_capsule_contract_v1_2026_06_30"
CAPSULE_SCHEMA_VERSION = "newsroom_offline_topic_mini_episode_capsule_with_animation_accent.v1"
CONTRACT_SCHEMA_VERSION = "newsroom_offline_topic_mini_episode_capsule_contract.v1"

DEFAULT_CAPSULE_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "offline_topic_mini_episode_capsule_with_animation_accent_v1.json"
)
DEFAULT_CAPSULE_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_CAPSULE_WITH_ANIMATION_ACCENT_V1_2026-06-30.md"
)
DEFAULT_CAPSULE_CONTRACT_PATH = Path(
    "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_contract_v1.json"
)

LOCAL_IGNORED_CAPSULE_YMMP_PATH = Path(
    "_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_with_animation_accent_v1.ymmp"
)

NEXT_AXIS_MATERIALIZATION = (
    "newsroom-offline-topic-mini-episode-capsule-materialization-v1"
)
NEXT_AXIS_PREVIEW = "newsroom-offline-topic-mini-episode-preview-operator-instruction-v1"
NEXT_AXIS_ROUTE_AUDIT = "newsroom-episode-capsule-route-audit-v1"
NEXT_AXIS_TOPIC_AUDIT = "newsroom-rss-topic-fixture-route-audit-v1"
NEXT_AXIS_LIVE_BOUNDARY_PLAN = "newsroom-live-rss-boundary-plan-v1"

ANIMATION_ASSIGNMENTS = {
    "none",
    "stable_pose_only",
    "expression_event",
    "short_nod_reaction",
    "expression_plus_short_nod",
}


def write_default_newsroom_offline_topic_mini_episode_capsule_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    capsule = build_default_offline_topic_mini_episode_capsule(root=base)
    contract = build_default_offline_topic_mini_episode_capsule_contract(root=base)
    _write_json(base / DEFAULT_CAPSULE_PATH, capsule)
    _write_text(base / DEFAULT_CAPSULE_DOC_PATH, render_capsule_markdown(capsule))
    _write_json(base / DEFAULT_CAPSULE_CONTRACT_PATH, contract)
    return {
        "capsule": capsule,
        "contract": contract,
    }


def build_default_offline_topic_mini_episode_capsule(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    bridge = _load_json_object(base / DEFAULT_BRIDGE_PATH)
    beats = _capsule_beats(bridge)
    local_access = _local_artifact_access(base)
    route = _mainline_route(local_access)
    return {
        "artifact_id": CAPSULE_ID,
        "capsule_id": CAPSULE_ID,
        "schema_version": CAPSULE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "live_fetch_used": False,
        "actual_audience_acceptance_claimed": False,
        "source_bridge_path": DEFAULT_BRIDGE_PATH.as_posix(),
        "source_topic_fixture_path": DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix(),
        "source_context": _source_context(base),
        "episode_capsule": {
            "episode_title": "Offline topic source-boundary mini explainer",
            "episode_goal": (
                "prove that an offline RSS-like topic can become a small "
                "review-only explainer structure before any live source work"
            ),
            "beat_count": len(beats),
            "beats": beats,
            "source_boundary_summary": (
                "All claims remain offline fixture claims; no live RSS/news, "
                "source truth, rights, quotes, media, or publication readiness is accepted."
            ),
            "animation_accent_summary": _animation_accent_summary(beats),
            "text_overlay_summary": (
                "Plain TextItem and diagnostic label roles support comprehension; "
                "no polished card, production subtitle, or visual layout tuning is included."
            ),
            "materialization_summary": _materialization_summary(local_access),
        },
        "mainline_route": route,
        "local_artifact_access": local_access,
        "business_goal_outcome_contract": _business_goal_outcome_contract(),
        "recommendation_logic": _recommendation_logic(local_access),
        "selected_next_axis": _selected_next_axis(local_access),
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
        "inertia_check": _inertia_check(),
        "completion_matrix": _completion_matrix(local_access),
    }


def build_default_offline_topic_mini_episode_capsule_contract(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    capsule = build_default_offline_topic_mini_episode_capsule(root=root)
    return {
        "artifact_id": CONTRACT_ID,
        "contract_id": CONTRACT_ID,
        "schema_version": CONTRACT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_capsule_path": DEFAULT_CAPSULE_PATH.as_posix(),
        "source_bridge_path": DEFAULT_BRIDGE_PATH.as_posix(),
        "capsule_id": capsule["capsule_id"],
        "beat_count": capsule["episode_capsule"]["beat_count"],
        "beat_contract": [
            {
                "beat_id": beat["beat_id"],
                "source_topic_id": beat["source_topic_id"],
                "beat_function": beat["beat_function"],
                "text_overlay_policy": {
                    "subtitle_or_text_role": beat["subtitle_or_text_role"],
                    "minimal_overlay_role": beat["minimal_overlay_role"],
                    "production_subtitle_design": False,
                    "production_card_design": False,
                },
                "animation_assignment": beat["animation_assignment"],
                "animation_accent_role": beat["background_animation_accent_role"],
                "source_boundary_role": beat["source_boundary_role"],
                "materialization_role": beat["materialization_role"],
                "review_status": beat["review_status"],
            }
            for beat in capsule["episode_capsule"]["beats"]
        ],
        "animation_accent_policy": {
            "policy_status": "frozen_mvp_policy_carried_forward",
            "allowed_assignments": sorted(ANIMATION_ASSIGNMENTS),
            "allowed": [
                "stable pose",
                "at most one expression event per relevant beat",
                "at most one short nod/reaction per relevant beat",
                "return to stable pose",
            ],
            "disabled": [
                *ANIMATION_ACCENT_DISABLED,
                "animation-only probe loop",
                "tempo-only loop",
            ],
            "do_not_force_animation_onto_every_beat": True,
        },
        "text_overlay_policy": {
            "plain_TextItem_role_acceptable": True,
            "diagnostic_label_role_acceptable": True,
            "polished_card_design": False,
            "production_subtitle_design": False,
            "card_redesign": False,
            "visual_layout_tuning": False,
        },
        "materialization_policy": {
            "local_ymmp_created_in_this_slice": False,
            "local_ymmp_materialization_status": "blocked_or_deferred",
            "reason": (
                "No safe non-speculative PLANNER007 multi-beat YMM4 route is "
                "identified yet; create the contract first, then materialize separately."
            ),
            "next_axis": NEXT_AXIS_MATERIALIZATION,
        },
        "not_accepted_scope": capsule["not_accepted_scope"],
        "boundaries": capsule["boundaries"],
    }


def render_capsule_markdown(payload: dict[str, Any]) -> str:
    episode = _dict(payload.get("episode_capsule"))
    route = _dict(payload.get("mainline_route"))
    local_access = _dict(payload.get("local_artifact_access"))
    lines = [
        "# Newsroom Offline Topic Mini Episode Capsule With Animation Accent v1",
        "",
        f"artifact_id: {payload.get('artifact_id')}",
        f"schema_version: {payload.get('schema_version')}",
        f"production_status: {payload.get('production_status')}",
        f"render_gate: {payload.get('render_gate')}",
        f"live_fetch_used: {str(payload.get('live_fetch_used')).lower()}",
        f"selected_next_axis: {payload.get('selected_next_axis')}",
        "",
    ]
    _append_mapping(lines, "Identity", {
        "capsule_id": payload.get("capsule_id"),
        "source_bridge_path": payload.get("source_bridge_path"),
        "source_topic_fixture_path": payload.get("source_topic_fixture_path"),
        "production_status": payload.get("production_status"),
        "render_gate": payload.get("render_gate"),
        "live_fetch_used": payload.get("live_fetch_used"),
    })
    _append_mapping(lines, "Source Context", payload.get("source_context"))
    _append_mapping(lines, "Episode Capsule Summary", {
        "episode_title": episode.get("episode_title"),
        "episode_goal": episode.get("episode_goal"),
        "beat_count": episode.get("beat_count"),
        "source_boundary_summary": episode.get("source_boundary_summary"),
        "animation_accent_summary": episode.get("animation_accent_summary"),
        "text_overlay_summary": episode.get("text_overlay_summary"),
        "materialization_summary": episode.get("materialization_summary"),
    })
    _append_rows(
        lines,
        "Beat Table Summary",
        [
            "beat_id",
            "beat_function",
            "explanation_line",
            "animation_assignment",
            "materialization_role",
            "materialization_status",
            "review_status",
        ],
        episode.get("beats"),
    )
    _append_mapping(lines, "Mainline Route", route)
    _append_mapping(lines, "Local Artifact Access", local_access)
    _append_mapping(
        lines,
        "Business Goal Outcome Contract",
        payload.get("business_goal_outcome_contract"),
    )
    _append_mapping(lines, "Recommendation Logic", payload.get("recommendation_logic"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    _append_rows(
        lines,
        "Inertia Check",
        ["gate", "status"],
        payload.get("inertia_check"),
    )
    _append_rows(
        lines,
        "Completion Matrix",
        ["gate", "status"],
        payload.get("completion_matrix"),
    )
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This capsule is diagnostic-only. It creates no local .ymmp, no render, "
        "no audio/TTS, no live RSS/news fetch, no polished card, no production "
        "subtitle/card design, and no public or audience acceptance claim."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _capsule_beats(bridge: dict[str, Any]) -> list[dict[str, Any]]:
    bridge_beats = _dict(bridge.get("mini_episode_capsule")).get("beats", [])
    assignments = {
        "offline_topic_mini_ep_beat_01_hook": "stable_pose_only",
        "offline_topic_mini_ep_beat_02_key_claim": "expression_event",
        "offline_topic_mini_ep_beat_03_source_warning": "expression_plus_short_nod",
        "offline_topic_mini_ep_beat_04_implication": "short_nod_reaction",
        "offline_topic_mini_ep_beat_05_close": "none",
    }
    route_candidates = {
        "offline_topic_mini_ep_beat_01_hook": "current_one_beat_text_plus_accent_route_candidate",
        "offline_topic_mini_ep_beat_02_key_claim": "contract_only_pending_multi_beat_route",
        "offline_topic_mini_ep_beat_03_source_warning": "proven_one_beat_boundary_line_candidate",
        "offline_topic_mini_ep_beat_04_implication": "contract_only_pending_multi_beat_route",
        "offline_topic_mini_ep_beat_05_close": "contract_only_no_animation_required",
    }
    result: list[dict[str, Any]] = []
    for index, beat in enumerate(bridge_beats, start=1):
        if not isinstance(beat, dict):
            continue
        beat_id = str(beat.get("beat_id"))
        assignment = assignments.get(beat_id, "none")
        materialization_status = (
            "existing_route_candidate"
            if beat.get("materialization_status") == "existing_route_candidate"
            else "contract_only"
        )
        result.append({
            "order": index,
            "beat_id": beat_id,
            "source_topic_id": beat.get("source_topic_id", TOPIC_ID),
            "beat_function": beat.get("beat_function"),
            "explanation_line": beat.get("explanation_line"),
            "narration_intent": beat.get("narration_intent"),
            "subtitle_or_text_role": beat.get("subtitle_or_text_role"),
            "minimal_overlay_role": beat.get("minimal_overlay_role"),
            "background_animation_accent_role": beat.get(
                "background_animation_accent_role"
            ),
            "animation_assignment": assignment,
            "source_boundary_role": beat.get("source_boundary_role"),
            "route_candidate": route_candidates.get(beat_id, "contract_only"),
            "materialization_role": (
                "candidate_for_future_multi_beat_ymmp"
                if materialization_status == "existing_route_candidate"
                else "capsule_contract_only"
            ),
            "materialization_status": materialization_status,
            "review_status": "diagnostic_review_ready",
            "not_accepted_scope": _not_accepted_scope(),
        })
    return result


def _source_context(base: Path) -> dict[str, Any]:
    return {
        "repo_root": str(base.resolve()),
        "source_bridge_path": DEFAULT_BRIDGE_PATH.as_posix(),
        "source_preview_observation_path": DEFAULT_PREVIEW_OBSERVATION_PATH.as_posix(),
        "source_topic_fixture_path": DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix(),
        "source_animated_beat_contract_path": DEFAULT_RSS_DRY_RUN_CONTRACT_PATH.as_posix(),
        "source_background_animation_mvp_freeze_path": (
            "samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json"
        ),
        "prior_episode_capsule_path": (
            "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json"
        ),
    }


def _mainline_route(local_access: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_name": "offline_topic_bridge_to_diagnostic_mini_episode_capsule",
        "existing_artifacts_used": [
            DEFAULT_BRIDGE_PATH.as_posix(),
            DEFAULT_PREVIEW_OBSERVATION_PATH.as_posix(),
            DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix(),
            DEFAULT_RSS_DRY_RUN_CONTRACT_PATH.as_posix(),
            "samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json",
            "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json",
        ],
        "new_artifacts_created": [
            DEFAULT_CAPSULE_PATH.as_posix(),
            DEFAULT_CAPSULE_DOC_PATH.as_posix(),
            DEFAULT_CAPSULE_CONTRACT_PATH.as_posix(),
            "src/pipeline/newsroom_offline_topic_mini_episode_capsule.py",
            "tests/test_newsroom_offline_topic_mini_episode_capsule.py",
        ],
        "transformation_steps": [
            "read the prior 5-beat bridge and current offline topic fixture",
            "promote bridge beats into a diagnostic episode capsule",
            "assign optional frozen animation accents without changing primitives",
            "carry forward plain TextItem and diagnostic label roles",
            "record that multi-beat local .ymmp materialization is deferred",
        ],
        "route_confidence": "high",
        "route_blockers": [
            "existing episode_production_capsule_v1 is an older fake-packet structural precedent, not the current offline topic route",
            "no verified PLANNER007 multi-beat YMM4 materialization route exists in this slice",
            "previous RSS dry-run .ymmp proof was host-local user evidence and is not required on PLANNER007",
        ],
        "next_required_route_work": [
            NEXT_AXIS_MATERIALIZATION,
            "define a non-speculative multi-beat YMM4 materialization route before any preview request",
        ],
        "local_ymmp_materialization_status": local_access["access_state"],
    }


def _local_artifact_access(base: Path) -> dict[str, Any]:
    target = base / LOCAL_IGNORED_CAPSULE_YMMP_PATH
    return {
        "artifact_id": "local_ignored_offline_topic_mini_episode_capsule_candidate",
        "repo_relative_path": LOCAL_IGNORED_CAPSULE_YMMP_PATH.as_posix(),
        "folder_full_path_current_host": str(target.parent.resolve()),
        "file_full_path_current_host": str(target.resolve()),
        "target_exists": target.exists(),
        "access_state": "not_created_deferred",
        "access_evidence_level": "L1_IGNORED_PATH_CONFIRMED_NO_FILE",
        "artifact_scope": "ignored_local_only_if_created_later",
        "evidence_source": "current_host_filesystem_plus_git_check_ignore",
        "git_check_ignore_result": _git_check_ignore(base, LOCAL_IGNORED_CAPSULE_YMMP_PATH),
        "size": None,
        "item_type_counts": None,
        "defer_reason": (
            "Route is contract-clear but local multi-beat YMM4 materialization "
            "would be speculative in this slice."
        ),
    }


def _animation_accent_summary(beats: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for beat in beats:
        assignment = str(beat.get("animation_assignment"))
        counts[assignment] = counts.get(assignment, 0) + 1
    return {
        "policy_status": "frozen_mvp_policy_carried_forward",
        "assignment_counts": counts,
        "allowed_assignments": sorted(ANIMATION_ASSIGNMENTS),
        "disabled": [
            *ANIMATION_ACCENT_DISABLED,
            "animation-only probe loop",
            "tempo-only loop",
        ],
        "animation_optional_not_forced": True,
    }


def _materialization_summary(local_access: dict[str, Any]) -> dict[str, Any]:
    return {
        "local_ymmp_materialization_status": "blocked_or_deferred",
        "local_ymmp_created_in_this_slice": False,
        "planned_repo_relative_path_if_later": local_access["repo_relative_path"],
        "reason": local_access["defer_reason"],
        "next_axis": NEXT_AXIS_MATERIALIZATION,
    }


def _business_goal_outcome_contract() -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": True,
            "rationale": "this moves beyond one-beat proof into a complete 5-beat capsule",
        },
        "offer_clear": {
            "status": True,
            "rationale": "the artifact shows a small episode structure with hook, claim, warning, implication, and close",
        },
        "proof_clear": {
            "status": True,
            "rationale": "the proof is capsule/content-flow structure, not production quality",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "card design, animation tuning, render, audio/TTS, and live RSS remain closed",
        },
        "next_action_clear": {
            "status": True,
            "rationale": NEXT_AXIS_MATERIALIZATION,
        },
        "visual_supports_explanation": {
            "status": True,
            "rationale": "animation assignments are optional and subordinate to text/narration",
        },
    }


def _recommendation_logic(local_access: dict[str, Any]) -> dict[str, Any]:
    selected = _selected_next_axis(local_access)
    return {
        "selected": selected,
        "if_capsule_contract_clear_but_no_local_ymmp": NEXT_AXIS_MATERIALIZATION,
        "if_new_multi_beat_local_ymmp_exists_and_preview_adds_value": NEXT_AXIS_PREVIEW,
        "if_existing_route_is_unclear": NEXT_AXIS_ROUTE_AUDIT,
        "if_topic_to_beat_is_too_synthetic": NEXT_AXIS_TOPIC_AUDIT,
        "if_offline_capsule_route_is_strong_and_source_boundary_is_next": NEXT_AXIS_LIVE_BOUNDARY_PLAN,
        "reason": (
            "The capsule contract is clear, but no non-speculative multi-beat "
            "local .ymmp was created; materialization should be its own next slice."
        ),
    }


def _selected_next_axis(local_access: dict[str, Any]) -> str:
    if local_access.get("target_exists") is True and local_access.get("access_state") == "verified_present":
        return NEXT_AXIS_PREVIEW
    return NEXT_AXIS_MATERIALIZATION


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "live_rss_or_news_fetch": False,
        "production_script_quality": False,
        "production_subtitle_design": False,
        "production_card_design": False,
        "production_animation_quality": False,
        "card_redesign": False,
        "visual_layout_tuning": False,
        "animation_tuning": False,
        "render_export_proof": False,
        "audio_or_tts_output": False,
        "public_upload_or_public_readiness": False,
        "actual_order_or_audience_acceptance": False,
        "source_truth_or_rights_approval": False,
    }


def _boundaries() -> dict[str, bool]:
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
        "local_ignored_ymmp_created_in_this_slice": False,
        "ymmp_or_media_staged_or_committed": False,
        "production_public_readiness_claimed": False,
        "actual_order_or_audience_acceptance_claimed": False,
    }


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "no_animation_only_loop", "status": True},
        {"gate": "no_primitive_or_tempo_loop", "status": True},
        {"gate": "no_card_polish_loop", "status": True},
        {"gate": "no_render_export_loop", "status": True},
        {"gate": "no_live_RSS_or_network_fetch", "status": True},
        {"gate": "next_axis_remains_episode_construction", "status": NEXT_AXIS_MATERIALIZATION},
    ]


def _completion_matrix(local_access: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"gate": "repo_state_verified", "status": True},
        {"gate": "previous_bridge_inspected", "status": True},
        {"gate": "five_beat_capsule_contract_created", "status": True},
        {"gate": "mainline_route_confidence_recorded", "status": True},
        {
            "gate": "local_ymmp_created_or_honestly_deferred",
            "status": "deferred" if not local_access.get("target_exists") else "created",
        },
        {"gate": "next_axis_selected", "status": True},
    ]


def _load_json_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def _git_check_ignore(base: Path, path: Path) -> dict[str, Any]:
    result = subprocess.run(
        ["git", "check-ignore", "-v", "--", path.as_posix()],
        cwd=base,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    return {
        "command": f"git check-ignore -v -- {path.as_posix()}",
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "ignored": result.returncode == 0,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def main() -> int:
    write_default_newsroom_offline_topic_mini_episode_capsule_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
