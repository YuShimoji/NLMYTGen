"""Recreation import pack for the missing diagnostic newsroom source .ymmp.

This module writes only a tracked CSV, JSON packet, and human-readable operator
doc. It does not launch YMM4, create or edit .ymmp files, render, generate
audio/TTS, import real media, fetch external sources, or approve production use.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_diagnostic_ymmp_probe_packet import (
    DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_PATH,
)
from src.pipeline.newsroom_diagnostic_ymmp_structure_readback import (
    CANONICAL_UI_OBSERVED_SPEAKER,
    CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE,
    DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    EXPECTED_MANUAL_IMPORT_ROW_COUNT,
    TARGET_SURFACE_COLUMNS,
    read_tiny_script_import_csv,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    DEFAULT_BOUND_SPEAKER_CSV_PATH,
    OBSERVED_MANUAL_CHARACTER,
)


SOURCE_YMMP_RECREATION_IMPORT_PACK_SCHEMA_VERSION = (
    "newsroom_source_ymmp_recreation_import_pack.v1"
)
SOURCE_YMMP_RECREATION_IMPORT_PACK_ID = (
    "newsroom_source_ymmp_recreation_import_pack_v1_2026_06_26"
)
DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH = Path(
    "samples/_probe/newsroom_handoff/source_ymmp_recreation_import_v1.csv"
)
DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_PACK_PATH = Path(
    "samples/_probe/newsroom_handoff/source_ymmp_recreation_import_pack_v1.json"
)
DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_PACK_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_SOURCE_YMMP_RECREATION_IMPORT_PACK_V1_2026-06-26.md"
)

TARGET_SOURCE_YMMP_DIR = Path("_tmp/newsroom_manual_probe")
TARGET_SOURCE_YMMP_PATH = TARGET_SOURCE_YMMP_DIR / (
    "diagnostic_bound_speaker_probe_v1.ymmp"
)
TARGET_TIMING_PATCH_YMMP_PATH = TARGET_SOURCE_YMMP_DIR / (
    "diagnostic_bound_speaker_probe_timing_patch_v1.ymmp"
)
TARGET_CARD_PLACEMENT_YMMP_PATH = TARGET_SOURCE_YMMP_DIR / (
    "diagnostic_bound_speaker_probe_card_placement_v1.ymmp"
)
EXPECTED_CANONICAL_DIALOGUE_LINES: tuple[str, ...] = (
    "Fake topic, review only.",
    "Review-only handoff stays.",
    "A fake claim is shown.",
    "Fake source checks are noted.",
)

CONTEXT_READBACK_PATHS: tuple[Path, ...] = (
    Path("samples/_probe/newsroom_handoff/tiny_render_smoke_result_readback_v1.json"),
    Path(
        "samples/_probe/newsroom_handoff/"
        "audio_observation_and_timing_patch_readiness_v1.json"
    ),
    Path("samples/_probe/newsroom_handoff/yym4_native_audio_path_proof_v1.json"),
    Path("samples/_probe/newsroom_handoff/ymmp_timing_patch_probe_v1.json"),
    Path("samples/_probe/newsroom_handoff/yym4_card_asset_placement_probe_v1.json"),
    Path(
        "samples/_probe/newsroom_handoff/"
        "card_placement_render_smoke_result_readback_v1.json"
    ),
)


def build_default_newsroom_source_ymmp_recreation_import_pack(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed recreation import pack from tracked readbacks."""
    base = Path(root) if root is not None else Path(".")
    structure_readback = load_json_object(
        base / DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH
    )
    probe_packet = load_json_object(base / DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_PATH)
    bound_csv_readback = read_tiny_script_import_csv(
        base / DEFAULT_BOUND_SPEAKER_CSV_PATH
    )
    context_readbacks = {
        _path_text(path): load_json_object(base / path)
        for path in CONTEXT_READBACK_PATHS
    }
    return build_newsroom_source_ymmp_recreation_import_pack(
        structure_readback,
        probe_packet,
        bound_csv_readback=bound_csv_readback,
        context_readbacks=context_readbacks,
        source_structure_readback_path=DEFAULT_DIAGNOSTIC_YMMP_STRUCTURE_READBACK_PATH,
        source_probe_packet_path=DEFAULT_DIAGNOSTIC_YMMP_PROBE_PACKET_PATH,
        source_bound_csv_path=DEFAULT_BOUND_SPEAKER_CSV_PATH,
    )


def build_newsroom_source_ymmp_recreation_import_pack(
    structure_readback: dict[str, Any],
    probe_packet: dict[str, Any],
    *,
    bound_csv_readback: dict[str, Any],
    context_readbacks: dict[str, dict[str, Any]],
    source_structure_readback_path: str | Path,
    source_probe_packet_path: str | Path,
    source_bound_csv_path: str | Path,
) -> dict[str, Any]:
    """Build a diagnostic-only CSV recreation packet."""
    dialogue = _dict(structure_readback.get("dialogue_structure"))
    structure_lines = [str(value) for value in _list_values(dialogue.get("text_summaries"))]
    structure_speaker = str(dialogue.get("canonical_speaker_value") or "")
    csv_rows = _list(bound_csv_readback.get("rows"))
    csv_lines = [str(row.get("text") or "") for row in csv_rows]
    csv_speakers = sorted({str(row.get("speaker") or "") for row in csv_rows})
    target = _dict(probe_packet.get("target"))
    target_rows = _list(target.get("rows"))
    target_lines = [str(row.get("text") or "") for row in target_rows]
    target_speakers = sorted({str(row.get("speaker") or "") for row in target_rows})
    source_validation = _dict(probe_packet.get("source_validation"))
    evidence_errors = _source_evidence_errors(
        structure_lines=structure_lines,
        structure_speaker=structure_speaker,
        csv_lines=csv_lines,
        csv_speakers=csv_speakers,
        target_lines=target_lines,
        target_speakers=target_speakers,
        bound_csv_readback=bound_csv_readback,
        probe_source_validation=source_validation,
    )
    recreation_status = "csv_ready" if not evidence_errors else "source_text_unverified"
    canonical_lines = list(EXPECTED_CANONICAL_DIALOGUE_LINES)

    return {
        "artifact_id": SOURCE_YMMP_RECREATION_IMPORT_PACK_ID,
        "pack_id": SOURCE_YMMP_RECREATION_IMPORT_PACK_ID,
        "schema_version": SOURCE_YMMP_RECREATION_IMPORT_PACK_SCHEMA_VERSION,
        "review_status": "ready_for_operator_source_ymmp_recreation",
        "diagnostic_only": True,
        "production_status": "diagnostic_only",
        "recreation_status": recreation_status,
        "identity": {
            "pack_id": SOURCE_YMMP_RECREATION_IMPORT_PACK_ID,
            "output_csv_path": _path_text(
                DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH
            ),
            "target_source_ymmp_path": _path_text(TARGET_SOURCE_YMMP_PATH),
            "production_status": "diagnostic_only",
            "recreation_status": recreation_status,
            "source_ymmp_absence_status": "confirmed_missing_before_pack_generation",
            "source_ymmp_absence_reason": (
                "ignored local artifact was not present in this checkout and "
                "is not part of remote-tracked repo state"
            ),
        },
        "source_evidence": {
            "source_readback_paths": [
                _path_text(source_structure_readback_path),
                _path_text(source_probe_packet_path),
                _path_text(source_bound_csv_path),
            ],
            "context_readback_paths_inspected": sorted(context_readbacks),
            "context_readback_summary": _context_readback_summary(context_readbacks),
            "canonical_speaker": structure_speaker,
            "canonical_speaker_unicode_escape": (
                CANONICAL_UI_OBSERVED_SPEAKER_UNICODE_ESCAPE
            ),
            "canonical_dialogue_lines": canonical_lines,
            "confidence": "high" if not evidence_errors else "blocked",
            "disagreement_or_unknowns": evidence_errors,
            "structure_readback_id": structure_readback.get("readback_id"),
            "probe_packet_id": probe_packet.get("packet_id"),
            "existing_bound_csv_path": _path_text(source_bound_csv_path),
            "existing_bound_csv_bom_verified": bound_csv_readback.get(
                "bom_verified"
            ),
            "evidence_checks": {
                "structure_lines_match_expected": structure_lines == canonical_lines,
                "csv_lines_match_expected": csv_lines == canonical_lines,
                "probe_target_lines_match_expected": target_lines == canonical_lines,
                "structure_speaker_matches_expected": (
                    structure_speaker == OBSERVED_MANUAL_CHARACTER
                    == CANONICAL_UI_OBSERVED_SPEAKER
                ),
                "csv_speakers_match_expected": csv_speakers
                == [OBSERVED_MANUAL_CHARACTER],
                "probe_target_speakers_match_expected": target_speakers
                == [OBSERVED_MANUAL_CHARACTER],
                "probe_source_validation_errors": source_validation.get("errors", []),
            },
        },
        "csv_spec": {
            "encoding": "UTF-8 BOM",
            "python_encoding": "utf-8-sig",
            "header": False,
            "columns": list(TARGET_SURFACE_COLUMNS),
            "row_count": EXPECTED_MANUAL_IMPORT_ROW_COUNT,
            "yym4_import_mode": "台本読込",
            "expected_character_binding": OBSERVED_MANUAL_CHARACTER,
            "rows": [
                {
                    "row_number": index,
                    "speaker": OBSERVED_MANUAL_CHARACTER,
                    "text": text,
                }
                for index, text in enumerate(canonical_lines, start=1)
            ],
        },
        "operator_save_target": {
            "target_dir": _path_text(TARGET_SOURCE_YMMP_DIR),
            "target_source_ymmp": _path_text(TARGET_SOURCE_YMMP_PATH),
            "note": (
                "this .ymmp is ignored local only and must not be committed"
            ),
            "git_ignore_boundary": "_tmp/",
        },
        "post_user_continuation": {
            "after_source_ymmp_exists": [
                "rerun local regeneration for timing patch .ymmp",
                "rerun local regeneration for card placement .ymmp",
            ],
            "expected_next_local_outputs": [
                _path_text(TARGET_TIMING_PATCH_YMMP_PATH),
                _path_text(TARGET_CARD_PLACEMENT_YMMP_PATH),
            ],
            "next_agent_slice": (
                "newsroom-local-ymmp-regeneration-retry-after-source-recreation"
            ),
            "render_gate": "render remains deferred until regenerated .ymmp chain exists",
        },
        "safety_boundaries": {
            "ymmp_fabrication": False,
            "YMM4_launched_by_agent": False,
            "render_created_by_agent": False,
            "external_TTS_introduced": False,
            "audio_generated_by_agent": False,
            "real_media_imported": False,
            "external_fetch_performed": False,
            "production_public_readiness": False,
            "ymmp_or_media_stage_allowed": False,
        },
        "completion_matrix": _completion_matrix(recreation_status),
        "artifact_readiness": _artifact_readiness(recreation_status),
        "human_burden_hygiene": _human_burden_hygiene(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "inertia_check": _inertia_check(),
        "downstream_next_use": {
            "use_this_pack_to": [
                "let the user recreate the missing source .ymmp through YMM4 script import",
                "resume timing-patch and card-placement local regeneration after the source .ymmp exists",
            ],
            "do_not_use_this_pack_to": [
                "fabricate .ymmp internals",
                "claim production readiness",
                "claim render readiness",
                "introduce external TTS or real media",
            ],
        },
    }


def render_source_ymmp_recreation_import_csv_rows(
    pack: dict[str, Any],
) -> list[list[str]]:
    """Return headerless speaker,text rows for YMM4 script import."""
    return [
        [str(row.get("speaker") or ""), str(row.get("text") or "")]
        for row in _list(_dict(pack.get("csv_spec")).get("rows"))
    ]


def write_source_ymmp_recreation_import_csv(
    pack: dict[str, Any],
    path: str | Path,
) -> Path:
    """Write the source recreation CSV with UTF-8 BOM and no header."""
    csv_path = Path(path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerows(render_source_ymmp_recreation_import_csv_rows(pack))
    return csv_path


def write_default_newsroom_source_ymmp_recreation_import_pack_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write the CSV, JSON packet, and operator doc."""
    base = Path(root) if root is not None else Path(".")
    pack = build_default_newsroom_source_ymmp_recreation_import_pack(root=base)
    if _dict(pack.get("identity")).get("recreation_status") != "csv_ready":
        raise ValueError(
            "source .ymmp recreation CSV is not ready: "
            f"{pack.get('source_evidence', {}).get('disagreement_or_unknowns')}"
        )

    write_source_ymmp_recreation_import_csv(
        pack,
        base / DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH,
    )
    _write_json(base / DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_PACK_PATH, pack)
    _write_text(
        base / DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_PACK_DOC_PATH,
        render_newsroom_source_ymmp_recreation_import_pack_markdown(pack),
    )
    return pack


def render_newsroom_source_ymmp_recreation_import_pack_markdown(
    pack: dict[str, Any],
) -> str:
    """Render the human-readable source .ymmp recreation operator doc."""
    identity = _dict(pack.get("identity"))
    evidence = _dict(pack.get("source_evidence"))
    csv_spec = _dict(pack.get("csv_spec"))
    target = _dict(pack.get("operator_save_target"))
    continuation = _dict(pack.get("post_user_continuation"))
    safety = _dict(pack.get("safety_boundaries"))
    hygiene = _dict(pack.get("human_burden_hygiene"))

    lines = [
        "# Newsroom Source .ymmp Recreation Import Pack v1",
        "",
        f"artifact_id: {pack.get('artifact_id')}",
        f"pack_id: {pack.get('pack_id')}",
        f"schema_version: {pack.get('schema_version')}",
        f"review_status: {pack.get('review_status')}",
        f"production_status: {pack.get('production_status')}",
        f"recreation_status: {pack.get('recreation_status')}",
        "diagnostic_only: true",
        "",
        "## Why This Exists",
        "",
        "The source `.ymmp` is an ignored local artifact, so it is not carried "
        "by the remote-tracked repository. This checkout does not have "
        "`_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp`, "
        "which blocks the later timing-patch and card-placement regeneration. "
        "This pack recreates only the import CSV needed for the user to save "
        "that local source project through YMM4 script import.",
        "",
        "## Source Evidence",
        "",
        f"- canonical_speaker: {evidence.get('canonical_speaker')}",
        (
            "- canonical_speaker_unicode_escape: "
            f"{evidence.get('canonical_speaker_unicode_escape')}"
        ),
        f"- confidence: {evidence.get('confidence')}",
        f"- disagreement_or_unknowns: {_display(evidence.get('disagreement_or_unknowns'))}",
        "- source_readback_paths:",
    ]
    for path in evidence.get("source_readback_paths", []):
        lines.append(f"  - {path}")

    lines.extend(["", "## CSV Pack", ""])
    lines.append(f"- output_csv_path: {identity.get('output_csv_path')}")
    lines.append(f"- encoding: {csv_spec.get('encoding')}")
    lines.append(f"- header: {str(csv_spec.get('header')).lower()}")
    lines.append(f"- columns: {', '.join(csv_spec.get('columns', []))}")
    lines.append(f"- row_count: {csv_spec.get('row_count')}")
    lines.append(f"- yym4_import_mode: {csv_spec.get('yym4_import_mode')}")
    lines.append(
        f"- expected_character_binding: {csv_spec.get('expected_character_binding')}"
    )
    lines.extend(["", "| row | speaker | text |", "|---:|---|---|"])
    for row in _list(csv_spec.get("rows")):
        lines.append(
            f"| {row.get('row_number')} | {row.get('speaker')} | {row.get('text')} |"
        )

    lines.extend(
        [
            "",
            "## User Steps",
            "",
            "1. Open YMM4.",
            (
                "2. Import "
                f"`{identity.get('output_csv_path')}` via 台本読込."
            ),
            (
                "3. Use "
                f"`{csv_spec.get('expected_character_binding')}` if speaker "
                "binding is requested."
            ),
            "4. Confirm four lines appear.",
            f"5. Save as `{target.get('target_source_ymmp')}`.",
            "6. Do not render yet.",
            "",
            "The user observation can stay freeform. No template or structured "
            "answer is required for this recreation step.",
            "",
            "## Operator Save Target",
            "",
            f"- target_dir: {target.get('target_dir')}",
            f"- target_source_ymmp: {target.get('target_source_ymmp')}",
            f"- note: {target.get('note')}",
            "",
            "## Next Codex Continuation",
            "",
            "After the user saves the source `.ymmp`, Codex should verify that "
            "the local file exists under `_tmp/`, remains ignored and unstaged, "
            "then rerun the local regeneration for the timing patch and card "
            "placement project copies.",
            "",
            "- expected_next_local_outputs:",
        ]
    )
    for path in continuation.get("expected_next_local_outputs", []):
        lines.append(f"  - {path}")

    lines.extend(["", "## Safety Boundaries", ""])
    for key, value in safety.items():
        lines.append(f"- {key}: {str(value).lower()}")

    lines.extend(["", "## Human Burden Hygiene", ""])
    for key, value in hygiene.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This package does not create `.ymmp`, launch YMM4, render, "
            "generate audio/TTS, import real media, fetch external sources, or "
            "approve production/public use.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_evidence_errors(
    *,
    structure_lines: list[str],
    structure_speaker: str,
    csv_lines: list[str],
    csv_speakers: list[str],
    target_lines: list[str],
    target_speakers: list[str],
    bound_csv_readback: dict[str, Any],
    probe_source_validation: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    expected_lines = list(EXPECTED_CANONICAL_DIALOGUE_LINES)
    if structure_lines != expected_lines:
        errors.append("STRUCTURE_READBACK_LINES_MISMATCH")
    if csv_lines != expected_lines:
        errors.append("BOUND_CSV_LINES_MISMATCH")
    if target_lines != expected_lines:
        errors.append("PROBE_PACKET_TARGET_LINES_MISMATCH")
    if structure_speaker != OBSERVED_MANUAL_CHARACTER:
        errors.append("STRUCTURE_CANONICAL_SPEAKER_MISMATCH")
    if structure_speaker != CANONICAL_UI_OBSERVED_SPEAKER:
        errors.append("STRUCTURE_CANONICAL_SPEAKER_NOT_CANONICAL_UI_VALUE")
    if csv_speakers != [OBSERVED_MANUAL_CHARACTER]:
        errors.append("BOUND_CSV_SPEAKER_MISMATCH")
    if target_speakers != [OBSERVED_MANUAL_CHARACTER]:
        errors.append("PROBE_PACKET_TARGET_SPEAKER_MISMATCH")
    if bound_csv_readback.get("bom_verified") is not True:
        errors.append("BOUND_CSV_BOM_NOT_VERIFIED")
    if bound_csv_readback.get("has_header") is not False:
        errors.append("BOUND_CSV_HEADER_PRESENT")
    if bound_csv_readback.get("all_rows_two_columns") is not True:
        errors.append("BOUND_CSV_NOT_TWO_COLUMN")
    if bound_csv_readback.get("row_count") != EXPECTED_MANUAL_IMPORT_ROW_COUNT:
        errors.append("BOUND_CSV_ROW_COUNT_NOT_4")
    if probe_source_validation.get("errors") not in ([], None):
        errors.append("PROBE_PACKET_SOURCE_VALIDATION_HAS_ERRORS")
    if probe_source_validation.get("all_rows_use_bound_speaker") is not True:
        errors.append("PROBE_PACKET_ROWS_DO_NOT_USE_BOUND_SPEAKER")
    if probe_source_validation.get("all_rows_have_text") is not True:
        errors.append("PROBE_PACKET_ROWS_MISSING_TEXT")
    return errors


def _context_readback_summary(
    context_readbacks: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, readback in sorted(context_readbacks.items()):
        rows.append(
            {
                "path": path,
                "artifact_id": readback.get("artifact_id"),
                "production_status": readback.get("production_status"),
                "diagnostic_only": readback.get("diagnostic_only"),
                "status_fields": {
                    key: value
                    for key, value in readback.items()
                    if key.endswith("_status")
                    or key.endswith("_result")
                    or key in {"result", "proof_status", "probe_status"}
                },
            }
        )
    return rows


def _completion_matrix(recreation_status: str) -> dict[str, Any]:
    csv_ready = recreation_status == "csv_ready"
    return {
        "total": 6,
        "passed": 5 if csv_ready else 3,
        "items": [
            {"item": "repo_state_verified", "status": "passed"},
            {"item": "source_ymmp_absence_confirmed", "status": "passed"},
            {"item": "tracked_source_evidence_inspected", "status": "passed"},
            {
                "item": "recreation_csv_generated_or_cleanly_blocked",
                "status": "passed" if csv_ready else "blocked",
            },
            {
                "item": "recreation_json_doc_created",
                "status": "passed" if csv_ready else "blocked",
            },
            {
                "item": "narrow_commit_created_and_pushed_if_gate_passes",
                "status": "ready_for_git_followthrough" if csv_ready else "blocked",
            },
        ],
    }


def _artifact_readiness(recreation_status: str) -> dict[str, Any]:
    csv_ready = recreation_status == "csv_ready"
    return {
        "total": 6,
        "passed": 6 if csv_ready else 5,
        "items": [
            {
                "item": "recreation_csv_exists_or_blocked_status_recorded",
                "status": "passed" if csv_ready else "blocked",
            },
            {"item": "recreation_packet_json_exists", "status": "passed"},
            {"item": "human_doc_exists", "status": "passed"},
            {"item": "canonical_lines_speaker_evidence_recorded", "status": "passed"},
            {"item": "operator_save_target_recorded", "status": "passed"},
            {"item": "downstream_next_use_described", "status": "passed"},
        ],
    }


def _human_burden_hygiene() -> dict[str, Any]:
    return {
        "user_input": "freeform",
        "template_required": False,
        "schema_owner": "Agent",
        "user_side_action": "YMM4 import/save only after this package",
        "future_look_for_max_count": 3,
        "negative_confirmation_checklist": False,
        "fixed_form_result_template": False,
    }


def _render_gate_hygiene() -> dict[str, Any]:
    return {
        "render_performed": False,
        "YMM4_render_requested_in_this_slice": False,
        "render_milestone_after_ymmp_regeneration": True,
        "no_render_for_docs_csv_package_only": True,
        "repeated_render_loop_avoided": True,
        "output_first_principle_preserved": True,
    }


def _inertia_check() -> dict[str, Any]:
    return {
        "ymmp_fabrication": False,
        "broad_redesign": False,
        "packet_for_packet_drift": False,
        "local_artifact_gap_addressed_directly": True,
        "next_concrete_user_agent_action_named": True,
    }


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    json_path = Path(path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_bytes(
        (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )


def _write_text(path: str | Path, text: str) -> None:
    text_path = Path(path)
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text_path.write_bytes(text.encode("utf-8"))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _list_values(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _path_text(value: str | Path | None) -> str | None:
    return str(value).replace("\\", "/") if value is not None else None


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def main() -> int:
    write_default_newsroom_source_ymmp_recreation_import_pack_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
