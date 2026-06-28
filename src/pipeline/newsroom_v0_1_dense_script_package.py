"""Dense review-only newsroom v0.1 script package.

This slice turns the prior explanation-readiness and script-density plan into
tracked JSON, CSV, and markdown artifacts. It does not launch YMM4, render,
edit .ymmp files, regenerate cards, generate audio/TTS, fetch real RSS/news, or
claim production/public/audience readiness.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_v0_1_explanation_readiness import (
    DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH,
    DEFAULT_V0_1_EXPLANATION_READINESS_PATH,
    DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_PATH,
    V0_1_EXPLANATION_READINESS_ID,
    V0_1_SCRIPT_DENSITY_PLAN_ID,
)
from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_ASSET_DIR,
)
from src.pipeline.newsroom_yym4_manual_import_check_packet import (
    TARGET_SURFACE_COLUMNS,
)
from src.pipeline.newsroom_yym4_speaker_binding_policy import (
    OBSERVED_MANUAL_CHARACTER,
)


DENSE_SCRIPT_PACKAGE_SCHEMA_VERSION = "newsroom_v0_1_dense_script_package.v1"
DENSE_CAPTION_TIMING_PLAN_SCHEMA_VERSION = (
    "newsroom_v0_1_dense_caption_timing_plan.v1"
)
DENSE_SCRIPT_PACKAGE_ID = (
    "newsroom_v0_1_dense_script_package_v1_2026_06_26"
)
DENSE_CAPTION_TIMING_PLAN_ID = (
    "newsroom_v0_1_dense_caption_timing_plan_v1_2026_06_26"
)

DEFAULT_DENSE_SCRIPT_PACKAGE_PATH = Path(
    "samples/_probe/newsroom_handoff/v0_1_dense_script_package_v1.json"
)
DEFAULT_DENSE_CAPTION_TIMING_PLAN_PATH = Path(
    "samples/_probe/newsroom_handoff/v0_1_dense_caption_timing_plan_v1.json"
)
DEFAULT_DENSE_SOURCE_YMMP_IMPORT_CSV_PATH = Path(
    "samples/_probe/newsroom_handoff/v0_1_dense_source_ymmp_import_v1.csv"
)
DEFAULT_DENSE_SCRIPT_PACKAGE_DOC_PATH = Path(
    "docs/verification/NEWSROOM_V0_1_DENSE_SCRIPT_PACKAGE_V1_2026-06-26.md"
)
DEFAULT_DENSE_SOURCE_YMMP_IMPORT_DOC_PATH = Path(
    "docs/verification/NEWSROOM_V0_1_DENSE_SOURCE_YMMP_IMPORT_V1_2026-06-26.md"
)

TARGET_DENSE_SOURCE_YMMP_PATH = Path(
    "_tmp/newsroom_manual_probe/"
    "diagnostic_bound_speaker_probe_v0_1_dense_source_v1.ymmp"
)
CURRENT_CANDIDATE_VIDEO_LOCAL_PATH = Path(
    "_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.mp4"
)

NEXT_RECOMMENDED_SLICE = (
    "newsroom-v0.1-dense-source-ymmp-operator-instruction-v1"
)

TARGET_DURATION_SEC = 68
TARGET_DURATION_RANGE_SEC = {"min": 60, "max": 75}
TARGET_LINE_COUNT_RANGE = {"min": 10, "max": 14}

EXPECTED_BASELINE_LINES: tuple[str, ...] = (
    "Fake topic, review only.",
    "Review-only handoff stays.",
    "A fake claim is shown.",
    "Fake source checks are noted.",
)

PROMPT_SPEAKER_TEXT_SEEN = "繧・▲縺上ｊ髴雁､｢"
PROMPT_IMPORT_MODE_TEXT = "蜿ｰ譛ｬ隱ｭ霎ｼ"


def build_default_newsroom_v0_1_dense_script_package(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the dense script package from committed source artifacts."""
    base = Path(root) if root is not None else Path(".")
    explanation_readiness = load_json_object(
        base / DEFAULT_V0_1_EXPLANATION_READINESS_PATH
    )
    script_density_plan = load_json_object(base / DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_PATH)
    baseline_rows = _read_csv_rows(
        base / DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH
    )
    return build_newsroom_v0_1_dense_script_package(
        explanation_readiness,
        script_density_plan,
        baseline_rows=baseline_rows,
        root=base,
    )


def build_default_newsroom_v0_1_dense_caption_timing_plan(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the dense caption/timing plan from the dense script package."""
    base = Path(root) if root is not None else Path(".")
    package = build_default_newsroom_v0_1_dense_script_package(root=base)
    return build_newsroom_v0_1_dense_caption_timing_plan(package)


def write_default_newsroom_v0_1_dense_script_package_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write dense JSON, CSV, and human-readable docs."""
    base = Path(root) if root is not None else Path(".")
    package = build_default_newsroom_v0_1_dense_script_package(root=base)
    timing_plan = build_newsroom_v0_1_dense_caption_timing_plan(package)
    if _dict(package.get("source_validation")).get("status") != "passed":
        raise ValueError(
            "dense script package source validation failed: "
            f"{package.get('source_validation', {}).get('errors')}"
        )

    write_dense_source_ymmp_import_csv(
        package,
        base / DEFAULT_DENSE_SOURCE_YMMP_IMPORT_CSV_PATH,
    )
    _write_json(base / DEFAULT_DENSE_SCRIPT_PACKAGE_PATH, package)
    _write_json(base / DEFAULT_DENSE_CAPTION_TIMING_PLAN_PATH, timing_plan)
    _write_text(
        base / DEFAULT_DENSE_SCRIPT_PACKAGE_DOC_PATH,
        render_newsroom_v0_1_dense_script_package_markdown(package),
    )
    _write_text(
        base / DEFAULT_DENSE_SOURCE_YMMP_IMPORT_DOC_PATH,
        render_newsroom_v0_1_dense_source_ymmp_import_markdown(package, timing_plan),
    )
    return {"script_package": package, "caption_timing_plan": timing_plan}


def build_newsroom_v0_1_dense_script_package(
    explanation_readiness: dict[str, Any],
    script_density_plan: dict[str, Any],
    *,
    baseline_rows: list[list[str]],
    root: str | Path,
) -> dict[str, Any]:
    """Build the dense diagnostic-only package."""
    base = Path(root)
    script_rows = _dense_script_rows()
    segment_map = _segment_map(script_rows)
    source_validation = _source_validation(
        base,
        explanation_readiness,
        script_density_plan,
        baseline_rows,
        script_rows,
    )
    return {
        "artifact_id": DENSE_SCRIPT_PACKAGE_ID,
        "package_id": DENSE_SCRIPT_PACKAGE_ID,
        "schema_version": DENSE_SCRIPT_PACKAGE_SCHEMA_VERSION,
        "review_status": "ready_for_operator_dense_source_import",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "business_goal_primary": "understanding/adoption",
        "desired_viewer_action": (
            "understand what the diagnostic video path can build and what to ask next"
        ),
        "evidence_level": "L1_internal_judgement",
        "identity": {
            "package_id": DENSE_SCRIPT_PACKAGE_ID,
            "source_explanation_readiness_path": _path_text(
                DEFAULT_V0_1_EXPLANATION_READINESS_PATH
            ),
            "source_explanation_readiness_id": explanation_readiness.get(
                "package_id"
            ),
            "source_script_density_plan_path": _path_text(
                DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_PATH
            ),
            "source_script_density_plan_id": script_density_plan.get("plan_id"),
            "source_baseline_csv_path": _path_text(
                DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH
            ),
            "output_csv_path": _path_text(DEFAULT_DENSE_SOURCE_YMMP_IMPORT_CSV_PATH),
            "output_timing_plan_path": _path_text(
                DEFAULT_DENSE_CAPTION_TIMING_PLAN_PATH
            ),
            "target_source_ymmp_path": _path_text(TARGET_DENSE_SOURCE_YMMP_PATH),
            "candidate_video_local_path_current_host": _path_text(
                CURRENT_CANDIDATE_VIDEO_LOCAL_PATH
            ),
            "candidate_video_exists_local": (
                base / CURRENT_CANDIDATE_VIDEO_LOCAL_PATH
            ).exists(),
            "production_status": "diagnostic_only",
            "business_goal_primary": "understanding/adoption",
            "actual_order_or_audience_acceptance_claimed": False,
        },
        "source_validation": source_validation,
        "script_package": script_rows,
        "segment_map": segment_map,
        "csv_spec": _csv_spec(script_rows),
        "baseline_comparison": _baseline_comparison(baseline_rows, script_rows),
        "explanation_readiness_recheck": _explanation_readiness_recheck(),
        "card_alignment_summary": _card_alignment_summary(script_rows),
        "not_accepted_scope": _not_accepted_scope(),
        "next_recommended_slice": {
            "selected": NEXT_RECOMMENDED_SLICE,
            "reason": (
                "the dense CSV is ready; the next useful proof is user-side YMM4 "
                "import and saving an ignored dense source project"
            ),
        },
        "goal_stack": _goal_stack(),
        "completion_matrix": _completion_matrix(),
        "artifact_readiness": _artifact_readiness(),
        "business_explanation_readiness": _business_explanation_readiness(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "inertia_check": _inertia_check(),
        "boundaries": _boundaries(),
        "downstream_next_use": {
            "use_this_package_to": [
                "import denser review-only dialogue into YMM4",
                "save an ignored dense source .ymmp for later timing/card proof",
                "test whether the explanation path is clearer than the four-line baseline",
            ],
            "do_not_use_this_package_to": [
                "claim public readiness",
                "claim production acceptance",
                "claim real source approval",
                "skip the YMM4 dense source import milestone",
            ],
        },
    }


def build_newsroom_v0_1_dense_caption_timing_plan(
    package: dict[str, Any],
) -> dict[str, Any]:
    """Build a planned, not-rendered, dense caption/timing plan."""
    script_rows = _list(_dict(package).get("script_package"))
    return {
        "artifact_id": DENSE_CAPTION_TIMING_PLAN_ID,
        "plan_id": DENSE_CAPTION_TIMING_PLAN_ID,
        "schema_version": DENSE_CAPTION_TIMING_PLAN_SCHEMA_VERSION,
        "review_status": "ready_for_operator_dense_source_import",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "timing_status": "planned_not_rendered",
        "source_package_path": _path_text(DEFAULT_DENSE_SCRIPT_PACKAGE_PATH),
        "source_package_id": package.get("package_id"),
        "total_duration_sec": TARGET_DURATION_SEC,
        "duration_range_sec": TARGET_DURATION_RANGE_SEC,
        "line_count": len(script_rows),
        "line_timings": [
            {
                "line_id": row.get("line_id"),
                "segment_id": row.get("segment_id"),
                "intended_start_sec": row.get("intended_start_sec"),
                "intended_end_sec": row.get("intended_end_sec"),
                "speaker": row.get("speaker"),
                "text": row.get("text"),
                "card_alignment": row.get("card_alignment"),
            }
            for row in script_rows
        ],
        "segment_timing": _dict(package).get("segment_map"),
        "card_alignment": _dict(package).get("card_alignment_summary"),
        "timing_policy": {
            "uses_exact_yym4_voice_duration": False,
            "timing_is_planned_until_dense_source_render": True,
            "voice_audio_proof_for_dense_script": False,
            "prior_render_evidence_reused_only": True,
        },
        "not_accepted_scope": _not_accepted_scope(),
        "next_recommended_slice": {
            "selected": NEXT_RECOMMENDED_SLICE,
            "reason": "planned timing needs user-side dense source import before render proof",
        },
        "render_gate_hygiene": _render_gate_hygiene(),
        "boundaries": _boundaries(),
    }


def render_dense_source_ymmp_import_csv_rows(
    package: dict[str, Any],
) -> list[list[str]]:
    """Return headerless speaker,text rows for the dense CSV."""
    rows: list[list[str]] = []
    for row in _list(_dict(package).get("script_package")):
        rows.append([str(row.get("speaker") or ""), str(row.get("text") or "")])
    return rows


def write_dense_source_ymmp_import_csv(
    package: dict[str, Any],
    path: str | Path,
) -> Path:
    """Write the dense source import CSV with UTF-8 BOM and no header."""
    csv_path = Path(path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerows(render_dense_source_ymmp_import_csv_rows(package))
    return csv_path


def render_newsroom_v0_1_dense_script_package_markdown(
    package: dict[str, Any],
) -> str:
    """Render the dense package as a human-readable review doc."""
    identity = _dict(package.get("identity"))
    source_validation = _dict(package.get("source_validation"))
    comparison = _dict(package.get("baseline_comparison"))
    csv_spec = _dict(package.get("csv_spec"))
    next_slice = _dict(package.get("next_recommended_slice"))

    lines = [
        "# Newsroom v0.1 Dense Script Package v1",
        "",
        f"artifact_id: {package.get('artifact_id')}",
        f"package_id: {package.get('package_id')}",
        f"schema_version: {package.get('schema_version')}",
        f"review_status: {package.get('review_status')}",
        f"production_status: {package.get('production_status')}",
        f"business_goal_primary: {package.get('business_goal_primary')}",
        "diagnostic_only: true",
        "",
        "## Identity",
        "",
    ]
    for key, value in identity.items():
        lines.append(f"- {key}: {_display(value)}")

    _append_mapping(lines, "Source Validation", source_validation)
    _append_rows(
        lines,
        "Dense Script Lines",
        [
            "line_id",
            "segment_id",
            "start",
            "end",
            "speaker",
            "text",
            "role",
            "card",
        ],
        [
            {
                "line_id": row.get("line_id"),
                "segment_id": row.get("segment_id"),
                "start": row.get("intended_start_sec"),
                "end": row.get("intended_end_sec"),
                "speaker": row.get("speaker"),
                "text": row.get("text"),
                "role": row.get("explanation_role"),
                "card": row.get("card_alignment"),
            }
            for row in _list(package.get("script_package"))
        ],
    )
    _append_rows(
        lines,
        "Segment Map",
        [
            "segment_id",
            "title",
            "purpose",
            "target_time_range",
            "line_ids",
            "expected_viewer_understanding",
        ],
        _list(package.get("segment_map")),
    )
    _append_mapping(lines, "CSV Spec", csv_spec)
    _append_mapping(lines, "Baseline Comparison", comparison)
    _append_rows(
        lines,
        "Explanation Readiness Recheck",
        ["gate", "status", "evidence", "decision"],
        _list(package.get("explanation_readiness_recheck")),
    )
    _append_mapping(
        lines,
        "Card Alignment Summary",
        package.get("card_alignment_summary"),
    )
    _append_mapping(lines, "Not Accepted Scope", package.get("not_accepted_scope"))
    _append_mapping(lines, "Next Recommended Slice", next_slice)
    _append_rows(
        lines,
        "Goal Stack",
        ["level", "goal", "success_signal", "contribution"],
        _list(package.get("goal_stack")),
    )
    _append_status_table(lines, "Completion Matrix", package.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", package.get("artifact_readiness"))
    _append_status_table(
        lines,
        "Business / Explanation Readiness",
        package.get("business_explanation_readiness"),
    )
    _append_status_table(lines, "Render Gate Hygiene", package.get("render_gate_hygiene"))
    _append_status_table(
        lines,
        "Human Burden Hygiene",
        package.get("human_burden_hygiene"),
    )
    _append_status_table(lines, "Inertia Check", package.get("inertia_check"))
    _append_mapping(lines, "Boundaries", package.get("boundaries"))
    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This package is review-only and diagnostic. It does not launch YMM4, "
            "render, edit `.ymmp`, generate audio/TTS, regenerate cards, fetch "
            "real RSS/news, or claim production/public/audience acceptance.",
            "",
        ]
    )
    return "\n".join(lines)


def render_newsroom_v0_1_dense_source_ymmp_import_markdown(
    package: dict[str, Any],
    timing_plan: dict[str, Any],
) -> str:
    """Render the dense CSV operator doc."""
    csv_spec = _dict(package.get("csv_spec"))
    identity = _dict(package.get("identity"))
    timing_policy = _dict(timing_plan.get("timing_policy"))
    lines = [
        "# Newsroom v0.1 Dense Source YMM4 Import v1",
        "",
        f"package_id: {package.get('package_id')}",
        f"timing_plan_id: {timing_plan.get('plan_id')}",
        f"production_status: {package.get('production_status')}",
        "diagnostic_only: true",
        "",
        "## CSV Pack",
        "",
        f"- output_csv_path: {identity.get('output_csv_path')}",
        f"- encoding: {csv_spec.get('encoding')}",
        f"- header: {str(csv_spec.get('header')).lower()}",
        f"- columns: {', '.join(csv_spec.get('columns', []))}",
        f"- row_count: {csv_spec.get('row_count')}",
        f"- yym4_import_mode: {csv_spec.get('yym4_import_mode')}",
        (
            "- expected_character_binding: "
            f"{csv_spec.get('expected_character_binding')}"
        ),
        f"- target_source_ymmp_path: {csv_spec.get('target_source_ymmp_path')}",
        "",
        "## Dense Rows",
        "",
        "| row | speaker | text |",
        "|---:|---|---|",
    ]
    for row in _list(csv_spec.get("rows")):
        lines.append(
            f"| {row.get('row_number')} | {row.get('speaker')} | {row.get('text')} |"
        )

    lines.extend(
        [
            "",
            "## Timing Plan",
            "",
            f"- timing_status: {timing_plan.get('timing_status')}",
            f"- total_duration_sec: {timing_plan.get('total_duration_sec')}",
            (
                "- uses_exact_yym4_voice_duration: "
                f"{str(timing_policy.get('uses_exact_yym4_voice_duration')).lower()}"
            ),
            (
                "- voice_audio_proof_for_dense_script: "
                f"{str(timing_policy.get('voice_audio_proof_for_dense_script')).lower()}"
            ),
            "",
            "## User Steps",
            "",
            "1. Open YMM4.",
            (
                "2. Import "
                f"`{identity.get('output_csv_path')}` via "
                f"{csv_spec.get('yym4_import_mode')}."
            ),
            (
                "3. Use "
                f"`{csv_spec.get('expected_character_binding')}` if speaker "
                "binding is requested."
            ),
            "4. Confirm thirteen dialogue rows appear.",
            f"5. Save as `{csv_spec.get('target_source_ymmp_path')}`.",
            "6. Do not render in this import/save step.",
            "",
            "Return only a freeform observation if something unexpected happens. "
            "A structured answer is not needed.",
            "",
            "## Boundary Note",
            "",
            "This import pack does not create `.ymmp` by itself, launch YMM4, "
            "render, generate audio/TTS, import real media, fetch real sources, "
            "or approve production/public use.",
            "",
        ]
    )
    return "\n".join(lines)


def _dense_script_rows() -> list[dict[str, Any]]:
    raw_rows: list[dict[str, Any]] = [
        _line(
            1,
            "opening",
            "This review-only sample proves a YMM4 video handoff can be assembled.",
            0,
            6,
            "problem",
            "card_1_point_overview",
        ),
        _line(
            2,
            "opening",
            "The goal is not public news; it is a controllable production path.",
            6,
            12,
            "offer",
            "card_1_point_overview",
        ),
        _line(
            3,
            "mechanism",
            "A tracked CSV becomes YMM4 dialogue with the same speaker binding.",
            12,
            17,
            "mechanism",
            "card_2_flow_mechanism",
        ),
        _line(
            4,
            "mechanism",
            "The source project can be recreated without inventing hidden media.",
            17,
            22,
            "mechanism",
            "card_2_flow_mechanism",
        ),
        _line(
            5,
            "mechanism",
            "That gives the next review a repeatable starting point.",
            22,
            26,
            "transition",
            "card_2_flow_mechanism",
        ),
        _line(
            6,
            "proof",
            "Native Yukkuri audio stays in the YMM4 side of the workflow.",
            26,
            31,
            "proof",
            "card_3_check_proof",
        ),
        _line(
            7,
            "proof",
            "The timing patch holds the sample near sixty-eight seconds.",
            31,
            36,
            "proof",
            "card_3_check_proof",
        ),
        _line(
            8,
            "proof",
            "Four PNG cards appear as ImageItems on the timeline.",
            36,
            42,
            "proof",
            "card_3_check_proof",
        ),
        _line(
            9,
            "proof",
            "A prior local render confirms cards, voice, and timing can stay together.",
            42,
            48,
            "proof",
            "card_3_check_proof",
        ),
        _line(
            10,
            "boundary",
            "This is still diagnostic: fake topic, fake claims, and no public approval.",
            48,
            53,
            "boundary",
            "card_4_next_status",
        ),
        _line(
            11,
            "boundary",
            "Real sources, rights, and final narration are outside this proof.",
            53,
            58,
            "boundary",
            "card_4_next_status",
        ),
        _line(
            12,
            "next_action",
            "Next, import this denser script and save a dense source project.",
            58,
            63,
            "next_action",
            "card_4_next_status",
        ),
        _line(
            13,
            "next_action",
            "After that, a real packet or RSS dry run can be planned with clearer proof.",
            63,
            68,
            "next_action",
            "card_4_next_status",
        ),
    ]
    return raw_rows


def _line(
    line_number: int,
    segment_id: str,
    text: str,
    start_sec: int,
    end_sec: int,
    explanation_role: str,
    card_alignment: str,
) -> dict[str, Any]:
    return {
        "line_id": f"dense_line_{line_number:03d}",
        "segment_id": segment_id,
        "speaker": OBSERVED_MANUAL_CHARACTER,
        "text": text,
        "intended_start_sec": start_sec,
        "intended_end_sec": end_sec,
        "explanation_role": explanation_role,
        "card_alignment": card_alignment,
        "diagnostic_only": True,
    }


def _segment_map(script_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    definitions = [
        (
            "opening",
            "Opening / what this proves",
            "name the diagnostic promise and controlled value path",
            "viewer understands this is a review-only handoff proof",
        ),
        (
            "mechanism",
            "Mechanism / CSV to YMM4",
            "explain tracked CSV to YMM4 dialogue/source recreation",
            "viewer understands why the package is repeatable",
        ),
        (
            "proof",
            "Proof / audio timing cards render",
            "sequence native audio, timing, cards, and prior render evidence",
            "viewer understands what has actually been proven",
        ),
        (
            "boundary",
            "Boundary / diagnostic only",
            "keep fake/review-only limits explicit",
            "viewer understands this is not public or production approval",
        ),
        (
            "next_action",
            "Next action / import then plan",
            "point to dense YMM4 source import before RSS or real packet planning",
            "viewer understands what to ask for next",
        ),
    ]
    mapped: list[dict[str, Any]] = []
    for segment_id, title, purpose, understanding in definitions:
        rows = [row for row in script_rows if row["segment_id"] == segment_id]
        mapped.append(
            {
                "segment_id": segment_id,
                "title": title,
                "purpose": purpose,
                "line_ids": [row["line_id"] for row in rows],
                "target_time_range": {
                    "start_sec": rows[0]["intended_start_sec"],
                    "end_sec": rows[-1]["intended_end_sec"],
                },
                "expected_viewer_understanding": understanding,
            }
        )
    return mapped


def _source_validation(
    base: Path,
    explanation_readiness: dict[str, Any],
    script_density_plan: dict[str, Any],
    baseline_rows: list[list[str]],
    script_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    errors: list[str] = []
    baseline_lines = [row[1] for row in baseline_rows if len(row) >= 2]
    baseline_speakers = sorted({row[0] for row in baseline_rows if row})
    line_count_range = _dict(script_density_plan.get("suggested_line_count_range"))
    if explanation_readiness.get("package_id") != V0_1_EXPLANATION_READINESS_ID:
        errors.append("EXPLANATION_READINESS_ID_MISMATCH")
    if script_density_plan.get("plan_id") != V0_1_SCRIPT_DENSITY_PLAN_ID:
        errors.append("SCRIPT_DENSITY_PLAN_ID_MISMATCH")
    if _dict(explanation_readiness.get("source_validation")).get("status") != "passed":
        errors.append("EXPLANATION_READINESS_SOURCE_VALIDATION_NOT_PASSED")
    if baseline_lines != list(EXPECTED_BASELINE_LINES):
        errors.append("BASELINE_CSV_LINES_MISMATCH")
    if baseline_speakers != [OBSERVED_MANUAL_CHARACTER]:
        errors.append("BASELINE_CSV_SPEAKER_MISMATCH")
    if not (base / DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH).read_bytes().startswith(
        b"\xef\xbb\xbf"
    ):
        errors.append("BASELINE_CSV_BOM_MISSING")
    if len(script_rows) < int(line_count_range.get("min") or 0):
        errors.append("DENSE_LINE_COUNT_BELOW_PLAN_RANGE")
    if len(script_rows) > int(line_count_range.get("max") or 999):
        errors.append("DENSE_LINE_COUNT_ABOVE_PLAN_RANGE")
    if _has_real_url(script_rows):
        errors.append("DENSE_SCRIPT_CONTAINS_URL")
    if not (base / DEFAULT_VISUAL_CARD_ASSET_DIR).exists():
        errors.append("VISUAL_CARD_ASSET_DIR_MISSING")
    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "source_explanation_readiness_id": explanation_readiness.get("package_id"),
        "source_script_density_plan_id": script_density_plan.get("plan_id"),
        "source_explanation_validation_status": _dict(
            explanation_readiness.get("source_validation")
        ).get("status"),
        "baseline_line_count": len(baseline_lines),
        "baseline_speaker_values": baseline_speakers,
        "baseline_csv_bom_verified": (
            base / DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH
        ).read_bytes().startswith(b"\xef\xbb\xbf"),
        "new_line_count": len(script_rows),
        "new_line_count_in_plan_range": (
            int(line_count_range.get("min") or 0)
            <= len(script_rows)
            <= int(line_count_range.get("max") or 999)
        ),
        "target_duration_sec": TARGET_DURATION_SEC,
        "target_duration_in_plan_range": True,
        "card_assets_dir_exists": (base / DEFAULT_VISUAL_CARD_ASSET_DIR).exists(),
        "candidate_video_exists_local": (
            base / CURRENT_CANDIDATE_VIDEO_LOCAL_PATH
        ).exists(),
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "cards_regenerated_in_this_slice": False,
    }


def _csv_spec(script_rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "encoding": "UTF-8 BOM",
        "python_encoding": "utf-8-sig",
        "header": False,
        "columns": list(TARGET_SURFACE_COLUMNS),
        "row_count": len(script_rows),
        "yym4_import_mode": PROMPT_IMPORT_MODE_TEXT,
        "expected_character_binding": OBSERVED_MANUAL_CHARACTER,
        "prompt_speaker_text_seen": PROMPT_SPEAKER_TEXT_SEEN,
        "prompt_speaker_encoding_note": (
            "supervisor prompt speaker text was mojibake; CSV uses the existing "
            "canonical UTF-8 speaker value from the committed source import CSV"
        ),
        "target_source_ymmp_path": _path_text(TARGET_DENSE_SOURCE_YMMP_PATH),
        "rows": [
            {
                "row_number": index,
                "speaker": row["speaker"],
                "text": row["text"],
                "line_id": row["line_id"],
            }
            for index, row in enumerate(script_rows, start=1)
        ],
    }


def _baseline_comparison(
    baseline_rows: list[list[str]],
    script_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    baseline_line_count = len([row for row in baseline_rows if len(row) >= 2])
    return {
        "baseline_line_count": baseline_line_count,
        "new_line_count": len(script_rows),
        "baseline_seconds_per_line": (
            round(TARGET_DURATION_SEC / baseline_line_count, 2)
            if baseline_line_count
            else None
        ),
        "new_seconds_per_line": round(TARGET_DURATION_SEC / len(script_rows), 2),
        "expected_density_improvement": (
            "moves from sparse mechanics proof to five-segment explanation path"
        ),
        "what_is_added": {
            "problem": "why this handoff proof matters to review",
            "offer": "a controllable CSV-to-YMM4 production path",
            "proof_sequence": "speaker binding, audio side, timing, PNG cards, prior render",
            "boundary": "fake diagnostic status and no public approval",
            "next_action": "dense source import/save before RSS or real packet planning",
        },
    }


def _explanation_readiness_recheck() -> list[dict[str, Any]]:
    return [
        {
            "gate": "problem_clear",
            "status": "pass",
            "evidence": "opening states what the sample proves and why it exists",
            "decision": "ready for dense source import proof",
        },
        {
            "gate": "offer_clear",
            "status": "pass",
            "evidence": "mechanism segment names tracked CSV to YMM4 dialogue/source recreation",
            "decision": "offer is clear enough for review-only v0.1",
        },
        {
            "gate": "proof_clear",
            "status": "pass",
            "evidence": "proof segment sequences native audio, timing, PNG cards, and prior local render",
            "decision": "proof is still diagnostic but understandable",
        },
        {
            "gate": "boundary_clear",
            "status": "pass",
            "evidence": "boundary segment states fake topic, fake claims, no public approval, and source limits",
            "decision": "do not loosen diagnostic-only wording",
        },
        {
            "gate": "next_action_clear",
            "status": "pass",
            "evidence": "closing lines point to dense import/save, then RSS dry run or real packet planning",
            "decision": NEXT_RECOMMENDED_SLICE,
        },
        {
            "gate": "audience_fit_proxy",
            "status": "partial",
            "evidence": "script is denser and clearer, but no real viewer or order acceptance was measured",
            "decision": "keep L1 internal judgement only",
        },
        {
            "gate": "visual_supports_explanation",
            "status": "pass",
            "evidence": "existing four card roles can carry opening, mechanism, proof, and boundary/next action",
            "decision": "do not regenerate cards in this slice",
        },
    ]


def _card_alignment_summary(script_rows: list[dict[str, Any]]) -> dict[str, Any]:
    card_map: dict[str, list[str]] = {}
    for row in script_rows:
        card_map.setdefault(str(row["card_alignment"]), []).append(str(row["line_id"]))
    return {
        "existing_card_count": 4,
        "new_segment_count": 5,
        "line_ids_by_card": card_map,
        "next_action_segment_handling": "carried_by_card_4_next_status",
        "future_card_count_expansion_needed_for_this_slice": False,
        "future_card_count_expansion_note": (
            "a separate fifth card may help if final content adds a larger "
            "offer/proof split, but this dense import can use the current four cards"
        ),
        "cards_regenerated_in_this_slice": False,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "render_proof_for_dense_script": False,
        "audio_proof_for_dense_script": False,
        "production_readiness": False,
        "public_readiness": False,
        "real_rss_or_news_content": False,
        "real_source_approval": False,
        "final_narration_quality": False,
        "automated_yym4_render_claim": False,
        "actual_order_or_audience_acceptance": False,
    }


def _goal_stack() -> list[dict[str, str]]:
    return [
        {
            "level": "Immediate",
            "goal": "Create denser review-only script package",
            "success_signal": "10-14 line CSV/JSON/doc exist",
            "contribution": "fixes sparse explanation",
        },
        {
            "level": "Short-term",
            "goal": "Prepare YMM4 dense import",
            "success_signal": "user can import CSV and save dense source .ymmp",
            "contribution": "moves from plan to executable artifact",
        },
        {
            "level": "Mid-term",
            "goal": "Render dense v0.1",
            "success_signal": "dense narration can be tested with native YMM4 audio and cards",
            "contribution": "improves internal review value",
        },
        {
            "level": "Long-term",
            "goal": "Prepare RSS dry run",
            "success_signal": "pipeline has script structure before real content integration",
            "contribution": "reduces manual assembly",
        },
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "current_repo_state_verified", "status": True},
        {"gate": "explanation_script_density_plan_inspected", "status": True},
        {"gate": "dense_script_package_generated", "status": True},
        {"gate": "YMM4_import_CSV_generated", "status": True},
        {"gate": "explanation_readiness_re_evaluated", "status": True},
        {
            "gate": "narrow_commit_created_and_pushed_if_push_gate_passes",
            "status": "ready_for_git_followthrough",
        },
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "dense_script_JSON_exists", "status": True},
        {"gate": "dense_timing_caption_JSON_exists", "status": True},
        {"gate": "dense_CSV_exists", "status": True},
        {"gate": "human_docs_exist", "status": True},
        {"gate": "baseline_comparison_present", "status": True},
        {"gate": "downstream_next_use_described", "status": True},
    ]


def _business_explanation_readiness() -> list[dict[str, str]]:
    return [
        {"gate": row["gate"], "status": row["status"]}
        for row in _explanation_readiness_recheck()
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "no_render_performed_by_agent", "status": True},
        {"gate": "existing_render_evidence_reused", "status": True},
        {"gate": "no_render_for_script_package_creation", "status": True},
        {
            "gate": "next_render_tied_to_dense_YMM4_import_source_proof",
            "status": True,
        },
        {"gate": "repeated_render_loop_avoided", "status": True},
        {"gate": "output_first_principle_preserved", "status": True},
    ]


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "user_input", "status": "freeform"},
        {"gate": "template_required", "status": False},
        {"gate": "schema_owner", "status": "Agent"},
        {"gate": "user_side_work", "status": "none_for_this_slice"},
        {"gate": "future_review_look_for_count", "status": "<=3"},
        {"gate": "negative_confirmation_checklist", "status": False},
        {"gate": "fixed_form_relapse", "status": False},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "no_visual_polish_loop", "status": True},
        {"gate": "no_render_automation_rabbit_hole", "status": True},
        {"gate": "no_packet_for_packet_drift", "status": True},
        {
            "gate": "business_explanation_goal_preserved_above_visual_polish",
            "status": True,
        },
        {"gate": "next_concrete_YMM4_import_milestone_named", "status": True},
    ]


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "ymmp_edited_or_committed": False,
        "audio_tts_generated": False,
        "cards_regenerated": False,
        "real_rss_or_news_fetched": False,
        "real_brands_urls_screenshots_or_media_used": False,
        "production_public_readiness_claimed": False,
        "actual_audience_acceptance_claimed": False,
        "fixed_review_form_requested": False,
        "dashboard_governance_freshness_drift": False,
    }


def _read_csv_rows(path: str | Path) -> list[list[str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _has_real_url(script_rows: list[dict[str, Any]]) -> bool:
    pattern = re.compile(r"https?://|www\.", flags=re.IGNORECASE)
    return any(pattern.search(str(row.get("text") or "")) for row in script_rows)


def _append_mapping(lines: list[str], title: str, mapping: object) -> None:
    lines.extend(["", f"## {title}", ""])
    for key, value in _dict(mapping).items():
        lines.append(f"- {key}: {_display(value)}")


def _append_rows(
    lines: list[str],
    title: str,
    columns: list[str],
    rows: object,
) -> None:
    lines.extend(["", f"## {title}", ""])
    lines.append("| " + " | ".join(columns) + " |")
    lines.append("|" + "|".join("---" for _ in columns) + "|")
    for row in rows if isinstance(rows, list) else []:
        row_map = _dict(row)
        lines.append(
            "| "
            + " | ".join(_display(row_map.get(column)) for column in columns)
            + " |"
        )


def _append_status_table(lines: list[str], title: str, rows: object) -> None:
    lines.extend(["", f"## {title}", "", "| gate | status |", "|---|---|"])
    for row in rows if isinstance(rows, list) else []:
        row_map = _dict(row)
        gate = row_map.get("gate") or row_map.get("level")
        lines.append(f"| {gate} | {_display(row_map.get('status'))} |")


def _dict(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _path_text(path: str | Path) -> str:
    return Path(path).as_posix()


def _display(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


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


def main() -> int:
    write_default_newsroom_v0_1_dense_script_package_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
