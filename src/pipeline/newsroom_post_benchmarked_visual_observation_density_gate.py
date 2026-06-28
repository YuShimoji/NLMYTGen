"""Record the post-benchmarked newsroom visual density gate.

This slice consumes a user freeform observation with screenshot support. It
does not launch YMM4, render video, regenerate card assets, edit .ymmp files,
generate audio/TTS, fetch external media, or claim production/public readiness.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_audience_fit_benchmark_evaluation import (
    DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_visual_audience_fit_benchmark import (
    DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH,
)
from src.pipeline.newsroom_visual_card_asset_bridge import DEFAULT_VISUAL_CARD_ASSET_DIR
from src.pipeline.newsroom_visual_card_benchmarked_refinement import (
    DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH,
)


POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_SCHEMA_VERSION = (
    "newsroom_post_benchmarked_visual_observation_density_gate.v1"
)
POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_ID = (
    "newsroom_post_benchmarked_visual_observation_density_gate_v1_2026_06_26"
)

DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "post_benchmarked_visual_observation_density_gate_v1.json"
)
DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_V1_2026-06-26.md"
)

NORMALIZED_NEXT_AXIS = "visual_information_density_gate"
RECOMMENDED_NEXT_AXIS = "newsroom-visual-density-simplification-spec-v1"
ALTERNATIVE_NEXT_AXIS = "newsroom-visual-information-density-benchmark-v1"
FOLLOW_ON_REFINEMENT_SLICE = "newsroom-visual-card-density-benchmarked-refinement-v1"
OPERATOR_REVIEW_SLICE = "newsroom-internal-review-v0.1-operator-review-card"

USER_OBSERVATION_SUMMARY = (
    "User observed that the four cards and slow yukkuri/native voice remain "
    "intact, but automatic wrapping can create unexpected five-line rendering, "
    "small text pushes close to box edges, format detail competes with content, "
    "and the overall information density is high enough to require sustained "
    "concentration even in a work presentation context."
)

USER_SCREENSHOT_BASENAMES = (
    "スクリーンショット 2026-06-28 140233.png",
    "スクリーンショット 2026-06-28 140244.png",
    "スクリーンショット 2026-06-28 140255.png",
    "スクリーンショット 2026-06-28 140308.png",
)


def build_default_newsroom_post_benchmarked_visual_observation_density_gate(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the density gate readback from current benchmark artifacts."""
    base = Path(root) if root is not None else Path(".")
    benchmarked_refinement = load_json_object(
        base / DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH
    )
    benchmark_evaluation = load_json_object(
        base / DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH
    )
    visual_benchmark = load_json_object(
        base / DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH
    )
    card_inventory = _card_asset_inventory(base, base / DEFAULT_VISUAL_CARD_ASSET_DIR)
    source_validation = _source_validation(
        base=base,
        benchmarked_refinement=benchmarked_refinement,
        benchmark_evaluation=benchmark_evaluation,
        visual_benchmark=visual_benchmark,
        card_inventory=card_inventory,
    )
    mechanics_status = "pass" if source_validation["status"] == "passed" else "blocked"
    return {
        "artifact_id": POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_ID,
        "readback_id": POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_ID,
        "schema_version": (
            POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_SCHEMA_VERSION
        ),
        "observation_status": "visual_density_issue_confirmed",
        "mechanics_status": mechanics_status,
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "visual_work_class": "audience_fit",
        "observation_source": "user_freeform_with_screenshot_support",
        "evidence_level": [
            "user_freeform_visual_observation",
            "user_supplied_yym4_screenshots",
            "existing_benchmark_readbacks",
        ],
        "audience_acceptance_claimed": False,
        "production_visual_quality_accepted": False,
        "public_video_ready": False,
        "recommended_next_axis": NORMALIZED_NEXT_AXIS,
        "card_assets_visible": True,
        "native_audio_present": True,
        "dialogue_item_count_preserved": True,
        "rendered_line_count_mismatch_warning": True,
        "text_fit_tight_warning": True,
        "source_or_small_text_tightness_warning": True,
        "manual_edit_quality_minor_issue": True,
        "format_attention_over_content": True,
        "bbc_like_surface_signal": True,
        "information_density_high": True,
        "cognitive_load_high": True,
        "identity": {
            "readback_id": POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_ID,
            "source_benchmarked_refinement_path": _path_text(
                DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH
            ),
            "source_benchmarked_refinement_id": benchmarked_refinement.get(
                "refinement_id"
            ),
            "source_benchmark_evaluation_path": _path_text(
                DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH
            ),
            "source_benchmark_evaluation_id": benchmark_evaluation.get(
                "evaluation_id"
            ),
            "source_visual_benchmark_path": _path_text(
                DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH
            ),
            "source_visual_benchmark_id": visual_benchmark.get("benchmark_id"),
            "source_cards_dir": _path_text(DEFAULT_VISUAL_CARD_ASSET_DIR),
            "production_status": "diagnostic_only",
            "visual_work_class": "audience_fit",
            "observation_source": "user_freeform_with_screenshot_support",
            "audience_acceptance_claimed": False,
        },
        "source_validation": source_validation,
        "user_observation": {
            "source": "user_freeform",
            "summary": USER_OBSERVATION_SUMMARY,
            "normalized_once": True,
            "template_required": False,
            "schema_owner": "Agent",
        },
        "screenshot_support": {
            "source": "user_supplied_screenshots",
            "count": len(USER_SCREENSHOT_BASENAMES),
            "basenames": list(USER_SCREENSHOT_BASENAMES),
            "observed_surface": "YMM4_v4_53_0_9_preview_and_timeline",
            "observed_project_name": "diagnostic_bound_speaker_probe_card_placement_v1",
            "observed_card_range": "CARD 1/4 through CARD 4/4",
            "observed_duration": "00:01:08.00",
        },
        "card_asset_inventory": card_inventory,
        "mechanics_preservation": _mechanics_preservation(),
        "visual_findings": _visual_findings(),
        "benchmark_impact": _benchmark_impact(),
        "decision": _decision(),
        "accepted_scope": _accepted_scope(),
        "not_accepted_scope": _not_accepted_scope(),
        "recommended_next_slice": _recommended_next_slice(),
        "recommended_next_slices": _recommended_next_slices(),
        "goal_stack": _goal_stack(),
        "completion_matrix": _completion_matrix(),
        "artifact_readiness": _artifact_readiness(),
        "visual_gate": _visual_gate(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(),
        "downstream_next_use": _downstream_next_use(),
        "push_gate_policy": _push_gate_policy(),
        "boundaries": _boundaries(),
    }


def write_default_newsroom_post_benchmarked_visual_observation_density_gate_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write the density gate JSON and verification document."""
    base = Path(root) if root is not None else Path(".")
    gate = build_default_newsroom_post_benchmarked_visual_observation_density_gate(
        root=base
    )
    _write_json(
        base / DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH,
        gate,
    )
    _write_text(
        base / DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_DOC_PATH,
        render_newsroom_post_benchmarked_visual_observation_density_gate_markdown(
            gate
        ),
    )
    return gate


def render_newsroom_post_benchmarked_visual_observation_density_gate_markdown(
    gate: dict[str, Any],
) -> str:
    """Render a compact human readback for the density gate."""
    lines = [
        "# Newsroom Post-Benchmarked Visual Observation Density Gate v1",
        "",
        f"artifact_id: {gate['artifact_id']}",
        f"readback_id: {gate['readback_id']}",
        f"schema_version: {gate['schema_version']}",
        f"observation_status: {gate['observation_status']}",
        f"mechanics_status: {gate['mechanics_status']}",
        f"production_status: {gate['production_status']}",
        "",
        "## Outcome",
        "",
        (
            "The post-benchmarked observation preserves the video mechanics "
            "surface while changing the next visual problem from local text-fit "
            "repair to information density and cognitive load. This is a "
            "readback and gate-setting artifact, not a card redesign, render, "
            "or production/public/audience acceptance result."
        ),
        "",
        "## Identity",
        "",
    ]
    _append_key_values(lines, gate["identity"])
    lines.extend(["", "## User Observation", ""])
    _append_key_values(lines, gate["user_observation"])
    lines.extend(["", "## Screenshot Support", ""])
    _append_key_values(lines, gate["screenshot_support"])
    lines.extend(["", "## Mechanics Preservation", ""])
    _append_key_values(lines, gate["mechanics_preservation"])
    lines.extend(["", "## Visual Findings", ""])
    _append_key_values(lines, gate["visual_findings"])
    lines.extend(
        [
            "",
            "## Benchmark Impact",
            "",
            "| metric | result | impact |",
            "|---|---|---|",
        ]
    )
    for metric_id, row in gate["benchmark_impact"].items():
        lines.append(f"| {metric_id} | {row['result']} | {row['impact']} |")
    lines.extend(["", "## Decision", ""])
    _append_key_values(lines, gate["decision"])
    lines.extend(["", "## Accepted Scope", ""])
    _append_key_values(lines, gate["accepted_scope"])
    lines.extend(["", "## Not Accepted Scope", ""])
    _append_key_values(lines, gate["not_accepted_scope"])
    lines.extend(["", "## Recommended Next Slice", ""])
    _append_key_values(lines, gate["recommended_next_slice"])
    lines.extend(
        [
            "",
            "## Recommended Next Slices",
            "",
            "| slice | timing | reason |",
            "|---|---|---|",
        ]
    )
    for row in gate["recommended_next_slices"]:
        lines.append(f"| {row['slice']} | {row['timing']} | {row['reason']} |")
    lines.extend(
        [
            "",
            "## Goal Stack",
            "",
            "| level | goal | success signal | contribution |",
            "|---|---|---|---|",
        ]
    )
    for row in gate["goal_stack"]:
        lines.append(
            "| "
            f"{row['level']} | "
            f"{row['goal']} | "
            f"{row['success_signal']} | "
            f"{row['contribution']} |"
        )
    _append_status_table(lines, "Completion Matrix", gate["completion_matrix"])
    _append_status_table(lines, "Artifact Readiness", gate["artifact_readiness"])
    _append_status_table(lines, "Visual Gate", gate["visual_gate"])
    _append_status_table(lines, "Render Gate Hygiene", gate["render_gate_hygiene"])
    _append_status_table(lines, "Human Burden Hygiene", gate["human_burden_hygiene"])
    _append_status_table(lines, "Review Non-Redundancy", gate["review_non_redundancy"])
    _append_status_table(lines, "Inertia Check", gate["inertia_check"])
    lines.extend(["", "## Downstream Next Use", ""])
    _append_key_values(lines, gate["downstream_next_use"])
    lines.extend(["", "## Boundaries", ""])
    _append_key_values(lines, gate["boundaries"])
    return "\n".join(lines) + "\n"


def _source_validation(
    *,
    base: Path,
    benchmarked_refinement: dict[str, Any],
    benchmark_evaluation: dict[str, Any],
    visual_benchmark: dict[str, Any],
    card_inventory: dict[str, Any],
) -> dict[str, Any]:
    expected_paths = [
        DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH,
        DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH,
        DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH,
    ]
    errors: list[str] = [
        f"SOURCE_PATH_MISSING:{_path_text(path)}"
        for path in expected_paths
        if not (base / path).exists()
    ]
    if benchmarked_refinement.get("refinement_status") != (
        "benchmarked_text_fit_improved"
    ):
        errors.append("BENCHMARKED_REFINEMENT_NOT_IMPROVED")
    if benchmarked_refinement.get("production_status") != "diagnostic_only":
        errors.append("BENCHMARKED_REFINEMENT_NOT_DIAGNOSTIC")
    if benchmark_evaluation.get("evaluation_status") not in {
        "material_proxy_failures_found",
        "applied",
    }:
        errors.append("BENCHMARK_EVALUATION_STATUS_UNEXPECTED")
    if visual_benchmark.get("benchmark_status") != "draft_proxy_benchmark_defined":
        errors.append("VISUAL_BENCHMARK_STATUS_UNEXPECTED")
    if card_inventory["svg_count"] != 4 or card_inventory["png_count"] != 4:
        errors.append("VISUAL_CARD_ASSET_COUNT_NOT_4")
    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "source_ids": {
            "benchmarked_refinement_id": benchmarked_refinement.get("refinement_id"),
            "benchmark_evaluation_id": benchmark_evaluation.get("evaluation_id"),
            "visual_benchmark_id": visual_benchmark.get("benchmark_id"),
        },
        "card_asset_counts": {
            "svg": card_inventory["svg_count"],
            "png": card_inventory["png_count"],
        },
    }


def _card_asset_inventory(base: Path, asset_dir: Path) -> dict[str, Any]:
    svg_files = sorted(asset_dir.glob("*.svg")) if asset_dir.exists() else []
    png_files = sorted(asset_dir.glob("*.png")) if asset_dir.exists() else []
    return {
        "asset_dir": _repo_path(base, asset_dir),
        "svg_count": len(svg_files),
        "png_count": len(png_files),
        "svg_paths": [_repo_path(base, path) for path in svg_files],
        "png_paths": [_repo_path(base, path) for path in png_files],
        "stable_paths_preserved": len(svg_files) == 4 and len(png_files) == 4,
    }


def _mechanics_preservation() -> dict[str, Any]:
    return {
        "card_assets_visible": True,
        "native_audio_present": True,
        "dialogue_items_preserved": True,
        "dialogue_item_count_preserved": True,
        "timing_or_duration_regression_reported": False,
        "render_or_preview_context": "user_observed_YMM4_surface",
        "production_ready": False,
        "source": "user_freeform_observation_with_screenshot_support",
    }


def _visual_findings() -> dict[str, Any]:
    return {
        "rendered_line_count_mismatch_warning": True,
        "text_fit_tight_warning": True,
        "source_or_small_text_tightness_warning": True,
        "manual_edit_quality_minor_issue": True,
        "format_attention_over_content": True,
        "bbc_like_surface_signal": True,
        "information_density_high": True,
        "cognitive_load_high": True,
        "issue_class": "visual_information_density_gate",
        "not_a_local_clipping_only_issue": True,
    }


def _benchmark_impact() -> dict[str, dict[str, str]]:
    return {
        "readability_at_a_glance": {
            "result": "warning",
            "impact": "requires sustained concentration despite mechanics pass",
        },
        "text_clipping_or_wrapping": {
            "result": "improved_but_tight",
            "impact": "previous hard failure improved, but line wrapping can still surprise",
        },
        "no_reliance_on_tiny_metadata": {
            "result": "warning",
            "impact": "small/source text and tight boxes attract attention",
        },
        "pacing_density_for_68_sec_video": {
            "result": "fail",
            "impact": "information load is too high for relaxed 68 sec viewing",
        },
        "familiar_explainer_visual_grammar": {
            "result": "mixed",
            "impact": "surface is familiar but format polish can compete with content",
        },
        "one_dominant_message_per_card": {
            "result": "warning",
            "impact": "format detail competes with the dominant message",
        },
        "actual_audience_acceptance": {
            "result": "unknown",
            "impact": "no live audience, retention, CTR, or target viewer evidence",
        },
    }


def _decision() -> dict[str, Any]:
    return {
        "normalized_next_axis": NORMALIZED_NEXT_AXIS,
        "recommended_next_axis": RECOMMENDED_NEXT_AXIS,
        "alternative_next_axis": ALTERNATIVE_NEXT_AXIS,
        "follow_on_refinement_slice": FOLLOW_ON_REFINEMENT_SLICE,
        "reason": [
            "the issue is not a local clipping bug only",
            "the issue is cognitive load and information density",
            "another card style tweak without density criteria would restart ad hoc iteration",
        ],
        "redesign_now": False,
        "render_now": False,
    }


def _accepted_scope() -> dict[str, bool]:
    return {
        "post_benchmarked_cards_visible": True,
        "audio_preserved": True,
        "benchmarked_text_fit_refinement_exposed_next_issue": True,
        "next_visual_issue_is_density_or_cognitive_load": True,
        "freeform_observation_normalized_once": True,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "production_visual_quality": False,
        "actual_audience_acceptance": False,
        "final_design_system": False,
        "retention_or_ctr_prediction": False,
        "real_newsroom_visual_acceptance": False,
        "public_readiness": False,
        "production_approval": False,
    }


def _recommended_next_slice() -> dict[str, Any]:
    return {
        "slice": RECOMMENDED_NEXT_AXIS,
        "reason": (
            "define density and simplification criteria before changing cards again"
        ),
        "user_side_work": "none_for_this_slice",
    }


def _recommended_next_slices() -> list[dict[str, str]]:
    return [
        {
            "slice": RECOMMENDED_NEXT_AXIS,
            "timing": "default_next",
            "reason": "current concern is information density and cognitive load",
        },
        {
            "slice": ALTERNATIVE_NEXT_AXIS,
            "timing": "if_existing_benchmark_density_criteria_are_insufficient",
            "reason": "upgrade the benchmark before applying another visual change",
        },
        {
            "slice": FOLLOW_ON_REFINEMENT_SLICE,
            "timing": "after_density_spec_or_sufficient_existing_criteria",
            "reason": "only then change the cards against density criteria",
        },
        {
            "slice": OPERATOR_REVIEW_SLICE,
            "timing": "only_if_supervisor_accepts_current_density_for_diagnostic_review",
            "reason": "do not ask for repeated review while density remains the named issue",
        },
    ]


def _goal_stack() -> list[dict[str, str]]:
    return [
        {
            "level": "Immediate",
            "goal": "Record latest post-benchmarked observation",
            "success_signal": "JSON/doc capture mechanics pass and density issue",
            "contribution": "prevents repeated informal review",
        },
        {
            "level": "Short-term",
            "goal": "Stop ad hoc visual tweaking",
            "success_signal": "next axis becomes density spec, not broad style change",
            "contribution": "keeps benchmark discipline",
        },
        {
            "level": "Mid-term",
            "goal": "Reduce cognitive load deliberately",
            "success_signal": "future refinement can remove/merge information using criteria",
            "contribution": "improves reviewability",
        },
        {
            "level": "Long-term",
            "goal": "Establish reusable card density baseline",
            "success_signal": "future RSS/content videos can use clearer card rules",
            "contribution": "supports automation",
        },
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"item": "current_repo_state_verified", "status": True},
        {"item": "latest_observation_normalized", "status": True},
        {"item": "benchmark_impact_mapped", "status": True},
        {"item": "density_cognitive_load_next_axis_selected", "status": True},
        {"item": "readback_json_doc_created", "status": True},
        {
            "item": "narrow_commit_created_and_pushed_if_push_gate_passes",
            "status": "agent_followthrough_after_validation",
        },
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"item": "readback_json_exists", "status": True},
        {"item": "human_doc_exists", "status": True},
        {"item": "mechanics_preservation_present", "status": True},
        {"item": "visual_findings_present", "status": True},
        {"item": "benchmark_impact_present", "status": True},
        {"item": "downstream_next_use_described", "status": True},
    ]


def _visual_gate() -> list[dict[str, Any]]:
    return [
        {"item": "latest_observation_consumed_once", "status": True},
        {"item": "benchmark_metrics_reused", "status": True},
        {"item": "density_cognitive_load_issue_identified", "status": True},
        {"item": "actual_audience_acceptance_not_claimed", "status": True},
        {"item": "unknowns_preserved", "status": True},
        {"item": "no_redesign_performed", "status": True},
        {"item": "next_axis_criteria_spec_linked", "status": True},
        {"item": "review_protocol_remains_bounded", "status": True},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"item": "no_render_performed_by_agent", "status": True},
        {"item": "existing_user_observation_consumed_once", "status": True},
        {"item": "no_render_for_docs_readback_only_change", "status": True},
        {
            "item": "next_render_tied_to_material_density_spec_linked_change",
            "status": True,
        },
        {"item": "repeated_render_loop_avoided", "status": True},
        {"item": "output_first_principle_preserved", "status": True},
    ]


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"item": "user_input_freeform", "status": True},
        {"item": "template_required_false", "status": True},
        {"item": "schema_owner_agent", "status": True},
        {"item": "user_side_work_none_for_this_slice", "status": True},
        {"item": "future_review_look_for_lte_3", "status": True},
        {"item": "no_negative_confirmation_checklist", "status": True},
        {"item": "no_fixed_form_relapse", "status": True},
    ]


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"item": "latest_observation_consumed_once", "status": True},
        {"item": "benchmark_evaluation_reused", "status": True},
        {"item": "next_axis_density_cognitive_load", "status": True},
        {"item": "not_accepted_scope_preserved", "status": True},
        {"item": "no_repeated_user_review_requested", "status": True},
        {"item": "no_mechanics_re_review_requested", "status": True},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"item": "no_ad_hoc_visual_iteration", "status": True},
        {"item": "no_broad_redesign", "status": True},
        {"item": "no_packet_for_packet_drift", "status": True},
        {"item": "readiness_separated_from_slice_completion", "status": True},
        {"item": "next_concrete_criteria_linked_milestone_named", "status": True},
    ]


def _downstream_next_use() -> dict[str, Any]:
    return {
        "default_next_slice": RECOMMENDED_NEXT_AXIS,
        "instruction": (
            "further visual work must target information density and cognitive load "
            "explicitly before another card surface change"
        ),
        "allowed_change_axis": [
            "density or simplification criteria",
            "benchmark upgrade if density criteria are insufficient",
            "later density-benchmarked card refinement",
        ],
        "disallowed_change_axis": [
            "broad style tweak",
            "repeated render request",
            "YMM4 or .ymmp work for this docs/readback-only gate",
            "audio/TTS generation",
            "production/public/audience acceptance claim",
        ],
    }


def _push_gate_policy() -> dict[str, Any]:
    return {
        "commit_message": "docs: record newsroom visual density gate",
        "force_push_allowed": False,
        "forbidden_staged_outputs": [
            ".ymmp",
            ".mp4",
            ".wav",
            ".mp3",
            ".m4a",
            "render output",
            "TTS output",
            "external media",
        ],
    }


def _boundaries() -> dict[str, bool]:
    return {
        "diagnostic_only": True,
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "ymmp_edited_or_committed": False,
        "svg_png_cards_regenerated": False,
        "audio_tts_or_voice_cache_created": False,
        "external_fetch_performed": False,
        "fixed_review_form_requested": False,
        "production_approval": False,
        "audience_acceptance_claimed": False,
        "public_video_ready": False,
    }


def _append_key_values(lines: list[str], value: dict[str, Any]) -> None:
    for key, item in value.items():
        lines.append(f"- {key}: {_display(item)}")


def _append_status_table(
    lines: list[str], title: str, rows: list[dict[str, Any]]
) -> None:
    lines.extend(["", f"## {title}", "", "| item | status |", "|---|---|"])
    for row in rows:
        lines.append(f"| {row['item']} | {_display(row['status'])} |")


def _display(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(_display(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _repo_path(base: Path, path: Path) -> str:
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: str | Path, text: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _path_text(path: str | Path) -> str:
    return Path(path).as_posix()
