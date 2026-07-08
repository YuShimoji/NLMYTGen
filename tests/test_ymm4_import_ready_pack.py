from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
)
from src.pipeline.ymm4_import_ready_pack import (
    DEFAULT_ARTIFACT_ID,
    REQUIRED_CUE_FIELDS,
    REQUIRED_YMM4_IMPORT_READY_FILES,
    build_ymm4_import_ready_pack,
    validate_ymm4_import_ready_pack,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_ymm4_import_ready_pack_builds_manifest_cue_map_and_preview(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_ready_pack"

    readback = build_ymm4_import_ready_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_YMM4_IMPORT_READY_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "ymm4_import_ready_manifest.json")
    cue_map = _load(output_dir / "edit_slice_to_ymm4_cue_map.json")
    gate_readback = _load(output_dir / "gate_readback.json")
    adapter_plan = _load(output_dir / "ymmp_adapter_plan.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    html = (output_dir / "ymm4_import_ready_preview.html").read_text(encoding="utf-8")
    sheet = (output_dir / "manual_ymm4_import_observation_sheet.md").read_text(encoding="utf-8")

    assert manifest["artifact_id"] == DEFAULT_ARTIFACT_ID
    assert manifest["source_episode_id"] == "yukkuri_newsroom_content_spine_002"
    assert manifest["queue_count"] == 7
    assert manifest["scene_count"] == 3
    assert manifest["cue_count"] == 9
    assert manifest["expected_voice_subtitle_links"]["count"] == 9
    assert len(manifest["visual_scene_links"]) == 3
    assert len(manifest["citation_overlay_links"]) == 3
    assert manifest["thumbnail_motif_status"] == "placeholder_context_transferred_not_final_approval"
    assert manifest["ymm4_import_state"] == "ready_for_manual_import_observation"
    assert manifest["actual_ymm4_imported"] is False
    assert manifest["rendered_video_created"] is False
    assert manifest["real_input_replaced"] is False
    assert manifest["rights_approved"] is False
    assert manifest["public_ready"] is False
    assert manifest["gates_closed"] is True
    assert cue_map["cue_count"] == 9
    assert cue_map["scene_count"] == 3
    assert len(cue_map["cues"]) == 9
    for cue in cue_map["cues"]:
        for field in REQUIRED_CUE_FIELDS:
            assert field in cue
        assert "VoiceItem" in cue["expected_yymm4_layer_or_track"]
        assert cue["required_asset_state"] in {"placeholder", "diagnostic", "real_required_later"}
    assert gate_readback["status"] == "ymm4_import_gates_closed"
    assert gate_readback["gates_closed"] is True
    assert all(value is False for value in gate_readback["closed_gate_flags"].values())
    assert adapter_plan["status"] == "adapter_plan_ready_no_ymmp_write"
    assert adapter_plan["ymmp_file_created"] is False
    assert source_index["local_edit_pack_read_only"] is True
    assert 'data-ymm4-import-ready="true"' in html
    assert 'data-region="cue-map"' in html
    assert "card-grid" not in html
    assert sheet.count("\n1.") == 1
    assert sheet.count("\n5.") == 1


def test_ymm4_import_ready_validation_catches_missing_cue_map(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_ready_pack"
    build_ymm4_import_ready_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )
    (output_dir / "edit_slice_to_ymm4_cue_map.json").unlink()

    readback = validate_ymm4_import_ready_pack(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:edit_slice_to_ymm4_cue_map.json" in readback["failed_checks"]


def test_cli_build_ymm4_import_ready_pack_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_ymm4_import_ready_pack"

    code = main(
        [
            "build-ymm4-import-ready-pack",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            DEFAULT_ARTIFACT_ID,
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["primary_review_file"].endswith("ymm4_import_ready_preview.html")
    assert payload["queue_count"] == 7
    assert payload["scene_count"] == 3
    assert payload["cue_count"] == 9
    assert payload["ymm4_import_state"] == "ready_for_manual_import_observation"
    assert payload["actual_ymm4_imported"] is False
    assert payload["rendered_video_created"] is False
    assert payload["real_input_replaced"] is False
    assert payload["rights_approved"] is False
    assert payload["public_ready"] is False
    assert payload["gates_closed"] is True
    assert payload["full_pytest_run"] is False


def test_ymm4_import_ready_pack_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_import_ready_pack"
    build_ymm4_import_ready_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )

    readback = _load(output_dir / "validation_readback.json")
    assert readback["status"] == "passed"
    assert readback["checks"]["external_dependency_status"] == "none_found"
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["temporary_copy_absent"] is True
    assert readback["checks"]["ymmp_file_created"] is False

    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for marker in EXTERNAL_REF_MARKERS:
            assert marker not in text, (path.name, marker)

    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_TRUE_CLAIMS:
            assert forbidden not in text, (path.name, forbidden)
