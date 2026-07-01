import json
from pathlib import Path

from src.pipeline.newsroom_episode_capsule_route_hardening import (
    write_default_newsroom_episode_capsule_route_hardening_artifacts,
)
from src.pipeline.newsroom_live_rss_boundary_plan import (
    write_default_newsroom_live_rss_boundary_plan_artifacts,
)
from src.pipeline.newsroom_live_rss_operator_authorization_sheet import (
    AUTHORIZATION_PACKET_TEMPLATE_ID,
    AUTHORIZATION_SHEET_ID,
    DEFAULT_AUTHORIZATION_PACKET_TEMPLATE_PATH,
    DEFAULT_OPERATOR_AUTHORIZATION_DOC_PATH,
    DEFAULT_OPERATOR_AUTHORIZATION_SHEET_PATH,
    build_live_rss_authorization_packet_template,
    build_live_rss_operator_authorization_sheet,
    render_live_rss_operator_authorization_sheet_markdown,
    write_default_newsroom_live_rss_operator_authorization_sheet_artifacts,
)
from src.pipeline.newsroom_live_rss_preflight_contract import (
    DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH,
    DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH,
    write_default_newsroom_live_rss_preflight_contract_artifacts,
)
from src.pipeline.newsroom_offline_rss_like_topic_fixture_v2 import (
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts,
)
from src.pipeline.newsroom_rss_topic_fixture_route_hardening import (
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts,
)
from src.pipeline.newsroom_source_boundary_adversarial_fixtures import (
    write_default_newsroom_source_boundary_adversarial_fixture_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]

OPERATOR_FIELDS = [
    "feed_title",
    "feed_url",
    "feed_owner_or_source_name",
    "why_this_feed",
    "max_entries",
    "expected_fetch_mode",
    "expected_output_root",
    "authorization_expiry",
    "operator_notes",
]

CONFIRMATIONS = [
    "allow_one_time_network_rss_feed_fetch",
    "disallow_article_page_scraping",
    "disallow_media_download",
    "disallow_render_export",
    "disallow_audio_tts",
    "disallow_production_public_claims",
    "require_local_ignored_raw_outputs",
    "require_source_boundary_validation_before_capsule",
    "require_rights_freshness_attribution_readback",
    "require_excluded_claims_readback",
    "allow_only_diagnostic_capsule_candidate_after_gates",
]

PACKET_FIELDS = [
    "authorization_packet_id",
    "derived_from_preflight_contract",
    "authorization_status",
    "requested_by",
    "authorized_by",
    "feed_id",
    "feed_title",
    "feed_url",
    "feed_owner_or_source_name",
    "authorization_scope",
    "network_access_allowed",
    "article_page_fetch_allowed",
    "media_download_allowed",
    "render_allowed",
    "audio_tts_allowed",
    "production_claim_allowed",
    "publication_allowed",
    "max_entries",
    "expected_fetch_mode",
    "expected_output_root",
    "authorization_expiry",
    "operator_confirmations",
    "abort_conditions",
    "required_future_artifacts",
    "next_gate_after_authorization",
]

FUTURE_ARTIFACTS = [
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


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_offline_rss_like_topic_fixture_v2_artifacts(root=ROOT)
    write_default_newsroom_rss_topic_fixture_route_hardening_artifacts(root=ROOT)
    write_default_newsroom_episode_capsule_route_hardening_artifacts(root=ROOT)
    write_default_newsroom_source_boundary_adversarial_fixture_artifacts(root=ROOT)
    write_default_newsroom_live_rss_boundary_plan_artifacts(root=ROOT)
    write_default_newsroom_live_rss_preflight_contract_artifacts(root=ROOT)
    write_default_newsroom_live_rss_operator_authorization_sheet_artifacts(root=ROOT)


def test_operator_authorization_artifacts_match_builders() -> None:
    _ensure_artifacts()
    preflight_contract = _load(DEFAULT_LIVE_RSS_PREFLIGHT_CONTRACT_PATH)
    preflight_packet_template = _load(DEFAULT_LIVE_RSS_PREFLIGHT_PACKET_TEMPLATE_PATH)
    expected_packet = build_live_rss_authorization_packet_template(
        preflight_contract=preflight_contract,
        preflight_packet_template=preflight_packet_template,
    )
    expected_sheet = build_live_rss_operator_authorization_sheet(
        preflight_contract=preflight_contract,
        preflight_packet_template=preflight_packet_template,
        authorization_packet_template=expected_packet,
    )

    assert _load(DEFAULT_AUTHORIZATION_PACKET_TEMPLATE_PATH) == expected_packet
    assert _load(DEFAULT_OPERATOR_AUTHORIZATION_SHEET_PATH) == expected_sheet
    assert (ROOT / DEFAULT_OPERATOR_AUTHORIZATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_live_rss_operator_authorization_sheet_markdown(
        authorization_sheet=expected_sheet,
        authorization_packet_template=expected_packet,
    )


def test_user_facing_sheet_has_required_fields_confirmations_and_results() -> None:
    _ensure_artifacts()
    sheet = _load(DEFAULT_OPERATOR_AUTHORIZATION_SHEET_PATH)
    user_sheet = sheet["user_facing_authorization_sheet"]

    assert sheet["authorization_sheet_id"] == AUTHORIZATION_SHEET_ID
    assert sheet["live_fetch_used"] is False
    assert sheet["network_access_used"] is False
    assert sheet["production_status"] == "authorization_template_only"
    assert "one-time diagnostic RSS fetch" in user_sheet["purpose"]["summary"]
    assert user_sheet["current_status"]["authorization_status"] == "not_requested"
    assert user_sheet["current_status"]["actual_authorization_requested_now"] is False
    assert [row["field_name"] for row in user_sheet["operator_fields"]] == OPERATOR_FIELDS
    assert [
        row["confirmation_id"]
        for row in user_sheet["required_yes_no_confirmations"]
    ] == CONFIRMATIONS
    assert [
        row["artifact_name"] for row in user_sheet["expected_future_results"]
    ] == FUTURE_ARTIFACTS


def test_machine_packet_template_defaults_remain_safe() -> None:
    _ensure_artifacts()
    packet = _load(DEFAULT_AUTHORIZATION_PACKET_TEMPLATE_PATH)
    defaults = packet["default_values"]

    assert packet["authorization_packet_template_id"] == AUTHORIZATION_PACKET_TEMPLATE_ID
    assert packet["field_list"] == PACKET_FIELDS
    assert defaults["authorization_status"] == "not_requested"
    assert defaults["requested_by"] == "not_requested"
    assert defaults["authorized_by"] == "not_requested"
    assert defaults["feed_url"] == "placeholder:future_feed_url_not_set"
    assert defaults["network_access_allowed"] is False
    assert defaults["article_page_fetch_allowed"] is False
    assert defaults["media_download_allowed"] is False
    assert defaults["render_allowed"] is False
    assert defaults["audio_tts_allowed"] is False
    assert defaults["production_claim_allowed"] is False
    assert defaults["publication_allowed"] is False
    assert defaults["max_entries"] == 0
    assert defaults["required_future_artifacts"] == FUTURE_ARTIFACTS
    assert packet["next_gate_after_authorization"] == "FETCH_RECEIPT_GATE"


def test_safety_classification_and_next_axis_are_non_authorizing() -> None:
    _ensure_artifacts()
    sheet = _load(DEFAULT_OPERATOR_AUTHORIZATION_SHEET_PATH)
    safety = sheet["safety_classification"]

    assert safety["authorization_sheet_ready"] is True
    assert safety["actual_authorization_requested_now"] is False
    assert safety["fetch_implementation_allowed_now"] is False
    assert safety["network_access_allowed_now"] is False
    assert safety["operator_action_required_now"] is False
    assert safety["next_allowed_state"] == "authorization_request_or_source_manifest_schema"
    assert safety["next_recommended_axis"] == "newsroom-rss-source-manifest-schema-v1"


def test_scope_boundaries_do_not_create_network_authorization_media_or_fetch_outputs() -> None:
    _ensure_artifacts()
    generated_paths = [
        DEFAULT_OPERATOR_AUTHORIZATION_SHEET_PATH,
        DEFAULT_AUTHORIZATION_PACKET_TEMPLATE_PATH,
        DEFAULT_OPERATOR_AUTHORIZATION_DOC_PATH,
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)

    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in generated_paths)
    assert "http" + "://" not in combined
    assert "https" + "://" not in combined
    assert '"live_fetch_used": ' + "true" not in combined
    assert '"network_access_used": ' + "true" not in combined
    assert '"network_fetch_performed": ' + "true" not in combined
    assert '"live_RSS_news_fetch_performed": ' + "true" not in combined
    assert '"fetch_adapter_implemented": ' + "true" not in combined
    assert '"authorization_requested_from_user": ' + "true" not in combined
    assert '"YMM4_launched_by_agent": ' + "true" not in combined
    assert '"render_performed_by_agent": ' + "true" not in combined
    assert '"audio_tts_generated": ' + "true" not in combined
