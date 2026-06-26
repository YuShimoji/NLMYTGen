"""Post-refinement render smoke package for newsroom visual cards.

This slice prepares the next milestone-gated manual render observation after
the visual card assets were refined in place. It does not launch YMM4, render,
edit .ymmp files, generate audio/TTS, import media, or approve production use.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from src.pipeline.newsroom_card_placement_render_smoke_result_readback import (
    DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH,
)
from src.pipeline.newsroom_episode_production_capsule import load_json_object
from src.pipeline.newsroom_visual_card_design_refinement import (
    DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH,
    VISUAL_CARD_DESIGN_REFINEMENT_ID,
)
from src.pipeline.newsroom_yym4_card_asset_placement_probe import (
    CARD_REMARK_PREFIX,
    DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH,
    DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_SCHEMA_VERSION = (
    "newsroom_card_placement_post_refinement_render_smoke.v1"
)
CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION = (
    "newsroom_card_placement_post_refinement_render_smoke_result_readback.v1"
)
CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_ID = (
    "newsroom_card_placement_post_refinement_render_smoke_v1_2026_06_26"
)
CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_BUILDER_ID = (
    "newsroom_card_placement_post_refinement_render_smoke_result_readback_builder_v1"
)
DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_PATH = Path(
    "samples/_probe/newsroom_handoff/"
    "card_placement_post_refinement_render_smoke_v1.json"
)
DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_DOC_PATH = Path(
    "docs/verification/"
    "NEWSROOM_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_V1_2026-06-26.md"
)
DEFAULT_POST_REFINEMENT_RENDER_OUTPUT_LOCAL_PATH = Path(
    "_tmp/newsroom_manual_probe/"
    "diagnostic_bound_speaker_probe_card_placement_post_refinement_v1.mp4"
)

NEXT_RESULT_READBACK_SLICE = (
    "newsroom-card-placement-post-refinement-render-smoke-result-readback-v1"
)
RENDER_FAILURE_CLASSIFICATION_SLICE = (
    "newsroom-card-placement-post-refinement-render-smoke-failure-classification-v1"
)
OPERATOR_UNCERTAINTY_SLICE = (
    "newsroom-card-placement-post-refinement-render-smoke-operator-uncertainty-v1"
)
INTERNAL_REVIEW_PREP_SLICE = "newsroom-internal-review-v0.1-prep"
PLACEMENT_REFRESH_SLICE = "newsroom-yym4-card-asset-placement-refresh-v1"

EXPECTED_DURATION_SEC = 68
EXPECTED_DURATION_TOLERANCE_SEC = 2
EXPECTED_CARD_COUNT = 4
EXPECTED_DIALOGUE_ITEM_COUNT = 4

PASS_CLASSIFICATION = "post_refinement_render_smoke_pass"
OPEN_FAILURE_CLASSIFICATION = "post_refinement_project_open_failure"
RENDER_FAILURE_CLASSIFICATION = "post_refinement_render_execution_failure"
DURATION_FAILURE_CLASSIFICATION = "post_refinement_duration_mismatch"
CARD_VISIBILITY_FAILURE_CLASSIFICATION = "post_refinement_card_visibility_regression"
READABILITY_FAILURE_CLASSIFICATION = "post_refinement_readability_regression"
DIALOGUE_FAILURE_CLASSIFICATION = "post_refinement_dialogue_preservation_regression"
NATIVE_AUDIO_FAILURE_CLASSIFICATION = "post_refinement_native_audio_regression"
OPERATOR_UNCERTAIN_CLASSIFICATION = "post_refinement_operator_observation_uncertain"

OBSERVATION_TARGETS: tuple[str, ...] = (
    "card-placement diagnostic project opens",
    "render completes to a separate post-refinement output",
    "output duration is approximately 68 seconds",
    "four refined PNG cards are visible and have no obvious text clipping",
    "dialogue timeline and native YMM4/Yukkuri audio remain present",
)
NORMALIZATION_FIELD_NAMES: tuple[str, ...] = (
    "placement_project_opened",
    "render_completed",
    "output_duration_observed_sec",
    "duration_approximately_68_sec",
    "refined_card_assets_visible",
    "card_count_observed",
    "no_obvious_text_clipping_or_readability_breakage",
    "dialogue_items_preserved",
    "dialogue_item_count_observed",
    "native_audio_present",
    "operator_notes",
    "error_message",
    "confidence",
    "unknowns",
    "classification",
    "result",
)


def build_default_newsroom_card_placement_post_refinement_render_smoke(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the committed post-refinement render smoke observation package."""
    base = Path(root) if root is not None else Path(".")
    refinement = load_json_object(base / DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH)
    placement_probe = load_json_object(
        base / DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH
    )
    prior_render_result = load_json_object(
        base / DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
    )
    ymmp_path = DEFAULT_CARD_PLACEMENT_YMMP_LOCAL_PATH
    output_path = DEFAULT_POST_REFINEMENT_RENDER_OUTPUT_LOCAL_PATH
    ymmp_summary = _ymmp_card_image_summary(base / ymmp_path, refinement)
    return build_newsroom_card_placement_post_refinement_render_smoke(
        refinement,
        placement_probe,
        prior_render_result,
        source_refinement_path=DEFAULT_VISUAL_CARD_DESIGN_REFINEMENT_PATH,
        source_placement_probe_path=DEFAULT_YYM4_CARD_ASSET_PLACEMENT_PROBE_PATH,
        source_prior_render_result_path=(
            DEFAULT_CARD_PLACEMENT_RENDER_SMOKE_RESULT_READBACK_PATH
        ),
        target_ymmp_path=ymmp_path,
        target_ymmp_exists=(base / ymmp_path).exists(),
        post_refinement_output_path=output_path,
        post_refinement_output_exists=(base / output_path).exists(),
        ymmp_summary=ymmp_summary,
        root=base,
    )


def write_default_newsroom_card_placement_post_refinement_render_smoke_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Write the JSON and human-readable post-refinement render smoke package."""
    base = Path(root) if root is not None else Path(".")
    package = build_default_newsroom_card_placement_post_refinement_render_smoke(
        root=base
    )
    _write_json(
        base / DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_PATH,
        package,
    )
    _write_text(
        base / DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_DOC_PATH,
        render_newsroom_card_placement_post_refinement_render_smoke_markdown(
            package
        ),
    )
    return package


def build_newsroom_card_placement_post_refinement_render_smoke(
    refinement: dict[str, Any],
    placement_probe: dict[str, Any],
    prior_render_result: dict[str, Any],
    *,
    source_refinement_path: str | Path,
    source_placement_probe_path: str | Path,
    source_prior_render_result_path: str | Path,
    target_ymmp_path: str | Path,
    target_ymmp_exists: bool,
    post_refinement_output_path: str | Path,
    post_refinement_output_exists: bool,
    ymmp_summary: dict[str, Any],
    root: str | Path,
) -> dict[str, Any]:
    """Build the diagnostic-only manual render smoke package."""
    source_validation = _source_validation(
        refinement,
        placement_probe,
        prior_render_result,
        target_ymmp_path=target_ymmp_path,
        target_ymmp_exists=target_ymmp_exists,
        ymmp_summary=ymmp_summary,
        root=Path(root),
    )
    package_status = (
        "ready_for_manual_milestone_render_smoke"
        if not source_validation["errors"]
        else "blocked"
    )
    return {
        "artifact_id": CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_ID,
        "smoke_id": CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_ID,
        "schema_version": (
            CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_SCHEMA_VERSION
        ),
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "smoke_status": "prepared_not_run",
        "package_status": package_status,
        "identity": {
            "smoke_id": CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_ID,
            "source_refinement_path": _path_text(source_refinement_path),
            "source_refinement_id": refinement.get("refinement_id"),
            "source_placement_probe_path": _path_text(source_placement_probe_path),
            "source_placement_probe_id": placement_probe.get("probe_id"),
            "source_prior_render_result_path": _path_text(
                source_prior_render_result_path
            ),
            "source_prior_render_result_id": prior_render_result.get("readback_id"),
            "target_card_placement_ymmp_path": _path_text(target_ymmp_path),
            "post_refinement_render_output_path": _path_text(
                post_refinement_output_path
            ),
            "production_status": "diagnostic_only",
            "render_smoke_status": "not_run",
        },
        "source_validation": source_validation,
        "target": _target(
            refinement,
            ymmp_summary,
            target_ymmp_path=target_ymmp_path,
            target_ymmp_exists=target_ymmp_exists,
            post_refinement_output_path=post_refinement_output_path,
            post_refinement_output_exists=post_refinement_output_exists,
        ),
        "milestone_render_gate": _milestone_render_gate(),
        "operator_observation_card": _operator_observation_card(
            target_ymmp_path,
            post_refinement_output_path,
        ),
        "result_normalization_schema": _result_normalization_schema(),
        "success_failure_classification_matrix": _classification_matrix(),
        "render_readback_builder": _render_readback_builder_contract(),
        "accepted_scope": _accepted_scope(package_status),
        "not_accepted_scope": _not_accepted_scope(),
        "readiness_separation": _readiness_separation(package_status),
        "completion_matrix": _completion_matrix(package_status),
        "artifact_readiness": _artifact_readiness(package_status),
        "visual_readiness": _visual_readiness(package_status),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "review_non_redundancy": _review_non_redundancy(),
        "inertia_check": _inertia_check(package_status),
        "boundaries": _boundaries(),
        "downstream_next_use": _downstream_next_use(package_status),
        "validation_expectations": _validation_expectations(),
    }


def normalize_render_smoke_observation(
    observation: dict[str, Any],
) -> dict[str, Any]:
    """Normalize an agent-read operator observation into the result schema."""
    normalized = {
        "placement_project_opened": _bool_or_unknown(
            observation.get("placement_project_opened")
        ),
        "render_completed": _bool_or_unknown(observation.get("render_completed")),
        "output_duration_observed_sec": _number(
            observation.get("output_duration_observed_sec")
        ),
        "duration_approximately_68_sec": _bool_or_unknown(
            observation.get("duration_approximately_68_sec")
        ),
        "refined_card_assets_visible": _bool_or_unknown(
            observation.get("refined_card_assets_visible")
        ),
        "card_count_observed": _intish(observation.get("card_count_observed")),
        "no_obvious_text_clipping_or_readability_breakage": _bool_or_unknown(
            observation.get("no_obvious_text_clipping_or_readability_breakage")
        ),
        "dialogue_items_preserved": _bool_or_unknown(
            observation.get("dialogue_items_preserved")
        ),
        "dialogue_item_count_observed": _intish(
            observation.get("dialogue_item_count_observed")
        ),
        "native_audio_present": _bool_or_unknown(
            observation.get("native_audio_present")
        ),
        "operator_notes": observation.get("operator_notes"),
        "error_message": observation.get("error_message"),
        "confidence": observation.get("confidence", "operator_freeform"),
        "unknowns": observation.get("unknowns", []),
    }
    if normalized["duration_approximately_68_sec"] == "unknown":
        duration = normalized["output_duration_observed_sec"]
        if duration is not None:
            normalized["duration_approximately_68_sec"] = _duration_is_approx_68(
                duration
            )
    if normalized["card_count_observed"] is not None:
        normalized["refined_card_assets_visible"] = (
            normalized["card_count_observed"] == EXPECTED_CARD_COUNT
        )
    if normalized["dialogue_item_count_observed"] is not None:
        normalized["dialogue_items_preserved"] = (
            normalized["dialogue_item_count_observed"]
            == EXPECTED_DIALOGUE_ITEM_COUNT
        )
    classification = classify_render_smoke_observation(normalized)
    normalized["classification"] = classification["classification"]
    normalized["result"] = classification["result"]
    return normalized


def classify_render_smoke_observation(
    observation: dict[str, Any],
) -> dict[str, Any]:
    """Classify the normalized render smoke observation by first blocker."""
    opened = _bool_or_unknown(observation.get("placement_project_opened"))
    render_completed = _bool_or_unknown(observation.get("render_completed"))
    duration_ok = _bool_or_unknown(observation.get("duration_approximately_68_sec"))
    cards_visible = _bool_or_unknown(observation.get("refined_card_assets_visible"))
    readability_ok = _bool_or_unknown(
        observation.get("no_obvious_text_clipping_or_readability_breakage")
    )
    dialogue_ok = _bool_or_unknown(observation.get("dialogue_items_preserved"))
    native_audio_ok = _bool_or_unknown(observation.get("native_audio_present"))

    if duration_ok == "unknown":
        duration = _number(observation.get("output_duration_observed_sec"))
        if duration is not None:
            duration_ok = _duration_is_approx_68(duration)
    card_count = _intish(observation.get("card_count_observed"))
    if card_count is not None:
        cards_visible = card_count == EXPECTED_CARD_COUNT
    dialogue_count = _intish(observation.get("dialogue_item_count_observed"))
    if dialogue_count is not None:
        dialogue_ok = dialogue_count == EXPECTED_DIALOGUE_ITEM_COUNT

    if opened is False:
        return _classification_result(
            OPEN_FAILURE_CLASSIFICATION,
            "fail",
            "YMM4 did not open the card-placement diagnostic project.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if opened != True:
        return _uncertain_result("project open status was not clear")
    if render_completed is False:
        return _classification_result(
            RENDER_FAILURE_CLASSIFICATION,
            "fail",
            "YMM4 opened the project but render did not complete.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if render_completed != True:
        return _uncertain_result("render completion status was not clear")
    if duration_ok is False:
        return _classification_result(
            DURATION_FAILURE_CLASSIFICATION,
            "fail",
            "Rendered output duration was not approximately 68 seconds.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if duration_ok != True:
        return _uncertain_result("output duration was not clear")
    if cards_visible is False:
        return _classification_result(
            CARD_VISIBILITY_FAILURE_CLASSIFICATION,
            "fail",
            "The four refined card PNGs were not all visible in the render.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if cards_visible != True:
        return _uncertain_result("refined card visibility was not clear")
    if readability_ok is False:
        return _classification_result(
            READABILITY_FAILURE_CLASSIFICATION,
            "fail",
            "The refined cards still show obvious clipping or readability breakage.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if readability_ok != True:
        return _uncertain_result("card readability status was not clear")
    if dialogue_ok is False:
        return _classification_result(
            DIALOGUE_FAILURE_CLASSIFICATION,
            "fail",
            "Dialogue items were missing or altered after render.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if dialogue_ok != True:
        return _uncertain_result("dialogue preservation was not clear")
    if native_audio_ok is False:
        return _classification_result(
            NATIVE_AUDIO_FAILURE_CLASSIFICATION,
            "fail",
            "Native YMM4/Yukkuri audio was absent after render.",
            RENDER_FAILURE_CLASSIFICATION_SLICE,
        )
    if native_audio_ok != True:
        return _uncertain_result("native audio presence was not clear")
    return _classification_result(
        PASS_CLASSIFICATION,
        "pass",
        "Post-refinement project opened, rendered, stayed about 68 sec, showed four readable cards, and preserved dialogue plus native audio.",
        NEXT_RESULT_READBACK_SLICE,
    )


def build_newsroom_card_placement_post_refinement_render_smoke_result_readback(
    package: dict[str, Any],
    observation: dict[str, Any],
    *,
    source_package_path: str | Path,
    readback_id: str = (
        "newsroom_card_placement_post_refinement_render_smoke_result_readback_v1"
    ),
    observation_source: str = "future_user_freeform",
) -> dict[str, Any]:
    """Build a future result readback from a normalized operator observation."""
    normalized = normalize_render_smoke_observation(observation)
    classification = classify_render_smoke_observation(normalized)
    return {
        "artifact_id": readback_id,
        "readback_id": readback_id,
        "schema_version": (
            CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION
        ),
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "observation_source": observation_source,
        "identity": {
            "readback_id": readback_id,
            "source_smoke_package_path": _path_text(source_package_path),
            "source_smoke_package_id": package.get("smoke_id"),
            "target_card_placement_ymmp_path": _dict(package.get("target")).get(
                "target_card_placement_ymmp_path"
            ),
            "production_status": "diagnostic_only",
        },
        "source_validation": _result_builder_source_validation(package),
        "normalized_result": normalized,
        "classification": classification,
        "accepted_scope": _accepted_scope_from_classification(classification),
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
        "next_recommended_slice": classification["next_recommended_slice"],
    }


def render_newsroom_card_placement_post_refinement_render_smoke_markdown(
    package: dict[str, Any],
) -> str:
    """Render a human-readable post-refinement render smoke package."""
    identity = _dict(package.get("identity"))
    validation = _dict(package.get("source_validation"))
    target = _dict(package.get("target"))
    gate = _dict(package.get("milestone_render_gate"))
    card = _dict(package.get("operator_observation_card"))
    schema = _dict(package.get("result_normalization_schema"))
    builder = _dict(package.get("render_readback_builder"))

    lines = [
        "# Newsroom Card Placement Post-Refinement Render Smoke v1",
        "",
        f"artifact_id: {package.get('artifact_id')}",
        f"smoke_id: {package.get('smoke_id')}",
        f"schema_version: {package.get('schema_version')}",
        f"review_status: {package.get('review_status')}",
        f"production_status: {package.get('production_status')}",
        f"smoke_status: {package.get('smoke_status')}",
        f"package_status: {package.get('package_status')}",
        "diagnostic_only: true",
        "",
        "## Source",
        "",
    ]
    for key, value in identity.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Source Validation", ""])
    for key, value in validation.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(["", "## Target", ""])
    for key, value in target.items():
        if key != "expected_refined_cards":
            lines.append(f"- {key}: {_display(value)}")
    lines.extend(
        [
            "",
            "| card | role | png | ymmp path reused |",
            "|---|---|---|---|",
        ]
    )
    for row in target.get("expected_refined_cards", []):
        lines.append(
            "| "
            f"{row.get('card_id')} | "
            f"{row.get('role')} | "
            f"{row.get('png_path')} | "
            f"{_display(row.get('ymmp_path_reused'))} |"
        )

    lines.extend(["", "## Milestone Render Gate", ""])
    for key, value in gate.items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Operator Observation Card",
            "",
            f"- status: {card.get('status')}",
            f"- target: {card.get('target')}",
            f"- target_ymmp_path: {card.get('target_ymmp_path')}",
            f"- output_path: {card.get('output_path')}",
            f"- why: {card.get('why')}",
            f"- action: {card.get('action')}",
            f"- answer_style: {card.get('answer_style')}",
            f"- answer_hint: {card.get('answer_hint')}",
            "- look_for:",
        ]
    )
    for item in card.get("look_for", []):
        lines.append(f"  - {item}")
    lines.append("- not_needed:")
    for item in card.get("not_needed", []):
        lines.append(f"  - {item}")

    lines.extend(
        [
            "",
            "## Result Normalization Schema",
            "",
            f"- schema_owner: {schema.get('schema_owner')}",
            f"- user_must_fill_schema: {_display(schema.get('user_must_fill_schema'))}",
            f"- duration_tolerance_sec: {schema.get('duration_tolerance_sec')}",
            "",
            "| field | type | normalization |",
            "|---|---|---|",
        ]
    )
    for row in schema.get("fields", []):
        lines.append(
            "| "
            f"{row.get('field')} | "
            f"{row.get('type')} | "
            f"{row.get('normalization')} |"
        )

    lines.extend(
        [
            "",
            "## Success / Failure Classification Matrix",
            "",
            "| classification | trigger | result | next slice |",
            "|---|---|---|---|",
        ]
    )
    for row in package.get("success_failure_classification_matrix", []):
        lines.append(
            "| "
            f"{row.get('classification')} | "
            f"{row.get('trigger')} | "
            f"{row.get('result')} | "
            f"{row.get('next_recommended_slice')} |"
        )

    lines.extend(["", "## Render Readback Builder", ""])
    for key, value in builder.items():
        lines.append(f"- {key}: {_display(value)}")

    _append_status_table(lines, "Completion Matrix", package.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", package.get("artifact_readiness"))
    _append_status_table(lines, "Visual Readiness", package.get("visual_readiness"))
    _append_status_table(lines, "Render Gate Hygiene", package.get("render_gate_hygiene"))
    _append_status_table(
        lines, "Human Burden Hygiene", package.get("human_burden_hygiene")
    )
    _append_status_table(
        lines, "Review Non-Redundancy", package.get("review_non_redundancy")
    )
    _append_status_table(lines, "Inertia Check", package.get("inertia_check"))

    lines.extend(["", "## Boundary", ""])
    for key, value in _dict(package.get("boundaries")).items():
        lines.append(f"- {key}: {_display(value)}")

    lines.extend(
        [
            "",
            "## Boundary Note",
            "",
            "This package prepares one milestone observation of the changed "
            "visual surface after the card assets were refined at stable paths. "
            "The agent did not launch YMM4, render, edit `.ymmp`, generate "
            "audio/TTS, stage media, or approve production/public use.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_validation(
    refinement: dict[str, Any],
    placement_probe: dict[str, Any],
    prior_render_result: dict[str, Any],
    *,
    target_ymmp_path: str | Path,
    target_ymmp_exists: bool,
    ymmp_summary: dict[str, Any],
    root: Path,
) -> dict[str, Any]:
    errors: list[str] = []
    design_changes = _list(refinement.get("design_changes"))
    refined_png_paths = [str(row.get("output_png_path")) for row in design_changes]
    prior_normalized = _dict(prior_render_result.get("normalized_render_result"))
    ymmp_card_paths = _list(ymmp_summary.get("card_items"))

    if refinement.get("refinement_id") != VISUAL_CARD_DESIGN_REFINEMENT_ID:
        errors.append("VISUAL_REFINEMENT_ID_MISMATCH")
    if refinement.get("refinement_status") != "assets_regenerated":
        errors.append("VISUAL_REFINEMENT_ASSETS_NOT_REGENERATED")
    if _dict(refinement.get("next_recommended_slice")).get("slice") != (
        "newsroom-card-placement-post-refinement-render-smoke-v1"
    ):
        errors.append("VISUAL_REFINEMENT_NEXT_SLICE_MISMATCH")
    if len(design_changes) != EXPECTED_CARD_COUNT:
        errors.append("REFINED_CARD_COUNT_NOT_4")
    if not all(row.get("png_valid") is True for row in design_changes):
        errors.append("REFINED_PNG_METADATA_NOT_VALID")
    for path in refined_png_paths:
        if not (root / path).exists():
            errors.append(f"REFINED_PNG_MISSING:{path}")
    if placement_probe.get("probe_status") != "placed_structurally":
        errors.append("CARD_PLACEMENT_PROBE_NOT_STRUCTURAL_PASS")
    if prior_render_result.get("result_status") != "pass":
        errors.append("PRIOR_CARD_PLACEMENT_RENDER_RESULT_NOT_PASS")
    if prior_normalized.get("output_duration_sec") != EXPECTED_DURATION_SEC:
        errors.append("PRIOR_CARD_PLACEMENT_RENDER_NOT_68_SEC")
    if prior_normalized.get("card_count_visible") != EXPECTED_CARD_COUNT:
        errors.append("PRIOR_VISIBLE_CARD_COUNT_NOT_4")
    if not target_ymmp_exists:
        errors.append("TARGET_CARD_PLACEMENT_YMMP_NOT_FOUND")
    if ymmp_summary.get("status") != "passed":
        errors.extend(_list_str(ymmp_summary.get("errors")))
    if len(ymmp_card_paths) != EXPECTED_CARD_COUNT:
        errors.append("TARGET_YMMP_CARD_IMAGE_ITEM_COUNT_NOT_4")
    reused_paths = [
        path
        for path in refined_png_paths
        if any(_path_matches_reference(row.get("file_path"), path) for row in ymmp_card_paths)
    ]
    if len(reused_paths) != len(refined_png_paths):
        errors.append("TARGET_YMMP_DOES_NOT_REUSE_ALL_REFINED_PNG_PATHS")
    if _git_has_output(root, ["ls-files", "--", _path_text(target_ymmp_path)]):
        errors.append("TARGET_YMMP_IS_TRACKED")
    if _git_has_output(
        root, ["diff", "--cached", "--name-only", "--", _path_text(target_ymmp_path)]
    ):
        errors.append("TARGET_YMMP_IS_STAGED")
    if not _git_returncode_zero(
        root, ["check-ignore", "-q", "--", _path_text(target_ymmp_path)]
    ):
        errors.append("TARGET_YMMP_NOT_IGNORED")

    return {
        "status": "passed" if not errors else "blocked",
        "errors": errors,
        "source_refinement_id": refinement.get("refinement_id"),
        "source_refinement_status": refinement.get("refinement_status"),
        "source_placement_probe_id": placement_probe.get("probe_id"),
        "source_placement_probe_status": placement_probe.get("probe_status"),
        "source_prior_render_result_id": prior_render_result.get("readback_id"),
        "source_prior_render_result": prior_render_result.get("result_status"),
        "prior_render_duration_sec": prior_normalized.get("output_duration_sec"),
        "prior_render_card_count_visible": prior_normalized.get("card_count_visible"),
        "refined_card_count": len(design_changes),
        "refined_png_paths": refined_png_paths,
        "target_ymmp_path": _path_text(target_ymmp_path),
        "target_ymmp_found_at_generation": target_ymmp_exists,
        "target_ymmp_card_image_item_count": len(ymmp_card_paths),
        "target_ymmp_reuses_refined_png_paths": len(reused_paths) == len(refined_png_paths),
        "target_ymmp_ignored": _git_returncode_zero(
            root, ["check-ignore", "-q", "--", _path_text(target_ymmp_path)]
        ),
        "target_ymmp_committed": _git_has_output(
            root, ["ls-files", "--", _path_text(target_ymmp_path)]
        ),
        "target_ymmp_staged": _git_has_output(
            root, ["diff", "--cached", "--name-only", "--", _path_text(target_ymmp_path)]
        ),
    }


def _target(
    refinement: dict[str, Any],
    ymmp_summary: dict[str, Any],
    *,
    target_ymmp_path: str | Path,
    target_ymmp_exists: bool,
    post_refinement_output_path: str | Path,
    post_refinement_output_exists: bool,
) -> dict[str, Any]:
    cards = []
    card_items = _list(ymmp_summary.get("card_items"))
    for row in _list(refinement.get("design_changes")):
        png_path = str(row.get("output_png_path"))
        cards.append(
            {
                "card_id": row.get("card_id"),
                "role": row.get("role"),
                "layout_motif": row.get("layout_motif"),
                "png_path": png_path,
                "ymmp_path_reused": any(
                    _path_matches_reference(item.get("file_path"), png_path)
                    for item in card_items
                ),
                "text_wrap_applied": row.get("text_wrap_applied"),
                "clipping_guard": row.get("clipping_guard"),
            }
        )
    return {
        "target_card_placement_ymmp_path": _path_text(target_ymmp_path),
        "target_ymmp_path_status": (
            "discoverable_local_file_at_generation_time"
            if target_ymmp_exists
            else "recorded_but_not_found_at_generation_time"
        ),
        "git_tracking_policy": "ignored_under_tmp_do_not_stage_or_commit",
        "ymmp_file_newly_modified_in_this_slice": False,
        "post_refinement_render_output_path": _path_text(post_refinement_output_path),
        "post_refinement_output_exists_at_generation": post_refinement_output_exists,
        "render_output_commit_allowed": False,
        "expected_duration_sec": EXPECTED_DURATION_SEC,
        "expected_card_count": EXPECTED_CARD_COUNT,
        "expected_dialogue_item_count": EXPECTED_DIALOGUE_ITEM_COUNT,
        "expected_refined_cards": cards,
        "render_objective": {
            "confirm_project_opens": True,
            "confirm_render_completes": True,
            "confirm_output_duration_about_68_sec": True,
            "confirm_refined_cards_visible_and_readable": True,
            "confirm_dialogue_and_native_audio_preserved": True,
            "production": False,
            "public_video": False,
        },
    }


def _milestone_render_gate() -> dict[str, Any]:
    return {
        "gate_type": "milestone_gated_verification",
        "milestone": "newsroom-card-placement-post-refinement-render-smoke-v1",
        "render_performed_in_this_slice": False,
        "YMM4_launched_by_agent": False,
        "manual_render_allowed_next": True,
        "manual_render_count": 1,
        "render_reason": (
            "Refined card PNGs replaced the prior visual surface at stable paths, "
            "so one observation can confirm YMM4 sees the updated assets."
        ),
        "timing_strategy_change_allowed": False,
        "external_TTS_allowed": False,
        "render_output_commit_allowed": False,
        "ymmp_commit_allowed": False,
    }


def _operator_observation_card(
    target_ymmp_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    return {
        "status": "required_next_milestone",
        "target": "post-refinement card-placement diagnostic render smoke",
        "target_ymmp_path": _path_text(target_ymmp_path),
        "output_path": _path_text(output_path),
        "why": "Confirm the existing card-placement project reads the regenerated refined PNG assets.",
        "action": (
            "Open the ignored card-placement .ymmp in YMM4 and render once to "
            "the separate post-refinement output path without changing timing, "
            "voice, media, or card placement."
        ),
        "look_for": list(OBSERVATION_TARGETS),
        "answer_style": "freeform",
        "answer_hint": (
            "opened and rendered; about 68 sec; four refined cards visible "
            "without obvious clipping; dialogue and native voice remained"
        ),
        "not_needed": [
            "fixed form",
            "another review of the old card design",
            "detailed sound quality judgement",
            "production quality approval",
            "committing .ymmp or media output",
        ],
    }


def _result_normalization_schema() -> dict[str, Any]:
    return {
        "schema_id": CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_BUILDER_ID,
        "schema_version": (
            CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION
        ),
        "schema_owner": "Agent",
        "user_must_fill_schema": False,
        "normalization_source": "future freeform operator observation",
        "duration_tolerance_sec": EXPECTED_DURATION_TOLERANCE_SEC,
        "fields": [
            {
                "field": "placement_project_opened",
                "type": "boolean_or_unknown",
                "normalization": "true only when the target .ymmp opens in YMM4",
            },
            {
                "field": "render_completed",
                "type": "boolean_or_unknown",
                "normalization": "true only when YMM4 export finishes",
            },
            {
                "field": "output_duration_observed_sec",
                "type": "number_or_null",
                "normalization": "observed media duration in seconds when known",
            },
            {
                "field": "duration_approximately_68_sec",
                "type": "boolean_or_unknown",
                "normalization": "true when duration is within the configured 68 sec tolerance",
            },
            {
                "field": "refined_card_assets_visible",
                "type": "boolean_or_unknown",
                "normalization": "true when all four refined PNG cards are visible",
            },
            {
                "field": "card_count_observed",
                "type": "integer_or_null",
                "normalization": "observed refined card count when reported",
            },
            {
                "field": "no_obvious_text_clipping_or_readability_breakage",
                "type": "boolean_or_unknown",
                "normalization": "true when the operator reports no obvious clipping or readability breakage",
            },
            {
                "field": "dialogue_items_preserved",
                "type": "boolean_or_unknown",
                "normalization": "true when the expected dialogue items remain present",
            },
            {
                "field": "dialogue_item_count_observed",
                "type": "integer_or_null",
                "normalization": "observed dialogue item count if reported",
            },
            {
                "field": "native_audio_present",
                "type": "boolean_or_unknown",
                "normalization": "true when native YMM4/Yukkuri audio is still audible",
            },
            {
                "field": "operator_notes",
                "type": "string_or_null",
                "normalization": "freeform notes retained without requiring a form",
            },
            {
                "field": "error_message",
                "type": "string_or_null",
                "normalization": "YMM4 or export error text when reported",
            },
            {
                "field": "confidence",
                "type": "string",
                "normalization": "agent confidence in the normalized observation",
            },
            {
                "field": "unknowns",
                "type": "array",
                "normalization": "required targets the observation did not settle",
            },
            {
                "field": "classification",
                "type": "enum",
                "normalization": "classification from the success/failure matrix",
            },
            {
                "field": "result",
                "type": "enum",
                "normalization": "pass, fail, or blocked_by_operator_uncertainty",
            },
        ],
    }


def _classification_matrix() -> list[dict[str, Any]]:
    return [
        {
            "classification": PASS_CLASSIFICATION,
            "trigger": "all post-refinement observation targets are true",
            "result": "pass",
            "next_recommended_slice": NEXT_RESULT_READBACK_SLICE,
        },
        {
            "classification": OPEN_FAILURE_CLASSIFICATION,
            "trigger": "card-placement project does not open",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": RENDER_FAILURE_CLASSIFICATION,
            "trigger": "project opens but render does not complete",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": DURATION_FAILURE_CLASSIFICATION,
            "trigger": "render completes but output is not approximately 68 sec",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": CARD_VISIBILITY_FAILURE_CLASSIFICATION,
            "trigger": "fewer than four refined cards are visible",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": READABILITY_FAILURE_CLASSIFICATION,
            "trigger": "cards render but still show obvious clipping or readability breakage",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": DIALOGUE_FAILURE_CLASSIFICATION,
            "trigger": "dialogue items are missing or altered",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": NATIVE_AUDIO_FAILURE_CLASSIFICATION,
            "trigger": "native audio is absent",
            "result": "fail",
            "next_recommended_slice": RENDER_FAILURE_CLASSIFICATION_SLICE,
        },
        {
            "classification": OPERATOR_UNCERTAIN_CLASSIFICATION,
            "trigger": "one or more required observation targets remain unknown",
            "result": "blocked_by_operator_uncertainty",
            "next_recommended_slice": OPERATOR_UNCERTAINTY_SLICE,
        },
    ]


def _render_readback_builder_contract() -> dict[str, Any]:
    return {
        "builder_id": CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_BUILDER_ID,
        "module": "src.pipeline.newsroom_card_placement_post_refinement_render_smoke",
        "function": (
            "build_newsroom_card_placement_post_refinement_render_smoke_result_readback"
        ),
        "input_package": _path_text(
            DEFAULT_CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_PATH
        ),
        "input_observation": "future freeform operator observation normalized by Agent",
        "output_schema_version": (
            CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_RESULT_READBACK_SCHEMA_VERSION
        ),
        "writes_artifact_in_this_slice": False,
        "requires_committed_media": False,
        "requires_committed_ymmp": False,
        "classification_function": "classify_render_smoke_observation",
    }


def _accepted_scope(package_status: str) -> dict[str, bool]:
    ready = package_status == "ready_for_manual_milestone_render_smoke"
    return {
        "refined_assets_confirmed_at_stable_paths": ready,
        "existing_card_placement_ymmp_reuses_refined_png_paths": ready,
        "post_refinement_render_smoke_package_prepared": ready,
        "future_freeform_readback_builder_defined": ready,
        "render_not_performed_by_agent": True,
    }


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "post_refinement_render_proof": False,
        "production_visual_quality": False,
        "final_design_system": False,
        "public_video_readiness": False,
        "real_newsroom_visuals": False,
        "real_content_readiness": False,
        "production_approval": False,
        "render_output_retention": False,
    }


def _readiness_separation(package_status: str) -> dict[str, Any]:
    return {
        "slice_completion": (
            "pass_for_render_smoke_package"
            if package_status == "ready_for_manual_milestone_render_smoke"
            else "blocked"
        ),
        "video_readiness_progress": "6/7",
        "visual_readiness_progress": "7/7_diagnostic_refined",
        "visual_readiness_current": "post_refinement_render_smoke_package_prepared",
        "video_readiness_next_missing_gate": (
            "post-refinement render smoke observation"
        ),
        "production_readiness": "low_diagnostic_only",
        "next_default_slice": NEXT_RESULT_READBACK_SLICE
        if package_status == "ready_for_manual_milestone_render_smoke"
        else PLACEMENT_REFRESH_SLICE,
    }


def _completion_matrix(package_status: str) -> list[dict[str, Any]]:
    ready = package_status == "ready_for_manual_milestone_render_smoke"
    return [
        {"gate": "current_repo_state_verified", "status": True},
        {"gate": "prior_visual_refinement_detected_as_complete", "status": True},
        {"gate": "stable_png_paths_verified_in_ignored_ymmp", "status": ready},
        {"gate": "manual_render_smoke_package_created", "status": True},
        {"gate": "future_readback_normalizer_defined", "status": True},
        {
            "gate": "narrow_commit_created_and_pushed_if_push_gate_passes",
            "status": "pending_until_git_gate",
        },
    ]


def _artifact_readiness(package_status: str) -> list[dict[str, Any]]:
    return [
        {"artifact": "render_smoke_package_json", "status": "present"},
        {"artifact": "human_render_smoke_doc", "status": "present"},
        {"artifact": "source_validation", "status": package_status},
        {"artifact": "operator_observation_card", "status": "present"},
        {"artifact": "result_normalization_schema", "status": "present"},
        {"artifact": "downstream_next_use", "status": "present"},
    ]


def _visual_readiness(package_status: str) -> list[dict[str, Any]]:
    ready = package_status == "ready_for_manual_milestone_render_smoke"
    return [
        {"gate": "visual_card_concept_selected", "status": True},
        {"gate": "external_card_assets_generated", "status": True},
        {"gate": "preview_contact_sheet_available", "status": True},
        {"gate": "assets_mapped_to_timeline_caption_units", "status": True},
        {"gate": "yym4_placement_contract_defined", "status": True},
        {"gate": "yym4_placement_paths_reused_after_refinement", "status": ready},
        {"gate": "post_refinement_render_reviewed", "status": False},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "render_performed_by_agent_in_this_slice", "status": False},
        {"gate": "existing_render_evidence_reused", "status": True},
        {"gate": "render_treated_as_milestone_gated", "status": True},
        {"gate": "next_render_tied_to_visual_surface_change", "status": True},
        {"gate": "no_render_for_docs_readback_changes", "status": True},
        {"gate": "repeated_timing_audio_review_avoided", "status": True},
    ]


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "user_input", "status": "freeform"},
        {"gate": "template_required", "status": False},
        {"gate": "schema_owner", "status": "Agent"},
        {"gate": "user_side_work_this_agent_slice", "status": "none"},
        {"gate": "required_future_observation_target_count", "status": len(OBSERVATION_TARGETS)},
        {"gate": "negative_confirmation_checklist", "status": False},
        {"gate": "fixed_form_relapse", "status": False},
    ]


def _review_non_redundancy() -> list[dict[str, Any]]:
    return [
        {"gate": "prior_internal_review_observation_reused", "status": True},
        {"gate": "prior_visual_refinement_reused", "status": True},
        {"gate": "prior_card_placement_render_evidence_reused", "status": True},
        {"gate": "next_axis_stated_as_post_refinement_render_smoke", "status": True},
        {"gate": "not_accepted_scope_preserved", "status": True},
        {"gate": "current_user_review_or_render_re_requested", "status": False},
    ]


def _inertia_check(package_status: str) -> list[dict[str, Any]]:
    return [
        {"gate": "packet_for_packet_drift", "status": False},
        {"gate": "readback_only_stall", "status": False},
        {"gate": "repeated_render_request_without_surface_change", "status": False},
        {"gate": "readiness_separated_from_slice_completion", "status": True},
        {
            "gate": "next_concrete_milestone",
            "status": NEXT_RESULT_READBACK_SLICE
            if package_status == "ready_for_manual_milestone_render_smoke"
            else PLACEMENT_REFRESH_SLICE,
        },
    ]


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "video_render_created_by_agent": False,
        "audio_generated_by_agent": False,
        "TTS_generated_by_agent": False,
        "external_TTS_introduced": False,
        "real_media_imported": False,
        "external_source_fetch_performed": False,
        "real_brand_url_or_news_screenshot_used": False,
        "ymmp_edited_by_agent": False,
        "ymmp_or_media_staged_or_committed": False,
        "render_output_staged_or_committed": False,
        "production_visual_quality_accepted": False,
        "production_approval": False,
        "public_video_ready": False,
        "dashboard_governance_freshness_changed": False,
    }


def _downstream_next_use(package_status: str) -> dict[str, list[str]]:
    if package_status == "ready_for_manual_milestone_render_smoke":
        use_this = [
            "guide one post-refinement render smoke of the ignored placement project",
            "normalize the later freeform observation into a repo readback",
            "decide whether internal review prep can proceed on the refined visual surface",
        ]
    else:
        use_this = [
            "identify whether placement refresh is needed before any render milestone",
            "avoid launching YMM4 while source validation is blocked",
        ]
    return {
        "use_this_package_to": use_this,
        "do_not_use_this_package_to": [
            "claim production visual quality",
            "claim public video readiness",
            "commit ignored .ymmp or render outputs",
            "introduce external TTS or real media",
        ],
    }


def _validation_expectations() -> dict[str, bool]:
    return {
        "json_parse_required": True,
        "focused_tests_required": True,
        "compileall_required": True,
        "git_diff_check_required": True,
        "git_cached_diff_check_required": True,
        "conflict_marker_scan_required": True,
        "forbidden_media_staging_scan_required": True,
        "YMM4_launched_by_agent": False,
        "render_created_by_agent": False,
    }


def _result_builder_source_validation(package: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if package.get("smoke_id") != CARD_PLACEMENT_POST_REFINEMENT_RENDER_SMOKE_ID:
        errors.append("SOURCE_PACKAGE_ID_MISMATCH")
    if package.get("package_status") != "ready_for_manual_milestone_render_smoke":
        errors.append("SOURCE_PACKAGE_NOT_READY")
    if package.get("smoke_status") != "prepared_not_run":
        errors.append("SOURCE_PACKAGE_SMOKE_STATUS_NOT_PREPARED")
    return {
        "status": "passed" if not errors else "blocked",
        "source_package_id": package.get("smoke_id"),
        "source_package_status": package.get("package_status"),
        "errors": errors,
    }


def _accepted_scope_from_classification(
    classification: dict[str, Any],
) -> dict[str, bool]:
    passed = classification.get("classification") == PASS_CLASSIFICATION
    return {
        "post_refinement_project_opened": passed,
        "render_completed": passed,
        "diagnostic_output_about_68_sec": passed,
        "four_refined_cards_visible_and_readable": passed,
        "dialogue_items_preserved": passed,
        "native_audio_present": passed,
        "production_ready": False,
        "public_video_ready": False,
    }


def _ymmp_card_image_summary(
    path: str | Path,
    refinement: dict[str, Any],
) -> dict[str, Any]:
    ymmp_path = Path(path)
    errors: list[str] = []
    if not ymmp_path.exists():
        return {
            "status": "blocked",
            "errors": ["TARGET_YMMP_MISSING"],
            "card_items": [],
        }
    try:
        data = load_ymmp(ymmp_path)
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "status": "blocked",
            "errors": [f"TARGET_YMMP_READ_FAILED:{exc}"],
            "card_items": [],
        }
    refined_card_ids = {
        row.get("card_id") for row in _list(refinement.get("design_changes"))
    }
    card_items = []
    for item in _get_timeline_items(data):
        remark = item.get("Remark")
        if (
            _item_type(item) == "ImageItem"
            and isinstance(remark, str)
            and remark.startswith(CARD_REMARK_PREFIX)
        ):
            card_id = remark.removeprefix(CARD_REMARK_PREFIX)
            card_items.append(
                {
                    "card_id": card_id,
                    "file_path": item.get("FilePath"),
                    "frame": item.get("Frame"),
                    "length": item.get("Length"),
                    "layer": item.get("Layer"),
                    "remark": remark,
                    "matches_refined_card": card_id in refined_card_ids,
                }
            )
    if len(card_items) != EXPECTED_CARD_COUNT:
        errors.append("TARGET_YMMP_CARD_IMAGE_ITEM_COUNT_NOT_4")
    if not all(row["matches_refined_card"] for row in card_items):
        errors.append("TARGET_YMMP_CARD_REMARKS_DO_NOT_MATCH_REFINED_CARDS")
    return {
        "status": "passed" if not errors else "blocked",
        "errors": errors,
        "card_items": card_items,
    }


def _classification_result(
    classification: str,
    result: str,
    reason: str,
    next_slice: str,
) -> dict[str, Any]:
    return {
        "classification": classification,
        "result": result,
        "reason": reason,
        "next_recommended_slice": next_slice,
    }


def _uncertain_result(reason: str) -> dict[str, Any]:
    return _classification_result(
        OPERATOR_UNCERTAIN_CLASSIFICATION,
        "blocked_by_operator_uncertainty",
        reason,
        OPERATOR_UNCERTAINTY_SLICE,
    )


def _duration_is_approx_68(duration_sec: float) -> bool:
    return abs(duration_sec - EXPECTED_DURATION_SEC) <= EXPECTED_DURATION_TOLERANCE_SEC


def _path_matches_reference(value: Any, repo_relative_path: str) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.replace("\\", "/")
    return normalized.endswith(repo_relative_path.replace("\\", "/"))


def _git_has_output(root: Path, args: list[str]) -> bool:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return bool(result.stdout.strip())


def _git_returncode_zero(root: Path, args: list[str]) -> bool:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def _append_status_table(lines: list[str], title: str, rows: Any) -> None:
    lines.extend(["", f"## {title}", "", "| item | status |", "|---|---|"])
    for row in rows if isinstance(rows, list) else []:
        key = row.get("gate") or row.get("artifact") or "item"
        lines.append(f"| {key} | {_display(row.get('status'))} |")


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


def _list_str(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _bool_or_unknown(value: Any) -> bool | str:
    if isinstance(value, bool):
        return value
    return "unknown"


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _intish(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _path_text(value: str | Path | None) -> str:
    return str(value).replace("\\", "/") if value is not None else ""


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, list):
        if not value:
            return "[]"
        return ", ".join(_display(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
