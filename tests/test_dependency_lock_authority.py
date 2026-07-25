from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON_MANIFEST = REPO_ROOT / "pyproject.toml"
PYTHON_LOCK = REPO_ROOT / "uv.lock"
GUI_MANIFEST = REPO_ROOT / "gui/package.json"
GUI_LOCK = REPO_ROOT / "gui/package-lock.json"

EXPECTED_MANIFEST_HASHES = {
    "pyproject.toml": "7b9ce97035187e00e396c50aa5d79862fce06c0404cc272435f93136b1efd51d",
    "gui/package.json": "60207998cdd3d1e1459351f1a1fd134120e725a5aa5dbbe93458fcb49e0e3261",
}
EXPECTED_ACCEPTED_AUTHORITY_HASHES = {
    (
        "production_pilots/yukkuri_newsroom_content_spine_002/"
        "external_editorial_input/new_banknote_security_notebooklm_001/"
        "auto_video_pipeline/human_real_media_cut_acceptance_receipt.json"
    ): "cd0b4f02fb54cb0b0dbf8625a5baed6db3952b0a7342257c5456d1426e23f4b8",
    (
        "production_pilots/yukkuri_newsroom_content_spine_002/"
        "external_editorial_input/new_banknote_security_notebooklm_001/"
        "auto_video_pipeline/validated_real_media_run_receipt.json"
    ): "fcdc1a58c7afe3f58307522d7f3a636272bce31c51ab5cb870e111b5b1fcada0",
    (
        "production_pilots/yukkuri_newsroom_content_spine_002/"
        "external_editorial_input/new_banknote_security_notebooklm_001/"
        "auto_video_pipeline/new_banknote_real_media_episode_manifest.json"
    ): "25ac9df0a9af1c0170c88b2e92fef34ff7278934f7d5570e87e4007d44ab46f1",
    (
        "production_pilots/yukkuri_newsroom_content_spine_002/"
        "external_editorial_input/new_banknote_security_notebooklm_001/"
        "auto_video_pipeline/new_banknote_real_media_provenance.json"
    ): "b96275a8e5f84494e17284135c1e4231df51930705a18f48f013d51746c2b920",
}
LOCK_PATHS = ("uv.lock", "gui/package-lock.json")
LOCAL_REFERENCE_PREFIXES = ("file:", "link:", "workspace:")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _walk_strings(value: object):
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_strings(child)
    elif isinstance(value, str):
        yield value


def test_dependency_locks_are_tracked_and_not_ignored() -> None:
    for relative_path in LOCK_PATHS:
        assert (REPO_ROOT / relative_path).is_file()
        assert _git("ls-files", "--error-unmatch", "--", relative_path).returncode == 0
        assert (
            _git(
                "check-ignore",
                "--no-index",
                "--quiet",
                "--",
                relative_path,
            ).returncode
            == 1
        )


def test_dependency_manifests_remain_byte_exact() -> None:
    for relative_path, expected_hash in EXPECTED_MANIFEST_HASHES.items():
        assert _sha256(REPO_ROOT / relative_path) == expected_hash


def test_python_lock_has_no_private_or_machine_local_dependency_source() -> None:
    source = PYTHON_LOCK.read_text(encoding="utf-8")
    assert 'source = { registry = "https://pypi.org/simple" }' in source
    assert "file://" not in source.lower()
    assert not re.search(r"(?im)^\s*(?:path|editable)\s*=", source)
    assert not re.search(r"(?i)(?:^|[\"'])[a-z]:[\\/]", source)
    assert not re.search(r"(?i)(?:^|[\"'])\\\\[^\\]", source)
    assert not re.search(r"https?://[^/\s:@]+:[^/\s@]+@", source)


def test_gui_lock_matches_manifest_and_pins_current_electron_43_2_0() -> None:
    manifest = json.loads(GUI_MANIFEST.read_text(encoding="utf-8"))
    lock = json.loads(GUI_LOCK.read_text(encoding="utf-8"))
    packages = lock["packages"]

    assert lock["lockfileVersion"] == 3
    assert packages[""]["devDependencies"] == manifest["devDependencies"]
    assert manifest["devDependencies"]["electron"] == "^43.2.0"
    assert packages["node_modules/electron"]["version"] == "43.2.0"


def test_gui_lock_has_only_public_https_dependency_sources() -> None:
    raw = GUI_LOCK.read_text(encoding="utf-8")
    lowered_raw = raw.lower()
    assert '"_authtoken"' not in lowered_raw
    assert '"username"' not in lowered_raw
    assert '"password"' not in lowered_raw
    lock = json.loads(raw)
    for value in _walk_strings(lock):
        lowered = value.lower()
        assert not lowered.startswith(LOCAL_REFERENCE_PREFIXES)
        assert not re.match(r"^[a-z]:[\\/]", value, flags=re.IGNORECASE)
        assert not value.startswith("\\\\")

    for package in lock["packages"].values():
        resolved = package.get("resolved")
        if not resolved:
            continue
        parsed = urlsplit(resolved)
        assert parsed.scheme == "https"
        assert parsed.hostname == "registry.npmjs.org"
        assert parsed.username is None
        assert parsed.password is None


def test_readme_uses_locked_reproducible_setup_commands() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "uv sync --extra dev --locked" in readme
    assert "npm --prefix gui ci" in readme
    assert "npm --prefix gui ls --depth=0" in readme


def test_accepted_cut_authority_remains_byte_exact() -> None:
    for relative_path, expected_hash in EXPECTED_ACCEPTED_AUTHORITY_HASHES.items():
        assert _sha256(REPO_ROOT / relative_path) == expected_hash
