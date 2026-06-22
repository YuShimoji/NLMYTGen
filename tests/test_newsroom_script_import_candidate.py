import csv
import json
import re
from pathlib import Path

from src.pipeline.newsroom_neutral_timeline_import_proof import (
    DEFAULT_CAPTION_IMPORT_CSV_PATH,
    DEFAULT_NEUTRAL_TIMELINE_PATH,
)
from src.pipeline.newsroom_script_import_candidate import (
    DEFAULT_SCRIPT_IMPORT_CANDIDATE_DOC_PATH,
    DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH,
    SCRIPT_IMPORT_CANDIDATE_ID,
    SCRIPT_IMPORT_CANDIDATE_SCHEMA_VERSION,
    SCRIPT_LINE_REQUIRED_FIELDS,
    build_default_newsroom_script_import_candidate,
    render_newsroom_script_import_candidate_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_PATH = ROOT / DEFAULT_SCRIPT_IMPORT_CANDIDATE_PATH
CANDIDATE_DOC_PATH = ROOT / DEFAULT_SCRIPT_IMPORT_CANDIDATE_DOC_PATH
CAPTION_CSV_PATH = ROOT / DEFAULT_CAPTION_IMPORT_CSV_PATH
NEUTRAL_TIMELINE_PATH = ROOT / DEFAULT_NEUTRAL_TIMELINE_PATH


def _candidate() -> dict:
    return json.loads(CANDIDATE_PATH.read_text(encoding="utf-8"))


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


def test_script_import_candidate_parses_and_matches_builder_output() -> None:
    candidate = _candidate()

    assert candidate == build_default_newsroom_script_import_candidate(root=ROOT)
    assert candidate["artifact_id"] == SCRIPT_IMPORT_CANDIDATE_ID
    assert candidate["script_candidate_id"] == SCRIPT_IMPORT_CANDIDATE_ID
    assert candidate["schema_version"] == SCRIPT_IMPORT_CANDIDATE_SCHEMA_VERSION
    assert candidate["review_status"] == "ready_for_supervisor_review"
    assert candidate["diagnostic_only"] is True
    assert candidate["production_status"] == "diagnostic_only"
    assert candidate["import_status"] == "candidate_with_placeholders"
    assert candidate["script_import_status"] == "passed"
    assert candidate["line_count"] == 4
    assert candidate["identity"]["source_csv_path"] == str(
        DEFAULT_CAPTION_IMPORT_CSV_PATH
    ).replace("\\", "/")
    assert candidate["identity"]["source_neutral_timeline_path"] == str(
        DEFAULT_NEUTRAL_TIMELINE_PATH
    ).replace("\\", "/")
    assert candidate["identity"]["source_episode_id"] == "episode_fake_nlmytgen_delta_v1"


def test_script_lines_have_required_schema_and_placeholders() -> None:
    candidate = _candidate()
    schema = candidate["schema_validation"]
    lines = candidate["script_lines"]

    assert schema["script_lines_array_present"] is True
    assert schema["required_line_fields"] == list(SCRIPT_LINE_REQUIRED_FIELDS)
    assert schema["line_count"] == 4
    assert schema["expected_line_count"] == 4
    assert schema["required_line_fields_present"] is True
    assert schema["errors"] == []
    assert schema["warnings"] == []
    assert [line["source_caption_id"] for line in lines] == [
        "cap_beat_fake_intro_001_01",
        "cap_beat_fake_intro_001_02",
        "cap_beat_fake_claim_001_01",
        "cap_beat_fake_claim_001_02",
    ]
    for index, line in enumerate(lines, start=1):
        assert line["line_id"].startswith(f"line_{index:02d}_")
        assert line["speaker_id"] == "synthetic_newsroom_placeholder"
        assert line["diagnostic_only"] is True
        assert line["production_ready"] is False
        assert line["tts_ready"] is False
        assert line["source_ref"] == f"caption_csv.caption_id:{line['source_caption_id']}"
        assert line["source_neutral_timeline_item_id"]
        assert line["voice_profile"] == {
            "voice_profile_id": "voice_placeholder_not_generated",
            "voice_status": "placeholder_not_generated",
            "TTS_generated": False,
            "audio_file": None,
            "audio_required_for_this_candidate": False,
        }


def test_script_lines_map_one_to_one_to_caption_csv_rows() -> None:
    candidate = _candidate()
    rows = _csv_rows()
    mapping = candidate["csv_to_script_mapping"]

    assert mapping["line_count"] == 4
    assert mapping["csv_row_count"] == 4
    assert mapping["every_line_maps_exactly_one_csv_caption_row"] is True
    assert mapping["every_csv_row_mapped"] is True
    assert mapping["source_caption_ids_are_unique"] is True
    assert mapping["timing_matches"] is True
    assert mapping["text_matches"] is True
    assert mapping["missing_csv_caption_rows"] == []
    assert mapping["extra_script_lines"] == []
    assert mapping["duplicate_source_caption_ids"] == []
    assert mapping["errors"] == []
    for line, row, mapping_row in zip(
        candidate["script_lines"],
        rows,
        mapping["rows"],
        strict=True,
    ):
        assert line["source_caption_id"] == row["caption_id"]
        assert line["beat_id"] == row["beat_id"]
        assert line["start_sec"] == int(row["start_sec"])
        assert line["end_sec"] == int(row["end_sec"])
        assert line["duration_sec"] == int(row["duration_sec"])
        assert line["text"] == row["text"]
        assert mapping_row["source_caption_id_exists_in_csv"] is True
        assert mapping_row["one_line_for_csv_caption"] is True
        assert mapping_row["timing_matches_csv"] is True
        assert mapping_row["text_matches_csv"] is True


def test_script_line_validation_keeps_diagnostic_and_tts_blocked() -> None:
    candidate = _candidate()
    line_validation = candidate["line_validation"]

    assert line_validation["line_count"] == 4
    assert line_validation["expected_line_count"] == 4
    assert line_validation["all_lines_valid"] is True
    assert line_validation["all_lines_diagnostic_only"] is True
    assert line_validation["all_lines_production_not_ready"] is True
    assert line_validation["all_lines_tts_not_ready"] is True
    assert line_validation["all_speakers_are_synthetic_placeholders"] is True
    assert line_validation["all_voice_profiles_are_placeholders"] is True
    assert line_validation["errors"] == []
    for row in line_validation["rows"]:
        assert row["source_caption_id_exists_in_csv"] is True
        assert row["timing_matches_csv"] is True
        assert row["text_matches_csv"] is True
        assert row["diagnostic_only_is_true"] is True
        assert row["production_ready_is_false"] is True
        assert row["tts_ready_is_false"] is True
        assert row["speaker_id_is_synthetic_placeholder"] is True
        assert row["voice_profile_is_placeholder_not_generated"] is True
        assert row["status"] == "passed"
        assert row["errors"] == []


def test_script_import_candidate_keeps_safety_and_next_use_closed() -> None:
    candidate = _candidate()
    safety = candidate["diagnostic_safety"]
    result = candidate["import_candidate_result"]
    boundary = candidate["boundary_assertions"]

    assert safety == {
        "real_urls": False,
        "real_media_paths": False,
        "TTS_generated": False,
        "render_created": False,
        "ymmp_created": False,
        "production_approval": False,
        "external_fetch_performed": False,
        "script_line_audio_files": [],
        "errors": [],
        "warnings": [],
    }
    assert result["script_import_status"] == "passed"
    assert result["allowed_next_artifacts"] == [
        "YMM4-adjacent no-media proof",
        "script import mapping proof",
        "tiny importable proof after another gate",
    ]
    assert result["prohibited_next_artifacts"] == [
        "production .ymmp",
        "render output",
        "TTS output",
        "real media",
    ]
    assert boundary["script_import_candidate"] is True
    assert boundary["source_csv_changed"] is False
    assert boundary["source_neutral_timeline_changed"] is False
    assert boundary["opens_production_transfer"] is False
    assert boundary["opens_YMM4_transfer"] is False
    assert boundary["real_urls"] is False
    assert boundary["real_media_paths"] is False
    assert boundary["TTS_generated"] is False
    assert boundary["render_created"] is False
    assert boundary["ymmp_created"] is False
    assert boundary["production_approval"] is False


def test_script_import_candidate_review_memory_and_doc_match_renderer() -> None:
    candidate = _candidate()
    review_memory = candidate["review_memory"]
    review_card = candidate["review_card"]
    doc_text = CANDIDATE_DOC_PATH.read_text(encoding="utf-8")

    assert review_memory["prior_user_review_count"] == 0
    assert "neutral_timeline_import_proof" in review_memory["accepted_scope"]
    assert "caption_csv_import_candidate_schema" in review_memory["accepted_scope"]
    assert review_memory["current_axis"] == "script_import_candidate_schema"
    assert review_memory["repeated_general_review_allowed"] is False
    assert review_card["status"] == "none"
    assert review_card["axis_if_needed"] == "script_import_candidate_schema"
    assert "No repeated timing" in review_card["not_asking"]
    assert doc_text == render_newsroom_script_import_candidate_markdown(candidate)
    assert "script_import_status: passed" in doc_text
    assert "voice_status=placeholder_not_generated" in doc_text
    assert "tts_ready=false" in doc_text
    assert "Review Card: none" in doc_text


def test_script_import_candidate_artifacts_have_no_real_urls_or_outputs() -> None:
    candidate_text = CANDIDATE_PATH.read_text(encoding="utf-8")
    doc_text = CANDIDATE_DOC_PATH.read_text(encoding="utf-8")
    csv_text = CAPTION_CSV_PATH.read_text(encoding="utf-8")
    neutral_timeline_text = NEUTRAL_TIMELINE_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(candidate_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert _real_url_pattern().search(csv_text) is None
    assert _real_url_pattern().search(neutral_timeline_text) is None
    assert not list(CANDIDATE_PATH.parent.glob("script_import_candidate*.ymmp"))
    assert not list(CANDIDATE_PATH.parent.glob("script_import_candidate*.mp4"))
    assert not list(CANDIDATE_PATH.parent.glob("script_import_candidate*.wav"))
    assert not list(CANDIDATE_PATH.parent.glob("script_import_candidate*.mp3"))
