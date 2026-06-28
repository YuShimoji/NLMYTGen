import json
from pathlib import Path

from src.pipeline.newsroom_yukkuri_background_animation_format_spec import (
    DEFAULT_INVENTORY_DOC_PATH,
    DEFAULT_INVENTORY_PATH,
    DEFAULT_RECOVERY_AUDIT_DOC_PATH,
    DEFAULT_RECOVERY_AUDIT_PATH,
    DEFAULT_SPEC_DOC_PATH,
    DEFAULT_SPEC_PATH,
    NEXT_RECOMMENDED_SLICE,
    build_default_newsroom_yukkuri_background_animation_format_spec,
    render_prior_animation_asset_recovery_audit_markdown,
    render_yukkuri_animation_primitive_inventory_markdown,
    render_yukkuri_background_animation_format_spec_markdown,
)


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _by_id(rows: list[dict], key: str) -> dict[str, dict]:
    return {row[key]: row for row in rows}


def test_spec_matches_builder_and_normalizes_user_correction() -> None:
    payload = build_default_newsroom_yukkuri_background_animation_format_spec(root=ROOT)
    spec = _load(DEFAULT_SPEC_PATH)

    assert spec == payload["format_spec"]
    assert spec["production_status"] == "diagnostic_only"
    assert spec["diagnostic_only"] is True
    correction = spec["user_correction_normalized"]
    assert correction["base_video_format"] == "yukkuri_explainer"
    assert correction["background_style_layer"] == "yukkuri_chaban_style_reenactment_pv"
    assert correction["rejected_interpretation"] == (
        "chaban_style_dialogue_script_as_the_main_format"
    )
    assert correction["rejected_path"] == (
        "line_count_density_and_card_only_visual_optimization"
    )
    assert spec["format_decision"]["background_animation_is_supportive"] is True
    assert spec["next_recommended_slice"]["selected"] == NEXT_RECOMMENDED_SLICE


def test_layer_model_scene_schema_and_business_gates() -> None:
    spec = _load(DEFAULT_SPEC_PATH)

    layers = _by_id(spec["layer_model"], "layer_id")
    assert set(layers) == {
        "narration_subtitle_layer",
        "background_animation_layer",
        "card_overlay_layer",
        "source_boundary_layer",
    }
    assert layers["background_animation_layer"]["role"] == "supportive_reenactment_pv"

    schema = spec["scene_beat_schema"]
    assert schema["required_fields"] == [
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
    ]
    assert schema["policy"]["animation_supports_explanation"] is True
    assert {gate["status"] for gate in spec["business_goal_evaluation"]} == {"pass"}
    assert {gate["gate"] for gate in spec["business_goal_evaluation"]} == {
        "problem_clear",
        "offer_clear",
        "proof_clear",
        "boundary_clear",
        "next_action_clear",
        "visual_supports_explanation",
    }
    assert len(spec["scene_beat_examples"]) >= 5
    assert all("fallback_if_animation_missing" in beat for beat in spec["scene_beat_examples"])


def test_primitive_inventory_has_required_primitives_and_probe_set() -> None:
    payload = build_default_newsroom_yukkuri_background_animation_format_spec(root=ROOT)
    inventory = _load(DEFAULT_INVENTORY_PATH)

    assert inventory == payload["primitive_inventory"]
    assert inventory["primitive_count"] == 11
    assert inventory["first_probe_candidate_count"] == 5
    primitives = _by_id(inventory["candidate_primitives"], "primitive_id")
    assert set(primitives) == {
        "head_nod",
        "head_shake",
        "expression_swap",
        "mouth_eye_change_if_feasible",
        "character_entrance_exit",
        "small_position_move",
        "scale_rotation_emphasis",
        "speech_balloon",
        "reaction_mark",
        "prop_object_cue",
        "background_pan_or_simple_camera",
    }
    assert primitives["head_nod"]["source_asset_status"] == "present"
    assert primitives["expression_swap"]["source_asset_status"] == "present"
    assert primitives["speech_balloon"]["source_asset_status"] == "unknown"
    assert primitives["reaction_mark"]["source_asset_status"] == "missing"
    assert inventory["first_probe_set"] == [
        "head_nod",
        "expression_swap",
        "character_entrance_exit",
        "small_position_move",
        "speech_balloon",
    ]
    assert inventory["probe_readiness_summary"]["enough_for_first_probe"] is True


def test_prior_asset_recovery_audit_uses_tracked_access_evidence() -> None:
    payload = build_default_newsroom_yukkuri_background_animation_format_spec(root=ROOT)
    audit = _load(DEFAULT_RECOVERY_AUDIT_PATH)

    expected = dict(payload["recovery_audit"])
    actual = dict(audit)
    expected.pop("log_findings", None)
    actual.pop("log_findings", None)
    assert actual == expected
    assert audit["log_findings"]
    assets = _by_id(audit["asset_access_findings"], "asset_id")
    docs = _by_id(audit["doc_access_findings"], "asset_id")
    for asset_id in [
        "reimu_expression_easy",
        "character_body_source",
        "nod_head_probe",
        "skit_group_template_source",
        "group_motion_map",
    ]:
        assert assets[asset_id]["target_exists"] is True
        assert assets[asset_id]["git_state"] == "tracked"
        assert assets[asset_id]["access_state"] == "tracked_repo_artifact_exists"

    for doc_id in [
        "background_skit_blueprint_validator",
        "skit_group_placement",
        "motion_recipe",
        "skit_group_template_spec",
    ]:
        assert docs[doc_id]["target_exists"] is True
        assert docs[doc_id]["git_state"] == "tracked"

    classification = audit["classification"]
    assert classification["head_body_separated_assets_exist"] is True
    assert classification["expression_parts_exist"] is True
    assert classification["previous_animation_project_docs_or_branches_exist"] is True
    assert classification["asset_status"] == "mixed_but_enough_for_first_probe"
    branch_refs = " ".join(row["ref"].lower() for row in audit["branch_findings"])
    log_subjects = " ".join(row["subject"].lower() for row in audit["log_findings"])
    assert "g24" in branch_refs or "g-24" in log_subjects
    assert "skit" in log_subjects or "motion" in log_subjects


def test_readiness_matrices_and_boundaries_are_diagnostic_only() -> None:
    spec = _load(DEFAULT_SPEC_PATH)
    inventory = _load(DEFAULT_INVENTORY_PATH)
    audit = _load(DEFAULT_RECOVERY_AUDIT_PATH)

    assert len(spec["completion_matrix"]) == 7
    assert len(spec["artifact_readiness"]) == 6
    assert len(spec["access_readiness"]) == 3
    assert len(spec["inertia_check"]) == 5
    assert {row["status"] for row in spec["artifact_readiness"]} == {True}
    assert {row["status"] for row in spec["access_readiness"]} == {True}
    assert all(row["status"] is True for row in spec["render_gate_hygiene"])
    assert all(row["status"] is True for row in spec["inertia_check"][:4])

    for artifact in [spec, inventory, audit]:
        assert artifact["production_status"] == "diagnostic_only"
        assert artifact["diagnostic_only"] is True
        assert set(artifact["boundaries"].values()) == {False}
        assert set(artifact["not_accepted_scope"].values()) == {False}


def test_markdown_outputs_match_renderers() -> None:
    spec = _load(DEFAULT_SPEC_PATH)
    inventory = _load(DEFAULT_INVENTORY_PATH)
    audit = _load(DEFAULT_RECOVERY_AUDIT_PATH)

    assert (ROOT / DEFAULT_SPEC_DOC_PATH).read_text(encoding="utf-8") == (
        render_yukkuri_background_animation_format_spec_markdown(spec)
    )
    assert (ROOT / DEFAULT_INVENTORY_DOC_PATH).read_text(encoding="utf-8") == (
        render_yukkuri_animation_primitive_inventory_markdown(inventory)
    )
    assert (ROOT / DEFAULT_RECOVERY_AUDIT_DOC_PATH).read_text(encoding="utf-8") == (
        render_prior_animation_asset_recovery_audit_markdown(audit)
    )


def test_no_forbidden_media_or_external_reference_outputs_created() -> None:
    generated_paths = [
        ROOT / DEFAULT_SPEC_PATH,
        ROOT / DEFAULT_SPEC_DOC_PATH,
        ROOT / DEFAULT_INVENTORY_PATH,
        ROOT / DEFAULT_INVENTORY_DOC_PATH,
        ROOT / DEFAULT_RECOVERY_AUDIT_PATH,
        ROOT / DEFAULT_RECOVERY_AUDIT_DOC_PATH,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in generated_paths)

    assert "http://" not in combined
    assert "https://" not in combined
    assert "www." not in combined
    assert "render again" not in combined.lower()

    handoff_dir = ROOT / "samples/_probe/newsroom_handoff"
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    generated_like = [
        *handoff_dir.glob("yukkuri_background_animation_format_spec_v1.*"),
        *handoff_dir.glob("yukkuri_animation_primitive_inventory_v1.*"),
        *handoff_dir.glob("prior_animation_asset_recovery_audit_v1.*"),
    ]
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_like)
