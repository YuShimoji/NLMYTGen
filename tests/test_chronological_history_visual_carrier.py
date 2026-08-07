import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
EPISODE = (
    ROOT
    / "production_pilots/yukkuri_benchmark_families_001/episodes/history_japan_standard_time_001"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_visual_carrier_plan_binds_exact_input_and_all_97_rows() -> None:
    plan = json.loads(
        (EPISODE / "visual_carrier/visual_carrier_plan.json").read_text(
            encoding="utf-8"
        )
    )
    scenes = plan["scenes"]

    assert plan["input_identity"] == {
        "script_sha256": _sha256(EPISODE / "script.txt"),
        "source_registry_sha256": _sha256(EPISODE / "source_registry.json"),
        "csv_sha256": _sha256(EPISODE / "yymm4_import.csv"),
        "csv_row_count": 97,
    }
    assert len(scenes) == 8
    assert scenes[0]["rows"][0] == 1
    assert scenes[-1]["rows"][1] == 97
    assert all(
        left["rows"][1] + 1 == right["rows"][0]
        for left, right in zip(scenes, scenes[1:])
    )
    assert all(scene["frame_range"] is None for scene in scenes)
    assert plan["timeline_contract"]["frame_binding_status"] == (
        "pending_target_yymm4_import"
    )
    assert plan["timeline_contract"]["voice_or_subtitle_mutation_allowed"] is False


def test_visual_carrier_svg_assets_are_original_self_contained_1080p_sources() -> None:
    plan = json.loads(
        (EPISODE / "visual_carrier/visual_carrier_plan.json").read_text(
            encoding="utf-8"
        )
    )

    for scene in plan["scenes"]:
        path = EPISODE / "visual_carrier" / scene["asset"]
        raw = path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(raw)
        assert root.tag == "{http://www.w3.org/2000/svg}svg"
        assert root.attrib["width"] == "1920"
        assert root.attrib["height"] == "1080"
        assert root.attrib["viewBox"] == "0 0 1920 1080"
        assert root.findall(".//{http://www.w3.org/2000/svg}image") == []
        assert "href=" not in raw

    assert plan["boundaries"] == {
        "benchmark_or_source_images_used": False,
        "benchmark_audio_or_branding_used": False,
        "reference_frame_layout_copied": False,
        "python_image_generation_or_compositing": False,
        "network_required": False,
        "target_yymm4_import_observed": False,
        "target_yymm4_render_observed": False,
        "publication_authorized": False,
        "human_acceptance_inferred": False,
    }


def test_visual_carrier_ir_matches_plan_without_claiming_frame_binding() -> None:
    plan = json.loads(
        (EPISODE / "visual_carrier/visual_carrier_plan.json").read_text(
            encoding="utf-8"
        )
    )
    ir = json.loads(
        (EPISODE / "visual_carrier/visual_carrier.ir.json").read_text(
            encoding="utf-8"
        )
    )
    sections = ir["macro"]["sections"]

    assert ir["utterances"] == []
    assert len(sections) == len(plan["scenes"])
    assert [section["start_index"] for section in sections] == [
        scene["rows"][0] for scene in plan["scenes"]
    ]
    assert [section["end_index"] for section in sections] == [
        scene["rows"][1] for scene in plan["scenes"]
    ]
    assert [section["default_bg"] for section in sections] == [
        scene["scene_id"] for scene in plan["scenes"]
    ]


def test_preflight_receipt_honestly_stops_before_yymm4_and_mp4_claims() -> None:
    receipt = json.loads(
        (EPISODE / "visual_carrier_preflight_receipt.json").read_text(
            encoding="utf-8"
        )
    )
    state = json.loads(
        (EPISODE / "execution_state.json").read_text(encoding="utf-8")
    )

    for asset in receipt["carrier_identity"]["assets"]:
        path = EPISODE / asset["path"]
        assert path.stat().st_size == asset["bytes"]
        assert _sha256(path) == asset["sha256"]

    assert receipt["target_yymm4_observation"]["csv_import_observed"] is False
    assert receipt["target_yymm4_observation"]["ymmp_written"] is False
    assert receipt["target_yymm4_observation"]["render_completed"] is False
    assert receipt["artifact_verification"]["ymmp"] is None
    assert receipt["artifact_verification"]["mp4"] is None
    assert receipt["review_axes"]["human_acceptance"] == "unverified"
    assert receipt["review_axes"]["publication_authorized"] is False
    assert _sha256(EPISODE / state["visual_carrier_preflight"]["receipt_path"]) == (
        state["visual_carrier_preflight"]["receipt_sha256"]
    )
    assert state["resume_gate"]["status"] == "DEPENDENCY_MISSING"
    assert state["completed"]["local_render_completed"] is False
