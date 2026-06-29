import json
from pathlib import Path

from src.pipeline.newsroom_background_animation_mvp_freeze import (
    ANIMATION_ACCENT_POLICY,
    DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_DOC_PATH,
    DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH,
    DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_DOC_PATH,
    DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_PATH,
    NEXT_AXIS_MAINLINE_PIPELINE,
    build_default_background_animation_mvp_freeze,
    build_default_minimal_integrated_scene_preview_observation,
    render_background_animation_mvp_freeze_markdown,
    render_minimal_integrated_scene_preview_observation_markdown,
    write_default_newsroom_background_animation_mvp_freeze_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_background_animation_mvp_freeze_artifacts(root=ROOT)


def test_preview_observation_normalizes_user_readback() -> None:
    _ensure_artifacts()
    payload = build_default_minimal_integrated_scene_preview_observation(root=ROOT)
    artifact = _load(DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_PATH)

    assert artifact == payload
    assert artifact["production_status"] == "diagnostic_only"
    assert artifact["render_gate"] == "L0_no_render"
    assert artifact["actual_audience_acceptance_claimed"] is False

    normalized = artifact["normalized_user_observation"]
    assert normalized == {
        "source_observation_role": "user_opened_minimal_integrated_scene_probe_preview",
        "source_probe_path": "_tmp/newsroom_manual_probe/background_animation_minimal_integrated_scene_probe_v1.ymmp",
        "yym4_opened": True,
        "minimal_integrated_scene_preview_observed": True,
        "expression_event_visible": True,
        "nod_after_expression_visible": True,
        "stable_pose_context": "not_negatively_reported",
        "body_forward_back_problem": "not_dominant_in_this_probe",
        "mvp_accent_layer_status": "accepted_with_boundary",
        "production_animation_quality": "not_accepted",
        "render_export_required_now": False,
        "next_axis": "animation_mvp_freeze_and_mainline_return",
    }
    assert artifact["local_probe_access"]["target_exists"] is True
    assert artifact["local_probe_access"]["access_state"] == "verified_present"
    assert artifact["mvp_acceptance_judgment"]["status"] == "accepted_with_boundary"
    assert artifact["mvp_acceptance_judgment"]["no_more_primitive_tuning"] is True


def test_mvp_freeze_closes_animation_loops_and_returns_mainline() -> None:
    _ensure_artifacts()
    payload = build_default_background_animation_mvp_freeze(root=ROOT)
    artifact = _load(DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH)

    assert artifact == payload
    decision = artifact["mvp_freeze_decision"]
    assert decision["status"] == "freeze_mvp_accent_layer"
    assert decision["mvp_accent_layer_status"] == "accepted_with_boundary"
    assert decision["primitive_loop_status"] == "closed"
    assert decision["animation_only_probe_loop_status"] == "closed"
    assert decision["tempo_only_probe_loop_status"] == "closed"
    assert decision["mainline_return_required"] is True

    policy = artifact["animation_accent_policy"]
    assert policy == ANIMATION_ACCENT_POLICY
    assert policy["policy_status"] == "frozen_for_mvp_accent_layer"
    assert policy["must_not_become_main_deliverable"] is True
    assert policy["allowed"] == [
        "stable_pose",
        "one_expression_event_tied_to_scene_beat",
        "one_short_nod_or_reaction_after_expression_event",
        "return_to_stable_pose",
    ]
    assert {
        "body_forward_back_movement",
        "repeated_nodding",
        "mechanical_expression_cycling",
        "speech_balloons",
        "full_chaban_scene",
        "animation_only_probe_loops",
        "tempo_only_probe_loops",
    } <= set(policy["disabled_by_default"])

    plan = artifact["mainline_return_plan"]
    assert plan["selected_next_axis"] == NEXT_AXIS_MAINLINE_PIPELINE
    assert plan["preferred_default"] == NEXT_AXIS_MAINLINE_PIPELINE
    assert {row["axis"] for row in plan["alternates"]} == {
        "newsroom-rss-dry-run-to-animated-explanation-beat-v1",
        "newsroom-animation-accent-policy-closed-return-to-episode-capsule-v1",
    }


def test_business_goal_contract_keeps_mvp_separate_from_production() -> None:
    _ensure_artifacts()
    artifact = _load(DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH)
    contract = artifact["business_goal_outcome_contract"]

    assert contract["problem_clear"]["status"] is True
    assert contract["offer_clear"]["status"] is True
    assert contract["proof_clear"]["status"] is True
    assert "production animation quality" in contract["proof_clear"]["rationale"]
    assert contract["boundary_clear"]["status"] is True
    assert contract["next_action_clear"]["rationale"] == NEXT_AXIS_MAINLINE_PIPELINE
    assert contract["visual_supports_explanation"]["status"] == "accepted_with_boundary"

    not_accepted = artifact["not_accepted_scope"]
    assert not_accepted["production_animation_quality"] is False
    assert not_accepted["render_proof"] is False
    assert not_accepted["public_upload_or_public_readiness"] is False
    assert not_accepted["full_chaban_scene"] is False
    assert not_accepted["animation_only_probe_loop"] is False
    assert not_accepted["tempo_only_probe_loop"] is False


def test_markdown_outputs_match_renderers() -> None:
    _ensure_artifacts()
    observation = _load(DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_PATH)
    freeze = _load(DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH)

    assert (ROOT / DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_minimal_integrated_scene_preview_observation_markdown(observation)
    assert (ROOT / DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_background_animation_mvp_freeze_markdown(freeze)


def test_outputs_do_not_request_render_or_new_probe_artifacts() -> None:
    _ensure_artifacts()
    generated_paths = [
        ROOT / DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_PATH,
        ROOT / DEFAULT_MINIMAL_INTEGRATED_SCENE_PREVIEW_OBSERVATION_DOC_PATH,
        ROOT / DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH,
        ROOT / DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_DOC_PATH,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in generated_paths)
    combined_lower = combined.lower()

    assert "http://" not in combined
    assert "https://" not in combined
    assert "www." not in combined
    assert "render again" not in combined_lower
    assert "launch ymm4 now" not in combined_lower
    assert "create audio" not in combined_lower
    assert "generate tts" not in combined_lower
    assert "create another animation-only" not in combined_lower
    assert "create another primitive" not in combined_lower

    tracked_forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in tracked_forbidden_suffixes for path in generated_paths)

    freeze = _load(DEFAULT_BACKGROUND_ANIMATION_MVP_FREEZE_PATH)
    assert freeze["boundaries"]["local_ignored_ymmp_created_in_this_slice"] is False
    assert freeze["boundaries"]["ymmp_or_media_staged_or_committed"] is False
