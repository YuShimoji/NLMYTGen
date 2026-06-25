import json
import re
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH,
    DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
    VISUAL_CARD_REFINEMENT_TOKENS,
    render_visual_card_svg,
)
from src.pipeline.newsroom_visual_card_design_refinement import (
    DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_DOC_PATH,
    DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_PATH,
    DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_DOC_PATH,
    DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH,
    INTERNAL_REVIEW_V0_1_RESULT_READBACK_ID,
    INTERNAL_REVIEW_V0_1_RESULT_READBACK_SCHEMA_VERSION,
    NEXT_DEFAULT_SLICE,
    VISUAL_CARD_DESIGN_REFINEMENT_ID,
    VISUAL_CARD_DESIGN_REFINEMENT_SCHEMA_VERSION,
    build_default_newsroom_internal_review_v0_1_result_readback,
    build_default_newsroom_visual_card_design_refinement,
    render_newsroom_internal_review_v0_1_result_readback_markdown,
    render_newsroom_visual_card_design_refinement_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
READBACK_PATH = ROOT / DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_PATH
READBACK_DOC_PATH = ROOT / DEFAULT_INTERNAL_REVIEW_V0_1_RESULT_READBACK_DOC_PATH
REFINEMENT_PATH = ROOT / DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH
REFINEMENT_DOC_PATH = ROOT / DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_DOC_PATH
BRIDGE_PATH = ROOT / DEFAULT_VISUAL_CARD_ASSET_BRIDGE_PATH
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


def test_internal_review_result_readback_matches_builder_and_normalization() -> None:
    readback = _json(READBACK_PATH)

    assert readback == build_default_newsroom_internal_review_v0_1_result_readback(
        root=ROOT
    )
    assert readback["readback_id"] == INTERNAL_REVIEW_V0_1_RESULT_READBACK_ID
    assert readback["schema_version"] == (
        INTERNAL_REVIEW_V0_1_RESULT_READBACK_SCHEMA_VERSION
    )
    assert readback["production_status"] == "diagnostic_only"
    assert readback["internal_review_status"] == "needs_visual_refinement"
    assert readback["mechanics_status"] == "pass"
    assert readback["timing_audio_render_status"] == "diagnostic_pass"
    assert readback["source_validation"]["status"] == "passed"
    assert readback["source_validation"]["errors"] == []

    normalized = readback["internal_review_normalization"]
    assert normalized == {
        "internal_review_status": "needs_visual_refinement",
        "mechanics_status": "pass",
        "timing_audio_render_status": "diagnostic_pass",
        "pacing_density_issue": "known",
        "text_clipping": True,
        "text_wrap_missing": True,
        "min_font_too_small": True,
        "large_font_too_large": True,
        "type_scale_unbalanced": True,
        "overall_readability_low": True,
        "card_variation_insufficient": True,
        "production_visual_quality_accepted": False,
        "public_video_ready": False,
        "recommended_next_axis": "visual_card_design_refinement",
    }
    assert readback["accepted_mechanics"] == {
        "timing": "diagnostic_pass",
        "native_audio": "diagnostic_pass",
        "render": "diagnostic_pass",
        "card_placement": "diagnostic_pass",
    }


def test_visual_refinement_json_matches_builder_identity_and_next_slice() -> None:
    refinement = _json(REFINEMENT_PATH)

    assert refinement == build_default_newsroom_visual_card_design_refinement(root=ROOT)
    assert refinement["refinement_id"] == VISUAL_CARD_DESIGN_REFINEMENT_ID
    assert refinement["schema_version"] == VISUAL_CARD_DESIGN_REFINEMENT_SCHEMA_VERSION
    assert refinement["production_status"] == "diagnostic_only"
    assert refinement["refinement_status"] == "assets_regenerated"
    assert refinement["next_recommended_slice"]["slice"] == NEXT_DEFAULT_SLICE
    assert refinement["readiness_separation"]["next_default_slice"] == (
        NEXT_DEFAULT_SLICE
    )
    assert refinement["not_accepted_scope"]["post_refinement_render_proof"] is False
    assert refinement["not_accepted_scope"]["public_video_readiness"] is False


def test_design_changes_have_wrapping_guards_and_distinct_roles() -> None:
    refinement = _json(REFINEMENT_PATH)
    changes = refinement["design_changes"]

    assert len(changes) == 4
    assert [row["role"] for row in changes] == [
        "intro_summary",
        "handoff_process",
        "claim_check",
        "source_status_next_action",
    ]
    assert [row["layout_motif"] for row in changes] == [
        "summary_stack",
        "process_ladder",
        "check_matrix",
        "status_panel",
    ]
    assert all(row["text_wrap_applied"] is True for row in changes)
    assert all(row["clipping_guard"] is True for row in changes)
    assert all(row["type_scale_status"] == "balanced_diagnostic" for row in changes)
    assert all(row["variation_status"] == "role_specific_layout" for row in changes)
    assert all(row["png_valid"] is True for row in changes)
    assert all((row["png_width"], row["png_height"]) == (1920, 1080) for row in changes)


def test_design_tokens_bound_type_scale_and_safe_area() -> None:
    refinement = _json(REFINEMENT_PATH)
    tokens = refinement["design_token_constraints"]

    assert tokens["canvas_size"] == {"width": 1920, "height": 1080}
    assert tokens["minimum_font_size"] >= 28
    assert tokens["maximum_font_size"] <= 54
    assert tokens["title_font_size"] == VISUAL_CARD_REFINEMENT_TOKENS["title_font_size"]
    assert tokens["body_font_size"] == VISUAL_CARD_REFINEMENT_TOKENS["body_font_size"]
    assert tokens["max_title_lines"] == 2
    assert tokens["body_max_lines"] == 3
    assert tokens["footer_debug_treatment"] == "removed_from_review_surface"
    assert tokens["real_brand_or_url_present"] is False
    assert tokens["production_claim_present"] is False
    assert tokens["subtitle_safe_reserve"]["y"] >= 800


def test_refined_svg_files_are_parseable_wrapped_and_font_bounded() -> None:
    bridge = _json(BRIDGE_PATH)
    minimum = VISUAL_CARD_REFINEMENT_TOKENS["minimum_font_size"]
    maximum = VISUAL_CARD_REFINEMENT_TOKENS["maximum_font_size"]

    for asset in bridge["assets"]:
        svg_path = ROOT / asset["repo_relative_path"]
        svg_text = svg_path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(svg_text)
        sizes = _font_sizes(svg_text)

        assert svg_text == render_visual_card_svg(asset)
        assert root.tag.endswith("svg")
        assert root.attrib["width"] == "1920"
        assert root.attrib["height"] == "1080"
        assert root.attrib["viewBox"] == "0 0 1920 1080"
        assert root.attrib["data-refinement"] == "v1"
        assert root.attrib["data-role"] == asset["design_refinement_role"]
        assert root.attrib["data-motif"] == asset["layout_motif"]
        assert min(sizes) >= minimum
        assert max(sizes) <= maximum
        assert 'font-size="82"' not in svg_text
        assert "SUBTITLE-SAFE RESERVE" in svg_text
        assert "DIAGNOSTIC" in svg_text
        assert "FAKE CONTENT" in svg_text
        assert asset["review_role_label"] in svg_text
        assert _real_url_pattern().search(svg_text.replace("http://www.w3.org/2000/svg", "")) is None


def test_refined_pngs_and_contact_sheet_are_local_and_stable() -> None:
    refinement = _json(REFINEMENT_PATH)
    contact_text = CONTACT_SHEET_PATH.read_text(encoding="utf-8")
    parser = _ImageCollector()

    parser.feed(contact_text)

    assert len(parser.images) == 4
    assert all(
        not src.startswith(("http" + "://", "https" + "://"))
        for src in parser.images
    )
    assert "Newsroom Visual Card Asset Bridge v1 - refined" in contact_text
    assert "role-specific motifs" in contact_text
    assert _real_url_pattern().search(contact_text) is None
    for row in refinement["design_changes"]:
        png_path = ROOT / row["output_png_path"]
        assert png_path.exists()
        assert _png_size(png_path) == (1920, 1080)


def test_refinement_docs_match_renderers_and_preserve_boundaries() -> None:
    readback = _json(READBACK_PATH)
    refinement = _json(REFINEMENT_PATH)
    readback_doc = READBACK_DOC_PATH.read_text(encoding="utf-8")
    refinement_doc = REFINEMENT_DOC_PATH.read_text(encoding="utf-8")

    assert readback_doc == render_newsroom_internal_review_v0_1_result_readback_markdown(
        readback
    )
    assert refinement_doc == render_newsroom_visual_card_design_refinement_markdown(
        refinement
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


def test_refinement_artifacts_have_no_forbidden_media_or_production_leakage() -> None:
    readback_text = READBACK_PATH.read_text(encoding="utf-8")
    refinement_text = REFINEMENT_PATH.read_text(encoding="utf-8")

    for text in [readback_text, refinement_text]:
        assert _real_url_pattern().search(text) is None
        assert "public_video_ready\": true" not in text
        assert "production_approval\": true" not in text
        assert "production_visual_quality_accepted\": true" not in text
    assert not list(READBACK_PATH.parent.glob("*visual_card_design_refinement*.ymmp"))
    assert not list(READBACK_PATH.parent.glob("*visual_card_design_refinement*.mp4"))
    assert not list(READBACK_PATH.parent.glob("*visual_card_design_refinement*.wav"))
    assert not list(READBACK_PATH.parent.glob("*visual_card_design_refinement*.mp3"))
    assert not list(READBACK_PATH.parent.glob("*visual_card_design_refinement*.m4a"))
