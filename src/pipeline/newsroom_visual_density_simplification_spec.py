"""Define the newsroom visual density simplification spec.

This is a criteria/specification slice only. It does not launch YMM4, render
video, regenerate card assets, edit .ymmp files, generate audio/TTS, fetch
external media, or claim production/public/audience acceptance.
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
from src.pipeline.newsroom_visual_audience_fit_benchmark import (
    DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH,
)
from src.pipeline.newsroom_visual_card_asset_bridge import DEFAULT_VISUAL_CARD_ASSET_DIR
from src.pipeline.newsroom_visual_card_benchmarked_refinement import (
    DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH,
)


VISUAL_DENSITY_SIMPLIFICATION_SPEC_SCHEMA_VERSION = (
    "newsroom_visual_density_simplification_spec.v1"
)
VISUAL_DENSITY_SIMPLIFICATION_SPEC_ID = (
    "newsroom_visual_density_simplification_spec_v1_2026_06_26"
)

DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH = Path(
    "samples/_probe/newsroom_handoff/visual_density_simplification_spec_v1.json"
)
DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_DOC_PATH = Path(
    "docs/verification/NEWSROOM_VISUAL_DENSITY_SIMPLIFICATION_SPEC_V1_2026-06-26.md"
)

NEXT_DEFAULT_SLICE = "newsroom-visual-card-density-benchmarked-refinement-v1"
INFORMATION_DENSITY_BENCHMARK_SLICE = (
    "newsroom-visual-information-density-benchmark-v1"
)
OPERATOR_REVIEW_SLICE = "newsroom-internal-review-v0.1-operator-review-card"
SOURCE_BAND_SIMPLIFICATION_SLICE = "newsroom-visual-card-source-band-simplification-v1"


def build_default_newsroom_visual_density_simplification_spec(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the density simplification spec from the current readbacks."""
    base = Path(root) if root is not None else Path(".")
    density_gate = load_json_object(
        base / DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH
    )
    benchmark_evaluation = load_json_object(
        base / DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH
    )
    visual_benchmark = load_json_object(
        base / DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH
    )
    benchmarked_refinement = load_json_object(
        base / DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH
    )
    card_inventory = _card_asset_inventory(base, base / DEFAULT_VISUAL_CARD_ASSET_DIR)
    card_diagnosis = _card_specific_preliminary_diagnosis(benchmarked_refinement)
    source_validation = _source_validation(
        base=base,
        density_gate=density_gate,
        benchmark_evaluation=benchmark_evaluation,
        visual_benchmark=visual_benchmark,
        benchmarked_refinement=benchmarked_refinement,
        card_inventory=card_inventory,
        card_diagnosis=card_diagnosis,
    )
    return {
        "artifact_id": VISUAL_DENSITY_SIMPLIFICATION_SPEC_ID,
        "spec_id": VISUAL_DENSITY_SIMPLIFICATION_SPEC_ID,
        "schema_version": VISUAL_DENSITY_SIMPLIFICATION_SPEC_SCHEMA_VERSION,
        "spec_status": "defined",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "visual_work_class": "audience_fit",
        "actual_audience_acceptance_claimed": False,
        "identity": {
            "spec_id": VISUAL_DENSITY_SIMPLIFICATION_SPEC_ID,
            "source_density_gate_path": _path_text(
                DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH
            ),
            "source_density_gate_id": density_gate.get("readback_id"),
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
            "source_benchmarked_refinement_path": _path_text(
                DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH
            ),
            "source_benchmarked_refinement_id": benchmarked_refinement.get(
                "refinement_id"
            ),
            "source_cards_dir": _path_text(DEFAULT_VISUAL_CARD_ASSET_DIR),
            "production_status": "diagnostic_only",
            "visual_work_class": "audience_fit",
            "spec_status": "defined",
            "actual_audience_acceptance_claimed": False,
        },
        "source_validation": source_validation,
        "problem_statement": _problem_statement(),
        "density_budget": _density_budget(),
        "simplification_operations": _simplification_operations(),
        "hard_constraints": _hard_constraints(),
        "card_asset_inventory": card_inventory,
        "card_specific_preliminary_diagnosis": card_diagnosis,
        "evaluation_criteria_for_next_refinement": _evaluation_criteria(),
        "next_slice_recommendation": _next_slice_recommendation(),
        "recommended_next_slices": _recommended_next_slices(),
        "not_accepted_scope": _not_accepted_scope(),
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


def write_default_newsroom_visual_density_simplification_spec_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write the density simplification spec JSON and Markdown doc."""
    base = Path(root) if root is not None else Path(".")
    spec = build_default_newsroom_visual_density_simplification_spec(root=base)
    _write_json(base / DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_PATH, spec)
    _write_text(
        base / DEFAULT_VISUAL_DENSITY_SIMPLIFICATION_SPEC_DOC_PATH,
        render_newsroom_visual_density_simplification_spec_markdown(spec),
    )
    return spec


def render_newsroom_visual_density_simplification_spec_markdown(
    spec: dict[str, Any],
) -> str:
    """Render a compact density simplification spec."""
    lines = [
        "# Newsroom Visual Density Simplification Spec v1",
        "",
        f"artifact_id: {spec['artifact_id']}",
        f"spec_id: {spec['spec_id']}",
        f"schema_version: {spec['schema_version']}",
        f"spec_status: {spec['spec_status']}",
        f"production_status: {spec['production_status']}",
        "",
        "## Outcome",
        "",
        (
            "This spec turns the recorded density/cognitive-load finding into "
            "bounded simplification criteria for the next visual refinement. It "
            "does not redesign cards, regenerate assets, launch YMM4, render "
            "video, edit .ymmp files, or claim production/public/audience "
            "acceptance."
        ),
        "",
        "## Identity",
        "",
    ]
    _append_key_values(lines, spec["identity"])
    lines.extend(["", "## Problem Statement", ""])
    _append_key_values(lines, spec["problem_statement"])
    lines.extend(["", "## Density Budget", ""])
    _append_key_values(lines, spec["density_budget"])
    lines.extend(
        [
            "",
            "## Simplification Operations",
            "",
            "| operation | rule | future use |",
            "|---|---|---|",
        ]
    )
    for row in spec["simplification_operations"]:
        lines.append(f"| {row['operation']} | {row['rule']} | {row['future_use']} |")
    lines.extend(["", "## Hard Constraints", ""])
    _append_key_values(lines, spec["hard_constraints"])
    lines.extend(
        [
            "",
            "## Card-Specific Preliminary Diagnosis",
            "",
            "| card | likely density problem | essential message | remove/demote | must stay | future direction |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in spec["card_specific_preliminary_diagnosis"]:
        lines.append(
            "| "
            f"{row['card_id']} | "
            f"{row['likely_density_problem']} | "
            f"{row['essential_message_to_preserve']} | "
            f"{_display(row['elements_that_can_be_removed_or_demoted'])} | "
            f"{_display(row['elements_that_must_stay'])} | "
            f"{row['suggested_future_simplification_direction']} |"
        )
    lines.extend(
        [
            "",
            "## Evaluation Criteria For Next Refinement",
            "",
            "| criterion | target |",
            "|---|---|",
        ]
    )
    for row in spec["evaluation_criteria_for_next_refinement"]:
        lines.append(f"| {row['criterion']} | {row['target']} |")
    lines.extend(["", "## Next Slice Recommendation", ""])
    _append_key_values(lines, spec["next_slice_recommendation"])
    lines.extend(
        [
            "",
            "## Recommended Next Slices",
            "",
            "| slice | timing | reason |",
            "|---|---|---|",
        ]
    )
    for row in spec["recommended_next_slices"]:
        lines.append(f"| {row['slice']} | {row['timing']} | {row['reason']} |")
    lines.extend(["", "## Not Accepted Scope", ""])
    _append_key_values(lines, spec["not_accepted_scope"])
    lines.extend(
        [
            "",
            "## Goal Stack",
            "",
            "| level | goal | success signal | contribution |",
            "|---|---|---|---|",
        ]
    )
    for row in spec["goal_stack"]:
        lines.append(
            "| "
            f"{row['level']} | "
            f"{row['goal']} | "
            f"{row['success_signal']} | "
            f"{row['contribution']} |"
        )
    _append_status_table(lines, "Completion Matrix", spec["completion_matrix"])
    _append_status_table(lines, "Artifact Readiness", spec["artifact_readiness"])
    _append_status_table(lines, "Visual Gate", spec["visual_gate"])
    _append_status_table(lines, "Render Gate Hygiene", spec["render_gate_hygiene"])
    _append_status_table(lines, "Human Burden Hygiene", spec["human_burden_hygiene"])
    _append_status_table(lines, "Review Non-Redundancy", spec["review_non_redundancy"])
    _append_status_table(lines, "Inertia Check", spec["inertia_check"])
    lines.extend(["", "## Downstream Next Use", ""])
    _append_key_values(lines, spec["downstream_next_use"])
    lines.extend(["", "## Boundaries", ""])
    _append_key_values(lines, spec["boundaries"])
    return "\n".join(lines) + "\n"


def _source_validation(
    *,
    base: Path,
    density_gate: dict[str, Any],
    benchmark_evaluation: dict[str, Any],
    visual_benchmark: dict[str, Any],
    benchmarked_refinement: dict[str, Any],
    card_inventory: dict[str, Any],
    card_diagnosis: list[dict[str, Any]],
) -> dict[str, Any]:
    expected_paths = [
        DEFAULT_POST_BENCHMARKED_VISUAL_OBSERVATION_DENSITY_GATE_PATH,
        DEFAULT_AUDIENCE_FIT_BENCHMARK_EVALUATION_PATH,
        DEFAULT_VISUAL_AUDIENCE_FIT_BENCHMARK_PATH,
        DEFAULT_VISUAL_CARD_BENCHMARKED_REFINEMENT_PATH,
    ]
    errors = [
        f"SOURCE_PATH_MISSING:{_path_text(path)}"
        for path in expected_paths
        if not (base / path).exists()
    ]
    if density_gate.get("observation_status") != "visual_density_issue_confirmed":
        errors.append("DENSITY_GATE_NOT_CONFIRMED")
    if density_gate.get("mechanics_status") != "pass":
        errors.append("DENSITY_GATE_MECHANICS_NOT_PASS")
    if density_gate.get("recommended_next_slice", {}).get("slice") != (
        "newsroom-visual-density-simplification-spec-v1"
    ):
        errors.append("DENSITY_GATE_NEXT_SLICE_MISMATCH")
    if benchmarked_refinement.get("refinement_status") != (
        "benchmarked_text_fit_improved"
    ):
        errors.append("BENCHMARKED_REFINEMENT_NOT_IMPROVED")
    if benchmark_evaluation.get("production_status") != "diagnostic_only":
        errors.append("BENCHMARK_EVALUATION_NOT_DIAGNOSTIC")
    if visual_benchmark.get("benchmark_status") != "draft_proxy_benchmark_defined":
        errors.append("VISUAL_BENCHMARK_STATUS_UNEXPECTED")
    if card_inventory["svg_count"] != 4 or card_inventory["png_count"] != 4:
        errors.append("VISUAL_CARD_ASSET_COUNT_NOT_4")
    if len(card_diagnosis) != 4:
        errors.append("CARD_DIAGNOSIS_COUNT_NOT_4")
    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "source_ids": {
            "density_gate_id": density_gate.get("readback_id"),
            "benchmark_evaluation_id": benchmark_evaluation.get("evaluation_id"),
            "visual_benchmark_id": visual_benchmark.get("benchmark_id"),
            "benchmarked_refinement_id": benchmarked_refinement.get("refinement_id"),
        },
        "card_asset_counts": {
            "svg": card_inventory["svg_count"],
            "png": card_inventory["png_count"],
        },
    }


def _problem_statement() -> dict[str, bool]:
    return {
        "mechanics_status_pass": True,
        "visual_density_issue": True,
        "cognitive_load_high": True,
        "format_attention_over_content": True,
        "text_fit_tight_warning": True,
        "pacing_density_issue_for_68_sec_video": True,
        "production_quality_accepted": False,
        "public_video_ready": False,
    }


def _density_budget() -> dict[str, Any]:
    return {
        "dominant_message_per_card": "exactly_one",
        "headline_budget": "maximum_1_headline",
        "primary_sentence_budget": "maximum_1_primary_sentence",
        "supporting_note_or_diagram_budget": "maximum_1",
        "meaningful_label_budget": "maximum_2_to_3_labels",
        "essential_meaning_in_tiny_metadata": False,
        "debug_or_source_text_policy": "shorten_demote_or_hide_from_main_viewing_path",
        "subtitle_reserve_policy": "simple_and_non_competing",
        "minimum_meaningful_font_size_policy": "preserve_or_increase",
        "box_count_policy": "reduce_or_merge_before_adding",
    }


def _simplification_operations() -> list[dict[str, str]]:
    return [
        {
            "operation": "remove_nonessential_microcopy",
            "rule": "delete text that explains diagnostic scaffolding but does not change the viewer's takeaway",
            "future_use": "reduce reading paths before changing style",
        },
        {
            "operation": "merge_repeated_labels",
            "rule": "combine repeated role/status labels into one visible boundary or cue",
            "future_use": "keep the diagnostic boundary without label clutter",
        },
        {
            "operation": "demote_diagnostic_source_metadata",
            "rule": "move source/debug detail out of the primary viewing path or shorten it to a tiny nonessential cue",
            "future_use": "prevent source/subtitle areas from competing with the card message",
        },
        {
            "operation": "replace_small_text_with_visual_markers",
            "rule": "use icons, numbers, or color-coded markers when the text only signals role/state",
            "future_use": "remove tiny reading obligations without losing role variation",
        },
        {
            "operation": "increase_whitespace_around_essential_text",
            "rule": "give the headline and primary sentence more breathing room before adding any explanatory box",
            "future_use": "make the dominant message visible within three seconds",
        },
        {
            "operation": "split_overloaded_roles_only_if_necessary",
            "rule": "split a card role only when removal/merge/demotion cannot preserve the essential message",
            "future_use": "avoid expanding the four-card structure casually",
        },
        {
            "operation": "preserve_fake_review_boundary_with_fewer_labels",
            "rule": "retain review-only/fake/diagnostic meaning through one compact boundary signal",
            "future_use": "keep publication safety while reducing surface noise",
        },
        {
            "operation": "preserve_card_role_variation",
            "rule": "keep point, flow, check, and next/source roles distinct after simplification",
            "future_use": "prevent simplification from flattening the explainer structure",
        },
    ]


def _hard_constraints() -> dict[str, bool]:
    return {
        "do_not_reduce_minimum_meaningful_font_size": True,
        "do_not_solve_density_by_shrinking_text": True,
        "do_not_add_more_boxes_to_explain_existing_boxes": True,
        "do_not_introduce_real_brands_urls_or_real_news_visuals": True,
        "do_not_convert_cards_into_complex_yym4_object_graphs": True,
        "do_not_claim_production_visual_quality": True,
        "do_not_claim_audience_acceptance": True,
    }


def _card_specific_preliminary_diagnosis(
    benchmarked_refinement: dict[str, Any],
) -> list[dict[str, Any]]:
    per_card = {
        int(row["display_order"]): row
        for row in benchmarked_refinement.get("per_card_changes", [])
    }
    static_diagnosis = {
        1: {
            "likely_density_problem": "intro card carries headline, summary, number motif, point panel, no-real-claim chip, and source band at once",
            "essential_message_to_preserve": "fake topic is review-only and the card is a plain point summary",
            "elements_that_can_be_removed_or_demoted": [
                "secondary POINT mini panel",
                "no-real-news-claim chip if boundary is preserved elsewhere",
                "extra diagnostic badge repetition",
            ],
            "elements_that_must_stay": [
                "review-only/fake boundary",
                "dominant fake-topic headline",
                "card order cue",
            ],
            "suggested_future_simplification_direction": "make one large point message with one compact diagnostic boundary and more whitespace",
        },
        2: {
            "likely_density_problem": "flow card repeats step numbers, labels, and simple-flow badge while also asking the viewer to read body copy",
            "essential_message_to_preserve": "handoff stays review-only through three simple steps",
            "elements_that_can_be_removed_or_demoted": [
                "simple-flow badge",
                "repeated explanatory body text",
                "extra box outlines around every step",
            ],
            "elements_that_must_stay": [
                "three-step flow",
                "review-only boundary",
                "role difference from point/check/source cards",
            ],
            "suggested_future_simplification_direction": "use three large step markers with short labels and remove secondary explanation",
        },
        3: {
            "likely_density_problem": "check card uses four small status boxes plus left body text, creating multiple reading paths",
            "essential_message_to_preserve": "a fake claim is shown and the viewer should understand it is check/review-only",
            "elements_that_can_be_removed_or_demoted": [
                "RESULT box",
                "STATUS box",
                "duplicate check/caution microcopy",
            ],
            "elements_that_must_stay": [
                "fake claim boundary",
                "check/caution role",
                "large readable primary message",
            ],
            "suggested_future_simplification_direction": "collapse status boxes into one check/caution visual cue and keep one primary sentence",
        },
        4: {
            "likely_density_problem": "next/source card stacks source, status, next panels and a next bubble, so metadata competes with the main next action",
            "essential_message_to_preserve": "fake source checks are noted and the next action remains diagnostic",
            "elements_that_can_be_removed_or_demoted": [
                "separate SOURCE/STATUS/NEXT panel headings",
                "next bubble",
                "source microcopy in the main reading path",
            ],
            "elements_that_must_stay": [
                "source-check awareness",
                "next-action role",
                "diagnostic/fake boundary",
            ],
            "suggested_future_simplification_direction": "merge source/status/next into one short next-action block with demoted source detail",
        },
    }
    rows: list[dict[str, Any]] = []
    for order in sorted(static_diagnosis):
        source = per_card.get(order, {})
        rows.append(
            {
                "card_id": source.get("card_id", f"card_{order}"),
                "display_order": order,
                "current_headline_lines": list(source.get("headline_lines", [])),
                "current_body_lines": list(source.get("body_lines", [])),
                "current_source_label": source.get("source_display_label"),
                "current_png_path": source.get("output_png_path"),
                **static_diagnosis[order],
                "implemented_in_this_slice": False,
            }
        )
    return rows


def _evaluation_criteria() -> list[dict[str, str]]:
    return [
        {
            "criterion": "dominant_message_visible_within_3_seconds",
            "target": "viewer can identify the card's single point without reading secondary metadata",
        },
        {
            "criterion": "no_more_than_one_primary_reading_path",
            "target": "headline and one primary sentence or diagram carry the main meaning",
        },
        {
            "criterion": "meaningful_text_fits_without_crowding",
            "target": "no essential text sits close to box edges or depends on unexpected wrap behavior",
        },
        {
            "criterion": "source_subtitle_debug_area_does_not_compete",
            "target": "source/subtitle/debug cues are visibly secondary to main content",
        },
        {
            "criterion": "role_difference_remains_clear",
            "target": "point, flow, check, and next/source roles remain distinguishable",
        },
        {
            "criterion": "diagnostic_fake_boundary_remains_visible",
            "target": "review-only/fake status remains clear with fewer labels",
        },
        {
            "criterion": "surface_feels_simpler_than_previous_density_gate",
            "target": "less broadcast/presentation-like concentration burden than the benchmarked cards",
        },
    ]


def _next_slice_recommendation() -> dict[str, Any]:
    return {
        "default_slice": NEXT_DEFAULT_SLICE,
        "reason": "density/cognitive-load issue now has a spec and can be addressed with a bounded card update",
        "user_side_work": "none_for_this_slice",
    }


def _recommended_next_slices() -> list[dict[str, str]]:
    return [
        {
            "slice": NEXT_DEFAULT_SLICE,
            "timing": "default_next",
            "reason": "apply remove/merge/demote/whitespace rules to the current card assets",
        },
        {
            "slice": INFORMATION_DENSITY_BENCHMARK_SLICE,
            "timing": "only_if_current_spec_cannot_define_adequate_criteria",
            "reason": "upgrade metrics before refinement only if these spec criteria are insufficient",
        },
        {
            "slice": OPERATOR_REVIEW_SLICE,
            "timing": "only_if_supervisor_accepts_current_density_for_diagnostic_v0_1",
            "reason": "skip additional visual change only with an explicit supervisor decision",
        },
        {
            "slice": SOURCE_BAND_SIMPLIFICATION_SLICE,
            "timing": "if_source_subtitle_band_is_dominant_actionable_issue",
            "reason": "narrow to source/subtitle band if the next diagnosis says that is the main burden",
        },
    ]


def _not_accepted_scope() -> dict[str, Any]:
    return {
        "actual_target_audience_acceptance": "unknown",
        "ctr_retention_prediction": "unknown",
        "production_visual_quality": False,
        "final_design_system": False,
        "real_newsroom_visual_acceptance": False,
        "public_readiness": False,
        "production_approval": False,
    }


def _goal_stack() -> list[dict[str, str]]:
    return [
        {
            "level": "Immediate",
            "goal": "Define density simplification rules",
            "success_signal": "spec JSON/doc exists",
            "contribution": "prevents another ad hoc visual tweak",
        },
        {
            "level": "Short-term",
            "goal": "Enable bounded density refinement",
            "success_signal": "next card change has explicit remove/merge/demote rules",
            "contribution": "reduces cognitive load",
        },
        {
            "level": "Mid-term",
            "goal": "Resume internal review v0.1",
            "success_signal": "refined cards can be reviewed for pacing and content, not visual clutter",
            "contribution": "improves review utility",
        },
        {
            "level": "Long-term",
            "goal": "Establish reusable density baseline",
            "success_signal": "future RSS/content videos inherit simpler card rules",
            "contribution": "supports automation",
        },
    ]


def _completion_matrix() -> list[dict[str, Any]]:
    return [
        {"item": "current_repo_state_verified", "status": True},
        {"item": "density_gate_inspected", "status": True},
        {"item": "density_budget_defined", "status": True},
        {"item": "simplification_operations_and_hard_constraints_defined", "status": True},
        {"item": "card_specific_preliminary_diagnosis_recorded", "status": True},
        {
            "item": "narrow_commit_created_and_pushed_if_push_gate_passes",
            "status": "agent_followthrough_after_validation",
        },
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"item": "spec_json_exists", "status": True},
        {"item": "human_doc_exists", "status": True},
        {"item": "density_budget_present", "status": True},
        {"item": "simplification_operations_present", "status": True},
        {"item": "next_refinement_criteria_present", "status": True},
        {"item": "downstream_next_use_described", "status": True},
    ]


def _visual_gate() -> list[dict[str, Any]]:
    return [
        {"item": "density_issue_preserved", "status": True},
        {"item": "cognitive_load_issue_preserved", "status": True},
        {"item": "no_redesign_performed", "status": True},
        {"item": "no_audience_acceptance_claimed", "status": True},
        {"item": "proxy_criteria_defined", "status": True},
        {"item": "next_iteration_bounded", "status": True},
        {"item": "unknowns_preserved", "status": True},
        {"item": "review_protocol_remains_freeform", "status": True},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"item": "no_render_performed_by_agent", "status": True},
        {"item": "no_render_for_spec_only_change", "status": True},
        {"item": "next_render_tied_to_material_density_linked_card_change", "status": True},
        {"item": "repeated_render_loop_avoided", "status": True},
        {"item": "existing_observation_consumed_once", "status": True},
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
        {"item": "density_gate_reused", "status": True},
        {"item": "benchmark_evaluation_reused", "status": True},
        {"item": "next_axis_density_simplification_spec", "status": True},
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
        "default_next_slice": NEXT_DEFAULT_SLICE,
        "instruction": "the next visual change must choose changes from this spec's remove/merge/demote/whitespace operations",
        "allowed_change_axis": [
            "density-benchmarked card refinement",
            "source/subtitle band simplification if it is the dominant burden",
            "benchmark upgrade only if this spec is inadequate",
        ],
        "disallowed_change_axis": [
            "broad redesign",
            "style-only polish",
            "text shrinking",
            "more boxes explaining existing boxes",
            "YMM4/render/audio/TTS work for this spec-only slice",
        ],
    }


def _push_gate_policy() -> dict[str, Any]:
    return {
        "commit_message": "docs: define newsroom visual density simplification spec",
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
            "SVG/PNG card assets",
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
        "card_redesign_performed": False,
        "production_approval": False,
        "audience_acceptance_claimed": False,
        "public_video_ready": False,
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
