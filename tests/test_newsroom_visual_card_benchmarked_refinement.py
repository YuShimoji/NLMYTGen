import json
import re
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_CONTACT_SHEET_PATH,
)
from src.pipeline.newsroom_visual_card_benchmarked_refinement import (
    DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_DOC_PATH,
    DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH,
    NEXT_DEFAULT_SLICE,
    VISUAL_CARD_BENCHMARKED_REFINEMENT_ID,
    VISUAL_CARD_BENCHMARKED_REFINEMENT_SCHEMA_VERSION,
    build_default_newsroom_visual_card_benchmarked_refinement,
    render_newsroom_visual_card_benchmarked_refinement_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
REFINEMENT_PATH = ROOT / DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH
REFINEMENT_DOC_PATH = ROOT / DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_DOC_PATH
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


def test_benchmarked_refinement_json_matches_builder_and_identity() -> None:
    refinement = _json(REFINEMENT_PATH)

    assert refinement == build_default_newsroom_visual_card_benchmarked_refinement(
        root=ROOT
    )
    assert refinement["refinement_id"] == VISUAL_CARD_BENCHMARKED_REFINEMENT_ID
    assert refinement["schema_version"] == (
        VISUAL_CARD_BENCHMARKED_REFINEMENT_SCHEMA_VERSION
    )
    assert refinement["production_status"] == "diagnostic_only"
    assert refinement["refinement_status"] == "benchmarked_text_fit_improved"
    assert refinement["source_validation"]["status"] == "passed"
    assert refinement["source_validation"]["errors"] == []
    assert refinement["next_recommended_slice"]["slice"] == NEXT_DEFAULT_SLICE
    assert refinement["audience_acceptance_claimed"] is False


def test_failure_to_fix_map_and_proxy_recheck_preserve_benchmark_boundaries() -> None:
    refinement = _json(REFINEMENT_PATH)
    failure_map = {
        row["source_metric_id"]: row for row in refinement["failure_to_fix_map"]
    }
    proxy = refinement["local_proxy_recheck"]

    assert failure_map["text_clipping_or_wrapping"]["prior_result"] == "fail"
    assert failure_map["text_clipping_or_wrapping"]["current_proxy_result"] == "pass"
    assert failure_map["readability_at_a_glance"]["prior_result"] == "warning"
    assert failure_map["readability_at_a_glance"]["current_proxy_result"] == "pass"
    assert failure_map["no_reliance_on_tiny_metadata"]["current_proxy_result"] == "pass"
    assert (
        failure_map["pacing_density_for_68_sec_video"]["current_proxy_result"]
        == "warning_deferred_to_render_smoke"
    )

    assert proxy["proxy_status"] == "improved_no_material_static_failures"
    assert proxy["fail_count"] == 0
    assert proxy["warning_count"] == 2
    assert proxy["render_or_yym4_checked"] is False
    assert proxy["external_reference_or_audience_checked"] is False
    assert refinement["not_accepted_scope"]["YMM4_launch_or_render"] is False
    assert refinement["not_accepted_scope"]["audience_acceptance"] is False
    assert refinement["not_accepted_scope"]["public_video_readiness"] is False


def test_per_card_changes_and_svg_assets_encode_benchmarked_text_fit() -> None:
    refinement = _json(REFINEMENT_PATH)
    changes = {row["display_order"]: row for row in refinement["per_card_changes"]}

    assert changes[1]["headline_lines"] == ["Fake topic, review", "only."]
    assert changes[2]["headline_lines"] == ["Review-only", "handoff stays."]
    assert changes[3]["headline_lines"] == ["A fake claim is", "shown."]
    assert changes[3]["body_lines"] == [
        "Plain check and caution",
        "boxes make the fake status",
        "obvious.",
    ]
    assert changes[4]["headline_lines"] == ["Fake source checks", "are noted."]
    assert changes[4]["body_lines"] == [
        "Status and next-action",
        "panels stay large and",
        "familiar.",
    ]

    for order, row in changes.items():
        svg_path = ROOT / row["output_svg_path"]
        svg_text = svg_path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(svg_text)

        assert root.attrib["width"] == "1920"
        assert root.attrib["height"] == "1080"
        assert root.attrib["data-refinement"] == "audience-fit-v1"
        assert row["stable_asset_paths_preserved"] is True
        assert row["headline_wrap_verified"] is True
        assert row["body_wrap_verified"] is True
        assert row["source_display_label"] == f"SRC {order}/4"
        assert f"SRC {order}/4" in svg_text
        assert "SOURCE:" not in svg_text
        assert "cap_beat_fake" not in svg_text
        assert _real_url_pattern().search(_without_svg_namespace(svg_text)) is None
        assert _png_size(ROOT / row["output_png_path"]) == (1920, 1080)


def test_design_constraints_and_docs_match_renderer() -> None:
    refinement = _json(REFINEMENT_PATH)
    doc_text = REFINEMENT_DOC_PATH.read_text(encoding="utf-8")
    constraints = refinement["design_constraints"]

    assert doc_text == render_newsroom_visual_card_benchmarked_refinement_markdown(
        refinement
    )
    assert constraints["stable_asset_paths"] is True
    assert constraints["card_count"] == 4
    assert constraints["headline_wrap_chars"] == 18
    assert constraints["headline_max_lines"] == 2
    assert constraints["body_wrap_chars"] == 27
    assert constraints["body_max_lines"] == 3
    assert constraints["minimum_meaningful_font_size"] >= 34
    assert constraints["source_display_format"] == "SRC N/4"
    assert "actual_audience_acceptance: True" not in doc_text
    assert "production_approval: True" not in doc_text
    assert "public_video_ready: True" not in doc_text
    assert _real_url_pattern().search(doc_text) is None


def test_contact_sheet_is_local_and_mentions_benchmarked_wraps() -> None:
    refinement = _json(REFINEMENT_PATH)
    contact_text = CONTACT_SHEET_PATH.read_text(encoding="utf-8")
    parser = _ImageCollector()

    parser.feed(contact_text)

    assert len(parser.images) == 4
    assert all(not src.startswith(("http" + "://", "https" + "://")) for src in parser.images)
    assert "Newsroom Visual Cards - audience fit v1" in contact_text
    assert "benchmarked text-fit wraps" in contact_text
    assert "No real brands, URLs, media" in contact_text
    assert parser.images == [
        Path(row["output_svg_path"]).name for row in refinement["per_card_changes"]
    ]
    assert _real_url_pattern().search(contact_text) is None
