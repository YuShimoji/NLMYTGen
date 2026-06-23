import csv
import json
import re
from pathlib import Path

from src.pipeline.newsroom_diagnostic_ymmp_probe_packet import (
    DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_DOC_PATH,
    DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_PATH,
    DIAGNOSTIC_YMMP_PROBE_PACKET_ID,
    DIAGNOSTIC_YMMP_PROBE_PACKET_SCHEMA_VERSION,
    RECOMMENDED_MANUAL_SAVE_PATH,
    build_default_newsroom_diagnostic_ymmp_probe_packet,
    render_newsroom_diagnostic_ymmp_probe_packet_markdown,
)
from src.pipeline.newsroom_minimal_ymmp_boundary_decision import (
    DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH,
)
from src.pipeline.newsroom_yym4_bound_speaker_import_readiness import (
    DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    DEFAULT_BOUND_SPEAKER_CSV_PATH,
    OBSERVED_MANUAL_CHARACTER,
)


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_PATH
DOC_PATH = ROOT / DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_DOC_PATH
BOUNDARY_PATH = ROOT / DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH
READINESS_PATH = ROOT / DEFAULT_BOUND_SPEAKER_IMPORT_READINESS_PATH
BOUND_CSV_PATH = ROOT / DEFAULT_BOUND_SPEAKER_CSV_PATH


def _packet() -> dict:
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


def _csv_rows() -> list[list[str]]:
    with BOUND_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_diagnostic_ymmp_probe_packet_matches_builder_output() -> None:
    packet = _packet()

    assert packet == build_default_newsroom_diagnostic_ymmp_probe_packet(root=ROOT)
    assert packet["artifact_id"] == DIAGNOSTIC_YMMP_PROBE_PACKET_ID
    assert packet["packet_id"] == DIAGNOSTIC_YMMP_PROBE_PACKET_ID
    assert packet["schema_version"] == DIAGNOSTIC_YMMP_PROBE_PACKET_SCHEMA_VERSION
    assert packet["review_status"] == "ready_for_future_manual_probe"
    assert packet["diagnostic_only"] is True
    assert packet["production_status"] == "diagnostic_only"
    assert packet["manual_probe_status"] == "not_run"
    assert packet["identity"]["source_boundary_decision_path"] == str(
        DEFAULT_MINIMAL_YMMP_BOUNDARY_DECISION_PATH
    ).replace("\\", "/")
    assert packet["identity"]["source_bound_csv_path"] == str(
        DEFAULT_BOUND_SPEAKER_CSV_PATH
    ).replace("\\", "/")


def test_target_and_source_validation_are_bound_csv_backed() -> None:
    packet = _packet()
    target = packet["target"]
    validation = packet["source_validation"]
    rows = _csv_rows()

    assert BOUND_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf")
    assert target["target_csv"] == str(DEFAULT_BOUND_SPEAKER_CSV_PATH).replace(
        "\\", "/"
    )
    assert target["intended_YMM4_environment"] == "manual/operator-run only"
    assert target["expected_row_count"] == 4
    assert target["observed_row_count_before_probe"] == 4
    assert target["speaker_value"] == OBSERVED_MANUAL_CHARACTER
    assert target["encoding"] == "UTF-8 BOM"
    assert target["bom_verified"] is True
    assert target["header"] is False
    assert target["has_header"] is False
    assert target["columns"] == ["speaker", "text"]
    assert len(rows) == 4
    assert all(row[0] == OBSERVED_MANUAL_CHARACTER for row in rows)
    assert all(len(row) == 2 for row in rows)
    assert validation["source_boundary_decision_status"] == (
        "approved_for_next_probe_packet"
    )
    assert validation["source_readiness_result"] == "pass"
    assert validation["bound_csv_bom_verified"] is True
    assert validation["bound_csv_has_header"] is False
    assert validation["bound_csv_all_rows_two_columns"] is True
    assert validation["bound_csv_row_count"] == 4
    assert validation["all_rows_use_bound_speaker"] is True
    assert validation["all_rows_have_text"] is True
    assert validation["errors"] == []


def test_expected_starting_point_allowed_and_forbidden_actions_are_bounded() -> None:
    packet = _packet()
    starting = packet["expected_starting_point"]
    allowed = packet["allowed_future_manual_action"]
    forbidden = packet["forbidden_actions"]
    boundary = packet["boundary_assertions"]

    assert starting == {
        "import_bound_speaker_csv": True,
        "confirm_4_rows_and_speaker": True,
        "save_minimal_diagnostic_ymmp_only_if_operator_comfortable": True,
        "do_not_render": True,
        "do_not_generate_TTS": True,
        "do_not_import_real_media": True,
        "timing_patch_in_this_probe": False,
    }
    assert allowed["manual_YMM4_launch_by_user_operator"] is True
    assert allowed["manual_diagnostic_ymmp_save"] is True
    assert allowed["recommended_save_location"] == str(
        RECOMMENDED_MANUAL_SAVE_PATH
    ).replace("\\", "/")
    assert allowed["recommended_save_location_created_by_agent"] is False
    assert allowed["committing_ymmp_allowed_now"] is False
    assert forbidden == {
        "Agent_YMM4_launch": False,
        "Agent_ymmp_creation": False,
        "render": False,
        "TTS_generation": False,
        "real_media_import": False,
        "production_approval": False,
        "public_video_claim": False,
        "external_fetch": False,
        "real_newsroom_ingest": False,
    }
    assert boundary["manual_probe_status"] == "not_run"
    assert boundary["agent_launched_yym4"] is False
    assert boundary["agent_created_or_edited_ymmp"] is False
    assert boundary["ymmp_created"] is False
    assert boundary["render_created"] is False
    assert boundary["TTS_generated"] is False
    assert boundary["real_media_imported"] is False


def test_operator_card_and_agent_normalization_keep_user_input_freeform() -> None:
    packet = _packet()
    card = packet["operator_observation_card"]
    normalization = packet["agent_normalization_plan"]
    hygiene = packet["human_burden_hygiene"]
    review = packet["review_memory"]

    assert card["status"] == "required_later"
    assert card["target"] == "diagnostic .ymmp probe from bound speaker CSV"
    assert "save the imported 4-line script" in card["why"]
    assert "only if comfortable" in card["action"]
    assert card["look_for"] == [
        "4 dialogue rows remain after save/reopen or save observation",
        f"speaker remains {OBSERVED_MANUAL_CHARACTER}",
        "timing stays natural short duration or changes unexpectedly",
    ]
    assert len(card["look_for"]) == 3
    assert card["answer_style"] == "freeform"
    assert "One sentence is enough" in card["answer_hint"]
    assert "fixed form" in card["not_needed"]
    assert normalization["schema_owner"] == "Agent"
    assert normalization["exposed_as_user_form"] is False
    assert normalization["fields"] == [
        "result",
        "ymmp_saved",
        "row_count_observed",
        "speaker_preserved",
        "timing_observation",
        "render_created",
        "TTS_generated",
        "media_imported",
        "confidence",
        "unknowns",
    ]
    assert hygiene == {
        "user_input": "freeform",
        "template_required": False,
        "schema_owner": "Agent",
        "max_required_points": 3,
        "screenshot_optional": True,
        "negative_confirmations_required_from_user": False,
        "fixed_form_result_template": False,
    }
    assert review["prior_user_review_count"] == {
        "manual_import_behavior": 1,
        "bound_speaker_behavior": 1,
        "minimal_ymmp_boundary": 0,
        "diagnostic_ymmp_probe_packet": 0,
    }
    assert review["repeated_general_review_allowed"] is False
    assert review["input_mode"] == "freeform"


def test_timing_policy_next_slices_and_not_accepted_scope_are_recorded() -> None:
    packet = _packet()
    timing = packet["timing_policy"]
    not_accepted = packet["not_accepted_scope"]

    assert timing["neutral_timeline_total_sec"] == 68
    assert timing["observed_yym4_import_approx_sec"] == 8.48
    assert timing["first_probe_expected_timing"] == "YMM4 natural duration"
    assert timing["timing_patch_in_this_probe"] is False
    assert timing["next_timing_axis"] == [
        "timing_gap_strategy",
        "optional ymmp_patch_strategy after project structure is known",
    ]
    assert packet["next_recommended_slices"] == [
        "newsroom-diagnostic-ymmp-manual-result-readback-v1",
        "newsroom-yym4-timing-gap-strategy-v1",
        "newsroom-ymmp-structure-readback-v1",
    ]
    assert not_accepted == {
        "production_readiness": False,
        "render_readiness": False,
        "TTS_readiness": False,
        "public_video_readiness": False,
        "visual_layout_import": False,
        "portability_across_all_YMM4_installations": False,
        "timing_import_from_neutral_timeline_metadata": False,
        "committed_ymmp_artifact": False,
    }


def test_doc_matches_renderer_and_has_no_fixed_form_relapse() -> None:
    packet = _packet()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_diagnostic_ymmp_probe_packet_markdown(packet)
    assert "manual_probe_status: not_run" in doc_text
    assert "answer_style: freeform" in doc_text
    assert "template_required: false" in doc_text
    assert "Review Card: none" in doc_text
    assert "result: pass / fail" not in doc_text
    assert "yes/no/unclear" not in doc_text.lower()


def test_diagnostic_ymmp_probe_packet_artifacts_have_no_real_urls_or_outputs() -> None:
    packet_text = PACKET_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    boundary_text = BOUNDARY_PATH.read_text(encoding="utf-8")
    readiness_text = READINESS_PATH.read_text(encoding="utf-8")
    csv_text = BOUND_CSV_PATH.read_text(encoding="utf-8-sig")

    assert _real_url_pattern().search(packet_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert _real_url_pattern().search(boundary_text) is None
    assert _real_url_pattern().search(readiness_text) is None
    assert _real_url_pattern().search(csv_text) is None
    assert not list(PACKET_PATH.parent.glob("diagnostic_ymmp_probe*.ymmp"))
    assert not list(PACKET_PATH.parent.glob("diagnostic_ymmp_probe*.mp4"))
    assert not list(PACKET_PATH.parent.glob("diagnostic_ymmp_probe*.wav"))
    assert not list(PACKET_PATH.parent.glob("diagnostic_ymmp_probe*.mp3"))
    assert not list(PACKET_PATH.parent.glob("diagnostic_ymmp_probe*.m4a"))
