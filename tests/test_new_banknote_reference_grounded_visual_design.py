from __future__ import annotations

import hashlib
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

from tests.regression_workspace import copy_tracked_tree, repo_relative_path

from src.pipeline.new_banknote_reference_grounded_visual_design import (
    BASE_REVISION,
    DESIGN_ID,
    KEYFRAME_SPECS,
    build_reference_grounded_visual_design,
)


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
OUTPUT = PILOT / "reference_grounded_visual_design"
OLD_PROOF = PILOT / "route_a_visual_proof"
EXPECTED_STATE = "nlmytgen-silent-execution-guarded-reference-proof-human-review-ready-v1"
HISTORICAL_STATE_REVISION = "649ada5050be5b9b2153c50c938d855797d5c19f"


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _visible_svg_text(path: Path) -> str:
    return " ".join(
        value.strip()
        for value in ElementTree.parse(path).getroot().itertext()
        if value.strip()
    )


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def _git_text(revision: str, relative: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{revision}:{relative}"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )


def _file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): _sha(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class _OfflineParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.resources: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(str(values["id"]))
        if tag in {"img", "script", "link", "iframe"}:
            value = values.get("src") or values.get("href")
            if value:
                self.resources.append(value)


def test_exact_base_approved_content_and_old_route_a_are_unchanged() -> None:
    assert _git("merge-base", "HEAD", BASE_REVISION) == BASE_REVISION
    approval = _load(PILOT / "human_script_approval_receipt.json")
    assert len(approval["approved_file_hashes"]) == 8
    for relative, expected in approval["approved_file_hashes"].items():
        assert _sha(PILOT / relative) == expected

    prefix = OLD_PROOF.relative_to(ROOT).as_posix()
    base_files = {
        row
        for row in _git("ls-tree", "-r", "--name-only", BASE_REVISION, "--", prefix).splitlines()
        if row
    }
    current_files = {
        path.relative_to(ROOT).as_posix() for path in OLD_PROOF.rglob("*") if path.is_file()
    }
    assert current_files == base_files
    for relative in sorted(base_files):
        assert _git("hash-object", "--", relative) == _git(
            "rev-parse", f"{BASE_REVISION}:{relative}"
        )


def test_research_registry_has_complete_visual_evidence_and_cohort_coverage() -> None:
    registry = _load(OUTPUT / "reference_registry.json")
    coverage = _load(OUTPUT / "reference_coverage_readback.json")
    rows = registry["references"]
    required = {
        "reference_id",
        "exact_title",
        "publisher_channel",
        "publication_update_date",
        "retrieval_timestamp",
        "canonical_url",
        "content_type",
        "cohort",
        "topic_scope",
        "accessibility_status",
        "visually_analyzed",
        "evidence_classes",
        "in_video_observation_ids",
        "inspected_surfaces",
        "representative_timestamps_or_sections",
        "primary_visual_subject",
        "object_image_diagram_character_ratio",
        "screen_composition",
        "subtitle_position_and_approximate_line_count",
        "character_speaker_placement",
        "title_and_key_term_treatment",
        "callout_arrow_zoom_usage",
        "source_credit_treatment",
        "background_treatment",
        "palette_role",
        "motion_type_and_frequency",
        "thumbnail_grammar",
        "strengths",
        "weaknesses",
        "misleading_risk",
        "rights_reuse_status",
        "patterns_worth_adopting",
        "patterns_to_avoid",
        "evidence_grade",
        "coverage_tags",
        "local_capture",
        "capture_note",
    }
    assert 15 <= len(rows) <= 18
    assert all(required <= set(row) for row in rows)
    usable = [row for row in rows if row["visually_analyzed"]]
    assert len(usable) >= 12
    assert all(row["inspected_surfaces"] for row in usable)
    assert all("metadata card only" not in row["capture_note"] for row in usable)
    assert coverage["usable_cohort_counts"] == {
        "official_educational": 4,
        "journalism_documentary": 5,
        "yukkuri_adjacent_explainer": 5,
    }
    assert coverage["checks"]["all_passed"] is True
    assert coverage["evidence_class_counts"] == {
        "in_video_frame_observed": 3,
        "inaccessible_not_counted": 2,
        "metadata_only": 7,
        "page_or_frame_observed": 9,
        "thumbnail_observed": 5,
    }
    assert coverage["thumbnail_only_reference_ids"] == ["Y04", "Y05"]
    assert coverage["in_video_frame_reference_ids"] == ["Y01", "Y02", "Y03"]
    assert coverage["in_video_observation_count"] == 3
    assert coverage["in_video_publisher_count"] == 3

    ids = [row["reference_id"] for row in rows]
    urls = [row["canonical_url"] for row in rows]
    assert len(ids) == len(set(ids))
    assert len(urls) == len(set(urls))
    assert all(row["exact_title"].strip() for row in rows)
    assert all(urlparse(url).scheme == "https" and urlparse(url).netloc for url in urls)
    policy = registry["research_policy"]
    assert policy["login_used"] is False
    assert policy["personal_cookie_profile_used"] is False
    assert policy["paywall_or_access_control_circumvented"] is False
    assert policy["video_or_audio_downloaded"] is False
    assert policy["bulk_scraping_used"] is False
    assert policy["public_visibility_treated_as_reuse_permission"] is False
    assert policy["public_no_login_player_frames_inspected"] == 3

    observation = _load(OUTPUT / "yukkuri_in_video_observation_readback.json")
    assert observation["status"] == "passed"
    assert observation["observation_count"] == 3
    assert observation["publisher_channel_count"] == 3
    assert observation["checks"]["all_passed"] is True
    assert all(row["observed_player_time_seconds"] is not None for row in observation["observations"])
    assert all(row["transition_motion_observation"].startswith("unknown") for row in observation["observations"])


def test_grammar_lineage_and_selection_are_thresholded_and_non_dominant() -> None:
    grammar = _load(OUTPUT / "visual_grammar_clusters.json")
    valid = {"dominant", "recurring", "cohort_specific", "outlier", "unsuitable", "inferred_constraint"}
    assert all(row["classification"] in valid for row in grammar["patterns"])
    assert all(row["supporting_reference_ids"] for row in grammar["patterns"])
    assert all(row["supporting_evidence"] for row in grammar["patterns"])
    for row in [item for item in grammar["patterns"] if item["video_body_claim"]]:
        assert row["classification"] == "inferred_constraint" or any(
            item["evidence_class"] in {"page_or_frame_observed", "in_video_frame_observed"}
            for item in row["supporting_evidence"]
        )

    registry_ids = {
        row["reference_id"] for row in _load(OUTPUT / "reference_registry.json")["references"]
    }
    lineage = _load(OUTPUT / "reference_to_visual_lineage.json")
    assert lineage["major_decision_count"] == 12
    assert lineage["covered_major_decision_count"] == 12
    assert lineage["coverage_ratio"] == 1.0
    for decision in lineage["decisions"]:
        assert set(decision["supporting_reference_ids"]) <= registry_ids
        assert decision["adaptation_description"]
        assert decision["supporting_evidence_classes"]
        assert decision["adopted_pattern_ids"]
        assert decision["original_glue_class"] == "neutral_glue"
        assert decision["human_approval_impact"] == "pending"
    dominance = lineage["source_dominance"]
    assert dominance["maximum_observed_share"] <= dominance["rule_maximum"] == 0.4
    assert dominance["passed"] is True

    scorecard = _load(OUTPUT / "reference_selection_scorecard.json")
    candidates = {row["candidate_id"]: row for row in scorecard["candidates"]}
    selection = scorecard["selection"]
    assert selection["selected_candidate"] == DESIGN_ID
    assert scorecard["score_type"] == "internal_selection_heuristic"
    assert "not audience-quality" in scorecard["interpretation_boundary"]
    assert candidates[DESIGN_ID]["score"] == selection["selected_score"] == 89
    assert selection["lead"] >= 5
    assert selection["selection_preserved_after_evidence_revision"] is True
    assert selection["reference_threshold_passed"] is True
    assert selection["hard_constraints_passed"] is True
    assert selection["human_approval_status"] == "pending"


def test_old_ai_original_is_demoted_without_becoming_a_visual_authority() -> None:
    receipt = _load(OUTPUT / "ai_original_visual_supersession_receipt.json")
    manifest = _load(OUTPUT / "reference_grounded_visual_proof_manifest.json")
    assert receipt["status"] == "exploratory_ai_original_not_reference_grounded"
    assert receipt["current_visual_authority"] is False
    assert receipt["content_authority"] == "unchanged"
    assert manifest["superseded_old_proof"]["status"] == (
        "exploratory_ai_original_not_reference_grounded"
    )
    assert manifest["superseded_old_proof"]["current_visual_authority"] is False
    protected = receipt["protected_artifact_sha256"]
    assert len(protected) == receipt["protected_file_count"] == 23
    assert all(_sha(ROOT / relative) == expected for relative, expected in protected.items())


def test_six_keyframes_and_nine_cues_preserve_approved_content_and_rights_boundary() -> None:
    script = _load(PILOT / "canonical_script.json")
    cue_text = {cue["cue_id"]: cue["text"] for cue in script["cues"]}
    keyframes = list((OUTPUT / "keyframes").glob("*.svg"))
    annotation_keyframes = list((OUTPUT / "annotation_keyframes").glob("*.svg"))
    assert len(keyframes) == len(KEYFRAME_SPECS) == 6
    assert len(annotation_keyframes) == len(KEYFRAME_SPECS) == 6
    for spec in KEYFRAME_SPECS:
        path = OUTPUT / "keyframes" / spec["filename"]
        text = path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(text)
        assert root.attrib["width"] == "1920"
        assert root.attrib["height"] == "1080"
        assert root.attrib["viewBox"] == "0 0 1920 1080"
        assert root.attrib["data-cue-id"] == spec["cue_id"]
        assert root.attrib["data-surface"] == "viewer"
        assert root.attrib["data-approved-text"] == cue_text[spec["cue_id"]]
        assert "https://" not in text and "http://" not in text.replace(
            "http://www.w3.org/2000/svg", ""
        )
        assert not re.search(r"(portrait|banknote likeness|seal|serial number)", text, re.I)
        visible = _visible_svg_text(path)
        assert spec["scene_id"] not in visible
        assert spec["cue_id"] not in visible
        assert all(reference_id not in visible for reference_id in spec["refs"])
        assert not re.search(r"\b(reference|refs|evidence|patterns|review|approval)\b", visible, re.I)

        annotation = OUTPUT / "annotation_keyframes" / spec["filename"]
        annotation_root = ElementTree.parse(annotation).getroot()
        annotation_visible = _visible_svg_text(annotation)
        assert annotation_root.attrib["data-surface"] == "annotation"
        assert spec["scene_id"] in annotation_visible
        assert spec["cue_id"] in annotation_visible
        assert all(reference_id in annotation_visible for reference_id in spec["refs"])
        assert all(term in annotation_visible.lower() for term in ("evidence", "patterns", "rights", "approval pending"))

    mapping = _load(OUTPUT / "reference_grounded_visual_mapping.json")
    assert mapping["cue_count"] == 9
    assert mapping["scene_allocation"] == {"S1": 2, "S2": 4, "S3": 3}
    assert mapping["speaker_counts"] == {"れいむ": 3, "まりさ": 6}
    for field in ("cue_id", "scene_id", "speaker", "text"):
        assert [row[field] for row in mapping["cues"]] == [
            row[field] for row in script["cues"]
        ]
    assert all(row["contact_sheet_thumbnail"] is True for row in mapping["cues"])
    assert all(row["external_asset"] is False for row in mapping["cues"])

    contact = ElementTree.parse(OUTPUT / "reference_grounded_nine_cue_contact_sheet.svg").getroot()
    assert contact.attrib["data-cue-coverage"] == "9/9"
    motion = _load(OUTPUT / "reference_grounded_motion_storyboard.json")
    assert motion["motion_bearing_cue_count"] == 9
    assert motion["principal_motion_maximum_per_cue"] == 1
    assert motion["continuous_loop_allowed"] is False
    assert motion["evidence_class"] == "inferred_constraint"
    assert motion["observed_playback_sequence_count"] == 0
    assert motion["timing_frequency_persistence_observed"] is False
    assert motion["states"] == ["start", "emphasis", "settled"]
    assert all(row["loop"] is False for row in motion["cues"])
    assert all(row["simultaneous_principal_motions"] == 1 for row in motion["cues"])


def test_viewer_is_offline_viewer_first_and_has_a_direct_lineage_mode() -> None:
    text = (OUTPUT / "reference_grounded_visual_proof.html").read_text(encoding="utf-8")
    parser = _OfflineParser()
    parser.feed(text)
    assert {"viewer", "annotation", "reference-lineage"} <= parser.ids
    assert text.index('id="viewer"') < text.index('id="reference-lineage"')
    assert text.index('id="viewer"') < text.index('id="annotation"')
    assert "#annotation" in text
    assert "#reference-lineage" in text
    assert "Security Inspection Lab" not in text
    assert all(not urlparse(value).scheme for value in parser.resources)
    assert all((OUTPUT / value).is_file() for value in parser.resources)
    assert text.count('<article class="lineage-card">') == 12


def test_local_research_media_are_ignored_and_absent_from_tracked_proof() -> None:
    forbidden_suffixes = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".webm"}
    tracked_surface = [
        path
        for path in OUTPUT.rglob("*")
        if path.is_file() and "local_" not in path.relative_to(OUTPUT).as_posix()
    ]
    assert all(path.suffix.lower() not in forbidden_suffixes for path in tracked_surface)
    for relative, is_directory in (
        ("local_reference_cache", True),
        ("local_reference_captures", True),
        ("local_in_video_observations", True),
        ("local_render_inspection", True),
        ("reference_contact_sheet.local.html", False),
    ):
        candidate = OUTPUT / relative
        if is_directory:
            candidate /= ".ignore-contract-probe"
        relative_path = repo_relative_path(ROOT, candidate)
        result = subprocess.run(
            ["git", "check-ignore", "-q", "--", relative_path],
            cwd=ROOT,
            check=False,
        )
        assert result.returncode == 0

    private = re.compile(
        r"(?i)(c:[\\/]users[\\/]|/users/|/home/|[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})"
    )
    assert all(not private.search(path.read_text(encoding="utf-8")) for path in tracked_surface)


def test_machine_outputs_parse_readback_passes_and_generation_is_deterministic(
    tmp_path: Path,
) -> None:
    for path in OUTPUT.glob("*.json"):
        _load(path)
    for path in [
        *(OUTPUT / "keyframes").glob("*.svg"),
        *(OUTPUT / "annotation_keyframes").glob("*.svg"),
        *OUTPUT.glob("*.svg"),
    ]:
        ElementTree.parse(path)
    parser = _OfflineParser()
    parser.feed((OUTPUT / "reference_grounded_visual_proof.html").read_text(encoding="utf-8"))
    readback = _load(OUTPUT / "reference_grounded_visual_proof_readback.json")
    assert readback["status"] == "passed"
    assert readback["checks"]["all_passed"] is True
    assert readback["output_inspection"]["repair_cycles"] == 1
    isolated_root = tmp_path / "repo"
    isolated_pilot = isolated_root / PILOT.relative_to(ROOT)
    copy_tracked_tree(
        PILOT,
        isolated_pilot,
        repo_root=ROOT,
    )
    isolated_output = isolated_root / OUTPUT.relative_to(ROOT)
    first = build_reference_grounded_visual_design(root=isolated_root)
    first_hashes = _file_hashes(isolated_output)
    second = build_reference_grounded_visual_design(root=isolated_root)
    assert first["status"] == "passed"
    assert second["status"] == "passed"
    assert second["changed"] == []
    assert _file_hashes(isolated_output) == first_hashes


def test_state_docs_point_to_the_reference_grounded_human_gate() -> None:
    runtime = _git_text(HISTORICAL_STATE_REVISION, "docs/runtime-state.md")
    cockpit = _git_text(HISTORICAL_STATE_REVISION, "docs/PROJECT_COCKPIT.md")
    registry = _git_text(HISTORICAL_STATE_REVISION, "docs/THREAD_REGISTRY.md")
    assert f"Project-State-ID: {EXPECTED_STATE}" in runtime
    assert f"Project-State-ID: {EXPECTED_STATE}" in cockpit
    assert "new-banknote-reference-grounded-visual-redesign-v1" in registry
    for text in (runtime, cockpit):
        assert "human-reference-grounded-visual-review" in text
        assert "final acceptance" in text.lower()
        assert "YMM4" in text
