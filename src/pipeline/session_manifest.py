"""Production session manifest / handoff sheet builder.

制作セッションで散らばりやすい CSV / 診断 / IR / apply-production / thumbnail
artifact を 1 つの読み取り用 manifest に束ねる。YMM4 操作や画像生成は行わない。
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

MANIFEST_VERSION = "0.1"

PATH_KEYS = (
    "source_script",
    "csv",
    "script_diagnostics",
    "production_ymmp",
    "ir_json",
    "validate_result",
    "apply_result",
    "patched_ymmp",
    "thumbnail_design",
    "thumbnail_output",
)


def build_session_manifest(
    *,
    video_id: str,
    paths: dict[str, str | None],
) -> dict[str, Any]:
    """Build a machine-readable production session manifest."""
    normalized_paths = {key: _path_record(paths.get(key)) for key in PATH_KEYS}
    validate_payload = _load_json_if_present(paths.get("validate_result"))
    apply_payload = _load_json_if_present(paths.get("apply_result"))
    diagnostics_payload = _load_json_if_present(paths.get("script_diagnostics"))

    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "video_id": video_id,
        "paths": normalized_paths,
        "csv": _summarize_csv(paths.get("csv")),
        "script_diagnostics": _summarize_script_diagnostics(diagnostics_payload),
        "ir_validation": _summarize_ir_validation(validate_payload),
        "apply_production": _summarize_apply_production(apply_payload, paths.get("patched_ymmp")),
        "manual_acceptance": _manual_acceptance_placeholders(),
        "next_action": "",
    }
    manifest["next_action"] = _derive_next_action(manifest)
    return manifest


def render_session_manifest_markdown(manifest: dict[str, Any]) -> str:
    """Render a concise operator handoff sheet."""
    lines: list[str] = [
        f"# Production Session Manifest — {manifest.get('video_id') or 'unknown'}",
        "",
        f"- manifest_version: {manifest.get('manifest_version', MANIFEST_VERSION)}",
        f"- next_action: {manifest.get('next_action', '')}",
        "",
        "## Paths",
        "",
        "| Artifact | Status | Path |",
        "|---|---|---|",
    ]

    for key in PATH_KEYS:
        record = manifest.get("paths", {}).get(key, {})
        lines.append(
            f"| `{key}` | {record.get('status', 'not_recorded')} | "
            f"{_md_value(record.get('path'))} |"
        )

    csv_summary = manifest.get("csv", {})
    diag = manifest.get("script_diagnostics", {})
    validation = manifest.get("ir_validation", {})
    apply = manifest.get("apply_production", {})
    lines.extend([
        "",
        "## Stage Summary",
        "",
        "| Stage | Status | Summary |",
        "|---|---|---|",
        (
            f"| CSV | {csv_summary.get('status')} | "
            f"rows={csv_summary.get('row_count', '-')}, "
            f"speakers={csv_summary.get('speaker_count', '-')} |"
        ),
        (
            f"| Script diagnostics | {diag.get('status')} | "
            f"errors={diag.get('error_count', '-')}, "
            f"warnings={diag.get('warning_count', '-')}, "
            f"codes={', '.join(diag.get('codes', [])) or '-'} |"
        ),
        (
            f"| IR validation | {validation.get('status')} | "
            f"success={validation.get('success', '-')}, "
            f"errors={validation.get('error_count', '-')}, "
            f"warnings={validation.get('warning_count', '-')} |"
        ),
        (
            f"| Apply production | {apply.get('status')} | "
            f"success={apply.get('success', '-')}, "
            f"dry_run={apply.get('dry_run', '-')}, "
            f"output={_md_value(apply.get('output'))} |"
        ),
        "",
        "## Manual Acceptance",
        "",
        "| Check | Status | Note |",
        "|---|---|---|",
    ])

    for key, record in manifest.get("manual_acceptance", {}).items():
        lines.append(
            f"| `{key}` | {record.get('status', 'manual_pending')} | "
            f"{record.get('note', '')} |"
        )

    lines.append("")
    return "\n".join(lines)


def emit_session_manifest_text(manifest: dict[str, Any], fmt: str) -> str:
    if fmt == "json":
        return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if fmt == "markdown":
        return render_session_manifest_markdown(manifest)
    raise ValueError(f"Unsupported session manifest format: {fmt}")


def _path_record(raw_path: str | None) -> dict[str, Any]:
    if not raw_path:
        return {"status": "not_recorded", "path": None, "exists": None}
    path = Path(raw_path)
    return {
        "status": "recorded" if path.exists() else "missing",
        "path": str(path),
        "exists": path.exists(),
    }


def _load_json_if_present(raw_path: str | None) -> dict[str, Any] | None:
    if not raw_path:
        return None
    path = Path(raw_path)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"Session manifest JSON input must be an object: {path}")
    return data


def _summarize_csv(raw_path: str | None) -> dict[str, Any]:
    base = {
        "status": "not_recorded",
        "row_count": 0,
        "speaker_count": 0,
        "speaker_rows": [],
        "build_options": "not_recorded",
        "stats_summary": "not_recorded",
    }
    if not raw_path:
        return base
    path = Path(raw_path)
    if not path.exists():
        base["status"] = "missing"
        return base

    speaker_counts: Counter[str] = Counter()
    row_count = 0
    with path.open(encoding="utf-8-sig", newline="") as file:
        for row in csv.reader(file):
            if not row:
                continue
            row_count += 1
            speaker = row[0] if row else ""
            if speaker:
                speaker_counts[speaker] += 1

    rows = [
        {"speaker": speaker, "utterances": count}
        for speaker, count in sorted(speaker_counts.items())
    ]
    return {
        **base,
        "status": "recorded",
        "row_count": row_count,
        "speaker_count": len(speaker_counts),
        "speaker_rows": rows,
        "stats_summary": {
            "total_utterances": row_count,
            "speakers": rows,
        },
    }


def _summarize_script_diagnostics(payload: dict[str, Any] | None) -> dict[str, Any]:
    if payload is None:
        return {
            "status": "not_recorded",
            "error_count": 0,
            "warning_count": 0,
            "codes": [],
        }

    diagnostics = payload.get("diagnostics", [])
    if not isinstance(diagnostics, list):
        diagnostics = []
    errors = [
        item for item in diagnostics
        if isinstance(item, dict) and str(item.get("severity", "")).lower() == "error"
    ]
    warnings = [
        item for item in diagnostics
        if isinstance(item, dict) and str(item.get("severity", "")).lower() == "warning"
    ]
    codes = sorted({
        str(item.get("code"))
        for item in diagnostics
        if isinstance(item, dict) and item.get("code")
    })
    return {
        "status": "recorded",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "codes": codes,
    }


def _summarize_ir_validation(payload: dict[str, Any] | None) -> dict[str, Any]:
    if payload is None:
        return {
            "status": "not_recorded",
            "success": None,
            "error_count": 0,
            "warning_count": 0,
        }
    validation = payload.get("validation") if isinstance(payload.get("validation"), dict) else payload
    return {
        "status": "recorded",
        "success": validation.get("success"),
        "error_count": int(validation.get("error_count", 0) or 0),
        "warning_count": int(validation.get("warning_count", 0) or 0),
        "utterance_count": validation.get("utterance_count"),
        "used_skit_group_motion_labels": validation.get("used_skit_group_motion_labels", []),
    }


def _summarize_apply_production(
    payload: dict[str, Any] | None,
    patched_ymmp: str | None,
) -> dict[str, Any]:
    if payload is None:
        return {
            "status": "not_recorded",
            "success": None,
            "dry_run": None,
            "output": patched_ymmp,
            "summary": {},
            "warning_count": 0,
        }
    summary = payload.get("summary")
    if not isinstance(summary, dict):
        summary = {}
    output = payload.get("output") or patched_ymmp
    return {
        "status": "recorded",
        "success": payload.get("success"),
        "dry_run": bool(payload.get("dry_run", False)),
        "output": output,
        "summary": summary,
        "warning_count": int(summary.get("warning_count", len(payload.get("warnings", []) or [])) or 0),
        "skit_group_placements": payload.get(
            "skit_group_placements",
            summary.get("skit_group_placements"),
        ),
        "skit_group_item_insertions": payload.get(
            "skit_group_item_insertions",
            summary.get("skit_group_item_insertions"),
        ),
    }


def _manual_acceptance_placeholders() -> dict[str, dict[str, str]]:
    return {
        "subtitle_check": {
            "status": "manual_pending",
            "note": "YMM4 import/read/subtitle display check is outside this manifest CLI.",
        },
        "ymm4_composition": {
            "status": "manual_pending",
            "note": "Open the patched .ymmp in YMM4 and judge spacing/timing/scene dominance.",
        },
        "thumbnail_check": {
            "status": "manual_pending",
            "note": "Use thumbnail_design/one-sheet when creating the YMM4 thumbnail template copy.",
        },
    }


def _derive_next_action(manifest: dict[str, Any]) -> str:
    paths = manifest.get("paths", {})
    validation = manifest.get("ir_validation", {})
    apply = manifest.get("apply_production", {})

    if paths.get("csv", {}).get("status") in {"not_recorded", "missing"}:
        return "Build CSV and record the output path."
    if paths.get("ir_json", {}).get("status") in {"not_recorded", "missing"}:
        return "Generate or collect Production IR for this CSV."
    if validation.get("status") == "not_recorded":
        return "Run validate-ir --format json and attach the result."
    if validation.get("success") is False:
        return "Fix IR validation errors before applying production changes."
    if apply.get("status") == "not_recorded":
        return "Run apply-production --dry-run or write mode and attach the result."
    if apply.get("success") is False:
        return "Fix apply-production failure before YMM4 acceptance."
    if apply.get("dry_run") is True:
        return "Run apply-production write mode after reviewing the dry-run summary."
    if paths.get("patched_ymmp", {}).get("status") in {"recorded", "missing"} or apply.get("output"):
        return "Open the patched .ymmp in YMM4 and record manual acceptance."
    return "Record the next production artifact or manual acceptance result."


def _md_value(value: Any) -> str:
    if value is None or value == "":
        return "-"
    return str(value).replace("|", "\\|")
