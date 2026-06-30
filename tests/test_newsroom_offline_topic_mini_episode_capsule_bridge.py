import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_offline_topic_mini_episode_capsule_bridge import (
    ANIMATION_ACCENT_ALLOWED,
    ANIMATION_ACCENT_DISABLED,
    DEFAULT_BRIDGE_DOC_PATH,
    DEFAULT_BRIDGE_PATH,
    DEFAULT_PREVIEW_OBSERVATION_DOC_PATH,
    DEFAULT_PREVIEW_OBSERVATION_PATH,
    NEXT_AXIS_MINI_EPISODE_WITH_ACCENT,
    build_default_offline_topic_mini_episode_capsule_bridge,
    build_default_rss_dry_run_animated_beat_preview_observation,
    render_bridge_markdown,
    render_preview_observation_markdown,
    write_default_newsroom_offline_topic_mini_episode_capsule_bridge_artifacts,
)
from src.pipeline.newsroom_rss_dry_run_to_animated_explanation_beat import (
    EXPLANATION_LINE,
    LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH,
    TOPIC_ID,
)


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_offline_topic_mini_episode_capsule_bridge_artifacts(
        root=ROOT
    )


def test_preview_observation_records_bounded_visual_pass() -> None:
    _ensure_artifacts()
    payload = build_default_rss_dry_run_animated_beat_preview_observation(root=ROOT)
    artifact = _load(DEFAULT_PREVIEW_OBSERVATION_PATH)

    assert artifact == payload
    assert artifact["production_status"] == "diagnostic_only"
    assert artifact["render_gate"] == "L0_no_render"

    observation = artifact["normalized_preview_observation"]
    assert observation["yym4_opened"] is True
    assert observation["rss_dry_run_probe_preview_observed"] is True
    assert observation["topic_textitem_visible"] is True
    assert observation["topic_textitem_text"] == EXPLANATION_LINE
    assert observation["animation_accent_visible"] is True
    assert observation["same_timing_co_presence"] is True
    assert observation["card_like_overlay_visible"] is False
    assert observation["production_subtitle_design_accepted"] is False
    assert observation["production_card_design_accepted"] is False
    assert observation["content_flow_visual_status"] == "pass_with_boundary"

    closure = artifact["visual_gate_closure"]
    assert closure["one_beat_visual_integration_gate"] == "closed"
    assert "production subtitle design" in closure["not_closed_for"]


def test_preview_observation_keeps_local_ymmp_host_local_and_ignored() -> None:
    _ensure_artifacts()
    artifact = _load(DEFAULT_PREVIEW_OBSERVATION_PATH)
    access = artifact["source_probe_access_state"]

    assert access["repo_relative_path"] == (
        LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH.as_posix()
    )
    assert access["artifact_scope"] == "ignored_local_only"
    assert access["git_check_ignore_result"]["ignored"] is True

    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-v",
            "--",
            LOCAL_IGNORED_RSS_DRY_RUN_ANIMATED_EXPLANATION_BEAT_PATH.as_posix(),
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "_tmp/" in result.stdout


def test_bridge_builds_five_beat_mini_episode_contract() -> None:
    _ensure_artifacts()
    payload = build_default_offline_topic_mini_episode_capsule_bridge(root=ROOT)
    artifact = _load(DEFAULT_BRIDGE_PATH)

    assert artifact == payload
    assert artifact["production_status"] == "diagnostic_only"
    assert artifact["render_gate"] == "L0_no_render"
    assert artifact["selected_next_axis"] == NEXT_AXIS_MINI_EPISODE_WITH_ACCENT

    capsule = artifact["mini_episode_capsule"]
    beats = capsule["beats"]
    assert capsule["source_topic_id"] == TOPIC_ID
    assert capsule["beat_count"] == 5
    assert [beat["beat_function"] for beat in beats] == [
        "hook / issue framing",
        "explanation / key claim",
        "source-boundary warning",
        "implication / why it matters",
        "close / next action",
    ]
    assert beats[2]["explanation_line"] == EXPLANATION_LINE


def test_each_bridge_beat_has_required_roles_and_animation_limits() -> None:
    _ensure_artifacts()
    bridge = _load(DEFAULT_BRIDGE_PATH)
    statuses = set()

    required_fields = {
        "beat_id",
        "source_topic_id",
        "beat_function",
        "explanation_line",
        "narration_intent",
        "subtitle_or_text_role",
        "minimal_overlay_role",
        "background_animation_accent_role",
        "source_boundary_role",
        "animation_accent_allowed",
        "animation_accent_disabled",
        "materialization_status",
    }
    allowed_statuses = {
        "contract_only",
        "existing_route_candidate",
        "blocked",
        "not_attempted",
    }
    for beat in bridge["mini_episode_capsule"]["beats"]:
        assert required_fields <= set(beat)
        assert beat["source_topic_id"] == TOPIC_ID
        assert beat["animation_accent_allowed"] == ANIMATION_ACCENT_ALLOWED
        assert beat["animation_accent_disabled"] == ANIMATION_ACCENT_DISABLED
        assert beat["materialization_status"] in allowed_statuses
        statuses.add(beat["materialization_status"])

    assert "existing_route_candidate" in statuses
    assert "contract_only" in statuses
    assert bridge["mini_episode_capsule"]["materialization_summary"][
        "local_ymmp_created_in_this_slice"
    ] is False


def test_bridge_business_readback_and_recommendation_logic() -> None:
    _ensure_artifacts()
    bridge = _load(DEFAULT_BRIDGE_PATH)

    outcome = bridge["business_goal_outcome_contract"]
    assert outcome["problem_clear"]["status"] is True
    assert outcome["offer_clear"]["status"] is True
    assert outcome["proof_clear"]["status"] is True
    assert outcome["boundary_clear"]["status"] is True
    assert outcome["next_action_clear"]["rationale"] == NEXT_AXIS_MINI_EPISODE_WITH_ACCENT
    assert outcome["visual_supports_explanation"]["status"] is True

    recommendation = bridge["recommendation_logic"]
    assert recommendation["preferred_default"] == NEXT_AXIS_MINI_EPISODE_WITH_ACCENT
    assert recommendation["selected"] == NEXT_AXIS_MINI_EPISODE_WITH_ACCENT
    assert recommendation["if_existing_episode_capsule_route_is_unclear"]
    assert recommendation["if_topic_to_beat_transformation_is_too_synthetic"]
    assert recommendation["if_animation_should_remain_frozen"]


def test_bridge_boundaries_do_not_reopen_forbidden_work() -> None:
    _ensure_artifacts()
    bridge = _load(DEFAULT_BRIDGE_PATH)
    observation = _load(DEFAULT_PREVIEW_OBSERVATION_PATH)

    for payload in [bridge, observation]:
        boundaries = payload["boundaries"]
        assert boundaries["network_fetch_performed"] is False
        assert boundaries["live_RSS_news_fetch_performed"] is False
        assert boundaries["YMM4_launched_by_agent"] is False
        assert boundaries["render_performed_by_agent"] is False
        assert boundaries["audio_tts_generated"] is False
        assert boundaries["card_redesign_performed"] is False
        assert boundaries["animation_tuned"] is False
        assert boundaries["local_ignored_ymmp_created_in_this_slice"] is False
        assert boundaries["ymmp_or_media_staged_or_committed"] is False


def test_docs_match_renderers_and_tracked_outputs_are_not_media() -> None:
    _ensure_artifacts()
    observation = _load(DEFAULT_PREVIEW_OBSERVATION_PATH)
    bridge = _load(DEFAULT_BRIDGE_PATH)

    assert (ROOT / DEFAULT_PREVIEW_OBSERVATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_preview_observation_markdown(observation)
    assert (ROOT / DEFAULT_BRIDGE_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_bridge_markdown(bridge)

    generated_paths = [
        DEFAULT_PREVIEW_OBSERVATION_PATH,
        DEFAULT_PREVIEW_OBSERVATION_DOC_PATH,
        DEFAULT_BRIDGE_PATH,
        DEFAULT_BRIDGE_DOC_PATH,
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)
