import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUEST_PATH = (
    ROOT / "samples" / "_probe" / "newsroom_handoff" / "upstream_export_delta_request.json"
)

ALLOWED_OWNERS = {
    "newsroom-yt-pipeline",
    "NLMYTGen",
    "human reviewer",
    "external/manual",
}
ALLOWED_REQUIRED_BEFORE = {
    "NLMYTGen ingest",
    "transfer candidate",
    "human review",
}
ALLOWED_CONSUMERS = {
    "validator",
    "slot-linkage proof",
    "transfer-planning proof",
    "Review Console planning panel",
    "not covered yet",
}
ALLOWED_FAILURE_BEHAVIOR = {
    "fail",
    "warn",
    "block transfer",
    "hold for review",
}
ALLOWED_REQUEST_PRIORITY = {
    "required",
    "transfer_gate",
    "optional",
    "human_review_hold",
}
REQUEST_ITEM_REQUIRED_FIELDS = {
    "field_name",
    "owner",
    "required_before",
    "current_consumer",
    "current_NLMYTGen_consumer",
    "failure_behavior",
    "request_priority",
    "why_needed",
}


def _request() -> dict:
    return json.loads(REQUEST_PATH.read_text(encoding="utf-8"))


def _items(request: dict) -> list[dict]:
    return request["request_items"]


def test_upstream_export_delta_request_parses_and_stays_request_only() -> None:
    request = _request()

    assert request["artifact_id"] == "newsroom_upstream_export_delta_request_v1_2026_06_20"
    assert request["repo_relative_path"] == (
        "samples/_probe/newsroom_handoff/upstream_export_delta_request.json"
    )
    assert request["status"] == "request_spec_only"
    assert request["review_status"] == "ready_for_supervisor_review"
    assert request["target_repo"] == "newsroom-yt-pipeline"
    assert request["current_packet_state"] == "synthetic_fixture_only"
    assert request["real_packet_accepted"] is False
    assert request["production_approval"] is False
    assert request["rights_approval"] is False
    assert request["ymm4_transfer_ready"] is False
    assert request["diagnostic_only"] is True


def test_upstream_export_delta_request_items_have_required_fields_and_values() -> None:
    request = _request()

    for item in _items(request):
        assert REQUEST_ITEM_REQUIRED_FIELDS <= set(item)
        assert item["field_name"]
        assert item["owner"] in ALLOWED_OWNERS
        assert item["required_before"] in ALLOWED_REQUIRED_BEFORE
        assert item["current_consumer"] in ALLOWED_CONSUMERS
        assert item["current_NLMYTGen_consumer"] == item["current_consumer"]
        assert item["failure_behavior"] in ALLOWED_FAILURE_BEHAVIOR
        assert item["request_priority"] in ALLOWED_REQUEST_PRIORITY
        assert item["why_needed"]


def test_upstream_export_delta_request_covers_required_optional_and_hold_fields() -> None:
    request = _request()
    field_names = {item["field_name"] for item in _items(request)}

    assert {
        "artifact_id",
        "contract_version",
        "episode_id",
        "title",
        "topic_summary",
        "episode_metadata",
        "source_notes",
        "provenance",
        "rights_summary",
        "notebooklm_packet_or_transcript_seed",
        "script_beats",
        "visual_plan",
        "g28_slot_hints",
        "review_warnings",
        "downstream_readiness",
        "rights_provenance_clearance",
        "media_source_availability",
        "review_approval_status",
        "visual_readiness",
        "blocked_prohibited_actions_resolved",
        "no_readiness_blocker_contradiction",
    } <= field_names
    assert set(request["optional_enrichment_fields"]) <= field_names
    assert set(request["hold_review_fields"]) <= field_names


def test_upstream_export_delta_request_preserves_forbidden_boundary() -> None:
    request = _request()
    prohibited_text = json.dumps(
        request["prohibited_upstream_assumptions"],
        ensure_ascii=False,
    )

    for expected in [
        "RSS/source discovery",
        "scrapes article pages",
        "Inoreader",
        "downloads live source material",
        "acquires rights",
        "production approval",
        "publishes or uploads",
        "silently infers missing approvals",
        ".ymmp",
        "render or media outputs",
    ]:
        assert expected in prohibited_text


def test_upstream_export_delta_request_uses_fake_non_fetching_fixture_shape() -> None:
    raw_text = REQUEST_PATH.read_text(encoding="utf-8")
    request = json.loads(raw_text)
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."

    assert re.search(f"{protocol_pattern}|{host_pattern}", raw_text, flags=re.IGNORECASE) is None
    assert request["proposed_newsroom_export_fixture_shape"]["artifact_id"].startswith("fake_")
    assert (
        request["proposed_newsroom_export_fixture_shape"]["provenance"][
            "external_fetch_allowed_by_nlmytgen"
        ]
        is False
    )
    assert (
        request["proposed_newsroom_export_fixture_shape"]["downstream_readiness"][
            "ymm4_transfer_ready"
        ]
        is False
    )
    assert request["validation_expectations"]["no_real_urls"] is True
    assert request["validation_expectations"]["no_ymmp_or_render_output"] is True
