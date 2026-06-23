import csv
import json
import re
from pathlib import Path

from src.pipeline.newsroom_yym4_bound_speaker_import_readiness import (
    BOUND_SPEAKER_IMPORT_READINESS_ID,
    BOUND_SPEAKER_IMPORT_READINESS_SCHEMA_VERSION,
    DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_DOC_PATH,
    DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH,
    OBSERVED_YYM4_TIMELINE_APPROX_SEC,
    OBSERVED_YYM4_VERSION,
    build_default_newsroom_yym4_bound_speaker_import_readiness,
    render_newsroom_yym4_bound_speaker_import_readiness_markdown,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    DEFAULT_BOUND_SPEAKER_CSV_PATH,
    DEFAULT_SPEAKER_BINDING_POLICY_PATH,
    OBSERVED_MANUAL_CHARACTER,
)


ROOT = Path(__file__).resolve().parents[1]
READBACK_PATH = ROOT / DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH
DOC_PATH = ROOT / DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_DOC_PATH
BOUND_CSV_PATH = ROOT / DEFAULT_BOUND_SPEAKER_CSV_PATH
POLICY_PATH = ROOT / DEFAULT_SPEAKER_BINDING_POLICY_PATH


def _readback() -> dict:
    return json.loads(READBACK_PATH.read_text(encoding="utf-8"))


def _csv_rows() -> list[list[str]]:
    with BOUND_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_bound_speaker_readiness_matches_builder_output() -> None:
    readback = _readback()

    assert readback == build_default_newsroom_yym4_bound_speaker_import_readiness(
        root=ROOT
    )
    assert readback["artifact_id"] == BOUND_SPEAKER_IMPORT_READINESS_ID
    assert readback["readback_id"] == BOUND_SPEAKER_IMPORT_READINESS_ID
    assert (
        readback["schema_version"]
        == BOUND_SPEAKER_IMPORT_READINESS_SCHEMA_VERSION
    )
    assert readback["review_status"] == "ready_for_supervisor_review"
    assert readback["diagnostic_only"] is True
    assert readback["production_status"] == "diagnostic_only"
    assert readback["manual_observation_source"] == (
        "user_freeform_and_supervisor_screenshot"
    )
    assert readback["result"] == "pass"
    assert readback["identity"]["source_policy_path"] == str(
        DEFAULT_SPEAKER_BINDING_POLICY_PATH
    ).replace("\\", "/")
    assert readback["identity"]["source_bound_csv_path"] == str(
        DEFAULT_BOUND_SPEAKER_CSV_PATH
    ).replace("\\", "/")


def test_normalized_result_records_bound_speaker_observation() -> None:
    readback = _readback()
    result = readback["normalized_result"]
    review = readback["review_memory"]

    assert result["result"] == "pass"
    assert result["YMM4_version"] == OBSERVED_YYM4_VERSION
    assert result["observed_line_count"] == 4
    assert result["expected_line_count"] == 4
    assert result["all_text_visible"] is True
    assert result["speaker_selection_prompt_shown"] is False
    assert result["speaker_behavior"] == (
        "automatically_bound_to_yukkuri_reimu_in_current_environment"
    )
    assert result["selected_speaker_or_character"] == OBSERVED_MANUAL_CHARACTER
    assert result["encoding_or_text_issues"] is False
    assert result["header_or_column_issues"] is False
    assert result["script_editor_rows_visible"] is True
    assert result["main_timeline_dialogue_items_visible"] is True
    assert result["preview_text_visible"] is True
    assert result["observed_yym4_timeline_approx_sec"] == (
        OBSERVED_YYM4_TIMELINE_APPROX_SEC
    )
    assert result["render_created"] is False
    assert result["ymmp_committed"] is False
    assert result["production_approval"] is False
    assert review["prior_user_review_count"] == {
        "manual_import_behavior": 1,
        "bound_speaker_behavior": 1,
    }
    assert review["repeated_general_review_allowed"] is False
    assert review["input_mode"] == "freeform"


def test_accepted_import_surface_is_source_backed_by_bound_csv() -> None:
    readback = _readback()
    surface = readback["accepted_import_surface"]
    validation = readback["source_validation"]
    rows = _csv_rows()

    assert BOUND_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf")
    assert surface["encoding"] == "UTF-8 BOM"
    assert surface["header"] is False
    assert surface["columns"] == ["speaker", "text"]
    assert surface["speaker_value"] == OBSERVED_MANUAL_CHARACTER
    assert surface["row_count"] == 4
    assert surface["accepted_for"] == (
        "diagnostic_yym4_script_import_in_current_environment"
    )
    assert surface["environment"] == f"Planner007/YMM4 {OBSERVED_YYM4_VERSION}"
    assert surface["timing_columns_in_csv"] is False
    assert surface["production_ready_flags_in_csv"] is False
    assert len(rows) == 4
    assert rows[0] != ["speaker", "text"]
    assert all(row[0] == OBSERVED_MANUAL_CHARACTER for row in rows)
    assert all(len(row) == 2 for row in rows)
    assert validation["source_policy_status"] == "diagnostic_candidate"
    assert validation["bound_csv_bom_verified"] is True
    assert validation["bound_csv_has_header"] is False
    assert validation["bound_csv_all_rows_two_columns"] is True
    assert validation["bound_csv_row_count"] == 4
    assert validation["all_rows_use_bound_speaker"] is True
    assert validation["all_text_matches_policy_candidate"] is True
    assert validation["errors"] == []


def test_timing_gap_and_next_axes_are_preserved() -> None:
    readback = _readback()
    timing = readback["timing_gap"]
    policy_linkage = readback["policy_linkage"]

    assert timing["prior_neutral_timeline_total_sec"] == 68
    assert timing["observed_yym4_timeline_approx_sec"] == 8.48
    assert timing["timing_imported_from_csv"] is False
    assert timing["gap_sec"] == 59.52
    assert timing["observed_to_prior_duration_ratio"] == 0.1247
    assert "does not import the neutral 68 second timeline" in timing["meaning"]
    assert timing["next_timing_axis"] == [
        "minimal_ymmp_boundary_decision",
        "timing_patch_strategy",
        "YMM4_natural_duration_strategy",
    ]
    assert policy_linkage["readiness_delta"]["before"] == "not_YMM4_verified"
    assert policy_linkage["readiness_delta"]["after"] == (
        "diagnostic_import_accepted_in_current_environment_with_timing_gap"
    )
    assert (
        policy_linkage["readiness_delta"][
            "speaker_selection_prompt_removed_in_current_environment"
        ]
        is True
    )
    assert (
        policy_linkage["readiness_delta"][
            "automatic_portability_across_all_YMM4_installations"
        ]
        is False
    )
    assert readback["recommended_next_slices"] == [
        "newsroom-minimal-ymmp-boundary-decision-v1",
        "newsroom-yym4-timing-gap-strategy-v1",
        "newsroom-diagnostic-ymmp-probe-packet-v1",
    ]


def test_not_accepted_scope_safety_and_doc_match_renderer() -> None:
    readback = _readback()
    not_accepted = readback["not_accepted_scope"]
    safety = readback["safety_boundary"]
    boundary = readback["boundary_assertions"]
    review_card = readback["review_card"]
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert not_accepted == {
        "automatic_portability_across_all_YMM4_installations": False,
        "TTS_ready": False,
        "render_ready": False,
        "production_ready": False,
        "visual_layout_ready": False,
        "public_video_ready": False,
        "timing_import_from_neutral_timeline_metadata": False,
        "ymmp_ready": False,
    }
    assert safety == {
        "ymmp_created": False,
        "YMM4_launched_by_agent": False,
        "render_created": False,
        "TTS_generated": False,
        "real_media_imported": False,
        "production_approval": False,
        "public_video_ready": False,
    }
    assert boundary["YMM4_launched_by_agent"] is False
    assert boundary["agent_claims_only_user_observed_result"] is True
    assert boundary["timing_imported_from_csv"] is False
    assert boundary["dashboard_governance_freshness_changed"] is False
    assert review_card["status"] == "none"
    assert review_card["axis_if_needed"] == "minimal_ymmp_boundary_decision"
    assert doc_text == render_newsroom_yym4_bound_speaker_import_readiness_markdown(
        readback
    )
    assert "result: pass" in doc_text
    assert "observed_yym4_timeline_approx_sec: 8.48" in doc_text
    assert "Review Card: none" in doc_text


def test_bound_speaker_readiness_artifacts_have_no_real_urls_or_outputs() -> None:
    readback_text = READBACK_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    csv_text = BOUND_CSV_PATH.read_text(encoding="utf-8-sig")
    policy_text = POLICY_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(readback_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert _real_url_pattern().search(csv_text) is None
    assert _real_url_pattern().search(policy_text) is None
    assert not list(READBACK_PATH.parent.glob("yym4_bound_speaker*.ymmp"))
    assert not list(READBACK_PATH.parent.glob("yym4_bound_speaker*.mp4"))
    assert not list(READBACK_PATH.parent.glob("yym4_bound_speaker*.wav"))
    assert not list(READBACK_PATH.parent.glob("yym4_bound_speaker*.mp3"))
    assert not list(READBACK_PATH.parent.glob("yym4_bound_speaker*.m4a"))
