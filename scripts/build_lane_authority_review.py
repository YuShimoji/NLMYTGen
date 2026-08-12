#!/usr/bin/env python3
"""Build a read-only review of competing NLMYTGen lane authorities."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REMOTE_REF = "origin/codex/nlmytgen-portable-review-bundle-v1"
SHARED_FIELDS = (
    "Project-State-ID",
    "State-Revision",
    "Updated",
    "Product-State",
    "Product-Gate",
    "Recommended-Next",
    "External-State",
)


@dataclass(frozen=True)
class GitResult:
    returncode: int
    stdout: str
    stderr: str


def _git(repo_root: Path, *args: str) -> GitResult:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return GitResult(
        returncode=completed.returncode,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
    )


def _required_git(repo_root: Path, *args: str) -> str:
    result = _git(repo_root, *args)
    if result.returncode != 0:
        detail = result.stderr or result.stdout or "unknown git failure"
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout


def parse_state_text(text: str, *, source: str) -> dict[str, str]:
    """Parse the seven shared state fields, rejecting duplicates and omissions."""

    values: dict[str, str] = {}
    lines = text.splitlines()
    for field in SHARED_FIELDS:
        prefix = f"{field}: "
        matches = [line[len(prefix) :] for line in lines if line.startswith(prefix)]
        if len(matches) != 1 or not matches[0].strip():
            raise ValueError(
                f"{source}: expected exactly one non-empty {field} line; "
                f"found {len(matches)}"
            )
        values[field] = matches[0].strip()
    return values


def _read_local_state(repo_root: Path, relative_path: str) -> dict[str, str]:
    path = repo_root / relative_path
    return parse_state_text(path.read_text(encoding="utf-8"), source=relative_path)


def _capture_status(repo_root: Path) -> dict[str, Any]:
    status_text = _required_git(
        repo_root, "status", "--porcelain=v1", "--untracked-files=all"
    )
    entries = status_text.splitlines() if status_text else []
    tracked = [entry for entry in entries if not entry.startswith("??")]
    untracked = [entry for entry in entries if entry.startswith("??")]
    return {
        "clean": not entries,
        "tracked_change_count": len(tracked),
        "untracked_count": len(untracked),
        "entries": entries,
    }


def _capture_git_snapshot(repo_root: Path) -> dict[str, Any]:
    upstream = _git(repo_root, "rev-parse", "--abbrev-ref", "@{upstream}")
    return {
        "branch": _required_git(repo_root, "branch", "--show-current"),
        "head": _required_git(repo_root, "rev-parse", "HEAD"),
        "upstream": upstream.stdout if upstream.returncode == 0 else None,
        "status": _capture_status(repo_root),
    }


def _capture_remote_candidate(repo_root: Path, remote_ref: str) -> dict[str, Any]:
    commit = _git(repo_root, "rev-parse", "--verify", f"{remote_ref}^{{commit}}")
    if commit.returncode != 0:
        return {
            "ref": remote_ref,
            "available": False,
            "commit": None,
            "state": None,
            "error": commit.stderr or commit.stdout or "ref not available",
        }

    state_file = _git(repo_root, "show", f"{remote_ref}:docs/runtime-state.md")
    if state_file.returncode != 0:
        return {
            "ref": remote_ref,
            "available": True,
            "commit": commit.stdout,
            "state": None,
            "error": state_file.stderr or state_file.stdout,
        }

    try:
        state = parse_state_text(
            state_file.stdout, source=f"{remote_ref}:docs/runtime-state.md"
        )
    except ValueError as exc:
        return {
            "ref": remote_ref,
            "available": True,
            "commit": commit.stdout,
            "state": None,
            "error": str(exc),
        }
    return {
        "ref": remote_ref,
        "available": True,
        "commit": commit.stdout,
        "state": state,
        "error": None,
    }


def _decision_candidates(remote_available: bool) -> list[dict[str, Any]]:
    return [
        {
            "id": "keep-six-channel-as-current-owner",
            "decision_required": True,
            "automated_adoption": False,
            "effect": "Keep the six-channel control plane and B05 static intake as the current working authority.",
            "preserves": "The unpublished six-channel commit and its bounded static evidence contract.",
            "safe_default": True,
        },
        {
            "id": "promote-remote-successor-lane",
            "decision_required": True,
            "automated_adoption": False,
            "effect": "Move project authority to the repaired 29.616-second history-proof human-review gate.",
            "preserves": "The remote successor history without claiming its untracked proof bytes are locally available.",
            "remote_evidence_available": remote_available,
            "safe_default": False,
        },
        {
            "id": "synchronize-cockpit-only",
            "decision_required": True,
            "automated_adoption": False,
            "effect": "Make PROJECT_COCKPIT mirror the six-channel runtime capsule.",
            "preserves": "The current code and media boundaries while changing the portfolio-level authority declaration.",
            "safe_default": False,
        },
        {
            "id": "return-to-default-master",
            "decision_required": True,
            "automated_adoption": False,
            "effect": "Return authority to the older Episode 002 default-branch state.",
            "preserves": "A synchronized public default branch at the cost of dropping later lanes from current authority.",
            "safe_default": False,
        },
        {
            "id": "merge-lanes-now",
            "decision_required": True,
            "automated_adoption": False,
            "effect": "Attempt to combine the unpublished six-channel work with the remote successor history.",
            "preserves": "Neither lane's meaning without an explicit conflict and authority review.",
            "safe_default": False,
        },
    ]


def build_lane_authority_review(
    repo_root: str | Path = DEFAULT_REPO_ROOT,
    *,
    remote_ref: str = DEFAULT_REMOTE_REF,
) -> dict[str, Any]:
    """Return a review packet without changing files, refs, index, or worktree."""

    root = Path(repo_root).resolve()
    runtime = _read_local_state(root, "docs/runtime-state.md")
    cockpit = _read_local_state(root, "docs/PROJECT_COCKPIT.md")
    comparison = [
        {
            "field": field,
            "runtime_state": runtime[field],
            "project_cockpit": cockpit[field],
            "matches": runtime[field] == cockpit[field],
        }
        for field in SHARED_FIELDS
    ]
    remote = _capture_remote_candidate(root, remote_ref)
    return {
        "schema_version": "nlmytgen-lane-authority-review.v1",
        "review_only": True,
        "automated_adoption": False,
        "media_opened": False,
        "audio_played": False,
        "git": _capture_git_snapshot(root),
        "local_documents": {
            "runtime_state": runtime,
            "project_cockpit": cockpit,
        },
        "shared_field_comparison": comparison,
        "mismatch_count": sum(not row["matches"] for row in comparison),
        "remote_candidate": remote,
        "candidates": _decision_candidates(bool(remote["available"])),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a read-only review of competing lane authorities."
    )
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--remote-ref", default=DEFAULT_REMOTE_REF)
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional JSON output path; must stay inside the repository root.",
    )
    args = parser.parse_args(argv)

    root = args.repo_root.resolve()
    report = build_lane_authority_review(root, remote_ref=args.remote_ref)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(rendered, end="")
        return 0

    output = args.output
    if not output.is_absolute():
        output = root / output
    output = output.resolve()
    try:
        output.relative_to(root)
    except ValueError:
        parser.error("--output must stay inside --repo-root")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(rendered)
    print(output.relative_to(root).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
