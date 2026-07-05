"""Static read-only dashboard panel for dashboard readiness ingest packages."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from src.pipeline.dashboard_readiness_ingest import REQUIRED_CAPABILITY_IDS, STATUS_CATEGORIES

DEFAULT_OUTPUT_DIRNAME = "gui_dashboard_panel"
DEFAULT_ARTIFACT_ID = "gui_dashboard_panel_ingest_001"

REQUIRED_GUI_PANEL_FILES = (
    "panel_manifest.json",
    "gui_dashboard_adapter.json",
    "panel_data.json",
    "dashboard_panel_preview.html",
    "dashboard_panel_preview.md",
    "dom_or_static_readback.json",
    "review_checklist.md",
    "limitations.md",
    "validation_readback.json",
)

REQUIRED_HTML_MARKERS = (
    'data-dashboard-panel="true"',
    'data-section="capability-grid"',
    'data-section="boundary-status"',
    'data-section="source-artifact-index"',
    'data-status="ready"',
    'data-status="partial"',
    'data-status="sample_fixture_not_real"',
    'data-status="blocked_by_real_input"',
    'data-status="blocked_by_true_gate"',
    'data-status="draft_offline"',
    'data-status="deferred"',
    'data-status="missing"',
    'data-status="unknown"',
)


def build_gui_dashboard_panel_package(
    *,
    package_dir: str | Path,
    ingest_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build a static GUI/dashboard panel package from dashboard ingest data."""
    source_root = Path(package_dir)
    ingest_root = Path(ingest_dir) if ingest_dir else source_root / "dashboard_readiness_ingest"
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)

    repo_root = _find_repo_root(source_root)
    adapter = _adapter_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        ingest_root=ingest_root,
        output_root=output_root,
        repo_root=repo_root,
    )
    panel_data = _panel_data_payload(adapter)
    html_text = _render_html_preview(panel_data)
    markdown_text = _render_markdown_preview(panel_data)
    static_readback = _dom_or_static_readback(
        output_root=output_root,
        html_text=html_text,
        adapter=adapter,
    )
    manifest = _panel_manifest_payload(
        artifact_id=artifact_id,
        source_root=source_root,
        ingest_root=ingest_root,
        output_root=output_root,
        adapter=adapter,
        static_readback=static_readback,
    )

    _write_json(output_root / "panel_manifest.json", manifest)
    _write_json(output_root / "gui_dashboard_adapter.json", adapter)
    _write_json(output_root / "panel_data.json", panel_data)
    _write_text(output_root / "dashboard_panel_preview.html", html_text)
    _write_text(output_root / "dashboard_panel_preview.md", markdown_text)
    _write_json(output_root / "dom_or_static_readback.json", static_readback)
    _write_text(output_root / "review_checklist.md", _render_review_checklist(panel_data))
    _write_text(output_root / "limitations.md", _render_limitations(panel_data))

    readback = validate_gui_dashboard_panel_package(output_root, require_readback=False)
    _write_json(output_root / "validation_readback.json", readback)
    final_readback = validate_gui_dashboard_panel_package(output_root)
    _write_json(output_root / "validation_readback.json", final_readback)
    return final_readback


def validate_gui_dashboard_panel_package(
    output_dir: str | Path,
    *,
    require_readback: bool = True,
) -> dict[str, Any]:
    """Validate generated GUI dashboard panel package and static DOM markers."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_GUI_PANEL_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if name == "validation_readback.json" and not require_readback:
            continue
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    manifest = _load_json_if_present(files["panel_manifest.json"])
    adapter = _load_json_if_present(files["gui_dashboard_adapter.json"])
    panel_data = _load_json_if_present(files["panel_data.json"])
    static_readback = _load_json_if_present(files["dom_or_static_readback.json"])

    json_payloads = {
        "panel_manifest": manifest,
        "gui_dashboard_adapter": adapter,
        "panel_data": panel_data,
        "dom_or_static_readback": static_readback,
    }
    for name, payload in json_payloads.items():
        if not isinstance(payload, dict):
            failed_checks.append(f"{name}_json_invalid")
            json_payloads[name] = {}

    manifest = json_payloads["panel_manifest"]
    adapter = json_payloads["gui_dashboard_adapter"]
    panel_data = json_payloads["panel_data"]
    static_readback = json_payloads["dom_or_static_readback"]

    rows = panel_data.get("capability_rows", [])
    if not isinstance(rows, list):
        rows = []
        failed_checks.append("panel_capability_rows_invalid")
    capability_ids = {row.get("capability_id") for row in rows if isinstance(row, dict)}
    missing_capabilities = [capability for capability in REQUIRED_CAPABILITY_IDS if capability not in capability_ids]
    failed_checks.extend(f"missing_capability:{capability}" for capability in missing_capabilities)

    row_states = {row.get("state") for row in rows if isinstance(row, dict)}
    missing_states = [state for state in _required_visible_states() if state not in row_states]
    failed_checks.extend(f"missing_visible_state:{state}" for state in missing_states)

    boundary_status = panel_data.get("boundary_status", {})
    if boundary_status.get("transcript_status") != "sample_fixture_not_real":
        failed_checks.append("sample_fixture_status_not_visible")
    if boundary_status.get("public_upload_status") != "blocked_by_true_gate":
        failed_checks.append("public_upload_gate_not_closed")
    if boundary_status.get("ymm4_render_status") != "blocked_by_true_gate":
        failed_checks.append("ymm4_render_gate_not_closed")

    html_text = files["dashboard_panel_preview.html"].read_text(encoding="utf-8") if files["dashboard_panel_preview.html"].exists() else ""
    missing_markers = [marker for marker in REQUIRED_HTML_MARKERS if marker not in html_text]
    failed_checks.extend(f"missing_html_marker:{marker}" for marker in missing_markers)
    for state in _required_visible_states():
        if state not in html_text:
            failed_checks.append(f"html_state_text_missing:{state}")
    if "source_artifact_index" not in html_text:
        failed_checks.append("html_source_artifact_index_missing")

    static_checks = static_readback.get("checks", {})
    if static_checks.get("html_references_expected_status_categories") is not True:
        failed_checks.append("static_readback_status_categories_missing")
    if static_checks.get("html_references_source_artifact_index") is not True:
        failed_checks.append("static_readback_source_index_missing")
    if manifest.get("artifact_kind") != "gui-dashboard-panel-ingest":
        failed_checks.append("manifest_artifact_kind_mismatch")
    if adapter.get("source_kind") != "dashboard_readiness_ingest":
        failed_checks.append("adapter_source_kind_mismatch")

    return {
        "schema_version": "gui_dashboard_panel_readback.v1",
        "status": "passed" if not failed_checks else "failed",
        "output_dir": str(root),
        "checked_files": {name: str(path) for name, path in files.items()},
        "checks": {
            "all_required_files_present": all(path.exists() for path in files.values()),
            "json_loads": all(isinstance(payload, dict) and bool(payload) for payload in json_payloads.values()),
            "required_capabilities_present": not missing_capabilities,
            "required_states_visible": not missing_states,
            "html_markers_present": not missing_markers,
            "sample_fixture_visible": boundary_status.get("transcript_status") == "sample_fixture_not_real",
            "public_upload_gate_closed": boundary_status.get("public_upload_status") == "blocked_by_true_gate",
            "ymm4_render_gate_closed": boundary_status.get("ymm4_render_status") == "blocked_by_true_gate",
            "source_artifact_index_visible": "source_artifact_index" in html_text,
        },
        "failed_checks": failed_checks,
        "artifact_id": manifest.get("artifact_id"),
        "source_package_dir": manifest.get("source_package_dir"),
        "ingest_dir": manifest.get("ingest_dir"),
        "selected_candidate_id": panel_data.get("selected_candidate_id"),
        "transcript_status": boundary_status.get("transcript_status"),
        "capability_count": len(rows),
        "primary_machine_readable": str(root / "gui_dashboard_adapter.json"),
        "primary_human_review": str(root / "dashboard_panel_preview.html"),
        "next_action": panel_data.get("next_action"),
    }


def _adapter_payload(
    *,
    artifact_id: str,
    source_root: Path,
    ingest_root: Path,
    output_root: Path,
    repo_root: Path,
) -> dict[str, Any]:
    manifest = _load_json(ingest_root / "dashboard_manifest.json")
    summary = _load_json(ingest_root / "readiness_summary.json")
    pipeline_status = _load_json(ingest_root / "pipeline_status.json")
    glyph_grid = _load_json(ingest_root / "capability_glyph_grid.json")
    visual_panel = _load_json(ingest_root / "symbolic_visual_panel.json")
    source_index = _load_json(ingest_root / "source_artifact_index.json")

    return {
        "schema_version": "gui_dashboard_adapter.v1",
        "artifact_id": artifact_id,
        "source_kind": "dashboard_readiness_ingest",
        "source_package_dir": str(source_root),
        "ingest_dir": str(ingest_root),
        "output_dir": str(output_root),
        "selected_candidate_id": summary.get("selected_candidate_id"),
        "dashboard_manifest": {
            "artifact_id": manifest.get("artifact_id"),
            "artifact_kind": manifest.get("artifact_kind"),
            "repo_relative_path": _relpath(ingest_root / "dashboard_manifest.json", repo_root),
        },
        "readiness_summary_path": _relpath(ingest_root / "readiness_summary.json", repo_root),
        "pipeline_status_path": _relpath(ingest_root / "pipeline_status.json", repo_root),
        "capability_glyph_grid_path": _relpath(ingest_root / "capability_glyph_grid.json", repo_root),
        "symbolic_visual_panel_path": _relpath(ingest_root / "symbolic_visual_panel.json", repo_root),
        "source_artifact_index_path": _relpath(ingest_root / "source_artifact_index.json", repo_root),
        "boundary_status": summary.get("boundary_status", {}),
        "status_groups": summary.get("status_groups", {}),
        "capability_rows": glyph_grid.get("rows", []),
        "visual_bars": visual_panel.get("bars", []),
        "bar_mode": visual_panel.get("bar_mode"),
        "source_artifacts": source_index.get("artifacts", []),
        "source_artifact_counts": source_index.get("artifact_counts", {}),
        "pipeline_route": pipeline_status.get("route", []),
        "roadmap_delta": pipeline_status.get("roadmap_delta", {}),
        "closed_gates": pipeline_status.get("closed_gates", []),
        "next_action": summary.get("next_action"),
        "boundaries": {
            "read_only_panel": True,
            "local_offline_review_only": True,
            "no_live_fetch": True,
            "no_media_download": True,
            "no_youtube_publication": True,
            "no_oauth_or_paid_api": True,
            "no_rights_or_legal_acceptance": True,
            "no_ymm4_gui_launch_or_render": True,
            "no_production_ymmp_generation": True,
            "no_audio_generation": True,
        },
    }


def _panel_data_payload(adapter: dict[str, Any]) -> dict[str, Any]:
    source_next_action = adapter.get("next_action") or ""
    return {
        "schema_version": "gui_dashboard_panel_data.v1",
        "artifact_id": adapter["artifact_id"],
        "selected_candidate_id": adapter.get("selected_candidate_id"),
        "headline_status": _headline_status(adapter),
        "boundary_status": adapter.get("boundary_status", {}),
        "status_groups": adapter.get("status_groups", {}),
        "capability_rows": adapter.get("capability_rows", []),
        "visual_bars": adapter.get("visual_bars", []),
        "bar_mode": adapter.get("bar_mode"),
        "source_artifacts": adapter.get("source_artifacts", []),
        "source_artifact_counts": adapter.get("source_artifact_counts", {}),
        "pipeline_route": adapter.get("pipeline_route", []),
        "roadmap_delta": adapter.get("roadmap_delta", {}),
        "closed_gates": adapter.get("closed_gates", []),
        "next_action": (
            "Open dashboard_panel_preview.html for the one-surface read-only view; "
            f"then {source_next_action[:1].lower()}{source_next_action[1:]}"
            if source_next_action
            else "Open dashboard_panel_preview.html for the one-surface read-only view."
        ),
    }


def _panel_manifest_payload(
    *,
    artifact_id: str,
    source_root: Path,
    ingest_root: Path,
    output_root: Path,
    adapter: dict[str, Any],
    static_readback: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "gui_dashboard_panel_manifest.v1",
        "artifact_id": artifact_id,
        "artifact_kind": "gui-dashboard-panel-ingest",
        "status": "generated",
        "source_package_dir": str(source_root),
        "ingest_dir": str(ingest_root),
        "output_dir": str(output_root),
        "selected_candidate_id": adapter.get("selected_candidate_id"),
        "files": {name: str(output_root / name) for name in REQUIRED_GUI_PANEL_FILES},
        "source_inputs": {
            "dashboard_manifest": str(ingest_root / "dashboard_manifest.json"),
            "readiness_summary": str(ingest_root / "readiness_summary.json"),
            "pipeline_status": str(ingest_root / "pipeline_status.json"),
            "capability_glyph_grid": str(ingest_root / "capability_glyph_grid.json"),
            "symbolic_visual_panel": str(ingest_root / "symbolic_visual_panel.json"),
            "source_artifact_index": str(ingest_root / "source_artifact_index.json"),
        },
        "readback_status": static_readback.get("status"),
        "boundaries": adapter["boundaries"],
    }


def _dom_or_static_readback(*, output_root: Path, html_text: str, adapter: dict[str, Any]) -> dict[str, Any]:
    states = sorted({row.get("state") for row in adapter.get("capability_rows", []) if isinstance(row, dict)})
    required_states = _required_visible_states()
    marker_presence = {marker: marker in html_text for marker in REQUIRED_HTML_MARKERS}
    return {
        "schema_version": "gui_dashboard_static_readback.v1",
        "status": "passed" if all(marker_presence.values()) and all(state in html_text for state in required_states) else "failed",
        "html_path": str(output_root / "dashboard_panel_preview.html"),
        "panel_data_path": str(output_root / "panel_data.json"),
        "adapter_path": str(output_root / "gui_dashboard_adapter.json"),
        "seen_states": states,
        "required_visible_states": required_states,
        "html_markers": marker_presence,
        "checks": {
            "html_references_expected_status_categories": all(state in html_text for state in required_states),
            "html_references_source_artifact_index": "source_artifact_index" in html_text,
            "html_references_sample_fixture": "sample_fixture_not_real" in html_text,
            "html_references_real_input_gate": "blocked_by_real_input" in html_text,
            "html_references_yymm4_render_gate": "ymm4_render_status" in html_text,
            "capability_rows_present": len(adapter.get("capability_rows", [])) >= len(REQUIRED_CAPABILITY_IDS),
        },
    }


def _render_html_preview(panel_data: dict[str, Any]) -> str:
    title = "Yukkuri Newsroom Dashboard Panel"
    rows = panel_data.get("capability_rows", [])
    bars = panel_data.get("visual_bars", [])
    boundary = panel_data.get("boundary_status", {})
    source_counts = panel_data.get("source_artifact_counts", {})
    route = panel_data.get("pipeline_route", [])
    source_artifacts = panel_data.get("source_artifacts", [])

    capability_cards = "\n".join(_capability_card(row) for row in rows if isinstance(row, dict))
    bar_rows = "\n".join(_bar_row(bar) for bar in bars if isinstance(bar, dict))
    boundary_rows = "\n".join(
        f"<tr><th>{_esc(key)}</th><td><span class=\"status-pill\" data-status=\"{_esc(_boundary_state(value))}\">{_esc(value)}</span></td></tr>"
        for key, value in boundary.items()
    )
    route_items = "\n".join(
        f"<li><span>{_esc(item.get('node', 'unknown'))}</span><span class=\"status-pill\" data-status=\"{_esc(item.get('state', 'unknown'))}\">{_esc(item.get('state', 'unknown'))}</span></li>"
        for item in route
        if isinstance(item, dict)
    )
    source_rows = "\n".join(
        "<tr>"
        f"<td>{_esc(item.get('id', 'unknown'))}</td>"
        f"<td><span class=\"status-pill\" data-status=\"{_esc(item.get('state', 'unknown'))}\">{_esc(item.get('state', 'unknown'))}</span></td>"
        f"<td>{_esc(str(item.get('exists')))}</td>"
        f"<td><code>{_esc(item.get('repo_relative_path', ''))}</code></td>"
        "</tr>"
        for item in source_artifacts
        if isinstance(item, dict)
    )
    status_palette = "\n".join(
        f"<span class=\"status-pill\" data-status=\"{_esc(state)}\">{_esc(state)}</span>"
        for state in STATUS_CATEGORIES
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --surface: #ffffff;
      --ink: #172033;
      --muted: #657085;
      --line: #d9e1ea;
      --ready: #0f766e;
      --draft: #6f5f18;
      --sample: #9f4f12;
      --input: #b42318;
      --gate: #7f1d1d;
      --deferred: #475569;
      --missing: #6b7280;
      --unknown: #4b5563;
      --accent: #2563eb;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; min-height: 100%; background: var(--bg); color: var(--ink); font-family: "Segoe UI", "Noto Sans", Arial, sans-serif; }}
    body {{ padding: 24px; }}
    .shell {{ max-width: 1320px; margin: 0 auto; }}
    header {{ display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 16px; align-items: end; margin-bottom: 20px; }}
    h1 {{ margin: 0; font-size: 28px; line-height: 1.15; font-weight: 700; letter-spacing: 0; }}
    h2 {{ margin: 0 0 12px; font-size: 16px; line-height: 1.25; letter-spacing: 0; }}
    p {{ margin: 0; color: var(--muted); line-height: 1.5; }}
    code {{ font-family: Consolas, "SFMono-Regular", monospace; font-size: 12px; overflow-wrap: anywhere; }}
    .topline {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }}
    .summary-strip {{ display: grid; grid-template-columns: repeat(4, minmax(140px, 1fr)); gap: 10px; margin-bottom: 18px; }}
    .metric, .panel, .card {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; }}
    .metric {{ padding: 14px; min-height: 78px; }}
    .metric b {{ display: block; font-size: 20px; margin-top: 6px; }}
    .layout {{ display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(320px, 0.8fr); gap: 16px; }}
    .panel {{ padding: 16px; margin-bottom: 16px; }}
    .capability-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }}
    .card {{ padding: 12px; display: grid; gap: 8px; min-height: 145px; }}
    .card-head {{ display: flex; justify-content: space-between; gap: 8px; align-items: flex-start; }}
    .card-title {{ font-size: 14px; font-weight: 700; line-height: 1.25; }}
    .note {{ font-size: 12px; color: var(--muted); line-height: 1.4; }}
    .path {{ padding-top: 2px; color: var(--muted); }}
    .status-pill {{ display: inline-flex; align-items: center; min-height: 24px; padding: 3px 8px; border-radius: 999px; font-size: 12px; font-weight: 700; border: 1px solid currentColor; background: #fff; }}
    [data-status="ready"] {{ color: var(--ready); }}
    [data-status="draft_offline"] {{ color: var(--draft); }}
    [data-status="sample_fixture_not_real"] {{ color: var(--sample); }}
    [data-status="blocked_by_real_input"] {{ color: var(--input); }}
    [data-status="blocked_by_true_gate"] {{ color: var(--gate); }}
    [data-status="deferred"] {{ color: var(--deferred); }}
    [data-status="missing"] {{ color: var(--missing); }}
    [data-status="partial"], [data-status="unknown"] {{ color: var(--unknown); }}
    .bars {{ display: grid; gap: 8px; }}
    .bar-row {{ display: grid; grid-template-columns: minmax(130px, 190px) minmax(0, 1fr) auto; gap: 10px; align-items: center; font-size: 13px; }}
    .track {{ height: 10px; border-radius: 999px; background: #e5e7eb; overflow: hidden; }}
    .fill {{ display: block; height: 100%; border-radius: inherit; background: var(--accent); }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ text-align: left; padding: 9px 8px; border-top: 1px solid var(--line); vertical-align: top; }}
    th {{ width: 190px; color: var(--muted); font-weight: 700; }}
    ul.route {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }}
    ul.route li {{ display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 9px 0; border-top: 1px solid var(--line); }}
    .legend {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .next {{ border-left: 4px solid var(--accent); padding-left: 12px; }}
    @media (max-width: 980px) {{
      body {{ padding: 14px; }}
      header, .layout {{ grid-template-columns: 1fr; }}
      .summary-strip, .capability-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 640px) {{
      .summary-strip, .capability-grid {{ grid-template-columns: 1fr; }}
      .bar-row {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="shell" data-dashboard-panel="true">
    <header>
      <div>
        <h1>{title}</h1>
        <p>Read-only pilot state for { _esc(panel_data.get("selected_candidate_id", "unknown")) }.</p>
        <div class="topline">{status_palette}</div>
      </div>
      <span class="status-pill" data-status="{_esc(_headline_state(panel_data))}">{_esc(panel_data.get("headline_status", "unknown"))}</span>
    </header>

    <section class="summary-strip" aria-label="dashboard summary">
      <div class="metric"><p>Capabilities</p><b>{len(rows)}</b></div>
      <div class="metric"><p>Source artifacts</p><b>{_esc(source_counts.get("present", 0))}/{_esc(source_counts.get("total", 0))}</b></div>
      <div class="metric"><p>Transcript</p><b>{_esc(boundary.get("transcript_status", "unknown"))}</b></div>
      <div class="metric"><p>Bar mode</p><b>{_esc(panel_data.get("bar_mode", "unknown"))}</b></div>
    </section>

    <section class="layout">
      <div>
        <section class="panel" data-section="capability-grid">
          <h2>Capability Status</h2>
          <div class="capability-grid">{capability_cards}</div>
        </section>

        <section class="panel" data-section="source-artifact-index">
          <h2>Source Artifact Index</h2>
          <table aria-label="source_artifact_index">
            <thead><tr><th>artifact</th><th>state</th><th>exists</th><th>path</th></tr></thead>
            <tbody>{source_rows}</tbody>
          </table>
        </section>
      </div>

      <aside>
        <section class="panel" data-section="visual-bars">
          <h2>Symbolic Bars</h2>
          <div class="bars">{bar_rows}</div>
        </section>

        <section class="panel" data-section="boundary-status">
          <h2>Boundaries</h2>
          <table aria-label="boundary status"><tbody>{boundary_rows}</tbody></table>
        </section>

        <section class="panel" data-section="pipeline-route">
          <h2>Pipeline Route</h2>
          <ul class="route">{route_items}</ul>
        </section>

        <section class="panel next" data-section="next-action">
          <h2>Next Safe Action</h2>
          <p>{_esc(panel_data.get("next_action", ""))}</p>
        </section>
      </aside>
    </section>
  </main>
</body>
</html>
"""


def _render_markdown_preview(panel_data: dict[str, Any]) -> str:
    lines = [
        "# GUI Dashboard Panel Preview",
        "",
        f"- artifact_id: {panel_data['artifact_id']}",
        f"- selected_candidate_id: {panel_data.get('selected_candidate_id')}",
        f"- headline_status: {panel_data.get('headline_status')}",
        f"- transcript_status: {panel_data.get('boundary_status', {}).get('transcript_status')}",
        "",
        "## Capability Status",
        "",
        "| capability | state | path |",
        "|---|---|---|",
    ]
    for row in panel_data.get("capability_rows", []):
        if isinstance(row, dict):
            lines.append(f"| {row.get('capability_id')} | {row.get('state')} | `{row.get('repo_relative_path')}` |")
    lines.extend(["", "## Boundary Status", "", "| boundary | status |", "|---|---|"])
    for key, value in panel_data.get("boundary_status", {}).items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Next Safe Action", "", str(panel_data.get("next_action", "")), ""])
    return "\n".join(lines)


def _render_review_checklist(panel_data: dict[str, Any]) -> str:
    return "\n".join([
        "# GUI Dashboard Panel Review Checklist",
        "",
        "- Open `dashboard_panel_preview.html` locally.",
        "- Confirm every capability row is visible in one surface.",
        "- Confirm `sample_fixture_not_real` is visible for transcript substitution.",
        "- Confirm `blocked_by_real_input` is visible for real transcript input.",
        "- Confirm YMM4 import preview and thumbnail visual proof remain deferred.",
        "- Confirm no public upload, render, rights, legal, payment, or OAuth gate is implied open.",
        "",
        "## Next Safe Action",
        "",
        str(panel_data.get("next_action", "")),
        "",
    ])


def _render_limitations(panel_data: dict[str, Any]) -> str:
    lines = [
        "# GUI Dashboard Panel Limitations",
        "",
        "This is a static read-only panel generated from dashboard readiness ingest data.",
        "",
        "Not performed:",
        "",
    ]
    for item in panel_data.get("closed_gates", []):
        lines.append(f"- {item}")
    lines.extend([
        "- real transcript rerun",
        "- YMM4 GUI launch/import/render",
        "- production .ymmp generation",
        "- thumbnail image generation or visual proof",
        "",
    ])
    return "\n".join(lines)


def _capability_card(row: dict[str, Any]) -> str:
    state = str(row.get("state", "unknown"))
    return (
        f'<article class="card" data-capability="{_esc(row.get("capability_id", "unknown"))}" data-status="{_esc(state)}">'
        '<div class="card-head">'
        f'<div class="card-title">{_esc(row.get("label", row.get("capability_id", "unknown")))}</div>'
        f'<span class="status-pill" data-status="{_esc(state)}">{_esc(state)}</span>'
        "</div>"
        f'<div class="note">{_esc(row.get("note", ""))}</div>'
        f'<div class="path"><code>{_esc(row.get("repo_relative_path", ""))}</code></div>'
        "</article>"
    )


def _bar_row(bar: dict[str, Any]) -> str:
    total = int(bar.get("total_units", 7) or 7)
    done = int(bar.get("done_units", 0) or 0)
    pct = 0 if total <= 0 else max(0, min(100, round(done * 100 / total)))
    state = str(bar.get("state", "unknown"))
    return (
        '<div class="bar-row">'
        f'<span>{_esc(bar.get("label", bar.get("capability_id", "")))}</span>'
        f'<span class="track" aria-label="{pct}%"><span class="fill" style="width:{pct}%"></span></span>'
        f'<span class="status-pill" data-status="{_esc(state)}">{_esc(state)}</span>'
        "</div>"
    )


def _headline_status(adapter: dict[str, Any]) -> str:
    boundary = adapter.get("boundary_status", {})
    if boundary.get("transcript_status") == "sample_fixture_not_real":
        return "sample fixture visible; real input blocked"
    return "local status panel generated"


def _headline_state(panel_data: dict[str, Any]) -> str:
    boundary = panel_data.get("boundary_status", {})
    if boundary.get("transcript_status") == "sample_fixture_not_real":
        return "sample_fixture_not_real"
    return "ready"


def _boundary_state(value: Any) -> str:
    text = str(value)
    if text in STATUS_CATEGORIES:
        return text
    if "blocked" in text:
        return "blocked_by_true_gate"
    if "sample" in text:
        return "sample_fixture_not_real"
    if "draft" in text or "offline" in text:
        return "draft_offline"
    if "deferred" in text:
        return "deferred"
    if "unknown" in text:
        return "unknown"
    return "ready"


def _required_visible_states() -> tuple[str, ...]:
    return (
        "ready",
        "sample_fixture_not_real",
        "draft_offline",
        "blocked_by_real_input",
        "deferred",
    )


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON input must be an object: {path}")
    return data


def _load_json_if_present(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _find_repo_root(path: Path) -> Path:
    resolved = path.resolve()
    for candidate in (resolved, *resolved.parents):
        if (candidate / "pyproject.toml").exists() or (candidate / "AGENTS.md").exists():
            return candidate
    return Path.cwd()


def _relpath(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
