import json
import re
import subprocess
from pathlib import Path

from src.pipeline.newsroom_ymmp_timing_patch_render_smoke_result_readback import (
    DEFAULT_RENDER_OUTPUT_LOCAL_PATH,
    DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_DOC_PATH,
    DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH,
    INTERNAL_REVIEW_PREP_SLICE,
    NEXT_DEFAULT_SLICE,
    RETENTION_POLICY_SLICE,
    RSS_DRY_RUN_PLAN_SLICE,
    USER_FREEFORM_OBSERVATION,
    VOICE_PATH,
    YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_ID,
    YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION,
    build_default_newsroom_ymmp_timing_patch_render_smoke_result_readback,
    render_newsroom_ymmp_timing_patch_render_smoke_result_readback_markdown,
)
from src.pipeline.newsroom_ymmp_timing_patch_probe import DEFAULT_PATCHED_YMMP_LOCAL_PATH


ROOT = Path(__file__).resolve().parents[1]
READBACK_PATH = ROOT / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_PATH
DOC_PATH = ROOT / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_DOC_PATH
PATCHED_YMMP_PATH = ROOT / DEFAULT_PATCHED_YMMP_LOCAL_PATH
RENDER_OUTPUT_PATH = ROOT / DEFAULT_RENDER_OUTPUT_LOCAL_PATH


def _readback() -> dict:
    return json.loads(READBACK_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_result_readback_matches_builder_output() -> None:
    readback = _readback()

    assert readback == (
        build_default_newsroom_ymmp_timing_patch_render_smoke_result_readback(
            root=ROOT
        )
    )
    assert readback["artifact_id"] == (
        YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_ID
    )
    assert readback["readback_id"] == YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_ID
    assert readback["schema_version"] == (
        YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION
    )
    assert readback["review_status"] == "ready_for_supervisor_review"
    assert readback["production_status"] == "diagnostic_only"
    assert readback["diagnostic_only"] is True
    assert readback["observation_source"] == "user_freeform_with_screenshot_support"
    assert readback["result_status"] == "pass"


def test_identity_and_source_validation_anchor_the_prior_smoke_package() -> None:
    readback = _readback()
    identity = readback["identity"]
    validation = readback["source_validation"]

    assert identity["source_render_smoke_package_path"] == (
        "samples/_probe/newsroom_handoff/ymmp_timing_patch_render_smoke_v1.json"
    )
    assert identity["source_timing_patch_probe_path"] == (
        "samples/_probe/newsroom_handoff/ymmp_timing_patch_probe_v1.json"
    )
    assert identity["source_timing_patch_strategy_path"] == (
        "samples/_probe/newsroom_handoff/ymmp_timing_patch_strategy_v1.json"
    )
    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["canonical_speaker"] == "ゆっくり霊夢"
    assert validation["canonical_speaker_unicode_escape"] == (
        "\\u3086\\u3063\\u304f\\u308a\\u970a\\u5922"
    )
    assert validation["expected_duration_sec"] == 68.0
    assert validation["expected_total_frames"] == 4080
    assert validation["expected_dialogue_item_count"] == 4
    assert validation["patched_ymmp_found_at_generation"] is True


def test_user_and_screenshot_observations_are_consumed_without_fixed_form() -> None:
    readback = _readback()
    operator = readback["operator_freeform_observation"]
    screenshot = readback["screenshot_supported_observation"]

    assert operator["input_mode"] == "freeform"
    assert operator["raw_observation"] == USER_FREEFORM_OBSERVATION
    assert operator["fixed_result_template_requested"] is False
    assert operator["manual_observation_re_requested"] is False
    assert screenshot["output_file_name"] == (
        "diagnostic_bound_speaker_probe_timing_patch_v1.mp4"
    )
    assert screenshot["windows_properties_duration"] == "00:01:08"
    assert screenshot["frame_width_height"] == "1920x1080"
    assert screenshot["frame_rate"] == "60.00 fps"
    assert screenshot["audio_stream_observed"] is True
    assert screenshot["audio_sample_rate"] == "48.000 kHz"
    assert screenshot["yym4_preview_project_duration"] == "00:01:08.00"
    assert screenshot["dialogue_items_remaining_on_timeline"] == 4
    assert screenshot["preview_text_observed"] == "Fake topic, review only."
    assert screenshot["media_file_committed"] is False


def test_normalized_render_result_closes_68_second_timing_smoke() -> None:
    result = _readback()["normalized_render_result"]

    assert result["render_smoke_result"] == "pass"
    assert result["yym4_opened_patched_project"] is True
    assert result["render_completed"] is True
    assert result["output_video_observed"] is True
    assert result["output_duration_observed"] == "00:01:08"
    assert result["output_duration_sec"] == 68
    assert result["expected_duration_sec"] == 68
    assert result["duration_matches_timing_patch"] is True
    assert result["output_resolution_observed"] == "1920x1080"
    assert result["output_fps_observed"] == 60
    assert result["audio_stream_observed"] is True
    assert result["audio_sample_rate_observed"] == "48kHz"
    assert result["native_audio_present"] is True
    assert result["voice_path"] == VOICE_PATH
    assert result["dialogue_items_visible"] is True
    assert result["dialogue_item_count_observed"] == 4
    assert result["majority_silence_observed"] is True
    assert result["majority_silence_expected_for_diagnostic_sparse_timeline"] is True
    assert result["post_speech_elements_extended"] is True
    assert result["timing_patch_effective_in_render"] is True
    assert result["production_pacing_accepted"] is False
    assert result["production_quality_accepted"] is False
    assert result["visual_layout_accepted"] is False
    assert result["public_video_ready"] is False


def test_accepted_and_not_accepted_scopes_keep_diagnostic_boundary() -> None:
    readback = _readback()

    assert readback["accepted_scope"] == {
        "patched_ymmp_can_be_opened_and_rendered_in_current_yym4_environment": True,
        "timing_patch_effective_in_rendered_output": True,
        "four_dialogue_items_remain_visible": True,
        "native_yukkuri_audio_remains_present": True,
        "sparse_silence_expected_for_this_diagnostic_skeleton": True,
        "timing_patch_smoke_passes_at_diagnostic_level": True,
    }
    assert readback["not_accepted_scope"] == {
        "production_pacing": False,
        "final_narration_pacing": False,
        "final_script_density": False,
        "visual_layout_quality": False,
        "public_video_readiness": False,
        "production_render_readiness": False,
        "real_content_readiness": False,
        "production_approval": False,
        "external_TTS_adoption": False,
    }


def test_readiness_separation_advances_video_but_not_production_readiness() -> None:
    readiness = _readback()["readiness_separation"]
    video = _readback()["video_readiness"]

    assert readiness["slice_completion"] == "pass_for_this_readback"
    assert readiness["video_readiness_progress"] == "6/7"
    assert readiness["video_readiness_current"] == (
        "targeted 68sec patched render observed"
    )
    assert readiness["video_readiness_next_missing_gate"] == (
        "internal review milestone after visual/card bridge"
    )
    assert readiness["production_readiness"] == "low_diagnostic_only"
    assert readiness["next_default_slice"] == NEXT_DEFAULT_SLICE
    assert [row["status"] for row in video] == [
        True,
        True,
        True,
        True,
        True,
        True,
        False,
    ]


def test_render_gate_consumes_observation_once_and_defers_next_render() -> None:
    gate = _readback()["render_gate_carry_forward"]

    assert gate["current_render_observation_consumed_once"] is True
    assert gate["new_render_in_this_slice"] is False
    assert gate["YMM4_launched_by_agent"] is False
    assert gate["render_audio_or_tts_created_by_agent"] is False
    assert gate["render_gate"] == "milestone_gated_not_docs_gated"
    assert gate["next_render_allowed_after"] == [
        "visual/card bridge affects the video surface",
        "internal review v0.1 milestone",
    ]
    assert gate["do_not_rerender_for"] == [
        "docs changes",
        "readback changes",
        "policy-only changes",
    ]
    assert gate["repeated_audio_or_render_check_requested"] is False


def test_recommended_next_slices_choose_visual_card_bridge_default() -> None:
    rows = _readback()["recommended_next_slices"]

    assert [row["slice"] for row in rows] == [
        NEXT_DEFAULT_SLICE,
        INTERNAL_REVIEW_PREP_SLICE,
        RETENTION_POLICY_SLICE,
        RSS_DRY_RUN_PLAN_SLICE,
    ]
    assert rows[0]["timing"] == "recommended_next_default"
    assert "visible card assets" in rows[0]["reason"]
    assert rows[2]["timing"] == "only_if_output_artifacts_need_retention"
    assert rows[3]["timing"] == "later_not_immediate"


def test_next_lane_principle_uses_external_cards_not_complex_ymmp_graphs() -> None:
    principles = _readback()["implementation_principle_for_next_lane"]

    assert principles == [
        "Do not rebuild cards as complex YMM4 object graphs.",
        (
            "Prefer external card assets generated from HTML/SVG/Canvas and "
            "imported or placed into YMM4 later."
        ),
        "Preserve the YMM4 native audio path.",
        (
            "Keep .ymmp mutation limited to ignored local copies and bounded "
            "timing/layout carrier operations."
        ),
    ]


def test_completion_matrices_and_hygiene_match_contract_counts() -> None:
    readback = _readback()

    assert len(readback["completion_matrix"]) == 6
    assert len(readback["artifact_readiness"]) == 6
    assert len(readback["video_readiness"]) == 7
    assert len(readback["render_gate_hygiene"]) == 6
    assert len(readback["human_burden_hygiene"]) == 7
    assert len(readback["review_non_redundancy"]) == 6
    assert len(readback["inertia_check"]) == 5
    assert readback["human_burden_hygiene"] == [
        {"gate": "user_input", "status": "freeform"},
        {"gate": "template_required", "status": False},
        {"gate": "schema_owner", "status": "Agent"},
        {"gate": "user_side_work", "status": "none"},
        {"gate": "future_look_for_points_max", "status": 3},
        {"gate": "negative_confirmation_checklist", "status": False},
        {"gate": "fixed_form_relapse", "status": False},
    ]
    assert readback["inertia_check"][-1] == {
        "gate": "next_concrete_milestone",
        "status": NEXT_DEFAULT_SLICE,
    }


def test_local_ymmp_and_mp4_are_ignored_untracked_and_not_committed() -> None:
    readback = _readback()
    local_status = readback["local_artifact_status"]

    assert PATCHED_YMMP_PATH.exists()
    assert RENDER_OUTPUT_PATH.exists()
    assert local_status["render_output_exists_at_readback_generation"] is True
    assert local_status["patched_ymmp_exists_at_readback_generation"] is True
    assert local_status["render_output_staged"] is False
    assert local_status["render_output_committed"] is False
    assert local_status["patched_ymmp_staged"] is False
    assert local_status["patched_ymmp_committed"] is False
    for rel_path in [
        DEFAULT_PATCHED_YMMP_LOCAL_PATH.as_posix(),
        DEFAULT_RENDER_OUTPUT_LOCAL_PATH.as_posix(),
    ]:
        check_ignore = subprocess.run(
            ["git", "check-ignore", "-v", "--", rel_path],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        ls_files = subprocess.run(
            ["git", "ls-files", "--", rel_path],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        status = subprocess.run(
            ["git", "status", "--short", "--", rel_path],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert check_ignore.returncode == 0
        assert "_tmp/" in check_ignore.stdout
        assert ls_files.stdout == ""
        assert status.stdout == ""


def test_doc_matches_renderer_and_avoids_repeated_render_or_fixed_form_request() -> None:
    readback = _readback()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == (
        render_newsroom_ymmp_timing_patch_render_smoke_result_readback_markdown(
            readback
        )
    )
    assert "result_status: pass" in doc_text
    assert "output_duration_sec: 68" in doc_text
    assert "video_readiness_progress: 6/7" in doc_text
    assert NEXT_DEFAULT_SLICE in doc_text
    assert "production_pacing: false" in doc_text
    assert "yes/no/unclear" not in doc_text.lower()
    assert "please render" not in doc_text.lower()
    assert "please check audio" not in doc_text.lower()
    assert "fixed form" not in doc_text.lower()


def test_result_readback_artifacts_have_no_real_urls_or_committed_media() -> None:
    readback_text = READBACK_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(readback_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(READBACK_PATH.parent.glob("*render_smoke_result_readback*.ymmp"))
    assert not list(READBACK_PATH.parent.glob("*render_smoke_result_readback*.mp4"))
    assert not list(READBACK_PATH.parent.glob("*render_smoke_result_readback*.wav"))
    assert not list(READBACK_PATH.parent.glob("*render_smoke_result_readback*.mp3"))
    assert not list(READBACK_PATH.parent.glob("*render_smoke_result_readback*.m4a"))
