import json
import re
import subprocess
from pathlib import Path

from src.pipeline.newsroom_card_placement_render_smoke_result_readback import (
    CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_ID,
    CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION,
    DEFAULT_CARD_PLACEMENT_RENDER_OUTPUT_LOCAL_PATH,
    DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_DOC_PATH,
    DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH,
    NEXT_DEFAULT_SLICE,
    build_default_newsroom_card_placement_render_smoke_result_readback,
    render_newsroom_card_placement_render_smoke_result_readback_markdown,
)
from src.pipeline.newsroom_yym4_card_asset_placement_probe import (
    DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH,
)


ROOT = Path(__file__).resolve().parents[1]
READBACK_PATH = ROOT / DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
DOC_PATH = ROOT / DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_DOC_PATH
RENDER_OUTPUT_PATH = ROOT / DEFAULT_CARD_PLACEMENT_RENDER_OUTPUT_LOCAL_PATH
CARD_PLACEMENT_YMMP_PATH = ROOT / DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH


def _readback() -> dict:
    return json.loads(READBACK_PATH.read_text(encoding="utf-8"))


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_result_readback_matches_builder_output_and_identity() -> None:
    readback = _readback()

    assert readback == build_default_newsroom_card_placement_render_smoke_result_readback(
        root=ROOT
    )
    assert readback["artifact_id"] == CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_ID
    assert readback["readback_id"] == CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_ID
    assert readback["schema_version"] == (
        CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION
    )
    assert readback["review_status"] == "ready_for_supervisor_review"
    assert readback["production_status"] == "diagnostic_only"
    assert readback["observation_source"] == "user_freeform_with_screenshot_support"
    assert readback["result_status"] == "pass"
    assert readback["diagnostic_only"] is True


def test_source_validation_reuses_card_placement_and_timing_evidence() -> None:
    validation = _readback()["source_validation"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["source_card_placement_probe_status"] == "placed_structurally"
    assert validation["source_timing_patch_render_result"] == "pass"
    assert validation["prior_duration_sec"] == 68
    assert validation["prior_native_audio_present"] is True
    assert validation["card_asset_count"] == 4
    assert validation["render_output_exists_at_generation"] is True
    assert validation["card_placement_ymmp_exists_at_generation"] is True
    assert validation["canonical_speaker_unicode_escape"] == (
        "\\u3086\\u3063\\u304f\\u308a\\u970a\\u5922"
    )


def test_normalized_render_result_records_card_placement_smoke_pass() -> None:
    result = _readback()["normalized_render_result"]

    assert result["render_smoke_result"] == "pass"
    assert result["yym4_opened_card_placement_project"] is True
    assert result["render_completed"] is True
    assert result["output_video_observed"] is True
    assert result["output_filename_observed"] == (
        "diagnostic_bound_speaker_probe_card_placement_v1.mp4"
    )
    assert result["output_duration_observed"] == "00:01:08"
    assert result["output_duration_sec"] == 68
    assert result["expected_duration_sec"] == 68
    assert result["duration_matches_timing_patch"] is True
    assert result["render_time_approx_sec"] == 30
    assert result["card_assets_visible"] is True
    assert result["card_count_visible"] == 4
    assert result["dialogue_items_visible"] is True
    assert result["dialogue_item_count_observed"] == 4
    assert result["visual_card_integrity"] == "pass"
    assert result["timing_preservation_regression_reported"] is False
    assert result["native_audio_regression_reported"] is False
    assert result["card_placement_effective_in_render"] is True
    assert result["production_visual_quality_accepted"] is False
    assert result["production_pacing_accepted"] is False
    assert result["public_video_ready"] is False


def test_card_observations_preserve_four_fake_review_only_cards() -> None:
    rows = _readback()["screenshot_supported_card_observations"]

    assert len(rows) == 4
    assert [row["card_index"] for row in rows] == [1, 2, 3, 4]
    assert all(row["visible_status"] is True for row in rows)
    assert all(row["observed_time_region"] == "unknown" for row in rows)
    assert all(row["visual_integrity"] == "pass" for row in rows)
    assert all("visual_card_" in row["expected_mapping_source"] for row in rows)
    assert all(
        row["notes"] == [
            "diagnostic fake/review-only card",
            "no real brand / URL / production claim",
        ]
        for row in rows
    )


def test_accepted_not_accepted_readiness_and_render_gate_are_separated() -> None:
    readback = _readback()
    readiness = readback["readiness_separation"]
    gate = readback["render_gate_carry_forward"]

    assert readback["accepted_scope"] == {
        "card_placement_ymmp_can_be_opened_and_rendered_in_current_yym4_environment": True,
        "output_remains_approximately_68_sec": True,
        "four_visual_card_assets_are_visible": True,
        "existing_dialogue_timeline_remains_visible": True,
        "no_obvious_visual_element_breakage_reported": True,
        "diagnostic_visual_placement_smoke_passes": True,
    }
    assert readback["not_accepted_scope"]["production_visual_quality"] is False
    assert readback["not_accepted_scope"]["public_video_readiness"] is False
    assert readback["not_accepted_scope"]["production_approval"] is False
    assert readiness["slice_completion"] == "pass_for_this_readback"
    assert readiness["video_readiness_progress"] == "6/7"
    assert readiness["visual_readiness_progress"] == "7/7"
    assert readiness["production_readiness"] == "low_diagnostic_only"
    assert readiness["next_default_slice"] == NEXT_DEFAULT_SLICE
    assert gate["current_render_observation_consumed_once"] is True
    assert gate["new_render_in_this_slice"] is False
    assert gate["YMM4_launched_by_agent"] is False
    assert gate["render_audio_or_tts_created_by_agent"] is False
    assert gate["repeated_timing_audio_render_or_card_check_requested"] is False


def test_next_slices_goal_stack_and_matrices_match_contract_counts() -> None:
    readback = _readback()

    assert [row["slice"] for row in readback["recommended_next_slices"]] == [
        NEXT_DEFAULT_SLICE,
        "newsroom-internal-review-v0.1-render-package-v1",
        "newsroom-render-output-retention-policy-v1",
        "newsroom-rss-dry-run-integration-plan-v1",
    ]
    assert readback["recommended_next_slices"][0]["timing"] == (
        "recommended_next_default"
    )
    assert [row["level"] for row in readback["goal_stack"]] == [
        "Immediate",
        "Short-term",
        "Mid-term",
        "Long-term",
    ]
    assert len(readback["completion_matrix"]) == 6
    assert len(readback["artifact_readiness"]) == 6
    assert len(readback["video_readiness"]) == 7
    assert len(readback["visual_readiness"]) == 7
    assert len(readback["render_gate_hygiene"]) == 6
    assert len(readback["human_burden_hygiene"]) == 7
    assert len(readback["review_non_redundancy"]) == 6
    assert len(readback["inertia_check"]) == 5
    assert readback["inertia_check"][-1] == {
        "gate": "next_concrete_milestone",
        "status": NEXT_DEFAULT_SLICE,
    }


def test_local_render_and_ymmp_are_ignored_untracked_and_not_staged() -> None:
    local = _readback()["local_artifact_status"]

    assert RENDER_OUTPUT_PATH.exists()
    assert CARD_PLACEMENT_YMMP_PATH.exists()
    assert local["render_output_exists_at_readback_generation"] is True
    assert local["card_placement_ymmp_exists_at_readback_generation"] is True
    assert local["render_output_staged"] is False
    assert local["render_output_committed"] is False
    assert local["render_output_ignored"] is True
    assert local["card_placement_ymmp_staged"] is False
    assert local["card_placement_ymmp_committed"] is False
    assert local["card_placement_ymmp_ignored"] is True
    for rel_path in [
        DEFAULT_CARD_PLACEMENT_RENDER_OUTPUT_LOCAL_PATH.as_posix(),
        DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH.as_posix(),
    ]:
        status = subprocess.run(
            ["git", "status", "--short", "--", rel_path],
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
        assert status.stdout == ""
        assert ls_files.stdout == ""


def test_doc_matches_renderer_and_avoids_repeated_render_or_rigid_form_request() -> None:
    readback = _readback()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == (
        render_newsroom_card_placement_render_smoke_result_readback_markdown(readback)
    )
    assert "result_status: pass" in doc_text
    assert "output_duration_sec: 68" in doc_text
    assert "visual_readiness_progress: 7/7" in doc_text
    assert NEXT_DEFAULT_SLICE in doc_text
    assert ("yes/no" + "/unclear") not in doc_text.lower()
    assert "please render" not in doc_text.lower()
    assert "please check audio" not in doc_text.lower()
    assert ("fixed " + "form") not in doc_text.lower()
    assert _real_url_pattern().search(doc_text) is None


def test_readback_artifacts_have_no_real_urls_or_committed_media_outputs() -> None:
    readback_text = READBACK_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(readback_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert "production_approval\": true" not in readback_text
    assert "public_video_ready\": true" not in readback_text
    assert not list(READBACK_PATH.parent.glob("*card_placement_render_smoke*.ymmp"))
    assert not list(READBACK_PATH.parent.glob("*card_placement_render_smoke*.mp4"))
    assert not list(READBACK_PATH.parent.glob("*card_placement_render_smoke*.wav"))
    assert not list(READBACK_PATH.parent.glob("*card_placement_render_smoke*.mp3"))
    assert not list(READBACK_PATH.parent.glob("*card_placement_render_smoke*.m4a"))
