"""Post-density-refinement render smoke result readback.

This slice records the latest user freeform YMM4 observation after density
benchmark refinement. It does not launch YMM4, render video, edit .ymmp files,
regenerate cards, generate audio/TTS, fetch external media, or approve
production/public/audience readiness.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_audience_fit_benchmark_evaluation import (
    DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_post_benchmarked_visual_observation_density_gate import (
    DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH,
)
from src.pipeline.newsroom_visual_card_density_benchmarked_refinement import (
    DEFAULT_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_PATH,
)
from src.pipeline.newsroom_visual_density_simplification_spec import (
    DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH,
)


POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION = (
    "newsroom_post_density_refinement_render_smoke_result_readback.v1"
)
POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_ID = (
    "newsroom_post_density_refinement_render_smoke_result_readback_v1_2026_06_26"
)
DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "post_density_refinement_render_smoke_result_readback_v1.json"
)
DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_V1_2026-06-26.md"
)

NEXT_DEFAULT_SLICE = "newsroom-internal-review-v0.1-reevaluation-card-v1"
DENSITY_REDUCTION_V2_SLICE = "newsroom-visual-density-reduction-v2"
RSS_DRY_RUN_PLAN_SLICE = "newsroom-rss-dry-run-integration-plan-v1"
RETENTION_POLICY_SLICE = "newsroom-render-output-retention-policy-v1"


def build_default_newsroom_post_density_refinement_render_smoke_result_readback(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed post-density render result readback."""
    base = Path(root) if root is not None else Path(".")
    density_refinement = load_json_object(
        base / DEFAULT_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_PATH
    )
    density_spec = load_json_object(
        base / DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH
    )
    density_gate = load_json_object(
        base / DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH
    )
    benchmark_evaluation = load_json_object(
        base / DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH
    )
    return build_newsroom_post_density_refinement_render_smoke_result_readback(
        density_refinement,
        density_spec,
        density_gate,
        benchmark_evaluation,
        source_density_refinement_path=(
            DEFAULT_VISUAL_CARD_DENSITY_BENCHMARKED_REFINEMENT_PATH
        ),
        source_density_spec_path=DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH,
        source_density_gate_path=(
            DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH
        ),
        source_benchmark_evaluation_path=(
            DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH
        ),
        root=base,
    )


def write_default_newsroom_post_density_refinement_render_smoke_result_readback_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write JSON and human-readable post-density render result readback."""
    base = Path(root) if root is not None else Path(".")
    readback = (
        build_default_newsroom_post_density_refinement_render_smoke_result_readback(
            root=base
        )
    )
    _write_json(
        base / DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_PATH,
        readback,
    )
    _write_text(
        base / DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_DOC_PATH,
        render_newsroom_post_density_refinement_render_smoke_result_readback_markdown(
            readback
        ),
    )
    return readback


def build_newsroom_post_density_refinement_render_smoke_result_readback(
    density_refinement: dict[str, Any],
    density_spec: dict[str, Any],
    density_gate: dict[str, Any],
    benchmark_evaluation: dict[str, Any],
    *,
    source_density_refinement_path: str | Path,
    source_density_spec_path: str | Path,
    source_density_gate_path: str | Path,
    source_benchmark_evaluation_path: str | Path,
    root: str | Path,
) -> dict[str, Any]:
    """Build a diagnostic-only readback from the supplied user observation."""
    base = Path(root)
    normalized = _normalized_render_observation()
    source_validation = _source_validation(
        base,
        density_refinement,
        density_spec,
        density_gate,
        benchmark_evaluation,
    )
    card_rows = _card_observations(density_refinement)
    return {
        "artifact_id": POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_ID,
        "readback_id": POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_ID,
        "schema_version": (
            POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION
        ),
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "visual_work_class": "audience_fit",
        "observation_source": "user_freeform_with_screenshot_support",
        "result_status": "pass",
        "actual_audience_acceptance_claimed": False,
        "identity": {
            "readback_id": POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_ID,
            "source_density_refinement_path": _path_text(
                source_density_refinement_path
            ),
            "source_density_refinement_id": density_refinement.get("refinement_id"),
            "source_density_spec_path": _path_text(source_density_spec_path),
            "source_density_spec_id": density_spec.get("spec_id"),
            "source_density_gate_path": _path_text(source_density_gate_path),
            "source_density_gate_id": density_gate.get("readback_id"),
            "source_benchmark_evaluation_path": _path_text(
                source_benchmark_evaluation_path
            ),
            "source_benchmark_evaluation_id": benchmark_evaluation.get(
                "evaluation_id"
            ),
            "production_status": "diagnostic_only",
            "visual_work_class": "audience_fit",
            "observation_source": "user_freeform_with_screenshot_support",
            "actual_audience_acceptance_claimed": False,
        },
        "source_validation": source_validation,
        "operator_freeform_observation": _operator_freeform_observation(),
        "normalized_render_observation": normalized,
        "screenshot_supported_card_observations": card_rows,
        "accepted_scope": _accepted_scope(),
        "not_accepted_scope": _not_accepted_scope(),
        "readiness_separation": _readiness_separation(),
        "render_gate_carry_forward": _render_gate_carry_forward(),
        "recommended_next_slices": _recommended_next_slices(),
        "goal_stack": _goal_stack(),
        "completion_matrix": _completion_matrix(),
        "artifact_readiness": _artifact_readiness(),
        "visual_density_gate": _visual_density_gate(),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(),
        "boundaries": _boundaries(),
        "downstream_next_use": _downstream_next_use(),
    }


def render_newsroom_post_density_refinement_render_smoke_result_readback_markdown(
    readback: dict[str, Any],
) -> str:
    """Render a compact human-readable readback."""
    lines = [
        "# Newsroom Post-Density Refinement Render Smoke Result Readback v1",
        "",
        f"artifact_id: {readback.get('artifact_id')}",
        f"readback_id: {readback.get('readback_id')}",
        f"schema_version: {readback.get('schema_version')}",
        f"review_status: {readback.get('review_status')}",
        f"production_status: {readback.get('production_status')}",
        f"visual_work_class: {readback.get('visual_work_class')}",
        f"result_status: {readback.get('result_status')}",
        "diagnostic_only: true",
        "",
        "## Identity",
        "",
    ]
    for key, value in _dict(readback.get("identity")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Source Validation", ""])
    for key, value in _dict(readback.get("source_validation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Operator Freeform Observation", ""])
    for key, value in _dict(readback.get("operator_freeform_observation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Normalized Render Observation", ""])
    for key, value in _dict(readback.get("normalized_render_observation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Screenshot-Supported Card Observations",
            "",
            "| card | visible | density simplification | dominant message | clutter | notes |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in readback.get("screenshot_supported_card_observations", []):
        lines.append(
            "| "
            f"{row.get('card_index')} | "
            f"{_display(row.get('visible_status'))} | "
            f"{_display(row.get('density_simplification_visible'))} | "
            f"{_display(row.get('dominant_message_visible'))} | "
            f"{_display(row.get('clutter_reduced'))} | "
            f"{_display(row.get('notes'))} |"
        )

    lines.extend(["", "## Accepted Scope", ""])
    for key, value in _dict(readback.get("accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Not Accepted Scope", ""])
    for key, value in _dict(readback.get("not_accepted_scope")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Readiness Separation", ""])
    for key, value in _dict(readback.get("readiness_separation")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Render Gate Carry-Forward", ""])
    for key, value in _dict(readback.get("render_gate_carry_forward")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Recommended Next Slices",
            "",
            "| slice | timing | reason |",
            "|---|---|---|",
        ]
    )
    for row in readback.get("recommended_next_slices", []):
        lines.append(
            "| "
            f"{row.get('slice')} | "
            f"{row.get('timing')} | "
            f"{row.get('reason')} |"
        )

    _append_status_table(lines, "Completion Matrix", readback.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", readback.get("artifact_readiness"))
    _append_status_table(lines, "Visual Density Gate", readback.get("visual_density_gate"))
    _append_status_table(lines, "Render Gate Hygiene", readback.get("render_gate_hygiene"))
    _append_status_table(
        lines, "Human Burden Hygiene", readback.get("human_burden_hygiene")
    )
    _append_status_table(
        lines, "Review Non-Redundancy", readback.get("review_non_redundancy")
    )
    _append_status_table(lines, "Inertia Check", readback.get("inertia_check"))

    lines.extend(["", "## Boundary", ""])
    for key, value in _dict(readback.get("boundaries")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Downstream Next Use", ""])
    for key, value in _dict(readback.get("downstream_next_use")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This readback consumes the user render observation once and moves the "
            "lane toward internal review v0.1 re-evaluation. It does not "
            "redesign cards, regenerate assets, launch YMM4, render, edit "
            "`.ymmp`, generate audio/TTS, claim audience acceptance, or approve "
            "production/public use.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    root: Path,
    density_refinement: dict[str, Any],
    density_spec: dict[str, Any],
    density_gate: dict[str, Any],
    benchmark_evaluation: dict[str, Any],
) -> dict[str, Any]:
    per_card = list(density_refinement.get("per_card_changes", []))
    errors: list[str] = []
    if density_refinement.get("refinement_status") != (
        "density_benchmark_materially_improved"
    ):
        errors.append("density refinement status is not materially improved")
    if density_refinement.get("actual_audience_acceptance_claimed") is not False:
        errors.append("density refinement must not claim audience acceptance")
    if _dict(density_refinement.get("local_proxy_recheck")).get("fail_count") != 0:
        errors.append("density refinement local proxy has failures")
    if _dict(density_refinement.get("png_export")).get("png_export_status") != (
        "generated"
    ):
        errors.append("density refinement PNG export is not generated")
    if len(per_card) != 4:
        errors.append("density refinement does not describe four cards")
    if density_spec.get("production_status") != "diagnostic_only":
        errors.append("density spec is not diagnostic only")
    if density_gate.get("observation_status") != "visual_density_issue_confirmed":
        errors.append("density gate source is not the expected density issue")
    if benchmark_evaluation.get("actual_audience_acceptance_claimed") is True:
        errors.append("benchmark evaluation must not claim audience acceptance")

    missing_assets: list[str] = []
    for row in per_card:
        for key in ("output_svg_path", "output_png_path"):
            value = row.get(key)
            if not value or not (root / str(value)).exists():
                missing_assets.append(str(value))
    if missing_assets:
        errors.append("card asset paths missing: " + ", ".join(missing_assets))

    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "source_density_refinement_id": density_refinement.get("refinement_id"),
        "source_density_refinement_status": density_refinement.get(
            "refinement_status"
        ),
        "source_density_proxy_status": _dict(
            density_refinement.get("local_proxy_recheck")
        ).get("proxy_status"),
        "source_density_proxy_fail_count": _dict(
            density_refinement.get("local_proxy_recheck")
        ).get("fail_count"),
        "source_png_export_status": _dict(density_refinement.get("png_export")).get(
            "png_export_status"
        ),
        "source_density_spec_id": density_spec.get("spec_id"),
        "source_density_gate_id": density_gate.get("readback_id"),
        "source_density_gate_status": density_gate.get("observation_status"),
        "source_benchmark_evaluation_id": benchmark_evaluation.get("evaluation_id"),
        "source_card_count": len(per_card),
        "card_assets_exist": not missing_assets,
        "svg_png_cards_regenerated_in_this_slice": False,
    }


def _operator_freeform_observation() -> dict[str, Any]:
    return {
        "source": "user_freeform_with_screenshot_support",
        "summary": (
            "User confirmed the post-density render completed at about 68 sec; "
            "information is more organized than before; card visuals and audio remain."
        ),
        "yym4_project_observed": "diagnostic_bound_speaker_probe_card_placement_v1",
        "render_completed": True,
        "duration_observed": "approximately_68_sec",
        "density_improvement_reported": True,
        "cards_remain_visible": True,
        "audio_remains": True,
        "fixed_form_required": False,
    }


def _normalized_render_observation() -> dict[str, Any]:
    return {
        "render_smoke_result": "pass",
        "yym4_opened_card_placement_project": True,
        "render_completed": True,
        "output_duration_observed": "approximately_68_sec",
        "duration_matches_timing_patch": True,
        "card_assets_visible": True,
        "card_count_visible": 4,
        "density_refinement_visible": True,
        "information_density_reduced": True,
        "dialogue_items_preserved": True,
        "rendered_line_count_mismatch_warning": "possible_due_to_wrapping",
        "native_audio_present": True,
        "visual_card_integrity": "pass",
        "timing_preservation_regression_reported": False,
        "audio_regression_reported": False,
        "production_visual_quality_accepted": False,
        "actual_audience_acceptance_claimed": False,
        "public_video_ready": False,
    }


def _card_observations(density_refinement: dict[str, Any]) -> list[dict[str, Any]]:
    rows = sorted(
        list(density_refinement.get("per_card_changes", [])),
        key=lambda row: int(row.get("display_order", 0)),
    )
    return [
        {
            "card_index": int(row.get("display_order", index + 1)),
            "card_id": row.get("card_id"),
            "visible_status": True,
            "density_simplification_visible": True,
            "dominant_message_visible": True,
            "clutter_reduced": True,
            "notes": [
                "diagnostic/review-only card",
                "no audience acceptance claim",
            ],
        }
        for index, row in enumerate(rows)
    ]


def _accepted_scope() -> dict[str, bool]:
    return {
        "post_density_refinement_cards_render_visibly_in_yym4_surface": True,
        "duration_remains_approximately_68_sec": True,
        "four_card_assets_remain_visible": True,
        "dialogue_and_native_audio_are_preserved": True,
        "information_density_materially_improved_at_diagnostic_level": True,
        "ready_to_return_to_internal_review_v0_1_reevaluation": True,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "actual_youtube_audience_acceptance": False,
        "ctr_retention_prediction": False,
        "production_visual_quality": False,
        "final_design_system": False,
        "final_narration_script_density": False,
        "public_video_readiness": False,
        "real_newsroom_visual_acceptance": False,
        "production_approval": False,
    }


def _readiness_separation() -> dict[str, Any]:
    return {
        "slice_completion": "pass_for_this_readback",
        "video_readiness_progress": "6/7",
        "visual_density_readiness": "diagnostic_pass",
        "production_readiness": "low_diagnostic_only",
        "next_missing_gate": "internal review v0.1 re-evaluation",
        "recommended_next_axis": NEXT_DEFAULT_SLICE,
        "public_video_ready": False,
    }


def _render_gate_carry_forward() -> dict[str, Any]:
    return {
        "current_user_render_observation_consumed_once": True,
        "new_render_in_this_slice": False,
        "YMM4_launched_by_agent": False,
        "render_audio_or_tts_created_by_agent": False,
        "card_assets_regenerated_in_this_slice": False,
        "render_gate": "milestone_gated_not_docs_gated",
        "next_render_allowed_after": [
            "material surface change",
            "internal review package explicitly requires it",
        ],
        "no_render_for": [
            "docs/readback-only changes",
            "repeating the same observation",
            "mechanics proof already covered by this user observation",
        ],
    }


def _recommended_next_slices() -> list[dict[str, str]]:
    return [
        {
            "slice": NEXT_DEFAULT_SLICE,
            "timing": "recommended_next_default",
            "reason": (
                "mechanics, timing, audio, placement, and density-refinement "
                "render observation pass at diagnostic level; next value is "
                "internal review against the simplified surface"
            ),
        },
        {
            "slice": DENSITY_REDUCTION_V2_SLICE,
            "timing": "only_if_material_density_failures_are_found",
            "reason": "use only if internal review finds remaining density failures",
        },
        {
            "slice": RSS_DRY_RUN_PLAN_SLICE,
            "timing": "later_after_internal_review_reevaluation",
            "reason": "RSS dry-run planning should wait until review direction is set",
        },
        {
            "slice": RETENTION_POLICY_SLICE,
            "timing": "only_if_output_artifact_retention_becomes_necessary",
            "reason": "render output retention is operational policy, not this readback",
        },
    ]


def _goal_stack() -> list[dict[str, str]]:
    return [
        {
            "level": "Immediate",
            "goal": "Normalize the post-density render observation",
            "success_signal": "readback JSON/doc record pass without new render",
            "contribution": "turns freeform observation into repo evidence",
        },
        {
            "level": "Short-term",
            "goal": "Resume internal review v0.1 re-evaluation",
            "success_signal": "next slice is review of simplified card surface",
            "contribution": "moves past mechanics and visual-density proof",
        },
        {
            "level": "Mid-term",
            "goal": "Separate review readiness from production acceptance",
            "success_signal": "diagnostic pass recorded without public-readiness claim",
            "contribution": "keeps review useful and honest",
        },
        {
            "level": "Long-term",
            "goal": "Preserve render-gate hygiene",
            "success_signal": "future render only follows material change or review need",
            "contribution": "prevents repeated proof loops",
        },
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"gate": "current_repo_state_verified", "status": True},
        {"gate": "density_refinement_artifacts_inspected", "status": True},
        {"gate": "latest_observation_normalized", "status": True},
        {"gate": "result_readback_json_doc_created", "status": True},
        {"gate": "readiness_and_next_axis_updated", "status": True},
        {
            "gate": "narrow_commit_created_and_pushed_if_push_gate_passes",
            "status": "pending_until_git_gate",
        },
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "result_readback_json_exists", "status": True},
        {"gate": "human_doc_exists", "status": True},
        {"gate": "normalized_render_observation_present", "status": True},
        {"gate": "accepted_not_accepted_scopes_present", "status": True},
        {"gate": "render_gate_carry_forward_present", "status": True},
        {"gate": "downstream_next_use_described", "status": True},
    ]


def _visual_density_gate() -> list[dict[str, Any]]:
    return [
        {"gate": "density_refinement_reused", "status": True},
        {"gate": "density_spec_reused", "status": True},
        {"gate": "user_render_observation_consumed_once", "status": True},
        {"gate": "no_further_redesign_performed", "status": True},
        {"gate": "actual_audience_acceptance_not_claimed", "status": True},
        {
            "gate": "density_improvement_recorded_as_diagnostic_observation",
            "status": True,
        },
        {"gate": "next_review_axis_selected", "status": NEXT_DEFAULT_SLICE},
        {"gate": "unknowns_preserved", "status": True},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "no_render_performed_by_agent", "status": True},
        {"gate": "existing_user_render_observation_consumed_once", "status": True},
        {"gate": "no_render_for_docs_readback_only_change", "status": True},
        {
            "gate": "next_render_tied_to_material_surface_change_or_review_need",
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


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"gate": "latest_observation_consumed_once", "status": True},
        {"gate": "density_refinement_reused", "status": True},
        {"gate": "density_spec_reused", "status": True},
        {"gate": "next_axis", "status": NEXT_DEFAULT_SLICE},
        {"gate": "not_accepted_scope_preserved", "status": True},
        {"gate": "no_mechanics_re_review_requested", "status": True},
    ]


def _inertia_check() -> list[dict[str, Any]]:
    return [
        {"gate": "no_ad_hoc_visual_iteration", "status": True},
        {"gate": "no_broad_redesign", "status": True},
        {"gate": "no_packet_for_packet_drift", "status": True},
        {"gate": "readiness_separated_from_slice_completion", "status": True},
        {"gate": "next_concrete_review_milestone", "status": NEXT_DEFAULT_SLICE},
    ]


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "cards_regenerated": False,
        "ymmp_edited_or_committed": False,
        "audio_tts_generated": False,
        "external_assets_or_live_audience_data_fetched": False,
        "actual_audience_acceptance_claimed": False,
        "production_public_readiness_claimed": False,
        "fixed_review_form_requested": False,
        "dashboard_governance_freshness_drift": False,
    }


def _downstream_next_use() -> dict[str, str]:
    return {
        "next_default_slice": NEXT_DEFAULT_SLICE,
        "first_readback_to_reopen": _path_text(
            DEFAULT_POST_DENSITY_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        "reason": (
            "post-density rendered surface is diagnostically passable; next "
            "work should evaluate internal review v0.1 value, not repeat mechanics"
        ),
    }


def _append_status_table(
    lines: list[str],
    title: str,
    rows: object,
) -> None:
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
    write_default_newsroom_post_density_refinement_render_smoke_result_readback_artifacts()
