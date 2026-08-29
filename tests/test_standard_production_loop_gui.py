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
        for name in ("basis", "episode", "runtime", "content", "run", "result")
    ]
    assert step_positions == sorted(step_positions)


def test_standard_loop_bridge_covers_manifest_doctor_dry_run_job_and_result() -> None:
    preload = (GUI_ROOT / "preload.js").read_text(encoding="utf-8")
    main = (GUI_ROOT / "main.js").read_text(encoding="utf-8")
    for channel in (
        "standard-loop-current-basis",
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
    assert "ALL_RUNTIME_PROFILES_NOT_READY" in main
    assert "SILENT_POLICY_REQUIRED" in main
    assert "realRenderProbe" not in main
    assert "standardLoopDryRunKey" in main
    assert "CURRENT_BASIS_BLOCKED" in main
    assert "LEGACY_MANIFEST_RETIRED" in main
    assert main.count("currentBasisCliBlock()") >= 6
    assert "ipcMain.handle('batch-default-selections'" in main
    assert "ipcMain.handle('batch-start'" in main


def test_standard_loop_exposes_current_basis_classification_without_copying_peer_vocabulary() -> None:
    html = (GUI_ROOT / "index.html").read_text(encoding="utf-8")
    renderer = (GUI_ROOT / "renderer.js").read_text(encoding="utf-8")
    assert "Evidence / Rule で閉じた判断" in html
    assert "Human correction（未回答）" in html
    assert "旧様式として退役" in html
    assert "standardLoopCurrentBasis" in renderer
    assert "['batch', 'csv', 'production']" in renderer
    assert 'id="standard-cockpit-artifact-sha"' in html
    assert 'id="standard-cockpit-source-artifact"' in html
    assert 'id="standard-cockpit-source-sha"' in html
    assert 'id="standard-cockpit-resulting-artifact"' in html
    assert 'id="standard-decision-chain"' in html
    assert 'id="btn-standard-open-basis"' in html
    assert 'id="standard-cockpit-artifact-preview"' in html
    assert 'id="standard-cockpit-artifact-content"' in html
    assert 'id="btn-standard-enter-intake"' in html
    assert "CURRENT_INTAKE_ROUTE_REACHED" in renderer
    assert "ARTIFACT_OPENED" in renderer
    assert "basis.decision_case.artifact_content" in renderer
    assert "Human correction:" in renderer
    assert "Resulting artifact:" in renderer
    assert "standardLoadAcceptedManifest();" not in renderer
    assert "standardRunDoctor();" not in renderer
    assert "window.nlmytgen.openRepoDoc(basis.path)" not in renderer
    assert "ClipPipeGen" not in html


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
    assert package["scripts"]["smoke:three-run-repeatability"] == (
        "electron three_run_operator_repeatability_smoke.js"
    )
