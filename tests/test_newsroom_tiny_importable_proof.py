import csv
import json
import re
from pathlib import Path

from src.pipeline.newsroom_tiny_importable_proof import (
    DEFAULT_TINY_IMPORT_CSV_PATH,
    DEFAULT_TINY_IMPORTABLE_DOC_PATH,
    DEFAULT_TINY_IMPORTABLE_PROOF_PATH,
    TINY_IMPORT_COLUMNS,
    TINY_IMPORT_WARNINGS,
    TINY_IMPORTABLE_PROOF_ID,
    TINY_IMPORTABLE_SCHEMA_VERSION,
    build_default_newsroom_tiny_importable_proof,
    render_newsroom_tiny_importable_proof_markdown,
)
from src.pipeline.newsroom_yym4_adjacent_no_media_import_shape import (
    DEFAULT_YYM4_ADJACENT_NO_MEDIA_PROOF_PATH,
)


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / DEFAULT_TINY_IMPORT_CSV_PATH
PROOF_PATH = ROOT / DEFAULT_TINY_IMPORTABLE_PROOF_PATH
PROOF_DOC_PATH = ROOT / DEFAULT_TINY_IMPORTABLE_DOC_PATH
YYM4_ADJACENT_PATH = ROOT / DEFAULT_YYM4_ADJACENT_NO_MEDIA_PROOF_PATH


def _proof() -> dict:
    return json.loads(PROOF_PATH.read_text(encoding="utf-8"))


def _yym4_adjacent_shape() -> dict:
    return json.loads(YYM4_ADJACENT_PATH.read_text(encoding="utf-8"))


def _csv_rows() -> list[list[str]]:
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_tiny_importable_proof_parses_and_matches_builder_output() -> None:
    proof = _proof()

    assert proof == build_default_newsroom_tiny_importable_proof(root=ROOT)
    assert proof["artifact_id"] == TINY_IMPORTABLE_PROOF_ID
    assert proof["proof_id"] == TINY_IMPORTABLE_PROOF_ID
    assert proof["schema_version"] == TINY_IMPORTABLE_SCHEMA_VERSION
    assert proof["review_status"] == "ready_for_supervisor_review"
    assert proof["diagnostic_only"] is True
    assert proof["production_status"] == "diagnostic_only"
    assert proof["tiny_importable_status"] == "passed_with_warnings"
    assert proof["identity"]["import_artifact_path"] == str(
        DEFAULT_TINY_IMPORT_CSV_PATH
    ).replace("\\", "/")
    assert proof["identity"]["import_artifact_type"] == "tool_adjacent_csv"
    assert proof["identity"]["repo_consistent_value"] == (
        "speaker_text_no_header_utf8_bom_when_written"
    )


def test_tiny_import_csv_uses_repo_two_column_no_header_contract() -> None:
    proof = _proof()
    rows = _csv_rows()
    raw = CSV_PATH.read_bytes()
    schema = proof["import_artifact_schema"]

    assert raw.startswith(b"\xef\xbb\xbf")
    assert schema["columns"] == list(TINY_IMPORT_COLUMNS)
    assert schema["has_header"] is False
    assert schema["encoding"] == "utf-8-sig"
    assert schema["delimiter"] == ","
    assert schema["row_count"] == 4
    assert schema["timing_columns_in_csv"] is False
    assert schema["production_ready_flags_in_csv"] is False
    assert len(rows) == 4
    assert rows[0] != ["speaker", "text"]
    assert all(len(row) == 2 for row in rows)
    assert rows == [
        [row["speaker"], row["text"]]
        for row in proof["import_artifact_rows"]
    ]


def test_tiny_import_rows_map_to_yym4_adjacent_rows() -> None:
    proof = _proof()
    yym4_adjacent = _yym4_adjacent_shape()
    mapping_rows = yym4_adjacent["mapping_rows"]

    assert proof["source_validation"]["source_artifacts_identified"] is True
    assert proof["source_validation"]["source_mapping_row_count"] == 4
    assert proof["source_validation"]["source_yym4_adjacent_status"] == (
        "passed_with_warnings"
    )
    assert len(proof["source_mapping"]) == 4
    for proof_row, source_row, csv_row in zip(
        proof["source_mapping"],
        mapping_rows,
        proof["import_artifact_rows"],
        strict=True,
    ):
        assert proof_row["source_row_id"] == source_row["row_id"]
        assert proof_row["source_line_id"] == source_row["source_line_id"]
        assert proof_row["source_caption_id"] == source_row["source_caption_id"]
        assert proof_row["beat_id"] == source_row["beat_id"]
        assert proof_row["start_sec"] == source_row["start_sec"]
        assert proof_row["end_sec"] == source_row["end_sec"]
        assert proof_row["duration_sec"] == source_row["duration_sec"]
        assert proof_row["timing_policy"] == "metadata_only_not_in_script_csv"
        assert csv_row["speaker"] == source_row["speaker_id"]
        assert csv_row["text"] == source_row["text"]
        assert csv_row["source_row_id"] == source_row["row_id"]


def test_row_validation_keeps_tiny_csv_clean_and_source_backed() -> None:
    proof = _proof()
    validation = proof["row_validation"]

    assert validation["row_count"] == 4
    assert validation["expected_row_count"] == 4
    assert validation["every_row_maps_exactly_one_source_row"] is True
    assert validation["all_rows_valid"] is True
    assert validation["no_real_names_detected"] is True
    assert validation["no_real_urls_detected"] is True
    assert validation["no_media_paths_detected"] is True
    assert validation["errors"] == []
    for row in validation["rows"]:
        assert row["source_row_exists"] is True
        assert row["speaker_non_empty"] is True
        assert row["text_non_empty"] is True
        assert row["text_matches_source_row"] is True
        assert row["no_real_names"] is True
        assert row["no_real_urls"] is True
        assert row["no_media_paths"] is True
        assert row["status"] == "passed"


def test_timing_no_media_and_boundary_status_are_preserved() -> None:
    proof = _proof()
    timing = proof["timing_policy"]
    boundary = proof["boundary_status"]
    assertions = proof["boundary_assertions"]

    assert timing == {
        "policy": "metadata_only",
        "not_in_script_csv": True,
        "metadata_fields": ["start_sec", "end_sec", "duration_sec"],
    }
    assert proof["no_media_policy"] == [
        "captions_and_script_rows_only",
        "no_render",
        "no_TTS",
        "no_real_assets",
    ]
    assert boundary["ymmp_created"] is False
    assert boundary["YMM4_launched"] is False
    assert boundary["YMM4_carrier_created"] is False
    assert boundary["YMM4_approval"] is False
    assert boundary["TTS_generated"] is False
    assert boundary["render_created"] is False
    assert boundary["production_approval"] is False
    assert boundary["public_video_ready"] is False
    assert assertions["tiny_importable_artifact_shape"] is True
    assert assertions["tool_adjacent_not_YMM4_verified"] is True
    assert assertions["opens_production_transfer"] is False
    assert assertions["opens_YMM4_transfer"] is False


def test_result_records_expected_warnings_and_next_slice() -> None:
    proof = _proof()
    safety = proof["diagnostic_safety"]
    result = proof["result"]

    assert safety == {
        "real_urls": False,
        "real_media_paths": False,
        "TTS_generated": False,
        "render_created": False,
        "ymmp_created": False,
        "production_approval": False,
        "external_fetch_performed": False,
        "row_audio_dependency_present": False,
        "row_media_dependency_present": False,
        "errors": [],
        "warnings": [],
    }
    assert result["tiny_importable_status"] == "passed_with_warnings"
    assert result["warnings"] == list(TINY_IMPORT_WARNINGS)
    assert result["errors"] == []
    assert result["recommended_next_slice"] == (
        "newsroom-import-readiness-review-surface-v1"
    )
    assert result["prohibited_next_artifacts"] == [
        "production .ymmp",
        "render output",
        "TTS output",
        "real media",
    ]


def test_review_memory_and_doc_match_renderer() -> None:
    proof = _proof()
    review_memory = proof["review_memory"]
    review_card = proof["review_card"]
    doc_text = PROOF_DOC_PATH.read_text(encoding="utf-8")

    assert review_memory["prior_user_review_count"] == 0
    assert "YMM4_adjacent_no_media_import_shape" in review_memory["accepted_scope"]
    assert review_memory["current_axis"] == "tiny_importable_artifact_shape"
    assert review_memory["repeated_general_review_allowed"] is False
    assert review_card["status"] == "none"
    assert review_card["axis_if_needed"] == "tiny_importable_artifact_shape"
    assert "No repeated timing/caption/copy" in review_card["not_asking"]
    assert doc_text == render_newsroom_tiny_importable_proof_markdown(proof)
    assert "tiny_importable_status: passed_with_warnings" in doc_text
    assert "has_header: false" in doc_text
    assert "timing_columns_in_csv: false" in doc_text
    assert "Review Card: none" in doc_text


def test_tiny_importable_artifacts_have_no_real_urls_or_outputs() -> None:
    proof_text = PROOF_PATH.read_text(encoding="utf-8")
    doc_text = PROOF_DOC_PATH.read_text(encoding="utf-8")
    csv_text = CSV_PATH.read_text(encoding="utf-8-sig")

    assert _real_url_pattern().search(proof_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert _real_url_pattern().search(csv_text) is None
    assert not list(CSV_PATH.parent.glob("tiny_script_import_candidate*.ymmp"))
    assert not list(CSV_PATH.parent.glob("tiny_script_import_candidate*.mp4"))
    assert not list(CSV_PATH.parent.glob("tiny_script_import_candidate*.wav"))
    assert not list(CSV_PATH.parent.glob("tiny_script_import_candidate*.mp3"))
