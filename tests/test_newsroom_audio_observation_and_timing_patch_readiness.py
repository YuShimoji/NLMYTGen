import json
import re
from pathlib import Path

from src.pipeline.newsroom_audio_observation_and_timing_patch_readiness import (
    AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_ID,
    AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_SCHEMA_VERSION,
    DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_DOC_PATH,
    DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH,
    ENGLISH_WORD_HANDLING,
    NEXT_RECOMMENDED_SLICE,
    OBSERVED_READING,
    OBSERVED_READING_UNICODE_ESCAPE,
    OBSERVED_SOURCE_WORD,
    VOICE_PATH,
    build_default_newsroom_audio_observation_and_timing_patch_readiness,
    render_newsroom_audio_observation_and_timing_patch_readiness_markdown,
)
from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
)


ROOT = Path(__file__).resolve().parents[1]
READBACK_PATH = ROOT / DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_PATH
DOC_PATH = ROOT / DEFAULT_AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_DOC_PATH


def _readback() -> dict:
    return json.loads(READBACK_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_audio_observation_readiness_matches_builder_output() -> None:
    readback = _readback()

    assert readback == (
        build_default_newsroom_audio_observation_and_timing_patch_readiness(
            root=ROOT
        )
    )
    assert readback["artifact_id"] == AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_ID
    assert readback["readback_id"] == AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_ID
    assert readback["schema_version"] == (
        AUDIO_OBSERVATION_AND_TIMING_PATCH_READINESS_SCHEMA_VERSION
    )
    assert readback["review_status"] == "ready_for_supervisor_review"
    assert readback["production_status"] == "diagnostic_only"
    assert readback["diagnostic_only"] is True
    assert readback["observation_source"] == "user_freeform"
    assert readback["readiness_status"] == "accepted_for_timing_patch_strategy"


def test_source_validation_reuses_existing_readbacks() -> None:
    validation = _readback()["source_validation"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["native_audio_path_prior_status"] == "passed_with_unknowns"
    assert validation["tiny_render_result"] == "pass"
    assert validation["tiny_render_duration_sec"] == 8
    assert validation["timing_gap_status"] == "unresolved"
    assert validation["canonical_speaker"] == CANONICAL_UI_OBSERVED_SPEAKER
    assert validation["canonical_speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )


def test_normalized_audio_observation_accepts_diagnostic_native_audio_only() -> None:
    observation = _readback()["normalized_audio_observation"]

    assert observation["audio_presence_in_render"] is True
    assert observation["voice_path"] == VOICE_PATH
    assert observation["canonical_speaker"] == CANONICAL_UI_OBSERVED_SPEAKER
    assert observation["canonical_speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )
    assert observation["english_word_handling"] == ENGLISH_WORD_HANDLING
    assert observation["observed_example"] == {
        "source_text": OBSERVED_SOURCE_WORD,
        "observed_reading": OBSERVED_READING,
        "observed_reading_unicode_escape": OBSERVED_READING_UNICODE_ESCAPE,
        "normalization": f"{OBSERVED_SOURCE_WORD} -> {OBSERVED_READING}",
    }
    assert observation["spelling_read_issue"] is False
    assert observation["diagnostic_audio_path_accepted"] is True
    assert observation["audio_quality_accepted_for_diagnostic_flow"] is True
    assert observation["audio_quality_accepted_for_production"] is False
    assert observation["TTS_ready_for_production"] is False
    assert observation["external_TTS_introduced"] is False
    assert observation["production_ready"] is False


def test_accepted_and_not_accepted_scopes_keep_production_separate() -> None:
    readback = _readback()

    assert readback["accepted_scope"] == {
        "tiny_render_includes_audible_native_yym4_yukkuri_voice": True,
        "audio_sufficient_to_continue_diagnostic_flow": True,
        "english_loanword_handling_acceptable_for_diagnostic_flow": True,
        "external_TTS_unnecessary_for_now": True,
    }
    assert readback["not_accepted_scope"] == {
        "production_narration_quality": False,
        "final_subtitle_narration_script": False,
        "public_video_readiness": False,
        "neutral_68_sec_timing_proof": False,
        "visual_layout_readiness": False,
        "real_content_readiness": False,
        "production_approval": False,
    }


def test_timing_readiness_separates_audio_acceptance_from_patch_work() -> None:
    timing = _readback()["timing_readiness"]

    assert timing == {
        "tiny_render_duration_sec": 8,
        "tiny_render_duration_qualifier": "approx",
        "first_smoke_timing_mode": "YMM4 natural duration",
        "neutral_timeline_total_sec": 68,
        "ymmp_natural_duration_sec": round(509 / 60, 6),
        "timing_gap_status": "unresolved",
        "neutral_68_sec_timing_patch_applied": False,
        "recommended_next_axis": NEXT_RECOMMENDED_SLICE,
        "reason": [
            "render path works",
            "native audio path is diagnostic-acceptable",
            "external TTS remains closed",
            "timing patch can now be handled as a separate axis",
        ],
    }


def test_render_gate_policy_prevents_docs_only_rerenders() -> None:
    readback = _readback()

    assert readback["render_gate_policy"] == {
        "new_render_in_this_slice": False,
        "render_gate": "milestone_gated_not_change_gated",
        "future_render_condition": (
            "only after timing patch or another output-affecting milestone"
        ),
        "do_not_rerender_for": [
            "docs changes",
            "readback changes",
            "policy changes",
        ],
    }
    assert readback["render_gate_hygiene"] == [
        {"gate": "render_performed_in_this_slice", "status": False},
        {"gate": "existing_render_observation_reused", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {"gate": "next_render_tied_to_output_milestone", "status": True},
        {"gate": "no_render_for_docs_readback_changes", "status": True},
        {"gate": "output_retention_deferred_unless_needed", "status": True},
    ]


def test_progress_and_next_slices_point_to_timing_patch_strategy() -> None:
    readback = _readback()

    assert readback["progress_strip"] == {
        "lane": "VIDEO v0.1 READINESS",
        "progress_completed": 5,
        "progress_total": 7,
        "current": "tiny render + native audio diagnostic pass",
        "next": NEXT_RECOMMENDED_SLICE,
        "main_blocker": "8 sec natural duration vs 68 sec neutral timeline",
        "user_work": "none",
    }
    assert readback["recommended_next_slices"] == [
        NEXT_RECOMMENDED_SLICE,
        "newsroom-ymmp-timing-patch-probe-v1",
        "milestone-gated-render-smoke-after-timing-patch",
        "newsroom-render-output-retention-policy-v1",
    ]


def test_hygiene_and_nonredundancy_do_not_reask_user_or_render() -> None:
    readback = _readback()

    assert readback["human_burden_hygiene"] == [
        {"gate": "user_input", "status": "freeform"},
        {"gate": "template_required", "status": False},
        {"gate": "schema_owner", "status": "Agent"},
        {"gate": "user_side_work", "status": "none"},
        {"gate": "future_look_for_points_max", "status": 3},
        {"gate": "negative_confirmation_checklist", "status": False},
        {"gate": "fixed_form_relapse", "status": False},
    ]
    assert readback["review_non_redundancy"] == [
        {"gate": "prior_render_evidence_reused", "status": True},
        {"gate": "prior_audio_tts_boundary_reused", "status": True},
        {"gate": "user_audio_observation_consumed_once", "status": True},
        {"gate": "next_axis_stated", "status": NEXT_RECOMMENDED_SLICE},
        {"gate": "not_accepted_scope_preserved", "status": True},
        {"gate": "repeated_audio_check_requested", "status": False},
    ]
    assert readback["inertia_check"][-1] == {
        "gate": "next_concrete_milestone",
        "status": NEXT_RECOMMENDED_SLICE,
    }


def test_boundaries_preserve_forbidden_action_claims() -> None:
    assert _readback()["boundaries"] == {
        "YMM4_launched_by_agent": False,
        "render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "real_media_imported": False,
        "external_fetch_performed": False,
        "ymmp_created_or_modified_by_agent": False,
        "ymmp_or_media_staged_or_committed": False,
        "production_approval": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


def test_doc_matches_renderer_and_has_no_fixed_form_relapse() -> None:
    readback = _readback()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == (
        render_newsroom_audio_observation_and_timing_patch_readiness_markdown(
            readback
        )
    )
    assert "readiness_status: accepted_for_timing_patch_strategy" in doc_text
    assert f"voice_path: {VOICE_PATH}" in doc_text
    assert f"normalization': '{OBSERVED_SOURCE_WORD} -> {OBSERVED_READING}'" in doc_text
    assert f"recommended_next_axis: {NEXT_RECOMMENDED_SLICE}" in doc_text
    assert "result: pass / fail" not in doc_text
    assert "yes/no/unclear" not in doc_text.lower()


def test_audio_observation_readiness_artifacts_have_no_real_urls_or_media() -> None:
    readback_text = READBACK_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(readback_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(READBACK_PATH.parent.glob("*audio_observation*.ymmp"))
    assert not list(READBACK_PATH.parent.glob("*audio_observation*.mp4"))
    assert not list(READBACK_PATH.parent.glob("*audio_observation*.wav"))
    assert not list(READBACK_PATH.parent.glob("*audio_observation*.mp3"))
    assert not list(READBACK_PATH.parent.glob("*audio_observation*.m4a"))
