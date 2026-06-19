import copy
import json
from pathlib import Path

from src.cli import main as cli_main
from src.pipeline.newsroom_handoff_validator import (
    ALLOWED_G28_SLOT_SET,
    build_g28_slot_linkage_proof,
    load_newsroom_handoff_packet,
    validate_newsroom_handoff_packet,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "samples" / "_probe" / "newsroom_handoff" / "minimal_episode_packet.json"


def _fixture() -> dict:
    return load_newsroom_handoff_packet(FIXTURE_PATH)


def test_minimal_newsroom_handoff_fixture_passes_structure_and_blocks_transfer() -> None:
    result = validate_newsroom_handoff_packet(_fixture(), packet_path=FIXTURE_PATH)

    assert result.status == "passed"
    assert result.transfer_status == "blocked"
    assert result.ymm4_transfer_ready is False
    assert result.counts["source_notes"] == 2
    assert result.counts["script_beats"] == 3
    assert result.counts["visual_plan"] == 2
    assert result.counts["g28_slot_hints"] == 4
    assert set(result.observed_g28_slots).issubset(set(ALLOWED_G28_SLOT_SET))
    assert "rights_summary_blocks_ymm4_transfer" in result.blockers
    assert any(blocker.startswith("review_warning_blocks_ymm4") for blocker in result.blockers)


def test_newsroom_handoff_validator_fails_closed_on_missing_identity() -> None:
    packet = _fixture()
    del packet["artifact_id"]

    result = validate_newsroom_handoff_packet(packet)

    assert result.status == "failed"
    assert "REQUIRED_FIELD_MISSING: artifact_id" in result.errors


def test_newsroom_handoff_validator_rejects_unknown_g28_slot() -> None:
    packet = _fixture()
    packet["g28_slot_hints"][0]["object_catalog_slot"] = "unknown_visual_slot"

    result = validate_newsroom_handoff_packet(packet)

    assert result.status == "failed"
    assert "G28_SLOT_UNKNOWN_OBJECT: slot_screenshot_frame->unknown_visual_slot" in result.errors


def test_newsroom_handoff_validator_rejects_unknown_references() -> None:
    packet = _fixture()
    packet["script_beats"][0]["evidence_refs"] = ["src_missing"]
    packet["visual_plan"][0]["beat_id"] = "beat_missing"
    packet["g28_slot_hints"][0]["source_ref"] = "src_missing"

    result = validate_newsroom_handoff_packet(packet)

    assert result.status == "failed"
    assert "SCRIPT_BEAT_UNKNOWN_SOURCE_REF: beat_001->src_missing" in result.errors
    assert "VISUAL_UNKNOWN_BEAT_REF: vis_001->beat_missing" in result.errors
    assert "G28_SLOT_UNKNOWN_SOURCE_REF: slot_screenshot_frame->src_missing" in result.errors


def test_newsroom_handoff_validator_rejects_transfer_ready_when_blockers_exist() -> None:
    packet = copy.deepcopy(_fixture())
    packet["downstream_readiness"]["ymm4_transfer_ready"] = True

    result = validate_newsroom_handoff_packet(packet)

    assert result.status == "failed"
    assert result.transfer_status == "blocked"
    assert "YMM4_READY_CONTRADICTS_BLOCKERS" in result.errors


def test_newsroom_handoff_validator_keeps_transfer_blocked_when_structure_fails() -> None:
    packet = _fixture()
    packet["rights_summary"]["clearance_state"] = "cleared"
    packet["rights_summary"]["blocked_uses"] = []
    packet["review_warnings"] = [
        {**warning, "blocks_ymm4_transfer": False}
        for warning in packet["review_warnings"]
    ]
    packet["downstream_readiness"]["ymm4_transfer_ready"] = True
    packet["downstream_readiness"]["blocking_reasons"] = []
    del packet["artifact_id"]

    result = validate_newsroom_handoff_packet(packet)

    assert result.status == "failed"
    assert result.transfer_status == "blocked"
    assert "REQUIRED_FIELD_MISSING: artifact_id" in result.errors


def test_cli_validate_newsroom_handoff_outputs_json(capsys) -> None:
    exit_code = cli_main.main(
        [
            "validate-newsroom-handoff",
            str(FIXTURE_PATH),
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["status"] == "passed"
    assert payload["transfer_status"] == "blocked"
    assert payload["counts"]["g28_slot_hints"] == 4


def test_cli_validate_newsroom_handoff_returns_nonzero_for_invalid_packet(
    tmp_path,
    capsys,
) -> None:
    packet = _fixture()
    packet.pop("source_notes")
    packet_path = tmp_path / "bad_packet.json"
    packet_path.write_text(json.dumps(packet), encoding="utf-8")

    exit_code = cli_main.main(
        [
            "validate-newsroom-handoff",
            str(packet_path),
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert payload["status"] == "failed"
    assert "REQUIRED_FIELD_MISSING: source_notes" in payload["errors"]


def test_g28_slot_linkage_proof_maps_fixture_to_review_surfaces() -> None:
    proof = build_g28_slot_linkage_proof(_fixture(), packet_path=FIXTURE_PATH)

    assert proof.status == "passed_with_warnings"
    assert proof.validator_status == "passed"
    assert proof.transfer_status == "blocked"
    assert len(proof.linkages) == 4
    assert all(item["slot_allowed"] for item in proof.linkages)
    assert {
        item["selected_g28_slot"] for item in proof.linkages
    } == {"screenshot_slot", "source_note", "quote_card", "caption_reserve"}
    assert any(
        warning == "MISSING_G28_SLOT_HINT: vis_001->callout_box,caption_reserve"
        for warning in proof.warnings
    )
    assert any(
        warning == "MISSING_G28_SLOT_HINT: vis_002->label_chip,source_note"
        for warning in proof.warnings
    )
    assert proof.review_surface_index["object_catalog"].endswith("object_catalog.html")


def test_g28_slot_linkage_proof_fails_when_validator_fails() -> None:
    packet = _fixture()
    packet["g28_slot_hints"][0]["object_catalog_slot"] = "unknown_visual_slot"

    proof = build_g28_slot_linkage_proof(packet)

    assert proof.status == "failed"
    assert "G28_SLOT_UNKNOWN_OBJECT: slot_screenshot_frame->unknown_visual_slot" in proof.errors
    assert any(
        item["slot_id"] == "slot_screenshot_frame" and item["slot_allowed"] is False
        for item in proof.linkages
    )


def test_g28_slot_linkage_proof_fails_closed_for_malformed_lists() -> None:
    packet = _fixture()
    packet["source_notes"].append("bad source note")
    packet["g28_slot_hints"].append("bad slot hint")

    proof = build_g28_slot_linkage_proof(packet)

    assert proof.status == "failed"
    assert "FIELD_ITEM_TYPE_INVALID: source_notes[2] must be an object" in proof.errors
    assert "FIELD_ITEM_TYPE_INVALID: g28_slot_hints[4] must be an object" in proof.errors


def test_g28_slot_linkage_proof_rejects_ready_claim_with_blockers() -> None:
    packet = _fixture()
    packet["downstream_readiness"]["ymm4_transfer_ready"] = True

    proof = build_g28_slot_linkage_proof(packet)

    assert proof.status == "failed"
    assert proof.transfer_status == "blocked"
    assert "YMM4_READY_CONTRADICTS_BLOCKERS" in proof.errors


def test_cli_prove_newsroom_g28_slot_linkage_outputs_json(capsys) -> None:
    exit_code = cli_main.main(
        [
            "prove-newsroom-g28-slot-linkage",
            str(FIXTURE_PATH),
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["status"] == "passed_with_warnings"
    assert payload["transfer_status"] == "blocked"
    assert len(payload["linkages"]) == 4
    assert payload["visual_slot_gaps"]


def test_cli_prove_newsroom_g28_slot_linkage_writes_markdown(tmp_path, capsys) -> None:
    output_path = tmp_path / "slot_linkage.md"

    exit_code = cli_main.main(
        [
            "prove-newsroom-g28-slot-linkage",
            str(FIXTURE_PATH),
            "-o",
            str(output_path),
        ]
    )

    captured = capsys.readouterr()
    text = output_path.read_text(encoding="utf-8")
    assert exit_code == 0
    assert "Written:" in captured.out
    assert "# Newsroom G-28 Slot Linkage Proof" in text
    assert "screenshot_slot" in text
    assert "transfer_status: blocked" in text
