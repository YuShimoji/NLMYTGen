import json
from pathlib import Path

from src.pipeline.newsroom_source_boundary_adversarial_fixtures import (
    ADVERSARIAL_CAPSULE_HARDENING_ID,
    ADVERSARIAL_SUITE_ID,
    ADVERSARIAL_VALIDATION_ID,
    DEFAULT_ADVERSARIAL_CAPSULE_HARDENING_PATH,
    DEFAULT_ADVERSARIAL_DOC_PATH,
    DEFAULT_ADVERSARIAL_FIXTURES_PATH,
    DEFAULT_ADVERSARIAL_VALIDATION_PATH,
    build_source_boundary_adversarial_capsule_hardening,
    build_source_boundary_adversarial_fixture_suite,
    build_source_boundary_adversarial_fixture_validation,
    render_adversarial_markdown,
    write_default_newsroom_source_boundary_adversarial_fixture_artifacts,
)
from src.pipeline.newsroom_offline_rss_like_topic_fixture_v2 import (
    build_default_fixture_v2_schema_contract,
    build_default_fixture_v2_to_mini_episode_capsule,
    build_default_offline_rss_like_topic_fixture_v2,
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts,
)
from src.pipeline.newsroom_rss_topic_fixture_route_hardening import (
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts,
)
from src.pipeline.newsroom_episode_capsule_route_hardening import (
    write_default_newsroom_episode_capsule_route_hardening_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]


EXPECTED_CASE_STATES = {
    "control_valid_diagnostic_fixture": "diagnostic_allowed_with_production_blockers",
    "missing_required_fields": "blocked_missing_required_fields",
    "unmarked_placeholder_source": "blocked_unmarked_placeholder",
    "invalid_source_url_or_timestamp": "invalid",
    "rights_unknown_or_unapproved": "blocked_rights_unknown",
    "freshness_unknown_or_stale": "blocked_freshness_unknown_or_stale",
    "excluded_claims_absent_or_empty": "blocked_excluded_claims_absent",
    "excluded_claim_used_as_positive_claim": (
        "blocked_excluded_claim_used_as_positive_claim"
    ),
    "source_boundary_unknown": "blocked_source_boundary_unknown",
    "production_ready_with_placeholders": "blocked_production_ready_with_placeholders",
    "live_fetch_attempt_flag": "blocked_live_fetch_attempt_flag",
}


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts(root=ROOT)
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts(root=ROOT)
    write_default_newsroom_episode_capsule_route_hardening_artifacts(root=ROOT)
    write_default_newsroom_source_boundary_adversarial_fixture_artifacts(root=ROOT)


def _source_payloads() -> tuple[dict, dict, dict]:
    fixture = build_default_offline_rss_like_topic_fixture_v2(root=ROOT)
    schema = build_default_fixture_v2_schema_contract()
    source_capsule = build_default_fixture_v2_to_mini_episode_capsule(
        root=ROOT,
        fixture=fixture,
        schema_contract=schema,
    )
    return fixture, schema, source_capsule


def test_adversarial_artifacts_match_builders() -> None:
    _ensure_artifacts()
    fixture, schema, source_capsule = _source_payloads()
    expected_suite = build_source_boundary_adversarial_fixture_suite(
        fixture=fixture,
        schema_contract=schema,
        source_capsule=source_capsule,
    )
    expected_validation = build_source_boundary_adversarial_fixture_validation(
        suite=expected_suite,
        schema_contract=schema,
        fallback_source_capsule=source_capsule,
    )
    expected_capsule_hardening = build_source_boundary_adversarial_capsule_hardening(
        suite=expected_suite,
        validation=expected_validation,
        schema_contract=schema,
        fallback_source_capsule=source_capsule,
    )

    assert _load(DEFAULT_ADVERSARIAL_FIXTURES_PATH) == expected_suite
    assert _load(DEFAULT_ADVERSARIAL_VALIDATION_PATH) == expected_validation
    assert _load(DEFAULT_ADVERSARIAL_CAPSULE_HARDENING_PATH) == expected_capsule_hardening
    assert (ROOT / DEFAULT_ADVERSARIAL_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_adversarial_markdown(
        suite=expected_suite,
        validation=expected_validation,
        capsule_hardening=expected_capsule_hardening,
    )


def test_all_required_adversarial_cases_are_present_and_classified() -> None:
    _ensure_artifacts()
    suite = _load(DEFAULT_ADVERSARIAL_FIXTURES_PATH)
    validation = _load(DEFAULT_ADVERSARIAL_VALIDATION_PATH)

    assert suite["adversarial_suite_id"] == ADVERSARIAL_SUITE_ID
    assert suite["live_fetch_used"] is False
    assert suite["render_gate"] == "L0_no_render"
    assert [case["case_type"] for case in suite["fixture_cases"]] == list(
        EXPECTED_CASE_STATES
    )

    actual_states = {
        result["case_type"]: result["actual_route_state"]
        for result in validation["case_results"]
    }
    assert actual_states == EXPECTED_CASE_STATES
    assert all(result["validator_passed_as_expected"] for result in validation["case_results"])
    assert all(result["production_script_ready"] is False for result in validation["case_results"])
    assert all(result["live_boundary_plan_ready"] is False for result in validation["case_results"])


def test_validation_summary_keeps_live_boundary_planning_as_next_not_live_fetch() -> None:
    _ensure_artifacts()
    validation = _load(DEFAULT_ADVERSARIAL_VALIDATION_PATH)
    summary = validation["validation_summary"]
    decision = validation["decision_readback"]

    assert validation["adversarial_validation_id"] == ADVERSARIAL_VALIDATION_ID
    assert summary["total_cases"] == 11
    assert summary["expected_pass_count"] == 1
    assert summary["expected_block_count"] == 10
    assert summary["unexpected_pass_count"] == 0
    assert summary["unexpected_fail_count"] == 0
    assert summary["missing_required_detected_count"] >= 1
    assert summary["unmarked_placeholder_detected_count"] >= 1
    assert summary["invalid_value_detected_count"] >= 1
    assert summary["rights_blocker_detected_count"] >= 1
    assert summary["source_boundary_blocker_detected_count"] >= 1
    assert summary["excluded_claim_misuse_detected_count"] == 1
    assert summary["production_ready_false_count"] == 11

    assert decision["validator_sufficient_for_next_step"] is True
    assert decision["next_recommended_axis"] == "newsroom-live-rss-boundary-plan-v1"
    assert "do not implement live fetch yet" in decision["required_followup"]


def test_capsule_hardening_blocks_clean_capsules_and_detects_excluded_claim_leak() -> None:
    _ensure_artifacts()
    capsule_hardening = _load(DEFAULT_ADVERSARIAL_CAPSULE_HARDENING_PATH)
    summary = capsule_hardening["capsule_hardening_summary"]

    assert (
        capsule_hardening["adversarial_capsule_hardening_id"]
        == ADVERSARIAL_CAPSULE_HARDENING_ID
    )
    assert summary["capsule_generation_allowed_count"] == 5
    assert summary["capsule_generation_blocked_count"] == 6
    assert summary["blockers_propagated_count"] == 5
    assert summary["excluded_claims_used_as_positive_claims_count"] == 1
    assert summary["production_script_ready_true_count"] == 0
    assert summary["live_boundary_plan_ready_true_count"] == 0

    results = {result["case_type"]: result for result in capsule_hardening["case_results"]}
    assert results["missing_required_fields"]["capsule_generation_allowed"] is False
    assert results["source_boundary_unknown"]["capsule_generation_allowed"] is False
    assert (
        results["excluded_claim_used_as_positive_claim"][
            "excluded_claims_used_as_positive_claims"
        ]
        is True
    )
    assert all(result["clean_capsule_generated"] is False for result in results.values())


def test_scope_boundaries_do_not_create_visual_media_or_live_fetch_outputs() -> None:
    _ensure_artifacts()
    generated_paths = [
        DEFAULT_ADVERSARIAL_FIXTURES_PATH,
        DEFAULT_ADVERSARIAL_VALIDATION_PATH,
        DEFAULT_ADVERSARIAL_CAPSULE_HARDENING_PATH,
        DEFAULT_ADVERSARIAL_DOC_PATH,
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)

    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in generated_paths)
    assert "http" + "://" not in combined
    assert "https" + "://" not in combined
    assert '"live_fetch_used": ' + "true" not in combined
    assert '"YMM4_launched_by_agent": ' + "true" not in combined
    assert '"render_performed_by_agent": ' + "true" not in combined
    assert '"audio_tts_generated": ' + "true" not in combined
