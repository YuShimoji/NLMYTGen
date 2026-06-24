import json
import re
from pathlib import Path

from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
)
from src.pipeline.newsroom_ymmp_timing_patch_strategy import (
    DEFAULT_YMMP_TIMING_PATCH_STRATEGY_DOC_PATH,
    DEFAULT_YMMP_TIMING_PATCH_STRATEGY_PATH,
    NEXT_PATCH_PROBE_SLICE,
    RECOMMENDED_DEFAULT,
    YMMP_TIMING_PATCH_STRATEGY_ID,
    YMMP_TIMING_PATCH_STRATEGY_SCHEMA_VERSION,
    build_default_newsroom_ymmp_timing_patch_strategy,
    render_newsroom_ymmp_timing_patch_strategy_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
STRATEGY_PATH = ROOT / DEFAULT_YMMP_TIMING_PATCH_STRATEGY_PATH
DOC_PATH = ROOT / DEFAULT_YMMP_TIMING_PATCH_STRATEGY_DOC_PATH


def _strategy() -> dict:
    return json.loads(STRATEGY_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_ymmp_timing_patch_strategy_matches_builder_output() -> None:
    strategy = _strategy()

    assert strategy == build_default_newsroom_ymmp_timing_patch_strategy(root=ROOT)
    assert strategy["artifact_id"] == YMMP_TIMING_PATCH_STRATEGY_ID
    assert strategy["strategy_id"] == YMMP_TIMING_PATCH_STRATEGY_ID
    assert strategy["schema_version"] == YMMP_TIMING_PATCH_STRATEGY_SCHEMA_VERSION
    assert strategy["review_status"] == "ready_for_supervisor_review"
    assert strategy["production_status"] == "diagnostic_only"
    assert strategy["diagnostic_only"] is True
    assert strategy["strategy_status"] == "recommended_for_probe"


def test_source_validation_reuses_audio_render_structure_and_neutral_timeline() -> None:
    validation = _strategy()["source_validation"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["canonical_speaker"] == CANONICAL_UI_OBSERVED_SPEAKER
    assert validation["canonical_speaker_unicode_escape"] == (
        CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
    )
    assert validation["tiny_render_duration_sec"] == 8
    assert validation["natural_duration_frames"] == 509
    assert validation["neutral_timeline_total_sec"] == 68
    assert validation["timing_gap_status"] == "unresolved"


def test_known_current_timing_state_records_8_sec_vs_68_sec_gap() -> None:
    timing = _strategy()["known_current_timing_state"]

    assert timing == {
        "tiny_render_duration_sec": 8,
        "tiny_render_duration_qualifier": "approx",
        "yym4_timebase_fps": 60,
        "natural_duration_frames": 509,
        "natural_duration_sec": round(509 / 60, 6),
        "neutral_timeline_total_sec": 68,
        "neutral_timeline_total_frames_at_60fps": 4080,
        "timing_gap_sec": 59.516667,
        "timing_gap_status": "unresolved",
        "audio_path_status": "diagnostic_pass",
        "voice_path": "YMM4_native_yukkuri_japanese",
        "external_TTS_status": "closed",
        "canonical_speaker": CANONICAL_UI_OBSERVED_SPEAKER,
    }


def test_strategy_candidates_cover_required_options_and_choose_default() -> None:
    candidates = {row["candidate_id"]: row for row in _strategy()["strategy_candidates"]}

    assert list(candidates) == [
        "A_keep_natural_8_sec_timing",
        "B_global_scale_current_item_frames_to_68_sec",
        "C_align_dialogue_start_end_to_neutral_timeline",
        "D_add_neutral_duration_tail_or_non_voice_carrier",
        "E_defer_68_sec_patch_until_script_density_increases",
    ]
    assert candidates["A_keep_natural_8_sec_timing"]["suitability"] == (
        "deferred_not_default_after_audio_pass"
    )
    assert candidates["B_global_scale_current_item_frames_to_68_sec"][
        "effect_on_voice_audio_assumptions"
    ].startswith("must preserve VoiceCache")
    assert candidates["C_align_dialogue_start_end_to_neutral_timeline"][
        "suitability"
    ] == "recommended_default"
    assert candidates["D_add_neutral_duration_tail_or_non_voice_carrier"][
        "suitability"
    ] == "fallback_if_voice_item_length_patch_is_unsafe"
    assert candidates["E_defer_68_sec_patch_until_script_density_increases"][
        "suitability"
    ] == "not_default_creative_density_is_separate"


def test_recommended_default_preserves_native_voice_and_separates_density() -> None:
    recommended = _strategy()["recommended_default"]

    assert recommended["choice"] == RECOMMENDED_DEFAULT
    assert recommended["next_probe"] == NEXT_PATCH_PROBE_SLICE
    assert "preserve YMM4 native voice fields, VoiceCache, speaker, and text" in (
        recommended["meaning"]
    )
    assert "do not introduce external TTS" in recommended["meaning"]
    assert "do not stretch or regenerate voice audio" in recommended["meaning"]
    assert "global voice/audio stretch" in recommended["not_recommended"]
    assert "production render immediately" in recommended["not_recommended"]


def test_patch_probe_boundary_allows_only_ignored_copy_and_structural_readback() -> None:
    boundary = _strategy()["patch_probe_boundary"]

    assert boundary["next_slice"] == NEXT_PATCH_PROBE_SLICE
    assert boundary["may_create_ignored_local_patched_ymmp_copy"] is True
    assert boundary["ymmp_commit_allowed"] is False
    assert boundary["json_patch_plan_first"] is True
    assert boundary["render_deferred_until_structural_readback_passes"] is True
    assert "Frame" in boundary["allowed_to_change"]
    assert "Length" in boundary["allowed_to_change"]
    assert "VoiceCache" in boundary["must_preserve"]
    assert "VoiceParameter" in boundary["must_preserve"]
    assert "Serif/text" in boundary["must_preserve"]
    assert "verify no .ymmp/media output is staged or committed" in (
        boundary["readback_required"]
    )


def test_render_gate_and_readiness_separation_keep_video_incomplete() -> None:
    strategy = _strategy()

    assert strategy["render_gate_carry_forward"] == {
        "render_gate_current": "L0 No Render",
        "next_render_trigger": (
            "after timing patch probe changes timeline surface and structural "
            "readback passes"
        ),
        "render_after_patch_expected_level": [
            "L2 Tiny Smoke Render",
            "L3 Targeted Regression Render",
        ],
        "render_performed_in_this_slice": False,
        "repeated_audio_check": False,
        "do_not_render_for": [
            "strategy docs",
            "readback JSON",
            "policy-only updates",
        ],
    }
    assert strategy["readiness_separation"]["video_readiness"]["status"] == (
        "incomplete"
    )
    assert strategy["readiness_separation"]["production_readiness"]["status"] == (
        "low_not_accepted"
    )


def test_not_accepted_scope_preserves_unproven_claims() -> None:
    assert _strategy()["not_accepted_scope"] == {
        "production_render_readiness": False,
        "public_video_readiness": False,
        "production_narration_quality": False,
        "final_script_narration_quality": False,
        "visual_layout_readiness": False,
        "real_content_readiness": False,
        "production_approval": False,
        "external_TTS_adoption": False,
        "neutral_68_sec_timing_proof": False,
    }


def test_video_and_production_readiness_totals_are_separate() -> None:
    strategy = _strategy()
    video = {row["gate"]: row["status"] for row in strategy["video_readiness"]}
    production = {
        row["gate"]: row["status"] for row in strategy["production_readiness"]
    }

    assert len(video) == 7
    assert video["source_input_path_proven"] is True
    assert video["timing_duration_strategy_defined"] is True
    assert video["targeted_regression_render_observed_if_required"] is False
    assert video["internal_review_milestone_reached"] is False
    assert len(production) == 7
    assert production["diagnostic_render_exists"] is True
    assert production["internal_review_accepted"] is False
    assert production["public_prod_use_explicitly_approved"] is False


def test_hygiene_nonredundancy_and_inertia_avoid_rechecks() -> None:
    strategy = _strategy()

    assert strategy["render_gate_hygiene"] == [
        {"gate": "render_performed_in_this_slice", "status": False},
        {"gate": "existing_render_audio_evidence_reused", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {"gate": "next_render_tied_to_timing_patch_probe_milestone", "status": True},
        {"gate": "no_render_for_docs_readback_changes", "status": True},
        {"gate": "repeated_audio_render_check_avoided", "status": True},
    ]
    assert strategy["human_burden_hygiene"] == [
        {"gate": "user_input", "status": "freeform"},
        {"gate": "template_required", "status": False},
        {"gate": "schema_owner", "status": "Agent"},
        {"gate": "user_side_work", "status": "none"},
        {"gate": "future_look_for_points_max", "status": 3},
        {"gate": "negative_confirmation_checklist", "status": False},
        {"gate": "fixed_form_relapse", "status": False},
    ]
    assert strategy["review_non_redundancy"][-1] == {
        "gate": "repeated_audio_render_review_requested",
        "status": False,
    }
    assert strategy["inertia_check"][-1] == {
        "gate": "next_concrete_milestone",
        "status": NEXT_PATCH_PROBE_SLICE,
    }


def test_boundaries_preserve_forbidden_action_claims() -> None:
    assert _strategy()["boundaries"] == {
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


def test_doc_matches_renderer_and_has_no_fixed_form_or_render_recheck() -> None:
    strategy = _strategy()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_ymmp_timing_patch_strategy_markdown(strategy)
    assert "strategy_status: recommended_for_probe" in doc_text
    assert f"choice: {RECOMMENDED_DEFAULT}" in doc_text
    assert f"next_slice: {NEXT_PATCH_PROBE_SLICE}" in doc_text
    assert "render_gate_current: L0 No Render" in doc_text
    assert "result: pass / fail" not in doc_text
    assert "yes/no/unclear" not in doc_text.lower()
    assert "please render" not in doc_text.lower()
    assert "please check audio" not in doc_text.lower()


def test_ymmp_timing_patch_strategy_artifacts_have_no_real_urls_or_media() -> None:
    strategy_text = STRATEGY_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(strategy_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(STRATEGY_PATH.parent.glob("*ymmp_timing_patch_strategy*.ymmp"))
    assert not list(STRATEGY_PATH.parent.glob("*ymmp_timing_patch_strategy*.mp4"))
    assert not list(STRATEGY_PATH.parent.glob("*ymmp_timing_patch_strategy*.wav"))
    assert not list(STRATEGY_PATH.parent.glob("*ymmp_timing_patch_strategy*.mp3"))
    assert not list(STRATEGY_PATH.parent.glob("*ymmp_timing_patch_strategy*.m4a"))
