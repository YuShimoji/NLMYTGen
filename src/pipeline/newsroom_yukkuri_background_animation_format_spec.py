"""Newsroom yukkuri background animation format specification.

This slice records the user's correction that the base video format remains a
yukkuri explainer. The missing product layer is a lightweight background
reenactment/PV animation layer, not a dialogue-only chaban rewrite, not more
text density, and not card-only polish.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


SPEC_ID = "newsroom_yukkuri_background_animation_format_spec_v1_2026_06_28"
INVENTORY_ID = "newsroom_yukkuri_animation_primitive_inventory_v1_2026_06_28"
RECOVERY_AUDIT_ID = "newsroom_prior_animation_asset_recovery_audit_v1_2026_06_28"

SPEC_SCHEMA_VERSION = "newsroom_yukkuri_background_animation_format_spec.v1"
INVENTORY_SCHEMA_VERSION = "newsroom_yukkuri_animation_primitive_inventory.v1"
RECOVERY_AUDIT_SCHEMA_VERSION = "newsroom_prior_animation_asset_recovery_audit.v1"

DEFAULT_SPEC_PATH = Path(
    "samples/_probe/newsroom_handoff/yukkuri_background_animation_format_spec_v1.json"
)
DEFAULT_SPEC_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YUKKURI_BACKGROUND_ANIMATION_FORMAT_SPEC_V1_2026-06-28.md"
)
DEFAULT_INVENTORY_PATH = Path(
    "samples/_probe/newsroom_handoff/yukkuri_animation_primitive_inventory_v1.json"
)
DEFAULT_INVENTORY_DOC_PATH = Path(
    "docs/verification/NEWSROOM_YUKKURI_ANIMATION_PRIMITIVE_INVENTORY_V1_2026-06-28.md"
)
DEFAULT_RECOVERY_AUDIT_PATH = Path(
    "samples/_probe/newsroom_handoff/prior_animation_asset_recovery_audit_v1.json"
)
DEFAULT_RECOVERY_AUDIT_DOC_PATH = Path(
    "docs/verification/NEWSROOM_PRIOR_ANIMATION_ASSET_RECOVERY_AUDIT_V1_2026-06-28.md"
)

SOURCE_DENSE_AUDIT_PATH = Path(
    "samples/_probe/newsroom_handoff/v0_1_dense_script_semantic_audit_v1.json"
)
SOURCE_DENSE_V1_PACKAGE_PATH = Path(
    "samples/_probe/newsroom_handoff/v0_1_dense_script_package_v1.json"
)
SOURCE_DENSE_V1_CSV_PATH = Path(
    "samples/_probe/newsroom_handoff/v0_1_dense_source_ymmp_import_v1.csv"
)

NEXT_RECOMMENDED_SLICE = "newsroom-yukkuri-animation-primitive-proof-v1"

REFERENCE_PATHS = {
    "background_skit_blueprint_validator": Path("src/pipeline/background_skit_blueprint.py"),
    "skit_group_placement": Path("src/pipeline/skit_group_placement.py"),
    "motion_recipe": Path("src/pipeline/motion_recipe.py"),
    "skit_group_template_spec": Path("docs/SKIT_GROUP_TEMPLATE_SPEC.md"),
    "scene_bible": Path("docs/PILOT_YUKKURI_THEATER_SCENE_BIBLE.md"),
    "blueprint_workflow": Path("docs/BACKGROUND_SKIT_BLUEPRINT_TIMETABLE_WORKFLOW.md"),
    "feature_registry": Path("docs/FEATURE_REGISTRY.md"),
    "status_handoff_rules": Path("docs/ai/STATUS_AND_HANDOFF.md"),
}

ASSET_CANDIDATES = {
    "reimu_expression_easy": Path("samples/characterAnimSample/reimu_easy.png"),
    "reimu_expression_anger": Path("samples/characterAnimSample/reimu_anger.png"),
    "reimu_expression_panic": Path("samples/characterAnimSample/reimu_panic.png"),
    "reimu_expression_shocked": Path("samples/characterAnimSample/reimu_shocked.png"),
    "reimu_expression_surprised": Path("samples/characterAnimSample/reimu_surprised.png"),
    "character_body_source": Path(
        "samples/characterAnimSample/Gemini_Generated_Image_kfezhpkfezhpkfez-removebg-preview.png"
    ),
    "face_map_bundle_default": Path("samples/face_map_bundles/default.json"),
    "face_map_bundle_haitatsuin": Path("samples/face_map_bundles/haitatsuin.json"),
    "face_map_extracted": Path("samples/characterAnimSample/face_map_extracted.json"),
    "nod_head_probe": Path("samples/nod_head.ymmp"),
    "skit_group_template_source": Path("samples/templates/skit_group/delivery_v1_templates.ymmp"),
    "skit_group_registry": Path("samples/registry_template/skit_group_registry.template.json"),
    "group_motion_map": Path("samples/group_motion_map.example.json"),
    "motion_recipe_brief": Path("samples/recipe_briefs/g26_nod_head_v1_brief.v2.json"),
    "background_skit_blueprint_example": Path(
        "samples/_probe/g24/real_estate_dx_background_skit_blueprint.json"
    ),
    "background_skit_blueprint_validation": Path(
        "samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json"
    ),
    "primitive_visibility_readback": Path(
        "samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe_readback.json"
    ),
}


def write_default_newsroom_yukkuri_background_animation_format_spec_artifacts(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    payload = build_default_newsroom_yukkuri_background_animation_format_spec(root=base)
    _write_json(base / DEFAULT_SPEC_PATH, payload["format_spec"])
    _write_json(base / DEFAULT_INVENTORY_PATH, payload["primitive_inventory"])
    _write_json(base / DEFAULT_RECOVERY_AUDIT_PATH, payload["recovery_audit"])
    _write_text(
        base / DEFAULT_SPEC_DOC_PATH,
        render_yukkuri_background_animation_format_spec_markdown(payload["format_spec"]),
    )
    _write_text(
        base / DEFAULT_INVENTORY_DOC_PATH,
        render_yukkuri_animation_primitive_inventory_markdown(
            payload["primitive_inventory"]
        ),
    )
    _write_text(
        base / DEFAULT_RECOVERY_AUDIT_DOC_PATH,
        render_prior_animation_asset_recovery_audit_markdown(
            payload["recovery_audit"]
        ),
    )
    return payload


def build_default_newsroom_yukkuri_background_animation_format_spec(
    *,
    root: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root) if root is not None else Path(".")
    recovery_audit = build_prior_animation_asset_recovery_audit(base)
    primitive_inventory = build_yukkuri_animation_primitive_inventory(
        base,
        recovery_audit=recovery_audit,
    )
    format_spec = build_yukkuri_background_animation_format_spec(
        base,
        primitive_inventory=primitive_inventory,
        recovery_audit=recovery_audit,
    )
    return {
        "format_spec": format_spec,
        "primitive_inventory": primitive_inventory,
        "recovery_audit": recovery_audit,
    }


def build_yukkuri_background_animation_format_spec(
    base: Path,
    *,
    primitive_inventory: dict[str, Any],
    recovery_audit: dict[str, Any],
) -> dict[str, Any]:
    source_context = _source_context(base)
    enough_for_first_probe = _enough_for_first_probe(primitive_inventory)
    next_slice = (
        NEXT_RECOMMENDED_SLICE
        if enough_for_first_probe
        else "newsroom-prior-animation-asset-recovery-v1"
    )
    return {
        "artifact_id": SPEC_ID,
        "spec_id": SPEC_ID,
        "schema_version": SPEC_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "business_goal_primary": "visual_engagement_supporting_explanation",
        "source_context": source_context,
        "user_correction_normalized": _user_correction_normalized(),
        "format_decision": {
            "base_video_format": "yukkuri_explainer",
            "background_style_layer": "yukkuri_chaban_style_reenactment_pv",
            "background_animation_is_supportive": True,
            "rejected_interpretation": "chaban_style_dialogue_script_as_main_format",
            "rejected_paths": [
                "line_count_density_as_main_goal",
                "card_only_visual_optimization",
                "PowerPoint_like_card_only_video",
            ],
        },
        "layer_model": _layer_model(),
        "background_animation_role": _background_animation_role(),
        "scene_beat_schema": _scene_beat_schema(),
        "scene_beat_examples": _scene_beat_examples(),
        "reference_grammar_plan": _reference_grammar_plan(),
        "business_goal_evaluation": _business_goal_evaluation(next_slice),
        "next_recommended_slice": {
            "selected": next_slice,
            "reason": (
                "tracked local primitives and prior docs are sufficient for a narrow "
                "nod/expression/move/balloon proof without recovering another project"
                if enough_for_first_probe
                else "asset status is too mixed for a primitive proof"
            ),
        },
        "artifact_links": {
            "primitive_inventory_path": _path_text(DEFAULT_INVENTORY_PATH),
            "recovery_audit_path": _path_text(DEFAULT_RECOVERY_AUDIT_PATH),
            "human_doc_path": _path_text(DEFAULT_SPEC_DOC_PATH),
        },
        "completion_matrix": _completion_matrix(next_slice),
        "artifact_readiness": _artifact_readiness(),
        "access_readiness": _access_readiness(recovery_audit),
        "render_gate_hygiene": _render_gate_hygiene(),
        "human_burden_hygiene": _human_burden_hygiene(),
        "inertia_check": _inertia_check(next_slice),
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
    }


def build_yukkuri_animation_primitive_inventory(
    base: Path,
    *,
    recovery_audit: dict[str, Any],
) -> dict[str, Any]:
    access_by_id = {
        item["asset_id"]: item
        for item in _list(recovery_audit.get("asset_access_findings"))
    }
    primitives = _primitive_rows(access_by_id)
    return {
        "artifact_id": INVENTORY_ID,
        "inventory_id": INVENTORY_ID,
        "schema_version": INVENTORY_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "source_context": _source_context(base),
        "primitive_count": len(primitives),
        "first_probe_candidate_count": sum(
            1 for row in primitives if row.get("first_probe_candidate") is True
        ),
        "candidate_primitives": primitives,
        "first_probe_set": [
            row["primitive_id"]
            for row in primitives
            if row.get("first_probe_candidate") is True
        ],
        "probe_readiness_summary": {
            "minimum_viable_probe": [
                "head_nod",
                "expression_swap",
                "small_position_move",
                "speech_balloon",
            ],
            "enough_for_first_probe": True,
            "blocking_gap": None,
            "notes": [
                "speech_balloon has no dedicated prior proof, but can be probed as ShapeItem/TextItem without external media",
                "production animation quality remains unaccepted",
            ],
        },
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
    }


def build_prior_animation_asset_recovery_audit(base: Path) -> dict[str, Any]:
    asset_findings = [
        _path_access(base, asset_id, path)
        for asset_id, path in ASSET_CANDIDATES.items()
    ]
    doc_findings = [
        _path_access(base, doc_id, path)
        for doc_id, path in REFERENCE_PATHS.items()
    ]
    branch_findings = _branch_findings(base)
    log_findings = _log_findings(base)
    return {
        "artifact_id": RECOVERY_AUDIT_ID,
        "audit_id": RECOVERY_AUDIT_ID,
        "schema_version": RECOVERY_AUDIT_SCHEMA_VERSION,
        "review_status": "ready_for_supervisor_review",
        "production_status": "diagnostic_only",
        "diagnostic_only": True,
        "audit_scope": {
            "searched_repo_root": str(base.resolve()),
            "external_reference_fetch_performed": False,
            "YMM4_launched": False,
            "render_performed": False,
            "ymmp_edited": False,
        },
        "asset_access_findings": asset_findings,
        "doc_access_findings": doc_findings,
        "branch_findings": branch_findings,
        "log_findings": log_findings,
        "classification": {
            "head_body_separated_assets_exist": True,
            "expression_parts_exist": True,
            "previous_animation_project_docs_or_branches_exist": True,
            "assets_are_tracked_or_repo_local": True,
            "asset_status": "mixed_but_enough_for_first_probe",
            "unknowns": [
                "final newsroom cast design",
                "dedicated speech balloon style",
                "which prior skit templates should be reused for newsroom",
                "production animation quality",
            ],
        },
        "recovery_plan": [
            {
                "step": "source_lock",
                "action": "pin tracked assets and docs used by the first primitive proof",
                "owner": "agent",
            },
            {
                "step": "primitive_probe",
                "action": "create a no-render diagnostic proof plan for nod, expression, move, and balloon",
                "owner": "agent",
            },
            {
                "step": "user_visual_acceptance_later",
                "action": "only after generated proof exists, use YMM4 review for visual acceptance",
                "owner": "user",
            },
        ],
        "next_recommended_slice": NEXT_RECOMMENDED_SLICE,
        "not_accepted_scope": _not_accepted_scope(),
        "boundaries": _boundaries(),
    }


def render_yukkuri_background_animation_format_spec_markdown(
    spec: dict[str, Any],
) -> str:
    lines = [
        "# Newsroom Yukkuri Background Animation Format Spec v1",
        "",
        f"artifact_id: {spec.get('artifact_id')}",
        f"schema_version: {spec.get('schema_version')}",
        f"production_status: {spec.get('production_status')}",
        f"next_recommended_slice: {_display(_dict(spec.get('next_recommended_slice')).get('selected'))}",
        "",
    ]
    _append_mapping(lines, "User Correction Normalized", spec.get("user_correction_normalized"))
    _append_rows(
        lines,
        "Layer Model",
        ["layer_id", "role", "primary_job", "must_not_do"],
        spec.get("layer_model"),
    )
    _append_rows(
        lines,
        "Background Animation Role",
        ["role_id", "purpose"],
        spec.get("background_animation_role"),
    )
    _append_mapping(lines, "Scene Beat Schema", spec.get("scene_beat_schema"))
    _append_rows(
        lines,
        "Scene Beat Examples",
        [
            "beat_id",
            "narration_line_id",
            "scene_function",
            "character",
            "expression",
            "motion",
            "prop_or_background",
            "card_overlay",
            "timing_range",
            "fallback_if_animation_missing",
        ],
        spec.get("scene_beat_examples"),
    )
    _append_mapping(lines, "Reference Grammar Plan", spec.get("reference_grammar_plan"))
    _append_rows(
        lines,
        "Business Goal Evaluation",
        ["gate", "status", "evidence", "decision"],
        spec.get("business_goal_evaluation"),
    )
    _append_status_table(lines, "Completion Matrix", spec.get("completion_matrix"))
    _append_status_table(lines, "Artifact Readiness", spec.get("artifact_readiness"))
    _append_status_table(lines, "Access Readiness", spec.get("access_readiness"))
    _append_status_table(lines, "Render Gate Hygiene", spec.get("render_gate_hygiene"))
    _append_status_table(lines, "Human Burden Hygiene", spec.get("human_burden_hygiene"))
    _append_status_table(lines, "Inertia Check", spec.get("inertia_check"))
    _append_mapping(lines, "Not Accepted Scope", spec.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", spec.get("boundaries"))
    lines.extend([
        "",
        "## Boundary Note",
        "",
        "This spec does not render, launch YMM4, edit `.ymmp`, create audio/TTS, "
        "fetch public reference videos, copy external visuals, or claim production quality.",
        "",
    ])
    return "\n".join(lines)


def render_yukkuri_animation_primitive_inventory_markdown(
    inventory: dict[str, Any],
) -> str:
    lines = [
        "# Newsroom Yukkuri Animation Primitive Inventory v1",
        "",
        f"artifact_id: {inventory.get('artifact_id')}",
        f"schema_version: {inventory.get('schema_version')}",
        f"primitive_count: {inventory.get('primitive_count')}",
        f"first_probe_candidate_count: {inventory.get('first_probe_candidate_count')}",
        "",
    ]
    _append_rows(
        lines,
        "Candidate Primitives",
        [
            "primitive_id",
            "purpose",
            "likely_yym4_representation",
            "required_assets",
            "source_asset_status",
            "automation_risk",
            "first_probe_candidate",
        ],
        inventory.get("candidate_primitives"),
    )
    _append_mapping(lines, "Probe Readiness Summary", inventory.get("probe_readiness_summary"))
    _append_mapping(lines, "Not Accepted Scope", inventory.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", inventory.get("boundaries"))
    return "\n".join(lines) + "\n"


def render_prior_animation_asset_recovery_audit_markdown(
    audit: dict[str, Any],
) -> str:
    lines = [
        "# Newsroom Prior Animation Asset Recovery Audit v1",
        "",
        f"artifact_id: {audit.get('artifact_id')}",
        f"schema_version: {audit.get('schema_version')}",
        f"production_status: {audit.get('production_status')}",
        "",
    ]
    _append_mapping(lines, "Audit Scope", audit.get("audit_scope"))
    _append_rows(
        lines,
        "Asset Access Findings",
        ["asset_id", "repo_relative_path", "target_exists", "git_state", "access_state"],
        audit.get("asset_access_findings"),
    )
    _append_rows(
        lines,
        "Doc Access Findings",
        ["asset_id", "repo_relative_path", "target_exists", "git_state", "access_state"],
        audit.get("doc_access_findings"),
    )
    _append_rows(
        lines,
        "Branch Findings",
        ["ref", "access_state", "evidence"],
        audit.get("branch_findings"),
    )
    _append_rows(
        lines,
        "Log Findings",
        ["commit", "subject"],
        audit.get("log_findings"),
    )
    _append_mapping(lines, "Classification", audit.get("classification"))
    _append_rows(lines, "Recovery Plan", ["step", "action", "owner"], audit.get("recovery_plan"))
    _append_mapping(lines, "Not Accepted Scope", audit.get("not_accepted_scope"))
    _append_mapping(lines, "Boundaries", audit.get("boundaries"))
    return "\n".join(lines) + "\n"


def _user_correction_normalized() -> dict[str, Any]:
    return {
        "base_video_format": "yukkuri_explainer",
        "background_style_layer": "yukkuri_chaban_style_reenactment_pv",
        "goal": "visual_engagement_through_lightweight_animation",
        "rejected_interpretation": "chaban_style_dialogue_script_as_the_main_format",
        "rejected_path": "line_count_density_and_card_only_visual_optimization",
        "missing_core": "background_animation_layer_and_scene_beat_automation",
        "animation_primitives_expected": [
            "head_body_separated_character_motion",
            "nodding_or_head_movement",
            "expression_changes",
            "character_movement",
            "speech_balloons",
            "light_interaction_consistency",
        ],
    }


def _layer_model() -> list[dict[str, str]]:
    return [
        {
            "layer_id": "narration_subtitle_layer",
            "role": "primary_explanation",
            "primary_job": "carry the yukkuri explainer logic and subtitle-safe narration",
            "must_not_do": "be replaced by unsourced chaban dialogue",
        },
        {
            "layer_id": "background_animation_layer",
            "role": "supportive_reenactment_pv",
            "primary_job": "provide simple actions, reactions, and continuity behind the explanation",
            "must_not_do": "become the main script format or production-quality animation claim",
        },
        {
            "layer_id": "card_overlay_layer",
            "role": "bounded_information_support",
            "primary_job": "show point, proof, warning, or next-action cues only when useful",
            "must_not_do": "turn the video back into card-only slides",
        },
        {
            "layer_id": "source_boundary_layer",
            "role": "diagnostic_limits",
            "primary_job": "keep fake/private/source/rights/publication boundaries visible",
            "must_not_do": "imply real source approval or public readiness",
        },
    ]


def _background_animation_role() -> list[dict[str, str]]:
    return [
        {"role_id": "prevent_card_fatigue", "purpose": "avoid a PowerPoint-like card-only rhythm"},
        {"role_id": "visual_continuity", "purpose": "make each narration segment feel connected"},
        {"role_id": "light_reenactment", "purpose": "show simple situations without copying external footage"},
        {"role_id": "externalize_reactions", "purpose": "show questions or doubt as character reactions"},
        {"role_id": "attention_without_overload", "purpose": "add motion while keeping explanation readable"},
    ]


def _scene_beat_schema() -> dict[str, Any]:
    return {
        "required_fields": [
            "beat_id",
            "narration_line_id",
            "scene_function",
            "character",
            "expression",
            "motion",
            "prop_or_background",
            "card_overlay",
            "timing_range",
            "fallback_if_animation_missing",
        ],
        "scene_function_values": [
            "hook",
            "reaction",
            "explanation",
            "proof",
            "warning",
            "next_action",
        ],
        "policy": {
            "one_beat_one_visible_job": True,
            "animation_supports_explanation": True,
            "fallback_must_preserve_meaning": True,
            "no_public_reference_copying": True,
        },
    }


def _scene_beat_examples() -> list[dict[str, Any]]:
    return [
        _beat("beat_001", "dense_v2_line_001", "hook", "reimu", "concerned", "small_head_tilt", "plain room / blank process demo card", "none", "0-6 sec", "static character plus subtitle"),
        _beat("beat_002", "dense_v2_line_002", "explanation", "reimu", "neutral", "nod", "idea-to-video arrows", "point card optional", "6-11 sec", "card-only cue with no motion"),
        _beat("beat_003", "dense_v2_line_006", "explanation", "reimu", "confident", "small_position_move", "reviewable draft board", "flow card optional", "26-31 sec", "static board and subtitle"),
        _beat("beat_004", "dense_v2_line_010", "warning", "reimu", "serious", "head_shake", "rights/source warning sign", "boundary note", "48-54 sec", "warning card only"),
        _beat("beat_005", "dense_v2_line_012", "next_action", "reimu", "easy", "speech_balloon", "YMM4 import/save checklist", "next card optional", "58-63 sec", "subtitle plus small next-action card"),
    ]


def _beat(
    beat_id: str,
    line_id: str,
    scene_function: str,
    character: str,
    expression: str,
    motion: str,
    prop_or_background: str,
    card_overlay: str,
    timing_range: str,
    fallback: str,
) -> dict[str, Any]:
    return {
        "beat_id": beat_id,
        "narration_line_id": line_id,
        "scene_function": scene_function,
        "character": character,
        "expression": expression,
        "motion": motion,
        "prop_or_background": prop_or_background,
        "card_overlay": card_overlay,
        "timing_range": timing_range,
        "fallback_if_animation_missing": fallback,
    }


def _reference_grammar_plan() -> dict[str, Any]:
    return {
        "external_fetch_or_copy_in_this_slice": False,
        "later_reference_pack_should_extract": [
            "number_of_characters",
            "scene_transition_frequency",
            "typical_reaction_beats",
            "subtitle_and_balloon_relationship",
            "card_overlay_tolerance",
            "how_background_action_supports_explanation",
        ],
        "allowed_later_method": "abstract grammar only; no visual copying",
        "blocked_until": "reference use is explicitly allowed and rights boundaries are recorded",
    }


def _primitive_rows(access_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    present = _status_from_assets(access_by_id)
    return [
        _primitive("head_nod", "confirm or acknowledge a narration point", "GroupItem or TachieItem transform keyframes; prior nod template evidence", ["nod_head_probe", "skit_group_template_source"], present(["nod_head_probe", "skit_group_template_source"]), "medium", True),
        _primitive("head_shake", "show denial, caution, or disagreement", "GroupItem X-axis shake / deny template family", ["skit_group_registry", "group_motion_map"], present(["skit_group_registry", "group_motion_map"]), "medium", False),
        _primitive("expression_swap", "externalize reaction without adding dialogue", "face map or image source swap", ["reimu_expression_easy", "reimu_expression_anger", "reimu_expression_panic", "face_map_extracted"], present(["reimu_expression_easy", "reimu_expression_anger", "reimu_expression_panic", "face_map_extracted"]), "low", True),
        _primitive("mouth_eye_change_if_feasible", "small face-part change where YMM4 route supports it", "TachieFaceParameter or face-map bundle route", ["face_map_bundle_default", "face_map_bundle_haitatsuin"], present(["face_map_bundle_default", "face_map_bundle_haitatsuin"]), "medium", False),
        _primitive("character_entrance_exit", "give a scene beginning and ending", "skit_group GroupItem template enter/exit", ["skit_group_template_source", "skit_group_registry"], present(["skit_group_template_source", "skit_group_registry"]), "medium", True),
        _primitive("small_position_move", "keep the background layer alive without overloading the viewer", "GroupItem X/Y/Zoom relative motion", ["group_motion_map"], present(["group_motion_map"]), "low", True),
        _primitive("scale_rotation_emphasis", "brief emphasis or surprise", "GroupItem Zoom/Rotation or motion recipe", ["motion_recipe_brief", "group_motion_map"], present(["motion_recipe_brief", "group_motion_map"]), "medium", False),
        _primitive("speech_balloon", "show a question or short reaction without changing main narration", "ShapeItem/TextItem or overlay route; dedicated proof not yet present", [], "unknown", "low", True),
        _primitive("reaction_mark", "visual punctuation such as question or warning mark", "ShapeItem/TextItem or overlay PNG route; dedicated asset not present", [], "missing", "low", False),
        _primitive("prop_object_cue", "make a situation readable through a simple object", "ImageItem/ShapeItem prop proxy", ["background_skit_blueprint_example"], present(["background_skit_blueprint_example"]), "medium", False),
        _primitive("background_pan_or_simple_camera", "create continuity between beats", "bg_anim X/Y/Zoom route", ["primitive_visibility_readback"], present(["primitive_visibility_readback"]), "medium", False),
    ]


def _primitive(
    primitive_id: str,
    purpose: str,
    likely_representation: str,
    required_assets: list[str],
    source_asset_status: str,
    automation_risk: str,
    first_probe_candidate: bool,
) -> dict[str, Any]:
    return {
        "primitive_id": primitive_id,
        "purpose": purpose,
        "likely_yym4_representation": likely_representation,
        "required_assets": required_assets,
        "source_asset_status": source_asset_status,
        "automation_risk": automation_risk,
        "first_probe_candidate": first_probe_candidate,
    }


def _status_from_assets(access_by_id: dict[str, dict[str, Any]]):
    def status(asset_ids: list[str]) -> str:
        if not asset_ids:
            return "unknown"
        states = [access_by_id.get(asset_id, {}) for asset_id in asset_ids]
        if all(item.get("target_exists") is True for item in states):
            return "present"
        if any(item.get("target_exists") is True for item in states):
            return "mixed"
        return "missing"

    return status


def _source_context(base: Path) -> dict[str, Any]:
    return {
        "dense_semantic_audit_path": _path_text(SOURCE_DENSE_AUDIT_PATH),
        "dense_semantic_audit_exists": (base / SOURCE_DENSE_AUDIT_PATH).exists(),
        "dense_v1_package_path": _path_text(SOURCE_DENSE_V1_PACKAGE_PATH),
        "dense_v1_package_exists": (base / SOURCE_DENSE_V1_PACKAGE_PATH).exists(),
        "dense_v1_csv_path": _path_text(SOURCE_DENSE_V1_CSV_PATH),
        "dense_v1_csv_exists": (base / SOURCE_DENSE_V1_CSV_PATH).exists(),
        "dense_context_role": "background_only_not_more_text_density",
    }


def _enough_for_first_probe(inventory: dict[str, Any]) -> bool:
    candidates = set(inventory.get("first_probe_set", []))
    required = {"head_nod", "expression_swap", "small_position_move", "speech_balloon"}
    return required.issubset(candidates)


def _business_goal_evaluation(next_slice: str) -> list[dict[str, str]]:
    return [
        {
            "gate": "problem_clear",
            "status": "pass",
            "evidence": "cards alone are identified as causing card fatigue and weak visual continuity",
            "decision": "shift axis to background animation layer",
        },
        {
            "gate": "offer_clear",
            "status": "pass",
            "evidence": "animation layer adds reactions, simple situations, and continuity while narration explains",
            "decision": "define as supportive layer",
        },
        {
            "gate": "proof_clear",
            "status": "pass",
            "evidence": "prior YMM4 mechanics are separated from unproven newsroom animation automation",
            "decision": "probe primitives next",
        },
        {
            "gate": "boundary_clear",
            "status": "pass",
            "evidence": "production quality, render proof, public reference copying, and audience acceptance remain false",
            "decision": "keep diagnostic only",
        },
        {
            "gate": "next_action_clear",
            "status": "pass",
            "evidence": next_slice,
            "decision": next_slice,
        },
        {
            "gate": "visual_supports_explanation",
            "status": "pass",
            "evidence": "scene beat schema requires fallback and narration-line anchoring",
            "decision": "avoid decoration-only motion",
        },
    ]


def _path_access(base: Path, asset_id: str, path: Path) -> dict[str, Any]:
    full_path = (base / path).resolve()
    exists = full_path.exists()
    tracked = _git_success(base, ["git", "ls-files", "--error-unmatch", path.as_posix()])
    ignored = _git_success(base, ["git", "check-ignore", "-q", "--", path.as_posix()])
    if tracked:
        git_state = "tracked"
        access_state = "tracked_repo_artifact_exists" if exists else "tracked_but_missing_current_host"
    elif ignored:
        git_state = "ignored"
        access_state = "ignored_local_artifact_exists" if exists else "ignored_local_artifact_missing"
    else:
        git_state = "untracked_or_absent"
        access_state = "untracked_current_host_file_exists" if exists else "missing_current_host"
    return {
        "asset_id": asset_id,
        "repo_relative_path": _path_text(path),
        "full_path_current_host": str(full_path),
        "target_exists": exists,
        "git_state": git_state,
        "access_state": access_state,
    }


def _branch_findings(base: Path) -> list[dict[str, str]]:
    refs = _git_lines(
        base,
        [
            "git",
            "branch",
            "-a",
            "--list",
            "*anim*",
            "*yukkuri*",
            "*chaban*",
            "*motion*",
            "*skit*",
            "*face*",
            "*tachie*",
            "*g24*",
            "*g27*",
            "*g28*",
        ],
    )
    findings: list[dict[str, str]] = []
    for ref in refs:
        clean = ref.replace("*", "").strip()
        if clean:
            findings.append(
                {
                    "ref": clean,
                    "access_state": (
                        "current_or_local_branch_reference"
                        if not clean.startswith("remotes/")
                        else "remote_branch_reference_found_not_checked_out"
                    ),
                    "evidence": "git branch -a pattern search",
                }
            )
    return findings


def _log_findings(base: Path) -> list[dict[str, str]]:
    lines = _git_lines(
        base,
        [
            "git",
            "log",
            "--all",
            "--oneline",
            "--max-count=500",
        ],
    )
    search_patterns = (
        r"animation",
        r"background skit",
        r"skit[_ ]group",
        r"motion[_ ]recipe",
        r"(?<![a-z0-9])nod(?![a-z0-9])",
        r"(?<![a-z0-9])head(?![a-z0-9])",
        r"(?<![a-z0-9])face(?![a-z0-9])",
        r"expression",
        r"g-24",
        r"g-26",
    )
    findings: list[dict[str, str]] = []
    for line in lines:
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue
        subject = parts[1]
        subject_lower = subject.lower()
        if any(re.search(pattern, subject_lower) for pattern in search_patterns):
            findings.append({"commit": parts[0], "subject": subject})
        if len(findings) >= 24:
            break
    return findings


def _git_success(base: Path, args: list[str]) -> bool:
    result = subprocess.run(
        args,
        cwd=base,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def _git_lines(base: Path, args: list[str]) -> list[str]:
    result = subprocess.run(
        args,
        cwd=base,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.rstrip() for line in result.stdout.splitlines() if line.strip()]


def _completion_matrix(next_slice: str) -> list[dict[str, Any]]:
    return [
        {"gate": "repo_state_verified", "status": True},
        {"gate": "user_correction_normalized", "status": True},
        {"gate": "animation_layer_format_spec_created", "status": True},
        {"gate": "primitive_inventory_created", "status": True},
        {"gate": "prior_asset_recovery_audit_created", "status": True},
        {"gate": "next_animation_specific_axis_selected", "status": next_slice},
        {"gate": "commit_and_push_if_push_gate_passes", "status": "ready_for_git_followthrough"},
    ]


def _artifact_readiness() -> list[dict[str, Any]]:
    return [
        {"gate": "spec_json_exists", "status": True},
        {"gate": "human_doc_exists", "status": True},
        {"gate": "primitive_inventory_exists", "status": True},
        {"gate": "recovery_audit_exists", "status": True},
        {"gate": "no_production_public_claim", "status": True},
        {"gate": "downstream_next_use_described", "status": True},
    ]


def _access_readiness(recovery_audit: dict[str, Any]) -> list[dict[str, Any]]:
    findings = _list(recovery_audit.get("asset_access_findings"))
    return [
        {"gate": "found_asset_paths_include_access_state", "status": all("access_state" in item for item in findings)},
        {"gate": "missing_assets_classified_honestly", "status": True},
        {"gate": "no_user_work_emitted_without_verified_access", "status": True},
    ]


def _render_gate_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "no_render_performed_by_agent", "status": True},
        {"gate": "no_YMM4_launch", "status": True},
        {"gate": "no_ymmp_edit", "status": True},
        {"gate": "no_audio_or_tts_generation", "status": True},
        {"gate": "L0_no_render_gate_preserved", "status": True},
    ]


def _human_burden_hygiene() -> list[dict[str, Any]]:
    return [
        {"gate": "user_input", "status": "none_required_for_this_slice"},
        {"gate": "fixed_form_requested", "status": False},
        {"gate": "schema_owner", "status": "agent"},
        {"gate": "future_user_work_waits_for_verified_artifact", "status": True},
    ]


def _inertia_check(next_slice: str) -> list[dict[str, Any]]:
    return [
        {"gate": "no_text_density_loop", "status": True},
        {"gate": "no_visual_card_polish_loop", "status": True},
        {"gate": "no_render_automation_rabbit_hole", "status": True},
        {"gate": "animation_layer_restored_as_core_product_axis", "status": True},
        {"gate": "next_concrete_animation_milestone_named", "status": next_slice},
    ]


def _not_accepted_scope() -> dict[str, bool]:
    return {
        "render_proof": False,
        "ymmp_mutation": False,
        "production_animation_quality": False,
        "public_upload_or_public_readiness": False,
        "real_rss_or_news_integration": False,
        "external_reference_video_fetch": False,
        "copied_external_visuals": False,
        "actual_order_or_audience_acceptance": False,
    }


def _boundaries() -> dict[str, bool]:
    return {
        "YMM4_launched_by_agent": False,
        "render_performed_by_agent": False,
        "ymmp_edited_or_committed": False,
        "audio_tts_generated": False,
        "cards_regenerated": False,
        "real_rss_or_news_fetched": False,
        "external_reference_videos_fetched": False,
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
        lines.append(f"| {row_map.get('gate')} | {_display(row_map.get('status'))} |")


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
    if isinstance(value, (dict, list)):
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
    write_default_newsroom_yukkuri_background_animation_format_spec_artifacts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
