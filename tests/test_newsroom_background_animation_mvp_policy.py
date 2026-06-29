import json
from pathlib import Path

from src.pipeline.newsroom_background_animation_mvp_policy import (
    DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_DOC_PATH,
    DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_PATH,
    DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_DOC_PATH,
    DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH,
    DEFAULT_SCENE_PREVIEW_OBSERVATION_DOC_PATH,
    DEFAULT_SCENE_PREVIEW_OBSERVATION_PATH,
    NEXT_AXIS_MINIMAL_INTEGRATED_SCENE_PROBE,
    RETURN_AXIS_RSS_STORY_INTEGRATION,
    build_default_background_animation_integration_plan,
    build_default_background_animation_mvp_policy,
    build_default_scene_preview_observation,
    render_background_animation_integration_plan_markdown,
    render_background_animation_mvp_policy_markdown,
    render_scene_preview_observation_markdown,
    write_default_newsroom_background_animation_mvp_policy_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_background_animation_mvp_policy_artifacts(root=ROOT)


def test_scene_preview_observation_normalizes_stop_loss_trigger() -> None:
    _ensure_artifacts()
    payload = build_default_scene_preview_observation(root=ROOT)
    artifact = _load(DEFAULT_SCENE_PREVIEW_OBSERVATION_PATH)

    assert artifact == payload
    normalized = artifact["normalized_user_observation"]
    assert normalized["yym4_opened"] is True
    assert normalized["scene_choreography_probe_observed"] is True
    assert normalized["scene_coherence"] == "partial"
    assert normalized["primitive_feasibility"] == "pass"
    assert normalized["expression_change_visible"] is True
    assert normalized["nod_visible"] is True
    assert normalized["body_motion_default_should_stop"] is True
    assert normalized["unstable_motion_near_angry_expression"] == "warning"
    assert normalized["animation_quality_for_final"] == "not_accepted"
    assert normalized["primitive_tuning_loop_risk"] == "high"
    assert normalized["render_export_required_now"] is False
    assert normalized["next_axis"] == "stop_loss_and_integration_plan"
    assert artifact["stop_loss_trigger"]["decision"] == (
        "stop_primitive_only_tuning_and_plan_integrated_scene"
    )
    assert artifact["source_scene_choreography_probe_access"]["repo_relative_path"].endswith(
        "yukkuri_animation_scene_choreography_probe_v1.ymmp"
    )


def test_mvp_policy_defines_allowed_disabled_and_review_gate() -> None:
    _ensure_artifacts()
    payload = build_default_background_animation_mvp_policy(root=ROOT)
    artifact = _load(DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH)

    assert artifact == payload
    assert artifact["selected_next_axis"] == NEXT_AXIS_MINIMAL_INTEGRATED_SCENE_PROBE
    assert artifact["next_recommended_axis"]["fallback_if_bad"] == RETURN_AXIS_RSS_STORY_INTEGRATION

    stop_loss_rules = {row["rule_id"]: row for row in artifact["stop_loss_policy"]}
    assert "no_more_primitive_only_iteration" in stop_loss_rules
    assert "integrated scene proves a specific primitive is blocking" in stop_loss_rules[
        "no_more_primitive_only_iteration"
    ]["requirement"]
    assert "body_forward_back_disabled_by_default" in stop_loss_rules
    assert "next_proof_uses_actual_explanation_beat" in stop_loss_rules
    assert "freeze_animation_if_integrated_scene_fails" in stop_loss_rules

    allowed = {
        row["primitive_id"]: row["allowed_default"]
        for row in artifact["allowed_default_primitives"]
    }
    assert allowed == {
        "stable_pose": True,
        "one_expression_event": True,
        "one_short_nod_or_reaction": True,
        "small_lateral_emphasis": "optional",
    }

    disabled = {row["primitive_id"] for row in artifact["disabled_by_default"]}
    assert {
        "repeated_nodding",
        "mechanical_expression_cycling",
        "body_forward_back_movement",
        "complex_speech_balloons",
        "full_chaban_scene",
    } <= disabled

    gates = {row["gate_id"] for row in artifact["review_gate"]}
    assert gates == {
        "supports_explanation",
        "does_not_distract",
        "reduces_card_fatigue",
        "introduces_no_confusion",
    }
    assert artifact["business_goal_outcome_contract"]["visual_supports_explanation"]["status"] == (
        "unknown_until_integrated_preview"
    )


def test_integration_plan_is_minimal_scene_probe_not_primitive_demo() -> None:
    _ensure_artifacts()
    payload = build_default_background_animation_integration_plan(root=ROOT)
    artifact = _load(DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_PATH)

    assert artifact == payload
    assert artifact["selected_next_axis"] == NEXT_AXIS_MINIMAL_INTEGRATED_SCENE_PROBE

    spec = artifact["integrated_scene_probe_spec"]
    assert spec["duration_sec_range"] == {"min": 10, "max": 20}
    assert spec["content_rule"] == "one actual explanation beat, not a primitive demo"
    assert spec["line_status"] == "review_only_diagnostic_line"
    assert spec["animation_budget"]["expression_event_count"] == 1
    assert spec["animation_budget"]["nod_or_reaction_count"] == 1
    assert spec["animation_budget"]["body_forward_back_movement"] == "disabled_by_default"
    assert spec["animation_budget"]["speech_balloon"] == "deferred"
    assert spec["output_policy"]["planning_slice_creates_ymmp"] is False
    assert spec["output_policy"]["tracked_ymmp_allowed"] is False
    assert spec["output_policy"]["render_export_required"] is False
    assert spec["preview_policy"]["user_review_mode"] == "one_freeform_preview_only"
    assert artifact["failure_signal"]["return_axis"] == RETURN_AXIS_RSS_STORY_INTEGRATION


def test_markdown_outputs_match_renderers() -> None:
    _ensure_artifacts()
    observation = _load(DEFAULT_SCENE_PREVIEW_OBSERVATION_PATH)
    policy = _load(DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH)
    plan = _load(DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_PATH)

    assert (ROOT / DEFAULT_SCENE_PREVIEW_OBSERVATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_scene_preview_observation_markdown(observation)
    assert (ROOT / DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_background_animation_mvp_policy_markdown(policy)
    assert (ROOT / DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_background_animation_integration_plan_markdown(plan)


def test_outputs_do_not_request_render_or_media_artifacts() -> None:
    _ensure_artifacts()
    generated_paths = [
        ROOT / DEFAULT_SCENE_PREVIEW_OBSERVATION_PATH,
        ROOT / DEFAULT_SCENE_PREVIEW_OBSERVATION_DOC_PATH,
        ROOT / DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_PATH,
        ROOT / DEFAULT_BACKGROUND_ANIMATION_MVP_POLICY_DOC_PATH,
        ROOT / DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_PATH,
        ROOT / DEFAULT_BACKGROUND_ANIMATION_INTEGRATION_PLAN_DOC_PATH,
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

    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_paths)
