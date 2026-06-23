import json
import re
from pathlib import Path

from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
    LOCAL_DIAGNOSTIC_YMMP_PATH,
)
from src.pipeline.newsroom_tiny_render_smoke_boundary import (
    DEFAULT_TINY_RENDER_SMOKE_BOUNDARY_DOC_PATH,
    DEFAULT_TINY_RENDER_SMOKE_BOUNDARY_PATH,
    SMOKE_FAILURE_CLASSIFICATION_SLICE,
    SMOKE_OPERATOR_POLISH_SLICE,
    SMOKE_SUCCESS_READBACK_SLICE,
    TIMING_PATCH_STRATEGY_SLICE,
    TINY_RENDER_SMOKE_BOUNDARY_ID,
    TINY_RENDER_SMOKE_BOUNDARY_SCHEMA_VERSION,
    build_default_newsroom_tiny_render_smoke_boundary,
    render_newsroom_tiny_render_smoke_boundary_markdown,
)
from src.pipeline.newsroom_yym4_timing_gap_strategy import RECOMMENDED_DEFAULT


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY_PATH = ROOT / DEFAULT_TINY_RENDER_SMOKE_BOUNDARY_PATH
DOC_PATH = ROOT / DEFAULT_TINY_RENDER_SMOKE_BOUNDARY_DOC_PATH


def _boundary() -> dict:
    return json.loads(BOUNDARY_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_tiny_render_smoke_boundary_matches_builder_output() -> None:
    boundary = _boundary()

    assert boundary == build_default_newsroom_tiny_render_smoke_boundary(root=ROOT)
    assert boundary["artifact_id"] == TINY_RENDER_SMOKE_BOUNDARY_ID
    assert boundary["boundary_id"] == TINY_RENDER_SMOKE_BOUNDARY_ID
    assert boundary["schema_version"] == TINY_RENDER_SMOKE_BOUNDARY_SCHEMA_VERSION
    assert boundary["review_status"] == "ready_for_supervisor_review"
    assert boundary["diagnostic_only"] is True
    assert boundary["production_status"] == "diagnostic_only"
    assert boundary["render_smoke_status"] == "not_run"
    assert boundary["boundary_status"] == "ready_for_future_manual_smoke"


def test_source_validation_reuses_timing_strategy_and_structure_readback() -> None:
    boundary = _boundary()
    validation = boundary["source_validation"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["recommended_timing_default"] == RECOMMENDED_DEFAULT
    assert validation["canonical_speaker_value"] == CANONICAL_UI_OBSERVED_SPEAKER
    assert validation["canonical_speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )
    assert validation["dialogue_item_count"] == 4
    assert validation["ymmp_total_frames"] == 509
    assert validation["ymmp_total_duration_sec"] == round(509 / 60, 6)


def test_target_records_diagnostic_ymmp_identity_and_expected_project_state() -> None:
    boundary = _boundary()
    target = boundary["target"]
    expected = target["expected_project_state"]

    assert target["diagnostic_ymmp_path"] == str(LOCAL_DIAGNOSTIC_YMMP_PATH).replace(
        "\\", "/"
    )
    assert (ROOT / LOCAL_DIAGNOSTIC_YMMP_PATH).exists()
    assert target["diagnostic_ymmp_path_status"] == (
        "discoverable_local_file_at_generation_time"
    )
    assert target["git_tracking_policy"] == "ignored_under_tmp_do_not_stage_or_commit"
    assert target["ymmp_file_newly_parsed_in_this_slice"] is False
    assert expected["dialogue_item_count"] == 4
    assert expected["speaker"] == CANONICAL_UI_OBSERVED_SPEAKER
    assert expected["speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )
    assert expected["fps"] == 60
    assert expected["total_frames"] == 509
    assert expected["natural_short_duration_sec"] == round(509 / 60, 6)
    assert expected["item_frames"] == [0, 130, 255, 369]
    assert expected["item_lengths"] == [130, 125, 114, 140]
    assert expected["voice_cache_present_but_not_tts_readiness"] is True
    assert expected["text_summaries"] == [
        "Fake topic, review only.",
        "Review-only handoff stays.",
        "A fake claim is shown.",
        "Fake source checks are noted.",
    ]


def test_allowed_future_manual_action_and_forbidden_actions_are_bounded() -> None:
    boundary = _boundary()
    allowed = boundary["allowed_future_manual_action"]
    forbidden = boundary["forbidden_actions"]
    assertions = boundary["boundary_assertions"]

    assert allowed["user_or_operator_may_open_yym4_manually_later"] is True
    assert allowed["user_or_operator_may_open_diagnostic_ymmp"] is True
    assert (
        allowed["user_or_operator_may_perform_one_tiny_render_smoke_if_comfortable"]
        is True
    )
    assert allowed["output_treated_as_diagnostic_only"] is True
    assert allowed["timing_changes_allowed_in_first_smoke"] is False
    assert allowed["agent_action_required_now"] is False
    assert forbidden == {
        "agent_yym4_launch": True,
        "agent_render": True,
        "production_render": True,
        "real_media_import": True,
        "timing_patch_during_first_smoke": True,
        "tts_configuration_changes_beyond_yym4_natural_existing_state": True,
        "public_video_claim": True,
        "commit_render_output_without_explicit_later_gate": True,
        "commit_ymmp_without_explicit_later_gate": True,
        "external_fetch": True,
        "dashboard_governance_freshness_change": True,
    }
    assert assertions["agent_launched_yym4"] is False
    assert assertions["agent_render_created"] is False
    assert assertions["ymmp_staged_or_committed"] is False
    assert assertions["render_output_staged_or_committed"] is False
    assert assertions["dashboard_governance_freshness_changed"] is False


def test_operator_observation_card_is_compact_freeform_and_later_only() -> None:
    boundary = _boundary()
    card = boundary["operator_observation_card"]
    hygiene = boundary["human_burden_hygiene"]

    assert card["status"] == "required_later"
    assert card["target"] == "diagnostic .ymmp tiny render smoke"
    assert card["answer_style"] == "freeform"
    assert "renderできました" in card["answer_hint"]
    assert len(card["look_for"]) == 3
    assert card["look_for"] == [
        "render completes or fails",
        "output plays and contains the four dialogue lines",
        "duration remains short/natural rather than 68 sec",
    ]
    assert "fixed form" in card["not_needed"]
    assert hygiene["user_input"] == "freeform"
    assert hygiene["template_required"] is False
    assert hygiene["schema_owner"] == "Agent"
    assert hygiene["max_required_points"] == 3
    assert hygiene["screenshot_optional"] is True
    assert hygiene["negative_confirmations_required_from_user"] is False
    assert hygiene["user_side_work_this_agent_slice"] == "none"


def test_agent_normalization_plan_and_timing_policy_are_separate_from_user_form() -> None:
    boundary = _boundary()
    normalization = boundary["agent_normalization_plan"]
    timing = boundary["timing_policy"]
    next_slices = boundary["next_recommended_slices"]

    assert normalization["schema_owner"] == "Agent"
    assert normalization["exposed_to_user_as_form"] is False
    assert normalization["user_must_fill_schema"] is False
    assert normalization["fields"] == [
        "result",
        "render_completed",
        "output_path_if_known",
        "output_duration_observed",
        "four_lines_visible_or_audible",
        "timing_observation",
        "error_message",
        "confidence",
        "unknowns",
    ]
    assert timing == {
        "first_smoke_timing_mode": "YMM4 natural duration",
        "natural_duration_sec": round(509 / 60, 6),
        "neutral_timeline_total_sec": 68,
        "neutral_68_sec_timing_patch": "deferred",
        "timing_patch_applied": False,
        "next_timing_axis_after_smoke": TIMING_PATCH_STRATEGY_SLICE,
    }
    assert next_slices == {
        "if_manual_render_succeeds": SMOKE_SUCCESS_READBACK_SLICE,
        "if_render_fails": SMOKE_FAILURE_CLASSIFICATION_SLICE,
        "if_operator_is_uncertain": SMOKE_OPERATOR_POLISH_SLICE,
        "next_timing_axis_after_smoke": TIMING_PATCH_STRATEGY_SLICE,
    }


def test_not_accepted_scope_and_review_memory_preserve_boundaries() -> None:
    boundary = _boundary()

    assert boundary["not_accepted_scope"] == {
        "production_ymmp": False,
        "timing_patch": False,
        "render_readiness_beyond_smoke_boundary": False,
        "TTS_readiness": False,
        "public_video_readiness": False,
        "visual_layout_import": False,
        "production_approval": False,
    }
    assert boundary["review_memory"]["prior_user_review_count"] == {
        "manual_import_behavior": 1,
        "bound_speaker_behavior": 1,
        "diagnostic_ymmp_manual_observation": 1,
        "ymmp_structure_readback": 1,
        "timing_gap_strategy": 1,
        "tiny_render_smoke_boundary": 0,
    }
    assert boundary["review_memory"]["repeated_general_review_allowed"] is False
    assert boundary["review_memory"]["input_mode"] == "freeform"


def test_doc_matches_renderer_and_has_no_fixed_form_relapse() -> None:
    boundary = _boundary()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_tiny_render_smoke_boundary_markdown(boundary)
    assert "render_smoke_status: not_run" in doc_text
    assert "diagnostic_ymmp_path: _tmp/newsroom_manual_probe" in doc_text
    assert "Operator Observation Card" in doc_text
    assert "look_for:" in doc_text
    assert "renderできました" in doc_text
    assert "schema_owner: Agent" in doc_text
    assert "first_smoke_timing_mode: YMM4 natural duration" in doc_text
    assert "agent_render_created: false" not in doc_text
    assert "result: pass / fail" not in doc_text
    assert "yes/no/unclear" not in doc_text.lower()


def test_tiny_render_smoke_boundary_artifacts_have_no_real_urls_or_outputs() -> None:
    boundary_text = BOUNDARY_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(boundary_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(BOUNDARY_PATH.parent.glob("*tiny_render_smoke*.ymmp"))
    assert not list(BOUNDARY_PATH.parent.glob("*tiny_render_smoke*.mp4"))
    assert not list(BOUNDARY_PATH.parent.glob("*tiny_render_smoke*.wav"))
    assert not list(BOUNDARY_PATH.parent.glob("*tiny_render_smoke*.mp3"))
    assert not list(BOUNDARY_PATH.parent.glob("*tiny_render_smoke*.m4a"))
