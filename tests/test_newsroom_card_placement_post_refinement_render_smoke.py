import json
import re
import subprocess
from pathlib import Path

from src.pipeline.newsroom_card_placement_post_refinement_render_smoke import (
    CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_ID,
    CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION,
    CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_SCHEMA_VERSION,
    CARD_VISIBILITY_FAILURE_CLASSIFICATION,
    DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_DOC_PATH,
    DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_PATH,
    DEFAULT_POST_REFINEMENT_RENDER_OUTPUT_LOCAL_PATH,
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
    READABILITY_FAILURE_CLASSIFICATION,
    RENDER_FAILURE_CLASSIFICATION,
    RENDER_FAILURE_CLASSIFICATION_SLICE,
    build_default_newsroom_card_placement_post_refinement_render_smoke,
    build_newsroom_card_placement_post_refinement_render_smoke_result_readback,
    classify_render_smoke_observation,
    normalize_render_smoke_observation,
    render_newsroom_card_placement_post_refinement_render_smoke_markdown,
)
from src.pipeline.newsroom_yym4_card_asset_placement_probe import (
    DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_PATH
DOC_PATH = ROOT / DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_DOC_PATH
TARGET_YMMP_PATH = ROOT / DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH
POST_REFINEMENT_OUTPUT_PATH = ROOT / DEFAULT_POST_REFINEMENT_RENDER_OUTPUT_LOCAL_PATH


def _package() -> dict:
    return json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))


def _pass_observation() -> dict:
    return {
        "placement_project_opened": True,
        "render_completed": True,
        "output_duration_observed_sec": 68,
        "duration_approximately_68_sec": True,
        "refined_card_assets_visible": True,
        "card_count_observed": 4,
        "no_obvious_text_clipping_or_readability_breakage": True,
        "dialogue_items_preserved": True,
        "dialogue_item_count_observed": 4,
        "native_audio_present": True,
        "operator_notes": (
            "opened and rendered; about 68 sec; refined cards readable; "
            "dialogue and native voice remained"
        ),
    }


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_post_refinement_render_smoke_package_matches_builder_output() -> None:
    package = _package()

    assert package == build_default_newsroom_card_placement_post_refinement_render_smoke(
        root=ROOT
    )
    assert package["artifact_id"] == CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_ID
    assert package["smoke_id"] == CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_ID
    assert package["schema_version"] == (
        CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_SCHEMA_VERSION
    )
    assert package["review_status"] == "ready_for_supervisor_review"
    assert package["production_status"] == "diagnostic_only"
    assert package["diagnostic_only"] is True
    assert package["smoke_status"] == "prepared_not_run"
    assert package["package_status"] == "ready_for_manual_milestone_render_smoke"


def test_source_validation_confirms_refined_pngs_are_reused_by_ignored_ymmp() -> None:
    validation = _package()["source_validation"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["source_refinement_status"] == "assets_regenerated"
    assert validation["source_placement_probe_status"] == "placed_structurally"
    assert validation["source_prior_render_result"] == "pass"
    assert validation["prior_render_duration_sec"] == 68
    assert validation["prior_render_card_count_visible"] == 4
    assert validation["refined_card_count"] == 4
    assert validation["target_ymmp_card_image_item_count"] == 4
    assert validation["target_ymmp_reuses_refined_png_paths"] is True
    assert validation["target_ymmp_found_at_generation"] is True
    assert validation["target_ymmp_ignored"] is True
    assert validation["target_ymmp_committed"] is False
    assert validation["target_ymmp_staged"] is False
    assert all(path.endswith(".png") for path in validation["refined_png_paths"])


def test_target_records_stable_refined_cards_without_mutating_ymmp() -> None:
    package = _package()
    target = package["target"]
    cards = target["expected_refined_cards"]

    assert target["target_card_placement_ymmp_path"] == (
        DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH.as_posix()
    )
    assert target["target_ymmp_path_status"] == (
        "discoverable_local_file_at_generation_time"
    )
    assert target["git_tracking_policy"] == "ignored_under_tmp_do_not_stage_or_commit"
    assert target["ymmp_file_newly_modified_in_this_slice"] is False
    assert target["post_refinement_render_output_path"] == (
        DEFAULT_POST_REFINEMENT_RENDER_OUTPUT_LOCAL_PATH.as_posix()
    )
    assert target["render_output_commit_allowed"] is False
    assert target["expected_duration_sec"] == 68
    assert target["expected_card_count"] == 4
    assert target["expected_dialogue_item_count"] == 4
    assert len(cards) == 4
    assert [row["role"] for row in cards] == [
        "intro_summary",
        "handoff_process",
        "claim_check",
        "source_status_next_action",
    ]
    assert all(row["ymmp_path_reused"] is True for row in cards)
    assert all(row["text_wrap_applied"] is True for row in cards)
    assert all(row["clipping_guard"] is True for row in cards)


def test_ignored_ymmp_target_is_present_untracked_and_not_staged() -> None:
    rel_path = DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH.as_posix()
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

    assert TARGET_YMMP_PATH.exists()
    assert check_ignore.returncode == 0
    assert "_tmp/" in check_ignore.stdout
    assert ls_files.stdout == ""
    assert status.stdout == ""


def test_operator_observation_card_is_freeform_and_minimal() -> None:
    package = _package()
    card = package["operator_observation_card"]
    hygiene = package["human_burden_hygiene"]

    assert card["status"] == "required_next_milestone"
    assert card["target"] == "post-refinement card-placement diagnostic render smoke"
    assert card["target_ymmp_path"] == DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH.as_posix()
    assert card["output_path"] == (
        DEFAULT_POST_REFINEMENT_RENDER_OUTPUT_LOCAL_PATH.as_posix()
    )
    assert card["answer_style"] == "freeform"
    assert card["look_for"] == list(OBSERVATION_TARGETS)
    assert len(card["look_for"]) == 5
    assert "fixed form" in card["not_needed"]
    assert hygiene[0] == {"gate": "user_input", "status": "freeform"}
    assert {"gate": "template_required", "status": False} in hygiene
    assert {"gate": "schema_owner", "status": "Agent"} in hygiene
    assert {"gate": "fixed_form_relapse", "status": False} in hygiene


def test_normalization_schema_is_agent_owned_and_matches_required_fields() -> None:
    schema = _package()["result_normalization_schema"]
    fields = [row["field"] for row in schema["fields"]]

    assert schema["schema_owner"] == "Agent"
    assert schema["user_must_fill_schema"] is False
    assert schema["normalization_source"] == "future freeform operator observation"
    assert schema["duration_tolerance_sec"] == EXPECTED_DURATION_TOLERANCE_SEC
    assert fields == list(NORMALIZATION_FIELD_NAMES)


def test_classification_matrix_covers_success_and_each_failure_axis() -> None:
    matrix = _package()["success_failure_classification_matrix"]

    assert [row["classification"] for row in matrix] == [
        PASS_CLASSIFICATION,
        OPEN_FAILURE_CLASSIFICATION,
        RENDER_FAILURE_CLASSIFICATION,
        DURATION_FAILURE_CLASSIFICATION,
        CARD_VISIBILITY_FAILURE_CLASSIFICATION,
        READABILITY_FAILURE_CLASSIFICATION,
        DIALOGUE_FAILURE_CLASSIFICATION,
        NATIVE_AUDIO_FAILURE_CLASSIFICATION,
        OPERATOR_UNCERTAIN_CLASSIFICATION,
    ]
    assert matrix[0]["trigger"] == "all post-refinement observation targets are true"
    assert matrix[0]["next_recommended_slice"] == NEXT_RESULT_READBACK_SLICE
    assert all(
        row["next_recommended_slice"] == RENDER_FAILURE_CLASSIFICATION_SLICE
        for row in matrix[1:8]
    )


def test_classifier_accepts_pass_and_routes_first_blocking_failure_axis() -> None:
    open_fail = _pass_observation() | {"placement_project_opened": False}
    render_fail = _pass_observation() | {"render_completed": False}
    duration_fail = _pass_observation() | {
        "duration_approximately_68_sec": False,
        "output_duration_observed_sec": 8,
    }
    card_fail = _pass_observation() | {"card_count_observed": 3}
    readability_fail = _pass_observation() | {
        "no_obvious_text_clipping_or_readability_breakage": False
    }
    dialogue_fail = _pass_observation() | {"dialogue_item_count_observed": 2}
    audio_fail = _pass_observation() | {"native_audio_present": False}
    uncertain = _pass_observation() | {"native_audio_present": "unknown"}

    assert classify_render_smoke_observation(_pass_observation())["classification"] == (
        PASS_CLASSIFICATION
    )
    assert classify_render_smoke_observation(open_fail)["classification"] == (
        OPEN_FAILURE_CLASSIFICATION
    )
    assert classify_render_smoke_observation(render_fail)["classification"] == (
        RENDER_FAILURE_CLASSIFICATION
    )
    assert classify_render_smoke_observation(duration_fail)["classification"] == (
        DURATION_FAILURE_CLASSIFICATION
    )
    assert classify_render_smoke_observation(card_fail)["classification"] == (
        CARD_VISIBILITY_FAILURE_CLASSIFICATION
    )
    assert classify_render_smoke_observation(readability_fail)["classification"] == (
        READABILITY_FAILURE_CLASSIFICATION
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


def test_normalize_observation_computes_duration_and_count_failures() -> None:
    normalized_duration = normalize_render_smoke_observation(
        _pass_observation()
        | {
            "duration_approximately_68_sec": "unknown",
            "output_duration_observed_sec": 65.9,
        }
    )
    normalized_cards = normalize_render_smoke_observation(
        _pass_observation() | {"card_count_observed": 2}
    )

    assert normalized_duration["duration_approximately_68_sec"] is False
    assert normalized_duration["classification"] == DURATION_FAILURE_CLASSIFICATION
    assert normalized_duration["result"] == "fail"
    assert normalized_cards["refined_card_assets_visible"] is False
    assert normalized_cards["classification"] == CARD_VISIBILITY_FAILURE_CLASSIFICATION


def test_render_readback_builder_normalizes_future_observation_without_media_commit() -> None:
    package = _package()
    readback = build_newsroom_card_placement_post_refinement_render_smoke_result_readback(
        package,
        _pass_observation(),
        source_package_path=(
            DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_PATH
        ),
    )

    assert readback["schema_version"] == (
        CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION
    )
    assert readback["source_validation"]["status"] == "passed"
    assert readback["normalized_result"]["classification"] == PASS_CLASSIFICATION
    assert readback["classification"]["result"] == "pass"
    assert readback["accepted_scope"] == {
        "post_refinement_project_opened": True,
        "render_completed": True,
        "diagnostic_output_about_68_sec": True,
        "four_refined_cards_visible_and_readable": True,
        "dialogue_items_preserved": True,
        "native_audio_present": True,
        "production_ready": False,
        "public_video_ready": False,
    }
    assert readback["boundaries"]["YMM4_launched_by_agent"] is False
    assert readback["boundaries"]["video_render_created_by_agent"] is False
    assert readback["boundaries"]["ymmp_or_media_staged_or_committed"] is False


def test_gate_boundaries_keep_render_audio_and_ymmp_edits_out_of_this_slice() -> None:
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
    assert package["boundaries"]["ymmp_edited_by_agent"] is False
    assert package["boundaries"]["render_output_staged_or_committed"] is False
    assert package["not_accepted_scope"]["post_refinement_render_proof"] is False


def test_doc_matches_renderer_and_names_post_refinement_package() -> None:
    package = _package()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == (
        render_newsroom_card_placement_post_refinement_render_smoke_markdown(
            package
        )
    )
    assert "package_status: ready_for_manual_milestone_render_smoke" in doc_text
    assert "post-refinement card-placement diagnostic render smoke" in doc_text
    assert DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH.as_posix() in doc_text
    assert DEFAULT_POST_REFINEMENT_RENDER_OUTPUT_LOCAL_PATH.as_posix() in doc_text
    assert "four refined PNG cards are visible" in doc_text
    assert NEXT_RESULT_READBACK_SLICE in doc_text
    assert "result: pass / fail" not in doc_text
    assert "fixed form result template" not in doc_text.lower()
    assert _real_url_pattern().search(doc_text) is None


def test_artifacts_have_no_real_urls_or_media_outputs() -> None:
    package_text = PACKAGE_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(package_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert "production_approval\": true" not in package_text
    assert "public_video_ready\": true" not in package_text
    assert not POST_REFINEMENT_OUTPUT_PATH.exists()
    assert not list(PACKAGE_PATH.parent.glob("*post_refinement_render_smoke*.ymmp"))
    assert not list(PACKAGE_PATH.parent.glob("*post_refinement_render_smoke*.mp4"))
    assert not list(PACKAGE_PATH.parent.glob("*post_refinement_render_smoke*.wav"))
    assert not list(PACKAGE_PATH.parent.glob("*post_refinement_render_smoke*.mp3"))
    assert not list(PACKAGE_PATH.parent.glob("*post_refinement_render_smoke*.m4a"))
