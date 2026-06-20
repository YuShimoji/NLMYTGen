import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST_PATH = (
    ROOT / "samples" / "_probe" / "newsroom_handoff" / "real_packet_readiness_checklist.json"
)

ALLOWED_OWNERS = {
    "newsroom-yt-pipeline",
    "NLMYTGen",
    "human reviewer",
    "external/manual",
}
ALLOWED_COVERAGE = {
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
    "ignore",
}
ALLOWED_NEXT_ACTION = {
    "accept",
    "request upstream field",
    "block transfer",
    "add validator check later",
    "Review Card later",
}
EXPECTED_CATEGORIES = {
    "required_before_nlmytgen_ingest",
    "required_before_transfer_candidate",
    "optional_enrichments",
    "prohibited_or_out_of_scope_for_nlmytgen",
    "hold_requires_human_review",
}


def _checklist() -> dict:
    return json.loads(CHECKLIST_PATH.read_text(encoding="utf-8"))


def _items(checklist: dict) -> list[dict]:
    return [
        item
        for category in checklist["categories"]
        for item in category["items"]
    ]


def test_real_packet_readiness_checklist_parses_and_identifies_artifact() -> None:
    checklist = _checklist()

    assert checklist["artifact_id"] == "newsroom_real_packet_readiness_checklist_v1_2026_06_20"
    assert checklist["repo_relative_path"] == (
        "samples/_probe/newsroom_handoff/real_packet_readiness_checklist.json"
    )
    assert checklist["review_status"] == "ready_for_supervisor_review"
    assert checklist["current_packet_state"] == "synthetic_fixture_only"
    assert checklist["real_packet_accepted"] is False
    assert checklist["production_approval"] is False
    assert checklist["ymm4_transfer_ready"] is False


def test_real_packet_readiness_checklist_has_required_categories() -> None:
    checklist = _checklist()

    categories = {category["category_id"] for category in checklist["categories"]}
    assert EXPECTED_CATEGORIES <= categories
    assert all(category["items"] for category in checklist["categories"])


def test_real_packet_readiness_items_have_required_fields_and_values() -> None:
    checklist = _checklist()

    for item in _items(checklist):
        assert item["owner"] in ALLOWED_OWNERS
        assert item["current_coverage"] in ALLOWED_COVERAGE
        assert item["failure_behavior"] in ALLOWED_FAILURE_BEHAVIOR
        assert item["next_action"] in ALLOWED_NEXT_ACTION
        assert item["id"]
        assert item["label"]
        assert item["requirement"]


def test_real_packet_readiness_prohibits_source_ymmp_render_and_publish_paths() -> None:
    checklist = _checklist()
    prohibited = next(
        category
        for category in checklist["categories"]
        if category["category_id"] == "prohibited_or_out_of_scope_for_nlmytgen"
    )
    text = json.dumps(prohibited, ensure_ascii=False)

    for expected in [
        "RSS/source discovery",
        "source fetching",
        "article scraping",
        "Inoreader operation",
        "YMM4 transfer",
        ".ymmp generation",
        "render generation",
        "publishing/upload",
    ]:
        assert expected in text


def test_real_packet_readiness_requires_no_real_urls_or_external_fetch() -> None:
    raw_text = CHECKLIST_PATH.read_text(encoding="utf-8")
    checklist = json.loads(raw_text)

    assert re.search(r"https?://|www\.", raw_text, flags=re.IGNORECASE) is None
    assert checklist["diagnostic_only"] is True
    assert checklist["real_packet_accepted"] is False
    assert checklist["source_artifacts"]["synthetic_packet"].endswith(
        "minimal_episode_packet.json"
    )
