"""Run the canonical clean-room regression set without changing Git state."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
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


@dataclass(frozen=True)
class GitSnapshot:
    status: bytes
    worktree_diff: bytes
    cached_diff: bytes


def _git_bytes(*args: str) -> bytes:
    return subprocess.check_output(
        ["git", *args],
        cwd=REPO_ROOT,
        stderr=subprocess.STDOUT,
    )


def _snapshot() -> GitSnapshot:
    return GitSnapshot(
        status=_git_bytes(
            "status", "--porcelain=v1", "--untracked-files=all"
        ),
        worktree_diff=_git_bytes("diff", "--binary"),
        cached_diff=_git_bytes("diff", "--cached", "--binary"),
    )


def _skip_class(message: str) -> str:
    marker = "requires_local_evidence:"
    if marker in message:
        suffix = message.split(marker, 1)[1]
        artifact_class = suffix.split(":", 1)[0]
        return f"{marker}{artifact_class}"
    normalized = " ".join(message.split())
    return normalized or "unclassified_skip"


def _junit_counts(path: Path) -> tuple[dict[str, int], dict[str, int]]:
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
    skip_classes = Counter(
        _skip_class(node.get("message", "")) for node in skipped_nodes
    )
    return counts, dict(sorted(skip_classes.items()))


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
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="nlmytgen-regression-integrity-") as temp:
        junit_path = Path(temp) / "pytest.xml"
        command = [
            sys.executable,
            "-m",
            "pytest",
            *CANONICAL_MODULES,
            "--junitxml",
            str(junit_path),
        ]
        completed = subprocess.run(command, cwd=REPO_ROOT, check=False)
        elapsed = time.perf_counter() - started
        if junit_path.is_file():
            counts, skip_classes = _junit_counts(junit_path)
        else:
            counts = {
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "skipped": 0,
                "total": 0,
            }
            skip_classes = {}

    after = _snapshot()
    integrity = {
        "status_unchanged": before.status == after.status,
        "worktree_diff_unchanged": before.worktree_diff == after.worktree_diff,
        "cached_diff_unchanged": before.cached_diff == after.cached_diff,
    }
    integrity["passed"] = all(integrity.values())
    summary = {
        "modules": list(CANONICAL_MODULES),
        "counts": counts,
        "skip_classes": skip_classes,
        "elapsed_seconds": round(elapsed, 3),
        "workspace_integrity": integrity,
        "pytest_exit_code": completed.returncode,
    }
    print("Regression integrity summary:")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if completed.returncode == 0 and integrity["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
