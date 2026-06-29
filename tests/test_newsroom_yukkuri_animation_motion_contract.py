import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_yukkuri_animation_motion_contract import (
    DEFAULT_MOTION_CONTRACT_DOC_PATH,
    DEFAULT_MOTION_CONTRACT_PATH,
    DEFAULT_OBSERVATION_DOC_PATH,
    DEFAULT_OBSERVATION_PATH,
    LOCAL_IGNORED_V2_MOTION_FIX_PATH,
    MOTION_CONTRACT,
    NEXT_AXIS_V2_PREVIEW,
    V2_BEAT_PLAN,
    V2_TIMELINE_LENGTH_FRAMES,
    build_default_motion_contract,
    build_default_preview_observation,
    materialize_local_v2_motion_fix_probe,
    render_motion_contract_markdown,
    render_preview_observation_markdown,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_v2_probe() -> None:
    materialize_local_v2_motion_fix_probe(root=ROOT)


def test_preview_observation_artifact_normalizes_user_readback_without_render() -> None:
    _ensure_v2_probe()
    payload = build_default_preview_observation(root=ROOT)
    artifact = _load(DEFAULT_OBSERVATION_PATH)

    assert artifact == payload
    normalized = artifact["normalized_user_observation"]
    assert normalized["yym4_opened"] is True
    assert normalized["character_visible"] is True
    assert normalized["head_body_attachment"] == "pass"
    assert normalized["expression_swap"] == "pass"
    assert normalized["character_motion_visible"] == "pass_with_warning"
    assert normalized["entrance_exit"] == "pass_with_facing_warning"
    assert normalized["small_position_move"] == "pass_with_anchor_continuity_warning"
    assert normalized["head_nod"] == "pass_with_timing_warning"
    assert normalized["major_visual_breakage"] is False
    assert artifact["render_export_checked"] is False
    assert artifact["render_export_required_now"] is False
    assert artifact["render_gate"] == "L0_no_render"


def test_motion_contract_artifact_materializes_ignored_v2_probe() -> None:
    _ensure_v2_probe()
    payload = build_default_motion_contract(root=ROOT)
    artifact = _load(DEFAULT_MOTION_CONTRACT_PATH)

    assert artifact == payload
    assert artifact["v2_materialization_status"] == "materialized_ignored_local_probe"
    assert artifact["selected_next_axis"] == NEXT_AXIS_V2_PREVIEW
    assert artifact["motion_contract"] == MOTION_CONTRACT
    assert {row["primitive_id"] for row in artifact["motion_contract"]} == {
        "head_nod",
        "expression_swap",
        "character_entrance_exit",
        "small_position_move",
    }

    v2 = artifact["v2_local_probe"]
    assert v2["repo_relative_path"] == LOCAL_IGNORED_V2_MOTION_FIX_PATH.as_posix()
    assert v2["target_exists"] is True
    assert v2["access_state"] == "verified_present"
    assert v2["access_evidence_level"] == "L3_VERIFIED_PRESENT"
    assert v2["artifact_scope"] == "ignored_local_only"
    assert v2["git_check_ignore_result"]["ignored"] is True
    assert (ROOT / LOCAL_IGNORED_V2_MOTION_FIX_PATH).exists()

    result = subprocess.run(
        ["git", "check-ignore", "-v", "--", LOCAL_IGNORED_V2_MOTION_FIX_PATH.as_posix()],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "_tmp/" in result.stdout


def test_v2_probe_readback_enforces_timing_facing_and_anchor_continuity() -> None:
    _ensure_v2_probe()
    artifact = _load(DEFAULT_MOTION_CONTRACT_PATH)
    readback = artifact["v2_probe_readback"]

    assert readback["readback_status"] == "structural_pass"
    assert readback["timeline"]["fps"] == 60
    assert readback["timeline"]["length_frames"] == V2_TIMELINE_LENGTH_FRAMES
    assert readback["timeline"]["length_sec"] == 30.0
    assert readback["timeline"]["item_type_counts"] == {
        "GroupItem": 10,
        "ImageItem": 10,
    }
    assert readback["timeline"]["unexpected_item_types"] == []

    primitive_status = {
        row["primitive_id"]: row["status"]
        for row in readback["primitive_status"]
    }
    assert primitive_status == {
        "head_nod": "pass",
        "expression_swap": "pass",
        "character_entrance_exit": "pass",
        "small_position_move": "pass",
    }
    assert readback["anchor_continuity"]["shared_anchor_x"] == -96.0
    assert readback["anchor_continuity"]["adjacent_boundaries_share_anchor"] is True

    beat_readback = {row["beat_id"]: row for row in readback["beat_readback"]}
    for beat in V2_BEAT_PLAN[1:4]:
        values = beat_readback[beat["beat_id"]]["parent_x_values"]
        assert values[0] == -96.0
        assert values[-1] == -96.0
    nod_values = beat_readback["v2_beat_02_nod_response"]["head_rotation_values"]
    assert nod_values == [0.0, -10.0, 0.0]

    probe = load_ymmp(ROOT / LOCAL_IGNORED_V2_MOTION_FIX_PATH)
    assert {_item_type(item) for item in _get_timeline_items(probe)} == {
        "GroupItem",
        "ImageItem",
    }


def test_markdown_outputs_match_renderers() -> None:
    _ensure_v2_probe()
    observation = _load(DEFAULT_OBSERVATION_PATH)
    contract = _load(DEFAULT_MOTION_CONTRACT_PATH)

    assert (ROOT / DEFAULT_OBSERVATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_preview_observation_markdown(observation)
    assert (ROOT / DEFAULT_MOTION_CONTRACT_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_motion_contract_markdown(contract)


def test_motion_contract_outputs_do_not_stage_render_or_media_artifacts() -> None:
    generated_paths = [
        ROOT / DEFAULT_OBSERVATION_PATH,
        ROOT / DEFAULT_OBSERVATION_DOC_PATH,
        ROOT / DEFAULT_MOTION_CONTRACT_PATH,
        ROOT / DEFAULT_MOTION_CONTRACT_DOC_PATH,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in generated_paths)

    assert "http://" not in combined
    assert "https://" not in combined
    assert "www." not in combined
    assert "render again" not in combined.lower()

    handoff_dir = ROOT / "samples/_probe/newsroom_handoff"
    generated_like = [
        *handoff_dir.glob("yukkuri_animation_primitive_preview_observation_v1.*"),
        *handoff_dir.glob("yukkuri_animation_motion_contract_v1.*"),
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_like)
