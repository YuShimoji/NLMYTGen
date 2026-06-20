import json
import re
from pathlib import Path

import pytest

from src.cli.main import main as cli_main
from src.pipeline.newsroom_export_adapter import (
    ADAPTER_VERSION,
    adapt_newsroom_export_fixture,
    build_newsroom_export_adapter_readback,
    load_newsroom_export_fixture,
)
from src.pipeline.newsroom_handoff_validator import (
    build_g28_slot_linkage_proof,
    build_newsroom_transfer_planning_proof,
    validate_newsroom_handoff_packet,
)


ROOT = Path(__file__).resolve().parents[1]
ADAPTED_PACKET_PATH = (
    ROOT / "samples" / "_probe" / "newsroom_handoff" / "adapted_newsroom_export_packet.json"
)
ADAPTER_READBACK_PATH = (
    ROOT / "samples" / "_probe" / "newsroom_handoff" / "newsroom_export_adapter_readback.json"
)
NEWSROOM_FIXTURE_PATH = (
    ROOT.parent
    / "newsroom-yt-pipeline"
    / "samples"
    / "_probe"
    / "newsroom_handoff"
    / "newsroom_export_fixture_v1.json"
)


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def _inline_fixture() -> dict:
    return {
        "schema_version": "newsroom_export_fixture.v1",
        "fixture_id": "newsroom_export_fixture_for_nlmytgen_v1",
        "review_status": "fake_only_contract_probe",
        "episode_id": "episode_fake_nlmytgen_delta_v1",
        "title": "Fake upstream export delta for NLMYTGen",
        "topic_summary": "Fake placeholder summary for validating the export contract shape.",
        "source_notes": [
            {
                "source_id": "source_fake_primary_001",
                "role": "primary_source",
                "source_name": "Fake Official Source",
                "title": "Fake primary source placeholder",
                "url_status": "omitted_fake_fixture",
                "source_confidence": "medium_fake",
                "review_status": "fake_only",
            },
            {
                "source_id": "source_fake_critical_001",
                "role": "critical_view",
                "source_name": "Fake Critical View",
                "title": "Fake critical source placeholder",
                "url_status": "omitted_fake_fixture",
                "source_confidence": "low_fake",
                "review_status": "hold_for_review",
            },
        ],
        "provenance": {
            "rss_fetch": "not_performed",
            "inoreader_fetch": "not_performed",
            "web_access": "not_performed",
            "external_downloads": "not_performed",
            "raw_article_body_included": False,
            "real_urls_included": False,
            "notes": "Fake fixture only.",
        },
        "rights_summary": {
            "status": "hold_for_review",
            "media_availability": "none_in_fixture",
            "external_assets": "not_included",
            "quote_clearance": "not_requested",
            "publication_approval": "not_granted",
            "failure_behavior": "block_transfer",
        },
        "notebooklm_packet": {
            "packet_id": "packet_fake_nlmytgen_delta_v1",
            "format_hint": "manual_bridge_seed",
            "source_refs": [
                "source_fake_primary_001",
                "source_fake_critical_001",
            ],
            "transcript_seed": {
                "status": "fake_seed",
                "summary": "Fake transcript seed only; not approved narration.",
            },
            "notebooklm_api_status": "not_performed",
        },
        "script_beats": [
            {
                "beat_id": "beat_fake_intro_001",
                "stable_id": "scriptbeat_fake_intro_001",
                "chapter_id": "chapter_fake_intro",
                "summary": "Introduce the fake topic.",
                "source_refs": [],
                "visual_refs": ["visual_fake_title_card_001"],
                "review_status": "fake_only",
            },
            {
                "beat_id": "beat_fake_claim_001",
                "stable_id": "scriptbeat_fake_claim_001",
                "chapter_id": "chapter_fake_claim",
                "summary": "Present a fake claim with source coverage.",
                "source_refs": [
                    "source_fake_primary_001",
                    "source_fake_critical_001",
                ],
                "visual_refs": ["visual_fake_evidence_card_001"],
                "review_status": "hold_for_review",
            },
        ],
        "visual_plan": [
            {
                "visual_id": "visual_fake_title_card_001",
                "stable_id": "visualslot_fake_title_card_001",
                "beat_id": "beat_fake_intro_001",
                "unit_type": "title_card",
                "asset_policy": "local_template_only",
                "approval_state": "fake_only",
            },
            {
                "visual_id": "visual_fake_evidence_card_001",
                "stable_id": "visualslot_fake_evidence_card_001",
                "beat_id": "beat_fake_claim_001",
                "unit_type": "claim_evidence_card",
                "asset_policy": "local_template_only",
                "approval_state": "hold_for_review",
            },
        ],
        "g28_slot_hints": [
            {
                "slot_id": "g28_slot_fake_title_001",
                "visual_id": "visual_fake_title_card_001",
                "hint_type": "text_safe_area",
                "recommended_role": "title_safe_readback",
                "geometry_authority": "downstream_nlmytgen",
            },
            {
                "slot_id": "g28_slot_fake_evidence_001",
                "visual_id": "visual_fake_evidence_card_001",
                "hint_type": "evidence_label_group",
                "recommended_role": "source_and_counterpoint_readback",
                "geometry_authority": "downstream_nlmytgen",
            },
        ],
        "review_warnings": [
            {
                "warning_id": "warning_fake_rights_hold",
                "severity": "hold_for_review",
                "message": "Rights and media availability require review.",
            },
            {
                "warning_id": "warning_fake_no_production_readiness",
                "severity": "block_transfer",
                "message": "Fake fixture does not imply production readiness.",
            },
        ],
        "downstream_readiness": {
            "nlmytgen_ingest": "warn",
            "transfer_candidate": "block_transfer",
            "human_review": "hold_for_review",
            "production_ymm4": "fail",
        },
        "export_metadata": {
            "created_by": "newsroom-yt-pipeline fake fixture",
            "source_repo": "newsroom-yt-pipeline",
            "intended_consumer": "NLMYTGen downstream adapter readiness probe",
            "contains_real_news": False,
            "contains_credentials": False,
            "contains_media": False,
            "contains_external_downloads": False,
        },
        "source_confidence": {"overall": "fake_only"},
        "editorial_priority": {"level": "medium_fake"},
        "reviewer_notes": [{"note_id": "reviewer_note_fake_001", "text": "Freeform note."}],
        "localization_notes": {"language": "ja-JP"},
        "channel_metadata": {
            "series_id": "series_fake_nlmytgen_delta",
            "package_id": "package_fake_nlmytgen_delta_v1",
        },
        "boundary_assertions": {
            "rss_source_discovery_owner": "newsroom-yt-pipeline",
            "production_readiness_implied": False,
            "ymm4_geometry_authority": "downstream_nlmytgen",
        },
    }


def test_adapter_maps_inline_fixture_to_validator_compatible_packet() -> None:
    packet = adapt_newsroom_export_fixture(_inline_fixture(), source_path="fake_fixture.json")
    validation = validate_newsroom_handoff_packet(packet)

    assert packet["artifact_id"] == "newsroom_export_fixture_for_nlmytgen_v1"
    assert packet["contract_version"] == "newsroom_export_fixture.v1"
    assert packet["adapter_version"] == ADAPTER_VERSION
    assert packet["provenance"]["external_fetch_allowed_by_nlmytgen"] is False
    assert packet["rights_summary"]["clearance_state"] == "hold_for_review"
    assert packet["downstream_readiness"]["ymm4_transfer_ready"] is False
    assert packet["adapter_readiness"]["production_approval"] is False
    assert packet["adapter_readiness"]["ymmp_generated"] is False
    assert validation.status == "passed"
    assert validation.transfer_status == "blocked"
    assert validation.errors == []


def test_adapter_preserves_stable_ids_and_g28_aliases() -> None:
    packet = adapt_newsroom_export_fixture(_inline_fixture())

    assert {beat["stable_id"] for beat in packet["script_beats"]} == {
        "scriptbeat_fake_intro_001",
        "scriptbeat_fake_claim_001",
    }
    assert {visual["stable_id"] for visual in packet["visual_plan"]} == {
        "visualslot_fake_title_card_001",
        "visualslot_fake_evidence_card_001",
    }
    assert {
        hint["object_catalog_slot"] for hint in packet["g28_slot_hints"]
    } == {"caption_reserve", "source_note"}


def test_committed_adapted_packet_passes_validator_and_blocks_transfer() -> None:
    packet = _json(ADAPTED_PACKET_PATH)
    validation = validate_newsroom_handoff_packet(packet, packet_path=ADAPTED_PACKET_PATH)

    assert validation.status == "passed"
    assert validation.transfer_status == "blocked"
    assert validation.errors == []
    assert validation.ymm4_transfer_ready is False
    assert "rights_clearance_not_cleared:hold_for_review" in validation.blockers
    assert "rights_summary_blocks_ymm4_transfer" in validation.blockers


def test_committed_adapter_readback_matches_existing_proof_chain() -> None:
    packet = _json(ADAPTED_PACKET_PATH)
    readback = _json(ADAPTER_READBACK_PATH)
    slot_linkage = build_g28_slot_linkage_proof(packet, packet_path=ADAPTED_PACKET_PATH)
    transfer = build_newsroom_transfer_planning_proof(
        packet,
        slot_linkage.to_dict(),
        packet_path=ADAPTED_PACKET_PATH,
    )
    transfer_payload = transfer.to_dict()

    assert readback["status"] == "passed_with_adapter_warnings_transfer_blocked"
    assert readback["raw_fixture_direct_ingest"] == "not_accepted_requires_adapter"
    assert readback["transform_counts"]["missing_required_count"] == 0
    assert readback["upstream_adjustment_still_needed"] is False
    assert readback["validation_result"]["adapter_packet_validator_status"] == "passed"
    assert readback["validation_result"]["slot_linkage_status"] == slot_linkage.status
    assert readback["validation_result"]["transfer_planning_status"] == transfer.status
    assert readback["validation_result"]["transfer_planning_blocker_count"] == (
        transfer_payload["blocker_count"]
    )
    assert transfer.transfer_status == "blocked"
    assert transfer_payload["unlock_requirement_count"] > 0


def test_adapter_readback_keeps_review_and_transfer_approvals_false() -> None:
    readback = _json(ADAPTER_READBACK_PATH)

    assert readback["real_packet_accepted"] is False
    assert readback["rights_approval"] is False
    assert readback["media_approval"] is False
    assert readback["review_approval"] is False
    assert readback["production_approval"] is False
    assert readback["ymm4_transfer_ready"] is False
    assert "media_source_availability" in readback["upstream_gap_fields"]


def test_adapter_artifacts_have_no_real_urls() -> None:
    for path in [ADAPTED_PACKET_PATH, ADAPTER_READBACK_PATH]:
        assert _real_url_pattern().search(path.read_text(encoding="utf-8")) is None


def test_sibling_newsroom_fixture_adapts_when_checkout_exists() -> None:
    if not NEWSROOM_FIXTURE_PATH.exists():
        pytest.skip("newsroom-yt-pipeline checkout is not available")

    fixture = load_newsroom_export_fixture(NEWSROOM_FIXTURE_PATH)
    packet = adapt_newsroom_export_fixture(
        fixture,
        source_path="../newsroom-yt-pipeline/samples/_probe/newsroom_handoff/newsroom_export_fixture_v1.json",
    )
    readback = build_newsroom_export_adapter_readback(
        fixture,
        packet,
        fixture_path="../newsroom-yt-pipeline/samples/_probe/newsroom_handoff/newsroom_export_fixture_v1.json",
        packet_path="samples/_probe/newsroom_handoff/adapted_newsroom_export_packet.json",
    )

    assert _real_url_pattern().search(NEWSROOM_FIXTURE_PATH.read_text(encoding="utf-8")) is None
    assert packet["artifact_id"] == "newsroom_export_fixture_for_nlmytgen_v1"
    assert readback["validation_result"]["adapter_packet_validator_status"] == "passed"
    assert readback["validation_result"]["transfer_planning_transfer_status"] == "blocked"


def test_adapter_cli_writes_packet_and_readback_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    fixture_path = tmp_path / "newsroom_export_fixture_v1.json"
    packet_path = tmp_path / "adapted_packet.json"
    readback_path = tmp_path / "adapter_readback.json"
    fixture_path.write_text(json.dumps(_inline_fixture(), ensure_ascii=False, indent=2), encoding="utf-8")

    exit_code = cli_main([
        "adapt-newsroom-export-fixture",
        str(fixture_path),
        "--out-packet",
        str(packet_path),
        "--out-readback",
        str(readback_path),
        "--format",
        "json",
    ])

    captured = capsys.readouterr()
    summary = json.loads(captured.out)
    packet = _json(packet_path)
    readback = _json(readback_path)

    assert exit_code == 0
    assert captured.err == ""
    assert summary["status"] == "passed_with_adapter_warnings_transfer_blocked"
    assert summary["adapter_packet_validator_status"] == "passed"
    assert summary["adapter_packet_transfer_status"] == "blocked"
    assert summary["transfer_planning_transfer_status"] == "blocked"
    assert summary["real_packet_accepted"] is False
    assert summary["rights_approval"] is False
    assert summary["production_approval"] is False
    assert summary["ymm4_transfer_ready"] is False
    assert packet["artifact_id"] == "newsroom_export_fixture_for_nlmytgen_v1"
    assert readback["validation_result"]["adapter_packet_validator_status"] == "passed"
    assert _real_url_pattern().search(packet_path.read_text(encoding="utf-8")) is None
    assert _real_url_pattern().search(readback_path.read_text(encoding="utf-8")) is None
    assert not list(tmp_path.glob("*.ymmp"))


def test_adapter_cli_missing_fixture_fails_without_outputs(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    packet_path = tmp_path / "adapted_packet.json"
    readback_path = tmp_path / "adapter_readback.json"

    exit_code = cli_main([
        "adapt-newsroom-export-fixture",
        str(tmp_path / "missing_fixture.json"),
        "--out-packet",
        str(packet_path),
        "--out-readback",
        str(readback_path),
        "--format",
        "json",
    ])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert "Error:" in captured.err
    assert not packet_path.exists()
    assert not readback_path.exists()


def test_adapter_cli_does_not_modify_sibling_newsroom_fixture(tmp_path: Path) -> None:
    if not NEWSROOM_FIXTURE_PATH.exists():
        pytest.skip("newsroom-yt-pipeline checkout is not available")

    before = NEWSROOM_FIXTURE_PATH.read_bytes()
    exit_code = cli_main([
        "adapt-newsroom-export-fixture",
        str(NEWSROOM_FIXTURE_PATH),
        "--out-packet",
        str(tmp_path / "adapted_packet.json"),
        "--out-readback",
        str(tmp_path / "adapter_readback.json"),
        "--format",
        "json",
    ])
    after = NEWSROOM_FIXTURE_PATH.read_bytes()

    assert exit_code == 0
    assert after == before
