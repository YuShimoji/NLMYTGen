from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_gui_file(name: str) -> str:
    return (REPO_ROOT / "gui" / name).read_text(encoding="utf-8")


def test_main_exposes_episode_pack_contract() -> None:
    main_js = _read_gui_file("main.js")

    assert "select-episode-pack" in main_js
    assert "save-json-artifact" in main_js
    assert "_validate.json" in main_js
    assert "_dry_run.json" in main_js
    assert "_apply.json" in main_js
    assert "_patched.ymmp" in main_js


def test_renderer_writes_episode_pack_outputs() -> None:
    renderer_js = _read_gui_file("renderer.js")

    assert "episodePack.paths.csv" in renderer_js
    assert "validateResult" in renderer_js
    assert "dryRunResult" in renderer_js
    assert "applyResult" in renderer_js
    assert "episodePack.paths.patchedYmmp" in renderer_js
    assert "output: episodePack && !dryRun ? episodePack.paths.patchedYmmp" in renderer_js


def test_episode_pack_ui_is_documented_in_index() -> None:
    index_html = _read_gui_file("index.html")

    assert "Episode Pack Root" in index_html
    assert "btn-select-episode-pack" in index_html
    assert "episode-pack-expected" in index_html
