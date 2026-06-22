import json
import re
from pathlib import Path

from src.pipeline.newsroom_neutral_timeline_import_proof import (
    DEFAULT_CAPTION_IMPORT_CSV_PATH,
    DEFAULT_NEUTRAL_TIMELINE_PATH,
)
from src.pipeline.newsroom_script_import_candidate import (
    DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH,
)
from src.pipeline.newsroom_yym4_adjacent_no_media_import_shape import (
    DEFAULT_YYM4_ADJACENT_NO_MEDIA_DOC_PATH,
    DEFAULT_YYM4_ADJACENT_NO_MEDIA_PROOF_PATH,
    MAPPING_ROW_REQUIRED_FIELDS,
    STATIC_COMPATIBILITY_WARNINGS,
    YYM4_ADJACENT_NO_MEDIA_PROOF_ID,
    YYM4_ADJACENT_NO_MEDIA_SCHEMA_VERSION,
    build_default_newsroom_yym4_adjacent_no_media_import_shape,
    render_newsroom_yym4_adjacent_no_media_import_shape_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = ROOT / DEFAULT_YYM4_ADJACENT_NO_MEDIA_PROOF_PATH
PROOF_DOC_PATH = ROOT / DEFAULT_YYM4_ADJACENT_NO_MEDIA_DOC_PATH
SCRIPT_CANDIDATE_PATH = ROOT / DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH
CAPTION_CSV_PATH = ROOT / DEFAULT_CAPTION_IMPORT_CSV_PATH
NEUTRAL_TIMELINE_PATH = ROOT / DEFAULT_NEUTRAL_TIMELINE_PATH


def _proof() -> dict:
    return json.loads(PROOF_PATH.read_text(encoding="utf-8"))


def _script_candidate() -> dict:
    return json.loads(SCRIPT_CANDIDATE_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_no_media_import_shape_parses_and_matches_builder_output() -> None:
    proof = _proof()

    assert proof == build_default_newsroom_yym4_adjacent_no_media_import_shape(root=ROOT)
    assert proof["artifact_id"] == YYM4_ADJACENT_NO_MEDIA_PROOF_ID
    assert proof["proof_id"] == YYM4_ADJACENT_NO_MEDIA_PROOF_ID
    assert proof["schema_version"] == YYM4_ADJACENT_NO_MEDIA_SCHEMA_VERSION
    assert proof["review_status"] == "ready_for_supervisor_review"
    assert proof["diagnostic_only"] is True
    assert proof["production_status"] == "diagnostic_only"
    assert proof["production_transfer_status"] == "blocked"
    assert proof["yym4_status"] == "passed_with_warnings"
    assert proof["no_media_import_shape_status"] == "passed_with_warnings"
    assert proof["identity"]["source_script_candidate_path"] == str(
        DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH
    ).replace("\\", "/")
    assert proof["identity"]["source_caption_csv_path"] == str(
        DEFAULT_CAPTION_IMPORT_CSV_PATH
    ).replace("\\", "/")
    assert proof["identity"]["source_neutral_timeline_path"] == str(
        DEFAULT_NEUTRAL_TIMELINE_PATH
    ).replace("\\", "/")


def test_mapping_rows_are_derived_from_script_lines() -> None:
    proof = _proof()
    script_candidate = _script_candidate()
    mapping = proof["mapping_validation"]

    assert mapping["mapping_row_count"] == 4
    assert mapping["expected_mapping_row_count"] == 4
    assert mapping["script_line_count"] == 4
    assert mapping["every_script_line_mapped"] is True
    assert mapping["source_line_ids_are_unique"] is True
    assert mapping["all_rows_valid"] is True
    assert mapping["errors"] == []
    for row, line, validation_row in zip(
        proof["mapping_rows"],
        script_candidate["script_lines"],
        mapping["rows"],
        strict=True,
    ):
        assert set(MAPPING_ROW_REQUIRED_FIELDS).issubset(row)
        assert row["source_line_id"] == line["line_id"]
        assert row["source_caption_id"] == line["source_caption_id"]
        assert row["beat_id"] == line["beat_id"]
        assert row["start_sec"] == line["start_sec"]
        assert row["end_sec"] == line["end_sec"]
        assert row["duration_sec"] == line["duration_sec"]
        assert row["speaker_id"] == line["speaker_id"]
        assert row["voice_profile"] == line["voice_profile"]
        assert row["text"] == line["text"]
        assert row["row_kind"] == "dialogue_caption"
        assert validation_row["matches_source_script_line"] is True
        assert validation_row["source_caption_id_exists_in_csv"] is True
        assert validation_row["status"] == "passed"


def test_rows_match_repo_yym4_csv_adjacent_surface_without_importing() -> None:
    proof = _proof()
    conventions = proof["known_yym4_script_import_conventions"]

    assert conventions["found_in_repo"] is True
    assert "src/contracts/ymm4_csv_schema.py" in conventions["sources"]
    assert "src/pipeline/assemble_csv.py" in conventions["sources"]
    assert conventions["compatible_surface"] == "speaker_text_two_column_static_match_only"
    assert conventions["YMM4_verified"] is False
    for row in proof["mapping_rows"]:
        adjacent = row["tool_adjacent_row"]
        assert adjacent == {
            "format_family": "repo_ymm4_csv_two_column_static_contract",
            "columns": ["speaker", "text"],
            "speaker": row["speaker_id"],
            "text": row["text"],
            "known_import_contract": "speaker_text_no_header_utf8_bom_when_written",
            "timing_metadata_not_csv_column": True,
            "YMM4_verified": False,
        }


def test_no_media_placeholder_policy_and_boundary_remain_closed() -> None:
    proof = _proof()
    no_media = proof["no_media_placeholder_policy"]
    validation = proof["no_media_validation"]
    boundary = proof["YMM4_boundary"]
    assertions = proof["boundary_assertions"]

    assert no_media["visual_placeholders_consumed"] == "reference_only"
    assert no_media["audio_placeholder_consumed"] == "reference_only"
    assert no_media["no_media_policy"] == [
        "captions_and_script_rows_only",
        "no_render",
        "no_TTS",
        "no_real_assets",
    ]
    assert "YMM4 timeline geometry" in no_media["intentionally_not_represented"]
    assert validation["all_rows_no_media"] is True
    assert validation["all_rows_no_audio"] is True
    assert validation["all_rows_no_tts"] is True
    assert validation["all_voice_profiles_placeholder_not_generated"] is True
    assert validation["errors"] == []
    assert boundary["ymmp_created"] is False
    assert boundary["YMM4_launched"] is False
    assert boundary["YMM4_carrier_created"] is False
    assert boundary["YMM4_approval"] is False
    assert boundary["production_transfer_status"] == "blocked"
    assert assertions["tool_adjacent_not_YMM4_verified"] is True
    assert assertions["ymmp_created"] is False
    assert assertions["YMM4_launched"] is False
    assert assertions["YMM4_carrier_created"] is False
    assert assertions["YMM4_approval"] is False


def test_safety_and_result_record_static_compatibility_warnings() -> None:
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
        "errors": [],
        "warnings": [],
    }
    assert result["no_media_import_shape_status"] == "passed_with_warnings"
    assert result["warnings"] == list(STATIC_COMPATIBILITY_WARNINGS)
    assert result["errors"] == []
    assert result["recommended_next_slice"] == "newsroom-tiny-importable-proof-v1"
    assert result["prohibited_next_artifacts"] == [
        "production .ymmp",
        "render output",
        "TTS output",
        "real media",
    ]
    assert "Decide whether to emit a real repo YMM4 CSV artifact." in result[
        "missing_for_tiny_importable_proof"
    ]


def test_review_memory_and_doc_match_renderer() -> None:
    proof = _proof()
    review_memory = proof["review_memory"]
    review_card = proof["review_card"]
    doc_text = PROOF_DOC_PATH.read_text(encoding="utf-8")

    assert review_memory["prior_user_review_count"] == 0
    assert "diagnostic_script_import_candidate" in review_memory["accepted_scope"]
    assert review_memory["current_axis"] == "YMM4_adjacent_no_media_import_shape"
    assert review_memory["repeated_general_review_allowed"] is False
    assert review_card["status"] == "none"
    assert review_card["axis_if_needed"] == "YMM4_adjacent_no_media_import_shape"
    assert "No repeated timing/caption/copy" in review_card["not_asking"]
    assert doc_text == render_newsroom_yym4_adjacent_no_media_import_shape_markdown(proof)
    assert "no_media_import_shape_status: passed_with_warnings" in doc_text
    assert "YMM4_verified: false" in doc_text
    assert "Review Card: none" in doc_text


def test_no_media_proof_artifacts_have_no_real_urls_or_outputs() -> None:
    proof_text = PROOF_PATH.read_text(encoding="utf-8")
    doc_text = PROOF_DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(proof_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(PROOF_PATH.parent.glob("yym4_adjacent_no_media*.ymmp"))
    assert not list(PROOF_PATH.parent.glob("yym4_adjacent_no_media*.mp4"))
    assert not list(PROOF_PATH.parent.glob("yym4_adjacent_no_media*.wav"))
    assert not list(PROOF_PATH.parent.glob("yym4_adjacent_no_media*.mp3"))
