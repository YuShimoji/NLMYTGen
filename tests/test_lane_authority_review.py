from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from scripts.build_lane_authority_review import (
    SHARED_FIELDS,
    build_lane_authority_review,
    main,
    parse_state_text,
)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def _state_text(prefix: str) -> str:
    revisions = {
        "runtime": ("2026-08-12.1", "2026-08-12 JST"),
        "cockpit": ("2026-08-11.1", "2026-08-11 JST"),
        "successor": ("2026-08-13.1", "2026-08-13 JST"),
    }
    revision, updated = revisions[prefix]
    values = {
        "Project-State-ID": f"{prefix}-state-v1",
        "State-Revision": revision,
        "Updated": updated,
        "Product-State": f"{prefix}-product-state",
        "Product-Gate": f"{prefix}-product-gate",
        "Recommended-Next": f"{prefix}-next-action",
        "External-State": f"{prefix}-external-state",
    }
    return "\n".join(f"{field}: {values[field]}" for field in SHARED_FIELDS) + "\n"


def _write_repo(repo: Path, *, aligned: bool = False) -> None:
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "runtime-state.md").write_text(
        _state_text("runtime"), encoding="utf-8"
    )
    (repo / "docs" / "PROJECT_COCKPIT.md").write_text(
        _state_text("runtime" if aligned else "cockpit"), encoding="utf-8"
    )
    _git(repo, "init")
    _git(repo, "config", "user.name", "Test User")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "add", "docs")
    _git(repo, "commit", "-m", "test state")


def test_parse_state_text_requires_all_seven_fields() -> None:
    text = _state_text("runtime")
    parsed = parse_state_text(text, source="fixture")
    assert tuple(parsed) == SHARED_FIELDS
    with pytest.raises(ValueError, match="External-State"):
        parse_state_text(text.replace("External-State: runtime-external-state\n", ""), source="fixture")


def test_review_reports_all_seven_mismatches_without_adopting(tmp_path: Path) -> None:
    _write_repo(tmp_path)
    before = _git(tmp_path, "status", "--porcelain=v1", "--untracked-files=all")
    report = build_lane_authority_review(tmp_path, remote_ref="missing/ref")
    after = _git(tmp_path, "status", "--porcelain=v1", "--untracked-files=all")

    assert report["mismatch_count"] == 7
    assert len(report["shared_field_comparison"]) == 7
    assert report["automated_adoption"] is False
    assert all(candidate["decision_required"] for candidate in report["candidates"])
    assert all(not candidate["automated_adoption"] for candidate in report["candidates"])
    assert before == after == ""


def test_review_passes_for_aligned_state(tmp_path: Path) -> None:
    _write_repo(tmp_path, aligned=True)
    report = build_lane_authority_review(tmp_path, remote_ref="missing/ref")
    assert report["mismatch_count"] == 0
    assert all(row["matches"] for row in report["shared_field_comparison"])


def test_missing_remote_ref_is_unavailable_not_false_parity(tmp_path: Path) -> None:
    _write_repo(tmp_path)
    remote = build_lane_authority_review(tmp_path, remote_ref="missing/ref")[
        "remote_candidate"
    ]
    assert remote["available"] is False
    assert remote["commit"] is None
    assert remote["state"] is None
    assert remote["error"]


def test_remote_state_is_read_from_git_object_without_checkout(tmp_path: Path) -> None:
    _write_repo(tmp_path)
    original_branch = _git(tmp_path, "branch", "--show-current")
    _git(tmp_path, "switch", "-c", "successor")
    (tmp_path / "docs" / "runtime-state.md").write_text(
        _state_text("successor"), encoding="utf-8"
    )
    _git(tmp_path, "add", "docs/runtime-state.md")
    _git(tmp_path, "commit", "-m", "successor state")
    successor_commit = _git(tmp_path, "rev-parse", "HEAD")
    _git(tmp_path, "switch", original_branch)

    report = build_lane_authority_review(tmp_path, remote_ref="successor")
    remote = report["remote_candidate"]
    assert remote["available"] is True
    assert remote["commit"] == successor_commit
    assert remote["state"]["Project-State-ID"] == "successor-state-v1"
    assert _git(tmp_path, "branch", "--show-current") == original_branch


def test_cli_writes_bounded_json_inside_repo(tmp_path: Path, capsys) -> None:
    _write_repo(tmp_path)
    output = Path("docs/verification/review.json")
    assert main(["--repo-root", str(tmp_path), "--remote-ref", "missing/ref", "--output", str(output)]) == 0
    report = json.loads((tmp_path / output).read_text(encoding="utf-8"))
    assert report["schema_version"] == "nlmytgen-lane-authority-review.v1"
    assert b"\r\n" not in (tmp_path / output).read_bytes()
    assert capsys.readouterr().out == "docs/verification/review.json\n"


def test_cli_rejects_output_outside_repo(tmp_path: Path) -> None:
    _write_repo(tmp_path)
    with pytest.raises(SystemExit):
        main(
            [
                "--repo-root",
                str(tmp_path),
                "--remote-ref",
                "missing/ref",
                "--output",
                str(tmp_path.parent / "outside.json"),
            ]
        )
