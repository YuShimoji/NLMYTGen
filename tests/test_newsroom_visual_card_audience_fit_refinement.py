import json
import re
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
)
from src.pipeline.newsroom_visual_card_audience_fit_refinement import (
    AUDIENCE_FIT_TOKENS,
    DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_DOC_PATH,
    DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_PATH,
    DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_DOC_PATH,
    DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_PATH,
    NEXT_DEFAULT_SLICE,
    VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_ID,
    VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_SCHEMA_VERSION,
    VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_ID,
    VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_SCHEMA_VERSION,
    _audience_fit_cards_from_source,
    build_default_newsroom_visual_card_audience_fit_refinement,
    build_default_newsroom_visual_card_audience_fit_review_readback,
    render_audience_fit_card_svg,
    render_newsroom_visual_card_audience_fit_refinement_markdown,
    render_newsroom_visual_card_audience_fit_review_readback_markdown,
)
from src.pipeline.newsroom_visual_card_design_refinement import (
    DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH,
)


ROOT = Path(__file__).resolve().parents[1]
READBACK_PATH = ROOT / DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_PATH
READBACK_DOC_PATH = ROOT / DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_DOC_PATH
REFINEMENT_PATH = ROOT / DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_PATH
REFINEMENT_DOC_PATH = ROOT / DEFAULT_VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_DOC_PATH
SOURCE_REFINEMENT_PATH = ROOT / DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH
CONTACT_SHEET_PATH = ROOT / DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH


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


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    assert header[:8] == b"\x89PNG\r\n\x1a\n"
    assert header[12:16] == b"IHDR"
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


def _font_sizes(svg_text: str) -> list[int]:
    return [int(value) for value in re.findall(r'font-size="(\d+)"', svg_text)]


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def _without_svg_namespace(text: str) -> str:
    return text.replace("http://www.w3.org/2000/svg", "")


def test_audience_fit_review_readback_matches_builder_and_normalization() -> None:
    readback = _json(READBACK_PATH)

    assert readback == build_default_newsroom_visual_card_audience_fit_review_readback(
        root=ROOT
    )
    assert readback["readback_id"] == VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_ID
    assert readback["schema_version"] == (
        VISUAL_CARD_AUDIENCE_FIT_REVIEW_READBACK_SCHEMA_VERSION
    )
    assert readback["production_status"] == "diagnostic_only"
    assert readback["internal_review_status"] == "needs_audience_fit_refinement"
    assert readback["source_validation"]["status"] == "passed"
    assert readback["source_validation"]["errors"] == []
    assert readback["accepted_scope"] == {
        "audience_fit_review_captured": True,
        "modern_visual_quality_signal_preserved": True,
        "audience_fit_refinement_axis_selected": True,
        "review_does_not_reopen_timing_audio_or_placement": True,
    }
    assert readback["audience_fit_review_normalization"] == {
        "internal_review_status": "needs_audience_fit_refinement",
        "modern_visual_quality_signal": "positive",
        "small_text_still_present": True,
        "audience_familiarity_mismatch": True,
        "too_saas_dashboard_like": True,
        "mainstream_youtube_visual_language_required": True,
        "production_visual_quality_accepted": False,
        "public_video_ready": False,
        "recommended_next_axis": "visual_card_audience_fit_refinement",
    }


def test_audience_fit_refinement_json_matches_builder_identity_and_next_slice() -> None:
    refinement = _json(REFINEMENT_PATH)
    expected = build_default_newsroom_visual_card_audience_fit_refinement(
        root=ROOT,
        png_export=refinement["raster_export_status"],
    )

    assert refinement == expected
    assert refinement["refinement_id"] == VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_ID
    assert refinement["schema_version"] == (
        VISUAL_CARD_AUDIENCE_FIT_REFINEMENT_SCHEMA_VERSION
    )
    assert refinement["production_status"] == "diagnostic_only"
    assert refinement["refinement_status"] == "assets_regenerated"
    assert refinement["next_recommended_slice"]["slice"] == NEXT_DEFAULT_SLICE
    assert refinement["readiness_separation"]["next_default_slice"] == NEXT_DEFAULT_SLICE
    assert refinement["not_accepted_scope"]["post_audience_fit_render_proof"] is False
    assert refinement["not_accepted_scope"]["public_video_readiness"] is False
    assert refinement["raster_export_status"]["png_export_status"] == "generated"
    assert refinement["raster_export_status"]["rasterization_method"] == (
        "bundled_python_pillow_svg_subset"
    )
    assert refinement["raster_export_status"]["errors"] == []


def test_audience_fit_tokens_and_card_changes_encode_familiar_youtube_language() -> None:
    refinement = _json(REFINEMENT_PATH)
    tokens = refinement["design_token_constraints"]
    changes = refinement["design_changes"]

    assert tokens["canvas_size"] == {"width": 1920, "height": 1080}
    assert tokens["minimum_font_size"] == AUDIENCE_FIT_TOKENS["minimum_font_size"]
    assert tokens["minimum_font_size"] >= 34
    assert tokens["headline_font_size"] == 76
    assert tokens["maximum_copy_font_size"] == 76
    assert tokens["display_number_font_size"] == 132
    assert tokens["maximum_font_size"] == 132
    assert tokens["footer_debug_treatment"] == (
        "removed_from_visible_review_surface"
    )
    assert "familiar_youtube_explainer" in tokens["audience_fit_style"]
    assert tokens["real_brand_or_url_present"] is False
    assert tokens["production_claim_present"] is False

    assert len(changes) == 4
    assert [row["role"] for row in changes] == [
        "intro_summary",
        "handoff_process",
        "claim_check",
        "source_status_next_action",
    ]
    assert [row["role_label"] for row in changes] == [
        "POINT",
        "FLOW",
        "CHECK",
        "NEXT",
    ]
    assert [row["layout_motif"] for row in changes] == [
        "large_number",
        "simple_process_steps",
        "check_warning_box",
        "source_status_panel",
    ]
    assert all(row["text_size_adjustment"] == "minimum visible text raised to 34px" for row in changes)
    assert all(row["type_scale_status"] == "audience_fit_larger_plain" for row in changes)
    assert all(row["variation_status"] == "role_specific_familiar_layout" for row in changes)
    assert all(row["png_valid"] is True for row in changes)
    assert all((row["png_width"], row["png_height"]) == (1920, 1080) for row in changes)


def test_audience_fit_svg_files_are_current_stable_assets() -> None:
    source_refinement = _json(SOURCE_REFINEMENT_PATH)
    cards = _audience_fit_cards_from_source(source_refinement)

    for card in cards:
        svg_path = ROOT / card["output_svg_path"]
        svg_text = svg_path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(svg_text)
        sizes = _font_sizes(svg_text)

        assert svg_text == render_audience_fit_card_svg(card)
        assert root.tag.endswith("svg")
        assert root.attrib["width"] == "1920"
        assert root.attrib["height"] == "1080"
        assert root.attrib["viewBox"] == "0 0 1920 1080"
        assert root.attrib["data-refinement"] == "audience-fit-v1"
        assert root.attrib["data-audience-fit"] == "familiar_youtube_explainer"
        assert root.attrib["data-role"] == card["role"]
        assert root.attrib["data-motif"] == card["layout_motif"]
        assert "REVIEW ONLY" in svg_text
        assert "DIAGNOSTIC" in svg_text
        assert "SUBTITLE AREA" in svg_text
        assert card["review_role_label"] in svg_text
        normalized_svg = svg_text.replace(",", "").replace(".", "")
        for token in str(card["headline"]).replace(",", "").replace(".", "").split():
            assert token in normalized_svg
        assert min(sizes) >= AUDIENCE_FIT_TOKENS["minimum_font_size"]
        assert max(sizes) <= AUDIENCE_FIT_TOKENS["maximum_font_size"]
        assert 'font-size="28"' not in svg_text
        assert 'font-size="30"' not in svg_text
        assert _real_url_pattern().search(_without_svg_namespace(svg_text)) is None


def test_audience_fit_pngs_and_contact_sheet_are_local_and_stable() -> None:
    refinement = _json(REFINEMENT_PATH)
    contact_text = CONTACT_SHEET_PATH.read_text(encoding="utf-8")
    parser = _ImageCollector()

    parser.feed(contact_text)

    assert len(parser.images) == 4
    assert all(
        not src.startswith(("http" + "://", "https" + "://"))
        for src in parser.images
    )
    assert "Newsroom Visual Cards - audience fit v1" in contact_text
    assert "mainstream explainer composition" in contact_text
    assert "No real brands, URLs, media" in contact_text
    assert _real_url_pattern().search(contact_text) is None
    assert parser.images == [
        Path(row["output_svg_path"]).name for row in refinement["design_changes"]
    ]
    for row in refinement["design_changes"]:
        png_path = ROOT / row["output_png_path"]
        assert png_path.exists()
        assert _png_size(png_path) == (1920, 1080)


def test_audience_fit_docs_match_renderers_and_preserve_boundaries() -> None:
    readback = _json(READBACK_PATH)
    refinement = _json(REFINEMENT_PATH)
    readback_doc = READBACK_DOC_PATH.read_text(encoding="utf-8")
    refinement_doc = REFINEMENT_DOC_PATH.read_text(encoding="utf-8")

    assert readback_doc == (
        render_newsroom_visual_card_audience_fit_review_readback_markdown(readback)
    )
    assert refinement_doc == (
        render_newsroom_visual_card_audience_fit_refinement_markdown(refinement)
    )
    for text in [readback_doc, refinement_doc]:
        lowered = text.lower()
        assert ("yes/no" + "/unclear") not in lowered
        assert ("please " + "render") not in lowered
        assert ("render " + "now") not in lowered
        assert ("please check " + "audio") not in lowered
        assert ("fixed " + "form") not in lowered
        assert _real_url_pattern().search(text) is None
        assert ("public_video_ready: " + "true") not in text
        assert ("production_approval: " + "true") not in text
    assert NEXT_DEFAULT_SLICE in refinement_doc


def test_audience_fit_artifacts_have_no_forbidden_media_or_production_leakage() -> None:
    readback_text = READBACK_PATH.read_text(encoding="utf-8")
    refinement_text = REFINEMENT_PATH.read_text(encoding="utf-8")

    for text in [readback_text, refinement_text]:
        assert _real_url_pattern().search(text) is None
        assert "public_video_ready\": true" not in text
        assert "production_approval\": true" not in text
        assert "production_visual_quality_accepted\": true" not in text
    for suffix in ["*.ymmp", "*.mp4", "*.wav", "*.mp3", "*.m4a"]:
        assert not list(READBACK_PATH.parent.glob(f"*audience_fit*{suffix[1:]}"))
