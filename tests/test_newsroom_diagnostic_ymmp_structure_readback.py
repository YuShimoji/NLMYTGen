import json
import re
from pathlib import Path

from src.pipeline.newsroom_diagnostic_ymmp_manual_result import (
    DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH,
    LOCAL_DIAGNOSTIC_YMMP_PATH,
)
from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_DOC_PATH,
    DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH,
    DIAGNOSTIC_YMMP_STRUCTURE_READBACK_ID,
    DIAGNOSTIC_YMMP_STRUCTURE_READBACK_SCHEMA_VERSION,
    build_default_newsroom_diagnostic_ymmp_structure_readback,
    parse_diagnostic_ymmp_structure,
    render_newsroom_diagnostic_ymmp_structure_readback_markdown,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    OBSERVED_MANUAL_CHARACTER,
)


ROOT = Path(__file__).resolve().parents[1]
READBACK_PATH = ROOT / DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
DOC_PATH = ROOT / DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_DOC_PATH
SOURCE_YMMP_PATH = ROOT / LOCAL_DIAGNOSTIC_YMMP_PATH


def _readback() -> dict:
    return json.loads(READBACK_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_structure_readback_matches_builder_output() -> None:
    readback = _readback()

    assert readback == build_default_newsroom_diagnostic_ymmp_structure_readback(
        root=ROOT
    )
    assert readback["artifact_id"] == DIAGNOSTIC_YMMP_STRUCTURE_READBACK_ID
    assert readback["readback_id"] == DIAGNOSTIC_YMMP_STRUCTURE_READBACK_ID
    assert readback["schema_version"] == (
        DIAGNOSTIC_YMMP_STRUCTURE_READBACK_SCHEMA_VERSION
    )
    assert readback["review_status"] == "ready_for_supervisor_review"
    assert readback["diagnostic_only"] is True
    assert readback["production_status"] == "diagnostic_only"
    assert readback["ymmp_committed"] is False


def test_identity_parse_status_and_source_ymmp_are_bounded() -> None:
    readback = _readback()
    identity = readback["identity"]
    parse_status = readback["parse_status"]

    assert SOURCE_YMMP_PATH.exists()
    assert identity["source_ymmp_path"] == str(LOCAL_DIAGNOSTIC_YMMP_PATH).replace(
        "\\", "/"
    )
    assert identity["source_manual_result_readback_path"] == str(
        DEFAULT_DIAGNOSTIC_YMMP_MANUAL_RESULT_PATH
    ).replace("\\", "/")
    assert identity["production_status"] == "diagnostic_only"
    assert identity["ymmp_committed"] is False
    assert parse_status == {
        "ymmp_found": True,
        "parse_status": "parsed",
        "parse_method": "python json utf-8-sig bounded structure read",
        "warnings": [],
    }


def test_parser_extracts_four_dialogue_items_without_voice_cache_payload() -> None:
    parsed = parse_diagnostic_ymmp_structure(SOURCE_YMMP_PATH)
    timeline = parsed["timeline"]
    items = parsed["items"]

    assert timeline["length_frames"] == 509
    assert timeline["fps"] == 60
    assert timeline["duration_sec"] == round(509 / 60, 6)
    assert timeline["item_count"] == 4
    assert [item["frame"] for item in items] == [0, 130, 255, 369]
    assert [item["length_frames"] for item in items] == [130, 125, 114, 140]
    assert [item["text"] for item in items] == [
        "Fake topic, review only.",
        "Review-only handoff stays.",
        "A fake claim is shown.",
        "Fake source checks are noted.",
    ]
    assert all(item["voice_cache_present"] is True for item in items)
    assert all(item["voice_cache_char_count"] > 0 for item in items)
    assert "VoiceCache" not in json.dumps(parsed, ensure_ascii=False)


def test_dialogue_timing_and_audio_boundaries_are_recorded() -> None:
    readback = _readback()
    dialogue = readback["dialogue_structure"]
    timing = readback["timing_structure"]
    audio = readback["audio_tts_structure"]

    assert dialogue["dialogue_item_count"] == 4
    assert dialogue["expected_dialogue_item_count"] == 4
    assert dialogue["canonical_speaker_value"] == OBSERVED_MANUAL_CHARACTER
    assert dialogue["text_fields"] == ["Serif"]
    assert dialogue["speaker_character_fields"] == ["CharacterName"]
    assert len(dialogue["raw_speaker_values"]) == 1
    assert len(dialogue["items"]) == 4
    assert timing["observed_project_duration_sec"] == round(509 / 60, 6)
    assert timing["observed_project_duration_frames"] == 509
    assert timing["neutral_timeline_total_sec"] == 68
    assert timing["prior_observed_yym4_import_approx_sec"] == 8.48
    assert timing["timing_gap_status"] == "unresolved"
    assert timing["ymmp_natural_duration_observed"] == "short_natural_duration"
    assert timing["timing_patch_applied"] is False
    assert audio["voice_item_count"] == 4
    assert audio["voice_cache_item_count"] == 4
    assert audio["audio_effect_total_count"] == 0
    assert audio["TTS_generated_by_agent"] is False
    assert audio["explicit_operator_TTS_generation"] is False
    assert audio["TTS_ready"] is False


def test_scope_review_and_human_burden_remain_nonredundant() -> None:
    readback = _readback()

    assert readback["accepted_scope"] == {
        "ymmp_structure_parsed_for_diagnostic_readback": True,
        "dialogue_rows_found": True,
        "speaker_raw_fields_recorded": True,
        "short_natural_timing_fields_recorded": True,
    }
    assert readback["not_accepted_scope"] == {
        "production_ymmp_ready": False,
        "render_readiness": False,
        "TTS_readiness": False,
        "timing_patch_strategy": False,
        "public_video_readiness": False,
    }
    assert readback["review_memory"]["prior_user_review_count"] == {
        "manual_import_behavior": 1,
        "bound_speaker_behavior": 1,
        "diagnostic_ymmp_manual_observation": 1,
        "ymmp_structure_readback": 0,
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
    assert readback["next_recommended_axes"] == [
        "newsroom-yym4-timing-gap-strategy-v1",
        "newsroom-audio-tts-boundary-v1",
        "newsroom-tiny-render-smoke-boundary-v1",
    ]


def test_boundary_keeps_ymmp_and_output_actions_closed() -> None:
    readback = _readback()
    boundary = readback["boundary"]

    assert boundary == {
        "render_created": False,
        "real_media_imported": False,
        "production_approval": False,
        "public_video_ready": False,
        "ymmp_staged_or_committed": False,
        "agent_launched_yym4": False,
        "agent_created_or_edited_ymmp": False,
        "TTS_generated_by_agent": False,
        "external_fetch_performed": False,
    }
    assert readback["review_debt"]["generic_review_card_emitted"] is False


def test_doc_matches_renderer_and_has_no_fixed_form_relapse() -> None:
    readback = _readback()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_diagnostic_ymmp_structure_readback_markdown(
        readback
    )
    assert "ymmp_committed: false" in doc_text
    assert "dialogue_item_count: 4" in doc_text
    assert "timing_gap_status: unresolved" in doc_text
    assert "TTS_ready: false" in doc_text
    assert "user_side_work_this_slice: none" in doc_text
    assert "result: pass / fail" not in doc_text
    assert "yes/no/unclear" not in doc_text.lower()


def test_structure_readback_artifacts_have_no_real_urls_or_outputs() -> None:
    readback_text = READBACK_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(readback_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(READBACK_PATH.parent.glob("*structure_readback*.ymmp"))
    assert not list(READBACK_PATH.parent.glob("*structure_readback*.mp4"))
    assert not list(READBACK_PATH.parent.glob("*structure_readback*.wav"))
    assert not list(READBACK_PATH.parent.glob("*structure_readback*.mp3"))
    assert not list(READBACK_PATH.parent.glob("*structure_readback*.m4a"))
