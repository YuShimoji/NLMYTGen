import json
from pathlib import Path

from src.pipeline.newsroom_offline_rss_like_topic_fixture_v2 import (
    DEFAULT_CAPSULE_PATH,
    DEFAULT_FIXTURE_V2_PATH,
    DEFAULT_SCHEMA_CONTRACT_PATH,
    build_default_fixture_v2_schema_contract,
    build_default_fixture_v2_to_mini_episode_capsule,
    build_default_offline_rss_like_topic_fixture_v2,
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts,
)
from src.pipeline.newsroom_rss_topic_fixture_route_hardening import (
    DEFAULT_HARDENING_DOC_PATH,
    DEFAULT_HARDENING_PATH,
    DEFAULT_VALIDATION_PATH,
    PLACEHOLDER_CAPABLE_FIELDS,
    SELECTED_NEXT_AXIS,
    build_fixture_route_hardening,
    build_fixture_v2_validation,
    render_fixture_route_hardening_markdown,
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts,
)
from src.pipeline.newsroom_rss_topic_fixture_route_audit import (
    REQUIRED_FIXTURE_SCHEMA_FIELDS,
)


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts(root=ROOT)
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts(root=ROOT)


def test_validation_and_hardening_match_builders() -> None:
    _ensure_artifacts()
    fixture = build_default_offline_rss_like_topic_fixture_v2(root=ROOT)
    schema = build_default_fixture_v2_schema_contract()
    capsule = build_default_fixture_v2_to_mini_episode_capsule(
        root=ROOT,
        fixture=fixture,
        schema_contract=schema,
    )
    expected_validation = build_fixture_v2_validation(
        fixture=fixture,
        schema_contract=schema,
        capsule=capsule,
    )
    expected_hardening = build_fixture_route_hardening(
        fixture=fixture,
        schema_contract=schema,
        capsule=capsule,
        validation=expected_validation,
    )

    assert _load(DEFAULT_FIXTURE_V2_PATH) == fixture
    assert _load(DEFAULT_SCHEMA_CONTRACT_PATH) == schema
    assert _load(DEFAULT_CAPSULE_PATH) == capsule
    assert _load(DEFAULT_VALIDATION_PATH) == expected_validation
    assert _load(DEFAULT_HARDENING_PATH) == expected_hardening


def test_field_validation_keeps_required_fields_and_placeholders_explicit() -> None:
    _ensure_artifacts()
    validation = _load(DEFAULT_VALIDATION_PATH)
    rows = {row["field_name"]: row for row in validation["field_validation"]}

    assert list(rows) == REQUIRED_FIXTURE_SCHEMA_FIELDS
    assert rows["topic_id"]["value_kind"] == "real_value"
    assert rows["title"]["value_kind"] == "real_value"
    assert rows["summary"]["value_kind"] == "real_value"
    assert rows["source_url_or_placeholder"]["value_kind"] == "explicit_placeholder"
    assert rows["published_at_or_placeholder"]["value_kind"] == "explicit_placeholder"
    assert rows["rights_status"]["value_kind"] == "explicit_placeholder"
    assert rows["excluded_claims"]["value_kind"] == "real_value"
    assert rows["production_status"]["value_kind"] == "real_value"

    assert rows["source_url_or_placeholder"]["production_blocker"] is True
    assert rows["published_at_or_placeholder"]["production_blocker"] is True
    assert rows["rights_status"]["production_blocker"] is True
    assert rows["source_url_or_placeholder"]["diagnostic_allowed"] is True
    assert rows["published_at_or_placeholder"]["diagnostic_allowed"] is True
    assert rows["rights_status"]["diagnostic_allowed"] is True
    assert rows["production_status"]["production_blocker"] is False


def test_placeholder_readback_reports_counts_and_blocker_fields() -> None:
    _ensure_artifacts()
    validation = _load(DEFAULT_VALIDATION_PATH)
    readback = validation["placeholder_readback"]

    assert [row["field_name"] for row in readback["placeholder_fields"]] == (
        PLACEHOLDER_CAPABLE_FIELDS
    )
    assert readback["explicit_placeholder_fields"] == PLACEHOLDER_CAPABLE_FIELDS
    assert readback["explicit_placeholder_count"] == 5
    assert readback["unmarked_placeholder_fields"] == []
    assert readback["unmarked_placeholder_count"] == 0
    assert readback["missing_required_count"] == 0
    assert readback["production_blocker_fields"] == PLACEHOLDER_CAPABLE_FIELDS
    assert readback["production_blocker_count"] == 5


def test_route_classification_and_capsule_readiness_select_next_axis() -> None:
    _ensure_artifacts()
    hardening = _load(DEFAULT_HARDENING_PATH)
    classification = hardening["route_classification"]
    states = hardening["route_boundary_states"]
    readiness = hardening["capsule_readiness"]

    assert classification["diagnostic_only"] is True
    assert classification["reusable_fixture_candidate"] is True
    assert classification["still_synthetic"] is True
    assert classification["blocked"] is False
    assert classification["production_blocked"] is True
    assert classification["live_boundary_ready_candidate"] is False
    assert classification["route_confidence"] == "medium_high"

    assert states["diagnostic_only"] is True
    assert states["reusable_offline_fixture"] is True
    assert states["blocked_missing_required_fields"] is False
    assert states["blocked_unmarked_placeholder"] is False
    assert states["blocked_rights_unknown"] is True
    assert states["blocked_source_boundary_unknown"] is False
    assert states["live_boundary_ready_candidate"] is False

    assert readiness["diagnostic_capsule_ready"] is True
    assert readiness["reusable_offline_fixture_ready"] is True
    assert readiness["live_boundary_plan_ready"] is False
    assert readiness["production_script_ready"] is False
    assert hardening["next_recommended_axis"] == SELECTED_NEXT_AXIS


def test_blockers_business_contract_and_docs_are_stable() -> None:
    _ensure_artifacts()
    hardening = _load(DEFAULT_HARDENING_PATH)

    blockers = "\n".join(hardening["blockers"])
    assert "placeholder source URL" in blockers
    assert "placeholder published timestamp" in blockers
    assert "rights_status remains unknown placeholder" in blockers
    assert "freshness_status remains placeholder" in blockers
    assert "attribution_note is fixture-only" in blockers
    assert "source_reliability_note does not score" in blockers

    outcome = hardening["business_goal_outcome_contract"]
    assert outcome["problem_clear"]["status"] is True
    assert outcome["offer_clear"]["status"] is True
    assert outcome["proof_clear"]["status"] is True
    assert outcome["boundary_clear"]["status"] is True
    assert outcome["next_action_clear"]["rationale"] == SELECTED_NEXT_AXIS
    assert outcome["visual_supports_explanation"]["status"] is True

    assert (ROOT / DEFAULT_HARDENING_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_fixture_route_hardening_markdown(hardening)


def test_unmarked_placeholder_and_missing_required_fields_block_validation() -> None:
    fixture = build_default_offline_rss_like_topic_fixture_v2(root=ROOT)
    schema = build_default_fixture_v2_schema_contract()
    capsule = build_default_fixture_v2_to_mini_episode_capsule(
        root=ROOT,
        fixture=fixture,
        schema_contract=schema,
    )
    fixture.pop("summary")
    fixture["source_url_or_placeholder"] = "offline-source-boundary-v2-no-live-url"

    validation = build_fixture_v2_validation(
        fixture=fixture,
        schema_contract=schema,
        capsule=capsule,
    )

    rows = {row["field_name"]: row for row in validation["field_validation"]}
    assert rows["summary"]["value_kind"] == "missing"
    assert rows["source_url_or_placeholder"]["value_kind"] == "invalid"
    assert validation["placeholder_readback"]["unmarked_placeholder_fields"] == [
        "source_url_or_placeholder"
    ]
    assert validation["route_boundary_states"]["blocked_missing_required_fields"] is True
    assert validation["route_boundary_states"]["blocked_unmarked_placeholder"] is True
    assert validation["route_classification"]["blocked"] is True


def test_scope_boundaries_do_not_create_visual_media_or_live_fetch_outputs() -> None:
    _ensure_artifacts()
    generated_paths = [
        DEFAULT_VALIDATION_PATH,
        DEFAULT_HARDENING_PATH,
        DEFAULT_HARDENING_DOC_PATH,
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)

    hardening = _load(DEFAULT_HARDENING_PATH)
    boundaries = hardening["boundaries"]
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

    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in generated_paths)
    assert "http" + "://" not in combined
    assert "https" + "://" not in combined
    assert '"YMM4_launched_by_agent": ' + "true" not in combined
    assert '"render_performed_by_agent": ' + "true" not in combined
    assert '"audio_tts_generated": ' + "true" not in combined
