import json
from pathlib import Path

from src.pipeline.newsroom_live_rss_boundary_plan import (
    DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH,
    DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH,
    write_default_newsroom_live_rss_boundary_plan_artifacts,
)
from src.pipeline.newsroom_live_rss_preflight_contract import (
    DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH,
    DEFAULT_LIVE_RSS_PREFLIGHT_DOC_PATH,
    DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH,
    PREFLIGHT_CONTRACT_ID,
    PREFLIGHT_PACKET_TEMPLATE_ID,
    build_live_rss_preflight_contract,
    build_live_rss_preflight_packet_template,
    render_live_rss_preflight_contract_markdown,
    write_default_newsroom_live_rss_preflight_contract_artifacts,
)
from src.pipeline.newsroom_source_boundary_adversarial_fixtures import (
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

REQUIRED_PACKET_FIELDS = [
    "preflight_id",
    "requested_by",
    "authorization_status",
    "authorization_scope",
    "feed_id",
    "feed_title",
    "feed_url",
    "feed_type",
    "expected_fetch_mode",
    "expected_output_root",
    "network_access_allowed",
    "max_entries",
    "article_page_fetch_allowed",
    "media_download_allowed",
    "render_allowed",
    "audio_tts_allowed",
    "production_claim_allowed",
    "publication_allowed",
    "operator_notes",
    "abort_conditions",
]

REQUIRED_ARTIFACTS = [
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

REQUIRED_ABORTS = [
    "ABORT_NO_EXPLICIT_AUTHORIZATION",
    "ABORT_FEED_URL_MISSING",
    "ABORT_FEED_URL_MALFORMED",
    "ABORT_OUTPUT_ROOT_MISSING",
    "ABORT_NETWORK_NOT_ALLOWED",
    "ABORT_ARTICLE_PAGE_FETCH_REQUESTED",
    "ABORT_MEDIA_DOWNLOAD_REQUESTED",
    "ABORT_PUBLICATION_RENDER_AUDIO_REQUESTED",
    "ABORT_TOO_MANY_ENTRIES",
    "ABORT_TERMS_RIGHTS_UNCLEAR",
    "ABORT_UNEXPECTED_REDIRECT_OR_NON_RSS",
    "ABORT_SCRAPING_REQUIRED",
    "ABORT_PRODUCTION_PUBLIC_CLAIM",
]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts(root=ROOT)
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts(root=ROOT)
    write_default_newsroom_episode_capsule_route_hardening_artifacts(root=ROOT)
    write_default_newsroom_source_boundary_adversarial_fixture_artifacts(root=ROOT)
    write_default_newsroom_live_rss_boundary_plan_artifacts(root=ROOT)
    write_default_newsroom_live_rss_preflight_contract_artifacts(root=ROOT)


def test_preflight_artifacts_match_builders() -> None:
    _ensure_artifacts()
    boundary_plan = _load(DEFAULT_LIVE_RSS_BOUNDARY_PLAN_PATH)
    boundary_contract = _load(DEFAULT_LIVE_RSS_BOUNDARY_CONTRACT_PATH)
    expected_template = build_live_rss_preflight_packet_template(
        boundary_plan=boundary_plan,
        boundary_contract=boundary_contract,
    )
    expected_contract = build_live_rss_preflight_contract(
        boundary_plan=boundary_plan,
        boundary_contract=boundary_contract,
        packet_template=expected_template,
    )

    assert _load(DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH) == expected_template
    assert _load(DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH) == expected_contract
    assert (ROOT / DEFAULT_LIVE_RSS_PREFLIGHT_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_live_rss_preflight_contract_markdown(
        contract=expected_contract,
        packet_template=expected_template,
    )


def test_preflight_packet_defaults_block_fetch_and_authorization_now() -> None:
    _ensure_artifacts()
    template = _load(DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH)
    defaults = template["packet_defaults"]
    fields = [row["field_name"] for row in template["preflight_packet_schema"]]

    assert template["preflight_packet_template_id"] == PREFLIGHT_PACKET_TEMPLATE_ID
    assert fields == REQUIRED_PACKET_FIELDS
    assert defaults["authorization_status"] == "not_requested"
    assert defaults["network_access_allowed"] is False
    assert defaults["article_page_fetch_allowed"] is False
    assert defaults["media_download_allowed"] is False
    assert defaults["render_allowed"] is False
    assert defaults["audio_tts_allowed"] is False
    assert defaults["production_claim_allowed"] is False
    assert defaults["publication_allowed"] is False
    assert defaults["feed_url"] == "placeholder:future_feed_url_not_set"
    assert defaults["max_entries"] == 0
    assert defaults["abort_conditions"] == REQUIRED_ABORTS


def test_authorization_model_output_policy_and_artifact_schemas_are_complete() -> None:
    _ensure_artifacts()
    contract = _load(DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH)

    assert contract["preflight_contract_id"] == PREFLIGHT_CONTRACT_ID
    assert contract["authorization_model"]["states"] == [
        "not_requested",
        "requested",
        "authorized_for_diagnostic_fetch_once",
        "denied",
        "expired",
        "revoked",
    ]
    assert (
        contract["authorization_model"]["current_authorization_state"]
        == "not_requested"
    )
    assert contract["authorization_model"]["current_slice_defaults"] == {
        "authorization_status": "not_requested",
        "network_access_allowed": False,
        "article_page_fetch_allowed": False,
        "media_download_allowed": False,
        "production_claim_allowed": False,
        "publication_allowed": False,
    }

    output_policy = contract["future_output_policy"]
    assert output_policy["expected_directory_pattern"].startswith("_tmp/")
    assert "raw feed response" in output_policy["local_only_artifacts"]
    assert "blocker summary" in output_policy["trackable_summary_artifacts"]
    assert "raw feed response body" in output_policy["never_commit_artifacts"]
    assert [
        artifact["artifact_name"]
        for artifact in contract["future_artifact_schemas"]
    ] == REQUIRED_ARTIFACTS


def test_abort_conditions_post_fetch_gates_and_readiness_classification() -> None:
    _ensure_artifacts()
    contract = _load(DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH)
    readiness = contract["readiness_classification"]

    assert [row["condition_id"] for row in contract["abort_conditions"]] == REQUIRED_ABORTS
    assert all(row["severity"] == "abort" for row in contract["abort_conditions"])
    assert sorted(contract["post_fetch_gate_definitions"]) == [
        "CAPSULE_INPUT_GATE",
        "FETCH_RECEIPT_GATE",
        "NORMALIZED_TOPIC_GATE",
        "SOURCE_BOUNDARY_GATE",
    ]
    assert all(
        gate["executed_in_this_slice"] is False
        for gate in contract["post_fetch_gate_definitions"].values()
    )

    assert readiness["preflight_contract_ready"] is True
    assert readiness["authorization_sheet_ready"] is True
    assert readiness["fetch_implementation_allowed_now"] is False
    assert readiness["network_access_allowed_now"] is False
    assert readiness["operator_action_required_now"] is False
    assert readiness["next_allowed_state"] == "authorization_request_preparation"


def test_scope_boundaries_do_not_create_network_fetch_authorization_or_media_outputs() -> None:
    _ensure_artifacts()
    generated_paths = [
        DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH,
        DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH,
        DEFAULT_LIVE_RSS_PREFLIGHT_DOC_PATH,
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
    assert '"authorization_requested_from_user": ' + "true" not in combined
    assert '"YMM4_launched_by_agent": ' + "true" not in combined
    assert '"render_performed_by_agent": ' + "true" not in combined
    assert '"audio_tts_generated": ' + "true" not in combined
