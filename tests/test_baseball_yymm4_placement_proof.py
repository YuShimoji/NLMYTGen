from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "placement"
    / "baseball_pitch_event_p05_placement_contract.json"
)
STATIC_MANIFEST_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "static"
    / "baseball_pitch_event_p05_manifest.json"
)
PROOF_YMMP_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "placement"
    / "baseball_pitch_event_p05_placement_proof.ymmp"
)
PROOF_MANIFEST_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "placement"
    / "baseball_pitch_event_p05_placement_proof_manifest.json"
)
PROOF_READBACK_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "placement"
    / "baseball_pitch_event_p05_placement_proof_readback.json"
)
PROOF_HANDOFF_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "placement"
    / "baseball_pitch_event_p05_placement_proof_handoff.md"
)
PREVIEW_SCREENSHOT_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "placement"
    / "baseball_pitch_event_p05_yymm4_preview_screenshot.png"
)
PREVIEW_REVIEW_PATH = (
    REPO_ROOT
    / "samples"
    / "_probe"
    / "baseball"
    / "placement"
    / "baseball_pitch_event_p05_yymm4_preview_review.json"
)
SCRIPT_PATH = (
    REPO_ROOT
    / "lanes"
    / "sports_news"
    / "scripts"
    / "build_baseball_yymm4_placement_proof.js"
)
LAUNCHER_PATH = (
    REPO_ROOT
    / "lanes"
    / "sports_news"
    / "scripts"
    / "open_baseball_bn05_preview.ps1"
)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _item_type(item: dict) -> str:
    return str(item.get("$type", "")).split(",")[0].split(".")[-1]


def _animated_value(item: dict, key: str):
    return item[key]["Values"][0]["Value"]


def test_baseball_placement_proof_script_exists() -> None:
    assert SCRIPT_PATH.exists()
    assert LAUNCHER_PATH.exists()


def test_baseball_placement_proof_ymmp_contains_one_image_item() -> None:
    contract = _load_json(CONTRACT_PATH)
    proof = _load_json(PROOF_YMMP_PATH)
    timeline = proof["Timelines"][0]
    items = timeline["Items"]
    baseball_items = [
        item
        for item in items
        if _item_type(item) == "ImageItem"
        and item.get("Remark")
        == "baseball_bn05_placement_proof segment=pitch_event_breakdown not_creative_acceptance no_render no_publish_gate"
    ]

    assert len(baseball_items) == 1
    item = baseball_items[0]
    expected = contract["placement"]["yymm4_item"]

    assert timeline["VideoInfo"]["FPS"] == 60
    assert timeline["VideoInfo"]["Width"] == 1920
    assert timeline["VideoInfo"]["Height"] == 1080
    assert timeline["CurrentFrame"] == 1560
    assert timeline["Length"] == 2880

    assert item["FilePath"] == expected["file_path"]
    assert expected["path_resolution_base"] == "proof_ymmp_directory"
    assert not Path(item["FilePath"]).is_absolute()
    assert (PROOF_YMMP_PATH.parent / item["FilePath"]).resolve() == (
        REPO_ROOT / contract["source"]["png_path"]
    ).resolve()
    assert item["Frame"] == contract["placement"]["start_frame"] == 1560
    assert item["Length"] == contract["placement"]["length_frames"] == 1320
    assert item["Layer"] == expected["proposed_layer"] == 12
    assert _animated_value(item, "X") == expected["x"] == 0
    assert _animated_value(item, "Y") == expected["y"] == 0
    assert _animated_value(item, "Zoom") == expected["zoom_percent"] == 150
    assert _animated_value(item, "Opacity") == expected["opacity_percent"] == 100


def test_baseball_placement_proof_manifest_and_readback_match_hashes() -> None:
    contract = _load_json(CONTRACT_PATH)
    static_manifest = _load_json(STATIC_MANIFEST_PATH)
    manifest = _load_json(PROOF_MANIFEST_PATH)
    readback = _load_json(PROOF_READBACK_PATH)

    assert manifest["schema_version"] == "baseball_yymm4_placement_proof_manifest.v1"
    assert manifest["artifact_type"] == "baseball_static_png_yymm4_insertion_proof"
    assert manifest["input"]["placement_contract_sha256"] == _sha256(CONTRACT_PATH)
    assert manifest["input"]["static_manifest_sha256"] == _sha256(STATIC_MANIFEST_PATH)
    assert manifest["input"]["png_sha256"] == contract["source"]["png_sha256"]
    assert manifest["input"]["png_sha256"] == static_manifest["output"]["sha256"]
    assert manifest["output"]["proof_ymmp_sha256"] == _sha256(PROOF_YMMP_PATH)

    assert readback["status"] == "passed"
    assert readback["proof_ymmp_sha256"] == _sha256(PROOF_YMMP_PATH)
    assert readback["checks"]["proof_has_single_baseball_image_item"] is True
    assert readback["checks"]["png_hash_matches_static_manifest"] is True
    assert readback["checks"]["media_path_is_relative"] is True
    assert readback["checks"]["media_path_resolution_base_is_proof_ymmp_directory"] is True
    assert readback["checks"]["media_path_resolves_to_source_png"] is True
    assert readback["checks"]["media_file_exists_from_proof_dir"] is True
    assert readback["checks"]["png_hash_matches_proof_dir_resolved_file"] is True
    assert readback["checks"]["file_path_matches_contract"] is True
    assert readback["checks"]["frame_matches_contract"] is True
    assert readback["checks"]["layer_matches_contract"] is True
    assert readback["failed_checks"] == []
    assert readback["placement_item"]["resolved_repo_relative_path"] == contract["source"]["png_path"]


def test_baseball_placement_proof_boundaries_and_handoff() -> None:
    manifest = _load_json(PROOF_MANIFEST_PATH)
    readback = _load_json(PROOF_READBACK_PATH)
    handoff = PROOF_HANDOFF_PATH.read_text(encoding="utf-8")

    for payload in (manifest, readback):
        assert payload["boundaries"]["not_creative_acceptance"] is True
        assert payload["boundaries"]["not_render_proof"] is True
        assert payload["boundaries"]["not_publish_gate"] is True
        assert payload["boundaries"]["not_animation_export"] is True

    assert "not production placement" in handoff
    assert "not a render proof" in handoff
    assert "not creative acceptance" in handoff
    assert "accepted_gate_only" in handoff
    assert "not production proof" in handoff


def test_baseball_placement_manual_preview_gate_acceptance_recorded() -> None:
    review = _load_json(PREVIEW_REVIEW_PATH)

    assert PREVIEW_SCREENSHOT_PATH.exists()
    assert _sha256(PREVIEW_SCREENSHOT_PATH) == review["screenshot"]["sha256"]
    assert review["status"] == "accepted_gate_only"
    assert review["target"]["frame"] == 1560
    assert review["target"]["timecode"] == "00:26.00"
    assert review["freeform_review_interpretation"]["interpreted_intent"] == "accept_gate_only"
    assert review["freeform_review_interpretation"]["confidence"] == "high"
    assert review["freeform_review_interpretation"]["user_rewrite_required"] is False
    assert review["acceptance_scope"]["manual_preview_gate_closed"] is True
    assert review["acceptance_scope"]["diagnostic_review_only"] is True
    assert review["acceptance_scope"]["not_render_completion"] is True
    assert review["acceptance_scope"]["not_production_proof"] is True
    assert review["acceptance_scope"]["not_creative_final_acceptance"] is True
    assert review["acceptance_scope"]["future_visual_redesign_is_separate"] is True
