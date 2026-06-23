import json
import re
from pathlib import Path

from src.pipeline.newsroom_diagnostic_ymmp_manual_result import (
    DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_DOC_PATH,
    DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH,
    DIAGNOSTIC_YMMP_MANUAL_RESULT_ID,
    DIAGNOSTIC_YMMP_MANUAL_RESULT_SCHEMA_VERSION,
    LOCAL_DIAGNOSTIC_YMMP_PATH,
    build_default_newsroom_diagnostic_ymmp_manual_result,
    render_newsroom_diagnostic_ymmp_manual_result_markdown,
)
from src.pipeline.newsroom_diagnostic_ymmp_probe_packet import (
    DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_PATH,
)
from src.pipeline.newsroom_minimal_ymmp_boundary_decision import (
    DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    DEFAULT_BOUND_SPEAKER_CSV_PATH,
    OBSERVED_MANUAL_CHARACTER,
)


ROOT = Path(__file__).resolve().parents[1]
READBACK_PATH = ROOT / DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH
DOC_PATH = ROOT / DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_DOC_PATH


def _readback() -> dict:
    return json.loads(READBACK_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_diagnostic_ymmp_manual_result_matches_builder_output() -> None:
    readback = _readback()

    assert readback == build_default_newsroom_diagnostic_ymmp_manual_result(root=ROOT)
    assert readback["artifact_id"] == DIAGNOSTIC_YMMP_MANUAL_RESULT_ID
    assert readback["result_id"] == DIAGNOSTIC_YMMP_MANUAL_RESULT_ID
    assert readback["schema_version"] == DIAGNOSTIC_YMMP_MANUAL_RESULT_SCHEMA_VERSION
    assert readback["review_status"] == "ready_for_supervisor_review"
    assert readback["diagnostic_only"] is True
    assert readback["production_status"] == "diagnostic_only"
    assert readback["manual_probe_status"] == "observed"
    assert readback["result"] == "pass"


def test_identity_and_source_validation_link_to_probe_and_bound_csv() -> None:
    readback = _readback()
    identity = readback["identity"]
    validation = readback["source_validation"]

    assert identity["source_probe_packet_path"] == str(
        DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_PATH
    ).replace("\\", "/")
    assert identity["source_boundary_decision_path"] == str(
        DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH
    ).replace("\\", "/")
    assert identity["source_bound_csv_path"] == str(
        DEFAULT_BOUND_SPEAKER_CSV_PATH
    ).replace("\\", "/")
    assert identity["production_status"] == "diagnostic_only"
    assert identity["manual_probe_status"] == "observed"
    assert identity["observation_source"] == (
        "user_freeform_and_supervisor_screenshot"
    )
    assert validation["source_probe_packet_manual_probe_status"] == "not_run"
    assert validation["source_boundary_decision_status"] == (
        "approved_for_next_probe_packet"
    )
    assert validation["bound_csv_bom_verified"] is True
    assert validation["bound_csv_has_header"] is False
    assert validation["bound_csv_all_rows_two_columns"] is True
    assert validation["bound_csv_row_count"] == 4
    assert validation["all_rows_use_bound_speaker"] is True
    assert validation["all_rows_have_text"] is True
    assert validation["errors"] == []


def test_normalized_result_preserves_manual_observation_without_production_claim() -> None:
    readback = _readback()
    result = readback["normalized_result"]
    discovery = readback["local_ymmp_discovery"]

    assert result == {
        "result": "pass",
        "diagnostic_ymmp_saved_or_save_attempt_observed": True,
        "local_ymmp_path": str(LOCAL_DIAGNOSTIC_YMMP_PATH).replace("\\", "/"),
        "ymmp_committed": False,
        "observed_line_count": 4,
        "all_text_visible": True,
        "speaker_preserved": True,
        "speaker_value_ui_observed": OBSERVED_MANUAL_CHARACTER,
        "raw_speaker_value_if_detected": "unknown",
        "encoding_note": (
            "Use the UI-observed speaker value as canonical; terminal mojibake or "
            "raw parse ambiguity is not treated as the accepted speaker value."
        ),
        "timing_observation": "short_natural_duration",
        "render_created": False,
        "explicit_tts_generation_by_operator": False,
        "real_media_imported": False,
        "production_approval": False,
    }
    assert discovery["local_ymmp_path"] == str(LOCAL_DIAGNOSTIC_YMMP_PATH).replace(
        "\\", "/"
    )
    assert discovery["path_status"] == "discoverable_local_file_at_readback_time"
    assert discovery["exists_at_readback_time"] is True
    assert discovery["file_inspected"] is False
    assert discovery["ymmp_structure_parsed"] is False
    assert discovery["ymmp_committed"] is False
    assert discovery["commit_policy"] == "do_not_stage_or_commit_in_this_slice"


def test_scope_timing_review_and_human_burden_are_bounded() -> None:
    readback = _readback()

    assert readback["accepted_scope"] == {
        "diagnostic_ymmp_probe_observed": True,
        "dialogue_rows_preserved": True,
        "speaker_binding_preserved": True,
        "short_natural_duration_observed": True,
    }
    assert readback["not_accepted_scope"] == {
        "production_ymmp_ready": False,
        "ymmp_structure_parsed": False,
        "timing_patch_ready": False,
        "TTS_ready": False,
        "render_ready": False,
        "public_video_ready": False,
    }
    assert readback["timing_gap_carry_forward"] == {
        "neutral_timeline_total_sec": 68,
        "observed_yym4_duration": "short_natural_duration",
        "prior_observed_yym4_import_approx_sec": 8.48,
        "timing_gap_status": "unresolved",
        "timing_patch_ready": False,
        "recommended_next_axis": [
            "ymmp_structure_readback",
            "timing_gap_strategy",
        ],
    }
    assert readback["review_memory"]["prior_user_review_count"] == {
        "manual_import_behavior": 1,
        "bound_speaker_behavior": 1,
        "diagnostic_ymmp_manual_observation": 1,
    }
    assert readback["review_memory"]["repeated_general_review_allowed"] is False
    assert readback["human_burden_hygiene"] == {
        "user_input": "freeform",
        "template_required": False,
        "schema_owner": "Agent",
        "max_required_points": 0,
        "screenshot_optional": True,
        "negative_confirmations_required_from_user": False,
        "fixed_form_result_template": False,
        "user_side_work_this_slice": "none",
    }
    assert readback["next_recommended_slices"] == [
        "newsroom-ymmp-structure-readback-v1",
        "newsroom-yym4-timing-gap-strategy-v1",
        "newsroom-audio-tts-boundary-v1",
    ]


def test_boundary_assertions_keep_agent_and_output_actions_closed() -> None:
    readback = _readback()
    boundary = readback["boundary_assertions"]
    review_debt = readback["review_debt"]

    assert boundary["agent_launched_yym4"] is False
    assert boundary["agent_created_or_edited_ymmp"] is False
    assert boundary["ymmp_committed"] is False
    assert boundary["ymmp_structure_parsed"] is False
    assert boundary["render_created"] is False
    assert boundary["TTS_generated"] is False
    assert boundary["real_media_imported"] is False
    assert boundary["production_approval"] is False
    assert boundary["public_video_ready"] is False
    assert boundary["external_fetch_performed"] is False
    assert boundary["dashboard_governance_freshness_changed"] is False
    assert review_debt["generic_review_card_emitted"] is False


def test_doc_matches_renderer_and_has_no_fixed_form_relapse() -> None:
    readback = _readback()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_diagnostic_ymmp_manual_result_markdown(readback)
    assert "manual_probe_status: observed" in doc_text
    assert "result: pass" in doc_text
    assert "template_required: false" in doc_text
    assert "user_side_work_this_slice: none" in doc_text
    assert "generic_review_card_emitted: false" in doc_text
    assert "result: pass / fail" not in doc_text
    assert "yes/no/unclear" not in doc_text.lower()


def test_diagnostic_ymmp_manual_result_artifacts_have_no_real_urls_or_outputs() -> None:
    readback_text = READBACK_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(readback_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(READBACK_PATH.parent.glob("*manual_result_readback*.ymmp"))
    assert not list(READBACK_PATH.parent.glob("*manual_result_readback*.mp4"))
    assert not list(READBACK_PATH.parent.glob("*manual_result_readback*.wav"))
    assert not list(READBACK_PATH.parent.glob("*manual_result_readback*.mp3"))
    assert not list(READBACK_PATH.parent.glob("*manual_result_readback*.m4a"))
