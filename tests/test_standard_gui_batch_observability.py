import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / "gui"


def read(name: str) -> str:
    return (GUI / name).read_text(encoding="utf-8")


def batch_html() -> str:
    html = read("index.html")
    return html[html.index('id="tab-batch"') : html.index("<!-- CSV")]


def test_standard_route_remains_default_and_batch_is_secondary() -> None:
    html = read("index.html")
    assert '<button class="tab active" data-tab="standard">自動動画生成</button>' in html
    assert '<button class="tab" data-tab="batch">バッチ実行</button>' in html
    assert html.index('data-tab="standard"') < html.index('data-tab="batch"')
    assert '<section id="tab-standard" class="tab-content active"' in html
    assert '<section id="tab-batch" class="tab-content"' in html


def test_batch_vertical_spine_and_first_viewport_information_order() -> None:
    html = batch_html()
    ordered = [
        "batch-step-inputs",
        "batch-step-plan",
        "batch-step-packages",
        "batch-step-authority",
        "batch-step-journal",
        "batch-step-result",
    ]
    positions = [html.index(f'id="{item}"') for item in ordered]
    assert positions == sorted(positions)
    for required in (
        "batch-queue-path",
        "batch-change-set-path",
        "batch-plan-status",
        "batch-mutation-count",
        "batch-next-action",
        "btn-batch-plan",
    ):
        assert f'id="{required}"' in html


def test_keyboard_control_order_matches_operator_sequence() -> None:
    html = batch_html()
    controls = [
        "btn-batch-select-queue",
        "btn-batch-select-change-set",
        "btn-batch-plan",
        "btn-batch-execute",
        "btn-batch-select-authority",
        "btn-batch-select-journal",
        "btn-batch-resume",
        "btn-batch-cancel",
        "btn-batch-result-details",
    ]
    positions = [html.index(f'id="{item}"') for item in controls]
    assert positions == sorted(positions)


def test_all_exact_journal_states_and_authority_states_are_mapped() -> None:
    module = read("batch_observability.js")
    for state in (
        "not_selected",
        "verified_noop",
        "planned",
        "authority_validated",
        "started",
        "succeeded",
        "failed",
        "effect_unknown",
        "skipped_after_failure",
    ):
        assert state in module
    for authority in (
        "not_required",
        "required",
        "absent",
        "invalid",
        "available",
        "consumed",
        "replacement_required",
        "reconciliation_required",
    ):
        assert authority in module
    assert "自動再試行不可・読み取り照合" in module
    assert "変更はありません" in module


def test_ipc_bridge_uses_actual_executor_and_safe_dialog_boundary() -> None:
    main = read("main.js")
    preload = read("preload.js")
    renderer = read("batch_renderer.js")
    module = read("batch_observability.js")
    for channel in (
        "batch-default-selections",
        "batch-select-file",
        "batch-open-recent-journal",
        "batch-start",
        "batch-cancel",
        "batch-job",
    ):
        assert f"ipcMain.handle('{channel}'" in main
    assert "dialog.showOpenDialog(mainWindow" in main
    assert "nlmytgen.factory_queue.v1" in main
    assert "nlmytgen.factory_queue.change_set.v1" in main
    assert "BATCH_${kind.toUpperCase()}_SCHEMA_INVALID" in main
    assert "'execute-factory-queue'" in module
    assert "'--queue'" in module
    assert "'--change-set'" in module
    assert "'--execute'" in module
    assert "'--resume-journal'" in module
    assert "shell command" not in batch_html().lower()
    assert "batchStart: (request)" in preload
    assert "onBatchJobEvent" in preload
    assert "window.nlmytgen.batchStart" in renderer


def test_single_job_and_project_owned_cancellation_are_shared() -> None:
    main = read("main.js")
    module = read("batch_observability.js")
    assert "isOtherJobActive: () => standardLoopJobs.snapshot().active" in main
    assert "if (batchJobs.snapshot().active)" in main
    assert "cancelProcess: cancelOwnedProcessTree" in main
    assert "PIPELINE_JOB_ALREADY_ACTIVE" in module
    assert "NO_MATCHING_ACTIVE_PIPELINE_JOB" in module
    assert "MAX_BATCH_LOG_LINES = 240" in module
    assert "worker pool" not in module.lower()
    assert "daemon" not in module.lower()


def test_executor_locators_and_local_journal_storage_stay_repo_relative() -> None:
    main = read("main.js")
    assert "path.join(REPO_ROOT, '_tmp', 'gui-batch-journals')" in main
    assert "registerBatchSelection(kind, result.filePaths[0], { repoOnly: true })" in main
    assert "authorityPath: mode === 'execute' ? (authority?.displayPath || null) : null" in main
    assert "journalPath: mode === 'execute' ? (journal?.displayPath || null) : null" in main
    assert "authority?.fullPath" not in main
    assert "journal?.fullPath" not in main


def test_batch_surface_is_japanese_first_without_forbidden_visual_system() -> None:
    html = batch_html()
    style = read("style.css")
    batch_style = style[style.index("/* Bounded batch") : style.index("/* Drop zone */")]
    for label in (
        "バッチ実行",
        "実行計画を確認",
        "変更対象",
        "権限状態",
        "Journal を開く",
        "安全な位置から再開",
        "実行を取り消す",
    ):
        assert label in html
    lowered = html.lower()
    assert "<svg" not in lowered
    assert "hero" not in lowered
    assert "card-grid" not in lowered
    assert "bento" not in lowered
    assert "gradient" not in batch_style.lower()
    assert "animation:" not in batch_style.lower()
    assert "@font-face" not in batch_style.lower()


def test_package_scripts_expose_narrow_batch_test_and_hidden_smoke() -> None:
    package = json.loads(read("package.json"))
    assert package["scripts"]["test:batch-observability"] == (
        "node --test batch_observability.test.js"
    )
    assert package["scripts"]["smoke:batch-observability"] == (
        "electron batch_observability_smoke.js"
    )
    assert package["scripts"]["start"] == "electron ."


def test_hidden_probe_checks_actual_noop_runtime_and_two_viewports() -> None:
    probe = read("batch_observability_probe.js")
    smoke = read("batch_observability_smoke.js")
    for check in (
        "actual_plan_only_completed",
        "actual_zero_change_execute_completed",
        "four_verified_noop_visible",
        "backend_dispatch_zero",
        "authority_consumption_zero",
        "journal_prefix_reopened",
        "effect_unknown_blocked",
        "first_viewport_has_required_plan_context",
        "no_horizontal_overflow",
        "no_console_errors",
    ):
        assert f"{check}:" in probe
    assert "captureAt(win, 1280, 720" in probe
    assert "captureAt(win, 1920, 1080" in probe
    assert "read_model_mode" in probe
    assert "NLMYTGEN_AUDIO_POLICY = 'silent'" in smoke
    assert "appendSwitch('mute-audio')" in smoke
