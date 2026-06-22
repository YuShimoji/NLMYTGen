import json
import re
from pathlib import Path

from src.pipeline.newsroom_diagnostic_transfer_candidate_proof import (
    DEFAULT_DIAGNOSTIC_TRANSFER_PROOF_DOC_PATH,
    DEFAULT_DIAGNOSTIC_TRANSFER_PROOF_PATH,
    DIAGNOSTIC_TRANSFER_PROOF_ID,
    DIAGNOSTIC_TRANSFER_PROOF_SCHEMA_VERSION,
    build_default_newsroom_diagnostic_transfer_candidate_proof,
    render_newsroom_diagnostic_transfer_candidate_proof_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = ROOT / DEFAULT_DIAGNOSTIC_TRANSFER_PROOF_PATH
PROOF_DOC_PATH = ROOT / DEFAULT_DIAGNOSTIC_TRANSFER_PROOF_DOC_PATH


def _proof() -> dict:
    return json.loads(PROOF_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_diagnostic_transfer_candidate_proof_parses_and_matches_builder() -> None:
    proof = _proof()

    assert proof == build_default_newsroom_diagnostic_transfer_candidate_proof(root=ROOT)
    assert proof["artifact_id"] == DIAGNOSTIC_TRANSFER_PROOF_ID
    assert proof["schema_version"] == DIAGNOSTIC_TRANSFER_PROOF_SCHEMA_VERSION
    assert proof["review_status"] == "ready_for_supervisor_review"
    assert proof["review_axis"] == "diagnostic_transfer_candidate_scope"
    assert proof["diagnostic_only"] is True
    assert proof["production_status"] == "diagnostic_transfer_candidate_proof_only"
    assert proof["source"]["prior_transfer_planning_blocker_count"] == 14


def test_decision_split_keeps_production_blocked_but_opens_synthetic_candidate() -> None:
    proof = _proof()
    decision = proof["decision_split"]
    production = proof["production_transfer_blockage"]
    diagnostic = proof["diagnostic_import_possibility"]

    assert decision["answer"] == "yes_for_synthetic_neutral_timeline_candidate"
    assert decision["production_transfer_status"] == "blocked"
    assert decision["production_YMM4_candidate"] is False
    assert decision["diagnostic_import_status"] == "candidate_with_placeholders"
    assert decision["diagnostic_import_candidate"] is True
    assert production["transfer_status"] == "blocked"
    assert production["YMM4_candidate"] is False
    assert production["blocker_count"] == 13
    assert production["unlock_requirement_count"] == 13
    assert diagnostic["status"] == "open_next_as_synthetic_candidate"
    assert diagnostic["candidate"] is True
    assert diagnostic["hard_blocker_count"] == 0


def test_existing_blockers_are_classified_for_synthetic_diagnostic_scope() -> None:
    proof = _proof()
    summary = proof["blocker_classification_summary"]
    rows = proof["blocker_classifications"]
    by_code = {row["code"]: row for row in rows}

    assert summary == {
        "production_only": 7,
        "diagnostic_hard_blocker": 0,
        "diagnostic_soft_warning": 5,
        "already_satisfied_for_synthetic": 1,
        "total_blockers": 13,
        "diagnostic_hard_blocker_codes": [],
    }
    assert set(by_code) == {
        "rights_clearance_not_cleared",
        "rights_summary_blocks_ymm4_transfer",
        "rights_risk_flags_present",
        "raw_source_material_not_included",
        "placeholder_source_notes_only",
        "review_warning_blocks_transfer:warning_fake_rights_hold",
        "review_warning_blocks_transfer:warning_fake_no_production_readiness",
        "review_console_is_read_only",
        "visual_slot_gaps_present",
        "validator_transfer_status_blocked",
        "slot_linkage_transfer_status_blocked",
        "ymm4_transfer_ready_false",
        "downstream_blocking_reasons_present",
    }
    assert by_code["rights_clearance_not_cleared"]["classification"] == "production_only"
    assert by_code["raw_source_material_not_included"]["classification"] == (
        "diagnostic_soft_warning"
    )
    assert by_code["placeholder_source_notes_only"]["classification"] == (
        "diagnostic_soft_warning"
    )
    assert by_code["review_console_is_read_only"]["classification"] == (
        "already_satisfied_for_synthetic"
    )
    assert by_code["visual_slot_gaps_present"]["classification"] == (
        "diagnostic_soft_warning"
    )
    assert by_code["ymm4_transfer_ready_false"]["classification"] == "production_only"
    assert {
        row["classification"] for row in rows
    } <= {
        "production_only",
        "diagnostic_hard_blocker",
        "diagnostic_soft_warning",
        "already_satisfied_for_synthetic",
    }


def test_minimal_import_requirements_are_met_without_audio_media_or_ymm4() -> None:
    proof = _proof()
    requirements = proof["minimal_import_requirements"]
    rows = requirements["requirements"]

    assert requirements["candidate_scope"] == "synthetic_neutral_timeline_import"
    assert requirements["all_minimal_requirements_met"] is True
    assert requirements["missing_fields_for_synthetic_candidate"] == []
    assert requirements["audio_required_for_synthetic_candidate"] is False
    assert requirements["media_required_for_synthetic_candidate"] is False
    assert requirements["YMM4_specific_mapping_required_next"] is True
    assert {row["requirement"] for row in rows} == {
        "episode identity",
        "beat timing windows",
        "caption unit timing",
        "refined caption text",
        "visual placeholder references",
        "no-audio/no-media boundary",
    }
    assert all(row["status"] == "available" for row in rows)
    assert "neutral import schema name and version" in requirements[
        "required_next_fields_before_importable_proof"
    ]
    assert "TTS or narration audio" in requirements[
        "non_requirements_for_synthetic_candidate"
    ]


def test_next_tiny_importable_proof_plan_is_neutral_and_bounded() -> None:
    proof = _proof()
    plan = proof["next_tiny_importable_proof_plan"]
    fields = {row["field"] for row in plan["exact_fields_to_map_next"]}

    assert plan["recommended_next_slice"] == "newsroom-neutral-timeline-import-proof-v1"
    assert plan["output_candidates"] == [
        "neutral_timeline_json",
        "optional_caption_csv",
    ]
    assert "episode_id" in fields
    assert "caption_id/refined_caption_text/line_count_target/max_chars_target" in fields
    assert "visual_id/g28_slot/layout_hint/caption_interference_risk" in fields
    assert "diagnostic_only/no_audio/no_media/no_render" in fields
    assert ".ymmp project" in plan["prohibited_outputs"]
    assert "YMM4 carrier" in plan["prohibited_outputs"]
    assert any("Production transfer remains blocked" in item for item in plan["acceptance_checks"])


def test_review_memory_boundary_and_video_readiness_remain_diagnostic_only() -> None:
    proof = _proof()
    review_memory = proof["review_memory"]
    review_card = proof["review_card"]
    video = proof["video_readiness"]
    boundary = proof["boundary_assertions"]

    assert review_memory["prior_user_review_count"] == 0
    assert review_memory["current_review_axis"] == "diagnostic_transfer_candidate_scope"
    assert review_memory["next_nonredundant_axis"] == "neutral_import_field_mapping"
    assert review_memory["repeated_general_caption_or_timing_review_allowed"] is False
    assert review_card["status"] == "none"
    assert video["total_duration_sec"] == 68
    assert video["caption_unit_count"] == 4
    assert video["visual_count"] == 2
    assert video["TTS_generated"] is False
    assert video["production_video_ready"] is False
    assert video["diagnostic_neutral_import_candidate"] is True
    assert boundary["opens_production_transfer"] is False
    assert boundary["opens_YMM4_transfer"] is False
    assert boundary["real_packet_ingested"] is False
    assert boundary["ymmp_generated"] is False
    assert boundary["render_generated"] is False
    assert boundary["tts_generated"] is False
    assert boundary["public_video"] is False


def test_diagnostic_transfer_artifacts_have_no_real_urls_or_media_outputs() -> None:
    json_text = PROOF_PATH.read_text(encoding="utf-8")
    doc_text = PROOF_DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(json_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(PROOF_PATH.parent.glob("diagnostic_transfer_candidate_proof*.ymmp"))
    assert not list(PROOF_PATH.parent.glob("diagnostic_transfer_candidate_proof*.mp4"))
    assert not list(PROOF_PATH.parent.glob("diagnostic_transfer_candidate_proof*.wav"))
    assert not list(PROOF_PATH.parent.glob("diagnostic_transfer_candidate_proof*.mp3"))


def test_diagnostic_transfer_doc_matches_renderer_and_states_boundary() -> None:
    proof = _proof()
    doc_text = PROOF_DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_diagnostic_transfer_candidate_proof_markdown(proof)
    assert "## Decision Split" in doc_text
    assert "candidate_with_placeholders" in doc_text
    assert "| diagnostic_hard_blocker | 0 |" in doc_text
    assert "Review Card: none" in doc_text
    assert "TTS_generated=false" in doc_text
    assert "fixed phrase required: yes" not in doc_text.lower()
