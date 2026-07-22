from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

import pytest

from src.pipeline.new_banknote_route_a_visual_proof import (
    APPROVED_SUBTITLE_LINES_BY_CUE,
    BASE_REVISION,
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    DISCLAIMER,
    KEYFRAME_SPECS,
    MOTION_DISPLAY_BY_CUE,
    PRESENTATION_BASE_REVISION,
    PRESENTATION_BEFORE_SHA256,
    REVIEW_QUESTIONS,
    ROUTE_ID,
    build_route_a_visual_proof,
)


ROOT = Path(__file__).resolve().parents[1]
PILOT = (
    ROOT
    / "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
PROOF = PILOT / "route_a_visual_proof"
KEYFRAMES = PROOF / "keyframes"
VIEWER_KEYFRAMES = PROOF / "viewer_keyframes"
EXPECTED_STATE = "new-banknote-route-a-dual-surface-visual-proof-human-review-ready-v1"
HISTORICAL_STATE_REVISION = "8d7fd5a19b392dd4869fa71536b7fe9f7fe3c028"
INTEGRATION_MANIFEST = (
    ROOT
    / "docs/verification/new_banknote_successor_selective_integration_manifest.json"
)


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_blob(revision: str, path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(
        ["git", "rev-parse", f"{revision}:{relative}"], cwd=ROOT, text=True
    ).strip()


def _current_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", "--", str(path)], cwd=ROOT, text=True
    ).strip()


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


def _ignored_local_evidence_locators() -> tuple[str, ...]:
    manifest = _load(INTEGRATION_MANIFEST)
    return tuple(row["path"] for row in manifest["ignored_local_evidence"]["artifacts"])


def _all_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_all_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_all_keys(item))
        return keys
    return set()


class _OfflineParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.resources: list[str] = []
        self.tags: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.tags.append(tag)
        for name, value in attrs:
            if value is None:
                continue
            if tag == "a" and name == "href":
                self.links.append(value)
            if tag in {"img", "script", "link", "iframe"} and name in {
                "src",
                "href",
            }:
                self.resources.append(value)


def test_direction_receipt_is_bounded_and_does_not_approve_implementation() -> None:
    receipt = _load(PROOF / "human_visual_direction_selection_receipt.json")
    assert receipt["route_id"] == ROUTE_ID
    assert receipt["selection_class"] == "direction_selected_for_concrete_proof"
    assert receipt["user_decision"] == "explicit"
    assert receipt["selection_scope"] == "visual_direction_for_concrete_proof_only"
    assert receipt["scene_spine"] == {"S1": 2, "S2": 4, "S3": 3}
    assert receipt["diagram_constraint"] == DISCLAIMER
    assert receipt["motion_constraint"] == {
        "principal_motion_maximum_per_cue": 1,
        "continuous_loop_allowed": False,
    }
    authorization = receipt["authorization"]
    assert authorization["concrete_visual_proof_generation"] is True
    assert all(
        authorization[key] is False
        for key in (
            "final_visual_acceptance",
            "implementation_authorized",
            "YMM4_authorized",
            "render_authorized",
            "production_authorized",
            "public_release_authorized",
            "rights_authorized",
        )
    )


def test_six_viewer_and_six_annotation_frames_are_exact_and_1920x1080() -> None:
    expected_names = {spec["filename"] for spec in KEYFRAME_SPECS}
    assert {path.name for path in KEYFRAMES.glob("*.svg")} == expected_names
    assert {path.name for path in VIEWER_KEYFRAMES.glob("*.svg")} == expected_names
    script = _load(PILOT / "canonical_script.json")
    cue_text = {cue["cue_id"]: cue["text"] for cue in script["cues"]}
    for directory, surface in ((KEYFRAMES, "annotation"), (VIEWER_KEYFRAMES, "viewer")):
        for spec in KEYFRAME_SPECS:
            path = directory / spec["filename"]
            text = path.read_text(encoding="utf-8")
            root = ElementTree.fromstring(text)
            assert root.attrib["width"] == str(CANVAS_WIDTH)
            assert root.attrib["height"] == str(CANVAS_HEIGHT)
            assert root.attrib["viewBox"] == "0 0 1920 1080"
            assert root.attrib["data-surface"] == surface
            assert root.attrib["data-cue-id"] == spec["cue_id"]
            assert root.attrib["data-approved-text"] == cue_text[spec["cue_id"]]
            assert root.attrib["data-subtitle-safe-area"] == "84,780,1752,220"
            assert root.attrib["data-implementation-authorized"] == "false"
            assert DISCLAIMER in text
            normalized = "".join("".join(root.itertext()).split())
            assert "".join(cue_text[spec["cue_id"]].split()) in normalized
            assert "http://" not in text.replace("http://www.w3.org/2000/svg", "")
            assert "https://" not in text


def test_semantic_wraps_preserve_approved_text_and_avoid_known_defects() -> None:
    script = _load(PILOT / "canonical_script.json")
    cue_text = {cue["cue_id"]: cue["text"] for cue in script["cues"]}
    assert set(APPROVED_SUBTITLE_LINES_BY_CUE) == set(cue_text)
    for cue_id, lines in APPROVED_SUBTITLE_LINES_BY_CUE.items():
        assert "".join(lines) == cue_text[cue_id]
        assert all(line and line[0] not in "、。）」』】！？!?" for line in lines)
        assert all(line not in {"、", "。", "！", "？", "!", "?"} for line in lines)
        assert not (len(lines) > 1 and len(lines[-1]) == 1)
    protected_units = ("技術", "見える", "描かない", "持たない", "傾ける", "確かめられる", "覚えておこう")
    for svg_path in [*KEYFRAMES.glob("*.svg"), *VIEWER_KEYFRAMES.glob("*.svg")]:
        root = ElementTree.parse(svg_path).getroot()
        visible_lines = [value.strip() for value in root.itertext() if value.strip()]
        assert all(value not in {"、", "。", "！", "？", "!", "?"} for value in visible_lines)
        assert all(value[0] not in "、。）」』】！？!?" for value in visible_lines)
        approved = root.attrib["data-approved-text"]
        expected_lines = APPROVED_SUBTITLE_LINES_BY_CUE[root.attrib["data-cue-id"]]
        boundaries: set[int] = set()
        cursor = 0
        for line in expected_lines[:-1]:
            cursor += len(line)
            boundaries.add(cursor)
        for unit in protected_units:
            start = approved.find(unit)
            if start >= 0:
                assert not any(start < boundary < start + len(unit) for boundary in boundaries)


def test_viewer_excludes_debug_ui_and_annotation_retains_audit_evidence() -> None:
    debug_labels = (
        "CONCRETE PROOF",
        "REVIEW PENDING",
        "PRINCIPAL MOTION",
        "loop: false",
        "principal: 1",
        "SOURCE-BOUNDED EXPLANATION",
        "SUBTITLE SAFE AREA",
    )
    viewer = "\n".join(path.read_text(encoding="utf-8") for path in VIEWER_KEYFRAMES.glob("*.svg"))
    annotation = "\n".join(path.read_text(encoding="utf-8") for path in KEYFRAMES.glob("*.svg"))
    assert all(label not in viewer for label in debug_labels)
    assert all(label in annotation for label in debug_labels)
    assert viewer.count(DISCLAIMER) == 6
    assert annotation.count(DISCLAIMER) == 6


def test_mapping_and_contact_sheet_cover_approved_nine_cues_exactly() -> None:
    script = _load(PILOT / "canonical_script.json")
    mapping = _load(PROOF / "route_a_cue_visual_mapping.json")
    assert mapping["cue_count"] == 9
    assert mapping["scene_allocation"] == {"S1": 2, "S2": 4, "S3": 3}
    assert [cue["cue_id"] for cue in mapping["cues"]] == [
        f"cue_{index:03d}" for index in range(1, 10)
    ]
    assert [cue["text"] for cue in mapping["cues"]] == [
        cue["text"] for cue in script["cues"]
    ]
    assert [cue["scene_id"] for cue in mapping["cues"]] == [
        cue["scene_id"] for cue in script["cues"]
    ]
    assert [cue["speaker"] for cue in mapping["cues"]] == [
        cue["speaker"] for cue in script["cues"]
    ]
    assert all(cue["thumbnail_present"] is True for cue in mapping["cues"])
    assert all(cue["disclaimer"] == DISCLAIMER for cue in mapping["cues"])
    assert all(cue["loop"] is False for cue in mapping["cues"])
    assert all(cue["principal_motion_count"] == 1 for cue in mapping["cues"])
    contact = ElementTree.parse(PROOF / "route_a_nine_cue_contact_sheet.svg").getroot()
    assert contact.attrib["data-cue-coverage"] == "9/9"
    rendered = (PROOF / "route_a_nine_cue_contact_sheet.svg").read_text(
        encoding="utf-8"
    )
    for index in range(1, 10):
        assert f'data-cue-id="cue_{index:03d}"' in rendered
    storyboard = (PROOF / "route_a_motion_storyboard.svg").read_text(encoding="utf-8")
    for label in MOTION_DISPLAY_BY_CUE.values():
        assert label in rendered
        assert label in storyboard
    assert all(
        truncated not in rendered
        for truncated in (
            "label transiti</text>",
            "layer reveal o</text>",
            "light reveal o</text>",
            "restrained til</text>",
            "loupe zoom onc</text>",
        )
    )


def test_motion_storyboard_has_start_emphasis_settled_and_no_loop() -> None:
    motion = _load(PROOF / "route_a_motion_storyboard.json")
    assert motion["motion_bearing_cue_count"] == 9
    assert motion["principal_motion_maximum_per_cue"] == 1
    assert motion["continuous_loop_allowed"] is False
    assert motion["states"] == ["start", "emphasis", "settled"]
    for cue in motion["cues"]:
        assert cue["start"]
        assert cue["emphasis"]
        assert cue["settled"]
        assert cue["duration_seconds"] > 0
        assert cue["easing"]
        assert cue["loop"] is False
        assert cue["simultaneous_principal_motions"] == 1
        assert cue["implementation_status"] == "proposal_only_not_implemented"
    svg = (PROOF / "route_a_motion_storyboard.svg").read_text(encoding="utf-8")
    ElementTree.fromstring(svg)
    assert svg.count('data-loop="false"') == 10
    assert svg.count('data-principal-motion-count="1"') == 9


def test_primary_html_is_offline_and_all_relative_targets_exist() -> None:
    path = PROOF / "route_a_visual_proof.html"
    text = path.read_text(encoding="utf-8")
    parser = _OfflineParser()
    parser.feed(text)
    assert parser.resources
    assert "iframe" not in parser.tags
    for target in parser.links + parser.resources:
        assert not target.startswith(("http://", "https://", "file://", "/"))
        if target.startswith("#"):
            assert f'id="{target[1:]}"' in text
            continue
        assert (path.parent / target).resolve().is_file()
    lowered = text.lower()
    assert all(
        token not in lowered
        for token in ("https://", "file://", "cdn.", "@import", "analytics")
    )
    assert 'data-external-resource-count="0"' in text
    assert 'data-default-surface="viewer"' in text
    assert '<section id="viewer-mode"' in text
    assert '<details id="annotation-mode"' in text
    assert text.index('<section id="viewer-mode"') < text.index('<details id="annotation-mode"')
    assert text.count('src="viewer_keyframes/') == 6
    assert text.count('src="keyframes/') == 6
    assert "意図する動画グラフィックではありません" in text
    assert "最終visual acceptance" in text
    assert "ymm4実装" in lowered


def test_review_sheet_asks_only_the_exact_four_questions() -> None:
    text = (PROOF / "route_a_visual_review_sheet.md").read_text(encoding="utf-8")
    numbered = re.findall(r"^[1-4]\. (.+)$", text, flags=re.MULTILINE)
    assert numbered == list(REVIEW_QUESTIONS)
    assert "`accept`" in text
    assert "`scene/cue-specific revision`" in text
    assert "A/B/Cを選び直す必要はありません" in text


def test_manifest_readback_hashes_privacy_and_prohibited_fields() -> None:
    manifest = _load(PROOF / "route_a_visual_proof_manifest.json")
    readback = _load(PROOF / "route_a_visual_proof_readback.json")
    assert manifest["status"] == "review_ready_not_accepted"
    assert manifest["source_base_revision"] == BASE_REVISION
    assert manifest["proof_contract"]["human_visual_acceptance"] is False
    assert manifest["proof_contract"]["implementation_authorized"] is False
    assert manifest["proof_contract"]["viewer_keyframes"] == 6
    assert manifest["proof_contract"]["annotation_keyframes"] == 6
    assert manifest["proof_contract"]["default_html_surface"] == "viewer"
    for row in manifest["artifacts"]:
        assert _sha(ROOT / row["path"]) == row["sha256"]
    assert readback["status"] == "passed"
    assert readback["checks"]["all_passed"] is True
    payloads = [
        _load(path)
        for path in PROOF.glob("*.json")
    ]
    prohibited_fields = {"portrait", "seal", "serial_number", "serialNumber"}
    assert not (prohibited_fields & set().union(*map(_all_keys, payloads)))
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="strict")
        for path in PROOF.rglob("*")
        if path.is_file()
    )
    assert re.search(
        r"(?i)(?:(?<![a-z0-9])[a-z]:[\\/]|/users/|/home/)", combined
    ) is None
    assert re.search(
        r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        combined,
    ) is None
    assert "notebooklm.google.com" not in combined.lower()
    assert not any(path.suffix.lower() in {".ymmp", ".mp4", ".png"} for path in PROOF.rglob("*"))


def test_presentation_revision_receipt_binds_before_after_and_pending_gate() -> None:
    receipt = _load(PROOF / "visual_proof_presentation_revision_receipt.json")
    assert receipt["receipt_id"] == "new-banknote-route-a-dual-surface-visual-proof-v1"
    assert receipt["presentation_base_revision"] == PRESENTATION_BASE_REVISION
    assert receipt["status"] == "human_review_ready_not_accepted"
    assert receipt["surface_separation"]["default_html_surface"] == "viewer"
    assert receipt["surface_separation"]["viewer_keyframe_count"] == 6
    assert receipt["surface_separation"]["annotation_keyframe_count"] == 6
    assert receipt["approved_content_invariance"]["approved_hashes_8_of_8_exact"] is True
    assert receipt["approved_content_invariance"]["cue_text_segment_concatenation_exact"] is True
    assert receipt["contact_sheet_motion_labels"]["display_values"] == list(
        MOTION_DISPLAY_BY_CUE.values()
    )
    assert receipt["artifact_sha256"]["before"] == PRESENTATION_BEFORE_SHA256
    assert len(receipt["artifact_sha256"]["after"]) == 15
    for relative, digest in receipt["artifact_sha256"]["before"].items():
        blob = _git_blob(PRESENTATION_BASE_REVISION, PROOF / relative)
        before = subprocess.check_output(
            ["git", "cat-file", "blob", blob], cwd=ROOT
        )
        assert hashlib.sha256(before).hexdigest() == digest
    for relative, digest in receipt["artifact_sha256"]["after"].items():
        assert _sha(PROOF / relative) == digest
    assert all(value is False for value in receipt["authorization"].values())


def test_approved_content_original_proposal_and_ignored_evidence_are_unchanged() -> None:
    approval = _load(PILOT / "human_script_approval_receipt.json")
    assert len(approval["approved_file_hashes"]) == 8
    for name, digest in approval["approved_file_hashes"].items():
        assert _sha(PILOT / name) == digest
        assert _current_blob(PILOT / name) == _git_blob(BASE_REVISION, PILOT / name)
    manifest = _load(PROOF / "route_a_visual_proof_manifest.json")
    protected = manifest["protected_original_visual_proposal"]
    assert protected["artifact_count"] > 0
    assert protected["modification_authorized"] is False
    for row in protected["artifacts"]:
        path = ROOT / row["path"]
        assert _sha(path) == row["sha256"]
        assert _current_blob(path) == _git_blob(BASE_REVISION, path)


@pytest.mark.requires_local_evidence(
    "historical_yymm4_import_evidence",
    *_ignored_local_evidence_locators(),
)
def test_ignored_yymm4_evidence_matches_historical_integration_receipt() -> None:
    integration_manifest = _load(INTEGRATION_MANIFEST)
    ignored = integration_manifest["ignored_local_evidence"]
    assert ignored["file_count"] == 3
    for row in ignored["artifacts"]:
        path = ROOT / row["path"]
        assert path.stat().st_size == row["before"]["size"]
        assert _sha(path) == row["before"]["sha256"]
        assert subprocess.run(
            ["git", "check-ignore", "--quiet", "--", str(path)],
            cwd=ROOT,
            check=False,
        ).returncode == 0


def test_generation_is_deterministic_and_state_is_review_ready(
    tmp_path: Path,
) -> None:
    isolated_root = tmp_path / "repo"
    isolated_pilot = isolated_root / PILOT.relative_to(ROOT)
    shutil.copytree(
        PILOT,
        isolated_pilot,
        ignore=shutil.ignore_patterns("local_outputs"),
    )
    isolated_proof = isolated_root / PROOF.relative_to(ROOT)
    first = build_route_a_visual_proof(root=isolated_root)
    first_hashes = _file_hashes(isolated_proof)
    second = build_route_a_visual_proof(root=isolated_root)
    assert first["status"] == "passed"
    assert second["status"] == "passed"
    assert second["changed"] == []
    assert _file_hashes(isolated_proof) == first_hashes
    runtime = _git_text(HISTORICAL_STATE_REVISION, "docs/runtime-state.md")
    cockpit = _git_text(HISTORICAL_STATE_REVISION, "docs/PROJECT_COCKPIT.md")
    for text in (runtime, cockpit):
        assert f"Project-State-ID: {EXPECTED_STATE}" in text
        assert "Product-State: new-banknote-route-a-viewer-and-annotation-proof-ready" in text
        assert "Product-Gate: human-route-a-visual-proof-review" in text
        assert "Recommended-Next: review-clean-route-a-viewer-frames" in text
