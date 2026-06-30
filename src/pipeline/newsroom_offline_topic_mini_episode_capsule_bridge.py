"""Bridge an offline RSS-like topic proof to a mini episode capsule contract.

This slice records the user-side preview observation for the RSS dry-run
animated beat and creates a diagnostic-only mini episode bridge. It does not
launch YMM4, render, create another local YMM4 project, fetch live RSS/news, or
approve production subtitle/card design.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_rss_dry_run_to_animated_explanation_beat import (
    DEFAULT_RSS_DRY_RUN_CONTRACT_PATH,
    DEFAULT_RSS_DRY_RUN_DOC_PATH,
    DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH,
    DRY_RUN_TOPIC_INPUT,
    EXPLANATION_LINE,
    LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH,
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


PREVIEW_OBSERVATION_ID = (
    "newsroom_rss_dry_run_animated_beat_preview_observation_v1_2026_06_30"
)
BRIDGE_ID = "newsroom_offline_topic_mini_episode_capsule_bridge_v1_2026_06_30"
PREVIEW_OBSERVATION_SCHEMA_VERSION = (
    "newsroom_rss_dry_run_animated_beat_preview_observation.v1"
)
BRIDGE_SCHEMA_VERSION = "newsroom_offline_topic_mini_episode_capsule_bridge.v1"

DEFAULT_PREVIEW_OBSERVATION_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "rss_dry_run_animated_beat_preview_observation_v1.json"
)
DEFAULT_PREVIEW_OBSERVATION_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_RSS_DRY_RUN_ANIMATED_BEAT_PREVIEW_OBSERVATION_V1_2026-06-30.md"
)
DEFAULT_BRIDGE_PATH = Path(
    "samples/_probe/newsroom_handoff/offline_topic_mini_episode_capsule_bridge_v1.json"
)
DEFAULT_BRIDGE_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_OFFLINE_TOPIC_MINI_EPISODE_CAPSULE_BRIDGE_V1_2026-06-30.md"
)

SOURCE_USER_REPORTED_FULL_PATH = (
    r"C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage"
    r"\_tmp\newsroom_manual_probe\rss_dry_run_animated_explanation_beat_v1.ymmp"
)

NEXT_AXIS_MINI_EPISODE_WITH_ACCENT = (
    "newsroom-offline-topic-mini-episode-capsule-with-animation-accent-v1"
)
NEXT_AXIS_EPISODE_CAPSULE_ROUTE_AUDIT = "newsroom-episode-capsule-route-audit-v1"
NEXT_AXIS_TOPIC_FIXTURE_ROUTE_AUDIT = "newsroom-rss-topic-fixture-route-audit-v1"
NEXT_AXIS_ANIMATION_POLICY_CLOSED = (
    "newsroom-animation-accent-policy-closed-return-to-episode-capsule-v1"
)

ANIMATION_ACCENT_ALLOWED = [
    "stable pose",
    "one expression event",
    "one short nod/reaction",
    "return to stable pose",
]
ANIMATION_ACCENT_DISABLED = [
    "body forward/back",
    "repeated nodding",
    "mechanical expression cycle",
    "speech balloon",
    "full chaban scene",
]


def write_default_newsroom_offline_topic_mini_episode_capsule_bridge_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    observation = build_default_rss_dry_run_animated_beat_preview_observation(root=base)
    bridge = build_default_offline_topic_mini_episode_capsule_bridge(root=base)
    _write_json(base / DEFAULT_PREVIEW_OBSERVATION_PATH, observation)
    _write_text(
        base / DEFAULT_PREVIEW_OBSERVATION_DOC_PATH,
        render_preview_observation_markdown(observation),
    )
    _write_json(base / DEFAULT_BRIDGE_PATH, bridge)
    _write_text(base / DEFAULT_BRIDGE_DOC_PATH, render_bridge_markdown(bridge))
    return {
        "preview_observation": observation,
        "mini_episode_capsule_bridge": bridge,
    }


def build_default_rss_dry_run_animated_beat_preview_observation(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    return {
        "artifact_id": PREVIEW_OBSERVATION_ID,
        "schema_version": PREVIEW_OBSERVATION_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "source_context": _source_context(base),
        "source_probe_access_state": _source_probe_access_state(base),
        "normalized_preview_observation": _normalized_preview_observation(),
        "visual_gate_closure": _visual_gate_closure(),
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
        "completion_matrix": [
            {"gate": "preview_observation_recorded", "status": True},
            {"gate": "one_beat_visual_integration_gate_closed", "status": True},
            {"gate": "another_visual_preview_requested", "status": False},
            {"gate": "render_or_yym4_launch_requested", "status": False},
        ],
        "selected_next_axis": "mini_episode_capsule_bridge",
    }


def build_default_offline_topic_mini_episode_capsule_bridge(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    beats = _mini_episode_beats()
    return {
        "artifact_id": BRIDGE_ID,
        "schema_version": BRIDGE_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "render_gate": "L0_no_render",
        "actual_audience_acceptance_claimed": False,
        "source_context": _source_context(base),
        "source_preview_observation_path": DEFAULT_PREVIEW_OBSERVATION_PATH.as_posix(),
        "existing_route_assessment": _existing_route_assessment(),
        "offline_topic_input": DRY_RUN_TOPIC_INPUT,
        "mini_episode_capsule": {
            "capsule_id": "offline_topic_mini_episode_capsule_bridge_v1",
            "capsule_status": "diagnostic_contract_bridge_only",
            "source_topic_id": TOPIC_ID,
            "episode_scope": (
                "small offline diagnostic mini episode; content-flow proof only"
            ),
            "beat_count": len(beats),
            "beats": beats,
            "materialization_summary": _materialization_summary(beats),
        },
        "business_goal_outcome_contract": _business_goal_outcome_contract(),
        "recommendation_logic": _recommendation_logic(),
        "selected_next_axis": NEXT_AXIS_MINI_EPISODE_WITH_ACCENT,
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
        "inertia_check": _inertia_check(),
        "completion_matrix": [
            {"gate": "repo_state_verified", "status": True},
            {"gate": "preview_observation_recorded", "status": True},
            {"gate": "one_beat_visual_integration_gate_closed", "status": True},
            {"gate": "mini_episode_capsule_bridge_created", "status": True},
            {"gate": "next_axis_selected", "status": True},
        ],
    }


def render_preview_observation_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Newsroom RSS Dry Run Animated Beat Preview Observation v1",
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
        "Source Probe Access State",
        payload.get("source_probe_access_state"),
    )
    _append_mapping(
        lines,
        "Normalized Preview Observation",
        payload.get("normalized_preview_observation"),
    )
    _append_mapping(lines, "Visual Gate Closure", payload.get("visual_gate_closure"))
    _append_mapping(lines, "Not Accepted Scope", payload.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", payload.get("boundaries"))
    _append_rows(
        lines,
        "Completion Matrix",
        ["gate", "status"],
        payload.get("completion_matrix"),
    )
    lines.extend(["", "## Boundary Note", ""])
    lines.append(
        "This readback records a user-side preview observation only. It closes "
        "the one-beat co-presence gate, but it does not accept production "
        "subtitle/card design or request another visual preview."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_bridge_markdown(payload: dict[str, Any]) -> str:
    capsule = _dict(payload.get("mini_episode_capsule"))
    lines = [
        "# Newsroom Offline Topic Mini Episode Capsule Bridge v1",
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
        "Existing Route Assessment",
        payload.get("existing_route_assessment"),
    )
    _append_mapping(lines, "Offline Topic Input", payload.get("offline_topic_input"))
    _append_mapping(
        lines,
        "Mini Episode Capsule Summary",
        {
            "capsule_id": capsule.get("capsule_id"),
            "capsule_status": capsule.get("capsule_status"),
            "source_topic_id": capsule.get("source_topic_id"),
            "episode_scope": capsule.get("episode_scope"),
            "beat_count": capsule.get("beat_count"),
            "materialization_summary": capsule.get("materialization_summary"),
        },
    )
    _append_rows(
        lines,
        "Mini Episode Beats",
        [
            "beat_id",
            "beat_function",
            "explanation_line",
            "subtitle_or_text_role",
            "minimal_overlay_role",
            "background_animation_accent_role",
            "source_boundary_role",
            "materialization_status",
        ],
        capsule.get("beats"),
    )
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
        "This is a diagnostic bridge from one offline topic-derived beat to a "
        "small capsule contract. It creates no new .ymmp, no render, no "
        "audio/TTS, no live RSS/news fetch, no designed card, and no public "
        "or production acceptance claim."
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _source_context(base: Path) -> dict[str, Any]:
    return {
        "source_rss_dry_run_topic_to_beat_path": (
            DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix()
        ),
        "source_rss_dry_run_contract_path": DEFAULT_RSS_DRY_RUN_CONTRACT_PATH.as_posix(),
        "source_rss_dry_run_doc_path": DEFAULT_RSS_DRY_RUN_DOC_PATH.as_posix(),
        "source_background_animation_mvp_freeze_path": (
            "samples/_probe/newsroom_handoff/background_animation_mvp_freeze_v1.json"
        ),
        "source_episode_capsule_path": (
            "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json"
        ),
        "source_minimal_episode_packet_path": (
            "samples/_probe/newsroom_handoff/minimal_episode_packet.json"
        ),
        "repo_root": str(base.resolve()),
    }


def _source_probe_access_state(base: Path) -> dict[str, Any]:
    repo_relative_path = LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH
    current_workspace_path = base / repo_relative_path
    return {
        "source_observation_role": "user_reported_yym4_preview_via_supervisor_prompt",
        "user_reported_full_path": SOURCE_USER_REPORTED_FULL_PATH,
        "repo_relative_path": repo_relative_path.as_posix(),
        "current_workspace_full_path": str(current_workspace_path.resolve()),
        "current_workspace_target_exists": current_workspace_path.exists(),
        "current_workspace_access_note": (
            "Ignored local .ymmp artifacts are host-local. This slice records "
            "the user's preview observation and does not recreate the .ymmp."
        ),
        "git_check_ignore_result": _git_check_ignore(base, repo_relative_path),
        "artifact_scope": "ignored_local_only",
    }


def _normalized_preview_observation() -> dict[str, Any]:
    return {
        "source_observation_role": "user_opened_rss_dry_run_probe_preview",
        "source_local_probe_path": SOURCE_USER_REPORTED_FULL_PATH,
        "repo_relative_source_probe_path": (
            LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH.as_posix()
        ),
        "yym4_opened": True,
        "rss_dry_run_probe_preview_observed": True,
        "topic_textitem_visible": True,
        "topic_textitem_text": EXPLANATION_LINE,
        "animation_accent_visible": True,
        "same_timing_co_presence": True,
        "timeline_visible_content_summary": (
            "plain topic-derived TextItem and character animation accent in "
            "the same scene timing"
        ),
        "card_like_overlay_visible": False,
        "production_subtitle_design_accepted": False,
        "production_card_design_accepted": False,
        "content_flow_visual_status": "pass_with_boundary",
        "next_axis": "mini_episode_capsule_bridge",
    }


def _visual_gate_closure() -> dict[str, Any]:
    return {
        "one_beat_visual_integration_gate": "closed",
        "gate_result": "pass_with_boundary",
        "closed_by": "user preview readback: topic TextItem and character accent co-present",
        "not_closed_for": [
            "production subtitle design",
            "production card design",
            "render quality",
            "public readiness",
            "animation tuning preference",
        ],
        "reason_no_further_visual_tuning_is_requested": (
            "The required proof was same-scene co-presence. Additional visual "
            "work would reopen card or animation loops, while the current "
            "bottleneck is episode/capsule structure."
        ),
    }


def _existing_route_assessment() -> dict[str, Any]:
    return {
        "one_beat_route": {
            "path": DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix(),
            "status": "available_current_topic_route",
            "use": "per-beat text role, source-boundary role, and frozen accent policy",
        },
        "prior_episode_capsule_route": {
            "path": "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json",
            "status": "structural_precedent_not_current_topic",
            "use": "episode/capsule shape reference only; it comes from an older fake packet",
        },
        "minimal_episode_packet_route": {
            "path": "samples/_probe/newsroom_handoff/minimal_episode_packet.json",
            "status": "fixture_shape_reference_not_materialization_target",
            "use": "beat ordering precedent only; no current RSS dry-run materialization",
        },
        "smallest_safe_bridge": (
            "create a 5-beat contract from the current offline topic without "
            "creating another .ymmp or requesting another preview"
        ),
        "route_clarity": "clear_for_contract_bridge",
    }


def _mini_episode_beats() -> list[dict[str, Any]]:
    base = {
        "source_topic_id": TOPIC_ID,
        "animation_accent_allowed": ANIMATION_ACCENT_ALLOWED,
        "animation_accent_disabled": ANIMATION_ACCENT_DISABLED,
    }
    beats = [
        {
            "beat_id": "offline_topic_mini_ep_beat_01_hook",
            "beat_function": "hook / issue framing",
            "explanation_line": (
                "A topic-like item is not a video yet; first prove the source boundary."
            ),
            "narration_intent": (
                "frame the viewer problem as source-boundary uncertainty before production"
            ),
            "subtitle_or_text_role": "plain TextItem hook; not final subtitle styling",
            "minimal_overlay_role": "short diagnostic label for the issue frame",
            "background_animation_accent_role": (
                "stable pose plus one light reaction after the issue is named"
            ),
            "source_boundary_role": "reminds that the topic is an offline fixture only",
            "materialization_status": "existing_route_candidate",
        },
        {
            "beat_id": "offline_topic_mini_ep_beat_02_key_claim",
            "beat_function": "explanation / key claim",
            "explanation_line": (
                "The key claim stays diagnostic until source truth, rights, and fit are reviewed."
            ),
            "narration_intent": (
                "state the central rule that prevents a dry-run topic from becoming public news"
            ),
            "subtitle_or_text_role": "plain TextItem explanation line",
            "minimal_overlay_role": "source-check label, not a designed card",
            "background_animation_accent_role": "one expression event tied to the key claim",
            "source_boundary_role": "keeps source truth and rights approval unaccepted",
            "materialization_status": "contract_only",
        },
        {
            "beat_id": "offline_topic_mini_ep_beat_03_source_warning",
            "beat_function": "source-boundary warning",
            "explanation_line": EXPLANATION_LINE,
            "narration_intent": (
                "reuse the proven one-beat line as the capsule's explicit boundary warning"
            ),
            "subtitle_or_text_role": "plain diagnostic TextItem boundary warning",
            "minimal_overlay_role": "current proven plain TextItem role; no card-like overlay",
            "background_animation_accent_role": (
                "frozen MVP accent remains subordinate to the warning text"
            ),
            "source_boundary_role": (
                "no live RSS, source quote, external media, or publication readiness"
            ),
            "materialization_status": "existing_route_candidate",
        },
        {
            "beat_id": "offline_topic_mini_ep_beat_04_implication",
            "beat_function": "implication / why it matters",
            "explanation_line": (
                "That boundary lets the structure be checked without pretending it is publishable."
            ),
            "narration_intent": (
                "explain why a private structural capsule is useful before real source work"
            ),
            "subtitle_or_text_role": "plain TextItem implication line",
            "minimal_overlay_role": "small readback label for why the proof matters",
            "background_animation_accent_role": "one short nod/reaction after the implication",
            "source_boundary_role": "separates structural confidence from public-source confidence",
            "materialization_status": "contract_only",
        },
        {
            "beat_id": "offline_topic_mini_ep_beat_05_close",
            "beat_function": "close / next action",
            "explanation_line": (
                "Next, build a small capsule with text roles and one frozen accent per beat."
            ),
            "narration_intent": (
                "name the next diagnostic milestone without asking for another preview now"
            ),
            "subtitle_or_text_role": "plain TextItem next-action line",
            "minimal_overlay_role": "next-step label only",
            "background_animation_accent_role": "return to stable pose at close",
            "source_boundary_role": "keeps live RSS/news and production acceptance out of scope",
            "materialization_status": "contract_only",
        },
    ]
    return [dict(base, **beat) for beat in beats]


def _materialization_summary(beats: list[dict[str, Any]]) -> dict[str, Any]:
    statuses: dict[str, int] = {}
    for beat in beats:
        status = str(beat.get("materialization_status"))
        statuses[status] = statuses.get(status, 0) + 1
    return {
        "status_counts": statuses,
        "local_ymmp_created_in_this_slice": False,
        "materialization_decision": (
            "bridge only; use existing one-beat route as a candidate and defer "
            "multi-beat YMM4 materialization to the selected next axis"
        ),
    }


def _business_goal_outcome_contract() -> dict[str, Any]:
    return {
        "problem_clear": {
            "status": True,
            "rationale": "the user preview closes the local one-beat visual proof loop",
        },
        "offer_clear": {
            "status": True,
            "rationale": "the work moves from one beat to a 5-beat mini episode contract",
        },
        "proof_clear": {
            "status": True,
            "rationale": "the proof is content-flow structure, not production quality",
        },
        "boundary_clear": {
            "status": True,
            "rationale": "card design, subtitle design, animation tuning, render, and live RSS stay closed",
        },
        "next_action_clear": {
            "status": True,
            "rationale": NEXT_AXIS_MINI_EPISODE_WITH_ACCENT,
        },
        "visual_supports_explanation": {
            "status": True,
            "rationale": "the accent policy stays subordinate to narration/text on every beat",
        },
    }


def _recommendation_logic() -> dict[str, Any]:
    return {
        "preferred_default": NEXT_AXIS_MINI_EPISODE_WITH_ACCENT,
        "selected": NEXT_AXIS_MINI_EPISODE_WITH_ACCENT,
        "if_existing_episode_capsule_route_is_unclear": NEXT_AXIS_EPISODE_CAPSULE_ROUTE_AUDIT,
        "if_topic_to_beat_transformation_is_too_synthetic": NEXT_AXIS_TOPIC_FIXTURE_ROUTE_AUDIT,
        "if_animation_should_remain_frozen": NEXT_AXIS_ANIMATION_POLICY_CLOSED,
        "reason": (
            "The bridge is clear enough to move into a small offline capsule "
            "with the frozen accent policy, while avoiding animation-only, "
            "card-polish, render, and live-source loops."
        ),
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_subtitle_design": False,
        "production_card_design": False,
        "production_animation_quality": False,
        "public_upload_or_public_readiness": False,
        "real_rss_or_news_integration": False,
        "real_source_truth_approved": False,
        "external_reference_video_fetch": False,
        "card_redesign_or_density_work": False,
        "dense_script_rewrite": False,
        "render_export_proof": False,
        "audio_or_tts_output": False,
        "actual_order_or_audience_acceptance": False,
        "speech_balloon_visual_acceptance": False,
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
        {
            "gate": "next_axis_remains_mainline_episode_construction",
            "status": NEXT_AXIS_MINI_EPISODE_WITH_ACCENT,
        },
    ]


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
    write_default_newsroom_offline_topic_mini_episode_capsule_bridge_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
