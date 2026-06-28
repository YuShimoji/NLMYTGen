import json
from pathlib import Path

from src.pipeline.newsroom_yukkuri_animation_primitive_proof import (
    DEFAULT_PROOF_DOC_PATH,
    DEFAULT_PROOF_PATH,
    DEFAULT_SCENE_BEAT_DOC_PATH,
    DEFAULT_SCENE_BEAT_PATH,
    LOCAL_IGNORED_PROBE_PATH,
    NEXT_AXIS_RENDER_SMOKE,
    SELECTED_PRIMITIVES,
    build_default_newsroom_yukkuri_animation_primitive_proof,
    render_yukkuri_animation_primitive_proof_markdown,
    render_yukkuri_animation_scene_beat_probe_markdown,
)


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _by_id(rows: list[dict], key: str) -> dict[str, dict]:
    return {row[key]: row for row in rows}


def test_primitive_proof_matches_builder_and_selects_expected_subset() -> None:
    payload = build_default_newsroom_yukkuri_animation_primitive_proof(root=ROOT)
    proof = _load(DEFAULT_PROOF_PATH)

    assert proof == payload["primitive_proof"]
    assert proof["production_status"] == "diagnostic_only"
    assert proof["diagnostic_only"] is True
    assert proof["render_gate"] == "L0_no_render"
    assert proof["selected_primitive_ids"] == SELECTED_PRIMITIVES
    assert proof["proof_summary"] == {
        "selected_count": 5,
        "pass_count": 4,
        "partial_count": 1,
        "blocked_count": 0,
        "structurally_provable_count": 4,
        "enough_for_next_render_smoke_axis": True,
        "local_ignored_probe_created": False,
    }
    assert proof["next_recommended_axis"]["selected"] == NEXT_AXIS_RENDER_SMOKE


def test_primitive_statuses_are_structural_not_render_acceptance() -> None:
    proof = _load(DEFAULT_PROOF_PATH)
    primitive_by_id = _by_id(proof["primitive_proofs"], "primitive_id")

    assert primitive_by_id["head_nod"]["proof_status"] == "pass"
    assert primitive_by_id["expression_swap"]["proof_status"] == "pass"
    assert primitive_by_id["character_entrance_exit"]["proof_status"] == "pass"
    assert primitive_by_id["small_position_move"]["proof_status"] == "pass"
    assert primitive_by_id["speech_balloon"]["proof_status"] == "partial"
    assert primitive_by_id["speech_balloon"]["can_prove_without_render"] is True
    assert "ShapeItem/TextItem" in primitive_by_id["speech_balloon"][
        "ymm4_representation_candidate"
    ]

    evidence = proof["structural_evidence"]
    assert evidence["head_nod"]["group_item_count"] >= 2
    assert evidence["head_nod"]["image_item_count"] >= 2
    assert any(len(route) >= 3 for route in evidence["head_nod"]["rotation_routes"])
    assert evidence["character_entrance_exit"]["has_template_analysis"] is True
    assert evidence["small_position_move"]["relative_motion_ids"] == [
        "approach",
        "nudge_left",
        "nudge_right",
        "retreat",
    ]


def test_asset_access_state_has_required_fields_and_truthful_local_probe() -> None:
    proof = _load(DEFAULT_PROOF_PATH)
    access = _by_id(proof["asset_access_state"], "artifact_id")

    required_fields = {
        "artifact_id",
        "repo_relative_path",
        "folder_full_path_current_host",
        "file_full_path_current_host",
        "target_exists",
        "access_state",
        "access_evidence_level",
        "evidence_source",
        "artifact_kind",
    }
    assert all(required_fields.issubset(row) for row in proof["asset_access_state"])
    for artifact_id in [
        "nod_head_probe",
        "reimu_expression_easy",
        "character_body_source",
        "skit_group_template_source",
        "skit_group_registry",
        "group_motion_map",
    ]:
        assert access[artifact_id]["target_exists"] is True
        assert access[artifact_id]["git_state"] == "tracked"
        assert access[artifact_id]["access_state"] == "tracked_repo_artifact_exists"

    local_probe = proof["local_ignored_output"]
    assert local_probe["repo_relative_path"] == LOCAL_IGNORED_PROBE_PATH.as_posix()
    assert local_probe["target_exists"] is False
    assert local_probe["git_state"] == "ignored"
    assert local_probe["created_in_this_slice"] is False
    assert local_probe["reason"].startswith("not created; this slice")


def test_scene_beat_probe_maps_narration_to_animation_without_dense_rewrite() -> None:
    payload = build_default_newsroom_yukkuri_animation_primitive_proof(root=ROOT)
    probe = _load(DEFAULT_SCENE_BEAT_PATH)

    assert probe == payload["scene_beat_probe"]
    assert probe["production_status"] == "diagnostic_only"
    assert probe["scene_beat_policy"]["not_a_dense_script_rewrite"] is True
    assert len(probe["beats"]) == 5
    assert probe["primitive_coverage"]["all_selected_primitives_used"] is True
    assert set(probe["primitive_coverage"]["coverage"]) == set(SELECTED_PRIMITIVES)
    assert all("narration_or_caption_role" in beat for beat in probe["beats"])
    assert all("fallback_if_animation_missing" in beat for beat in probe["beats"])
    assert probe["next_recommended_axis"] == NEXT_AXIS_RENDER_SMOKE


def test_boundaries_and_readiness_matrices_stay_no_render() -> None:
    proof = _load(DEFAULT_PROOF_PATH)
    probe = _load(DEFAULT_SCENE_BEAT_PATH)

    assert len(proof["completion_matrix"]) == 8
    assert len(proof["access_readiness"]) == 4
    assert len(proof["inertia_check"]) == 5
    assert all(row["status"] for row in proof["access_readiness"])
    assert all(row["status"] is True for row in proof["inertia_check"][:4])
    for artifact in [proof, probe]:
        assert artifact["render_gate"] == "L0_no_render"
        assert set(artifact["boundaries"].values()) == {False}
        assert set(artifact["not_accepted_scope"].values()) == {False}


def test_markdown_outputs_match_renderers() -> None:
    proof = _load(DEFAULT_PROOF_PATH)
    probe = _load(DEFAULT_SCENE_BEAT_PATH)

    assert (ROOT / DEFAULT_PROOF_DOC_PATH).read_text(encoding="utf-8") == (
        render_yukkuri_animation_primitive_proof_markdown(proof)
    )
    assert (ROOT / DEFAULT_SCENE_BEAT_DOC_PATH).read_text(encoding="utf-8") == (
        render_yukkuri_animation_scene_beat_probe_markdown(probe)
    )


def test_no_forbidden_media_or_external_reference_outputs_created() -> None:
    generated_paths = [
        ROOT / DEFAULT_PROOF_PATH,
        ROOT / DEFAULT_PROOF_DOC_PATH,
        ROOT / DEFAULT_SCENE_BEAT_PATH,
        ROOT / DEFAULT_SCENE_BEAT_DOC_PATH,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in generated_paths)

    assert "http://" not in combined
    assert "https://" not in combined
    assert "www." not in combined
    assert "render again" not in combined.lower()

    handoff_dir = ROOT / "samples/_probe/newsroom_handoff"
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    generated_like = [
        *handoff_dir.glob("yukkuri_animation_primitive_proof_v1.*"),
        *handoff_dir.glob("yukkuri_animation_scene_beat_probe_v1.*"),
    ]
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_like)
