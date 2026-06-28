import json
import subprocess
from pathlib import Path

from src.pipeline.newsroom_yukkuri_animation_primitive_probe_materialization import (
    DEFAULT_MATERIALIZATION_DOC_PATH,
    DEFAULT_MATERIALIZATION_PATH,
    LOCAL_IGNORED_PROBE_PATH,
    NEXT_AXIS_RENDER_SMOKE,
    PROVEN_PRIMITIVES,
    build_default_newsroom_yukkuri_animation_primitive_probe_materialization,
    materialize_local_primitive_probe_ymmp,
    render_newsroom_yukkuri_animation_primitive_probe_materialization_markdown,
)
from src.pipeline.ymmp_patch import _get_timeline_items, _item_type, load_ymmp


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _ensure_local_probe() -> None:
    materialize_local_primitive_probe_ymmp(root=ROOT)


def test_materialization_artifact_matches_builder_and_verifies_ignored_probe() -> None:
    _ensure_local_probe()
    payload = build_default_newsroom_yukkuri_animation_primitive_probe_materialization(
        root=ROOT
    )
    artifact = _load(DEFAULT_MATERIALIZATION_PATH)

    assert artifact == payload
    assert artifact["production_status"] == "diagnostic_only"
    assert artifact["diagnostic_only"] is True
    assert artifact["render_gate"] == "L0_no_render"
    assert artifact["materialization_status"] == "materialized_ignored_local_probe"
    assert artifact["selected_primitives"] == PROVEN_PRIMITIVES
    assert artifact["next_recommended_axis"]["selected"] == NEXT_AXIS_RENDER_SMOKE

    local_probe = artifact["local_probe"]
    assert local_probe["repo_relative_path"] == LOCAL_IGNORED_PROBE_PATH.as_posix()
    assert local_probe["target_exists"] is True
    assert local_probe["access_state"] == "verified_present_ignored_local_artifact"
    assert local_probe["git_state"] == "ignored"
    assert local_probe["git_check_ignore"]["ignored"] is True
    assert (ROOT / LOCAL_IGNORED_PROBE_PATH).exists()

    result = subprocess.run(
        ["git", "check-ignore", "-v", "--", LOCAL_IGNORED_PROBE_PATH.as_posix()],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "_tmp/" in result.stdout


def test_probe_ymmp_readback_covers_four_proven_primitives_without_media_or_audio() -> None:
    _ensure_local_probe()
    artifact = _load(DEFAULT_MATERIALIZATION_PATH)
    readback = artifact["probe_ymmp_readback"]

    assert readback["readback_status"] == "structural_pass"
    assert readback["target_exists"] is True
    assert readback["timeline"]["fps"] == 60
    assert readback["timeline"]["length_frames"] == 3600
    assert readback["timeline"]["item_count"] == 20
    assert readback["timeline"]["item_type_counts"] == {
        "GroupItem": 10,
        "ImageItem": 10,
    }
    assert readback["timeline"]["unexpected_item_types"] == []

    primitive_status = {
        row["primitive_id"]: row["status"]
        for row in readback["primitive_status"]
    }
    assert primitive_status == {
        "head_nod": "pass",
        "expression_swap": "pass",
        "character_entrance_exit": "pass",
        "small_position_move": "pass",
        "speech_balloon": "omitted_partial",
    }

    coverage = artifact["primitive_coverage"]
    assert coverage["all_proven_primitives_covered"] is True
    assert coverage["speech_balloon_intentionally_omitted"] is True
    assert set(coverage["covered_primitives"]) == set(PROVEN_PRIMITIVES)
    assert coverage["coverage"]["speech_balloon"] == []

    probe = load_ymmp(ROOT / LOCAL_IGNORED_PROBE_PATH)
    item_types = {_item_type(item) for item in _get_timeline_items(probe)}
    assert item_types == {"GroupItem", "ImageItem"}
    combined_paths = "\n".join(
        str(item.get("FilePath", ""))
        for item in _get_timeline_items(probe)
        if isinstance(item, dict)
    )
    assert "http://" not in combined_paths
    assert "https://" not in combined_paths
    assert ".mp4" not in combined_paths.lower()
    assert ".wav" not in combined_paths.lower()
    assert ".mp3" not in combined_paths.lower()


def test_boundaries_access_and_completion_matrices_are_no_render() -> None:
    _ensure_local_probe()
    artifact = _load(DEFAULT_MATERIALIZATION_PATH)

    assert len(artifact["access_readiness"]) == 6
    assert all(row["status"] is True for row in artifact["access_readiness"])
    assert len(artifact["completion_matrix"]) == 8
    assert artifact["completion_matrix"][3]["status"] is True
    assert len(artifact["inertia_check"]) == 5
    assert all(row["status"] is True for row in artifact["inertia_check"][:4])

    boundaries = artifact["boundaries"]
    assert boundaries["local_ignored_probe_created"] is True
    for key, value in boundaries.items():
        if key != "local_ignored_probe_created":
            assert value is False
    assert set(artifact["not_accepted_scope"].values()) == {False}
    assert artifact["probe_ymmp_readback"]["YMM4_launch_status"] == "not_launched"
    assert artifact["probe_ymmp_readback"]["render_status"] == "not_rendered"
    assert artifact["probe_ymmp_readback"]["audio_tts_status"] == "not_created"
    assert artifact["expected_next_user_action_if_verified"][
        "this_slice_user_action_required"
    ] is False


def test_markdown_output_matches_renderer() -> None:
    _ensure_local_probe()
    artifact = _load(DEFAULT_MATERIALIZATION_PATH)

    assert (ROOT / DEFAULT_MATERIALIZATION_DOC_PATH).read_text(
        encoding="utf-8"
    ) == render_newsroom_yukkuri_animation_primitive_probe_materialization_markdown(
        artifact
    )


def test_tracked_handoff_does_not_include_forbidden_media_outputs() -> None:
    generated_paths = [
        ROOT / DEFAULT_MATERIALIZATION_PATH,
        ROOT / DEFAULT_MATERIALIZATION_DOC_PATH,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in generated_paths)

    assert "http://" not in combined
    assert "https://" not in combined
    assert "www." not in combined
    assert "render again" not in combined.lower()

    handoff_dir = ROOT / "samples/_probe/newsroom_handoff"
    forbidden_suffixes = {".ymmp", ".mp4", ".wav", ".mp3", ".m4a", ".aac"}
    generated_like = [
        *handoff_dir.glob("yukkuri_animation_primitive_probe_materialization_v1.*"),
    ]
    assert all(path.suffix.lower() not in forbidden_suffixes for path in generated_like)
