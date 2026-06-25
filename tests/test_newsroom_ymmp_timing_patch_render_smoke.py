import json
import re
import subprocess
from pathlib import Path

from src.pipeline.newsroom_ymmp_timing_patch_probe import DEFAULT_PATCHED_YMMP_LOCAL_PATH
from src.pipeline.newsroom_ymmp_timing_patch_render_smoke import (
    DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_DOC_PATH,
    DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_PATH,
    DIALOGUE_FAILURE_CLASSIFICATION,
    DURATION_FAILURE_CLASSIFICATION,
    EXPECTED_DURATION_TOLERANCE_SEC,
    NATIVE_AUDIO_FAILURE_CLASSIFICATION,
    NEXT_RESULT_READBACK_SLICE,
    NORMALIZATION_FIELD_NAMES,
    OBSERVATION_TARGETS,
    OPEN_FAILURE_CLASSIFICATION,
    OPERATOR_UNCERTAIN_CLASSIFICATION,
    PASS_CLASSIFICATION,
    RENDER_FAILURE_CLASSIFICATION,
    RENDER_FAILURE_CLASSIFICATION_SLICE,
    YMMP_TIMING_PATCH_RENDER_SMOKE_ID,
    YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION,
    YMMP_TIMING_PATCH_RENDER_SMOKE_SCHEMA_VERSION,
    build_default_newsroom_ymmp_timing_patch_render_smoke,
    build_newsroom_ymmp_timing_patch_render_smoke_result_readback,
    classify_render_smoke_observation,
    normalize_render_smoke_observation,
    render_newsroom_ymmp_timing_patch_render_smoke_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_PATH
DOC_PATH = ROOT / DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_DOC_PATH
PATCHED_YMMP_PATH = ROOT / DEFAULT_PATCHED_YMMP_LOCAL_PATH


def _package() -> dict:
    return json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))


def _pass_observation() -> dict:
    return {
        "patched_project_opened": True,
        "render_completed": True,
        "output_duration_observed_sec": 68,
        "duration_approximately_68_sec": True,
        "dialogue_items_preserved": True,
        "dialogue_item_count_observed": 4,
        "native_audio_present": True,
        "operator_notes": "opened and rendered; about 68 sec; four lines and voice remained",
    }


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_render_smoke_package_matches_builder_output() -> None:
    package = _package()

    assert package == build_default_newsroom_ymmp_timing_patch_render_smoke(root=ROOT)
    assert package["artifact_id"] == YMMP_TIMING_PATCH_RENDER_SMOKE_ID
    assert package["smoke_id"] == YMMP_TIMING_PATCH_RENDER_SMOKE_ID
    assert package["schema_version"] == YMMP_TIMING_PATCH_RENDER_SMOKE_SCHEMA_VERSION
    assert package["review_status"] == "ready_for_supervisor_review"
    assert package["production_status"] == "diagnostic_only"
    assert package["diagnostic_only"] is True
    assert package["smoke_status"] == "prepared_not_run"
    assert package["package_status"] == "ready_for_manual_milestone_render_smoke"


def test_source_validation_reuses_structural_patch_and_native_audio_readbacks() -> None:
    validation = _package()["source_validation"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["patch_method"] == (
        "neutral_timeline_skeleton_patch_with_native_voice_preserved"
    )
    assert validation["patched_ymmp_path"] == (
        "_tmp/newsroom_manual_probe/"
        "diagnostic_bound_speaker_probe_timing_patch_v1.ymmp"
    )
    assert validation["patched_ymmp_found_at_generation"] is True
    assert validation["patched_total_sec"] == 68.0
    assert validation["patched_total_frames"] == 4080
    assert validation["patched_dialogue_item_count"] == 4
    assert validation["native_voice_path_preserved"] is True
    assert validation["external_TTS_introduced"] is False
    assert validation["render_already_performed"] is False


def test_target_records_only_the_ignored_patched_ymmp_as_smoke_target() -> None:
    package = _package()
    target = package["target"]
    expected = target["expected_project_state"]

    assert target["patched_ymmp_path"] == str(DEFAULT_PATCHED_YMMP_LOCAL_PATH).replace(
        "\\", "/"
    )
    assert target["patched_ymmp_path_status"] == (
        "discoverable_local_file_at_generation_time"
    )
    assert target["git_tracking_policy"] == "ignored_under_tmp_do_not_stage_or_commit"
    assert target["ymmp_file_newly_modified_in_this_slice"] is False
    assert expected["fps"] == 60
    assert expected["total_frames"] == 4080
    assert expected["total_duration_sec"] == 68.0
    assert expected["dialogue_item_count"] == 4
    assert expected["item_frames"] == [0, 720, 1440, 2760]
    assert expected["item_lengths"] == [720, 720, 1320, 1320]
    assert expected["item_end_frames"] == [720, 1440, 2760, 4080]
    assert expected["native_audio_expected_from_preserved_yym4_fields"] is True


def test_patched_ymmp_target_is_present_ignored_and_untracked() -> None:
    rel_path = DEFAULT_PATCHED_YMMP_LOCAL_PATH.as_posix()
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

    assert PATCHED_YMMP_PATH.exists()
    assert check_ignore.returncode == 0
    assert "_tmp/" in check_ignore.stdout
    assert ls_files.stdout == ""
    assert status.stdout == ""


def test_operator_observation_card_keeps_the_five_required_targets_minimal() -> None:
    package = _package()
    card = package["operator_observation_card"]
    hygiene = package["human_burden_hygiene"]

    assert card["status"] == "required_next_milestone"
    assert card["target"] == "patched diagnostic .ymmp render smoke"
    assert card["patched_ymmp_path"] == str(DEFAULT_PATCHED_YMMP_LOCAL_PATH).replace(
        "\\", "/"
    )
    assert card["answer_style"] == "freeform"
    assert card["look_for"] == list(OBSERVATION_TARGETS)
    assert len(card["look_for"]) == 5
    assert "fixed form" in card["not_needed"]
    assert hygiene["user_input"] == "freeform"
    assert hygiene["template_required"] is False
    assert hygiene["schema_owner"] == "Agent"
    assert hygiene["required_observation_target_count"] == 5
    assert hygiene["observation_targets_are_minimal"] is True
    assert hygiene["fixed_form_result_template"] is False


def test_normalization_schema_is_agent_owned_and_matches_required_fields() -> None:
    schema = _package()["result_normalization_schema"]
    fields = [row["field"] for row in schema["fields"]]

    assert schema["schema_owner"] == "Agent"
    assert schema["user_must_fill_schema"] is False
    assert schema["normalization_source"] == "future freeform operator observation"
    assert schema["duration_tolerance_sec"] == EXPECTED_DURATION_TOLERANCE_SEC
    assert fields == list(NORMALIZATION_FIELD_NAMES)


def test_classification_matrix_covers_success_and_each_required_failure_axis() -> None:
    matrix = _package()["success_failure_classification_matrix"]

    assert [row["classification"] for row in matrix] == [
        PASS_CLASSIFICATION,
        OPEN_FAILURE_CLASSIFICATION,
        RENDER_FAILURE_CLASSIFICATION,
        DURATION_FAILURE_CLASSIFICATION,
        DIALOGUE_FAILURE_CLASSIFICATION,
        NATIVE_AUDIO_FAILURE_CLASSIFICATION,
        OPERATOR_UNCERTAIN_CLASSIFICATION,
    ]
    assert matrix[0]["trigger"] == "all five observation targets are true"
    assert matrix[0]["next_recommended_slice"] == NEXT_RESULT_READBACK_SLICE
    assert all(
        row["next_recommended_slice"] == RENDER_FAILURE_CLASSIFICATION_SLICE
        for row in matrix[1:6]
    )


def test_classifier_accepts_pass_and_duration_tolerance_from_observed_seconds() -> None:
    direct = classify_render_smoke_observation(_pass_observation())
    inferred = classify_render_smoke_observation(
        {
            "patched_project_opened": True,
            "render_completed": True,
            "output_duration_observed_sec": 69.9,
            "dialogue_items_preserved": True,
            "dialogue_item_count_observed": 4,
            "native_audio_present": True,
        }
    )

    assert direct["classification"] == PASS_CLASSIFICATION
    assert direct["result"] == "pass"
    assert direct["next_recommended_slice"] == NEXT_RESULT_READBACK_SLICE
    assert inferred["classification"] == PASS_CLASSIFICATION


def test_classifier_routes_first_blocking_failure_axis() -> None:
    open_fail = _pass_observation() | {"patched_project_opened": False}
    render_fail = _pass_observation() | {"render_completed": False}
    duration_fail = _pass_observation() | {
        "duration_approximately_68_sec": False,
        "output_duration_observed_sec": 8,
    }
    dialogue_fail = _pass_observation() | {"dialogue_item_count_observed": 3}
    audio_fail = _pass_observation() | {"native_audio_present": False}
    uncertain = _pass_observation() | {"native_audio_present": "unknown"}

    assert classify_render_smoke_observation(open_fail)["classification"] == (
        OPEN_FAILURE_CLASSIFICATION
    )
    assert classify_render_smoke_observation(render_fail)["classification"] == (
        RENDER_FAILURE_CLASSIFICATION
    )
    assert classify_render_smoke_observation(duration_fail)["classification"] == (
        DURATION_FAILURE_CLASSIFICATION
    )
    assert classify_render_smoke_observation(dialogue_fail)["classification"] == (
        DIALOGUE_FAILURE_CLASSIFICATION
    )
    assert classify_render_smoke_observation(audio_fail)["classification"] == (
        NATIVE_AUDIO_FAILURE_CLASSIFICATION
    )
    assert classify_render_smoke_observation(uncertain)["classification"] == (
        OPERATOR_UNCERTAIN_CLASSIFICATION
    )


def test_render_readback_builder_normalizes_future_observation_without_media_commit() -> None:
    package = _package()
    readback = build_newsroom_ymmp_timing_patch_render_smoke_result_readback(
        package,
        _pass_observation(),
        source_package_path=DEFAULT_YMMP_TIMING_PATCH_RENDER_SMOKE_PATH,
    )

    assert readback["schema_version"] == (
        YMMP_TIMING_PATCH_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION
    )
    assert readback["source_validation"]["status"] == "passed"
    assert readback["normalized_result"]["classification"] == PASS_CLASSIFICATION
    assert readback["classification"]["result"] == "pass"
    assert readback["accepted_scope"] == {
        "patched_project_opened": True,
        "render_completed": True,
        "diagnostic_output_about_68_sec": True,
        "dialogue_items_preserved": True,
        "native_audio_present": True,
        "production_ready": False,
        "public_video_ready": False,
    }
    assert readback["boundaries"]["YMM4_launched_by_agent"] is False
    assert readback["boundaries"]["render_created_by_agent"] is False
    assert readback["boundaries"]["ymmp_or_media_staged_or_committed"] is False


def test_normalize_observation_computes_duration_and_dialogue_count_failures() -> None:
    normalized_duration = normalize_render_smoke_observation(
        _pass_observation()
        | {
            "duration_approximately_68_sec": "unknown",
            "output_duration_observed_sec": 65.9,
        }
    )
    normalized_dialogue = normalize_render_smoke_observation(
        _pass_observation() | {"dialogue_item_count_observed": 2}
    )

    assert normalized_duration["duration_approximately_68_sec"] is False
    assert normalized_duration["classification"] == DURATION_FAILURE_CLASSIFICATION
    assert normalized_duration["result"] == "fail"
    assert normalized_dialogue["dialogue_items_preserved"] is False
    assert normalized_dialogue["classification"] == DIALOGUE_FAILURE_CLASSIFICATION


def test_gate_boundaries_keep_render_and_timing_strategy_out_of_this_slice() -> None:
    package = _package()
    gate = package["milestone_render_gate"]

    assert gate["gate_type"] == "milestone_gated_verification"
    assert gate["render_performed_in_this_slice"] is False
    assert gate["YMM4_launched_by_agent"] is False
    assert gate["manual_render_allowed_next"] is True
    assert gate["manual_render_count"] == 1
    assert gate["timing_strategy_change_allowed"] is False
    assert gate["external_TTS_allowed"] is False
    assert gate["render_output_commit_allowed"] is False
    assert gate["ymmp_commit_allowed"] is False
    assert package["boundaries"]["timing_strategy_changed"] is False
    assert package["boundaries"]["render_output_staged_or_committed"] is False
    assert package["not_accepted_scope"]["production_render_readiness"] is False
    assert package["not_accepted_scope"]["render_smoke_result"] is False


def test_doc_matches_renderer_and_names_the_minimal_observation_package() -> None:
    package = _package()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_ymmp_timing_patch_render_smoke_markdown(
        package
    )
    assert "package_status: ready_for_manual_milestone_render_smoke" in doc_text
    assert "patched_ymmp_path: _tmp/newsroom_manual_probe" in doc_text
    assert "output duration is approximately 68 seconds" in doc_text
    assert "Success / Failure Classification Matrix" in doc_text
    assert "build_newsroom_ymmp_timing_patch_render_smoke_result_readback" in doc_text
    assert "result: pass / fail" not in doc_text
    assert "fixed form result template" not in doc_text.lower()


def test_render_smoke_artifacts_have_no_real_urls_or_media_outputs() -> None:
    package_text = PACKAGE_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(package_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert not list(PACKAGE_PATH.parent.glob("*ymmp_timing_patch_render_smoke*.ymmp"))
    assert not list(PACKAGE_PATH.parent.glob("*ymmp_timing_patch_render_smoke*.mp4"))
    assert not list(PACKAGE_PATH.parent.glob("*ymmp_timing_patch_render_smoke*.wav"))
    assert not list(PACKAGE_PATH.parent.glob("*ymmp_timing_patch_render_smoke*.mp3"))
    assert not list(PACKAGE_PATH.parent.glob("*ymmp_timing_patch_render_smoke*.m4a"))
