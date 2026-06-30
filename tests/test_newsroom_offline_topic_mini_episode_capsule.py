import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_offline_topic_mini_episode_capsule import (
    ANIMATION_ASSIGNMENTS,
    DEFAULT_CAPSULE_CONTRACT_PATH,
    DEFAULT_CAPSULE_DOC_PATH,
    DEFAULT_CAPSULE_PATH,
    LOCAL_IGNORED_CAPSULE_YMMP_PATH,
    NEXT_AXIS_MATERIALIZATION,
    build_default_offline_topic_mini_episode_capsule,
    build_default_offline_topic_mini_episode_capsule_contract,
    render_capsule_markdown,
    write_default_newsroom_offline_topic_mini_episode_capsule_artifacts,
)
from src.pipeline.newsroom_offline_topic_mini_episode_capsule_bridge import (
    DEFAULT_BRIDGE_PATH,
)
from src.pipeline.newsroom_rss_dry_run_to_animated_explanation_beat import (
    DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH,
    TOPIC_ID,
)


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_offline_topic_mini_episode_capsule_artifacts(root=ROOT)


def test_capsule_artifact_matches_builder_and_identity() -> None:
    _ensure_artifacts()
    payload = build_default_offline_topic_mini_episode_capsule(root=ROOT)
    artifact = _load(DEFAULT_CAPSULE_PATH)

    assert artifact == payload
    assert artifact["production_status"] == "diagnostic_only"
    assert artifact["render_gate"] == "L0_no_render"
    assert artifact["live_fetch_used"] is False
    assert artifact["source_bridge_path"] == DEFAULT_BRIDGE_PATH.as_posix()
    assert artifact["source_topic_fixture_path"] == (
        DEFAULT_RSS_DRY_RUN_TOPIC_TO_BEAT_PATH.as_posix()
    )
    assert artifact["selected_next_axis"] == NEXT_AXIS_MATERIALIZATION


def test_capsule_has_five_ordered_beats_with_required_roles() -> None:
    _ensure_artifacts()
    capsule = _load(DEFAULT_CAPSULE_PATH)
    beats = capsule["episode_capsule"]["beats"]

    assert capsule["episode_capsule"]["beat_count"] == 5
    assert [beat["beat_function"] for beat in beats] == [
        "hook / issue framing",
        "explanation / key claim",
        "source-boundary warning",
        "implication / why it matters",
        "close / next action",
    ]
    required = {
        "beat_id",
        "source_topic_id",
        "beat_function",
        "explanation_line",
        "narration_intent",
        "subtitle_or_text_role",
        "minimal_overlay_role",
        "background_animation_accent_role",
        "source_boundary_role",
        "materialization_role",
        "review_status",
        "route_candidate",
        "materialization_status",
        "not_accepted_scope",
    }
    for beat in beats:
        assert required <= set(beat)
        assert beat["source_topic_id"] == TOPIC_ID
        assert beat["review_status"] == "diagnostic_review_ready"
        assert beat["subtitle_or_text_role"].startswith("plain")
        assert beat["minimal_overlay_role"]
        assert beat["source_boundary_role"]


def test_animation_assignments_stay_frozen_and_optional() -> None:
    _ensure_artifacts()
    capsule = _load(DEFAULT_CAPSULE_PATH)
    beats = capsule["episode_capsule"]["beats"]
    assignments = [beat["animation_assignment"] for beat in beats]

    assert set(assignments) <= ANIMATION_ASSIGNMENTS
    assert "none" in assignments
    assert "expression_plus_short_nod" in assignments
    summary = capsule["episode_capsule"]["animation_accent_summary"]
    assert summary["policy_status"] == "frozen_mvp_policy_carried_forward"
    assert summary["animation_optional_not_forced"] is True
    assert "animation-only probe loop" in summary["disabled"]
    assert "tempo-only loop" in summary["disabled"]


def test_local_ymmp_materialization_is_deferred_and_ignored_path_is_verified() -> None:
    _ensure_artifacts()
    capsule = _load(DEFAULT_CAPSULE_PATH)
    access = capsule["local_artifact_access"]
    materialization = capsule["episode_capsule"]["materialization_summary"]

    assert access["repo_relative_path"] == LOCAL_IGNORED_CAPSULE_YMMP_PATH.as_posix()
    assert access["target_exists"] is False
    assert access["access_state"] == "not_created_deferred"
    assert access["git_check_ignore_result"]["ignored"] is True
    assert materialization["local_ymmp_created_in_this_slice"] is False
    assert materialization["local_ymmp_materialization_status"] == "blocked_or_deferred"

    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-v",
            "--",
            LOCAL_IGNORED_CAPSULE_YMMP_PATH.as_posix(),
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


def test_mainline_route_records_fake_packet_precedent_and_next_work() -> None:
    _ensure_artifacts()
    capsule = _load(DEFAULT_CAPSULE_PATH)
    route = capsule["mainline_route"]

    assert route["route_name"] == "offline_topic_bridge_to_diagnostic_mini_episode_capsule"
    assert route["route_confidence"] == "high"
    assert any("fake-packet" in blocker for blocker in route["route_blockers"])
    assert NEXT_AXIS_MATERIALIZATION in route["next_required_route_work"]
    assert route["local_ymmp_materialization_status"] == "not_created_deferred"


def test_contract_artifact_matches_builder_and_carries_policies() -> None:
    _ensure_artifacts()
    contract = _load(DEFAULT_CAPSULE_CONTRACT_PATH)
    expected = build_default_offline_topic_mini_episode_capsule_contract(root=ROOT)

    assert contract == expected
    assert contract["production_status"] == "diagnostic_only"
    assert contract["render_gate"] == "L0_no_render"
    assert contract["beat_count"] == 5
    assert len(contract["beat_contract"]) == 5
    assert contract["animation_accent_policy"]["do_not_force_animation_onto_every_beat"] is True
    assert contract["text_overlay_policy"]["polished_card_design"] is False
    assert contract["materialization_policy"]["local_ymmp_created_in_this_slice"] is False
    assert contract["materialization_policy"]["next_axis"] == NEXT_AXIS_MATERIALIZATION


def test_business_boundaries_and_docs_match_renderer() -> None:
    _ensure_artifacts()
    capsule = _load(DEFAULT_CAPSULE_PATH)

    outcome = capsule["business_goal_outcome_contract"]
    assert outcome["problem_clear"]["status"] is True
    assert outcome["offer_clear"]["status"] is True
    assert outcome["proof_clear"]["status"] is True
    assert outcome["boundary_clear"]["status"] is True
    assert outcome["next_action_clear"]["rationale"] == NEXT_AXIS_MATERIALIZATION
    assert outcome["visual_supports_explanation"]["status"] is True

    boundaries = capsule["boundaries"]
    assert boundaries["network_fetch_performed"] is False
    assert boundaries["live_RSS_news_fetch_performed"] is False
    assert boundaries["YMM4_launched_by_agent"] is False
    assert boundaries["render_performed_by_agent"] is False
    assert boundaries["audio_tts_generated"] is False
    assert boundaries["card_redesign_performed"] is False
    assert boundaries["animation_tuned"] is False
    assert boundaries["local_ignored_ymmp_created_in_this_slice"] is False
    assert boundaries["ymmp_or_media_staged_or_committed"] is False

    assert (ROOT / DEFAULT_CAPSULE_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_capsule_markdown(capsule)


def test_outputs_do_not_include_tracked_media_or_execution_relapse() -> None:
    _ensure_artifacts()
    generated_paths = [
        DEFAULT_CAPSULE_PATH,
        DEFAULT_CAPSULE_DOC_PATH,
        DEFAULT_CAPSULE_CONTRACT_PATH,
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)

    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in generated_paths)
    combined_lower = combined.lower()
    assert "http://" not in combined
    assert "https://" not in combined
    assert '"YMM4_launched_by_agent": true' not in combined
    assert '"render_performed_by_agent": true' not in combined
    assert '"audio_tts_generated": true' not in combined
    assert '"local_ignored_ymmp_created_in_this_slice": true' not in combined
    assert "fetch live" not in combined_lower
    assert "render again" not in combined_lower
    assert "generate tts" not in combined_lower
