import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EPISODE = (
    ROOT
    / "production_pilots/yukkuri_benchmark_families_001/episodes/civil_arakawa_floodway_001"
)


def test_visual_carrier_plan_is_contiguous_and_preserves_verified_timeline() -> None:
    plan = json.loads(
        (EPISODE / "visual_carrier/visual_carrier_plan.json").read_text(
            encoding="utf-8"
        )
    )
    scenes = plan["scenes"]

    assert plan["timeline_contract"] == {
        "fps": 60,
        "source_voice_item_count": 92,
        "source_timeline_frames": 22427,
        "voice_or_subtitle_mutation_allowed": False,
    }
    assert plan["safe_area"]["subtitle_reserved_region"] == [240, 700, 1440, 300]
    assert len(scenes) == 6
    assert [scene["start_frame"] for scene in scenes] == [
        0,
        2424,
        5351,
        10996,
        13783,
        16613,
    ]
    assert [scene["end_frame"] for scene in scenes] == [
        2424,
        5351,
        10996,
        13783,
        16613,
        22427,
    ]
    assert all(
        left["end_frame"] == right["start_frame"]
        for left, right in zip(scenes, scenes[1:])
    )
    assert all(
        (EPISODE / "visual_carrier" / scene["asset"]).is_file()
        for scene in scenes
    )
    assert plan["boundaries"] == {
        "source_or_reference_images_used": False,
        "reference_frame_layout_copied": False,
        "python_image_generation_or_compositing": False,
        "network_required": False,
        "publication_authorized": False,
        "human_acceptance_inferred": False,
    }


def test_visual_carrier_ir_maps_all_92_rows_once() -> None:
    ir = json.loads(
        (EPISODE / "visual_carrier/visual_carrier.ir.json").read_text(
            encoding="utf-8"
        )
    )
    sections = ir["macro"]["sections"]

    assert ir["utterances"] == []
    assert sections[0]["start_index"] == 1
    assert sections[-1]["end_index"] == 92
    assert all(
        left["end_index"] + 1 == right["start_index"]
        for left, right in zip(sections, sections[1:])
    )
    assert len({section["default_bg"] for section in sections}) == 6


def test_civil_sources_and_measurement_keep_media_and_authority_boundaries() -> None:
    measurement = json.loads(
        (EPISODE / "benchmark_measurement.json").read_text(encoding="utf-8")
    )
    sources = json.loads(
        (EPISODE / "source_registry.json").read_text(encoding="utf-8")
    )

    assert measurement["surface_observation"]["full_timeline_frame_verified"] is False
    assert measurement["surface_observation"]["audio_subject_verified"] is False
    assert all(value is False for key, value in measurement["copy_boundary"].items() if key.endswith("_used") or key.endswith("_reused"))
    assert sources["rights"] == {
        "benchmark_media_reused": False,
        "source_media_reused": False,
        "episode_script_original": True,
        "visual_carrier_original": True,
        "internal_review_only": True,
        "human_acceptance": "unverified",
        "production_authorized": False,
        "publication_authorized": False,
    }
