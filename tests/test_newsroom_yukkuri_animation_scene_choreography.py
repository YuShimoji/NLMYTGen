import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_yukkuri_animation_scene_choreography import (
    DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_DOC_PATH,
    DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_PATH,
    DEFAULT_SCENE_CHOREOGRAPHY_PROBE_PATH,
    DEFAULT_V4_SWEEP_OBSERVATION_DOC_PATH,
    DEFAULT_V4_SWEEP_OBSERVATION_PATH,
    LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH,
    NEXT_AXIS_SCENE_PREVIEW,
    SCENE_BEAT_MAPPING,
    SCENE_TIMELINE_LENGTH_FRAMES,
    build_default_scene_choreography_contract,
    build_default_scene_choreography_probe_readback,
    build_default_v4_sweep_observation,
    materialize_local_scene_choreography_probe,
    render_scene_choreography_contract_markdown,
    render_v4_sweep_observation_markdown,
    write_default_newsroom_yukkuri_animation_scene_choreography_artifacts,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_yukkuri_animation_scene_choreography_artifacts(root=ROOT)


def test_v4_observation_exits_tempo_only_loop() -> None:
    _ensure_artifacts()
    payload = build_default_v4_sweep_observation(root=ROOT)
    artifact = _load(DEFAULT_V4_SWEEP_OBSERVATION_PATH)

    assert artifact == payload
    normalized = artifact["normalized_user_observation"]
    assert normalized["yym4_opened"] is True
    assert normalized["v4_preview_observed"] is True
    assert normalized["default_tempo_band"] == "0.75s"
    assert normalized["default_frame_span_at_60fps"] == 45
    assert normalized["scene_dependency"] is True
    assert normalized["one_second_status"] == "acceptable_variant_for_slower_explanatory_or_readability_heavy_moments"
    assert normalized["half_second_status"] == "acceptable_variant_for_quick_reaction_punch_or_small_emphasis"
    assert normalized["one_point_five_second_status"] == "not_selected_as_default_upper_comparison_or_special_slow_case_only"
    assert normalized["tempo_loop_exit"] is True
    assert normalized["primitive_only_loop_exit"] is True
    assert normalized["next_axis"] == NEXT_AXIS_SCENE_PREVIEW
    assert normalized["render_export_required_now"] is False
    assert normalized["production_public_render_approval_given"] is False
    assert artifact["user_observation_notes"] == [
        "0.75s looks the most natural.",
        "However, the best duration depends on the scene.",
        "1.0s is also within acceptable range.",
        "0.5s is also within acceptable range.",
        "No production/public/render approval was given.",
    ]
    assert artifact["tempo_default_policy"]["default_tempo_band"] == "0.75s"
    assert artifact["tempo_default_policy"]["default_frame_span_at_60fps"] == 45
    assert artifact["render_gate"] == "L0_no_render"


def test_scene_choreography_contract_has_required_beat_fields() -> None:
    _ensure_artifacts()
    payload = build_default_scene_choreography_contract(root=ROOT)
    artifact = _load(DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_PATH)

    assert artifact == payload
    assert artifact["scene_probe_materialization_status"] == "materialized_ignored_local_probe"
    assert artifact["selected_next_axis"] == NEXT_AXIS_SCENE_PREVIEW
    assert artifact["tempo_default_policy"]["status"] == "active_for_scene_beat_integration"
    assert artifact["tempo_default_policy"]["scene_dependency"] is True
    assert artifact["tempo_default_policy"]["default_tempo_band"] == "0.75s"
    assert artifact["tempo_default_policy"]["default_frame_span_at_60fps"] == 45
    assert artifact["tempo_default_policy"]["use_case_policy"] == [
        {
            "use_case": "default light reenactment beat",
            "tempo": "0.75s",
            "frames_at_60fps": 45,
            "note": "user-selected most natural",
        },
        {
            "use_case": "quick reaction / punch / short emphasis",
            "tempo": "0.5s",
            "frames_at_60fps": 30,
            "note": "acceptable but use selectively",
        },
        {
            "use_case": "explanatory / readable / calmer beat",
            "tempo": "1.0s",
            "frames_at_60fps": 60,
            "note": "acceptable, useful when readability matters",
        },
        {
            "use_case": "slow upper comparison",
            "tempo": "1.5s",
            "frames_at_60fps": 90,
            "note": "not default; contrast or special slow scene only",
        },
    ]
    assert artifact["provisional_tempo_policy"] == {
        "default_reaction_motion": "45 frames / 0.75s",
        "quick_reaction_or_punch": "30 frames / 0.5s",
        "readability_heavy_or_calm_explanation": "60 frames / 1.0s",
        "slow_upper_comparison": "90 frames / 1.5s",
        "scene_dependency": True,
        "status": "superseded_by_tempo_default_policy",
    }
    assert artifact["scene_beat_integration_risks"] == [
        {
            "risk_id": "primitive_only_tempo_loop",
            "status": "exited",
            "mitigation": "use the tempo policy inside an actual scene/beat structure",
        },
        {
            "risk_id": "scene_dependent_timing",
            "status": "active",
            "mitigation": "select 0.5s, 0.75s, or 1.0s by beat function instead of forcing one global value",
        },
        {
            "risk_id": "slow_upper_bound_overuse",
            "status": "guarded",
            "mitigation": "do not use 1.5s as default; reserve it for contrast or a specific slow scene",
        },
    ]

    required_keys = {
        "scene_id",
        "scene_function",
        "beat_id",
        "viewer_information_goal",
        "character_state_before",
        "motion_reason",
        "primitive_used",
        "expression_reason",
        "facing_policy",
        "anchor_policy",
        "active_motion_span",
        "hold_span",
        "transition_policy",
        "forbidden_motion",
        "fallback_if_primitive_unavailable",
    }
    assert len(artifact["scene_beat_mapping"]) == len(SCENE_BEAT_MAPPING)
    for row in artifact["scene_beat_mapping"]:
        assert required_keys <= set(row)
        assert row["motion_reason"]
        assert row["expression_reason"]
        assert row["active_motion_span"] <= 60
        assert row["hold_span"] >= 120


def test_scene_probe_materializes_ignored_local_ymmp() -> None:
    _ensure_artifacts()
    payload = build_default_scene_choreography_probe_readback(root=ROOT)
    artifact = _load(DEFAULT_SCENE_CHOREOGRAPHY_PROBE_PATH)

    assert artifact == payload
    assert artifact["scene_probe_materialization_status"] == "materialized_ignored_local_probe"
    access = artifact["scene_probe_access"]
    assert access["repo_relative_path"] == LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH.as_posix()
    assert access["target_exists"] is True
    assert access["access_state"] == "verified_present"
    assert access["access_evidence_level"] == "L3_VERIFIED_PRESENT"
    assert access["artifact_scope"] == "ignored_local_only"
    assert access["git_check_ignore_result"]["ignored"] is True
    assert (ROOT / LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH).exists()

    result = subprocess.run(
        ["git", "check-ignore", "-v", "--", LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH.as_posix()],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "_tmp/" in result.stdout


def test_scene_probe_readback_is_choreography_not_speed_sweep() -> None:
    _ensure_artifacts()
    artifact = _load(DEFAULT_SCENE_CHOREOGRAPHY_PROBE_PATH)
    readback = artifact["scene_probe_readback"]

    assert readback["readback_status"] == "structural_pass"
    assert readback["timeline"]["fps"] == 60
    assert readback["timeline"]["length_frames"] == SCENE_TIMELINE_LENGTH_FRAMES
    assert readback["timeline"]["length_sec"] == 18.0
    assert readback["timeline"]["item_type_counts"] == {
        "GroupItem": 16,
        "ImageItem": 16,
    }
    assert readback["timeline"]["unexpected_item_types"] == []
    assert readback["segment_count"] == 8

    semantic = readback["semantic_checks"]
    assert semantic["status"] == "pass"
    assert semantic["nod_beats"] == ["beat_c_one_short_ack_nod"]
    assert semantic["moving_beats"] == ["beat_e_one_small_intentional_nudge"]
    assert semantic["expression_change_beats"] == [
        "beat_b_question_reaction_cue",
        "beat_d_reasoned_expression_shift",
        "beat_f_stable_explanation_pose",
    ]
    assert all(semantic["checks"].values())

    probe = load_ymmp(ROOT / LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH)
    assert {_item_type(item) for item in _get_timeline_items(probe)} == {
        "GroupItem",
        "ImageItem",
    }


def test_scene_materializer_can_be_called_directly() -> None:
    materialize_local_scene_choreography_probe(root=ROOT)
    assert (ROOT / LOCAL_IGNORED_SCENE_CHOREOGRAPHY_PROBE_PATH).exists()


def test_markdown_outputs_match_renderers() -> None:
    _ensure_artifacts()
    observation = _load(DEFAULT_V4_SWEEP_OBSERVATION_PATH)
    contract = _load(DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_PATH)

    assert (ROOT / DEFAULT_V4_SWEEP_OBSERVATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_v4_sweep_observation_markdown(observation)
    assert (ROOT / DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_scene_choreography_contract_markdown(contract)


def test_scene_outputs_do_not_stage_render_or_media_artifacts() -> None:
    _ensure_artifacts()
    generated_paths = [
        ROOT / DEFAULT_V4_SWEEP_OBSERVATION_PATH,
        ROOT / DEFAULT_V4_SWEEP_OBSERVATION_DOC_PATH,
        ROOT / DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_PATH,
        ROOT / DEFAULT_SCENE_CHOREOGRAPHY_CONTRACT_DOC_PATH,
        ROOT / DEFAULT_SCENE_CHOREOGRAPHY_PROBE_PATH,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in generated_paths)

    assert "http://" not in combined
    assert "https://" not in combined
    assert "www." not in combined
    assert "render again" not in combined.lower()

    handoff_dir = ROOT / "samples/_probe/newsroom_handoff"
    generated_like = [
        *handoff_dir.glob("yukkuri_animation_v4_tempo_sweep_observation_v1.*"),
        *handoff_dir.glob("yukkuri_animation_scene_choreography_contract_v1.*"),
        *handoff_dir.glob("yukkuri_animation_scene_choreography_probe_v1.*"),
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_like)
