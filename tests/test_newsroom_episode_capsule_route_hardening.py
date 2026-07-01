import json
from pathlib import Path

from src.pipeline.newsroom_episode_capsule_route_hardening import (
    DEFAULT_EPISODE_CAPSULE_ROUTE_HARDENING_DOC_PATH,
    DEFAULT_EPISODE_CAPSULE_ROUTE_HARDENING_PATH,
    DEFAULT_HARDENED_CAPSULE_PATH,
    SELECTED_NEXT_AXIS,
    build_episode_capsule_route_hardening,
    build_hardened_episode_capsule,
    render_episode_capsule_route_hardening_markdown,
    write_default_newsroom_episode_capsule_route_hardening_artifacts,
)
from src.pipeline.newsroom_offline_rss_like_topic_fixture_v2 import (
    DEFAULT_CAPSULE_PATH,
    DEFAULT_FIXTURE_V2_PATH,
    build_default_fixture_v2_schema_contract,
    build_default_fixture_v2_to_mini_episode_capsule,
    build_default_offline_rss_like_topic_fixture_v2,
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts,
)
from src.pipeline.newsroom_rss_topic_fixture_route_hardening import (
    DEFAULT_HARDENING_PATH as DEFAULT_FIXTURE_ROUTE_HARDENING_PATH,
    DEFAULT_VALIDATION_PATH as DEFAULT_FIXTURE_VALIDATION_PATH,
    build_fixture_route_hardening,
    build_fixture_v2_validation,
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts(root=ROOT)
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts(root=ROOT)
    write_default_newsroom_episode_capsule_route_hardening_artifacts(root=ROOT)


def _source_payloads() -> tuple[dict, dict, dict, dict]:
    fixture = build_default_offline_rss_like_topic_fixture_v2(root=ROOT)
    schema = build_default_fixture_v2_schema_contract()
    source_capsule = build_default_fixture_v2_to_mini_episode_capsule(
        root=ROOT,
        fixture=fixture,
        schema_contract=schema,
    )
    validation = build_fixture_v2_validation(
        fixture=fixture,
        schema_contract=schema,
        capsule=source_capsule,
    )
    fixture_route_hardening = build_fixture_route_hardening(
        fixture=fixture,
        schema_contract=schema,
        capsule=source_capsule,
        validation=validation,
    )
    return fixture, validation, fixture_route_hardening, source_capsule


def test_hardened_capsule_and_route_hardening_match_builders() -> None:
    _ensure_artifacts()
    fixture, validation, fixture_route_hardening, source_capsule = _source_payloads()
    expected_capsule = build_hardened_episode_capsule(
        fixture=fixture,
        validation=validation,
        source_capsule=source_capsule,
    )
    expected_hardening = build_episode_capsule_route_hardening(
        fixture=fixture,
        validation=validation,
        fixture_route_hardening=fixture_route_hardening,
        source_capsule=source_capsule,
        hardened_capsule=expected_capsule,
    )

    assert _load(DEFAULT_FIXTURE_V2_PATH) == fixture
    assert _load(DEFAULT_CAPSULE_PATH) == source_capsule
    assert _load(DEFAULT_FIXTURE_VALIDATION_PATH) == validation
    assert _load(DEFAULT_FIXTURE_ROUTE_HARDENING_PATH) == fixture_route_hardening
    assert _load(DEFAULT_HARDENED_CAPSULE_PATH) == expected_capsule
    assert _load(DEFAULT_EPISODE_CAPSULE_ROUTE_HARDENING_PATH) == expected_hardening


def test_capsule_boundary_summary_and_readiness_stay_offline() -> None:
    _ensure_artifacts()
    hardened = _load(DEFAULT_HARDENED_CAPSULE_PATH)
    summary = hardened["capsule_boundary_summary"]
    readiness = hardened["capsule_readiness"]

    assert hardened["beat_count"] == 5
    assert summary["fixture_validation_status"] == "pass_with_explicit_production_blockers"
    assert summary["diagnostic_only"] is True
    assert summary["reusable_offline_fixture_candidate"] is True
    assert summary["live_boundary_ready_candidate"] is False
    assert summary["production_script_ready"] is False
    assert summary["production_blocker_count"] == 6
    assert summary["explicit_placeholder_count"] == 5
    assert "offline diagnostic fixture" in summary["source_boundary_summary"]
    assert "not production-approved" in summary["rights_boundary_summary"]
    assert "placeholder-bound" in summary["freshness_boundary_summary"]
    assert "fixture-only" in summary["attribution_boundary_summary"]
    assert summary["excluded_claims_summary"]["excluded_claim_count"] == 3
    assert summary["excluded_claims_summary"]["excluded_claims_carried_to_every_beat"] is True

    assert readiness["diagnostic_capsule_ready"] is True
    assert readiness["reusable_offline_capsule_ready"] is True
    assert readiness["live_boundary_plan_ready"] is False
    assert readiness["production_script_ready"] is False


def test_every_beat_carries_boundary_fields_and_false_production_claims() -> None:
    _ensure_artifacts()
    hardened = _load(DEFAULT_HARDENED_CAPSULE_PATH)
    beats = hardened["beats"]

    assert len(beats) == 5
    for beat in beats:
        assert beat["excluded_claims_applied"]
        assert beat["rights_status_applied"].startswith("placeholder:")
        assert beat["freshness_status_applied"] == "placeholder_not_evaluable_without_live_source"
        assert "fixture label only" in beat["attribution_status_applied"]
        assert beat["production_status_applied"] == "diagnostic_only"
        assert beat["can_be_used_for_diagnostic"] is True
        assert beat["can_be_used_for_live_boundary_plan"] is False
        assert beat["can_be_used_for_production_script"] is False
        assert beat["production_claim_allowed"] is False
        assert beat["not_accepted_scope"]["live_rss_or_news_fetch"] is False
        assert beat["boundary_inputs_from_validation"]["explicit_placeholder_count"] == 5
        assert beat["boundary_inputs_from_validation"]["production_blocker_count"] == 6


def test_source_warning_beat_contains_mandatory_warning_parts() -> None:
    _ensure_artifacts()
    hardened = _load(DEFAULT_HARDENED_CAPSULE_PATH)
    warning_beats = [
        beat for beat in hardened["beats"] if beat["beat_function"] == "source-boundary warning"
    ]

    assert len(warning_beats) == 1
    warning = warning_beats[0]
    line = warning["explanation_line"].lower()
    assert warning["warning_required"] is True
    assert "offline fixture" in line
    assert "placeholder source" in line
    assert "rights" in line
    assert "freshness" in line
    assert "attribution" in line
    assert "not production-approved" in line
    assert "excluded claims" in line
    assert "must not be asserted" in line


def test_validation_readback_enforces_excluded_claims_and_propagation() -> None:
    _ensure_artifacts()
    hardening = _load(DEFAULT_EPISODE_CAPSULE_ROUTE_HARDENING_PATH)
    readback = hardening["validation_readback"]

    assert readback["excluded_claims_absent"] is False
    assert readback["excluded_claims_used_as_positive_claims"] is False
    assert readback["production_blockers_propagated"] is True
    assert readback["placeholder_fields_propagated"] is True
    assert readback["source_warning_beat_present"] is True
    assert readback["source_warning_mentions_fixture_offline_status"] is True
    assert readback["source_warning_mentions_placeholder_source_fields"] is True
    assert readback["source_warning_mentions_rights_freshness_attribution"] is True
    assert readback["source_warning_mentions_excluded_claims"] is True
    assert readback["production_script_ready"] is False
    assert readback["live_boundary_plan_ready"] is False


def test_empty_excluded_claims_warn_and_block_diagnostic_readiness() -> None:
    fixture, validation, _fixture_route_hardening, source_capsule = _source_payloads()
    fixture["excluded_claims"] = []
    validation["production_blockers"] = list(validation["production_blockers"]) + [
        "excluded claims are absent or empty"
    ]
    hardened = build_hardened_episode_capsule(
        fixture=fixture,
        validation=validation,
        source_capsule=source_capsule,
    )

    assert hardened["validation_readback"]["excluded_claims_absent"] is True
    assert hardened["capsule_readiness"]["diagnostic_capsule_ready"] is False
    assert hardened["capsule_readiness"]["reusable_offline_capsule_ready"] is False
    assert "excluded_claims are absent or empty" in "\n".join(hardened["warnings"])


def test_docs_recommendation_and_scope_boundaries_are_stable() -> None:
    _ensure_artifacts()
    hardening = _load(DEFAULT_EPISODE_CAPSULE_ROUTE_HARDENING_PATH)

    assert hardening["next_recommended_axis"] == SELECTED_NEXT_AXIS
    assert hardening["recommendation_logic"]["selected"] == SELECTED_NEXT_AXIS
    assert hardening["business_goal_outcome_contract"]["problem_clear"]["status"] is True
    assert hardening["business_goal_outcome_contract"]["offer_clear"]["status"] is True
    assert hardening["business_goal_outcome_contract"]["proof_clear"]["status"] is True
    assert hardening["business_goal_outcome_contract"]["boundary_clear"]["status"] is True
    assert hardening["business_goal_outcome_contract"]["visual_supports_explanation"]["status"] is True

    assert (ROOT / DEFAULT_EPISODE_CAPSULE_ROUTE_HARDENING_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_episode_capsule_route_hardening_markdown(hardening)

    generated_paths = [
        DEFAULT_HARDENED_CAPSULE_PATH,
        DEFAULT_EPISODE_CAPSULE_ROUTE_HARDENING_PATH,
        DEFAULT_EPISODE_CAPSULE_ROUTE_HARDENING_DOC_PATH,
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)

    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in generated_paths)
    assert "http" + "://" not in combined
    assert "https" + "://" not in combined
    assert '"YMM4_launched_by_agent": ' + "true" not in combined
    assert '"render_performed_by_agent": ' + "true" not in combined
    assert '"audio_tts_generated": ' + "true" not in combined
