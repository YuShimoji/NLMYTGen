import json
from pathlib import Path

from src.pipeline.newsroom_offline_rss_like_topic_fixture_v2 import (
    ALLOWED_ANIMATION_ASSIGNMENTS,
    BEAT_FUNCTIONS,
    DEFAULT_CAPSULE_DOC_PATH,
    DEFAULT_CAPSULE_PATH,
    DEFAULT_FIXTURE_V2_PATH,
    DEFAULT_SCHEMA_CONTRACT_PATH,
    NEXT_AXIS_ROUTE_HARDENING,
    RECOMMENDED_FIXTURE_FIELDS,
    TOPIC_ID,
    build_default_fixture_v2_schema_contract,
    build_default_fixture_v2_to_mini_episode_capsule,
    build_default_offline_rss_like_topic_fixture_v2,
    render_fixture_v2_capsule_markdown,
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts,
)
from src.pipeline.newsroom_rss_topic_fixture_route_audit import (
    REQUIRED_FIXTURE_SCHEMA_FIELDS,
)


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts(root=ROOT)


def test_fixture_v2_matches_builder_and_fills_required_fields() -> None:
    _ensure_artifacts()
    fixture = _load(DEFAULT_FIXTURE_V2_PATH)
    expected = build_default_offline_rss_like_topic_fixture_v2(root=ROOT)

    assert fixture == expected
    assert fixture["topic_id"] == TOPIC_ID
    assert fixture["production_status"] == "diagnostic_only"
    assert fixture["diagnostic_only"] is True
    for field in REQUIRED_FIXTURE_SCHEMA_FIELDS:
        assert field in fixture
        assert fixture[field]

    assert fixture["source_name"] == "Offline diagnostic newsroom fixture"
    assert fixture["source_url_or_placeholder"].startswith("placeholder:")
    assert fixture["published_at_or_placeholder"].startswith("placeholder:")
    assert fixture["rights_status"].startswith("placeholder:")
    assert fixture["source_kind"] == "offline_rss_like_fixture_v2"
    assert fixture["freshness_status"] == "placeholder_not_evaluable_without_live_source"
    assert fixture["v2_improvement_over_v1"]["stronger_than_v1"] is True
    assert fixture["v2_improvement_over_v1"]["still_synthetic"] is True
    assert fixture["source_boundary_fields"]["live_RSS_news_fetch_performed"] is False


def test_schema_contract_declares_required_recommended_and_placeholder_policy() -> None:
    _ensure_artifacts()
    schema = _load(DEFAULT_SCHEMA_CONTRACT_PATH)
    expected = build_default_fixture_v2_schema_contract()

    assert schema == expected
    assert schema["required_fields"] == REQUIRED_FIXTURE_SCHEMA_FIELDS
    assert schema["recommended_additional_fields"] == RECOMMENDED_FIXTURE_FIELDS
    for field in REQUIRED_FIXTURE_SCHEMA_FIELDS + RECOMMENDED_FIXTURE_FIELDS:
        assert field in schema["field_purposes"]
    assert schema["required_placeholder_policy"]["must_be_explicit"] is True
    assert schema["required_placeholder_policy"]["must_not_be_treated_as_live_source"] is True
    assert "YMM4 project materialization" in schema["episode_generation_policy"][
        "forbidden_output"
    ]


def test_capsule_matches_builder_and_contains_five_required_beats() -> None:
    _ensure_artifacts()
    capsule = _load(DEFAULT_CAPSULE_PATH)
    expected = build_default_fixture_v2_to_mini_episode_capsule(root=ROOT)

    assert capsule == expected
    assert capsule["production_status"] == "diagnostic_only"
    assert capsule["render_gate"] == "L0_no_render"
    assert capsule["selected_next_axis"] == NEXT_AXIS_ROUTE_HARDENING

    beats = capsule["mini_episode_capsule"]["beats"]
    assert capsule["mini_episode_capsule"]["beat_count"] == 5
    assert [beat["beat_function"] for beat in beats] == BEAT_FUNCTIONS
    required_beat_fields = {
        "beat_id",
        "source_topic_id",
        "beat_function",
        "explanation_line",
        "narration_intent",
        "subtitle_or_text_role",
        "minimal_overlay_role",
        "background_animation_accent_role",
        "source_boundary_role",
        "source_fields_used",
        "excluded_claims_applied",
        "production_status",
        "not_accepted_scope",
    }
    for beat in beats:
        assert required_beat_fields <= set(beat)
        assert beat["source_topic_id"] == TOPIC_ID
        assert beat["production_status"] == "diagnostic_only"
        assert beat["subtitle_or_text_role"].startswith("plain diagnostic TextItem")
        assert beat["minimal_overlay_role"]
        assert beat["source_fields_used"]
        assert beat["excluded_claims_applied"]


def test_capsule_maps_animation_assignments_without_reopening_animation_loop() -> None:
    _ensure_artifacts()
    capsule = _load(DEFAULT_CAPSULE_PATH)
    beats = capsule["mini_episode_capsule"]["beats"]
    assignments = [beat["animation_accent_assignment"] for beat in beats]
    expected_beat_assignments = [
        "stable_pose_only",
        "expression_event",
        "expression_plus_short_nod",
        "short_nod_reaction",
        "none",
    ]

    assert assignments == expected_beat_assignments
    assert set(assignments) == set(ALLOWED_ANIMATION_ASSIGNMENTS)
    for beat in beats:
        assert beat["background_animation_accent_role"] == beat["animation_accent_assignment"]

    summary = capsule["mini_episode_capsule"]["animation_accent_summary"]
    assert summary["policy_status"] == "frozen_mvp_policy_carried_forward"
    assert summary["allowed_assignments"] == ALLOWED_ANIMATION_ASSIGNMENTS
    assert summary["animation_optional_not_forced"] is True
    assert "body forward/back" in summary["disabled"]
    assert "mechanical expression cycling" in summary["disabled"]
    assert "designed card layout" in summary["disabled"]


def test_fixture_readback_transformation_and_route_assessment() -> None:
    _ensure_artifacts()
    capsule = _load(DEFAULT_CAPSULE_PATH)
    readback = capsule["fixture_readback"]
    transformation = capsule["transformation_readback"]
    route = capsule["route_assessment"]

    assert readback["topic_id"] == TOPIC_ID
    assert readback["missing_required_fields"] == []
    assert readback["required_fields_present"] == REQUIRED_FIXTURE_SCHEMA_FIELDS
    assert readback["placeholder_count"] == 4
    assert readback["source_boundary_fields"]["network_fetch_performed"] is False

    assert transformation["source_topic_id"] == TOPIC_ID
    assert transformation["beat_count"] == 5
    assert transformation["beat_functions"] == BEAT_FUNCTIONS
    assert transformation["network_fetch_performed"] is False
    assert transformation["live_RSS_news_fetch_performed"] is False
    assert transformation["source_boundary_propagated"] is True
    assert transformation["excluded_claims_applied_to_every_beat"] is True

    classification = route["current_route_classification"]
    assert route["route_classification"] == "current_partial"
    assert classification["diagnostic_only"] is True
    assert classification["reusable_fixture_candidate"] is True
    assert classification["still_synthetic"] is True
    assert classification["stronger_than_v1"] is True
    assert classification["blocked"] is False
    assert route["route_confidence"] == "medium"
    assert NEXT_AXIS_ROUTE_HARDENING in route["next_required_route_work"]


def test_business_boundaries_docs_and_scans_stay_in_scope() -> None:
    _ensure_artifacts()
    capsule = _load(DEFAULT_CAPSULE_PATH)

    outcome = capsule["business_goal_outcome_contract"]
    assert outcome["problem_clear"]["status"] is True
    assert outcome["offer_clear"]["status"] is True
    assert outcome["proof_clear"]["status"] is True
    assert outcome["boundary_clear"]["status"] is True
    assert outcome["next_action_clear"]["rationale"] == NEXT_AXIS_ROUTE_HARDENING
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
    assert boundaries["local_ignored_ymmp_modified_in_this_slice"] is False
    assert boundaries["ymmp_or_media_staged_or_committed"] is False

    inertia = {row["gate"]: row["status"] for row in capsule["inertia_check"]}
    assert inertia["no_animation_only_loop"] is True
    assert inertia["no_card_polish_loop"] is True
    assert inertia["no_live_RSS_or_network_fetch"] is True
    assert inertia["no_local_ymmp_creation_or_modification"] is True

    assert (ROOT / DEFAULT_CAPSULE_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_fixture_v2_capsule_markdown(capsule)


def test_outputs_do_not_create_tracked_media_or_live_fetch_relapse() -> None:
    _ensure_artifacts()
    generated_paths = [
        DEFAULT_FIXTURE_V2_PATH,
        DEFAULT_SCHEMA_CONTRACT_PATH,
        DEFAULT_CAPSULE_PATH,
        DEFAULT_CAPSULE_DOC_PATH,
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)

    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in generated_paths)
    combined_lower = combined.lower()
    assert "http" + "://" not in combined
    assert "https" + "://" not in combined
    assert '"YMM4_launched_by_agent": true' not in combined
    assert '"render_performed_by_agent": true' not in combined
    assert '"audio_tts_generated": true' not in combined
    assert '"local_ignored_ymmp_created_in_this_slice": true' not in combined
    assert '"local_ignored_ymmp_modified_in_this_slice": true' not in combined
    assert "requests" + "." not in combined_lower
    assert "htt" + "px" not in combined_lower
    assert "url" + "lib" not in combined_lower
