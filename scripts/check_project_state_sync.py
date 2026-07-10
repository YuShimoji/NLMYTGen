#!/usr/bin/env python3
"""Check that the repository's compact project-state surfaces stay aligned."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[1]
MAX_RUNTIME_STATE_LINES = 160

_STATE_ID_RE = re.compile(r"^Project-State-ID: ([a-z0-9]+(?:-[a-z0-9]+)*)$")
_UPDATED_RE = re.compile(r"^Updated: (\d{4}-\d{2}-\d{2} JST)$")
_SHARED_FIELD_PATTERNS = {
    "State-Revision": re.compile(r"^State-Revision: ([a-z0-9]+(?:[.-][a-z0-9]+)*)$"),
    "Product-State": re.compile(r"^Product-State: ([a-z0-9]+(?:-[a-z0-9]+)*)$"),
    "Product-Gate": re.compile(r"^Product-Gate: ([a-z0-9]+(?:-[a-z0-9]+)*)$"),
    "Recommended-Next": re.compile(r"^Recommended-Next: ([a-z0-9]+(?:-[a-z0-9]+)*)$"),
    "External-State": re.compile(r"^External-State: ([a-z0-9]+(?:-[a-z0-9]+)*)$"),
}
_COCKPIT_INLINE_LINK_RE = re.compile(
    r"\]\(\s*<?(?:\./)?docs/PROJECT_COCKPIT\.md"
    r"(?:#[^)\s>]*)?>?(?:\s+[^)]*)?\)"
)
_COCKPIT_REFERENCE_LINK_RE = re.compile(
    r"^\s{0,3}\[[^]]+\]:\s*<?(?:\./)?docs/PROJECT_COCKPIT\.md"
    r"(?:#[^\s>]*)?>?(?:\s+.*)?$",
    re.MULTILINE,
)


def _read_text(repo_root: Path, relative_path: str, errors: list[str]) -> str | None:
    path = repo_root / relative_path
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing file: {relative_path}")
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot read {relative_path}: {exc}")
    return None


def _state_id(text: str, relative_path: str, errors: list[str]) -> str | None:
    state_ids = [
        match.group(1)
        for line in text.splitlines()
        if (match := _STATE_ID_RE.fullmatch(line)) is not None
    ]
    if len(state_ids) != 1:
        errors.append(
            f"{relative_path}: expected exactly one lowercase Project-State-ID line; "
            f"found {len(state_ids)}"
        )
        return None
    return state_ids[0]


def _updated_value(text: str, relative_path: str, errors: list[str]) -> str | None:
    updated_values = [
        match.group(1)
        for line in text.splitlines()
        if (match := _UPDATED_RE.fullmatch(line)) is not None
    ]
    if len(updated_values) != 1:
        errors.append(
            f"{relative_path}: expected exactly one ISO-date Updated line; "
            f"found {len(updated_values)}"
        )
        return None
    return updated_values[0]


def _shared_fields(text: str, relative_path: str, errors: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    lines = text.splitlines()
    for field_name, pattern in _SHARED_FIELD_PATTERNS.items():
        values = [
            match.group(1)
            for line in lines
            if (match := pattern.fullmatch(line)) is not None
        ]
        if len(values) != 1:
            errors.append(
                f"{relative_path}: expected exactly one {field_name} line; "
                f"found {len(values)}"
            )
        else:
            fields[field_name] = values[0]
    return fields


def _has_cockpit_link(readme: str) -> bool:
    return bool(
        _COCKPIT_INLINE_LINK_RE.search(readme)
        or _COCKPIT_REFERENCE_LINK_RE.search(readme)
    )


def check_project_state_sync(
    repo_root: str | Path = DEFAULT_REPO_ROOT,
    *,
    expected_state_id: str | None = None,
) -> list[str]:
    """Return all project-state synchronization errors for *repo_root*."""

    root = Path(repo_root).resolve()
    errors: list[str] = []
    runtime = _read_text(root, "docs/runtime-state.md", errors)
    cockpit = _read_text(root, "docs/PROJECT_COCKPIT.md", errors)
    readme = _read_text(root, "README.md", errors)

    runtime_id = cockpit_id = None
    runtime_updated = cockpit_updated = None
    runtime_fields: dict[str, str] = {}
    cockpit_fields: dict[str, str] = {}
    if runtime is not None:
        runtime_id = _state_id(runtime, "docs/runtime-state.md", errors)
        runtime_updated = _updated_value(runtime, "docs/runtime-state.md", errors)
        runtime_fields = _shared_fields(runtime, "docs/runtime-state.md", errors)
        current_slice_count = sum(
            line == "## Current Slice" for line in runtime.splitlines()
        )
        if current_slice_count != 1:
            errors.append(
                "docs/runtime-state.md: expected exactly one '## Current Slice'; "
                f"found {current_slice_count}"
            )
        line_count = len(runtime.splitlines())
        if line_count > MAX_RUNTIME_STATE_LINES:
            errors.append(
                f"docs/runtime-state.md: {line_count} lines exceeds {MAX_RUNTIME_STATE_LINES}"
            )

    if cockpit is not None:
        cockpit_id = _state_id(cockpit, "docs/PROJECT_COCKPIT.md", errors)
        cockpit_updated = _updated_value(cockpit, "docs/PROJECT_COCKPIT.md", errors)
        cockpit_fields = _shared_fields(cockpit, "docs/PROJECT_COCKPIT.md", errors)

    if runtime_id is not None and cockpit_id is not None and runtime_id != cockpit_id:
        errors.append(
            "Project-State-ID mismatch: "
            f"runtime-state={runtime_id}, PROJECT_COCKPIT={cockpit_id}"
        )
    if (
        runtime_updated is not None
        and cockpit_updated is not None
        and runtime_updated != cockpit_updated
    ):
        errors.append(
            "Updated mismatch: "
            f"runtime-state={runtime_updated}, PROJECT_COCKPIT={cockpit_updated}"
        )
    for field_name in _SHARED_FIELD_PATTERNS:
        runtime_value = runtime_fields.get(field_name)
        cockpit_value = cockpit_fields.get(field_name)
        if (
            runtime_value is not None
            and cockpit_value is not None
            and runtime_value != cockpit_value
        ):
            errors.append(
                f"{field_name} mismatch: runtime-state={runtime_value}, "
                f"PROJECT_COCKPIT={cockpit_value}"
            )

    if expected_state_id is not None:
        if not _STATE_ID_RE.fullmatch(f"Project-State-ID: {expected_state_id}"):
            errors.append(
                "expected state id must be a lowercase hyphenated slug: "
                f"{expected_state_id}"
            )
        elif runtime_id is not None and runtime_id != expected_state_id:
            errors.append(
                f"Expected Project-State-ID {expected_state_id}, found {runtime_id}"
            )

    if readme is not None and not _has_cockpit_link(readme):
        errors.append("README.md: missing Markdown link to docs/PROJECT_COCKPIT.md")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check that project-state documents are synchronized."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help="Repository root (default: root containing this script).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress the PASS line; errors are still printed.",
    )
    parser.add_argument(
        "--expected-state-id",
        help="Require the capsule to match this state id.",
    )
    args = parser.parse_args(argv)

    errors = check_project_state_sync(
        args.repo_root, expected_state_id=args.expected_state_id
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if not args.quiet:
        print("PASS: project state is synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
