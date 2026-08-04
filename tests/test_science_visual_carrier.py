import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / "production_pilots/yukkuri_benchmark_families_001/episodes/science_light_distance_001"


def test_visual_carrier_plan_is_contiguous_and_preserves_verified_timeline() -> None:
    plan = json.loads((EPISODE / "visual_carrier/visual_carrier_plan.json").read_text(encoding="utf-8"))
    scenes = plan["scenes"]
    assert plan["timeline_contract"] == {
        "fps": 60,
        "source_voice_item_count": 92,
        "source_timeline_frames": 19807,
        "voice_or_subtitle_mutation_allowed": False,
    }
    assert len(scenes) == 6
    assert [scene["start_frame"] for scene in scenes] == [0, 3414, 6048, 10713, 13284, 16294]
    assert [scene["end_frame"] for scene in scenes] == [3414, 6048, 10713, 13284, 16294, 19807]
    assert scenes[0]["start_frame"] == 0
    assert scenes[-1]["end_frame"] == 19807
    assert all(left["end_frame"] == right["start_frame"] for left, right in zip(scenes, scenes[1:]))
    assert all((EPISODE / "visual_carrier" / scene["asset"]).is_file() for scene in scenes)
    assert plan["boundaries"]["source_or_reference_images_used"] is False
    assert plan["boundaries"]["python_image_generation_or_compositing"] is False


def test_visual_carrier_ir_maps_all_92_rows_once() -> None:
    ir = json.loads((EPISODE / "visual_carrier/visual_carrier.ir.json").read_text(encoding="utf-8"))
    sections = ir["macro"]["sections"]
    assert ir["utterances"] == []
    assert sections[0]["start_index"] == 1
    assert sections[-1]["end_index"] == 92
    assert all(left["end_index"] + 1 == right["start_index"] for left, right in zip(sections, sections[1:]))
    assert len({section["default_bg"] for section in sections}) == 6
