import json
import re
from pathlib import Path

from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
    DISALLOWED_CANONICAL_SPEAKER_MOJIBAKE,
)
from src.pipeline.newsroom_yym4_timing_gap_strategy import (
    AFTER_TINY_RENDER_SMOKE_SLICE,
    DEFAULT_YYM4_TIMING_GAP_STRATEGY_DOC_PATH,
    DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH,
    NEXT_RECOMMENDED_SLICE,
    RECOMMENDED_DEFAULT,
    YYM4_TIMING_GAP_STRATEGY_ID,
    YYM4_TIMING_GAP_STRATEGY_SCHEMA_VERSION,
    build_default_newsroom_yym4_timing_gap_strategy,
    render_newsroom_yym4_timing_gap_strategy_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
STRATEGY_PATH = ROOT / DEFAULT_YYM4_TIMING_GAP_STRATEGY_PATH
DOC_PATH = ROOT / DEFAULT_YYM4_TIMING_GAP_STRATEGY_DOC_PATH


def _strategy() -> dict:
    return json.loads(STRATEGY_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_timing_gap_strategy_matches_builder_output() -> None:
    strategy = _strategy()

    assert strategy == build_default_newsroom_yym4_timing_gap_strategy(root=ROOT)
    assert strategy["artifact_id"] == YYM4_TIMING_GAP_STRATEGY_ID
    assert strategy["strategy_id"] == YYM4_TIMING_GAP_STRATEGY_ID
    assert strategy["schema_version"] == YYM4_TIMING_GAP_STRATEGY_SCHEMA_VERSION
    assert strategy["review_status"] == "ready_for_supervisor_review"
    assert strategy["diagnostic_only"] is True
    assert strategy["production_status"] == "diagnostic_only"
    assert strategy["strategy_status"] == "accepted_for_next_tiny_render_smoke"


def test_source_validation_preserves_structure_and_canonical_speaker() -> None:
    strategy = _strategy()
    validation = strategy["source_validation"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["parse_status"] == "parsed"
    assert validation["manual_result"] == "pass"
    assert validation["dialogue_item_count"] == 4
    assert validation["canonical_speaker_value"] == CANONICAL_UI_OBSERVED_SPEAKER
    assert validation["canonical_speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )
    assert validation["canonical_speaker_value"] != (
        DISALLOWED_CANONICAL_SPEAKER_MOJIBAKE
    )
    assert validation["accepted_speaker_value_must_not_equal_mojibake"] is True
    assert validation["timing_gap_status"] == "unresolved"


def test_timing_facts_extract_gap_without_patching() -> None:
    strategy = _strategy()
    facts = strategy["timing_facts"]

    assert facts["neutral_timeline_total_sec"] == 68
    assert facts["ymmp_fps"] == 60
    assert facts["ymmp_total_frames"] == 509
    assert facts["ymmp_total_duration_sec"] == round(509 / 60, 6)
    assert facts["item_frames"] == [0, 130, 255, 369]
    assert facts["item_lengths"] == [130, 125, 114, 140]
    assert facts["timing_gap_sec"] == round(68 - round(509 / 60, 6), 6)
    assert facts["timing_imported_by_csv"] is False
    assert facts["timing_patch_applied"] is False
    assert facts["source_timing_gap_status"] == "unresolved"
    assert facts["ymmp_natural_duration_observed"] == "short_natural_duration"


def test_strategy_options_choose_hybrid_as_default() -> None:
    strategy = _strategy()
    options = strategy["strategy_options"]
    recommended = strategy["recommended_default"]
    next_path = strategy["next_path"]

    assert [option["option_id"] for option in options] == [
        "accept_yym4_natural_duration_for_first_smoke",
        "patch_ymmp_to_neutral_68s_before_render",
        RECOMMENDED_DEFAULT,
        "keep_timing_external_until_render_path",
    ]
    assert recommended["choice"] == RECOMMENDED_DEFAULT
    assert recommended["next_recommended_slice"] == NEXT_RECOMMENDED_SLICE
    assert recommended["after_that"] == AFTER_TINY_RENDER_SMOKE_SLICE
    assert "first tiny render smoke" in recommended["reasoning"][0]
    assert next_path["if_hybrid_chosen"] == {
        "next_recommended_slice": NEXT_RECOMMENDED_SLICE,
        "after_that": AFTER_TINY_RENDER_SMOKE_SLICE,
    }
    assert next_path["if_timing_patch_first_chosen"] == {
        "next_recommended_slice": "newsroom-ymmp-timing-patch-planning-v1",
    }
    assert next_path["if_blocked"]["missing_evidence"] == []
    assert any(
        option["decision_role"] == "recommended_default"
        and NEXT_RECOMMENDED_SLICE in option["what_it_enables"]
        for option in options
    )


def test_boundaries_and_not_accepted_scope_stay_closed() -> None:
    strategy = _strategy()
    boundary = strategy["boundary"]
    not_accepted = strategy["not_accepted_scope"]

    assert boundary == {
        "ymmp_patched_in_this_slice": False,
        "ymmp_created_in_this_slice": False,
        "ymmp_staged_or_committed": False,
        "ymmp_committed": False,
        "agent_launched_yym4": False,
        "render_created": False,
        "TTS_generated": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "real_newsroom_ingest_performed": False,
        "dashboard_governance_freshness_changed": False,
        "production_approval": False,
        "public_video_ready": False,
    }
    assert not_accepted == {
        "production_ymmp": False,
        "timing_patch": False,
        "render_readiness": False,
        "TTS_readiness": False,
        "public_video_readiness": False,
        "visual_layout_import": False,
        "production_approval": False,
    }


def test_human_burden_and_review_memory_do_not_request_more_manual_work() -> None:
    strategy = _strategy()
    hygiene = strategy["human_burden_hygiene"]
    review = strategy["review_memory"]

    assert hygiene == {
        "user_input": "freeform",
        "template_required": False,
        "schema_owner": "Agent",
        "max_required_points": 0,
        "screenshot_optional": True,
        "negative_confirmations_required_from_user": False,
        "fixed_form_result_template": False,
        "operator_observation_card": "none",
        "user_side_work_this_slice": "none",
    }
    assert review["prior_user_review_count"] == {
        "manual_import_behavior": 1,
        "bound_speaker_behavior": 1,
        "diagnostic_ymmp_manual_observation": 1,
        "ymmp_structure_readback": 1,
        "timing_gap_strategy": 0,
    }
    assert review["repeated_general_review_allowed"] is False
    assert review["input_mode"] == "freeform"
    assert review["next_nonredundant_axis"] == [
        NEXT_RECOMMENDED_SLICE,
        AFTER_TINY_RENDER_SMOKE_SLICE,
        "newsroom-audio-tts-boundary-v1",
    ]


def test_doc_matches_renderer_and_has_no_fixed_form_relapse() -> None:
    strategy = _strategy()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_yym4_timing_gap_strategy_markdown(strategy)
    assert "strategy_status: accepted_for_next_tiny_render_smoke" in doc_text
    assert f"canonical_speaker_value: {CANONICAL_UI_OBSERVED_SPEAKER}" in doc_text
    assert "timing_gap_sec: 59.516667" in doc_text
    assert f"choice: {RECOMMENDED_DEFAULT}" in doc_text
    assert f"if_hybrid_chosen: {NEXT_RECOMMENDED_SLICE}" in doc_text
    assert "ymmp_patched_in_this_slice: false" in doc_text
    assert "operator_observation_card: none" in doc_text
    assert "Operator Observation Card" not in doc_text
    assert "result: pass / fail" not in doc_text
    assert "yes/no/unclear" not in doc_text.lower()


def test_timing_gap_artifacts_have_no_real_urls_or_outputs() -> None:
    strategy_text = STRATEGY_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(strategy_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(STRATEGY_PATH.parent.glob("*timing_gap_strategy*.ymmp"))
    assert not list(STRATEGY_PATH.parent.glob("*timing_gap_strategy*.mp4"))
    assert not list(STRATEGY_PATH.parent.glob("*timing_gap_strategy*.wav"))
    assert not list(STRATEGY_PATH.parent.glob("*timing_gap_strategy*.mp3"))
    assert not list(STRATEGY_PATH.parent.glob("*timing_gap_strategy*.m4a"))
