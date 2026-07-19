from __future__ import annotations

import hashlib
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from src.pipeline.new_banknote_route_a_visual_proof import (
    BASE_REVISION,
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    DISCLAIMER,
    KEYFRAME_SPECS,
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
EXPECTED_STATE = "new-banknote-route-a-concrete-visual-proof-review-ready-v1"


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


def test_six_full_frame_keyframes_are_parseable_1920x1080_and_subtitle_safe() -> None:
    expected_names = {spec["filename"] for spec in KEYFRAME_SPECS}
    assert {path.name for path in KEYFRAMES.glob("*.svg")} == expected_names
    script = _load(PILOT / "canonical_script.json")
    cue_text = {cue["cue_id"]: cue["text"] for cue in script["cues"]}
    for spec in KEYFRAME_SPECS:
        path = KEYFRAMES / spec["filename"]
        text = path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(text)
        assert root.attrib["width"] == str(CANVAS_WIDTH)
        assert root.attrib["height"] == str(CANVAS_HEIGHT)
        assert root.attrib["viewBox"] == "0 0 1920 1080"
        assert root.attrib["data-cue-id"] == spec["cue_id"]
        assert root.attrib["data-subtitle-safe-area"] == "84,780,1752,220"
        assert root.attrib["data-implementation-authorized"] == "false"
        assert DISCLAIMER in text
        normalized = "".join("".join(root.itertext()).split())
        assert "".join(cue_text[spec["cue_id"]].split()) in normalized
        assert "http://" not in text.replace("http://www.w3.org/2000/svg", "")
        assert "https://" not in text


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
        assert (path.parent / target).resolve().is_file()
    lowered = text.lower()
    assert all(
        token not in lowered
        for token in ("https://", "file://", "cdn.", "@import", "analytics")
    )
    assert 'data-external-resource-count="0"' in text
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
    integration_manifest = _load(
        ROOT
        / "docs/verification/new_banknote_successor_selective_integration_manifest.json"
    )
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


def test_generation_is_deterministic_and_state_is_review_ready() -> None:
    first = build_route_a_visual_proof(root=ROOT)
    second = build_route_a_visual_proof(root=ROOT)
    assert first["status"] == "passed"
    assert second["status"] == "passed"
    assert first["changed"] == []
    assert second["changed"] == []
    runtime = (ROOT / "docs/runtime-state.md").read_text(encoding="utf-8")
    cockpit = (ROOT / "docs/PROJECT_COCKPIT.md").read_text(encoding="utf-8")
    for text in (runtime, cockpit):
        assert f"Project-State-ID: {EXPECTED_STATE}" in text
        assert "Product-State: new-banknote-route-a-keyframes-and-motion-proof-ready" in text
        assert "Product-Gate: human-route-a-visual-proof-review" in text
        assert "Recommended-Next: review-route-a-concrete-keyframes-and-motion" in text
