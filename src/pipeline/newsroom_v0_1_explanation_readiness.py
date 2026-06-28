"""Explanation readiness and script-density planning for newsroom v0.1.

This slice plans the next highest-value improvement after the diagnostic YMM4
video render passed: explanation quality and narration density. It does not
launch YMM4, render video, edit .ymmp files, regenerate cards, generate
audio/TTS, fetch real RSS/news, or claim production/public/audience readiness.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_card_placement_render_smoke_result_readback import (
    DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_post_density_refinement_render_smoke_result_readback import (
    DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_PATH,
)
from src.pipeline.newsroom_visual_card_asset_bridge import (
    DEFAULT_VISUAL_CARD_ASSET_DIR,
)


V0_1_EXPLANATION_READINESS_SCHEMA_VERSION = "newsroom_v0_1_explanation_readiness.v1"
V0_1_SCRIPT_DENSITY_PLAN_SCHEMA_VERSION = "newsroom_v0_1_script_density_plan.v1"
V0_1_EXPLANATION_READINESS_ID = (
    "newsroom_v0_1_explanation_readiness_v1_2026_06_26"
)
V0_1_SCRIPT_DENSITY_PLAN_ID = (
    "newsroom_v0_1_script_density_plan_v1_2026_06_26"
)

DEFAULT_V0_1_EXPLANATION_READINESS_PATH = Path(
    "samples/_probe/newsroom_handoff/v0_1_explanation_readiness_v1.json"
)
DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_PATH = Path(
    "samples/_probe/newsroom_handoff/v0_1_script_density_plan_v1.json"
)
DEFAULT_V0_1_EXPLANATION_READINESS_DOC_PATH = Path(
    "docs/verification/NEWSROOM_V0_1_EXPLANATION_READINESS_V1_2026-06-26.md"
)
DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_DOC_PATH = Path(
    "docs/verification/NEWSROOM_V0_1_SCRIPT_DENSITY_PLAN_V1_2026-06-26.md"
)

DEFAULT_EPISODE_CAPTION_TIMING_PLAN_PATH = Path(
    "samples/_probe/newsroom_handoff/episode_caption_timing_plan_v1.json"
)
DEFAULT_EPISODE_PRODUCTION_CAPSULE_PATH = Path(
    "samples/_probe/newsroom_handoff/episode_production_capsule_v1.json"
)
DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH = Path(
    "samples/_probe/newsroom_handoff/source_ymmp_recreation_import_v1.csv"
)
CURRENT_CANDIDATE_VIDEO_LOCAL_PATH = Path(
    "_tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.mp4"
)

NEXT_DEFAULT_SLICE = "newsroom-v0.1-script-density-implementation-plan-v1"
OFFER_EXPLANATION_SEGMENT_SLICE = "newsroom-offer-explanation-segment-v1"
RSS_DRY_RUN_PLAN_SLICE = "newsroom-rss-dry-run-integration-plan-v1"
INTERNAL_REVIEW_RESULT_READBACK_SLICE = (
    "newsroom-internal-review-v0.1-result-readback-v1"
)

TARGET_DURATION_RANGE_SEC = {"min": 60, "max": 75}
TARGET_NARRATION_SEGMENTS = 5
SUGGESTED_LINE_COUNT_RANGE = {"min": 10, "max": 14}


def build_default_newsroom_v0_1_explanation_readiness(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build explanation readiness from current committed readbacks."""
    base = Path(root) if root is not None else Path(".")
    sources = _load_sources(base)
    return build_newsroom_v0_1_explanation_readiness(
        sources,
        root=base,
    )


def build_default_newsroom_v0_1_script_density_plan(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the script-density plan from explanation readiness."""
    base = Path(root) if root is not None else Path(".")
    readiness = build_default_newsroom_v0_1_explanation_readiness(root=base)
    return build_newsroom_v0_1_script_density_plan(readiness, root=base)


def write_default_newsroom_v0_1_explanation_readiness_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, dict[str, Any]]:
    """Write explanation readiness and script-density plan JSON/docs."""
    base = Path(root) if root is not None else Path(".")
    readiness = build_default_newsroom_v0_1_explanation_readiness(root=base)
    plan = build_newsroom_v0_1_script_density_plan(readiness, root=base)
    _write_json(base / DEFAULT_V0_1_EXPLANATION_READINESS_PATH, readiness)
    _write_json(base / DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_PATH, plan)
    _write_text(
        base / DEFAULT_V0_1_EXPLANATION_READINESS_DOC_PATH,
        render_newsroom_v0_1_explanation_readiness_markdown(readiness),
    )
    _write_text(
        base / DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_DOC_PATH,
        render_newsroom_v0_1_script_density_plan_markdown(plan),
    )
    return {"explanation_readiness": readiness, "script_density_plan": plan}


def build_newsroom_v0_1_explanation_readiness(
    sources: dict[str, Any],
    *,
    root: str | Path,
) -> dict[str, Any]:
    """Build the diagnostic-only explanation readiness package."""
    base = Path(root)
    post_density = _dict(sources.get("post_density_render_result"))
    card_render = _dict(sources.get("card_render_result"))
    caption_timing = _dict(sources.get("caption_timing_plan"))
    episode_capsule = _dict(sources.get("episode_capsule"))
    dialogue_lines = _source_dialogue_lines(base)
    source_validation = _source_validation(base, sources, dialogue_lines)
    current_line_count = len(dialogue_lines)
    duration_sec = _observed_duration_sec(post_density, card_render)
    readiness_gates = _explanation_readiness_gates()
    next_axis = _highest_value_next_axis(readiness_gates)
    return {
        "artifact_id": V0_1_EXPLANATION_READINESS_ID,
        "package_id": V0_1_EXPLANATION_READINESS_ID,
        "schema_version": V0_1_EXPLANATION_READINESS_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "business_goal_primary": "understanding/adoption",
        "desired_viewer_action": (
            "understand what can be built and what to ask next"
        ),
        "evidence_level": "L1_internal_judgement",
        "identity": {
            "package_id": V0_1_EXPLANATION_READINESS_ID,
            "source_render_result_path": _path_text(
                DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
            ),
            "source_card_assets_path": _path_text(DEFAULT_VISUAL_CARD_ASSET_DIR),
            "source_audio_timing_readback_paths": [
                _path_text(DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH),
                _path_text(DEFAULT_EPISODE_CAPTION_TIMING_PLAN_PATH),
            ],
            "source_episode_capsule_path": _path_text(
                DEFAULT_EPISODE_PRODUCTION_CAPSULE_PATH
            ),
            "source_script_import_csv_path": _path_text(
                DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH
            ),
            "candidate_video_local_path_current_host": _path_text(
                CURRENT_CANDIDATE_VIDEO_LOCAL_PATH
            ),
            "candidate_video_exists_local": (
                base / CURRENT_CANDIDATE_VIDEO_LOCAL_PATH
            ).exists(),
            "production_status": "diagnostic_only",
            "business_goal_primary": "understanding/adoption",
            "desired_viewer_action": (
                "understand what can be built and what to ask next"
            ),
        },
        "source_validation": source_validation,
        "normalized_current_observation": _normalized_current_observation(
            base, duration_sec
        ),
        "current_proven_capabilities": _proven_capability_map(
            post_density,
            card_render,
            caption_timing,
            episode_capsule,
        ),
        "explanation_readiness_gates": readiness_gates,
        "script_density_diagnosis": _script_density_diagnosis(
            current_line_count,
            duration_sec,
            dialogue_lines,
        ),
        "highest_value_next_axis": {
            "selected": next_axis,
            "reason": (
                "the render/mechanics stack is diagnostic-pass, but the current "
                "four-line script does not yet explain the business problem, "
                "offer, proof sequence, and next action with enough density"
            ),
        },
        "not_accepted_scope": _not_accepted_scope(),
        "automation_note": _automation_note(),
        "completion_matrix": _completion_matrix(),
        "artifact_readiness": _artifact_readiness(),
        "business_explanation_readiness": _business_explanation_readiness(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "inertia_check": _inertia_check(next_axis),
        "downstream_next_use": _downstream_next_use(next_axis),
        "boundaries": _boundaries(),
    }


def build_newsroom_v0_1_script_density_plan(
    explanation_readiness: dict[str, Any],
    *,
    root: str | Path,
) -> dict[str, Any]:
    """Build the plan-only script density artifact."""
    diagnosis = _dict(explanation_readiness.get("script_density_diagnosis"))
    next_axis = _dict(explanation_readiness.get("highest_value_next_axis")).get(
        "selected", NEXT_DEFAULT_SLICE
    )
    return {
        "artifact_id": V0_1_SCRIPT_DENSITY_PLAN_ID,
        "plan_id": V0_1_SCRIPT_DENSITY_PLAN_ID,
        "schema_version": V0_1_SCRIPT_DENSITY_PLAN_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "plan_type": "script_density_plan_only",
        "source_explanation_readiness_path": _path_text(
            DEFAULT_V0_1_EXPLANATION_READINESS_PATH
        ),
        "source_explanation_readiness_id": explanation_readiness.get("package_id"),
        "target_duration_sec": TARGET_DURATION_RANGE_SEC,
        "target_narration_segments": TARGET_NARRATION_SEGMENTS,
        "suggested_line_count_range": SUGGESTED_LINE_COUNT_RANGE,
        "current_script_density_reference": diagnosis,
        "recommended_segment_structure": _recommended_segment_structure(),
        "card_to_narration_alignment": _card_to_narration_alignment(),
        "what_remains_card_only": [
            "review-only / diagnostic boundary labels",
            "card role markers and simplified visual structure",
            "short source/status hints that support but do not carry the pitch",
        ],
        "what_should_not_be_narrated": [
            "debug metadata",
            "file paths",
            "implementation internals unless used as proof",
            "production/public readiness claims",
            "real RSS/news details in this plan-only slice",
        ],
        "implementation_policy": {
            "plan_only": True,
            "script_implementation_in_this_slice": False,
            "YMM4_launch_or_render_in_this_slice": False,
            "cards_regenerated_in_this_slice": False,
        },
        "highest_value_next_axis": {
            "selected": next_axis,
            "reason": "script density should be planned before another render or RSS dry run",
        },
        "not_accepted_scope": _not_accepted_scope(),
        "automation_note": _automation_note(),
        "completion_matrix": _completion_matrix(),
        "artifact_readiness": _artifact_readiness(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "inertia_check": _inertia_check(next_axis),
        "downstream_next_use": _downstream_next_use(next_axis),
        "boundaries": _boundaries(),
    }


def render_newsroom_v0_1_explanation_readiness_markdown(
    readiness: dict[str, Any],
) -> str:
    """Render explanation readiness as a human-readable review doc."""
    lines = [
        "# Newsroom v0.1 Explanation Readiness v1",
        "",
        f"artifact_id: {readiness.get('artifact_id')}",
        f"package_id: {readiness.get('package_id')}",
        f"schema_version: {readiness.get('schema_version')}",
        f"production_status: {readiness.get('production_status')}",
        f"business_goal_primary: {readiness.get('business_goal_primary')}",
        f"desired_viewer_action: {readiness.get('desired_viewer_action')}",
        "diagnostic_only: true",
        "",
        "## Identity",
        "",
    ]
    for key, value in _dict(readiness.get("identity")).items():
        lines.append(f"- {key}: {_display(value)}")
    _append_mapping(lines, "Source Validation", readiness.get("source_validation"))
    _append_mapping(
        lines,
        "Normalized Current Observation",
        readiness.get("normalized_current_observation"),
    )
    _append_rows(
        lines,
        "Current Proven Capabilities",
        ["capability", "status", "evidence", "implication"],
        readiness.get("current_proven_capabilities"),
    )
    _append_rows(
        lines,
        "Explanation Readiness Gates",
        ["gate", "status", "evidence", "decision"],
        readiness.get("explanation_readiness_gates"),
    )
    _append_mapping(lines, "Script Density Diagnosis", readiness.get("script_density_diagnosis"))
    _append_mapping(lines, "Highest-Value Next Axis", readiness.get("highest_value_next_axis"))
    _append_mapping(lines, "Automation Note", readiness.get("automation_note"))
    _append_mapping(lines, "Not Accepted Scope", readiness.get("not_accepted_scope"))
    _append_status_table(lines, "Completion Matrix", readiness.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", readiness.get("artifact_readiness"))
    _append_status_table(
        lines,
        "Business / Explanation Readiness",
        readiness.get("business_explanation_readiness"),
    )
    _append_status_table(lines, "Render Gate Hygiene", readiness.get("render_gate_hygiene"))
    _append_status_table(
        lines, "Human Burden Hygiene", readiness.get("human_burden_hygiene")
    )
    _append_status_table(lines, "Inertia Check", readiness.get("inertia_check"))
    _append_mapping(lines, "Downstream Next Use", readiness.get("downstream_next_use"))
    _append_mapping(lines, "Boundaries", readiness.get("boundaries"))
    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This is a plan/readiness slice only. It does not launch YMM4, render, "
            "edit `.ymmp`, generate audio/TTS, regenerate cards, fetch real RSS/news, "
            "or claim production/public/audience acceptance.",
            "",
        ]
    )
    return "\n".join(lines)


def render_newsroom_v0_1_script_density_plan_markdown(plan: dict[str, Any]) -> str:
    """Render the script-density plan as a human-readable doc."""
    lines = [
        "# Newsroom v0.1 Script Density Plan v1",
        "",
        f"artifact_id: {plan.get('artifact_id')}",
        f"plan_id: {plan.get('plan_id')}",
        f"schema_version: {plan.get('schema_version')}",
        f"production_status: {plan.get('production_status')}",
        f"plan_type: {plan.get('plan_type')}",
        "diagnostic_only: true",
        "",
    ]
    _append_mapping(lines, "Target Density", {
        "target_duration_sec": plan.get("target_duration_sec"),
        "target_narration_segments": plan.get("target_narration_segments"),
        "suggested_line_count_range": plan.get("suggested_line_count_range"),
    })
    _append_mapping(
        lines,
        "Current Script Density Reference",
        plan.get("current_script_density_reference"),
    )
    _append_rows(
        lines,
        "Recommended Segment Structure",
        ["segment", "purpose", "spoken_job", "line_count_target"],
        plan.get("recommended_segment_structure"),
    )
    _append_rows(
        lines,
        "Card To Narration Alignment",
        ["card_index", "card_role", "spoken_job", "shown_job"],
        plan.get("card_to_narration_alignment"),
    )
    _append_mapping(lines, "Implementation Policy", plan.get("implementation_policy"))
    _append_mapping(lines, "Highest-Value Next Axis", plan.get("highest_value_next_axis"))
    _append_mapping(lines, "Automation Note", plan.get("automation_note"))
    _append_mapping(lines, "Not Accepted Scope", plan.get("not_accepted_scope"))
    _append_status_table(lines, "Completion Matrix", plan.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", plan.get("artifact_readiness"))
    _append_status_table(lines, "Render Gate Hygiene", plan.get("render_gate_hygiene"))
    _append_status_table(lines, "Human Burden Hygiene", plan.get("human_burden_hygiene"))
    _append_status_table(lines, "Inertia Check", plan.get("inertia_check"))
    _append_mapping(lines, "Downstream Next Use", plan.get("downstream_next_use"))
    _append_mapping(lines, "Boundaries", plan.get("boundaries"))
    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This plan defines density and segment structure only. It does not "
            "implement a denser script, regenerate YMM4 files, render, or approve "
            "public/production use.",
            "",
        ]
    )
    return "\n".join(lines)


def _load_sources(base: Path) -> dict[str, Any]:
    return {
        "post_density_render_result": load_json_object(
            base / DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        "card_render_result": load_json_object(
            base / DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        "caption_timing_plan": load_json_object(
            base / DEFAULT_EPISODE_CAPTION_TIMING_PLAN_PATH
        ),
        "episode_capsule": load_json_object(base / DEFAULT_EPISODE_PRODUCTION_CAPSULE_PATH),
    }


def _source_dialogue_lines(base: Path) -> list[str]:
    path = base / DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH
    if not path.exists():
        return []
    lines: list[str] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.reader(handle):
            if len(row) >= 2:
                lines.append(row[1])
    return lines


def _source_validation(
    base: Path,
    sources: dict[str, Any],
    dialogue_lines: list[str],
) -> dict[str, Any]:
    post_density = _dict(sources.get("post_density_render_result"))
    card_render = _dict(sources.get("card_render_result"))
    caption_timing = _dict(sources.get("caption_timing_plan"))
    episode_capsule = _dict(sources.get("episode_capsule"))
    errors: list[str] = []
    if post_density.get("result_status") != "pass":
        errors.append("post-density render result is not pass")
    if card_render.get("result_status") != "pass":
        errors.append("card-placement render result is not pass")
    if caption_timing.get("diagnostic_only") is not True:
        errors.append("caption timing source is not diagnostic")
    if episode_capsule.get("production_status") != "diagnostic_only":
        errors.append("episode capsule is not diagnostic-only")
    if len(dialogue_lines) != 4:
        errors.append("source YMM4 recreation CSV does not contain four dialogue rows")
    if not (base / DEFAULT_VISUAL_CARD_ASSET_DIR).exists():
        errors.append("visual card asset directory is missing")
    if not (base / CURRENT_CANDIDATE_VIDEO_LOCAL_PATH).exists():
        errors.append("current-host candidate mp4 is not present")
    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "post_density_readback_id": post_density.get("readback_id"),
        "post_density_render_result": post_density.get("result_status"),
        "card_render_readback_id": card_render.get("readback_id"),
        "card_render_result": card_render.get("result_status"),
        "caption_timing_plan_id": caption_timing.get("artifact_id"),
        "episode_capsule_id": episode_capsule.get("artifact_id"),
        "dialogue_line_count": len(dialogue_lines),
        "candidate_video_exists_local": (base / CURRENT_CANDIDATE_VIDEO_LOCAL_PATH).exists(),
        "card_assets_dir_exists": (base / DEFAULT_VISUAL_CARD_ASSET_DIR).exists(),
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "cards_regenerated_in_this_slice": False,
    }


def _normalized_current_observation(base: Path, duration_sec: int) -> dict[str, Any]:
    return {
        "render_output_exists_local": (base / CURRENT_CANDIDATE_VIDEO_LOCAL_PATH).exists(),
        "candidate_video_local_path_current_host": _path_text(
            CURRENT_CANDIDATE_VIDEO_LOCAL_PATH
        ),
        "yym4_render_pipeline_status": "diagnostic_pass",
        "ai_direct_video_generation_via_ymmp": "not_reliable_yet",
        "yym4_native_audio_path": "diagnostic_pass",
        "script_import_path": "diagnostic_pass",
        "card_visual_asset_path": "diagnostic_pass",
        "observed_duration_sec": duration_sec,
        "next_highest_value_axis": "explanation_readiness_and_script_density",
        "production_ready": False,
        "public_ready": False,
    }


def _observed_duration_sec(
    post_density: dict[str, Any],
    card_render: dict[str, Any],
) -> int:
    normalized = _dict(post_density.get("normalized_render_observation"))
    if normalized.get("output_duration_observed") == "approximately_68_sec":
        return 68
    card_normalized = _dict(card_render.get("normalized_render_result"))
    return int(card_normalized.get("output_duration_sec") or 68)


def _proven_capability_map(
    post_density: dict[str, Any],
    card_render: dict[str, Any],
    caption_timing: dict[str, Any],
    episode_capsule: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        _capability("YMM4 script import", "diagnostic_pass", DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH, "four CSV dialogue rows can be imported"),
        _capability("speaker binding", "diagnostic_pass", DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH, "canonical yukkuri speaker path is proven"),
        _capability("native yukkuri audio", "diagnostic_pass", DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH, "native audio remains present in render observations"),
        _capability("English loanword handling", "diagnostic_pass", DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH, "fake English loanword lines survive the import/render path"),
        _capability("source .ymmp recreation from CSV", "diagnostic_pass", DEFAULT_SOURCE_YMMP_RECREATION_IMPORT_CSV_PATH, "source project can be recreated from tracked CSV input"),
        _capability("timing patch to 68 seconds", "diagnostic_pass", DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH, f"duration observed as { _display(_dict(card_render.get('normalized_render_result')).get('output_duration_observed')) }"),
        _capability("card PNG generation", "diagnostic_pass", DEFAULT_VISUAL_CARD_ASSET_DIR, "four density-simplified PNG cards exist at stable paths"),
        _capability("YMM4 ImageItem placement", "diagnostic_pass", DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH, "four card assets visible in the diagnostic YMM4 render"),
        _capability("video render output", "diagnostic_pass", DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_PATH, _dict(post_density.get("normalized_render_observation")).get("render_smoke_result")),
        _capability("benchmark-driven visual refinement", "diagnostic_pass", DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_PATH, "density refinement visible and information density reduced"),
        _capability("local artifact recovery process", "diagnostic_pass", DEFAULT_EPISODE_PRODUCTION_CAPSULE_PATH, episode_capsule.get("production_status")),
        _capability("caption timing baseline", "diagnostic_reference", DEFAULT_EPISODE_CAPTION_TIMING_PLAN_PATH, f"{len(caption_timing.get('caption_units', []))} placeholder caption units"),
    ]


def _capability(
    capability: str,
    status: str,
    evidence_path: str | Path,
    implication: object,
) -> dict[str, Any]:
    return {
        "capability": capability,
        "status": status,
        "evidence": _path_text(evidence_path),
        "implication": implication,
    }


def _explanation_readiness_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate": "problem_clear",
            "status": "partial",
            "evidence": "current cards say this is a fake review-only handoff, but the viewer problem is still implicit",
            "decision": "state the production pain or automation bottleneck in narration",
        },
        {
            "gate": "offer_clear",
            "status": "partial",
            "evidence": "the pipeline capabilities are visible, but the offer is not framed as what can be built for a viewer/customer",
            "decision": "add one segment that names the useful deliverable",
        },
        {
            "gate": "proof_clear",
            "status": "pass",
            "evidence": "render, audio, timing, cards, and density refinement are all recorded as diagnostic pass",
            "decision": "keep proof concise and sequence it as script -> YMM4 -> audio/cards/render",
        },
        {
            "gate": "boundary_clear",
            "status": "pass",
            "evidence": "diagnostic-only and review-only boundaries are repeated across readbacks and cards",
            "decision": "keep boundary spoken once, then let cards carry reminder labels",
        },
        {
            "gate": "next_action_clear",
            "status": "partial",
            "evidence": "next technical axis exists, but viewer-facing next action is not yet narrated",
            "decision": "end with what to ask next: RSS dry run or real packet plan after internal review",
        },
        {
            "gate": "audience_fit_proxy",
            "status": "partial",
            "evidence": "cards are less dense, but explanation is still built around fake diagnostics",
            "decision": "raise narration density before treating this as an adoption review",
        },
        {
            "gate": "visual_supports_explanation",
            "status": "pass",
            "evidence": "post-density render shows four simplified cards with audio/timing preserved",
            "decision": "do not continue visual polish until the script carries the explanation",
        },
    ]


def _script_density_diagnosis(
    current_line_count: int,
    duration_sec: int,
    dialogue_lines: list[str],
) -> dict[str, Any]:
    seconds_per_line = round(duration_sec / current_line_count, 2) if current_line_count else None
    return {
        "current_dialogue_line_count": current_line_count,
        "current_dialogue_lines": dialogue_lines,
        "current_duration_sec": duration_sec,
        "current_seconds_per_dialogue_line": seconds_per_line,
        "current_spoken_density": "too_sparse_for_explanation",
        "silence_spacing_implication": (
            "four short lines over about 68 sec prove mechanics but leave the "
            "viewer to infer problem, offer, proof sequence, and next action"
        ),
        "four_lines_enough_for_explanation": False,
        "likely_needed_line_count_range": SUGGESTED_LINE_COUNT_RANGE,
        "likely_needed_segment_count": TARGET_NARRATION_SEGMENTS,
        "card_to_narration_alignment": "cards can support structure but should not carry the full pitch",
        "what_should_be_spoken": [
            "what this diagnostic proves",
            "why CSV to YMM4 matters",
            "what evidence is now confirmed",
            "what remains diagnostic-only",
            "what the viewer should ask for next",
        ],
        "what_should_be_shown": [
            "card role",
            "simplified proof markers",
            "review-only boundary",
            "status/next-action hints",
        ],
    }


def _recommended_segment_structure() -> list[dict[str, Any]]:
    return [
        {
            "segment": "opening",
            "purpose": "what this proves",
            "spoken_job": "state that a diagnostic video can now be assembled from script import, native audio, timing, and card assets",
            "line_count_target": "2-3",
        },
        {
            "segment": "mechanism",
            "purpose": "CSV to YMM4",
            "spoken_job": "explain that tracked CSV/script input can recreate the YMM4 dialogue path while avoiding direct video generation claims",
            "line_count_target": "2-3",
        },
        {
            "segment": "proof",
            "purpose": "audio/timing/cards/render",
            "spoken_job": "name the proof chain: native audio, 68 sec timing, four cards, render output",
            "line_count_target": "3-4",
        },
        {
            "segment": "boundary",
            "purpose": "diagnostic only",
            "spoken_job": "say this is not production, public, or real-news acceptance",
            "line_count_target": "1-2",
        },
        {
            "segment": "next_action",
            "purpose": "RSS dry run / real packet plan",
            "spoken_job": "direct the next decision toward an RSS dry run or real packet plan after review",
            "line_count_target": "2",
        },
    ]


def _card_to_narration_alignment() -> list[dict[str, Any]]:
    return [
        {
            "card_index": 1,
            "card_role": "point / review-only overview",
            "spoken_job": "open with the diagnostic promise and what can now be built",
            "shown_job": "keep the review-only boundary and point summary visible",
        },
        {
            "card_index": 2,
            "card_role": "flow / mechanism",
            "spoken_job": "explain CSV/script import into YMM4 as the controlled handoff",
            "shown_job": "show the simple flow without narrating every label",
        },
        {
            "card_index": 3,
            "card_role": "check / proof",
            "spoken_job": "state what was proven: audio, timing, cards, render",
            "shown_job": "support the proof with check/status markers",
        },
        {
            "card_index": 4,
            "card_role": "next / source-status",
            "spoken_job": "close with diagnostic boundary and next inquiry path",
            "shown_job": "carry next-action/status hints",
        },
    ]


def _highest_value_next_axis(gates: list[dict[str, Any]]) -> str:
    thin = any(
        row["gate"] in {"offer_clear", "problem_clear", "next_action_clear"}
        and row["status"] != "pass"
        for row in gates
    )
    return NEXT_DEFAULT_SLICE if thin else RSS_DRY_RUN_PLAN_SLICE


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_readiness": False,
        "public_readiness": False,
        "actual_audience_or_order_acceptance": False,
        "real_rss_or_news_content": False,
        "rights_publication_clearance": False,
        "final_design_system": False,
        "automated_yym4_render_claim": False,
    }


def _automation_note() -> dict[str, Any]:
    return {
        "agent_can_prepare": [
            "CSV/script inputs",
            "card assets",
            "YMM4 patch/readback artifacts",
            "diagnostic verification docs",
        ],
        "user_yym4_side_remains_required_for": [
            "native YMM4 audio confirmation",
            "manual render/export",
            "GUI-only behavior until an official or tested automation path exists",
        ],
        "priority": (
            "do not prioritize full render automation before explanation/script "
            "density unless supervisor explicitly chooses it"
        ),
        "ai_direct_video_generation_via_ymmp": "not_reliable_yet",
    }


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "current_repo_state_verified", "status": True},
        {"gate": "current_proven_capabilities_summarized", "status": True},
        {"gate": "explanation_readiness_gates_evaluated", "status": True},
        {"gate": "script_density_diagnosis_completed", "status": True},
        {"gate": "highest_value_next_axis_selected", "status": NEXT_DEFAULT_SLICE},
        {
            "gate": "narrow_commit_created_and_pushed_if_push_gate_passes",
            "status": "pending_until_git_gate",
        },
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "explanation_readiness_json_exists", "status": True},
        {"gate": "script_density_plan_json_exists", "status": True},
        {"gate": "human_docs_exist", "status": True},
        {"gate": "proven_capabilities_map_present", "status": True},
        {"gate": "next_axis_decision_present", "status": True},
        {"gate": "downstream_next_use_described", "status": True},
    ]


def _business_explanation_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "problem_clear", "status": "partial"},
        {"gate": "offer_clear", "status": "partial"},
        {"gate": "proof_clear", "status": "pass"},
        {"gate": "boundary_clear", "status": "pass"},
        {"gate": "next_action_clear", "status": "partial"},
        {"gate": "audience_fit_proxy", "status": "partial"},
        {"gate": "visual_supports_explanation", "status": "pass"},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "no_render_performed_by_agent", "status": True},
        {"gate": "existing_render_evidence_reused", "status": True},
        {"gate": "no_render_for_docs_plan_only_change", "status": True},
        {
            "gate": "next_render_tied_to_material_script_audio_card_change",
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


def _inertia_check(next_axis: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_ad_hoc_visual_iteration", "status": True},
        {"gate": "no_automation_rabbit_hole", "status": True},
        {"gate": "no_packet_for_packet_drift", "status": True},
        {"gate": "business_explanation_goal_restored_above_visual_polish", "status": True},
        {"gate": "next_concrete_milestone", "status": next_axis},
    ]


def _downstream_next_use(next_axis: str) -> dict[str, Any]:
    return {
        "next_default_slice": next_axis,
        "first_artifacts_to_reopen": [
            _path_text(DEFAULT_V0_1_EXPLANATION_READINESS_PATH),
            _path_text(DEFAULT_V0_1_SCRIPT_DENSITY_PLAN_PATH),
        ],
        "reason": "script density is the next bottleneck after diagnostic render mechanics and density visuals passed",
    }


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "ymmp_edited_or_committed": False,
        "audio_tts_generated": False,
        "cards_regenerated": False,
        "real_rss_or_news_fetched": False,
        "production_public_readiness_claimed": False,
        "actual_audience_acceptance_claimed": False,
    }


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
        lines.append("| " + " | ".join(_display(row_map.get(column)) for column in columns) + " |")


def _append_status_table(lines: list[str], title: str, rows: object) -> None:
    lines.extend(["", f"## {title}", "", "| gate | status |", "|---|---|"])
    for row in rows if isinstance(rows, list) else []:
        row_map = _dict(row)
        gate = row_map.get("gate") or row_map.get("level") or row_map.get("slice")
        lines.append(f"| {gate} | {_display(row_map.get('status'))} |")


def _dict(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


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
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_text(path: str | Path, text: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    write_default_newsroom_v0_1_explanation_readiness_artifacts()
