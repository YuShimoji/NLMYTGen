from __future__ import annotations

from pathlib import Path

from scripts.check_project_state_sync import check_project_state_sync, main


def _write_state_repo(
    repo_root: Path,
    *,
    runtime_id: str = "episode-002-local-review",
    cockpit_id: str = "episode-002-local-review",
    runtime_line_count: int | None = None,
    link_cockpit: bool = True,
    runtime_updated: str = "2026-07-10 JST",
    cockpit_updated: str = "2026-07-10 JST",
    runtime_next: str = "verify-ymm4-five-observations",
    cockpit_next: str = "verify-ymm4-five-observations",
) -> None:
    docs = repo_root / "docs"
    docs.mkdir()

    runtime_lines = [
        f"Project-State-ID: {runtime_id}",
        "State-Revision: 2026-07-10.1",
        f"Updated: {runtime_updated}",
        "Product-State: episode-002-ymm4-observation-ready",
        "Product-Gate: five-point-ymm4-import-observation",
        f"Recommended-Next: {runtime_next}",
        "External-State: public-repo-feature-branch",
        "",
        "## Current Slice",
        "",
        "The local review slice is active.",
    ]
    if runtime_line_count is not None:
        if runtime_line_count < len(runtime_lines):
            raise ValueError("runtime_line_count is below the fixture minimum")
        runtime_lines.extend(
            f"Bounded state note {index}"
            for index in range(runtime_line_count - len(runtime_lines))
        )

    (docs / "runtime-state.md").write_text(
        "\n".join(runtime_lines) + "\n", encoding="utf-8"
    )
    (docs / "PROJECT_COCKPIT.md").write_text(
        f"# Project Cockpit\n\nProject-State-ID: {cockpit_id}\n"
        "State-Revision: 2026-07-10.1\n"
        f"Updated: {cockpit_updated}\n"
        "Product-State: episode-002-ymm4-observation-ready\n"
        "Product-Gate: five-point-ymm4-import-observation\n"
        f"Recommended-Next: {cockpit_next}\n"
        "External-State: public-repo-feature-branch\n",
        encoding="utf-8",
    )
    readme_line = (
        "[Project Cockpit](docs/PROJECT_COCKPIT.md)"
        if link_cockpit
        else "Project cockpit details are maintained separately."
    )
    (repo_root / "README.md").write_text(
        f"# Fixture Repository\n\n{readme_line}\n", encoding="utf-8"
    )


def test_project_state_sync_passes_for_aligned_state(tmp_path, capsys) -> None:
    _write_state_repo(tmp_path)
    code = main(["--repo-root", str(tmp_path)])
    assert code == 0
    assert capsys.readouterr().out == "PASS: project state is synchronized\n"
    assert check_project_state_sync(tmp_path) == []


def test_project_state_sync_quiet_mode_suppresses_pass_line(tmp_path, capsys) -> None:
    _write_state_repo(tmp_path)
    code = main(["--repo-root", str(tmp_path), "--quiet"])
    assert code == 0
    assert capsys.readouterr().out == ""


def test_project_state_sync_rejects_mismatched_ids(tmp_path) -> None:
    _write_state_repo(
        tmp_path,
        runtime_id="episode-002-local-review",
        cockpit_id="episode-002-real-input",
    )
    assert check_project_state_sync(tmp_path) == [
        "Project-State-ID mismatch: runtime-state=episode-002-local-review, "
        "PROJECT_COCKPIT=episode-002-real-input"
    ]


def test_project_state_sync_rejects_mismatched_updated_dates(tmp_path) -> None:
    _write_state_repo(tmp_path, cockpit_updated="2026-07-09 JST")
    assert check_project_state_sync(tmp_path) == [
        "Updated mismatch: runtime-state=2026-07-10 JST, "
        "PROJECT_COCKPIT=2026-07-09 JST"
    ]


def test_project_state_sync_rejects_same_day_next_action_drift(tmp_path) -> None:
    _write_state_repo(tmp_path, cockpit_next="prepare-verified-real-input")
    assert check_project_state_sync(tmp_path) == [
        "Recommended-Next mismatch: "
        "runtime-state=verify-ymm4-five-observations, "
        "PROJECT_COCKPIT=prepare-verified-real-input"
    ]


def test_project_state_sync_checks_expected_state_id(tmp_path) -> None:
    _write_state_repo(tmp_path)
    errors = check_project_state_sync(
        tmp_path, expected_state_id="supervisor-only-control-boundary-restored-v1"
    )
    assert errors == [
        "Expected Project-State-ID supervisor-only-control-boundary-restored-v1, "
        "found episode-002-local-review"
    ]


def test_project_state_sync_rejects_oversize_runtime_state(tmp_path) -> None:
    _write_state_repo(tmp_path, runtime_line_count=161)
    assert check_project_state_sync(tmp_path) == [
        "docs/runtime-state.md: 161 lines exceeds 160"
    ]


def test_project_state_sync_requires_readme_markdown_link(tmp_path) -> None:
    _write_state_repo(tmp_path, link_cockpit=False)
    assert check_project_state_sync(tmp_path) == [
        "README.md: missing Markdown link to docs/PROJECT_COCKPIT.md"
    ]
