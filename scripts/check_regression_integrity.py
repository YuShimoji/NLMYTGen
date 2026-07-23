"""Run the canonical clean-room regression set without changing Git state."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree


REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_MODULES = (
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
_LOCAL_EVIDENCE_SKIP_RE = re.compile(
    r"^requires_local_evidence:"
    r"(?P<artifact_class>[a-z0-9_]+):"
    r"missing=(?P<locators>[^,\s]+(?:,[^,\s]+)*)$"
)


@dataclass(frozen=True)
class GitSnapshot:
    status: bytes
    worktree_diff: bytes
    cached_diff: bytes


@dataclass(frozen=True)
class RegressionExecution:
    counts: dict[str, int]
    skip_classes: dict[str, int]
    invalid_skip_classes: dict[str, int]
    elapsed_seconds: float
    pytest_exit_code: int
    temporary_workspace_removed: bool


def _git_bytes(repo_root: Path, *args: str) -> bytes:
    return subprocess.check_output(
        ["git", *args],
        cwd=repo_root,
        stderr=subprocess.STDOUT,
    )


def _snapshot(repo_root: Path = REPO_ROOT) -> GitSnapshot:
    return GitSnapshot(
        status=_git_bytes(repo_root, "status", "--porcelain"),
        worktree_diff=_git_bytes(repo_root, "diff", "--no-ext-diff"),
        cached_diff=_git_bytes(
            repo_root,
            "diff",
            "--cached",
            "--no-ext-diff",
        ),
    )


def _skip_class(message: str) -> str:
    marker = "requires_local_evidence:"
    if marker in message:
        suffix = message.split(marker, 1)[1]
        artifact_class = suffix.split(":", 1)[0]
        return f"{marker}{artifact_class}"
    normalized = " ".join(message.split())
    return normalized or "unclassified_skip"


def _valid_local_evidence_skip(message: str) -> bool:
    normalized = " ".join(message.split())
    match = _LOCAL_EVIDENCE_SKIP_RE.fullmatch(normalized)
    if match is None:
        return False
    for locator in match.group("locators").split(","):
        if "\\" in locator or re.match(r"^[a-zA-Z]:", locator):
            return False
        path = PurePosixPath(locator)
        if path.is_absolute() or ".." in path.parts:
            return False
    return True


def _junit_counts(
    path: Path,
) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    root = ElementTree.parse(path).getroot()
    testcases = root.findall(".//testcase")
    failures = sum(case.find("failure") is not None for case in testcases)
    errors = sum(case.find("error") is not None for case in testcases)
    skipped_nodes = [
        skipped
        for case in testcases
        if (skipped := case.find("skipped")) is not None
    ]
    skipped = len(skipped_nodes)
    total = len(testcases)
    counts = {
        "passed": total - failures - errors - skipped,
        "failed": failures,
        "errors": errors,
        "skipped": skipped,
        "total": total,
    }
    skip_rows = [
        (
            _skip_class(node.get("message", "")),
            _valid_local_evidence_skip(node.get("message", "")),
        )
        for node in skipped_nodes
    ]
    skip_classes = Counter(row[0] for row in skip_rows)
    invalid_skip_classes = Counter(
        row[0] for row in skip_rows if not row[1]
    )
    return (
        counts,
        dict(sorted(skip_classes.items())),
        dict(sorted(invalid_skip_classes.items())),
    )


def _pytest_command(junit_path: Path) -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        *CANONICAL_MODULES,
        "--junitxml",
        str(junit_path),
    ]


def _run_pytest(repo_root: Path = REPO_ROOT) -> RegressionExecution:
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(
        prefix="nlmytgen-regression-integrity-"
    ) as temp:
        temp_path = Path(temp)
        junit_path = temp_path / "pytest.xml"
        completed = subprocess.run(
            _pytest_command(junit_path),
            cwd=repo_root,
            check=False,
        )
        elapsed = time.perf_counter() - started
        if junit_path.is_file():
            counts, skip_classes, invalid_skip_classes = _junit_counts(
                junit_path
            )
        else:
            counts = {
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "skipped": 0,
                "total": 0,
            }
            skip_classes = {}
            invalid_skip_classes = {"missing_junit_report": 1}
    return RegressionExecution(
        counts=counts,
        skip_classes=skip_classes,
        invalid_skip_classes=invalid_skip_classes,
        elapsed_seconds=round(elapsed, 3),
        pytest_exit_code=completed.returncode,
        temporary_workspace_removed=not temp_path.exists(),
    )


def main() -> int:
    missing = [
        module
        for module in CANONICAL_MODULES
        if not (REPO_ROOT / module).is_file()
    ]
    if missing:
        print(json.dumps({"missing_modules": missing}, indent=2))
        return 2

    print("Canonical regression modules:", flush=True)
    for module in CANONICAL_MODULES:
        print(f"- {module}", flush=True)

    before = _snapshot()
    execution = _run_pytest()
    after = _snapshot()
    integrity = {
        "status_unchanged": before.status == after.status,
        "worktree_diff_unchanged": before.worktree_diff == after.worktree_diff,
        "cached_diff_unchanged": before.cached_diff == after.cached_diff,
    }
    integrity["passed"] = all(integrity.values())
    skip_contract = {
        "valid": not execution.invalid_skip_classes,
        "invalid_classes": execution.invalid_skip_classes,
    }
    summary = {
        "modules": list(CANONICAL_MODULES),
        "counts": execution.counts,
        "skip_classes": execution.skip_classes,
        "skip_contract": skip_contract,
        "elapsed_seconds": execution.elapsed_seconds,
        "workspace_integrity": integrity,
        "temporary_workspace_removed": (
            execution.temporary_workspace_removed
        ),
        "pytest_exit_code": execution.pytest_exit_code,
    }
    print("Regression integrity summary:")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return (
        0
        if (
            execution.pytest_exit_code == 0
            and integrity["passed"]
            and skip_contract["valid"]
            and execution.temporary_workspace_removed
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
