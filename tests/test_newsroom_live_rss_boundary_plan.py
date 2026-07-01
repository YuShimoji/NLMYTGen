import json
from pathlib import Path

from src.pipeline.newsroom_live_rss_boundary_plan import (
    CONTRACT_ID,
    DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH,
    DEFAULT_LIVE_RSS_BOUNDARY_DOC_PATH,
    DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH,
    PLAN_ID,
    build_live_rss_boundary_contract,
    build_live_rss_boundary_plan,
    render_live_rss_boundary_plan_markdown,
    write_default_newsroom_live_rss_boundary_plan_artifacts,
)
from src.pipeline.newsroom_source_boundary_adversarial_fixtures import (
    DEFAULT_ADVERSARIAL_CAPSULE_HARDENING_PATH,
    DEFAULT_ADVERSARIAL_VALIDATION_PATH,
    write_default_newsroom_source_boundary_adversarial_fixture_artifacts,
)
from src.pipeline.newsroom_episode_capsule_route_hardening import (
    write_default_newsroom_episode_capsule_route_hardening_artifacts,
)
from src.pipeline.newsroom_offline_rss_like_topic_fixture_v2 import (
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts,
)
from src.pipeline.newsroom_rss_topic_fixture_route_hardening import (
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_STATES = [
    "offline_fixture_only",
    "offline_fixture_validated",
    "adversarial_validation_passed",
    "live_boundary_planned",
    "live_fetch_authorized_for_diagnostic_smoke",
    "live_fetch_result_captured",
    "live_source_boundary_validated",
    "diagnostic_capsule_ready",
    "production_script_blocked",
    "production_ready_requires_separate_approval",
]

REQUIRED_FUTURE_ARTIFACTS = [
    "fetch_receipt",
    "feed_source_manifest",
    "raw_entry_snapshot",
    "normalized_topic_candidate",
    "source_boundary_validation",
    "rights_attribution_freshness_readback",
    "excluded_claims_readback",
    "capsule_input_candidate",
    "operator_action_log",
]

REQUIRED_SCHEMA_FIELDS = [
    "topic_id",
    "feed_id",
    "feed_title",
    "entry_title",
    "entry_url",
    "entry_published_at",
    "entry_summary",
    "source_name",
    "source_url",
    "retrieved_at",
    "fetch_receipt_id",
    "rights_status",
    "attribution_note",
    "freshness_status",
    "source_reliability_note",
    "key_claim_candidates",
    "excluded_claims",
    "uncertainty_or_boundary",
    "intended_episode_angle",
    "production_status",
]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts(root=ROOT)
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts(root=ROOT)
    write_default_newsroom_episode_capsule_route_hardening_artifacts(root=ROOT)
    write_default_newsroom_source_boundary_adversarial_fixture_artifacts(root=ROOT)
    write_default_newsroom_live_rss_boundary_plan_artifacts(root=ROOT)


def test_live_rss_boundary_artifacts_match_builders() -> None:
    _ensure_artifacts()
    adversarial_validation = _load(DEFAULT_ADVERSARIAL_VALIDATION_PATH)
    adversarial_capsule = _load(DEFAULT_ADVERSARIAL_CAPSULE_HARDENING_PATH)
    expected_contract = build_live_rss_boundary_contract(
        adversarial_validation=adversarial_validation,
        adversarial_capsule=adversarial_capsule,
    )
    expected_plan = build_live_rss_boundary_plan(
        contract=expected_contract,
        adversarial_validation=adversarial_validation,
        adversarial_capsule=adversarial_capsule,
    )

    assert _load(DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH) == expected_contract
    assert _load(DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH) == expected_plan
    assert (ROOT / DEFAULT_LIVE_RSS_BOUNDARY_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_live_rss_boundary_plan_markdown(
        plan=expected_plan,
        contract=expected_contract,
    )


def test_state_machine_stops_at_live_boundary_planned() -> None:
    _ensure_artifacts()
    plan = _load(DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH)
    state_machine = plan["state_machine"]
    state_status = {
        row["state"]: row["reached_in_this_slice"]
        for row in state_machine["state_status"]
    }

    assert plan["plan_id"] == PLAN_ID
    assert state_machine["allowed_states"] == REQUIRED_STATES
    assert state_machine["current_state"] == "live_boundary_planned"
    assert state_status["offline_fixture_only"] is True
    assert state_status["offline_fixture_validated"] is True
    assert state_status["adversarial_validation_passed"] is True
    assert state_status["live_boundary_planned"] is True
    assert state_status["live_fetch_authorized_for_diagnostic_smoke"] is False
    assert state_status["live_fetch_result_captured"] is False
    assert state_status["live_source_boundary_validated"] is False
    assert state_status["diagnostic_capsule_ready"] is False
    assert state_status["production_ready_requires_separate_approval"] is False
    assert state_machine["next_allowed_transition"]["allowed_now"] is False


def test_artifact_contract_schema_and_gates_are_complete() -> None:
    _ensure_artifacts()
    contract = _load(DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH)

    assert contract["contract_id"] == CONTRACT_ID
    assert [
        artifact["artifact_name"]
        for artifact in contract["future_live_rss_artifact_contract"]
    ] == REQUIRED_FUTURE_ARTIFACTS
    assert all(
        artifact["can_contain_live_source_data"] is True
        for artifact in contract["future_live_rss_artifact_contract"]
    )
    assert all(
        artifact["can_be_committed"] is False
        for artifact in contract["future_live_rss_artifact_contract"]
    )
    assert all(
        artifact["must_remain_local_ignored"] is True
        for artifact in contract["future_live_rss_artifact_contract"]
    )

    assert [
        field["field_name"]
        for field in contract["normalized_live_rss_topic_schema"]
    ] == REQUIRED_SCHEMA_FIELDS
    assert all(
        field["diagnostic_capsule_required"]
        for field in contract["normalized_live_rss_topic_schema"]
    )
    assert all(
        field["production_script_candidate_required"]
        for field in contract["normalized_live_rss_topic_schema"]
    )
    assert sorted(contract["gate_definitions"]) == [
        "CAPSULE_GENERATION_GATE",
        "LIVE_FETCH_GATE",
        "PUBLICATION_GATE",
        "SOURCE_BOUNDARY_GATE",
    ]
    assert contract["gate_definitions"]["LIVE_FETCH_GATE"]["status_now"] == "closed"
    assert contract["gate_definitions"]["PUBLICATION_GATE"]["status_now"] == "closed"


def test_decision_readback_and_source_misuse_classification_are_safe() -> None:
    _ensure_artifacts()
    plan = _load(DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH)
    readback = plan["source_readback"]
    decision = plan["decision_readback"]

    assert readback["adversarial_total_cases"] == 11
    assert readback["adversarial_unexpected_pass_count"] == 0
    assert readback["adversarial_unexpected_fail_count"] == 0
    assert readback["adversarial_production_ready_false_count"] == 11
    assert readback["excluded_claims_used_as_positive_claims_count"] == 1
    assert readback["excluded_claim_misuse_classification"] == (
        "detected adversarial misuse case; not a production-ready leak"
    )
    assert readback["production_script_ready_true_count"] == 0
    assert readback["live_boundary_plan_ready_true_count"] == 0

    assert decision["live_fetch_implementation_allowed_now"] is False
    assert decision["live_boundary_plan_ready"] is True
    assert decision["next_recommended_axis"] == "newsroom-live-rss-preflight-contract-v1"


def test_scope_boundaries_do_not_create_network_visual_media_or_live_fetch_outputs() -> None:
    _ensure_artifacts()
    generated_paths = [
        DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH,
        DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH,
        DEFAULT_LIVE_RSS_BOUNDARY_DOC_PATH,
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)

    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in generated_paths)
    assert "http" + "://" not in combined
    assert "https" + "://" not in combined
    assert '"live_fetch_used": ' + "true" not in combined
    assert '"network_fetch_performed": ' + "true" not in combined
    assert '"live_RSS_news_fetch_performed": ' + "true" not in combined
    assert '"fetch_adapter_implemented": ' + "true" not in combined
    assert '"YMM4_launched_by_agent": ' + "true" not in combined
    assert '"render_performed_by_agent": ' + "true" not in combined
    assert '"audio_tts_generated": ' + "true" not in combined
