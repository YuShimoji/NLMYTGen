from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

import scripts.check_regression_integrity as regression
from tests.regression_workspace import (
    copy_tracked_tree,
    repo_relative_path,
    snapshot_git_state,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_ROOT = REPO_ROOT / (
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001/"
    "auto_video_pipeline"
)
ACCEPTANCE_RECEIPT = (
    PIPELINE_ROOT / "human_real_media_cut_acceptance_receipt.json"
)
VALIDATED_RECEIPT = PIPELINE_ROOT / "validated_real_media_run_receipt.json"
EXPECTED_MODULES = (
    "tests/test_content_transformation_lineage.py",
    "tests/test_editorial_provenance.py",
    "tests/test_episode_video_pipeline.py",
    "tests/test_media_validation.py",
    "tests/test_new_banknote_authoritative_script.py",
    "tests/test_new_banknote_reference_grounded_visual_design.py",
    "tests/test_new_banknote_reference_layout_reconstruction.py",
    "tests/test_new_banknote_route_a_visual_proof.py",
    "tests/test_new_banknote_successor_selective_integration.py",
    "tests/test_new_banknote_yymm4_existing_evidence_revalidation.py",
    "tests/test_new_banknote_yymm4_import_intake_visual_decision.py",
    "tests/test_new_banknote_yymm4_import_operator_batch.py",
    "tests/test_notebooklm_audio_transcript.py",
    "tests/test_notebooklm_source_reconciliation.py",
    "tests/test_project_state_sync.py",
    "tests/test_silent_media_runtime.py",
)


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


def _make_repo(path: Path) -> Path:
    path.mkdir()
    _git(path, "init", "-q")
    _git(path, "config", "user.name", "Regression Fixture")
    _git(path, "config", "user.email", "regression@example.invalid")
    package = path / "package"
    package.mkdir()
    (path / ".gitignore").write_text(
        "package/private/\nprofiles/\n",
        encoding="utf-8",
    )
    (package / "tracked.txt").write_text("tracked\n", encoding="utf-8")
    _git(path, "add", ".")
    _git(path, "commit", "-q", "-m", "fixture")
    return path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_tracked_workspace_excludes_ignored_large_trees_and_preserves_git(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path / "repo")
    ignored = repo / "package/private/large-media.bin"
    ignored.parent.mkdir(parents=True)
    ignored.write_bytes(b"x" * (2 * 1024 * 1024))
    profile = repo / "profiles/browser/cache.bin"
    profile.parent.mkdir(parents=True)
    profile.write_bytes(b"browser-private")
    before = snapshot_git_state(repo)

    destination = tmp_path / "tracked-copy"
    copy_tracked_tree(
        repo / "package",
        destination,
        repo_root=repo,
    )

    assert (destination / "tracked.txt").read_text(encoding="utf-8") == "tracked\n"
    assert not (destination / "private").exists()
    assert not (destination / "profiles").exists()
    assert snapshot_git_state(repo) == before


def test_unrelated_ignored_evidence_does_not_change_collection_authority(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path / "repo")
    before = regression._pytest_command(tmp_path / "before.xml")
    unrelated = repo / "profiles/browser/unrelated-cache.bin"
    unrelated.parent.mkdir(parents=True)
    unrelated.write_bytes(b"not a collection input")
    after = regression._pytest_command(tmp_path / "after.xml")
    assert tuple(before[3 : 3 + len(EXPECTED_MODULES)]) == EXPECTED_MODULES
    assert tuple(after[3 : 3 + len(EXPECTED_MODULES)]) == EXPECTED_MODULES
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_linked_worktree_git_file_and_repo_relative_ignore_contract(
    tmp_path: Path,
) -> None:
    repo = _make_repo(tmp_path / "repo")
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "--detach", str(linked), "HEAD")
    try:
        assert (linked / ".git").is_file()
        ignored = linked / "package/private/.ignore-contract-probe"
        relative = repo_relative_path(linked, ignored)
        result = subprocess.run(
            ["git", "check-ignore", "--quiet", "--", relative],
            cwd=linked,
            check=False,
        )
        assert result.returncode == 0

        before = snapshot_git_state(linked)
        destination = tmp_path / "linked-tracked-copy"
        copy_tracked_tree(
            linked / "package",
            destination,
            repo_root=linked,
        )
        assert (destination / "tracked.txt").is_file()
        assert not (destination / "private").exists()
        assert snapshot_git_state(linked) == before
    finally:
        _git(repo, "worktree", "remove", "--force", str(linked))
    assert not linked.exists()


def test_private_skip_requires_exact_repo_relative_locator(
    tmp_path: Path,
) -> None:
    junit = tmp_path / "pytest.xml"
    junit.write_text(
        (
            '<testsuite tests="2" failures="0" errors="0" skipped="1">'
            '<testcase classname="portable" name="passes"/>'
            '<testcase classname="private" name="skips">'
            '<skipped message="requires_local_evidence:private_media:'
            'missing=production_pilots/example/local.mp4"/>'
            "</testcase></testsuite>"
        ),
        encoding="utf-8",
    )
    counts, classes, invalid = regression._junit_counts(junit)
    assert counts == {
        "passed": 1,
        "failed": 0,
        "errors": 0,
        "skipped": 1,
        "total": 2,
    }
    assert classes == {"requires_local_evidence:private_media": 1}
    assert invalid == {}
    assert not regression._valid_local_evidence_skip(
        r"requires_local_evidence:private_media:missing=C:\private\file.mp4"
    )
    assert not regression._valid_local_evidence_skip("historical evidence absent")


def test_runner_keeps_canonical_selection_and_removes_temp_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Path | list[str]] = {}

    def fake_run(
        command: list[str],
        *,
        cwd: Path,
        check: bool,
    ) -> subprocess.CompletedProcess[str]:
        assert cwd == tmp_path
        assert check is False
        junit = Path(command[command.index("--junitxml") + 1])
        captured["command"] = command
        captured["temporary_directory"] = junit.parent
        junit.write_text(
            '<testsuite tests="1"><testcase name="pass"/></testsuite>',
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(regression.subprocess, "run", fake_run)
    execution = regression._run_pytest(tmp_path)
    assert regression.CANONICAL_MODULES == EXPECTED_MODULES
    assert "tests/test_regression_integrity_runner.py" not in EXPECTED_MODULES
    assert execution.counts["passed"] == 1
    assert execution.invalid_skip_classes == {}
    assert execution.temporary_workspace_removed is True
    assert not Path(captured["temporary_directory"]).exists()
    command = [str(value) for value in captured["command"]]
    assert command[1:3] == ["-m", "pytest"]
    assert tuple(command[3 : 3 + len(EXPECTED_MODULES)]) == EXPECTED_MODULES
    assert command[-2] == "--junitxml"
    assert command[-1] == str(
        Path(captured["temporary_directory"]) / "pytest.xml"
    )


def test_accepted_cut_receipt_freezes_identity_and_closed_dimensions() -> None:
    receipt = json.loads(ACCEPTANCE_RECEIPT.read_text(encoding="utf-8"))
    validated = json.loads(VALIDATED_RECEIPT.read_text(encoding="utf-8"))
    artifact = receipt["reviewed_artifact"]
    assert receipt["status"] == "stable_internal_cut"
    assert artifact["run_id"] == "new_banknote_real_media_review_v1"
    assert artifact["filename"] == "internal_review_real_media.mp4"
    assert artifact["sha256"] == validated["media"]["sha256"]
    assert (
        artifact["generated_project_sha256"]
        == validated["generated_project"]["sha256"]
    )
    assert receipt["decision"] == {
        "speech": "accepted",
        "wording_order": "accepted",
        "cue_timing": "accepted",
        "subtitle_timing": "accepted",
        "subtitle_line_breaks": "accepted",
        "real_media_visual_treatment": "accepted",
        "rerender_required": False,
    }
    assert receipt["boundary"] == {
        "internal_review_only": True,
        "rights_clearance": False,
        "production": False,
        "publication": False,
        "external_upload": False,
        "release": False,
        "master_merge": False,
    }
    assert _sha256(
        PIPELINE_ROOT / "human_review_visual_rejection_receipt.json"
    ) == (
        "aae43809b8afe00b3cec27840e7fef099a65c89c4082df4cf3e664fe7ca19fca"
    )
