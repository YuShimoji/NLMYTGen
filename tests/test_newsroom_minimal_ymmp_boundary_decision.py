import csv
import json
import re
from pathlib import Path

from src.pipeline.newsroom_minimal_ymmp_boundary_decision import (
    DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_DOC_PATH,
    DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH,
    MINIMAL_YMMP_BOUNDARY_DECISION_ID,
    MINIMAL_YMMP_BOUNDARY_DECISION_SCHEMA_VERSION,
    RECOMMENDED_NEXT_SLICE,
    build_default_newsroom_minimal_ymmp_boundary_decision,
    render_newsroom_minimal_ymmp_boundary_decision_markdown,
)
from src.pipeline.newsroom_yym4_bound_speaker_import_readiness import (
    DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    DEFAULT_BOUND_SPEAKER_CSV_PATH,
    OBSERVED_MANUAL_CHARACTER,
)


ROOT = Path(__file__).resolve().parents[1]
DECISION_PATH = ROOT / DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH
DOC_PATH = ROOT / DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_DOC_PATH
READINESS_PATH = ROOT / DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH
BOUND_CSV_PATH = ROOT / DEFAULT_BOUND_SPEAKER_CSV_PATH


def _decision() -> dict:
    return json.loads(DECISION_PATH.read_text(encoding="utf-8"))


def _csv_rows() -> list[list[str]]:
    with BOUND_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_minimal_ymmp_boundary_decision_matches_builder_output() -> None:
    decision = _decision()

    assert decision == build_default_newsroom_minimal_ymmp_boundary_decision(
        root=ROOT
    )
    assert decision["artifact_id"] == MINIMAL_YMMP_BOUNDARY_DECISION_ID
    assert decision["decision_id"] == MINIMAL_YMMP_BOUNDARY_DECISION_ID
    assert (
        decision["schema_version"]
        == MINIMAL_YMMP_BOUNDARY_DECISION_SCHEMA_VERSION
    )
    assert decision["review_status"] == "ready_for_supervisor_review"
    assert decision["diagnostic_only"] is True
    assert decision["production_status"] == "diagnostic_only"
    assert decision["decision_status"] == "approved_for_next_probe_packet"
    assert decision["identity"]["source_bound_speaker_readiness_path"] == str(
        DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH
    ).replace("\\", "/")
    assert decision["identity"]["source_bound_csv_path"] == str(
        DEFAULT_BOUND_SPEAKER_CSV_PATH
    ).replace("\\", "/")


def test_accepted_inputs_and_source_validation_preserve_bound_speaker_evidence() -> None:
    decision = _decision()
    accepted = decision["accepted_inputs"]
    validation = decision["source_validation"]
    rows = _csv_rows()

    assert BOUND_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf")
    assert accepted["bound_CSV_accepted_in_current_environment"] is True
    assert accepted["speaker_value"] == OBSERVED_MANUAL_CHARACTER
    assert accepted["row_count"] == 4
    assert accepted["text_visible"] is True
    assert accepted["speaker_prompt_shown"] is False
    assert accepted["speaker_prompt_not_shown"] is True
    assert accepted["csv_encoding"] == "UTF-8 BOM"
    assert accepted["csv_header"] is False
    assert accepted["csv_columns"] == ["speaker", "text"]
    assert len(rows) == 4
    assert all(row[0] == OBSERVED_MANUAL_CHARACTER for row in rows)
    assert validation["source_readiness_result"] == "pass"
    assert validation["bound_csv_bom_verified"] is True
    assert validation["bound_csv_has_header"] is False
    assert validation["bound_csv_all_rows_two_columns"] is True
    assert validation["bound_csv_row_count"] == 4
    assert validation["all_rows_use_bound_speaker"] is True
    assert validation["all_rows_have_text"] is True
    assert validation["speaker_prompt_shown"] is False
    assert validation["timing_imported_from_csv"] is False
    assert validation["errors"] == []


def test_ymmp_boundary_forbids_current_artifact_creation_and_production_paths() -> None:
    decision = _decision()
    boundary = decision["ymmp_boundary"]
    assertions = decision["boundary_assertions"]
    not_accepted = decision["not_accepted_scope"]

    assert boundary["current_ymmp_status"] == "not_created"
    assert boundary["agent_may_create_ymmp_now"] is False
    assert boundary["user_manual_ymmp_probe_may_be_prepared_next"] is True
    assert boundary["production_ymmp_allowed"] is False
    assert boundary["render_allowed"] is False
    assert boundary["TTS_generation_allowed"] is False
    assert boundary["real_media_allowed"] is False
    assert boundary["real_newsroom_ingest_allowed"] is False
    assert boundary["external_fetch_allowed"] is False
    assert assertions["decision_only_no_probe_execution"] is True
    assert assertions["YMM4_launched_by_agent"] is False
    assert assertions["external_fetch_performed"] is False
    assert assertions["dashboard_governance_freshness_changed"] is False
    assert not_accepted["production_readiness"] is False
    assert not_accepted["render_readiness"] is False
    assert not_accepted["TTS_readiness"] is False
    assert not_accepted["public_video_readiness"] is False
    assert not_accepted["timing_import_from_neutral_timeline_metadata"] is False


def test_recommended_next_path_and_timing_gap_policy_are_narrow() -> None:
    decision = _decision()
    next_path = decision["recommended_next_path"]
    timing = decision["timing_gap_policy"]

    assert next_path["choice"] == "prepare_manual_diagnostic_ymmp_probe_packet"
    assert next_path["next_recommended_slice"] == RECOMMENDED_NEXT_SLICE
    assert "prepare, not execute" in next_path["reason"]
    assert [item["path"] for item in next_path["alternatives_considered"]] == [
        "timing_gap_strategy_first",
        "TTS_boundary_first",
        "defer_ymmp",
    ]
    assert timing["neutral_timeline_total_sec"] == 68
    assert timing["observed_yym4_import_approx_sec"] == 8.48
    assert timing["timing_imported_by_csv"] is False
    assert timing["options"] == [
        "accept YMM4 natural duration for first diagnostic .ymmp",
        "patch timing after import",
        "keep timing metadata external until render path",
    ]
    assert timing["recommended_default"] == (
        "accept YMM4 natural duration for first diagnostic .ymmp"
    )
    assert "save/readback boundary first" in timing["reason"]
    assert decision["next_recommended_slice"] == (
        "newsroom-diagnostic-ymmp-probe-packet-v1"
    )


def test_human_burden_hygiene_and_operator_card_stay_freeform() -> None:
    decision = _decision()
    hygiene = decision["human_burden_hygiene"]
    evidence = decision["evidence_policy"]
    operator_card = decision["operator_observation_card"]
    review = decision["review_memory"]

    assert hygiene == {
        "user_input": "freeform",
        "template_required": False,
        "schema_owner": "Agent",
        "max_required_points": 3,
        "screenshot_optional": True,
        "negative_confirmations_required_from_user": False,
        "fixed_form_result_template": False,
    }
    assert evidence["input_mode"] == "freeform"
    assert evidence["template_required"] is False
    assert evidence["schema_owner"] == "Agent"
    assert evidence["screenshot_optional"] is True
    assert len(evidence["sufficient_freeform_evidence"]) == 3
    assert operator_card["status"] == "for_next_probe_packet_only"
    assert operator_card["answer_style"] == "freeform"
    assert len(operator_card["look_for"]) == 3
    assert "fixed result form" in operator_card["not_needed"]
    assert review["prior_user_review_count"] == {
        "manual_import_behavior": 1,
        "bound_speaker_behavior": 1,
        "minimal_ymmp_boundary": 0,
    }
    assert review["repeated_general_review_allowed"] is False
    assert review["input_mode"] == "freeform"


def test_doc_matches_renderer_and_has_no_fixed_form_relapse() -> None:
    decision = _decision()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_minimal_ymmp_boundary_decision_markdown(
        decision
    )
    assert "decision_status: approved_for_next_probe_packet" in doc_text
    assert "agent_may_create_ymmp_now: false" in doc_text
    assert "answer_style: freeform" in doc_text
    assert "Review Card: none" in doc_text
    assert "result: pass / fail" not in doc_text
    assert "fixed result form" in doc_text
    assert "template_required: false" in doc_text


def test_minimal_ymmp_boundary_artifacts_have_no_real_urls_or_outputs() -> None:
    decision_text = DECISION_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    readiness_text = READINESS_PATH.read_text(encoding="utf-8")
    csv_text = BOUND_CSV_PATH.read_text(encoding="utf-8-sig")

    assert _real_url_pattern().search(decision_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert _real_url_pattern().search(readiness_text) is None
    assert _real_url_pattern().search(csv_text) is None
    assert not list(DECISION_PATH.parent.glob("minimal_ymmp_boundary*.ymmp"))
    assert not list(DECISION_PATH.parent.glob("minimal_ymmp_boundary*.mp4"))
    assert not list(DECISION_PATH.parent.glob("minimal_ymmp_boundary*.wav"))
    assert not list(DECISION_PATH.parent.glob("minimal_ymmp_boundary*.mp3"))
    assert not list(DECISION_PATH.parent.glob("minimal_ymmp_boundary*.m4a"))
