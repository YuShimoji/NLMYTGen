import json
import re
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
)
from src.pipeline.newsroom_visual_card_density_benchmarked_refinement import (
    DEFAULT_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_DOC_PATH,
    DEFAULT_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_PATH,
    NEXT_DEFAULT_SLICE,
    VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_ID,
    VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_SCHEMA_VERSION,
    build_default_newsroom_visual_card_density_benchmarked_refinement,
    render_newsroom_visual_card_density_benchmarked_refinement_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
REFINEMENT_PATH = ROOT / DEFAULT_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_PATH
REFINEMENT_DOC_PATH = (
    ROOT / DEFAULT_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_DOC_PATH
)
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


def _real_url_pattern() -> re.Pattern[str]:
    protocol_pattern = "http" + "s?://"
    host_pattern = ("w" * 3) + r"\."
    return re.compile(f"{protocol_pattern}|{host_pattern}", flags=re.IGNORECASE)


def _without_svg_namespace(text: str) -> str:
    return text.replace("http://www.w3.org/2000/svg", "")


def test_density_refinement_json_matches_builder_and_identity() -> None:
    refinement = _json(REFINEMENT_PATH)
    deterministic_refinement = dict(refinement)
    deterministic_refinement.pop("png_export", None)

    assert deterministic_refinement == build_default_newsroom_visual_card_density_benchmarked_refinement(
        root=ROOT
    )
    assert refinement["refinement_id"] == VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_ID
    assert refinement["schema_version"] == (
        VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_SCHEMA_VERSION
    )
    assert refinement["refinement_status"] == "density_benchmark_materially_improved"
    assert refinement["production_status"] == "diagnostic_only"
    assert refinement["visual_work_class"] == "audience_fit"
    assert refinement["refinement_type"] == "density_benchmark_linked"
    assert refinement["actual_audience_acceptance_claimed"] is False
    assert refinement["source_validation"]["status"] == "passed"
    assert refinement["source_validation"]["errors"] == []


def test_density_fix_map_and_design_constraints_apply_spec_rules() -> None:
    refinement = _json(REFINEMENT_PATH)
    rules = {row["rule_id"]: row for row in refinement["density_fix_map"]}
    constraints = refinement["design_constraints"]

    assert rules["one_dominant_message_per_card"]["status"] == "applied"
    assert rules["remove_nonessential_microcopy"]["operation"] == "remove"
    assert rules["merge_repeated_labels"]["operation"] == "merge"
    assert rules["demote_source_debug_metadata"]["operation"] == "demote"
    assert rules["increase_whitespace_around_essential_text"]["operation"] == "enlarge"
    assert constraints["canvas_size"] == {"width": 1920, "height": 1080}
    assert constraints["minimum_meaningful_font_size"] >= 42
    assert constraints["max_headlines"] == 1
    assert constraints["max_primary_sentences"] == 1
    assert constraints["max_support_notes_or_diagrams"] == 1
    assert constraints["max_meaningful_labels"] == 3
    assert constraints["no_real_brand_or_url"] is True
    assert constraints["production_claim_present"] is False


def test_per_card_changes_preserve_messages_and_stable_asset_paths() -> None:
    refinement = _json(REFINEMENT_PATH)
    changes = {row["display_order"]: row for row in refinement["per_card_changes"]}

    assert len(changes) == 4
    assert changes[1]["essential_message_preserved"] == (
        "fake topic is review-only and the card is a plain point summary"
    )
    assert "secondary POINT mini panel" in changes[1]["removed_or_demoted_elements"]
    assert "no extra flow badge" in changes[2]["simplified_elements"]
    assert "RESULT box" in changes[3]["removed_or_demoted_elements"]
    assert "source-check awareness" in changes[4]["elements_that_must_stay"]

    for row in changes.values():
        assert row["text_density_change"] == "reduced"
        assert row["label_count_after"] < row["label_count_before"]
        assert row["label_count_after"] <= 3
        assert row["small_metadata_dependency_reduced"] is True
        assert row["dominant_message_status"] == "single_primary_reading_path"
        assert row["stable_asset_paths_preserved"] is True
        assert row["svg_matches_current_renderer"] is True
        assert row["svg_parse_valid"] is True
        assert row["source_debug_demoted"] is True
        assert row["boundary_visible"] is True
        assert row["no_real_url_or_www_visible"] is True
        assert _png_size(ROOT / row["output_png_path"]) == (1920, 1080)


def test_generated_svgs_are_density_refined_and_do_not_use_real_urls() -> None:
    refinement = _json(REFINEMENT_PATH)

    for row in refinement["per_card_changes"]:
        svg_path = ROOT / row["output_svg_path"]
        svg_text = svg_path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(svg_text)

        assert root.attrib["width"] == "1920"
        assert root.attrib["height"] == "1080"
        assert root.attrib["data-refinement"] == "density-benchmarked-v1"
        assert "REVIEW ONLY / DIAGNOSTIC" in svg_text
        assert "SUBTITLE AREA" in svg_text
        assert "SOURCE:" not in svg_text
        assert "NO REAL NEWS CLAIM" not in svg_text
        assert "SIMPLE FLOW" not in svg_text
        assert _real_url_pattern().search(_without_svg_namespace(svg_text)) is None

        card = next(
            item
            for item in build_default_newsroom_visual_card_density_benchmarked_refinement(
                root=ROOT
            )["per_card_changes"]
            if item["card_id"] == row["card_id"]
        )
        assert card["svg_matches_current_renderer"] is True


def test_proxy_recheck_and_next_slice_are_ready_for_render_smoke() -> None:
    refinement = _json(REFINEMENT_PATH)
    proxy = refinement["local_proxy_recheck"]
    metrics = {row["metric_id"]: row for row in proxy["metric_results"]}

    assert refinement["png_export"]["png_export_status"] == "generated"
    assert refinement["png_export"]["png_file_count"] == 4
    assert refinement["png_export"]["errors"] == []
    assert proxy["proxy_status"] == "materially_improved"
    assert proxy["fail_count"] == 0
    assert proxy["material_density_change"] is True
    assert metrics["one_dominant_message_per_card"]["result"] == "pass"
    assert metrics["no_reliance_on_tiny_metadata"]["result"] == "pass"
    assert metrics["information_density_high"]["result"] == "pass"
    assert metrics["cognitive_load_high"]["result"] == "pass"
    assert metrics["glance_readability"]["result"] == "pass"
    assert metrics["text_fit_tight_warning"]["result"] == "pass"
    assert metrics["diagnostic_boundary_visibility"]["result"] == "pass"
    assert refinement["next_recommended_slice"]["slice"] == NEXT_DEFAULT_SLICE
    assert refinement["accepted_scope"]["ready_for_post_density_refinement_render_smoke"] is True
    assert refinement["not_accepted_scope"]["actual_audience_acceptance"] is False
    assert refinement["not_accepted_scope"]["post_density_refinement_render_proof"] is False


def test_doc_and_contact_sheet_match_expected_outputs() -> None:
    refinement = _json(REFINEMENT_PATH)
    doc_text = REFINEMENT_DOC_PATH.read_text(encoding="utf-8")
    contact_text = CONTACT_SHEET_PATH.read_text(encoding="utf-8")
    parser = _ImageCollector()

    parser.feed(contact_text)

    assert doc_text == render_newsroom_visual_card_density_benchmarked_refinement_markdown(
        refinement
    )
    assert len(parser.images) == 4
    assert all(not src.startswith(("http" + "://", "https" + "://")) for src in parser.images)
    assert "Newsroom Visual Cards - density refined v1" in contact_text
    assert "No real brands" not in contact_text
    assert "real brands" in contact_text
    assert _real_url_pattern().search(contact_text) is None
    assert "actual_audience_acceptance_claimed: True" not in doc_text
    assert "production_approval: True" not in doc_text
    assert "public_video_ready: True" not in doc_text
