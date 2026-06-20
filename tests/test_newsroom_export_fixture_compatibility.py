import json
import re
from collections import Counter
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
COMPATIBILITY_PATH = (
    ROOT
    / "samples"
    / "_probe"
    / "newsroom_handoff"
    / "newsroom_export_fixture_compatibility_readback.json"
)
REQUEST_PATH = (
    ROOT / "samples" / "_probe" / "newsroom_handoff" / "upstream_export_delta_request.json"
)
NEWSROOM_FIXTURE_PATH = (
    ROOT.parent
    / "newsroom-yt-pipeline"
    / "samples"
    / "_probe"
    / "newsroom_handoff"
    / "newsroom_export_fixture_v1.json"
)

ALLOWED_STATUSES = {
    "direct_match",
    "transform_required",
    "missing_required",
    "missing_transfer_candidate",
    "hold_for_human_review",
    "upstream_only",
    "downstream_only",
}
ALLOWED_CONSUMERS = {
    "validator",
    "slot-linkage proof",
    "transfer-planning proof",
    "Review Console panel",
    "checklist only",
}
REQUIRED_ITEM_FIELDS = {
    "field_name",
    "newsroom_path",
    "nlmytgen_expected_path",
    "compatibility_status",
    "owner",
    "failure_behavior",
    "consumer",
    "next_action",
}


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _all_checks(readback: dict) -> list[dict]:
    return (
        readback["compatibility_items"]
        + readback["prohibited_assumption_checks"]
        + readback["downstream_only_checks"]
    )


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_newsroom_export_fixture_compatibility_readback_parses_and_blocks_transfer() -> None:
    readback = _json(COMPATIBILITY_PATH)

    assert readback["artifact_id"] == "newsroom_export_fixture_compatibility_v1_2026_06_20"
    assert readback["status"] == "passed_with_adapter_warnings_transfer_blocked"
    assert readback["review_status"] == "ready_for_supervisor_review"
    assert readback["diagnostic_only"] is True
    assert readback["target_repo"] == "newsroom-yt-pipeline"
    assert readback["target_fixture_commit"] == "912ce3b"
    assert readback["real_packet_accepted"] is False
    assert readback["rights_approval"] is False
    assert readback["media_approval"] is False
    assert readback["review_approval"] is False
    assert readback["production_approval"] is False
    assert readback["ymm4_transfer_ready"] is False
    assert readback["raw_fixture_direct_ingest"] == "not_accepted_requires_adapter"


def test_newsroom_export_fixture_compatibility_covers_every_requested_item() -> None:
    readback = _json(COMPATIBILITY_PATH)
    request = _json(REQUEST_PATH)

    requested_fields = {item["field_name"] for item in request["request_items"]}
    compatibility_fields = {item["field_name"] for item in readback["compatibility_items"]}

    assert requested_fields <= compatibility_fields
    assert len(readback["compatibility_items"]) == len(request["request_items"])


def test_newsroom_export_fixture_compatibility_items_have_required_schema() -> None:
    readback = _json(COMPATIBILITY_PATH)
    checks = _all_checks(readback)
    status_counts = Counter(item["compatibility_status"] for item in checks)

    assert set(readback["compatibility_status_categories"]) == ALLOWED_STATUSES
    assert readback["summary_counts"]["total_checks"] == len(checks)
    for status in ALLOWED_STATUSES:
        assert readback["summary_counts"][status] == status_counts.get(status, 0)
    for item in checks:
        assert REQUIRED_ITEM_FIELDS <= set(item)
        assert item["compatibility_status"] in ALLOWED_STATUSES
        assert item["consumer"] in ALLOWED_CONSUMERS
        assert item["next_action"]


def test_newsroom_export_fixture_compatibility_has_no_real_urls() -> None:
    raw_text = COMPATIBILITY_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(raw_text) is None
    assert _json(COMPATIBILITY_PATH)["validation_result"]["readback_real_url_scan"] == (
        "passed_none_found"
    )


def test_newsroom_fixture_can_be_read_when_local_checkout_exists() -> None:
    if not NEWSROOM_FIXTURE_PATH.exists():
        pytest.skip("newsroom-yt-pipeline checkout is not available")

    raw_text = NEWSROOM_FIXTURE_PATH.read_text(encoding="utf-8")
    fixture = json.loads(raw_text)

    assert _real_url_pattern().search(raw_text) is None
    assert fixture["fixture_id"] == "newsroom_export_fixture_for_nlmytgen_v1"
    assert fixture["review_status"] == "fake_only_contract_probe"
    assert fixture["export_metadata"]["contains_real_news"] is False
    assert fixture["export_metadata"]["contains_credentials"] is False
    assert fixture["export_metadata"]["contains_media"] is False
    assert fixture["export_metadata"]["contains_external_downloads"] is False
    assert fixture["downstream_readiness"]["transfer_candidate"] == "block_transfer"
    assert fixture["downstream_readiness"]["production_ymm4"] == "fail"


def test_newsroom_fixture_rights_hold_cannot_pass_as_approval() -> None:
    readback = _json(COMPATIBILITY_PATH)
    rights_item = next(
        item for item in readback["compatibility_items"] if item["field_name"] == "rights_summary"
    )

    assert rights_item["compatibility_status"] == "hold_for_human_review"
    assert rights_item["failure_behavior"] == "block transfer"
    assert readback["validation_result"]["rights_approval"] == "not_granted"
    assert readback["validation_result"]["transfer_readiness"] == "blocked"
