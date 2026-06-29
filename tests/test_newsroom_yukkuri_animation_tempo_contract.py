import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_yukkuri_animation_tempo_contract import (
    DEFAULT_TEMPO_CONTRACT_DOC_PATH,
    DEFAULT_TEMPO_CONTRACT_PATH,
    DEFAULT_V2_PREVIEW_OBSERVATION_DOC_PATH,
    DEFAULT_V2_PREVIEW_OBSERVATION_PATH,
    LOCAL_IGNORED_V3_TEMPO_FIX_PATH,
    NEXT_AXIS_V3_PREVIEW,
    TEMPO_CONTRACT,
    V3_BEAT_LENGTH_FRAMES,
    V3_BEAT_PLAN,
    V3_TIMELINE_LENGTH_FRAMES,
    build_default_tempo_contract,
    build_default_v2_preview_observation,
    materialize_local_v3_tempo_fix_probe,
    render_tempo_contract_markdown,
    render_v2_preview_observation_markdown,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_v3_probe() -> None:
    materialize_local_v3_tempo_fix_probe(root=ROOT)


def test_v2_preview_observation_artifact_normalizes_tempo_feedback() -> None:
    _ensure_v3_probe()
    payload = build_default_v2_preview_observation(root=ROOT)
    artifact = _load(DEFAULT_V2_PREVIEW_OBSERVATION_PATH)

    assert artifact == payload
    normalized = artifact["normalized_user_observation"]
    assert normalized["yym4_opened"] is True
    assert normalized["v2_preview_observed"] is True
    assert normalized["anchor_continuity"] == "improved"
    assert normalized["segment_connection"] == "pass"
    assert normalized["x_jump_regression"] == "not_reported"
    assert normalized["motion_speed"] == "too_slow"
    assert normalized["tempo_status"] == "fail_or_warning"
    assert normalized["render_export_checked"] is False
    assert normalized["render_export_required_now"] is False
    assert artifact["render_gate"] == "L0_no_render"


def test_tempo_contract_artifact_materializes_ignored_v3_probe() -> None:
    _ensure_v3_probe()
    payload = build_default_tempo_contract(root=ROOT)
    artifact = _load(DEFAULT_TEMPO_CONTRACT_PATH)

    assert artifact == payload
    assert artifact["v3_materialization_status"] == "materialized_ignored_local_probe"
    assert artifact["selected_next_axis"] == NEXT_AXIS_V3_PREVIEW
    assert artifact["tempo_contract"] == TEMPO_CONTRACT
    assert {row["primitive_id"] for row in artifact["tempo_contract"]} == {
        "head_nod",
        "expression_swap",
        "character_entrance_exit",
        "small_position_move",
    }

    v3 = artifact["v3_local_probe"]
    assert v3["repo_relative_path"] == LOCAL_IGNORED_V3_TEMPO_FIX_PATH.as_posix()
    assert v3["target_exists"] is True
    assert v3["access_state"] == "verified_present"
    assert v3["access_evidence_level"] == "L3_VERIFIED_PRESENT"
    assert v3["artifact_scope"] == "ignored_local_only"
    assert v3["git_check_ignore_result"]["ignored"] is True
    assert (ROOT / LOCAL_IGNORED_V3_TEMPO_FIX_PATH).exists()

    result = subprocess.run(
        ["git", "check-ignore", "-v", "--", LOCAL_IGNORED_V3_TEMPO_FIX_PATH.as_posix()],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "_tmp/" in result.stdout


def test_v3_probe_readback_halves_v2_duration_without_anchor_regression() -> None:
    _ensure_v3_probe()
    artifact = _load(DEFAULT_TEMPO_CONTRACT_PATH)
    readback = artifact["v3_probe_readback"]

    assert readback["readback_status"] == "structural_pass"
    assert readback["timeline"]["fps"] == 60
    assert readback["timeline"]["length_frames"] == V3_TIMELINE_LENGTH_FRAMES
    assert readback["timeline"]["length_sec"] == 15.0
    assert readback["timeline"]["item_type_counts"] == {
        "GroupItem": 10,
        "ImageItem": 10,
    }
    assert readback["timeline"]["unexpected_item_types"] == []
    assert readback["tempo_change"] == {
        "v2_beat_length_frames": 360,
        "v3_beat_length_frames": V3_BEAT_LENGTH_FRAMES,
        "duration_ratio": 0.5,
        "tempo_multiplier": 2.0,
    }
    assert readback["anchor_continuity"]["shared_anchor_x"] == -96.0
    assert readback["anchor_continuity"]["adjacent_boundaries_share_anchor"] is True

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
    beat_readback = {row["beat_id"]: row for row in readback["beat_readback"]}
    for beat in V3_BEAT_PLAN:
        row = beat_readback[beat["beat_id"]]
        assert row["length"] == V3_BEAT_LENGTH_FRAMES
    for beat in V3_BEAT_PLAN[1:4]:
        values = beat_readback[beat["beat_id"]]["parent_x_values"]
        assert values[0] == -96.0
        assert values[-1] == -96.0
    assert beat_readback["v3_beat_02_nod_response"]["head_rotation_values"] == [
        0.0,
        -10.0,
        0.0,
    ]

    probe = load_ymmp(ROOT / LOCAL_IGNORED_V3_TEMPO_FIX_PATH)
    assert {_item_type(item) for item in _get_timeline_items(probe)} == {
        "GroupItem",
        "ImageItem",
    }


def test_markdown_outputs_match_renderers() -> None:
    _ensure_v3_probe()
    observation = _load(DEFAULT_V2_PREVIEW_OBSERVATION_PATH)
    contract = _load(DEFAULT_TEMPO_CONTRACT_PATH)

    assert (ROOT / DEFAULT_V2_PREVIEW_OBSERVATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_v2_preview_observation_markdown(observation)
    assert (ROOT / DEFAULT_TEMPO_CONTRACT_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_tempo_contract_markdown(contract)


def test_tempo_contract_outputs_do_not_stage_render_or_media_artifacts() -> None:
    generated_paths = [
        ROOT / DEFAULT_V2_PREVIEW_OBSERVATION_PATH,
        ROOT / DEFAULT_V2_PREVIEW_OBSERVATION_DOC_PATH,
        ROOT / DEFAULT_TEMPO_CONTRACT_PATH,
        ROOT / DEFAULT_TEMPO_CONTRACT_DOC_PATH,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in generated_paths)

    assert "http://" not in combined
    assert "https://" not in combined
    assert "www." not in combined
    assert "render again" not in combined.lower()

    handoff_dir = ROOT / "samples/_probe/newsroom_handoff"
    generated_like = [
        *handoff_dir.glob("yukkuri_animation_v2_preview_observation_v1.*"),
        *handoff_dir.glob("yukkuri_animation_tempo_contract_v1.*"),
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_like)
