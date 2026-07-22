from __future__ import annotations

import csv
import hashlib
import json
import posixpath
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
PILOT = (
    REPO_ROOT
    / "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
MANIFEST = (
    REPO_ROOT
    / "docs/verification/new_banknote_successor_selective_integration_manifest.json"
)
HISTORICAL_INTEGRATION_REVISION = "d38075b97efabc99d1a23e8e0afafd5d44f1e2de"
EXPECTED_REFS = {
    "primary": "5e50ff707806724e67a5e0cec215bdd3b604ce32",
    "candidate": "833717f63713db9555f563a2a26285fa2f621e3d",
    "audit": "ee052489a33e9247f77b90af27cdd56911acc527",
    "common_baseline": "b05eb3867caabda496fb9a0070d230a4e81aea01",
    "origin_master_at_audit": "37a02fbcecaf324f61b055b8677b6537735853fd",
}
_PRIVATE_PATH_RE = re.compile(
    r"(?i)(?:(?<![a-z])[a-z]:[\\/]|\\\\[^\\\s]+[\\/]|/home/|/users/)"
)
_UUID_RE = re.compile(
    r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
)
_BANNED_BODY_KEYS = {
    "raw_text",
    "source_body",
    "source_quote_text",
    "transcript_body",
    "verbatim_excerpt",
}


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _git_blob_at(revision: str, relative: str) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"{revision}:{relative}"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _git_bytes_at(revision: str, relative: str) -> bytes:
    blob = _git_blob_at(revision, relative)
    if blob is None:
        raise AssertionError(f"missing historical path: {revision}:{relative}")
    return subprocess.check_output(
        ["git", "cat-file", "blob", blob],
        cwd=REPO_ROOT,
    )


def _git_text_at(revision: str, relative: str) -> str:
    return _git_bytes_at(revision, relative).decode("utf-8")


def _load_historical(relative: str) -> dict:
    payload = json.loads(_git_text_at(HISTORICAL_INTEGRATION_REVISION, relative))
    assert isinstance(payload, dict)
    return payload


def _ignored_local_evidence_locators() -> tuple[str, ...]:
    manifest = _load(MANIFEST)
    return tuple(row["path"] for row in manifest["ignored_local_evidence"]["artifacts"])


def _all_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value).union(*(_all_keys(item) for item in value.values()))
    if isinstance(value, list):
        return set().union(*(_all_keys(item) for item in value)) if value else set()
    return set()


class _BoardParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag == "a":
            self.hrefs.extend(
                value for name, value in attrs if name == "href" and value
            )


def test_exact_partition_hashes_and_exclusions_are_accounted_for() -> None:
    manifest = _load(MANIFEST)
    assert manifest["status"] == "passed"
    assert manifest["refs"] == EXPECTED_REFS
    assert manifest["partition"] == {
        "accepted_count": 27,
        "historical_count": 2,
        "regenerated_count": 8,
        "excluded_count": 14,
        "total_candidate_treatments": 51,
        "lists_disjoint": True,
        "audit_contract_drift": False,
    }
    categories = [
        manifest["accepted_candidate_paths"],
        manifest["historical_candidate_paths"],
        manifest["regenerated_paths"],
        manifest["excluded_candidate_paths"],
    ]
    paths = [row["path"] for category in categories for row in category]
    assert len(paths) == len(set(paths)) == 51
    for category in categories[:3]:
        for row in category:
            assert (
                _git_blob_at(HISTORICAL_INTEGRATION_REVISION, row["path"])
                == row["successor_git_blob"]
            )
    assert {
        row["path"] for row in manifest["adapted_candidate_paths"]
    } == {
        "src/pipeline/editorial_provenance.py",
        "tests/test_editorial_provenance.py",
    }
    assert all(
        row["candidate_blob_materialized"] is False
        for row in manifest["excluded_candidate_paths"]
    )
    for row in manifest["excluded_candidate_paths"]:
        historical_blob = _git_blob_at(
            HISTORICAL_INTEGRATION_REVISION, row["path"]
        )
        if row["successor_git_blob"] is None:
            assert historical_blob is None
        else:
            assert historical_blob == row["successor_git_blob"]
            assert row["candidate_git_blob"] != row["successor_git_blob"]
    protected = manifest["protected_primary"]
    assert protected["artifact_count"] == 31
    assert protected["all_exact"] is True
    for row in protected["artifacts"]:
        assert row["exact"] is True
        assert row["primary_git_blob"] == row["successor_git_blob"]
        assert (
            _git_blob_at(HISTORICAL_INTEGRATION_REVISION, row["path"])
            == row["successor_git_blob"]
        )


def test_primary_authority_historical_yymm4_and_visual_status_are_unified() -> None:
    approval = _load(PILOT / "human_script_approval_receipt.json")
    script = _load(PILOT / "canonical_script.json")
    lineage = _load(PILOT / "content_lineage_readback.json")
    current = _load(PILOT / "existing_yymm4_evidence_revalidation_receipt.json")
    historical = _load(PILOT / "yymm4_import_observation_readback.json")
    lock = _load(PILOT / "editorial_provenance/content_lock_receipt.json")
    visual = _load(
        PILOT / "visual_scene_decision/recommended_visual_direction.json"
    )
    assert approval["status"] == "valid"
    assert len(approval["approved_file_hashes"]) == 8
    for name, digest in approval["approved_file_hashes"].items():
        assert hashlib.sha256((PILOT / name).read_bytes()).hexdigest() == digest
    cues = script["cues"]
    assert len(cues) == 9
    assert {
        scene: sum(cue["scene_id"] == scene for cue in cues)
        for scene in ("S1", "S2", "S3")
    } == {"S1": 2, "S2": 4, "S3": 3}
    assert {speaker: sum(cue["speaker"] == speaker for cue in cues) for speaker in ("れいむ", "まりさ")} == {"れいむ": 3, "まりさ": 6}
    assert script["unsupported_claim_count"] == 0
    assert lineage["checks"]["stage_coverage_T00_T07"] is True
    assert lineage["checks"]["adopted_claims_15"] is True
    assert lineage["checks"]["factual_units_20"] is True
    assert lineage["checks"]["claim_edges_21"] is True
    current_metrics = current["structural_readback"]
    historical_metrics = historical["evidence_snapshot"]["project_verification"]
    for key in ("VoiceItem_count", "fps", "timeline_frames", "duration_seconds"):
        assert current_metrics[key] == historical_metrics[key]
    assert lock["authority_resolution"]["content_lineage"]["current"] == "primary_T00_T07"
    assert lock["authority_resolution"]["editorial_provenance"]["secondary_deep_audit"] == "candidate_D00_D10"
    assert lock["authority_resolution"]["yymm4"]["current"] == "primary_existing_evidence_revalidation"
    assert visual["status"] == "recommended_not_selected"
    assert visual.get("selected_route") is None
    assert visual["human_selection_required"] is True
    assert visual["implementation_authorized"] is False
    with (PILOT / "canonical_yymm4.csv").open(encoding="utf-8-sig", newline="") as handle:
        canonical = list(csv.reader(handle))
    with (PILOT / "derived_yymm4_import.csv").open(encoding="utf-8-sig", newline="") as handle:
        derived = list(csv.reader(handle))
    assert [row[1] for row in canonical] == [row[1] for row in derived]


def test_integrated_json_html_privacy_and_local_binary_boundaries() -> None:
    manifest = _load(MANIFEST)
    paths = {
        row["path"]
        for key in (
            "accepted_candidate_paths",
            "historical_candidate_paths",
            "regenerated_paths",
        )
        for row in manifest[key]
    }
    paths.add(
        "docs/verification/new_banknote_successor_selective_integration_manifest.json"
    )
    paths.add(
        "docs/verification/new_banknote_successor_selective_integration_receipt.json"
    )
    paths.add("docs/verification/NEW_BANKNOTE_SUCCESSOR_SELECTIVE_INTEGRATION.md")
    payloads = [
        _load_historical(path) for path in paths if Path(path).suffix == ".json"
    ]
    assert not (_BANNED_BODY_KEYS & set().union(*map(_all_keys, payloads)))
    privacy_paths = {
        path
        for path in paths
        if Path(path).suffix != ".py" and path != "docs/project-context.md"
    }
    current_context = (
        _git_text_at(HISTORICAL_INTEGRATION_REVISION, "docs/project-context.md")
        .split("## 直前の別端末再開ハンドオフ", 1)[0]
    )
    combined = current_context + "\n" + "\n".join(
        _git_bytes_at(HISTORICAL_INTEGRATION_REVISION, path).decode(
            "utf-8", errors="replace"
        )
        for path in privacy_paths
        if Path(path).suffix in {".json", ".md", ".html"}
    )
    assert _PRIVATE_PATH_RE.search(combined) is None
    assert _UUID_RE.search(combined) is None
    assert "notebooklm.google.com" not in combined.lower()
    board = (
        PILOT / "visual_scene_decision/visual_direction_board.html"
    ).relative_to(REPO_ROOT).as_posix()
    parser = _BoardParser()
    parser.feed(_git_text_at(HISTORICAL_INTEGRATION_REVISION, board))
    assert parser.hrefs
    for href in parser.hrefs:
        assert not href.startswith(("http://", "https://", "file://", "/"))
        target = posixpath.normpath(f"{posixpath.dirname(board)}/{href}")
        assert _git_blob_at(HISTORICAL_INTEGRATION_REVISION, target) is not None
    tracked = subprocess.check_output(
        ["git", "ls-files", "--", str(PILOT / "local_outputs")],
        cwd=REPO_ROOT,
        text=True,
    ).splitlines()
    assert tracked == []
    ignored = manifest["ignored_local_evidence"]
    assert ignored["file_count"] == 3
    assert ignored["all_unchanged"] is True
    assert ignored["all_ignored"] is True


@pytest.mark.requires_local_evidence(
    "historical_yymm4_import_evidence",
    *_ignored_local_evidence_locators(),
)
def test_ignored_local_evidence_matches_historical_integration_receipt() -> None:
    manifest = _load(MANIFEST)
    ignored = manifest["ignored_local_evidence"]
    for row in ignored["artifacts"]:
        path = REPO_ROOT / row["path"]
        assert path.stat().st_size == row["before"]["size"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["before"]["sha256"]
        assert subprocess.run(
            ["git", "check-ignore", "--quiet", "--", str(path)],
            cwd=REPO_ROOT,
            check=False,
        ).returncode == 0
