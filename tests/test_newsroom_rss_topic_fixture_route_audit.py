import json
from pathlib import Path

from src.pipeline.newsroom_rss_topic_fixture_route_audit import (
    DEFAULT_READABLE_PREVIEW_OBSERVATION_DOC_PATH,
    DEFAULT_READABLE_PREVIEW_OBSERVATION_PATH,
    DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_DOC_PATH,
    DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH,
    NEXT_AXIS_OFFLINE_FIXTURE_V2_TO_CAPSULE,
    REQUIRED_FIXTURE_SCHEMA_FIELDS,
    VISIBLE_READABLE_LINES,
    build_default_readable_preview_observation,
    build_default_rss_topic_fixture_route_audit,
    render_readable_preview_observation_markdown,
    render_rss_topic_fixture_route_audit_markdown,
    write_default_newsroom_rss_topic_fixture_route_audit_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_rss_topic_fixture_route_audit_artifacts(root=ROOT)


def test_readable_preview_observation_closes_visual_gate() -> None:
    _ensure_artifacts()
    observation = _load(DEFAULT_READABLE_PREVIEW_OBSERVATION_PATH)
    expected = build_default_readable_preview_observation(root=ROOT)

    assert observation == expected
    normalized = observation["normalized_preview_observation"]
    assert normalized["yym4_opened"] is True
    assert normalized["readable_v2_preview_observed"] is True
    assert normalized["five_textitems_visible"] is True
    assert normalized["five_textitems_human_readable"] is True
    assert normalized["debug_label_visible_as_primary_text"] is False
    assert normalized["hook_key_warning_implication_close_visible"] is True
    assert normalized["animation_accent_not_reported_as_blocking"] is True
    assert normalized["readable_materialization_status"] == "pass_with_boundary"
    assert normalized["production_subtitle_design_accepted"] is False
    assert normalized["production_card_design_accepted"] is False
    assert normalized["yym4_visual_gate_status"] == "closed_for_now"
    assert normalized["visible_lines"] == VISIBLE_READABLE_LINES

    closure = observation["visual_gate_closure"]
    assert closure["yym4_visual_gate_status"] == "closed_for_now"
    assert "next bottleneck is the offline topic/RSS fixture route" in closure[
        "reason_no_further_visual_preview_is_requested"
    ]
    assert observation["boundaries"]["additional_YMM4_preview_requested"] is False


def test_audit_identifies_current_route_and_classification() -> None:
    _ensure_artifacts()
    audit = _load(DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH)
    expected = build_default_rss_topic_fixture_route_audit(root=ROOT)

    assert audit == expected
    assert audit["route_id"] == "offline_rss_like_topic_fixture_001_to_mini_episode_capsule_v1"
    assert audit["source_kind"] == "offline_fixture_or_diagnostic"
    classification = audit["current_route_classification"]
    assert classification["diagnostic_only"] is True
    assert classification["reusable_fixture_candidate"] is True
    assert classification["too_synthetic"] is True
    assert classification["blocked"] is False
    assert audit["route_confidence"] == "medium"
    assert audit["selected_next_axis"] == NEXT_AXIS_OFFLINE_FIXTURE_V2_TO_CAPSULE


def test_audit_reports_available_required_missing_and_placeholder_fields() -> None:
    _ensure_artifacts()
    audit = _load(DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH)
    status = audit["field_status"]

    assert audit["topic_fields_currently_available"] == [
        "boundary_note",
        "explanation_angle",
        "key_fact_or_claim",
        "source_kind",
        "title",
        "topic_id",
    ]
    assert audit["fields_required_for_safer_episode_generation"] == REQUIRED_FIXTURE_SCHEMA_FIELDS
    assert status["topic_id"] == "present_exact"
    assert status["title"] == "present_exact"
    assert status["key_claim"] == "present_as_key_fact_or_claim"
    assert status["intended_episode_angle"] == "present_as_explanation_angle"
    assert status["uncertainty_or_boundary"] == "present_as_boundary_note"
    assert status["source_name"] == "missing_or_placeholder_required"
    assert status["source_url_or_placeholder"] == "missing_or_placeholder_required"
    assert status["published_at_or_placeholder"] == "missing_or_placeholder_required"
    assert status["summary"] == "missing_or_placeholder_required"
    assert status["rights_status"] == "missing_or_placeholder_required"
    assert status["excluded_claims"] == "missing_or_placeholder_required"

    blockers = "\n".join(audit["route_blockers"])
    assert "source_name" in blockers
    assert "source_url_or_placeholder" in blockers
    assert "rights_status" in blockers
    assert audit["freshness_placeholder"]["freshness_status"] == (
        "not_evaluable_from_current_fixture"
    )
    assert audit["title_summary_claim_source_url_placeholder_status"] == {
        "title": "present",
        "summary": "missing_explicit_field",
        "claim": "present_as_key_fact_or_claim",
        "source_url_or_placeholder": "missing_explicit_field",
    }


def test_transformation_steps_cover_five_mini_episode_beats() -> None:
    _ensure_artifacts()
    audit = _load(DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH)
    steps = audit["transformation_steps"]

    assert [step["beat"] for step in steps] == [
        "hook",
        "key_claim",
        "source_warning",
        "implication",
        "close",
    ]
    assert all(step["current_derivation"] for step in steps)
    assert "Offline fixture: verify source boundary before production." in [
        step["current_derivation"] for step in steps
    ]
    assert all(step["source_fields_used"] for step in steps)
    assert all(step["audit_note"] for step in steps)


def test_recommended_minimal_fixture_schema_contains_required_fields() -> None:
    _ensure_artifacts()
    audit = _load(DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH)
    schema = audit["minimal_offline_rss_like_topic_schema_recommendation"]

    assert schema["schema_id"] == "offline_rss_like_topic_fixture_v2_minimal"
    assert schema["required_fields"] == REQUIRED_FIXTURE_SCHEMA_FIELDS
    for field in REQUIRED_FIXTURE_SCHEMA_FIELDS:
        assert field in schema["field_purposes"]
    assert schema["example_status_values"]["production_status"] == ["diagnostic_only"]


def test_business_boundaries_and_inertia_keep_scope_offline() -> None:
    _ensure_artifacts()
    audit = _load(DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH)
    observation = _load(DEFAULT_READABLE_PREVIEW_OBSERVATION_PATH)

    assert audit["business_goal_outcome_contract"]["problem_clear"]["status"] is True
    assert audit["business_goal_outcome_contract"]["offer_clear"]["status"] is True
    assert audit["business_goal_outcome_contract"]["proof_clear"]["status"] is True
    assert audit["business_goal_outcome_contract"]["boundary_clear"]["status"] is True
    assert audit["business_goal_outcome_contract"]["visual_supports_explanation"]["status"] is True

    for payload in (audit, observation):
        boundaries = payload["boundaries"]
        assert boundaries["network_fetch_performed"] is False
        assert boundaries["live_RSS_news_fetch_performed"] is False
        assert boundaries["YMM4_launched_by_agent"] is False
        assert boundaries["render_performed_by_agent"] is False
        assert boundaries["audio_tts_generated"] is False
        assert boundaries["card_redesign_performed"] is False
        assert boundaries["animation_tuned"] is False
        assert boundaries["ymmp_or_media_staged_or_committed"] is False

    inertia = {row["gate"]: row["status"] for row in audit["inertia_check"]}
    assert inertia["no_YMM4_visual_loop"] is True
    assert inertia["no_live_RSS_or_network_fetch"] is True
    assert inertia["next_axis_remains_topic_RSS_to_episode_construction"] == (
        NEXT_AXIS_OFFLINE_FIXTURE_V2_TO_CAPSULE
    )


def test_docs_match_renderers_and_tracked_outputs_are_not_media() -> None:
    _ensure_artifacts()
    observation = _load(DEFAULT_READABLE_PREVIEW_OBSERVATION_PATH)
    audit = _load(DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH)

    assert (ROOT / DEFAULT_READABLE_PREVIEW_OBSERVATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_readable_preview_observation_markdown(observation)
    assert (ROOT / DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_rss_topic_fixture_route_audit_markdown(audit)

    generated_paths = [
        DEFAULT_READABLE_PREVIEW_OBSERVATION_PATH,
        DEFAULT_READABLE_PREVIEW_OBSERVATION_DOC_PATH,
        DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_PATH,
        DEFAULT_RSS_TOPIC_FIXTURE_ROUTE_AUDIT_DOC_PATH,
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)

    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in generated_paths)
    assert "http://" not in combined
    assert "https://" not in combined
    assert '"YMM4_launched_by_agent": true' not in combined
    assert '"render_performed_by_agent": true' not in combined
    assert '"audio_tts_generated": true' not in combined
