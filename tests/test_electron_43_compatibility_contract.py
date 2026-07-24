import hashlib
import json
import subprocess
from pathlib import Path
from urllib.parse import urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
GUI_ROOT = REPO_ROOT / "gui"
SOURCE_COMMIT = "2e11987ff0732d21df4a5da83d1ea557614991ac"
ROLLBACK_LOCK_SHA256 = "81b060f37fd2c7c4151fcf6fc402b554476d4ea6785022c8eef01aaaa9ff4a73"
CANDIDATE_LOCK_SHA256 = "095706aba72687058863d8bca16c5a9a9f7d4e45cde3397dda3197a528d0f047"
UV_LOCK_SHA256 = "40e64f793775f0b0181f5ba8972c17842717dbe14bc8c0a6c0cabd14442435d0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_candidate_manifest_and_lock_resolve_exact_electron_43() -> None:
    manifest = load_json(GUI_ROOT / "package.json")
    lock = load_json(GUI_ROOT / "package-lock.json")

    assert manifest["devDependencies"] == {"electron": "^43.2.0"}
    assert lock["packages"][""]["devDependencies"] == manifest["devDependencies"]
    assert lock["packages"]["node_modules/electron"]["version"] == "43.2.0"
    assert sha256(GUI_ROOT / "package-lock.json") == CANDIDATE_LOCK_SHA256


def test_python_lock_and_rollback_lock_identity_are_preserved() -> None:
    rollback_lock = subprocess.run(
        ["git", "show", f"{SOURCE_COMMIT}:gui/package-lock.json"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    ).stdout

    assert hashlib.sha256(rollback_lock).hexdigest() == ROLLBACK_LOCK_SHA256
    assert sha256(REPO_ROOT / "uv.lock") == UV_LOCK_SHA256


def test_candidate_lock_uses_only_public_portable_sources() -> None:
    lock_text = (GUI_ROOT / "package-lock.json").read_text(encoding="utf-8")
    lock = json.loads(lock_text)

    for package in lock["packages"].values():
        resolved = package.get("resolved")
        if resolved:
            assert resolved.startswith("https://registry.npmjs.org/")
            parsed = urlsplit(resolved)
            assert parsed.username is None
            assert parsed.password is None
    for forbidden in ("file:", "link:", "workspace:", "localhost", "_auth"):
        assert forbidden not in lock_text


def test_smoke_preserves_security_and_real_application_entrypoints() -> None:
    main = (GUI_ROOT / "main.js").read_text(encoding="utf-8")
    preload = (GUI_ROOT / "preload.js").read_text(encoding="utf-8")
    entry = (GUI_ROOT / "electron_compatibility_smoke.js").read_text(encoding="utf-8")
    probe = (GUI_ROOT / "electron_compatibility_probe.js").read_text(encoding="utf-8")

    assert "contextIsolation: true" in main
    assert "nodeIntegration: false" in main
    assert "loadFile(path.join(__dirname, 'index.html'))" in main
    assert "require('./main')" in entry
    assert "NLMYTGEN_AUDIO_POLICY = 'silent'" in entry
    assert "appendSwitch('mute-audio')" in entry
    assert "contextBridge.exposeInMainWorld('nlmytgen'" in preload
    assert "diagnoseScript" in preload
    assert "no_unhandled_renderer_errors" in probe
    assert "integration_timeout_ms" in probe


def test_capture_has_ignored_output_override_without_changing_default() -> None:
    capture = (GUI_ROOT / "capture_pipeline_smoke_fixtures.js").read_text(encoding="utf-8")

    assert "NLMYTGEN_PIPELINE_SMOKE_OUTPUT_ROOT" in capture
    assert "'samples/_probe/pipeline_smoke'" in capture
    assert "NLMYTGEN_PIPELINE_SMOKE_PROFILE" in capture
    assert "offscreen: true" in capture


def test_sanitized_decision_receipt_matches_candidate() -> None:
    receipt = load_json(
        REPO_ROOT / "docs" / "verification" / "ELECTRON_43_COMPATIBILITY_2026-07-25.json"
    )

    assert receipt["classification"] == "upgrade_candidate_ready"
    assert receipt["source"]["commit"] == SOURCE_COMMIT
    assert receipt["candidate"]["electron"] == "43.2.0"
    assert receipt["candidate"]["package_lock_sha256"] == CANDIDATE_LOCK_SHA256
    assert receipt["audit"]["candidate"]["total"] == 0
    assert receipt["actual_gui"]["real_main_window"] is True
    assert receipt["actual_gui"]["production_preload"] is True
    assert receipt["actual_gui"]["sandbox"] is True
    assert receipt["capture"]["topics"] == 3
    assert receipt["execution_boundaries"]["project_electron_processes_after"] == 0
