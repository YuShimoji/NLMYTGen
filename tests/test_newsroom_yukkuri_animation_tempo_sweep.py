import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_yukkuri_animation_tempo_sweep import (
    DEFAULT_TEMPO_SWEEP_CONTRACT_DOC_PATH,
    DEFAULT_TEMPO_SWEEP_CONTRACT_PATH,
    DEFAULT_V3_PREVIEW_OBSERVATION_DOC_PATH,
    DEFAULT_V3_PREVIEW_OBSERVATION_PATH,
    LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH,
    NEXT_AXIS_V4_SWEEP_PREVIEW,
    TEMPO_SWEEP_BANDS,
    V4_BEAT_PLAN,
    V4_TIMELINE_LENGTH_FRAMES,
    build_default_tempo_sweep_contract,
    build_default_v3_preview_observation,
    materialize_local_v4_tempo_sweep_probe,
    render_tempo_sweep_contract_markdown,
    render_v3_preview_observation_markdown,
    write_default_newsroom_yukkuri_animation_tempo_sweep_artifacts,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_artifacts() -> None:
    write_default_newsroom_yukkuri_animation_tempo_sweep_artifacts(root=ROOT)


def test_v3_preview_observation_normalizes_single_value_iteration_risk() -> None:
    _ensure_artifacts()
    payload = build_default_v3_preview_observation(root=ROOT)
    artifact = _load(DEFAULT_V3_PREVIEW_OBSERVATION_PATH)

    assert artifact == payload
    normalized = artifact["normalized_user_observation"]
    assert normalized["yym4_opened"] is True
    assert normalized["v3_preview_observed"] is True
    assert normalized["motion_speed"] == "still_too_slow"
    assert normalized["floatiness"] == "high"
    assert normalized["v3_tempo_improved_but_insufficient"] is True
    assert normalized["single_value_iteration_risk"] is True
    assert normalized["recommended_method"] == "tempo_sweep"
    assert normalized["render_export_checked"] is False
    assert normalized["render_export_required_now"] is False
    assert artifact["render_gate"] == "L0_no_render"


def test_tempo_sweep_contract_materializes_ignored_v4_probe() -> None:
    _ensure_artifacts()
    payload = build_default_tempo_sweep_contract(root=ROOT)
    artifact = _load(DEFAULT_TEMPO_SWEEP_CONTRACT_PATH)

    assert artifact == payload
    assert artifact["v4_materialization_status"] == "materialized_ignored_local_probe"
    assert artifact["selected_next_axis"] == NEXT_AXIS_V4_SWEEP_PREVIEW
    assert [row["frame_span"] for row in artifact["speed_bands"]] == [30, 45, 60, 90]
    assert artifact["expected_default_candidate"] == {
        "band_id": "tempo_band_060f_1_0s",
        "frame_span": 60,
        "seconds_at_60fps": 1.0,
        "reason": "The user suggested starting around 1 second; 0.75 and 0.5 seconds are comparison lower bounds.",
    }

    v4 = artifact["v4_local_probe"]
    assert v4["repo_relative_path"] == LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH.as_posix()
    assert v4["target_exists"] is True
    assert v4["access_state"] == "verified_present"
    assert v4["access_evidence_level"] == "L3_VERIFIED_PRESENT"
    assert v4["artifact_scope"] == "ignored_local_only"
    assert v4["git_check_ignore_result"]["ignored"] is True
    assert (ROOT / LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH).exists()

    result = subprocess.run(
        ["git", "check-ignore", "-v", "--", LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH.as_posix()],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "_tmp/" in result.stdout


def test_v4_probe_readback_covers_all_tempo_bands_without_anchor_regression() -> None:
    _ensure_artifacts()
    artifact = _load(DEFAULT_TEMPO_SWEEP_CONTRACT_PATH)
    readback = artifact["v4_probe_readback"]

    assert readback["readback_status"] == "structural_pass"
    assert readback["timeline"]["fps"] == 60
    assert readback["timeline"]["length_frames"] == V4_TIMELINE_LENGTH_FRAMES
    assert readback["timeline"]["length_sec"] == 18.75
    assert readback["timeline"]["item_type_counts"] == {
        "GroupItem": 40,
        "ImageItem": 40,
    }
    assert readback["timeline"]["unexpected_item_types"] == []
    assert readback["tempo_sweep_summary"] == {
        "band_count": 4,
        "beat_count_per_band": 5,
        "total_beat_count": len(V4_BEAT_PLAN),
        "frame_spans": [30, 45, 60, 90],
        "seconds_at_60fps": [0.5, 0.75, 1.0, 1.5],
        "expected_default_candidate": "tempo_band_060f_1_0s",
    }

    by_band = {row["band_id"]: row for row in readback["band_readback"]}
    assert list(by_band) == [band["band_id"] for band in TEMPO_SWEEP_BANDS]
    for band in TEMPO_SWEEP_BANDS:
        row = by_band[band["band_id"]]
        assert row["frame_span"] == band["frame_span"]
        assert row["seconds_at_60fps"] == band["seconds_at_60fps"]
        assert row["beat_count"] == 5
        assert row["primitive_ids"] == [
            "character_entrance_exit",
            "expression_swap",
            "head_nod",
            "small_position_move",
        ]
        assert row["anchor_continuity"] == "pass"
        assert row["status"] == "pass"

    probe = load_ymmp(ROOT / LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH)
    assert {_item_type(item) for item in _get_timeline_items(probe)} == {
        "GroupItem",
        "ImageItem",
    }


def test_v4_materializer_can_be_called_directly() -> None:
    materialize_local_v4_tempo_sweep_probe(root=ROOT)
    assert (ROOT / LOCAL_IGNORED_V4_TEMPO_SWEEP_PATH).exists()


def test_markdown_outputs_match_renderers() -> None:
    _ensure_artifacts()
    observation = _load(DEFAULT_V3_PREVIEW_OBSERVATION_PATH)
    contract = _load(DEFAULT_TEMPO_SWEEP_CONTRACT_PATH)

    assert (ROOT / DEFAULT_V3_PREVIEW_OBSERVATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_v3_preview_observation_markdown(observation)
    assert (ROOT / DEFAULT_TEMPO_SWEEP_CONTRACT_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_tempo_sweep_contract_markdown(contract)


def test_tempo_sweep_outputs_do_not_stage_render_or_media_artifacts() -> None:
    _ensure_artifacts()
    generated_paths = [
        ROOT / DEFAULT_V3_PREVIEW_OBSERVATION_PATH,
        ROOT / DEFAULT_V3_PREVIEW_OBSERVATION_DOC_PATH,
        ROOT / DEFAULT_TEMPO_SWEEP_CONTRACT_PATH,
        ROOT / DEFAULT_TEMPO_SWEEP_CONTRACT_DOC_PATH,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in generated_paths)

    assert "http://" not in combined
    assert "https://" not in combined
    assert "www." not in combined
    assert "render again" not in combined.lower()

    handoff_dir = ROOT / "samples/_probe/newsroom_handoff"
    generated_like = [
        *handoff_dir.glob("yukkuri_animation_v3_preview_observation_v1.*"),
        *handoff_dir.glob("yukkuri_animation_tempo_sweep_contract_v1.*"),
    ]
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_like)
