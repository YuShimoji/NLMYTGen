import csv
import json
import re
from pathlib import Path

from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    ALLOWED_MANUAL_IMPORT_RESULTS,
    DEFAULT_MANUAL_IMPORT_CHECK_PACKET_DOC_PATH,
    DEFAULT_MANUAL_IMPORT_CHECK_PACKET_PATH,
    DEFAULT_MANUAL_IMPORT_RESULT_TEMPLATE_PATH,
    EXPECTED_MANUAL_IMPORT_ROW_COUNT,
    FAILURE_CATEGORIES,
    MANUAL_IMPORT_CHECK_PACKET_ID,
    MANUAL_IMPORT_CHECK_PACKET_SCHEMA_VERSION,
    MANUAL_IMPORT_RESULT_TEMPLATE_ID,
    MANUAL_IMPORT_RESULT_TEMPLATE_SCHEMA_VERSION,
    REQUIRED_EVIDENCE_FIELDS,
    TARGET_SURFACE_COLUMNS,
    build_default_newsroom_yym4_manual_import_check_packet,
    build_default_newsroom_yym4_manual_import_result_template,
    render_newsroom_yym4_manual_import_check_packet_markdown,
)
from src.pipeline.newsroom_tiny_importable_proof import (
    DEFAULT_TINY_IMPORT_CSV_PATH,
    DEFAULT_TINY_IMPORTABLE_PROOF_PATH,
)


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / DEFAULT_MANUAL_IMPORT_CHECK_PACKET_PATH
RESULT_TEMPLATE_PATH = ROOT / DEFAULT_MANUAL_IMPORT_RESULT_TEMPLATE_PATH
DOC_PATH = ROOT / DEFAULT_MANUAL_IMPORT_CHECK_PACKET_DOC_PATH
CSV_PATH = ROOT / DEFAULT_TINY_IMPORT_CSV_PATH
TINY_PROOF_PATH = ROOT / DEFAULT_TINY_IMPORTABLE_PROOF_PATH


def _packet() -> dict:
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


def _result_template() -> dict:
    return json.loads(RESULT_TEMPLATE_PATH.read_text(encoding="utf-8"))


def _tiny_proof() -> dict:
    return json.loads(TINY_PROOF_PATH.read_text(encoding="utf-8"))


def _csv_rows() -> list[list[str]]:
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_manual_import_check_packet_matches_builder_output() -> None:
    packet = _packet()

    assert packet == build_default_newsroom_yym4_manual_import_check_packet(root=ROOT)
    assert packet["artifact_id"] == MANUAL_IMPORT_CHECK_PACKET_ID
    assert packet["packet_id"] == MANUAL_IMPORT_CHECK_PACKET_ID
    assert packet["schema_version"] == MANUAL_IMPORT_CHECK_PACKET_SCHEMA_VERSION
    assert packet["review_status"] == "ready_for_operator_manual_check"
    assert packet["diagnostic_only"] is True
    assert packet["production_status"] == "diagnostic_only"
    assert packet["manual_check_status"] == "not_run"
    assert packet["identity"]["packet_id"] == MANUAL_IMPORT_CHECK_PACKET_ID
    assert packet["identity"]["source_tiny_csv_path"] == str(
        DEFAULT_TINY_IMPORT_CSV_PATH
    ).replace("\\", "/")
    assert packet["identity"]["source_tiny_proof_path"] == str(
        DEFAULT_TINY_IMPORTABLE_PROOF_PATH
    ).replace("\\", "/")
    assert packet["identity"]["production_status"] == "diagnostic_only"
    assert packet["identity"]["manual_check_status"] == "not_run"


def test_target_artifact_is_the_committed_tiny_csv_contract() -> None:
    packet = _packet()
    tiny_proof = _tiny_proof()
    target = packet["target_artifact"]
    rows = _csv_rows()

    assert CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf")
    assert target["path"] == str(DEFAULT_TINY_IMPORT_CSV_PATH).replace("\\", "/")
    assert target["filename"] == "tiny_script_import_candidate_v1.csv"
    assert target["encoding"] == "utf-8-sig"
    assert target["encoding_verified"] is True
    assert target["has_header"] is False
    assert target["header_expectation"] == "no_header"
    assert target["surface"] == list(TARGET_SURFACE_COLUMNS)
    assert target["expected_rows"] == EXPECTED_MANUAL_IMPORT_ROW_COUNT
    assert target["observed_rows_before_manual_check"] == 4
    assert target["all_rows_two_columns"] is True
    assert target["timing_columns_expected"] is False
    assert target["production_ready_flags_expected"] is False
    assert rows[0] != ["speaker", "text"]
    assert len(rows) == 4
    assert all(len(row) == 2 for row in rows)
    assert [[row["speaker"], row["text"]] for row in target["rows"]] == rows
    assert target["rows"] == [
        {
            "row_number": row["csv_row_number"],
            "speaker": row["speaker"],
            "text": row["text"],
        }
        for row in tiny_proof["import_artifact_rows"]
    ]


def test_preconditions_and_procedure_keep_yym4_manual_only() -> None:
    packet = _packet()
    preconditions = packet["preconditions"]
    procedure_text = "\n".join(
        step["action"] for step in packet["manual_procedure"]
    )
    precondition_text = "\n".join(
        item["requirement"] for item in preconditions["items"]
    )

    assert preconditions["YMM4_manual_open_only"] is True
    assert preconditions["no_production_project"] is True
    assert preconditions["no_render"] is True
    assert preconditions["no_TTS"] is True
    assert preconditions["no_real_media"] is True
    assert preconditions["do_not_commit_experimental_ymmp"] is True
    assert preconditions["tiny_csv_synthetic_diagnostic_only"] is True
    assert "user/operator only" in precondition_text
    assert "Do not commit any `.ymmp`" in precondition_text
    assert "blocked_by_operator_uncertainty" in precondition_text
    assert len(packet["manual_procedure"]) == 8
    assert "tiny_script_import_candidate_v1.csv" in procedure_text
    assert "Open YMM4 manually" in procedure_text
    assert "script import / 台本読み込み" in procedure_text
    assert "ツール -> 台本読み込み" in procedure_text
    assert "operator_menu_unknown" in procedure_text
    assert "UTF-8 BOM / utf-8-sig" in procedure_text
    assert "headerless" in procedure_text
    assert "speaker,text" in procedure_text
    assert "exactly 4 lines/rows" in procedure_text
    assert "without render" in procedure_text
    assert "without committing any `.ymmp`" in procedure_text


def test_success_observation_and_failure_categories_are_complete() -> None:
    packet = _packet()
    expected = packet["expected_successful_observation"]
    failures = packet["failure_categories"]

    assert expected["imported_line_count"] == 4
    assert "synthetic_newsroom_placeholder" in expected["speaker_placeholder_behavior"]
    assert "safely unmapped" in expected["speaker_placeholder_behavior"]
    assert expected["text_behavior"] == "all 4 target CSV texts appear in order"
    assert expected["expected_texts"] == [row[1] for row in _csv_rows()]
    assert expected["timing_import_expected"] is False
    assert expected["audio_media_render_expected"] is False
    assert expected["audio_expected"] is False
    assert expected["media_expected"] is False
    assert expected["render_expected"] is False
    assert [failure["category"] for failure in failures] == list(FAILURE_CATEGORIES)
    for required in (
        "encoding_error",
        "header_or_column_mismatch",
        "speaker_binding_error",
        "text_import_error",
        "row_count_mismatch",
        "unsupported_csv_shape",
        "operator_menu_unknown",
        "unexpected_YMM4_behavior",
    ):
        assert required in [failure["category"] for failure in failures]


def test_evidence_contract_result_template_and_next_actions_are_bounded() -> None:
    packet = _packet()
    template = _result_template()
    evidence = packet["evidence_template"]
    contract = packet["result_recording_contract"]
    next_actions = packet["next_actions_by_result"]

    assert template == build_default_newsroom_yym4_manual_import_result_template(
        root=ROOT
    )
    assert template["artifact_id"] == MANUAL_IMPORT_RESULT_TEMPLATE_ID
    assert template["template_id"] == MANUAL_IMPORT_RESULT_TEMPLATE_ID
    assert (
        template["schema_version"]
        == MANUAL_IMPORT_RESULT_TEMPLATE_SCHEMA_VERSION
    )
    assert template["packet_id"] == packet["packet_id"]
    assert template["manual_check_status"] == "not_run"
    assert template["source_packet_path"] == str(
        DEFAULT_MANUAL_IMPORT_CHECK_PACKET_PATH
    ).replace("\\", "/")
    assert contract["required_fields"] == list(REQUIRED_EVIDENCE_FIELDS)
    assert contract["allowed_results"] == list(ALLOWED_MANUAL_IMPORT_RESULTS)
    assert contract["accepts_only_human_operator_observation"] is True
    assert (
        contract["no_agent_claim_of_YMM4_result_without_operator_evidence"]
        is True
    )
    assert evidence["screenshot_path_placeholder"] == (
        "operator_screenshot_path_placeholder"
    )
    assert evidence["observed_line_count"] is None
    assert evidence["observed_speaker_behavior"] is None
    assert evidence["observed_text_behavior"] is None
    assert evidence["error_message"] is None
    assert evidence["operator_notes_freeform"] == ""
    assert evidence["result"] is None
    assert evidence["allowed_results"] == list(ALLOWED_MANUAL_IMPORT_RESULTS)
    assert template["evidence_template"] == evidence
    assert next_actions["pass"].startswith("Create a result readback")
    assert "tiny YMM4 import-readiness proof" in next_actions["pass"]
    assert next_actions["pass_with_warnings"].startswith("Classify warnings")
    assert next_actions["fail"].startswith("Adjust CSV shape or encoding")
    assert next_actions["blocked_by_operator_uncertainty"] == (
        "Improve manual instructions, not the pipeline."
    )


def test_safety_validation_review_card_and_doc_match_renderer() -> None:
    packet = _packet()
    template = _result_template()
    validation = packet["validation"]
    review_memory = packet["review_memory"]
    review_card = packet["review_card"]
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert packet["safety_boundary"] == {
        "ymmp_created_by_agent": False,
        "YMM4_launched_by_agent": False,
        "render_created": False,
        "TTS_generated": False,
        "real_media_imported": False,
        "production_approval": False,
        "public_video_ready": False,
    }
    assert packet["boundary_assertions"]["agent_import_observation_claimed"] is False
    assert packet["boundary_assertions"]["external_fetch_performed"] is False
    assert (
        packet["boundary_assertions"]["real_newsroom_ingest_performed"]
        is False
    )
    assert validation["target_csv_bom_verified"] is True
    assert validation["target_csv_has_no_header"] is True
    assert validation["target_csv_row_count_matches_expected"] is True
    assert validation["target_csv_all_rows_two_columns"] is True
    assert validation["manual_check_not_run"] is True
    assert validation["review_card_required"] is False
    assert review_memory["current_axis"] == "YMM4_manual_import_check_packet"
    assert "tiny_importable_artifact_shape" in review_memory["accepted_scope"]
    assert review_memory["repeated_general_review_allowed"] is False
    assert review_card["status"] == "none"
    assert review_card["axis_if_needed"] == "YMM4_manual_import_check_packet"
    assert doc_text == render_newsroom_yym4_manual_import_check_packet_markdown(
        packet,
        template,
    )
    assert "manual_check_status: not_run" in doc_text
    assert "Review Card: none" in doc_text
    assert "YMM4_launched_by_agent: false" in doc_text


def test_manual_import_check_artifacts_have_no_real_urls_or_outputs() -> None:
    packet_text = PACKET_PATH.read_text(encoding="utf-8")
    template_text = RESULT_TEMPLATE_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    csv_text = CSV_PATH.read_text(encoding="utf-8-sig")

    assert _real_url_pattern().search(packet_text) is None
    assert _real_url_pattern().search(template_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert _real_url_pattern().search(csv_text) is None
    assert not list(PACKET_PATH.parent.glob("yym4_manual_import*.ymmp"))
    assert not list(PACKET_PATH.parent.glob("yym4_manual_import*.mp4"))
    assert not list(PACKET_PATH.parent.glob("yym4_manual_import*.wav"))
    assert not list(PACKET_PATH.parent.glob("yym4_manual_import*.mp3"))
    assert not list(PACKET_PATH.parent.glob("yym4_manual_import*.m4a"))
