from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from src.pipeline.new_banknote_reference_layout_reconstruction import (
    BASE_REVISION,
    DESIGN_ID,
    KEYFRAME_SPECS,
    REJECTED_PROOF_TREE_OID,
    ROUTE_A_TREE_OID,
    STATE_ID,
    build_reference_layout_reconstruction,
)


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
OUTPUT = PILOT / "reference_layout_reconstruction"
ROUTE_A = PILOT / "route_a_visual_proof"
REJECTED = PILOT / "reference_grounded_visual_design"
EXPECTED_PROOF = (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001/"
    "reference_layout_reconstruction/reference_layout_proof.html"
)


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def _visible_svg_text(path: Path) -> str:
    return "".join(
        value.strip()
        for value in ElementTree.parse(path).getroot().itertext()
        if value.strip()
    )


def _file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): _sha(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class _ResourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.resources: list[str] = []
        self.tags: list[str] = []
        self.classes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.tags.append(tag)
        self.classes.extend(str(values.get("class") or "").split())
        if tag in {"img", "script", "link", "iframe", "audio", "video", "source"}:
            resource = values.get("src") or values.get("href")
            if resource:
                self.resources.append(resource)


def test_exact_base_and_all_preexisting_pilot_content_are_unchanged() -> None:
    assert _git("merge-base", "HEAD", BASE_REVISION) == BASE_REVISION
    approval = _load(PILOT / "human_script_approval_receipt.json")
    assert len(approval["approved_file_hashes"]) == 8
    for relative, expected in approval["approved_file_hashes"].items():
        assert _sha(PILOT / relative) == expected

    pilot_prefix = PILOT.relative_to(ROOT).as_posix()
    ignore_path = f"{pilot_prefix}/.gitignore"
    base_files = _git("ls-tree", "-r", "--name-only", BASE_REVISION, "--", pilot_prefix).splitlines()
    for relative in base_files:
        if relative == ignore_path:
            continue
        assert (ROOT / relative).is_file()
        assert _git("hash-object", "--", relative) == _git(
            "rev-parse", f"{BASE_REVISION}:{relative}"
        )

    route_path = ROUTE_A.relative_to(ROOT).as_posix()
    rejected_path = REJECTED.relative_to(ROOT).as_posix()
    assert _git("rev-parse", f"{BASE_REVISION}:{route_path}") == ROUTE_A_TREE_OID
    assert _git("rev-parse", f"{BASE_REVISION}:{rejected_path}") == REJECTED_PROOF_TREE_OID
    assert _git("rev-parse", f"HEAD:{route_path}") == ROUTE_A_TREE_OID
    assert _git("rev-parse", f"HEAD:{rejected_path}") == REJECTED_PROOF_TREE_OID


def test_supersession_receipt_and_ai_template_audit_are_complete() -> None:
    receipt = _load(OUTPUT / "current_chatgpt_style_supersession_receipt.json")
    assert receipt["status"] == "reference_researched_but_ai_template_presentation_rejected"
    assert receipt["current_visual_authority"] is False
    assert receipt["historical_evidence"] is True
    assert receipt["protected_historical_tree_oid"] == REJECTED_PROOF_TREE_OID
    assert receipt["earlier_ai_original_tree_oid"] == ROUTE_A_TREE_OID
    assert receipt["replacement_design_id"] == DESIGN_ID

    audit = (OUTPUT / "current_chatgpt_style_deviation_report.md").read_text(encoding="utf-8")
    required = {
        "hero heading",
        "English eyebrow",
        "count pills",
        "Authority card",
        "rounded two-column gallery",
        "nested frame cards",
        "palette",
        "typography scale",
        "whitespace and marketing-page hierarchy",
        "meta-status copy",
        "viewer-frame miniaturization",
        "circular icon grammar",
        "reference metadata placement",
    }
    assert all(item in audit for item in required)
    assert REJECTED_PROOF_TREE_OID in audit
    assert "replace" in audit


def test_six_actual_surface_traces_cover_all_cohorts_and_visual_geometry() -> None:
    registry = _load(OUTPUT / "reference_layout_trace_registry.json")
    matrix = _load(OUTPUT / "reference_layout_trace_matrix.json")
    traces = registry["traces"]
    assert registry["status"] == "tracing_complete_before_replacement_design"
    assert registry["trace_count"] == len(traces) == 6
    assert registry["cohort_counts"] == {
        "official_educational": 2,
        "journalism_documentary": 2,
        "yukkuri_adjacent_explainer": 2,
    }
    assert registry["tracing_completed_at"] < registry["design_generation_started_at"]
    assert len({row["publisher"] for row in traces}) == 6
    assert matrix["checks"] == {
        "visual_wireframe_per_trace": True,
        "actual_surface_per_trace": True,
        "source_specific_branding_separated": True,
        "minimum_two_per_cohort": True,
    }
    bounds = matrix["bounds_fields"]
    for trace in traces:
        assert trace["evidence_class"] in {"page_or_frame_observed", "in_video_frame_observed"}
        assert trace["inspected_surface"]
        assert trace["dominant_visual_weight"]
        assert trace["simultaneous_focal_regions"] in {1, 2}
        assert trace["motion_state"]
        assert trace["source_specific_exclusions"]
        assert trace["shared_patterns"]
        assert trace["confidence"]
        assert any(trace[field] for field in bounds)
        assert (OUTPUT / trace["local_capture"]).is_file()
        trace_svg = OUTPUT / "traces" / f'{trace["trace_id"]}.svg'
        root = ElementTree.parse(trace_svg).getroot()
        assert root.attrib["viewBox"] == "0 0 1920 1080"
        assert root.attrib["data-trace-id"] == trace["trace_id"]


def test_shared_grammar_and_decision_lineage_are_thresholded() -> None:
    grammar = _load(OUTPUT / "reference_layout_shared_grammar.json")
    assert grammar["derivation_boundary"].endswith("tracings were completed and inspected")
    assert all(grammar["checks"].values())
    for pattern in grammar["patterns"]:
        assert pattern["passed"] is True
        assert len(pattern["supporting_trace_ids"]) >= 3
        assert len(pattern["cohorts"]) >= 2

    lineage = _load(OUTPUT / "reference_layout_decision_lineage.json")
    assert lineage["major_decision_count"] == lineage["covered_major_decision_count"] == 10
    assert lineage["coverage_ratio"] == 1.0
    assert lineage["source_dominance"]["rule_maximum"] == 0.4
    assert lineage["source_dominance"]["maximum_observed_share"] <= 0.4
    assert lineage["source_dominance"]["passed"] is True
    for decision in lineage["decisions"]:
        assert decision["selected_structure"]
        assert decision["shared_pattern_threshold_result"]
        assert decision["source_specific_elements_rejected"]
        assert decision["ai_original_contribution"].startswith("none")
        assert decision["human_approval_status"] == "pending"
        if not decision["supporting_trace_ids"]:
            assert decision["classification"] == "neutral_glue"
            assert decision["neutral_glue"]

    contract = _load(OUTPUT / "reconstructed_layout_contract.json")
    assert contract["design_id"] == DESIGN_ID
    assert contract["theme_created"] is False
    assert contract["external_assets"] == 0
    assert contract["viewer_annotation_separated"] is True
    assert all(contract["ai_template_bans"].values())
    forbidden_glue = {
        "palette identity",
        "theme",
        "decorative system",
        "icon family",
        "card system",
        "branded typography",
        "fictional environment",
        "marketing hierarchy",
    }
    assert forbidden_glue == set(contract["unsupported_elements_policy"]["not_neutral_glue"])


def test_primary_html_is_plain_offline_and_has_no_ai_template_shell() -> None:
    html_text = (OUTPUT / "reference_layout_proof.html").read_text(encoding="utf-8")
    parser = _ResourceParser()
    parser.feed(html_text)
    assert "audio" not in parser.tags and "video" not in parser.tags and "iframe" not in parser.tags
    assert all(not re.match(r"(?:https?:)?//", value) for value in parser.resources)
    assert set(parser.classes).isdisjoint({"hero", "eyebrow", "pill", "authority", "card", "card-grid", "gallery"})
    assert "Authority" not in html_text
    assert "box-shadow" not in html_text
    assert "gradient" not in html_text.lower()
    assert "#15181D" not in html_text and "#F7F5EF" not in html_text and "#52C7C7" not in html_text
    radii = re.findall(r"border-radius\s*:\s*([0-9]+)px", html_text)
    assert radii and max(map(int, radii)) <= 6
    assert '<div class="viewer">' in html_text
    assert '<nav class="filmstrip"' in html_text
    assert 'id="annotation-toggle"' in html_text
    assert 'id="reference-traces"' in html_text
    assert 'id="lineage"' in html_text


def test_viewer_and_annotation_frames_preserve_exact_subtitles_and_boundaries() -> None:
    script = _load(PILOT / "canonical_script.json")
    cues = {row["cue_id"]: row for row in script["cues"]}
    viewer_files = sorted((OUTPUT / "keyframes").glob("*.svg"))
    annotation_files = sorted((OUTPUT / "annotation_keyframes").glob("*.svg"))
    assert len(viewer_files) == len(annotation_files) == len(KEYFRAME_SPECS) == 6
    for spec in KEYFRAME_SPECS:
        approved = cues[spec["cue_id"]]["text"]
        viewer = OUTPUT / "keyframes" / spec["filename"]
        annotation = OUTPUT / "annotation_keyframes" / spec["filename"]
        viewer_root = ElementTree.parse(viewer).getroot()
        annotation_root = ElementTree.parse(annotation).getroot()
        assert viewer_root.attrib["width"] == annotation_root.attrib["width"] == "1920"
        assert viewer_root.attrib["height"] == annotation_root.attrib["height"] == "1080"
        assert viewer_root.attrib["viewBox"] == annotation_root.attrib["viewBox"] == "0 0 1920 1080"
        assert viewer_root.attrib["data-surface"] == "viewer"
        assert annotation_root.attrib["data-surface"] == "annotation"
        assert viewer_root.attrib["data-approved-text"] == approved
        assert annotation_root.attrib["data-approved-text"] == approved
        assert approved == "".join(_visible_svg_text(viewer).split(cues[spec["cue_id"]]["speaker"], 1)[-1].split())[-len("".join(approved.split())) :]
        viewer_text = _visible_svg_text(viewer)
        assert not re.search(r"cue_\d|T-[OJY]\d|RIGHTS|APPROVAL|pending|review|evidence|hash", viewer_text, re.I)
        annotation_text = _visible_svg_text(annotation)
        assert spec["cue_id"] in annotation_text
        assert spec["scene_id"] in annotation_text
        assert all(trace_id in annotation_text for trace_id in spec["refs"])
        assert "RIGHTS" in annotation_text and "APPROVAL pending" in annotation_text
        raw_viewer = viewer.read_text(encoding="utf-8")
        assert "<circle" not in raw_viewer and "gradient" not in raw_viewer.lower()
        assert not re.search(r"(?:https?:)?//", raw_viewer.replace("http://www.w3.org/2000/svg", ""))
        assert "#15181D" not in raw_viewer and "#F7F5EF" not in raw_viewer and "#52C7C7" not in raw_viewer


def test_nine_cue_filmstrip_preserves_order_content_counts_and_machine_metadata() -> None:
    script = _load(PILOT / "canonical_script.json")
    cues = script["cues"]
    assert Counter(row["scene_id"] for row in cues) == {"S1": 2, "S2": 4, "S3": 3}
    assert Counter(row["speaker"] for row in cues) == {"れいむ": 3, "まりさ": 6}
    root = ElementTree.parse(OUTPUT / "reference_layout_nine_cue_strip.svg").getroot()
    groups = [item for item in root if item.tag.endswith("g")]
    assert root.attrib["data-cue-coverage"] == "9/9"
    assert [item.attrib["data-cue-id"] for item in groups] == [row["cue_id"] for row in cues]
    assert [item.attrib["data-scene-id"] for item in groups] == [row["scene_id"] for row in cues]
    assert [item.attrib["data-approved-subtitle"] for item in groups] == [row["text"] for row in cues]

    manifest = _load(OUTPUT / "reference_layout_proof_manifest.json")
    assert manifest["content_lock"] == {
        "approved_hash_count": 8,
        "cue_count": 9,
        "scene_counts": {"S1": 2, "S2": 4, "S3": 3},
        "speaker_counts": {"れいむ": 3, "まりさ": 6},
        "changed": False,
    }
    assert manifest["viewer_keyframe_count"] == manifest["annotation_keyframe_count"] == 6
    assert manifest["cue_coverage"] == "9/9"
    assert manifest["external_asset_count"] == 0
    assert all(manifest[name] is False for name in (
        "human_visual_acceptance",
        "shot_motion_authorized",
        "asset_rights_authorized",
        "yymm4_authorized",
        "render_authorized",
        "production_authorized",
        "publication_authorized",
        "pr_created",
        "master_integrated",
    ))


def test_manifest_hashes_readback_access_and_silent_policy_are_exact() -> None:
    manifest = _load(OUTPUT / "reference_layout_proof_manifest.json")
    for relative, expected in manifest["file_sha256"].items():
        assert _sha(OUTPUT / relative) == expected
    readback = _load(OUTPUT / "reference_layout_proof_readback.json")
    assert readback["status"] == "human_reference_layout_review_ready"
    assert readback["project_state_id"] == STATE_ID
    assert readback["repo_relative_path"] == EXPECTED_PROOF
    assert readback["launcher_format"] == "Start-Process <exact-full-path-from-agent-report>"
    expected_false = {"approved_content_changed", "external_tracked_assets", "human_acceptance"}
    assert all(
        value is (name not in expected_false)
        for name, value in readback["checks"].items()
    )
    assert readback["checks"]["human_acceptance"] is False
    assert readback["checks"]["silent_audio_policy"] is True


def test_all_generated_html_xml_json_parse_and_tracked_resources_remain_local() -> None:
    for path in OUTPUT.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    for path in OUTPUT.rglob("*.svg"):
        ElementTree.parse(path)
        raw = path.read_text(encoding="utf-8")
        assert not re.search(r"(?:href|src)=[\"'](?:https?:)?//", raw, re.I)
    for path in OUTPUT.rglob("*.html"):
        parser = _ResourceParser()
        parser.feed(path.read_text(encoding="utf-8"))
        assert all(not re.match(r"(?:https?:)?//", value) for value in parser.resources)
        assert "audio" not in parser.tags and "video" not in parser.tags


def test_ignored_local_surfaces_are_present_ignored_and_untracked() -> None:
    local_paths = [
        OUTPUT / "local_reference_trace_board.html",
        OUTPUT / "local_reference_proxy_preview.html",
        OUTPUT / "local_reference_traces",
        OUTPUT / "local_render_inspection",
        OUTPUT / "local_browser_profile",
    ]
    for path in local_paths:
        assert path.exists()
        relative = path.relative_to(ROOT).as_posix()
        assert _git("check-ignore", relative) == relative
        assert _git("ls-files", "--", relative) == ""
    assert "INTERNAL REFERENCE PROXY — NOT A PRODUCTION ASSET" in (
        OUTPUT / "local_reference_trace_board.html"
    ).read_text(encoding="utf-8")
    proxy = (OUTPUT / "local_reference_proxy_preview.html").read_text(encoding="utf-8")
    assert "INTERNAL REFERENCE PROXY — NOT A PRODUCTION ASSET" in proxy
    for spec in KEYFRAME_SPECS:
        assert (
            spec["filename"] + " / supporting traces " + " / ".join(spec["refs"])
        ) in proxy


def test_tracked_reconstruction_has_no_private_path_uuid_or_local_binary() -> None:
    forbidden_extensions = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp3", ".wav", ".mp4", ".mov"}
    ignored_names = {
        "local_reference_trace_board.html",
        "local_reference_proxy_preview.html",
        "local_reference_traces",
        "local_render_inspection",
        "local_browser_profile",
    }
    for path in OUTPUT.rglob("*"):
        if not path.is_file() or any(part in ignored_names for part in path.relative_to(OUTPUT).parts):
            continue
        assert path.suffix.lower() not in forbidden_extensions
        text = path.read_text(encoding="utf-8")
        assert "C:\\Users\\" not in text
        assert not re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", text, re.I)


def test_regeneration_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    build_reference_layout_reconstruction(first, stage="all", create_local=False)
    build_reference_layout_reconstruction(second, stage="all", create_local=False)
    assert _file_hashes(first) == _file_hashes(second)
