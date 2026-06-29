import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_background_animation_minimal_integrated_scene import (
    DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_DOC_PATH,
    DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_PATH,
    DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_DOC_PATH,
    DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH,
    LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH,
    NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION,
    SCENE_DURATION_SEC,
    SCENE_TIMELINE_LENGTH_FRAMES,
    build_default_minimal_integrated_scene_contract,
    build_default_minimal_integrated_scene_probe_readback,
    materialize_local_minimal_integrated_scene_probe,
    render_minimal_integrated_scene_contract_markdown,
    render_minimal_integrated_scene_probe_markdown,
    write_default_newsroom_background_animation_minimal_integrated_scene_artifacts,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_background_animation_minimal_integrated_scene_artifacts(root=ROOT)


def test_contract_defines_one_integrated_explanation_beat() -> None:
    _ensure_artifacts()
    payload = build_default_minimal_integrated_scene_contract(root=ROOT)
    artifact = _load(DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_PATH)

    assert artifact == payload
    assert artifact["production_status"] == "diagnostic_only"
    assert artifact["render_gate"] == "L0_no_render"
    assert artifact["actual_audience_acceptance_claimed"] is False
    assert artifact["selected_next_axis"] == NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION

    scene = artifact["scene_description"]
    assert scene["duration_target_sec"] == SCENE_DURATION_SEC
    assert 10.0 <= scene["duration_target_sec"] <= 20.0
    assert scene["animation_role"] == "small background accent supporting the explanation"
    assert scene["card_overlay_role"] == "none; existing minimal card or overlay context only"
    assert scene["source_boundary_role"] == "review-only diagnostic line; no real RSS/news source is used"

    plan = artifact["animation_plan"]
    assert plan["stable_start_pose"]["expression"] == "easy"
    assert plan["expression_event"]["expression"] == "panic"
    assert plan["nod_or_reaction"]["head_rotation_values"] == [0.0, -8.0, 0.0]
    assert plan["optional_lateral_emphasis"]["status"] == "omitted_not_needed"
    assert plan["stable_end_pose"]["head_rotation_values"] == [0.0]
    assert plan["disabled_primitives"] == [
        "repeated_nods",
        "mechanical_expression_cycle",
        "body_forward_back",
        "complex_balloon",
    ]


def test_probe_materializes_ignored_local_integrated_scene() -> None:
    _ensure_artifacts()
    payload = build_default_minimal_integrated_scene_probe_readback(root=ROOT)
    artifact = _load(DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH)

    assert artifact == payload
    assert artifact["scene_probe_materialization_status"] == "materialized_ignored_local_probe"
    assert artifact["selected_next_axis"] == NEXT_AXIS_PREVIEW_OPERATOR_INSTRUCTION
    access = artifact["local_probe_access"]
    assert access["repo_relative_path"] == LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH.as_posix()
    assert access["target_exists"] is True
    assert access["access_state"] == "verified_present"
    assert access["access_evidence_level"] == "L3_VERIFIED_PRESENT"
    assert access["artifact_scope"] == "ignored_local_only"
    assert access["git_check_ignore_result"]["ignored"] is True
    assert (ROOT / LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH).exists()

    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-v",
            "--",
            LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH.as_posix(),
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "_tmp/" in result.stdout


def test_probe_readback_is_integrated_scene_not_primitive_loop() -> None:
    _ensure_artifacts()
    artifact = _load(DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH)
    readback = artifact["local_probe_readback"]

    assert readback["readback_status"] == "structural_pass"
    assert readback["timeline"]["fps"] == 60
    assert readback["timeline"]["length_frames"] == SCENE_TIMELINE_LENGTH_FRAMES
    assert readback["timeline"]["length_sec"] == SCENE_DURATION_SEC
    assert readback["timeline"]["item_type_counts"] == {
        "GroupItem": 8,
        "ImageItem": 8,
    }
    assert readback["timeline"]["unexpected_item_types"] == []
    assert readback["segment_count"] == 4

    semantic = readback["semantic_checks"]
    assert semantic["status"] == "pass"
    assert semantic["expression_event_segments"] == ["expression_event_key_phrase"]
    assert semantic["nod_or_reaction_segments"] == ["one_short_nod_after_key_phrase"]
    assert semantic["parent_x_values"] == [-96.0, -96.0, -96.0, -96.0]
    assert all(semantic["checks"].values())

    probe = load_ymmp(ROOT / LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH)
    assert {_item_type(item) for item in _get_timeline_items(probe)} == {
        "GroupItem",
        "ImageItem",
    }


def test_materializer_can_be_called_directly() -> None:
    materialize_local_minimal_integrated_scene_probe(root=ROOT)
    assert (ROOT / LOCAL_IGNORED_MINIMAL_INTEGRATED_SCENE_PROBE_PATH).exists()


def test_markdown_outputs_match_renderers() -> None:
    _ensure_artifacts()
    contract = _load(DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_PATH)
    probe = _load(DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH)

    assert (ROOT / DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_minimal_integrated_scene_contract_markdown(contract)
    assert (ROOT / DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_minimal_integrated_scene_probe_markdown(probe)


def test_outputs_do_not_request_render_or_media_artifacts() -> None:
    _ensure_artifacts()
    generated_paths = [
        ROOT / DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_PATH,
        ROOT / DEFAULT_MINIMAL_INTEGRATED_SCENE_CONTRACT_DOC_PATH,
        ROOT / DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_PATH,
        ROOT / DEFAULT_MINIMAL_INTEGRATED_SCENE_PROBE_DOC_PATH,
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

    tracked_forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in tracked_forbidden_suffixes for path in generated_paths)
