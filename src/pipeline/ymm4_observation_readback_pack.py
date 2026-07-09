"""YMM4 observation readback package for episode 002."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.pipeline.split_view_decision_evidence_prototype import (
    _dict,
    _escape,
    _external_refs_in_files,
    _find_repo_root,
    _forbidden_true_claims,
    _list,
    _load_json_if_present,
    _relpath,
    _temporary_copy_hits,
    _write_json,
    _write_text,
)

DEFAULT_OUTPUT_DIRNAME = "ymm4_observation_readback_pack"
DEFAULT_ARTIFACT_ID = "episode_002_ymm4_observation_readback_pack_v1"
EPISODE_ID = "yukkuri_newsroom_content_spine_002"

YMM4_IMPORT_READY_DIRNAME = "ymm4_import_ready_pack"
REAL_INPUT_PREP_DIRNAME = "real_input_replacement_readiness_pack"

REQUIRED_YMM4_OBSERVATION_FILES = (
    "observation_readback.json",
    "observation_preview.html",
    "manual_ymm4_observation_readback.md",
    "source_artifact_index.json",
    "README_YMM4_OBSERVATION_READBACK.md",
    "limitations.md",
)

CLOSED_GATE_FLAGS = (
    "rendered_video_created",
    "ymmp_file_created",
    "production_ymmp_written",
    "real_input_replaced",
    "rights_approved",
    "public_ready",
    "final_thumbnail_approval",
    "youtube_uploaded",
    "live_fetch_performed",
    "external_media_downloaded",
)


def build_ymm4_observation_readback_pack(
    *,
    package_dir: str | Path,
    output_dir: str | Path | None = None,
    artifact_id: str = DEFAULT_ARTIFACT_ID,
) -> dict[str, Any]:
    """Build an observation-only YMM4 readback package."""
    source_root = Path(package_dir)
    output_root = Path(output_dir) if output_dir else source_root / DEFAULT_OUTPUT_DIRNAME
    output_root.mkdir(parents=True, exist_ok=True)
    repo_root = _find_repo_root(source_root)

    paths = _input_paths(source_root)
    payloads = _load_payloads(paths)
    state = _state(
        artifact_id=artifact_id,
        source_root=source_root,
        output_root=output_root,
        repo_root=repo_root,
        paths=paths,
        payloads=payloads,
    )
    readback = _observation_readback(state, output_root, repo_root)
    source_index = _source_artifact_index(state)

    _write_json(output_root / "observation_readback.json", readback)
    _write_json(output_root / "source_artifact_index.json", source_index)
    _write_text(output_root / "observation_preview.html", _render_html(state, readback))
    _write_text(output_root / "manual_ymm4_observation_readback.md", _render_manual_readback(state, readback))
    _write_text(output_root / "README_YMM4_OBSERVATION_READBACK.md", _render_readme(state, readback))
    _write_text(output_root / "limitations.md", _render_limitations())

    return validate_ymm4_observation_readback_pack(output_root)


def validate_ymm4_observation_readback_pack(output_dir: str | Path) -> dict[str, Any]:
    """Validate the YMM4 observation readback package."""
    root = Path(output_dir)
    files = {name: root / name for name in REQUIRED_YMM4_OBSERVATION_FILES}
    failed_checks: list[str] = []

    for name, path in files.items():
        if not path.exists():
            failed_checks.append(f"missing_file:{name}")

    readback = _load_json_if_present(files["observation_readback.json"])
    source_index = _load_json_if_present(files["source_artifact_index.json"])
    if not isinstance(readback, dict):
        failed_checks.append("observation_readback_json_invalid")
        readback = {}
    if not isinstance(source_index, dict):
        failed_checks.append("source_index_json_invalid")
        source_index = {}

    readback = _dict(readback)
    source_index = _dict(source_index)
    html_text = files["observation_preview.html"].read_text(encoding="utf-8") if files["observation_preview.html"].exists() else ""
    manual_text = files["manual_ymm4_observation_readback.md"].read_text(encoding="utf-8") if files["manual_ymm4_observation_readback.md"].exists() else ""
    limitations_text = files["limitations.md"].read_text(encoding="utf-8") if files["limitations.md"].exists() else ""
    closed_gates = _dict(readback.get("closed_gate_flags"))
    manual_check_count = _numbered_check_count(manual_text)

    if readback.get("schema_version") != "ymm4_observation_readback.v1":
        failed_checks.append("readback_schema_version_mismatch")
    if readback.get("status") not in {"passed", "blocked", "partial"}:
        failed_checks.append("readback_status_invalid")
    if readback.get("status") == "passed" and readback.get("actual_ymm4_imported") is not True:
        failed_checks.append("passed_without_actual_import")
    if readback.get("artifact_id") != DEFAULT_ARTIFACT_ID:
        failed_checks.append("artifact_id_mismatch")
    if readback.get("episode_id") != EPISODE_ID:
        failed_checks.append("episode_id_mismatch")
    if readback.get("observation_mode") not in {"actual_ymm4_gui_observation", "operator_instruction_only", "blocked"}:
        failed_checks.append("observation_mode_invalid")
    if readback.get("observation_mode") == "operator_instruction_only":
        if readback.get("actual_ymm4_import_attempted") is not False:
            failed_checks.append("operator_instruction_attempted_import")
        if readback.get("actual_ymm4_imported") is not False:
            failed_checks.append("operator_instruction_imported_true")
        if readback.get("cue_count_observed") != 0:
            failed_checks.append("operator_instruction_observed_cues_not_zero")
    for flag in CLOSED_GATE_FLAGS:
        if readback.get(flag) is not False:
            failed_checks.append(f"gate_not_false:{flag}")
        if closed_gates.get(flag) is not False:
            failed_checks.append(f"closed_gate_not_false:{flag}")
    if readback.get("cue_count_expected") != 9:
        failed_checks.append("cue_count_expected_mismatch")
    if readback.get("scene_count_expected") != 3:
        failed_checks.append("scene_count_expected_mismatch")
    if readback.get("next_gate") not in {"manual_ymm4_import_observation_return", "adapter_correction_after_observation", "render_proof_after_observation"}:
        failed_checks.append("next_gate_invalid")
    if source_index.get("ymm4_import_ready_pack_read_only") is not True:
        failed_checks.append("ymm4_import_ready_pack_not_read_only")
    if source_index.get("real_input_prep_pack_read_only") is not True:
        failed_checks.append("real_input_prep_pack_not_read_only")
    if '<html lang="ja"' not in html_text:
        failed_checks.append("html_not_japanese_lang")
    for marker in (
        'data-ymm4-observation-readback="true"',
        'data-region="pipeline-runway"',
        'data-region="observation-matrix"',
        'data-region="closed-gates"',
        'data-region="next-decision"',
    ):
        if marker not in html_text:
            failed_checks.append(f"html_marker_missing:{marker}")
    if "card-grid" in html_text or 'data-region="card-grid"' in html_text:
        failed_checks.append("html_card_grid_marker_found")
    if "実観測は未実行" not in html_text and readback.get("observation_mode") == "operator_instruction_only":
        failed_checks.append("html_blocked_copy_missing")
    if manual_check_count > 5:
        failed_checks.append("manual_checks_too_many")
    if manual_check_count < 1:
        failed_checks.append("manual_checks_missing")
    if "Do not render/export" not in manual_text:
        failed_checks.append("manual_missing_render_stop")
    if "Do not launch render/export" not in limitations_text:
        failed_checks.append("limitations_render_stop_missing")

    visible_files = [path for path in files.values() if path.exists()]
    external_refs = _external_refs_in_files(visible_files)
    forbidden_claims = _forbidden_true_claims(root)
    temporary_hits = _temporary_copy_hits(visible_files)
    failed_checks.extend(f"external_ref:{hit}" for hit in external_refs)
    failed_checks.extend(f"forbidden_true_claim:{hit}" for hit in forbidden_claims)
    failed_checks.extend(f"temporary_copy:{hit}" for hit in temporary_hits)

    validation_status = "passed" if not failed_checks else "failed"
    readback["validation_status"] = validation_status
    readback["failed_checks"] = failed_checks
    readback["checks"] = {
        "all_required_files_present": all(path.exists() for path in files.values()),
        "json_loads": isinstance(readback, dict) and isinstance(source_index, dict),
        "html_preview_exists": files["observation_preview.html"].exists(),
        "manual_readback_exists": files["manual_ymm4_observation_readback.md"].exists(),
        "japanese_first_surface": '<html lang="ja"' in html_text,
        "primary_card_grid_absent": "card-grid" not in html_text,
        "operator_instruction_check_count": manual_check_count,
        "closed_gate_flags": closed_gates,
        "external_dependency_status": "none_found" if not external_refs else external_refs,
        "forbidden_true_claims_absent": not forbidden_claims,
        "temporary_copy_absent": not temporary_hits,
    }
    readback["primary_review_file"] = str(root / "observation_preview.html")
    readback["primary_human_review"] = str(root / "observation_preview.html")
    readback["primary_machine_readable"] = str(root / "observation_readback.json")
    readback["launcher_or_open_command"] = f'Invoke-Item -LiteralPath "{(root / "observation_preview.html").resolve()}"'
    readback["access_state"] = "verified_present" if (root / "observation_preview.html").exists() else "missing"
    _write_json(root / "observation_readback.json", readback)
    return readback


def _input_paths(source_root: Path) -> dict[str, Path]:
    import_root = source_root / YMM4_IMPORT_READY_DIRNAME
    real_input_root = source_root / REAL_INPUT_PREP_DIRNAME
    return {
        "ymm4_import_ready_root": import_root,
        "ymm4_import_ready_validation": import_root / "validation_readback.json",
        "ymm4_import_ready_manifest": import_root / "ymm4_import_ready_manifest.json",
        "ymm4_cue_map": import_root / "edit_slice_to_ymm4_cue_map.json",
        "ymm4_manual_sheet": import_root / "manual_ymm4_import_observation_sheet.md",
        "real_input_prep_root": real_input_root,
        "real_input_prep_validation": real_input_root / "validation_readback.json",
        "real_input_prep_contract": real_input_root / "real_input_replacement_contract.md",
        "ir_bridge_csv": source_root / "ir_bridge" / "draft_yymm4.csv",
        "regenerated_csv": source_root / "transcript_substitution_readiness" / "regenerated_draft_yymm4.csv",
        "preview_csv": source_root / "ymm4_import_preview_pack" / "draft_yymm4_preview.csv",
    }


def _load_payloads(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "ymm4_import_ready_validation": _load_json_if_present(paths["ymm4_import_ready_validation"]),
        "ymm4_import_ready_manifest": _load_json_if_present(paths["ymm4_import_ready_manifest"]),
        "ymm4_cue_map": _load_json_if_present(paths["ymm4_cue_map"]),
        "real_input_prep_validation": _load_json_if_present(paths["real_input_prep_validation"]),
    }


def _state(
    *,
    artifact_id: str,
    source_root: Path,
    output_root: Path,
    repo_root: Path,
    paths: dict[str, Path],
    payloads: dict[str, Any],
) -> dict[str, Any]:
    cue_map = _dict(payloads.get("ymm4_cue_map"))
    import_validation = _dict(payloads.get("ymm4_import_ready_validation"))
    real_input_validation = _dict(payloads.get("real_input_prep_validation"))
    detected = _detect_yymm4()
    csv_candidates = _csv_candidates(paths, cue_map, repo_root)
    return {
        "schema_version": "ymm4_observation_state.v1",
        "artifact_id": artifact_id,
        "episode_id": EPISODE_ID,
        "source_package_dir": _relpath(source_root, repo_root),
        "output_dir": _relpath(output_root, repo_root),
        "paths": {name: _relpath(path, repo_root) for name, path in paths.items()},
        "source_import_ready_pack_reference": _relpath(paths["ymm4_import_ready_root"], repo_root),
        "source_real_input_prep_reference": _relpath(paths["real_input_prep_root"], repo_root),
        "cue_count_expected": cue_map.get("cue_count") or import_validation.get("cue_count") or 0,
        "scene_count_expected": cue_map.get("scene_count") or import_validation.get("scene_count") or 0,
        "queue_count": import_validation.get("queue_count"),
        "real_input_prep_status": real_input_validation.get("status"),
        "csv_candidates": csv_candidates,
        "primary_import_csv": csv_candidates[0]["repo_relative_path"] if csv_candidates else "",
        "yymm4_environment": detected,
        "blocker": _observation_blocker(detected),
        "next_gate": "manual_ymm4_import_observation_return",
    }


def _observation_readback(state: dict[str, Any], output_root: Path, repo_root: Path) -> dict[str, Any]:
    closed_gates = {flag: False for flag in CLOSED_GATE_FLAGS}
    blocker = _dict(state.get("blocker"))
    return {
        "schema_version": "ymm4_observation_readback.v1",
        "status": "blocked",
        "artifact_id": DEFAULT_ARTIFACT_ID,
        "episode_id": EPISODE_ID,
        "source_import_ready_pack_reference": state.get("source_import_ready_pack_reference"),
        "source_real_input_prep_reference": state.get("source_real_input_prep_reference"),
        "observation_mode": "operator_instruction_only",
        "actual_ymm4_import_attempted": False,
        "actual_ymm4_imported": False,
        "observed_at": "not_observed_2026-07-09_JST",
        "observed_by_environment": state.get("yymm4_environment"),
        "cue_count_expected": state.get("cue_count_expected"),
        "cue_count_observed": 0,
        "scene_count_expected": state.get("scene_count_expected"),
        "voice_item_observed": "not_observed",
        "subtitle_item_observed": "not_observed",
        "timing_order_observed": "not_observed",
        "placeholder_boundary_observed": "not_observed",
        "import_errors": [],
        "deviations": [
            {
                "deviation_id": "actual_gui_observation_not_performed",
                "severity": "blocking_for_observation_pass",
                "detail": blocker.get("reason"),
            }
        ],
        "blocker": blocker,
        "expected_import_path": state.get("primary_import_csv"),
        "importable_csv_candidates": state.get("csv_candidates"),
        "screenshot_or_visual_evidence_paths": [],
        "rendered_video_created": False,
        "ymmp_file_created": False,
        "production_ymmp_written": False,
        "real_input_replaced": False,
        "rights_approved": False,
        "public_ready": False,
        "final_thumbnail_approval": False,
        "youtube_uploaded": False,
        "live_fetch_performed": False,
        "external_media_downloaded": False,
        "closed_gate_flags": closed_gates,
        "next_gate": state.get("next_gate"),
        "output_dir": _relpath(output_root, repo_root),
    }


def _source_artifact_index(state: dict[str, Any]) -> dict[str, Any]:
    paths = _dict(state.get("paths"))
    records = [
        _source_record("ymm4_import_ready_validation", paths.get("ymm4_import_ready_validation"), "import_ready_readback", True),
        _source_record("ymm4_import_ready_manifest", paths.get("ymm4_import_ready_manifest"), "import_ready_manifest", True),
        _source_record("ymm4_cue_map", paths.get("ymm4_cue_map"), "cue_map_expected_observation", True),
        _source_record("ymm4_manual_sheet", paths.get("ymm4_manual_sheet"), "prior_operator_sheet", True),
        _source_record("real_input_prep_validation", paths.get("real_input_prep_validation"), "real_input_gate_readback", True),
        _source_record("real_input_prep_contract", paths.get("real_input_prep_contract"), "real_input_gate_contract", True),
    ]
    return {
        "schema_version": "ymm4_observation_source_artifact_index.v1",
        "artifact_id": state.get("artifact_id"),
        "ymm4_import_ready_pack_read_only": True,
        "real_input_prep_pack_read_only": True,
        "records": records,
    }


def _source_record(record_id: str, path: Any, role: str, exists_expected: bool) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "repo_relative_path": str(path or ""),
        "role": role,
        "exists_expected": exists_expected,
        "display_zone": "source_artifact_index",
    }


def _render_html(state: dict[str, Any], readback: dict[str, Any]) -> str:
    runway_steps = [
        ("準備済み", "import-ready pack", "3 scenes / 9 cues の観測対象は定義済み。"),
        ("今回の判定", "operator_instruction_only", "YMM4実行ファイルは検出したが、GUI importを安全に操作・視認できる経路がない。"),
        ("返却待ち", "manual observation", "operatorがYMM4上でimport結果を確認し、5点だけ返す。"),
        ("次判断", str(readback.get("next_gate")), "観測結果によりadapter correction、real input receipt、render proof待ちを分岐する。"),
    ]
    runway = "\n".join(_render_runway_step(index, *step) for index, step in enumerate(runway_steps, start=1))
    status_rows = "\n".join(
        _render_status_row(label, value)
        for label, value in (
            ("observation_mode", readback.get("observation_mode")),
            ("actual_ymm4_import_attempted", readback.get("actual_ymm4_import_attempted")),
            ("actual_ymm4_imported", readback.get("actual_ymm4_imported")),
            ("cue_count_expected", readback.get("cue_count_expected")),
            ("cue_count_observed", readback.get("cue_count_observed")),
            ("voice_item_observed", readback.get("voice_item_observed")),
            ("subtitle_item_observed", readback.get("subtitle_item_observed")),
            ("timing_order_observed", readback.get("timing_order_observed")),
            ("placeholder_boundary_observed", readback.get("placeholder_boundary_observed")),
        )
    )
    gate_rows = "\n".join(_render_gate_row(flag, value) for flag, value in _dict(readback.get("closed_gate_flags")).items())
    env = _dict(readback.get("observed_by_environment"))
    blocker = _dict(readback.get("blocker"))
    csv_rows = "\n".join(_render_csv_row(row) for row in _list(readback.get("importable_csv_candidates")))
    return f"""<!doctype html>
<html lang="ja" data-ymm4-observation-readback="true" data-artifact-kind="episode-ymm4-observation-readback-pack">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Episode 002 YMM4観測readback</title>
  <style>
    :root {{
      color-scheme: dark light;
      --bg: #101413;
      --surface: #18211f;
      --panel: #202b28;
      --ink: #f0f7f4;
      --muted: #a9bbb3;
      --line: #34463f;
      --accent: #7dd7c2;
      --warn: #f1cc75;
      --stop: #f0a0a0;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; background: var(--bg); color: var(--ink); line-height: 1.5; }}
    main {{ max-width: 1240px; margin: 0 auto; padding: 28px 18px 44px; }}
    h1, h2 {{ margin: 0; letter-spacing: 0; }}
    h1 {{ font-size: clamp(28px, 4vw, 42px); line-height: 1.08; }}
    h2 {{ font-size: 20px; margin: 30px 0 12px; }}
    p {{ color: var(--muted); margin: 0; }}
    code {{ color: var(--warn); }}
    .hero {{ display: grid; gap: 14px; padding-bottom: 18px; border-bottom: 1px solid var(--line); }}
    .metrics {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .metric {{ border: 1px solid var(--line); border-radius: 999px; padding: 5px 10px; background: var(--surface); font-size: 12px; }}
    .runway {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; }}
    .step {{ border-top: 4px solid var(--accent); background: var(--surface); padding: 10px; min-height: 118px; }}
    .step strong {{ display: block; color: var(--warn); margin-bottom: 6px; }}
    .matrix {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
    th, td {{ border: 1px solid var(--line); padding: 9px; vertical-align: top; overflow-wrap: anywhere; }}
    th {{ color: var(--warn); background: var(--panel); text-align: left; }}
    td {{ background: var(--surface); }}
    .band {{ border: 1px solid var(--line); background: var(--surface); padding: 12px; }}
    .ok {{ color: var(--accent); }}
    .hold {{ color: var(--stop); }}
    @media (prefers-color-scheme: light) {{
      :root {{ --bg: #f7faf8; --surface: #ffffff; --panel: #edf5f1; --ink: #17211e; --muted: #516258; --line: #c8d9d1; }}
    }}
    @media (max-width: 860px) {{
      main {{ padding: 20px 12px 34px; }}
      .runway {{ grid-template-columns: 1fr; }}
      .matrix {{ display: block; overflow-x: auto; white-space: normal; }}
      th, td {{ min-width: 180px; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div class="metrics">
        <span class="metric">status: {_escape(readback.get("status"))}</span>
        <span class="metric">mode: {_escape(readback.get("observation_mode"))}</span>
        <span class="metric">expected cues: {_escape(readback.get("cue_count_expected"))}</span>
        <span class="metric">observed cues: {_escape(readback.get("cue_count_observed"))}</span>
      </div>
      <h1>Episode 002 YMM4観測readback</h1>
      <p>実観測は未実行。YMM4 executable は検出済みだが、GUI importをこのworkerが安全に操作・視認する経路がないため、operator instructionとして保持する。</p>
    </section>

    <section data-region="pipeline-runway">
      <h2>pipeline runway</h2>
      <div class="runway">{runway}</div>
    </section>

    <section data-region="observation-matrix">
      <h2>観測matrix / result or blocker</h2>
      <table class="matrix">
        <thead><tr><th>項目</th><th>readback</th></tr></thead>
        <tbody>{status_rows}</tbody>
      </table>
    </section>

    <section data-region="expected-import-path">
      <h2>expected import path</h2>
      <div class="band">
        <p>YMM4: <code>{_escape(env.get("yymm4_executable_path"))}</code></p>
        <p>CSV: <code>{_escape(readback.get("expected_import_path"))}</code></p>
        <p>blocker: <span class="hold">{_escape(blocker.get("reason"))}</span></p>
      </div>
      <table class="matrix">
        <thead><tr><th>candidate</th><th>exists</th><th>role</th></tr></thead>
        <tbody>{csv_rows}</tbody>
      </table>
    </section>

    <section data-region="untested">
      <h2>未検証のまま残る項目</h2>
      <div class="band">
        <p>VoiceItem、subtitle、timing order、placeholder boundary、visual evidence は actual GUI importが未実行のため未観測。</p>
      </div>
    </section>

    <section data-region="closed-gates">
      <h2>閉じたgate</h2>
      <table class="matrix">
        <thead><tr><th>gate key</th><th>値</th><th>意味</th></tr></thead>
        <tbody>{gate_rows}</tbody>
      </table>
    </section>

    <section data-region="next-decision">
      <h2>次の判断</h2>
      <div class="band">
        <p><code>{_escape(readback.get("next_gate"))}</code>: operatorが5点の観測結果を返した後、adapter correction / real input receipt / later render proof のどれに進むかを決める。</p>
      </div>
    </section>
  </main>
</body>
</html>
"""


def _render_runway_step(index: int, label: str, status: str, note: str) -> str:
    return f"""<div class="step">
  <strong>{index}. {_escape(label)}</strong>
  <code>{_escape(status)}</code>
  <p>{_escape(note)}</p>
</div>"""


def _render_status_row(label: str, value: Any) -> str:
    return f"""<tr>
  <td><code>{_escape(label)}</code></td>
  <td>{_escape(value)}</td>
</tr>"""


def _render_gate_row(flag: str, value: Any) -> str:
    return f"""<tr>
  <td><code>{_escape(flag)}</code></td>
  <td><code>{_escape(value)}</code></td>
  <td><span class="ok">false = 未実行 / このpackageでは閉じたまま</span></td>
</tr>"""


def _render_csv_row(row: Any) -> str:
    item = _dict(row)
    return f"""<tr>
  <td><code>{_escape(item.get("repo_relative_path"))}</code></td>
  <td>{_escape(item.get("exists"))}</td>
  <td>{_escape(item.get("role"))}</td>
</tr>"""


def _render_manual_readback(state: dict[str, Any], readback: dict[str, Any]) -> str:
    env = _dict(readback.get("observed_by_environment"))
    blocker = _dict(readback.get("blocker"))
    return f"""# Episode 002 YMM4観測readback

状態: `operator_instruction_only`

実観測は未実行。YMM4 executable は検出されたが、このworkerからGUI import結果を安全に操作・視認する経路がないため、観測passは付けない。

YMM4 executable:
`{env.get("yymm4_executable_path")}`

開くもの:
`{state.get("source_import_ready_pack_reference")}/ymm4_import_ready_preview.html`

import候補CSV:
`{readback.get("expected_import_path")}`

blocker:
{blocker.get("reason")}

## operatorが返す観測5点

1. CSV import後、cue順がS1 -> S2 -> S3、csv_row_1 -> csv_row_9として読めるか。
2. VoiceItemが9 cue分に見えるか、欠落・重複・順序入れ替わりがあるか。
3. subtitle/textがspeakerとcueに対応し、sample/diagnostic textであることが誤解なく見えるか。
4. timing orderは仮timingの流れを崩していないか。
5. visual/overlay/citation/thumbnail要素がplaceholder境界として読め、final素材やpublic-readyを示していないか。

Do not render/export. Do not save or write production `.ymmp`. Do not replace real input. Do not approve rights/public/final thumbnail. Do not upload.
"""


def _render_readme(state: dict[str, Any], readback: dict[str, Any]) -> str:
    return f"""# Episode 002 YMM4観測readback pack

Primary review: `observation_preview.html`
Machine readback: `observation_readback.json`
Manual operator sheet: `manual_ymm4_observation_readback.md`

This package records the current observation-only state. Actual GUI import was
not performed, so `status=blocked` and `observation_mode=operator_instruction_only`.

- source import-ready pack: `{readback.get("source_import_ready_pack_reference")}`
- source real-input prep pack: `{readback.get("source_real_input_prep_reference")}`
- expected cue count: `{readback.get("cue_count_expected")}`
- observed cue count: `{readback.get("cue_count_observed")}`
- next gate: `{readback.get("next_gate")}`

No render/export, production `.ymmp`, real input replacement, rights/public
approval, thumbnail approval, upload, live fetch, or external media download
occurred.
"""


def _render_limitations() -> str:
    return """# Limitations

Do not launch render/export from this package.
Do not write or save a production `.ymmp` file.
Do not replace sample placeholders with real input.
Do not approve rights, legal status, public readiness, final thumbnail, or upload.
Do not live fetch, scrape, download external media, use OAuth/API keys, or perform payment work.

Actual observed means actual GUI/manual observation occurred. This package is
blocked/operator-instruction-only until that evidence is returned.
"""


def _detect_yymm4() -> dict[str, Any]:
    home = Path.home()
    shortcut = home / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "YukkuriMovieMaker.lnk"
    candidates = [
        home / "Downloads" / "YukkuriMovieMaker_v4" / "YukkuriMovieMaker.exe",
        home / "AppData" / "Local" / "YukkuriMovieMaker" / "YukkuriMovieMaker.exe",
    ]
    executable = next((path for path in candidates if path.exists()), None)
    status = "executable_detected_but_gui_observation_not_attempted" if executable else "not_detected"
    if executable is None and shortcut.exists():
        status = "start_menu_shortcut_detected_but_target_not_resolved"
    return {
        "terminal_or_device": "Planner007",
        "yymm4_availability_status": status,
        "yymm4_executable_detected": executable is not None,
        "yymm4_executable_path": str(executable) if executable else "",
        "start_menu_shortcut_detected": shortcut.exists(),
        "start_menu_shortcut_path": str(shortcut) if shortcut.exists() else "",
        "launch_attempted": False,
        "gui_observation_channel_available": False,
    }


def _observation_blocker(detected: dict[str, Any]) -> dict[str, Any]:
    if detected.get("yymm4_executable_detected"):
        reason = (
            "YMM4 executable was detected locally, but this worker has no safe "
            "manual/GUI visual readback channel for importing and inspecting the project."
        )
    else:
        reason = "YMM4 executable was not detected in the checked local paths."
    return {
        "blocker_id": "manual_gui_observation_required",
        "status": "blocked_for_actual_observation",
        "reason": reason,
        "operator_action": "Open YMM4 manually, import the CSV candidate, inspect cue/voice/subtitle/timing/placeholder boundaries, and return the five observations.",
    }


def _csv_candidates(paths: dict[str, Path], cue_map: dict[str, Any], repo_root: Path) -> list[dict[str, Any]]:
    candidates: list[Path] = []
    for cue in _list(cue_map.get("cues")):
        source = _dict(cue).get("voice_or_subtitle_action", {})
        expected = _dict(source).get("expected_subtitle_source")
        if isinstance(expected, str) and expected:
            candidates.append(repo_root / expected.split("#", 1)[0])
    for key in ("regenerated_csv", "ir_bridge_csv", "preview_csv"):
        candidates.append(paths[key])

    seen: set[str] = set()
    rows: list[dict[str, Any]] = []
    for path in candidates:
        resolved = path.resolve()
        marker = str(resolved).lower()
        if marker in seen:
            continue
        seen.add(marker)
        rows.append(
            {
                "repo_relative_path": _relpath(path, repo_root),
                "exists": path.exists(),
                "role": "primary_import_candidate" if not rows else "alternate_import_candidate",
            }
        )
    return rows


def _numbered_check_count(text: str) -> int:
    prefixes = tuple(f"{index}." for index in range(1, 10))
    return sum(1 for line in text.splitlines() if line.strip().startswith(prefixes))
