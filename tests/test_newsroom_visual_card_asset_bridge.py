import json
import re
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_ASSET_BRIDGE_DOC_PATH,
    DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH,
    DEFAULT_VISUAL_CARD_ASSET_DIR,
    DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
    NEXT_DEFAULT_SLICE,
    NEXT_RENDER_SMOKE_SLICE,
    VISUAL_CARD_ASSET_BRIDGE_ID,
    VISUAL_CARD_ASSET_BRIDGE_SCHEMA_VERSION,
    build_default_newsroom_visual_card_asset_bridge,
    render_newsroom_visual_card_asset_bridge_markdown,
    render_visual_card_contact_sheet_html,
    render_visual_card_svg,
)


ROOT = Path(__file__).resolve().parents[1]
BRIDGE_PATH = ROOT / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH
DOC_PATH = ROOT / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_DOC_PATH
CARD_DIR = ROOT / DEFAULT_VISUAL_CARD_ASSET_DIR
CONTACT_SHEET_PATH = ROOT / DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH
EXPECTED_TEXTS = [
    "Fake topic, review only.",
    "Review-only handoff stays.",
    "A fake claim is shown.",
    "Fake source checks are noted.",
]
EXPECTED_TIMINGS = [(0, 12), (12, 24), (24, 46), (46, 68)]


class _ImageCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "img":
            return
        attr_map = {key: value for key, value in attrs}
        src = attr_map.get("src")
        if src is not None:
            self.images.append(src)


def _bridge() -> dict:
    return json.loads(BRIDGE_PATH.read_text(encoding="utf-8"))


def _real_url_matches(text: str) -> list[str]:
    pattern = re.compile(r"https?://|www\.", flags=re.IGNORECASE)
    return [
        match.group(0)
        for match in pattern.finditer(text)
        if "w3.org/2000/svg" not in text[max(0, match.start() - 16): match.end() + 32]
    ]


def test_bridge_json_matches_builder_output_and_identity() -> None:
    bridge = _bridge()

    assert bridge == build_default_newsroom_visual_card_asset_bridge(root=ROOT)
    assert bridge["artifact_id"] == VISUAL_CARD_ASSET_BRIDGE_ID
    assert bridge["bridge_id"] == VISUAL_CARD_ASSET_BRIDGE_ID
    assert bridge["schema_version"] == VISUAL_CARD_ASSET_BRIDGE_SCHEMA_VERSION
    assert bridge["review_status"] == "ready_for_supervisor_review"
    assert bridge["production_status"] == "diagnostic_only"
    assert bridge["visual_status"] == "asset_bridge_created"
    assert bridge["preview_status"] == "preview_only"
    assert bridge["png_export_status"] == "png_export_deferred"
    assert bridge["diagnostic_only"] is True


def test_source_validation_reuses_render_smoke_timing_audio_and_caption_rows() -> None:
    bridge = _bridge()
    validation = bridge["source_validation"]
    source_state = bridge["source_state"]

    assert validation["status"] == "passed"
    assert validation["errors"] == []
    assert validation["render_smoke_result"] == "pass"
    assert validation["duration_sec"] == 68
    assert validation["caption_item_count"] == 4
    assert validation["card_asset_count"] == 4
    assert validation["canonical_speaker"] == "yukkuri_reimu"
    assert validation["canonical_speaker_unicode_escape"] == (
        "\\u3086\\u3063\\u304f\\u308a\\u970a\\u5922"
    )
    assert source_state["render_smoke_result"] == "pass"
    assert source_state["duration_sec"] == 68
    assert source_state["native_audio_status"] == "diagnostic_pass"
    assert source_state["timing_patch_status"] == "diagnostic_pass"
    assert source_state["current_visual_state"] == "sparse_text_on_black"
    assert source_state["public_video_ready"] is False


def test_card_assets_map_one_to_each_existing_caption_unit() -> None:
    bridge = _bridge()
    assets = bridge["assets"]

    assert len(assets) == 4
    assert [asset["text"] for asset in assets] == EXPECTED_TEXTS
    assert [
        (asset["intended_start_sec"], asset["intended_end_sec"])
        for asset in assets
    ] == EXPECTED_TIMINGS
    assert [asset["asset_type"] for asset in assets] == ["svg"] * 4
    assert [asset["display_order"] for asset in assets] == [1, 2, 3, 4]
    assert all(asset["review_status"] == "diagnostic_only" for asset in assets)
    assert all(asset["fake_content_only"] is True for asset in assets)
    assert all(asset["contains_real_urls"] is False for asset in assets)
    assert all(asset["contains_real_brands"] is False for asset in assets)
    assert all(asset["external_dependencies"] is False for asset in assets)
    assert all(asset["intended_layer"] == 2 for asset in assets)
    assert all(
        asset["placement_role"] == "diagnostic_visual_card_image_asset"
        for asset in assets
    )
    assert all(asset["repo_relative_path"].endswith(".svg") for asset in assets)


def test_svg_card_files_are_deterministic_parseable_and_subtitle_safe() -> None:
    bridge = _bridge()

    for asset in bridge["assets"]:
        svg_path = ROOT / asset["repo_relative_path"]
        svg_text = svg_path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(svg_text)

        assert svg_text == render_visual_card_svg(asset)
        assert root.tag.endswith("svg")
        assert root.attrib["width"] == "1920"
        assert root.attrib["height"] == "1080"
        assert root.attrib["viewBox"] == "0 0 1920 1080"
        assert asset["text"] in svg_text
        assert "SUBTITLE-SAFE RESERVE" in svg_text
        assert "DIAGNOSTIC" in svg_text
        assert "FAKE CONTENT" in svg_text
        assert _real_url_matches(svg_text) == []
        assert "public_video_ready: true" not in svg_text
        assert "production_approval: true" not in svg_text
        reserve = asset["subtitle_safe_lower_area"]
        assert reserve["reserved"] is True
        assert reserve["y"] >= 760


def test_contact_sheet_html_is_local_parseable_and_references_four_cards() -> None:
    bridge = _bridge()
    html_text = CONTACT_SHEET_PATH.read_text(encoding="utf-8")
    parser = _ImageCollector()

    parser.feed(html_text)

    assert html_text == render_visual_card_contact_sheet_html(bridge)
    assert len(parser.images) == 4
    assert parser.images == [
        Path(asset["repo_relative_path"]).name for asset in bridge["assets"]
    ]
    assert all(not src.startswith(("http://", "https://")) for src in parser.images)
    assert _real_url_matches(html_text) == []
    assert "No real brands" in html_text
    assert "production approval" in html_text


def test_bridge_accepted_not_accepted_and_placement_contract_are_separated() -> None:
    bridge = _bridge()
    placement = bridge["placement_contract"]

    assert bridge["accepted_scope"] == {
        "external_visual_card_assets_created": True,
        "preview_contact_sheet_created": True,
        "mapped_to_existing_dialogue_caption_units": True,
        "suitable_for_later_yym4_placement_probe": True,
        "diagnostic_fake_content_safe": True,
        "subtitle_safe_lower_area_reserved": True,
    }
    assert bridge["not_accepted_scope"] == {
        "production_visual_quality": False,
        "final_design_system": False,
        "YMM4_placement_proof": False,
        "post_card_render_proof": False,
        "public_video_readiness": False,
        "real_newsroom_visuals": False,
        "real_content_readiness": False,
        "production_approval": False,
    }
    assert placement["future_yym4_placement_mode"] == "image_asset_import"
    assert placement["direct_yym4_card_object_graph"] is False
    assert placement["yym4_text_shape_reconstruction"] is False
    assert placement["preserves_native_audio_path"] is True
    assert placement["preserves_existing_timing_strategy"] is True
    assert placement["render_required_now"] is False
    assert placement["YMM4_launch_required_now"] is False
    assert placement["ymmp_edit_required_now"] is False
    assert placement["next_render_should_be_milestone_gated"] is True


def test_readiness_separation_and_next_slices_name_the_next_milestone() -> None:
    bridge = _bridge()
    readiness = bridge["readiness_separation"]
    next_slices = bridge["recommended_next_slices"]

    assert readiness["slice_completion"] == "pass_for_this_asset_bridge"
    assert readiness["video_readiness_progress"] == "6/7"
    assert readiness["visual_readiness_progress"] == "4/7"
    assert readiness["production_readiness"] == "low_diagnostic_only"
    assert readiness["next_default_slice"] == NEXT_DEFAULT_SLICE
    assert [row["slice"] for row in next_slices] == [
        NEXT_DEFAULT_SLICE,
        NEXT_RENDER_SMOKE_SLICE,
        "newsroom-internal-review-v0.1-prep",
        "newsroom-render-output-retention-policy-v1",
    ]
    assert next_slices[0]["timing"] == "recommended_next_default"
    assert "image-asset placement" in next_slices[0]["reason"]


def test_completion_matrices_and_hygiene_match_contract_counts() -> None:
    bridge = _bridge()

    assert len(bridge["completion_matrix"]) == 6
    assert len(bridge["artifact_readiness"]) == 6
    assert len(bridge["video_readiness"]) == 7
    assert len(bridge["visual_readiness"]) == 7
    assert len(bridge["render_gate_hygiene"]) == 6
    assert len(bridge["human_burden_hygiene"]) == 7
    assert len(bridge["review_non_redundancy"]) == 6
    assert len(bridge["inertia_check"]) == 5
    assert [row["status"] for row in bridge["video_readiness"]] == [
        True,
        True,
        True,
        True,
        True,
        True,
        False,
    ]
    assert [row["status"] for row in bridge["visual_readiness"]] == [
        True,
        True,
        True,
        True,
        True,
        False,
        False,
    ]
    assert bridge["inertia_check"][-1] == {
        "gate": "next_concrete_milestone",
        "status": NEXT_DEFAULT_SLICE,
    }


def test_doc_matches_renderer_and_avoids_fixed_form_or_render_repetition() -> None:
    bridge = _bridge()
    doc_text = DOC_PATH.read_text(encoding="utf-8")

    assert doc_text == render_newsroom_visual_card_asset_bridge_markdown(bridge)
    assert "visual_status: asset_bridge_created" in doc_text
    assert "png_export_status: png_export_deferred" in doc_text
    assert NEXT_DEFAULT_SLICE in doc_text
    assert "future_yym4_placement_mode: image_asset_import" in doc_text
    assert "direct_yym4_card_object_graph: false" in doc_text
    assert "yes/no/unclear" not in doc_text.lower()
    assert "please render" not in doc_text.lower()
    assert "render now" not in doc_text.lower()
    assert "please check audio" not in doc_text.lower()
    assert "fixed form" not in doc_text.lower()
    assert _real_url_matches(doc_text) == []


def test_generated_bridge_artifacts_have_no_forbidden_media_outputs() -> None:
    bridge_text = BRIDGE_PATH.read_text(encoding="utf-8")
    doc_text = DOC_PATH.read_text(encoding="utf-8")
    contact_text = CONTACT_SHEET_PATH.read_text(encoding="utf-8")
    placement_probe_path = (
        ROOT
        / "samples/_probe/newsroom_handoff/yym4_card_asset_placement_probe_v1.json"
    )
    png_cards = sorted(CARD_DIR.glob("*.png"))

    assert _real_url_matches(bridge_text) == []
    assert _real_url_matches(doc_text) == []
    assert _real_url_matches(contact_text) == []
    assert "production_approval\": true" not in bridge_text
    assert "public_video_ready\": true" not in bridge_text
    assert "real_newsroom_visuals\": true" not in bridge_text
    assert not list(CARD_DIR.glob("*.ymmp"))
    assert not list(CARD_DIR.glob("*.mp4"))
    assert not list(CARD_DIR.glob("*.wav"))
    assert not list(CARD_DIR.glob("*.mp3"))
    assert not list(CARD_DIR.glob("*.m4a"))
    if placement_probe_path.exists():
        assert len(png_cards) == 4
    else:
        assert not png_cards
    assert _bridge()["png_export_status"] == "png_export_deferred"
