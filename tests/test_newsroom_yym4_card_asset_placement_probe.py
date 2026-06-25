import json
import re
import subprocess
from pathlib import Path

from src.pipeline.newsroom_yym4_card_asset_placement_probe import (
    CARD_LAYER,
    CARD_REMARK_PREFIX,
    DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH,
    DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_DOC_PATH,
    DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH,
    EXPECTED_TEXTS,
    NEXT_DEFAULT_SLICE,
    YYM4_CARD_ASSET_PLACEMENT_PROBE_ID,
    YYM4_CARD_ASSET_PLACEMENT_PROBE_SCHEMA_VERSION,
    build_default_newsroom_yym4_card_asset_placement_probe,
    render_newsroom_yym4_card_asset_placement_probe_markdown,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


ROOT = Path(__file__).resolve().parents[1]
PROBE_PATH = ROOT / DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH
DOC_PATH = ROOT / DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_DOC_PATH
PATCHED_YMMP_PATH = ROOT / DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH
EXPECTED_FRAMES = [(0, 720), (720, 720), (1440, 1320), (2760, 1320)]


def _probe() -> dict:
    return json.loads(PROBE_PATH.read_text(encoding="utf-8"))


def _png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    assert header[:8] == b"\x89PNG\r\n\x1a\n"
    assert header[12:16] == b"IHDR"
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def test_placement_probe_json_matches_builder_output_and_identity() -> None:
    probe = _probe()

    assert probe == build_default_newsroom_yym4_card_asset_placement_probe(root=ROOT)
    assert probe["artifact_id"] == YYM4_CARD_ASSET_PLACEMENT_PROBE_ID
    assert probe["probe_id"] == YYM4_CARD_ASSET_PLACEMENT_PROBE_ID
    assert probe["schema_version"] == YYM4_CARD_ASSET_PLACEMENT_PROBE_SCHEMA_VERSION
    assert probe["review_status"] == "ready_for_supervisor_review"
    assert probe["production_status"] == "diagnostic_only"
    assert probe["probe_status"] == "placed_structurally"
    assert probe["diagnostic_only"] is True
    assert probe["identity"]["patched_ymmp_local_path"] == (
        "_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp"
    )


def test_source_assets_map_one_card_to_each_caption_and_png() -> None:
    assets = _probe()["source_assets"]

    assert len(assets) == 4
    assert [asset["mapped_dialogue_text"] for asset in assets] == list(EXPECTED_TEXTS)
    assert [
        (asset["intended_start_sec"], asset["intended_end_sec"])
        for asset in assets
    ] == [(0, 12), (12, 24), (24, 46), (46, 68)]
    assert [(asset["start_frame"], asset["length_frames"]) for asset in assets] == (
        EXPECTED_FRAMES
    )
    assert all(asset["source_svg_path"].endswith(".svg") for asset in assets)
    assert all(asset["png_path"].endswith(".png") for asset in assets)
    assert all((ROOT / asset["source_svg_path"]).exists() for asset in assets)
    assert all((ROOT / asset["png_path"]).exists() for asset in assets)
    assert all(asset["direct_yym4_card_object_graph"] is False for asset in assets)
    assert all(asset["yym4_text_shape_reconstruction"] is False for asset in assets)


def test_raster_export_status_records_deterministic_png_metadata() -> None:
    raster = _probe()["raster_export_status"]

    assert raster["png_export_status"] == "generated"
    assert raster["rasterization_method"] == "existing_toolchain"
    assert raster["deterministic_export"] is True
    assert raster["external_fetch_performed"] is False
    assert raster["real_media_dependency"] is False
    assert raster["png_file_count"] == 4
    assert raster["expected_png_file_count"] == 4
    assert raster["errors"] == []
    for row in raster["png_files"]:
        png_path = ROOT / row["path"]
        assert row["valid"] is True
        assert row["width"] == 1920
        assert row["height"] == 1080
        assert _png_size(png_path) == (1920, 1080)


def test_ignored_ymmp_copy_contains_only_image_items_for_cards() -> None:
    data = load_ymmp(PATCHED_YMMP_PATH)
    items = _get_timeline_items(data)
    voice_items = [item for item in items if _item_type(item) == "VoiceItem"]
    card_items = [
        item
        for item in items
        if _item_type(item) == "ImageItem"
        and isinstance(item.get("Remark"), str)
        and item["Remark"].startswith(CARD_REMARK_PREFIX)
    ]
    forbidden_card_graph_items = [
        item for item in card_items if _item_type(item) in {"TextItem", "ShapeItem"}
    ]

    assert PATCHED_YMMP_PATH.exists()
    assert len(voice_items) == 4
    assert [item.get("Serif") or item.get("Text") for item in voice_items] == list(
        EXPECTED_TEXTS
    )
    assert len(card_items) == 4
    assert forbidden_card_graph_items == []
    assert [(item["Frame"], item["Length"]) for item in card_items] == EXPECTED_FRAMES
    assert all(item["Layer"] == CARD_LAYER for item in card_items)
    assert all(str(item["FilePath"]).lower().endswith(".png") for item in card_items)
    assert all(Path(item["FilePath"]).exists() for item in card_items)


def test_preservation_checks_and_structural_result_are_passed() -> None:
    probe = _probe()
    preservation = probe["preservation_checks"]
    structural = probe["structural_result"]

    assert preservation["timeline_duration_preserved"] is True
    assert preservation["dialogue_items_preserved"] is True
    assert preservation["native_audio_fields_preserved"] is True
    assert preservation["speaker_preserved"] is True
    assert preservation["direct_yym4_card_object_graph"] is False
    assert preservation["yym4_text_shape_reconstruction"] is False
    assert preservation["external_TTS_introduced"] is False
    assert preservation["render_created"] is False
    assert preservation["media_committed"] is False
    assert structural["patched_ymmp_created_locally"] is True
    assert structural["patched_ymmp_committed"] is False
    assert structural["visual_assets_committed"] is True
    assert structural["card_item_count_added_or_planned"] == 4
    assert structural["placement_structural_readback_status"] == "pass"
    assert structural["next_render_trigger"] == NEXT_DEFAULT_SLICE


def test_placement_operations_are_applied_as_image_asset_imports() -> None:
    operations = _probe()["placement_operations"]

    assert len(operations) == 4
    assert all(operation["applied"] is True for operation in operations)
    assert all(operation["safety_class"] == "diagnostic_only" for operation in operations)
    assert all(operation["asset_path"].endswith(".png") for operation in operations)
    assert all(
        operation["field_changed_or_item_added"] == "Timelines[0].Items[] ImageItem"
        for operation in operations
    )
    assert [(row["start_frame"], row["length_frames"]) for row in operations] == (
        EXPECTED_FRAMES
    )


def test_readiness_and_hygiene_matrices_match_contract_counts() -> None:
    probe = _probe()

    assert probe["readiness_separation"]["next_default_slice"] == NEXT_DEFAULT_SLICE
    assert probe["readiness_separation"]["visual_readiness_progress"] == "6/7"
    assert len(probe["completion_matrix"]) == 6
    assert len(probe["artifact_readiness"]) == 6
    assert len(probe["video_readiness"]) == 7
    assert len(probe["visual_readiness"]) == 7
    assert len(probe["render_gate_hygiene"]) == 6
    assert len(probe["human_burden_hygiene"]) == 7
    assert len(probe["review_non_redundancy"]) == 6
    assert len(probe["inertia_check"]) == 5
    assert probe["inertia_check"][-1] == {
        "gate": "next_concrete_milestone",
        "status": NEXT_DEFAULT_SLICE,
    }


def test_doc_matches_renderer_and_avoids_manual_result_template_requests() -> None:
    probe = _probe()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_yym4_card_asset_placement_probe_markdown(probe)
    assert "probe_status: placed_structurally" in doc_text
    assert "png_export_status: generated" in doc_text
    assert "placement_mode: image_asset_import" in doc_text
    assert "direct_yym4_card_object_graph: false" in doc_text
    assert NEXT_DEFAULT_SLICE in doc_text
    assert ("yes/no" + "/unclear") not in doc_text.lower()
    assert "please render" not in doc_text.lower()
    assert "please check audio" not in doc_text.lower()
    assert ("fixed " + "form") not in doc_text.lower()
    assert _real_url_pattern().search(doc_text) is None


def test_local_ymmp_is_ignored_untracked_and_not_staged() -> None:
    local = _probe()["local_artifact_status"]

    assert local["patched_ymmp_exists_at_readback_generation"] is True
    assert local["patched_ymmp_staged"] is False
    assert local["patched_ymmp_committed"] is False
    assert local["patched_ymmp_ignored"] is True
    for args in [
        ["check-ignore", "-q", "--", DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH.as_posix()],
        ["status", "--short", "--", DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH.as_posix()],
        ["ls-files", "--", DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH.as_posix()],
    ]:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if args[0] == "check-ignore":
            assert result.returncode == 0
        else:
            assert result.stdout == ""


def test_probe_artifacts_have_no_render_outputs_or_real_url_dependencies() -> None:
    probe_text = PROBE_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert _real_url_pattern().search(probe_text) is None
    assert _real_url_pattern().search(doc_text) is None
    assert "public_video_ready\": true" not in probe_text
    assert "production_approval\": true" not in probe_text
    assert not list(PROBE_PATH.parent.glob("*card_asset_placement*.mp4"))
    assert not list(PROBE_PATH.parent.glob("*card_asset_placement*.wav"))
    assert not list(PROBE_PATH.parent.glob("*card_asset_placement*.mp3"))
    assert not list(PROBE_PATH.parent.glob("*card_asset_placement*.m4a"))
