import json
import re
from pathlib import Path

from src.pipeline.newsroom_yym4_manual_import_result import (
    DEFAULT_MANUAL_IMPORT_RESULT_DOC_PATH,
    DEFAULT_MANUAL_IMPORT_RESULT_PATH,
    MANUAL_IMPORT_RESULT_ID,
    MANUAL_IMPORT_RESULT_SCHEMA_VERSION,
    OPERATOR_MANUAL_IMPORT_RESULT_V1,
    build_default_newsroom_yym4_manual_import_result,
    render_newsroom_yym4_manual_import_result_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / DEFAULT_MANUAL_IMPORT_RESULT_PATH
DOC_PATH = ROOT / DEFAULT_MANUAL_IMPORT_RESULT_DOC_PATH


def _result() -> dict:
    return json.loads(RESULT_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_manual_import_result_matches_builder_output() -> None:
    result = _result()

    assert result == build_default_newsroom_yym4_manual_import_result(root=ROOT)
    assert result["artifact_id"] == MANUAL_IMPORT_RESULT_ID
    assert result["result_id"] == MANUAL_IMPORT_RESULT_ID
    assert result["schema_version"] == MANUAL_IMPORT_RESULT_SCHEMA_VERSION
    assert result["review_status"] == "ready_for_supervisor_review"
    assert result["diagnostic_only"] is True
    assert result["production_status"] == "diagnostic_only"
    assert result["manual_check_status"] == "observed"
    assert result["result"] == "pass_with_warnings"


def test_manual_import_result_preserves_operator_observation() -> None:
    result = _result()
    operator_result = result["operator_result"]
    observation = result["observation"]

    for key, value in OPERATOR_MANUAL_IMPORT_RESULT_V1.items():
        assert operator_result[key] == value
    assert operator_result["normalized_result"] == "pass_with_warnings"
    assert observation["observed_line_count"] == 4
    assert observation["expected_line_count"] == 4
    assert observation["all_text_visible"] is True
    assert observation["speaker_behavior"] == "mapped_after_manual_selection"
    assert observation["selected_speaker_or_character"] == "ゆっくり霊夢"
    assert observation["encoding_or_text_issues"] is False
    assert observation["header_or_column_issues"] is False
    assert observation["error_message"] is None
    assert observation["screenshot_reference"] == "provided_in_supervisor_thread"
    assert operator_result["did_not_generate_tts"] == (
        "operator_did_not_explicitly_generate_tts"
    )


def test_manual_import_result_classifies_warning_only_pass() -> None:
    result = _result()
    classification = result["result_classification"]
    warning_classification = result["warning_classification"]
    readiness = result["readiness_delta"]

    assert classification["result"] == "pass_with_warnings"
    assert classification["line_count_matches"] is True
    assert classification["text_import_passed"] is True
    assert classification["speaker_required_manual_selection"] is True
    assert classification["selected_speaker_or_character"] == "ゆっくり霊夢"
    assert classification["primary_warning_id"] == "manual_speaker_binding_required"
    assert warning_classification[0] == {
        "warning_id": "manual_speaker_binding_required",
        "severity": "medium",
        "meaning": (
            "YMM4 accepted rows/text but required manual binding to an existing "
            "character."
        ),
        "next_axis": "speaker_binding_policy",
    }
    assert classification["blocking_failures"] == []
    assert readiness["manual_check_before"] == "not_run"
    assert readiness["manual_check_after"] == "observed_pass_with_warnings"
    assert readiness["tiny_csv_text_import_observed"] is True
    assert readiness["speaker_mapping_observed_after_manual_selection"] is True
    assert readiness["automatic_speaker_binding_observed"] is False
    assert readiness["explicit_tts_generation_by_operator"] is False
    assert readiness["transfer_status"] == "blocked"
    assert readiness["public_video_ready"] is False


def test_manual_import_result_keeps_review_memory_nonredundant() -> None:
    result = _result()
    review = result["review_memory"]
    accepted = result["accepted_scope"]
    not_accepted = result["not_accepted_scope"]

    assert review["prior_user_review_count"] == 1
    assert review["repeated_general_review_allowed"] is False
    assert review["next_nonredundant_axis"] == [
        "speaker_binding_policy",
        "YMM4_import_readiness_after_manual_result",
        "minimal_ymmp_boundary_decision",
    ]
    assert accepted == {
        "tiny_csv_shape_observed_in_YMM4": True,
        "row_text_import_observed": True,
        "manual_speaker_binding_observed": True,
    }
    assert not_accepted["automatic_speaker_binding"] is False
    assert not_accepted["TTS_ready"] is False
    assert not_accepted["render_ready"] is False
    assert not_accepted["production_ready"] is False
    assert not_accepted["YMM4_project_ready"] is False


def test_manual_import_result_keeps_diagnostic_boundaries_closed() -> None:
    result = _result()
    safety = result["safety"]
    boundary = result["boundary_assertions"]

    assert safety["render_created"] is False
    assert safety["explicit_tts_generation_by_operator"] is False
    assert safety["did_not_generate_tts_interpretation"] == (
        "operator_did_not_explicitly_generate_tts"
    )
    assert safety["real_media_imported"] is False
    assert safety["ymmp_committed"] is False
    assert safety["production_approval"] is False
    assert safety["public_video_ready"] is False
    assert boundary["agent_launched_yym4"] is False
    assert boundary["agent_created_or_edited_ymmp"] is False
    assert boundary["agent_rendered_media"] is False
    assert boundary["agent_generated_tts"] is False
    assert boundary["dashboard_governance_freshness_changed"] is False
    assert boundary["external_fetch_performed"] is False


def test_manual_import_result_doc_matches_renderer_and_mentions_boundaries() -> None:
    result = _result()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_yym4_manual_import_result_markdown(result)
    assert "manual_check_status: observed" in doc_text
    assert "result: pass_with_warnings" in doc_text
    assert "warning_id: manual_speaker_binding_required" in doc_text
    assert "speaker_required_manual_selection: true" in doc_text
    assert "transfer_status: blocked" in doc_text
    assert "production readiness" in doc_text
    assert "YMM4 transfer approval" in doc_text


def test_manual_import_result_artifacts_have_no_real_urls_or_outputs() -> None:
    result_text = RESULT_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(result_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(RESULT_PATH.parent.glob("*manual_import_result*.ymmp"))
    assert not list(RESULT_PATH.parent.glob("*manual_import_result*.mp4"))
    assert not list(RESULT_PATH.parent.glob("*manual_import_result*.wav"))
    assert not list(RESULT_PATH.parent.glob("*manual_import_result*.mp3"))
    assert not list(RESULT_PATH.parent.glob("*manual_import_result*.m4a"))
