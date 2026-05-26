from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
STATIC_MANIFEST_PATH = (
    REPO_ROOT / "samples" / "_probe" / "baseball" / "static" / "baseball_pitch_event_p05_manifest.json"
)
PNG_PATH = REPO_ROOT / "samples" / "_probe" / "baseball" / "static" / "baseball_pitch_event_p05.png"
PLACEMENT_CONTRACT_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "placement"
    / "baseball_pitch_event_p05_placement_contract.json"
)
PLACEMENT_READBACK_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "placement"
    / "baseball_pitch_event_p05_placement_readback.json"
)
ANIMATION_PLAN_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "animation"
    / "baseball_pitch_event_p05_animation_export_plan.json"
)
ANIMATION_READBACK_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "animation"
    / "baseball_pitch_event_p05_animation_plan_readback.json"
)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_baseball_bn05_placement_contract_tracks_static_png() -> None:
    static_manifest = _load_json(STATIC_MANIFEST_PATH)
    contract = _load_json(PLACEMENT_CONTRACT_PATH)

    assert contract["schema_version"] == "baseball_yymm4_placement_contract.v1"
    assert contract["artifact_type"] == "baseball_static_png_yymm4_placement_contract"
    assert contract["source"]["static_manifest_path"] == (
        "samples/_probe/baseball/static/baseball_pitch_event_p05_manifest.json"
    )
    assert contract["source"]["static_manifest_sha256"] == _sha256(STATIC_MANIFEST_PATH)
    assert contract["source"]["png_path"] == static_manifest["output"]["png_path"]
    assert contract["source"]["png_sha256"] == _sha256(PNG_PATH)
    assert contract["source"]["png_sha256"] == static_manifest["output"]["sha256"]


def test_baseball_bn05_placement_contract_fixes_yymm4_image_item_span() -> None:
    contract = _load_json(PLACEMENT_CONTRACT_PATH)
    placement = contract["placement"]
    item = placement["yymm4_item"]

    assert placement["segment_id"] == "pitch_event_breakdown"
    assert placement["voice_time_range"] == "00:26-00:48"
    assert placement["fps"] == 60
    assert placement["start_frame"] == 26 * 60
    assert placement["length_frames"] == 22 * 60
    assert placement["start_frame"] + placement["length_frames"] == 48 * 60
    assert placement["target_canvas"] == {"width": 1920, "height": 1080}

    assert item["item_type"] == "ImageItem"
    assert item["layer_name"] == "sports_news_overlay"
    assert item["proposed_layer"] == 12
    assert item["file_path"] == "samples/_probe/baseball/static/baseball_pitch_event_p05.png"
    assert item["x"] == 0
    assert item["y"] == 0
    assert item["zoom_percent"] == 150
    assert item["fit"] == "contain_16_9_png_to_1920x1080"


def test_baseball_bn05_readback_keeps_boundaries_and_preview_gate() -> None:
    contract = _load_json(PLACEMENT_CONTRACT_PATH)
    readback = _load_json(PLACEMENT_READBACK_PATH)

    assert readback["status"] == "passed"
    assert readback["checks"]["png_hash_matches_static_manifest"] is True
    assert readback["checks"]["timeline_math_matches_voice_range"] is True
    assert readback["checks"]["manual_preview_gate_present"] is True
    assert readback["checks"]["not_yymm4_file_write"] is True
    assert readback["checks"]["not_creative_acceptance"] is True
    assert readback["derived"]["end_frame_exclusive"] == 2880

    assert contract["manual_preview_gate"]["required_before_creative_acceptance"] is True
    assert contract["boundaries"]["not_yymm4_file_write"] is True
    assert contract["boundaries"]["not_yymm4_proof"] is True
    assert contract["boundaries"]["not_animation_export"] is True
    assert contract["boundaries"]["not_creative_acceptance"] is True


def test_baseball_bn04_animation_export_plan_is_defined_but_not_exported() -> None:
    plan = _load_json(ANIMATION_PLAN_PATH)
    readback = _load_json(ANIMATION_READBACK_PATH)

    assert plan["schema_version"] == "baseball_animation_export_plan.v1"
    assert plan["status"] == "contract_defined_not_exported"
    assert plan["export_decision"]["mode"] == "frame_sequence_first"
    assert plan["planned_outputs"]["width"] == 1280
    assert plan["planned_outputs"]["height"] == 720
    assert plan["planned_outputs"]["fps"] == 30
    assert plan["planned_outputs"]["frame_count"] == 5
    assert len(plan["state_sequence"]) == 3
    assert "visual data has fewer than two pitches" in plan["failure_conditions"]
    assert plan["boundaries"]["not_exported_in_this_slice"] is True
    assert plan["boundaries"]["not_yymm4_placement"] is True
    assert plan["boundaries"]["not_creative_acceptance"] is True

    assert readback["status"] == "passed_contract_only"
    assert readback["checks"]["mode_is_frame_sequence_first"] is True
    assert readback["checks"]["not_exported_in_this_slice"] is True
