import csv
import json
import re
from pathlib import Path

from src.pipeline.newsroom_caption_csv_import_candidate import (
    CAPTION_CSV_IMPORT_CANDIDATE_ID,
    CAPTION_CSV_IMPORT_CANDIDATE_SCHEMA_VERSION,
    DEFAULT_CAPTION_CSV_IMPORT_CANDIDATE_DOC_PATH,
    DEFAULT_CAPTION_CSV_IMPORT_CANDIDATE_READBACK_PATH,
    REQUIRED_COLUMNS,
    build_default_newsroom_caption_csv_import_candidate,
    render_newsroom_caption_csv_import_candidate_markdown,
)
from src.pipeline.newsroom_neutral_timeline_import_proof import (
    DEFAULT_CAPTION_IMPORT_CSV_PATH,
    DEFAULT_NEUTRAL_TIMELINE_PATH,
)


ROOT = Path(__file__).resolve().parents[1]
READBACK_PATH = ROOT / DEFAULT_CAPTION_CSV_IMPORT_CANDIDATE_READBACK_PATH
READBACK_DOC_PATH = ROOT / DEFAULT_CAPTION_CSV_IMPORT_CANDIDATE_DOC_PATH
CAPTION_CSV_PATH = ROOT / DEFAULT_CAPTION_IMPORT_CSV_PATH
NEUTRAL_TIMELINE_PATH = ROOT / DEFAULT_NEUTRAL_TIMELINE_PATH


def _readback() -> dict:
    return json.loads(READBACK_PATH.read_text(encoding="utf-8"))


def _neutral_timeline() -> dict:
    return json.loads(NEUTRAL_TIMELINE_PATH.read_text(encoding="utf-8"))


def _csv_rows() -> list[dict[str, str]]:
    return list(
        csv.DictReader(
            CAPTION_CSV_PATH.read_text(encoding="utf-8").splitlines()
        )
    )


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_caption_csv_import_candidate_parses_and_matches_builder_output() -> None:
    readback = _readback()

    assert readback == build_default_newsroom_caption_csv_import_candidate(root=ROOT)
    assert readback["artifact_id"] == CAPTION_CSV_IMPORT_CANDIDATE_ID
    assert readback["schema_version"] == CAPTION_CSV_IMPORT_CANDIDATE_SCHEMA_VERSION
    assert readback["review_status"] == "ready_for_supervisor_review"
    assert readback["diagnostic_only"] is True
    assert readback["production_status"] == "diagnostic_only"
    assert readback["caption_csv_import_status"] == "passed"
    assert readback["source"]["source_csv_path"] == str(
        DEFAULT_CAPTION_IMPORT_CSV_PATH
    ).replace("\\", "/")
    assert readback["source"]["source_neutral_timeline_path"] == str(
        DEFAULT_NEUTRAL_TIMELINE_PATH
    ).replace("\\", "/")
    assert readback["source"]["source_episode_id"] == "episode_fake_nlmytgen_delta_v1"


def test_caption_csv_schema_is_caption_only_and_has_no_ymm4_requirements() -> None:
    readback = _readback()
    schema = readback["schema_validation"]
    rows = _csv_rows()

    assert rows
    assert schema["required_columns"] == list(REQUIRED_COLUMNS)
    assert schema["actual_columns"] == list(REQUIRED_COLUMNS)
    assert list(rows[0].keys()) == list(REQUIRED_COLUMNS)
    assert schema["missing_columns"] == []
    assert schema["extra_columns"] == []
    assert schema["required_columns_present"] is True
    assert schema["column_order_matches_required"] is True
    assert schema["extra_columns_blocking"] is False
    assert schema["required_YMM4_columns"] == []
    assert schema["YMM4_columns_required"] is False
    assert schema["errors"] == []
    assert schema["warnings"] == []


def test_caption_csv_rows_validate_minimum_import_candidate_contract() -> None:
    readback = _readback()
    row_validation = readback["row_validation"]
    rows = row_validation["rows"]

    assert row_validation["row_count"] == 4
    assert row_validation["expected_row_count"] == 4
    assert row_validation["all_rows_valid"] is True
    assert row_validation["errors"] == []
    assert [row["caption_id"] for row in rows] == [
        "cap_beat_fake_intro_001_01",
        "cap_beat_fake_intro_001_02",
        "cap_beat_fake_claim_001_01",
        "cap_beat_fake_claim_001_02",
    ]
    for row in rows:
        assert row["caption_id"]
        assert row["beat_id"]
        assert row["start_sec"] < row["end_sec"]
        assert row["duration_sec"] == row["end_sec"] - row["start_sec"]
        assert row["text"]
        assert row["diagnostic_only_is_true"] is True
        assert row["production_ready_is_false"] is True
        assert row["status"] == "passed"
        assert row["errors"] == []


def test_caption_csv_matches_neutral_timeline_caption_items() -> None:
    readback = _readback()
    timeline = _neutral_timeline()
    consistency = readback["neutral_timeline_consistency"]
    caption_items = [
        item
        for item in timeline["items"]
        if item["item_kind"] == "caption"
    ]

    assert consistency["neutral_timeline_caption_count"] == 4
    assert consistency["csv_caption_count"] == 4
    assert consistency["every_csv_caption_id_exists"] is True
    assert consistency["timing_matches"] is True
    assert consistency["text_matches"] is True
    assert consistency["missing_caption_rows"] == []
    assert consistency["extra_caption_rows"] == []
    assert consistency["errors"] == []
    assert len(consistency["rows"]) == len(caption_items)
    for row, item in zip(consistency["rows"], caption_items, strict=True):
        assert row["caption_id"] == item["caption_id"]
        assert row["neutral_timeline_item_id"] == item["item_id"]
        assert row["exists_in_neutral_timeline"] is True
        assert row["timing_matches"] is True
        assert row["text_matches"] is True


def test_caption_csv_import_candidate_keeps_diagnostic_safety_and_next_use() -> None:
    readback = _readback()
    safety = readback["diagnostic_safety"]
    result = readback["import_candidate_result"]
    boundary = readback["boundary_assertions"]

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
    assert result["caption_csv_import_status"] == "passed"
    assert result["recommended_next_slice"] == "newsroom-script-import-candidate-v1"
    assert result["allowed_next_artifacts"] == [
        "script import candidate",
        "neutral timeline consumer proof",
        "YMM4-adjacent no-media proof",
    ]
    assert "production .ymmp" in result["prohibited_next_artifacts"]
    assert "render output" in result["prohibited_next_artifacts"]
    assert "TTS output" in result["prohibited_next_artifacts"]
    assert boundary["caption_only_import_candidate"] is True
    assert boundary["source_csv_changed"] is False
    assert boundary["opens_production_transfer"] is False
    assert boundary["opens_YMM4_transfer"] is False
    assert boundary["requires_YMM4_columns"] is False
    assert boundary["ymmp_created"] is False
    assert boundary["render_created"] is False
    assert boundary["TTS_generated"] is False
    assert boundary["production_approval"] is False


def test_caption_csv_import_candidate_review_memory_and_doc_match_renderer() -> None:
    readback = _readback()
    review_memory = readback["review_memory"]
    review_card = readback["review_card"]
    doc_text = READBACK_DOC_PATH.read_text(encoding="utf-8")

    assert review_memory["prior_user_review_count"] == 0
    assert "neutral_timeline_import_proof" in review_memory["accepted_scope"]
    assert review_memory["current_axis"] == "caption_csv_import_candidate_schema"
    assert review_memory["repeated_general_review_allowed"] is False
    assert review_card["status"] == "none"
    assert review_card["axis_if_needed"] == "caption_csv_import_candidate_schema"
    assert "No repeated timing" in review_card["not_asking"]
    assert doc_text == render_newsroom_caption_csv_import_candidate_markdown(readback)
    assert "caption_csv_import_status: passed" in doc_text
    assert "required_YMM4_columns: none" in doc_text
    assert "production_ready=false" in doc_text
    assert "Review Card: none" in doc_text
    assert "fixed phrase required: yes" not in doc_text.lower()


def test_caption_csv_import_candidate_artifacts_have_no_real_urls_or_outputs() -> None:
    readback_text = READBACK_PATH.read_text(encoding="utf-8")
    doc_text = READBACK_DOC_PATH.read_text(encoding="utf-8")
    csv_text = CAPTION_CSV_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(readback_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert _real_url_pattern().search(csv_text) is None
    assert not list(READBACK_PATH.parent.glob("caption_csv_import_candidate*.ymmp"))
    assert not list(READBACK_PATH.parent.glob("caption_csv_import_candidate*.mp4"))
    assert not list(READBACK_PATH.parent.glob("caption_csv_import_candidate*.wav"))
    assert not list(READBACK_PATH.parent.glob("caption_csv_import_candidate*.mp3"))
