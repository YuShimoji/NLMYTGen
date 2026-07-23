"""Git-object based helpers for isolated regression fixtures."""

from __future__ import annotations

import fnmatch
import io
import shutil
import subprocess
import tarfile
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class GitState:
    status: bytes
    worktree_diff: bytes
    cached_diff: bytes


def repo_relative_path(repo_root: Path, path: Path) -> str:
    """Return a Git-safe POSIX path relative to the actual worktree root."""
    root = repo_root.resolve()
    resolved = path.resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError(f"path is outside repository root: {path}") from exc


def snapshot_git_state(repo_root: Path) -> GitState:
    """Capture the three byte-exact Git surfaces guarded by the runner."""

    def git_bytes(*args: str) -> bytes:
        return subprocess.check_output(
            ["git", *args],
            cwd=repo_root,
            stderr=subprocess.STDOUT,
        )

    return GitState(
        status=git_bytes("status", "--porcelain"),
        worktree_diff=git_bytes("diff", "--no-ext-diff"),
        cached_diff=git_bytes("diff", "--cached", "--no-ext-diff"),
    )


def _validate_archive_members(
    destination: Path,
    members: list[tarfile.TarInfo],
) -> None:
    root = destination.resolve()
    for member in members:
        if not (member.isfile() or member.isdir()):
            raise ValueError(
                f"tracked archive contains unsupported entry type: {member.name}"
            )
        resolved = (destination / member.name).resolve()
        if not resolved.is_relative_to(root):
            raise ValueError(
                f"tracked archive entry escapes destination: {member.name}"
            )


def _extract_archive_members(
    archive: tarfile.TarFile,
    destination: Path,
    members: list[tarfile.TarInfo],
) -> None:
    for member in members:
        target = destination / member.name
        if member.isdir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        source = archive.extractfile(member)
        if source is None:
            raise ValueError(
                f"tracked archive file has no readable body: {member.name}"
            )
        with source, target.open("wb") as output:
            shutil.copyfileobj(source, output)
        target.chmod(member.mode & 0o777)


@lru_cache(maxsize=16)
def _tracked_archive_bytes(
    repo_root: str,
    revision: str,
    relative: str,
) -> bytes:
    return subprocess.check_output(
        [
            "git",
            "archive",
            "--format=tar",
            f"{revision}:{relative}",
        ],
        cwd=repo_root,
        stderr=subprocess.STDOUT,
    )


def _excluded_member(
    member: tarfile.TarInfo,
    exclude_names: tuple[str, ...],
) -> bool:
    parts = Path(member.name).parts
    return any(
        fnmatch.fnmatchcase(part, pattern)
        for part in parts
        for pattern in exclude_names
    )


def copy_tracked_tree(
    source: Path,
    destination: Path,
    *,
    repo_root: Path,
    revision: str = "HEAD",
    exclude_names: tuple[str, ...] = (),
) -> Path:
    """Materialize only committed files from ``source`` into ``destination``.

    The source worktree is never traversed. Git creates the archive from the
    requested object, so ignored media, browser profiles, and other private
    evidence cannot enter the fixture even when they are present beside the
    tracked files.
    """
    if destination.exists():
        raise FileExistsError(destination)

    relative = repo_relative_path(repo_root, source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()

    try:
        archive_bytes = _tracked_archive_bytes(
            str(repo_root.resolve()),
            revision,
            relative,
        )
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
            members = [
                member
                for member in archive.getmembers()
                if not _excluded_member(member, exclude_names)
            ]
            _validate_archive_members(destination, members)
            _extract_archive_members(archive, destination, members)
    except BaseException:
        shutil.rmtree(destination)
        raise

    return destination
