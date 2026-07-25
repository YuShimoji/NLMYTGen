from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GUI_ROOT = REPO_ROOT / "gui"


def test_standard_loop_is_default_and_legacy_tabs_are_preserved() -> None:
    html = (GUI_ROOT / "index.html").read_text(encoding="utf-8")
    assert '<button class="tab active" data-tab="standard">自動動画生成</button>' in html
    for label in ("CSV 変換", "演出適用", "デザインレビュー", "品質診断"):
        assert f">{label}</button>" in html
    step_positions = [
        html.index(f'id="standard-step-{name}"')
        for name in ("episode", "runtime", "content", "run", "result")
    ]
    assert step_positions == sorted(step_positions)


def test_standard_loop_bridge_covers_manifest_doctor_dry_run_job_and_result() -> None:
    preload = (GUI_ROOT / "preload.js").read_text(encoding="utf-8")
    main = (GUI_ROOT / "main.js").read_text(encoding="utf-8")
    for channel in (
        "standard-loop-accepted-manifest",
        "standard-loop-select-manifest",
        "standard-loop-load-manifest",
        "standard-loop-doctor",
        "standard-loop-dry-run",
        "standard-loop-start",
        "standard-loop-cancel",
        "standard-loop-job",
        "standard-loop-open-output",
    ):
        assert channel in preload
        assert channel in main
    assert "PIPELINE_JOB_ALREADY_ACTIVE" in (
        GUI_ROOT / "standard_production_loop.js"
    ).read_text(encoding="utf-8")
    assert "SUCCESSFUL_DRY_RUN_REQUIRED" in main
    assert "REGENERATE_PROFILE_NOT_READY" in main
    assert "SILENT_POLICY_REQUIRED" in main


def test_gui_slice_adds_no_generated_design_asset_or_forbidden_visual_direction() -> None:
    html = (GUI_ROOT / "index.html").read_text(encoding="utf-8").lower()
    css = (GUI_ROOT / "style.css").read_text(encoding="utf-8").lower()
    standard_html = html[html.index('id="tab-standard"') : html.index("<!-- csv")]
    standard_css = css[
        css.index("/* 標準自動制作ループ") : css.index("/* drop zone */")
    ]
    assert "<img" not in standard_html
    assert "<svg" not in standard_html
    assert "gradient(" not in standard_css
    assert "hero" not in standard_html
    assert "card-grid" not in standard_html
    assert "border-radius: 999" not in standard_css
    assert "<button" in standard_html
    assert ">公開<" not in standard_html
    assert ">アップロード<" not in standard_html


def test_package_scripts_expose_focused_contract_and_electron_smoke() -> None:
    package = json.loads((GUI_ROOT / "package.json").read_text(encoding="utf-8"))
    assert package["scripts"]["test:standard-production-loop"] == (
        "node --test standard_production_loop.test.js"
    )
    assert package["scripts"]["smoke:standard-production-loop"] == (
        "electron standard_production_loop_smoke.js"
    )
