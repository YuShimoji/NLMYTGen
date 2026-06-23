import json
import re
from pathlib import Path

from src.pipeline.newsroom_audio_tts_boundary import (
    AUDIO_TTS_BOUNDARY_ID,
    AUDIO_TTS_BOUNDARY_SCHEMA_VERSION,
    DEFAULT_AUDIO_TTS_BOUNDARY_DOC_PATH,
    DEFAULT_AUDIO_TTS_BOUNDARY_PATH,
    RECOMMENDED_DEFAULT,
    TIMING_PATCH_STRATEGY_SLICE,
    TINY_AUDIO_OBSERVATION_SLICE,
    YYM4_NATIVE_AUDIO_PATH_PROOF_SLICE,
    build_default_newsroom_audio_tts_boundary,
    render_newsroom_audio_tts_boundary_markdown,
)
from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
)


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY_PATH = ROOT / DEFAULT_AUDIO_TTS_BOUNDARY_PATH
DOC_PATH = ROOT / DEFAULT_AUDIO_TTS_BOUNDARY_DOC_PATH


def _boundary() -> dict:
    return json.loads(BOUNDARY_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_audio_tts_boundary_matches_builder_output() -> None:
    boundary = _boundary()

    assert boundary == build_default_newsroom_audio_tts_boundary(root=ROOT)
    assert boundary["artifact_id"] == AUDIO_TTS_BOUNDARY_ID
    assert boundary["boundary_id"] == AUDIO_TTS_BOUNDARY_ID
    assert boundary["schema_version"] == AUDIO_TTS_BOUNDARY_SCHEMA_VERSION
    assert boundary["review_status"] == "ready_for_supervisor_review"
    assert boundary["diagnostic_only"] is True
    assert boundary["production_status"] == "diagnostic_only"
    assert boundary["boundary_status"] == "accepted_for_next_audio_observation"


def test_source_validation_reuses_render_result_structure_and_timing_strategy() -> None:
    boundary = _boundary()
    validation = boundary["source_validation"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["canonical_speaker_value"] == CANONICAL_UI_OBSERVED_SPEAKER
    assert validation["canonical_speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )
    assert validation["voice_cache_item_count"] == 4
    assert validation["voice_audio_related_fields_present"] == [
        "VoiceLength",
        "VoiceCache",
        "VoiceParameter",
        "Pronounce",
        "Hatsuon",
        "AudioEffects",
    ]


def test_known_render_result_is_pass_but_not_audio_acceptance() -> None:
    boundary = _boundary()
    result = boundary["known_render_result"]

    assert result["tiny_render_smoke_result"] == "pass"
    assert result["output_video_observed"] is True
    assert result["approximate_duration_sec"] == 8
    assert result["four_dialogue_lines_visible"] is True
    assert result["timing_mode"] == "YMM4 natural duration"
    assert result["neutral_68_sec_timing_patch_applied"] is False
    assert result["render_output_path_if_known"] == (
        "_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.mp4"
    )
    assert result["render_output_committed"] is False
    assert result["render_output_staged"] is False


def test_audio_tts_knowns_record_voicecache_but_keep_audio_presence_unknown() -> None:
    boundary = _boundary()
    knowns = boundary["audio_tts_knowns_and_unknowns"]

    assert knowns["VoiceCache_or_voice_fields_present_in_ymmp"] is True
    assert knowns["voice_item_count"] == 4
    assert knowns["voice_cache_item_count"] == 4
    assert knowns["character_voice_apis"] == ["AquesTalk"]
    assert knowns["TTS_generated_by_agent"] is False
    assert knowns["explicit_operator_TTS_generation"] is False
    assert knowns["audio_presence_in_render"] == "unknown"
    assert knowns["audio_quality_accepted"] is False
    assert knowns["TTS_ready"] is False
    assert knowns["voice_binding_ready"] == "partial"
    assert knowns["speaker_binding_status"] == (
        f"{CANONICAL_UI_OBSERVED_SPEAKER} accepted for diagnostic import"
    )
    assert knowns["speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )
    assert "do not establish audio presence" in knowns["known_unknown_note"]


def test_responsibility_split_recommends_yym4_native_and_keeps_external_tts_closed() -> None:
    boundary = _boundary()
    rows = {row["path_id"]: row for row in boundary["responsibility_split"]}

    assert list(rows) == [
        "yym4_native_voice_audio_path",
        "external_tts_path",
        "metadata_only_voice_profile_path",
        "no_audio_diagnostic_render_path",
    ]
    assert rows["yym4_native_voice_audio_path"]["role"] == (
        "recommended_next_diagnostic_path"
    )
    assert "native voice path proof" in rows["yym4_native_voice_audio_path"][
        "what_it_enables"
    ]
    assert rows["external_tts_path"]["role"] == "closed_for_now"
    assert "adds timing drift before the native path is understood" in rows[
        "external_tts_path"
    ]["risks"]
    assert rows["metadata_only_voice_profile_path"]["role"] == "planning_only"
    assert rows["no_audio_diagnostic_render_path"]["role"] == (
        "fallback_if_audio_remains_unneeded"
    )


def test_recommended_default_and_audio_observation_card_are_compact() -> None:
    boundary = _boundary()
    recommended = boundary["recommended_default"]
    card = boundary["operator_observation_card_if_needed"]

    assert recommended["choice"] == RECOMMENDED_DEFAULT
    assert "keep YMM4 native voice/audio path as the next diagnostic path" in (
        recommended["do_now"]
    )
    assert "external TTS generation" in recommended["defer"]
    assert "audio quality acceptance" in recommended["defer"]
    assert card["status"] == "proposed_if_needed"
    assert card["answer_style"] == "freeform"
    assert len(card["look_for"]) == 3
    assert card["look_for"] == [
        "whether any audio is present",
        "whether the voice sounds like the expected YMM4 speaker",
        "whether there is obvious silence, cutoff, or mismatch",
    ]
    assert "fixed form" in card["not_needed"]
    assert "new render" in card["not_needed"]
    assert "external TTS" in card["not_needed"]


def test_timing_interaction_and_next_slices_keep_patch_deferred() -> None:
    boundary = _boundary()
    timing = boundary["timing_interaction"]
    next_slices = boundary["next_recommended_slices"]

    assert timing == {
        "first_render_smoke_used_natural_duration": True,
        "first_smoke_duration_sec": 8,
        "first_smoke_duration_qualifier": "approx",
        "prior_ymmp_natural_duration_sec": round(509 / 60, 6),
        "neutral_68_sec_timing_patch_remains_deferred": True,
        "audio_tts_choice_may_affect_timing_duration": True,
        "do_not_patch_timing_before_audio_tts_boundary_understood": True,
        "timing_patch_applied": False,
    }
    assert next_slices == {
        "if_audio_presence_is_sufficient_from_existing_evidence": (
            TIMING_PATCH_STRATEGY_SLICE
        ),
        "if_audio_presence_is_unknown_and_needed": TINY_AUDIO_OBSERVATION_SLICE,
        "if_audio_path_should_be_defined_first": (
            YYM4_NATIVE_AUDIO_PATH_PROOF_SLICE
        ),
        "do_not_recommend": "production_render_immediately",
    }


def test_boundary_status_and_human_burden_keep_generation_closed() -> None:
    boundary = _boundary()
    status = boundary["boundary_status_detail"]
    hygiene = boundary["human_burden_hygiene"]

    assert status == {
        "render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "real_media_imported": False,
        "production_approval": False,
        "public_video_ready": False,
        "output_retention_required_now": False,
        "dashboard_governance_freshness_changed": False,
    }
    assert hygiene == {
        "user_input": "freeform",
        "template_required": False,
        "schema_owner": "Agent",
        "user_side_work_this_slice": "none",
        "future_observation_max_required_points": 3,
        "screenshot_optional": True,
        "negative_confirmations_required_from_user": False,
        "fixed_form_result_template": False,
    }
    assert boundary["review_memory"]["repeated_general_review_allowed"] is False
    assert boundary["review_memory"]["user_side_work_re_requested"] is False


def test_not_accepted_scope_preserves_audio_and_production_boundaries() -> None:
    boundary = _boundary()

    assert boundary["not_accepted_scope"] == {
        "production_render_readiness": False,
        "public_video_readiness": False,
        "neutral_68_sec_timing_proof": False,
        "visual_layout_readiness": False,
        "TTS_audio_quality_acceptance": False,
        "TTS_readiness": False,
        "real_content_readiness": False,
        "production_approval": False,
    }
    assert "claim audio quality acceptance" in boundary["downstream_next_use"][
        "do_not_use_this_boundary_to"
    ]
    assert "generate or import audio" in boundary["downstream_next_use"][
        "do_not_use_this_boundary_to"
    ]


def test_doc_matches_renderer_and_has_no_fixed_form_relapse() -> None:
    boundary = _boundary()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_audio_tts_boundary_markdown(boundary)
    assert "boundary_status: accepted_for_next_audio_observation" in doc_text
    assert "audio_presence_in_render: unknown" in doc_text
    assert f"choice: {RECOMMENDED_DEFAULT}" in doc_text
    assert "external_tts_path | closed_for_now" in doc_text
    assert "Operator Observation Card If Needed" in doc_text
    assert "future_observation_max_required_points: 3" in doc_text
    assert "result: pass / fail" not in doc_text
    assert "yes/no/unclear" not in doc_text.lower()


def test_audio_tts_boundary_artifacts_have_no_real_urls_or_outputs() -> None:
    boundary_text = BOUNDARY_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(boundary_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(BOUNDARY_PATH.parent.glob("*audio_tts_boundary*.ymmp"))
    assert not list(BOUNDARY_PATH.parent.glob("*audio_tts_boundary*.mp4"))
    assert not list(BOUNDARY_PATH.parent.glob("*audio_tts_boundary*.wav"))
    assert not list(BOUNDARY_PATH.parent.glob("*audio_tts_boundary*.mp3"))
    assert not list(BOUNDARY_PATH.parent.glob("*audio_tts_boundary*.m4a"))
