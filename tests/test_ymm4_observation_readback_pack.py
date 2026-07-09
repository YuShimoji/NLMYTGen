from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
)
from src.pipeline.ymm4_observation_readback_pack import (
    DEFAULT_ARTIFACT_ID,
    REQUIRED_YMM4_OBSERVATION_FILES,
    build_ymm4_observation_readback_pack,
    validate_ymm4_observation_readback_pack,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_ymm4_observation_readback_builds_operator_instruction_package(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_observation_readback_pack"

    readback = build_ymm4_observation_readback_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )

    assert readback["validation_status"] == "passed"
    assert readback["status"] == "blocked"
    for filename in REQUIRED_YMM4_OBSERVATION_FILES:
        assert (output_dir / filename).exists(), filename

    observation = _load(output_dir / "observation_readback.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    html = (output_dir / "observation_preview.html").read_text(encoding="utf-8")
    manual = (output_dir / "manual_ymm4_observation_readback.md").read_text(encoding="utf-8")

    assert observation["artifact_id"] == DEFAULT_ARTIFACT_ID
    assert observation["episode_id"] == "yukkuri_newsroom_content_spine_002"
    assert observation["source_import_ready_pack_reference"].endswith("ymm4_import_ready_pack")
    assert observation["source_real_input_prep_reference"].endswith("real_input_replacement_readiness_pack")
    assert observation["observation_mode"] == "operator_instruction_only"
    assert observation["actual_ymm4_import_attempted"] is False
    assert observation["actual_ymm4_imported"] is False
    assert observation["cue_count_expected"] == 9
    assert observation["scene_count_expected"] == 3
    assert observation["cue_count_observed"] == 0
    assert observation["voice_item_observed"] == "not_observed"
    assert observation["subtitle_item_observed"] == "not_observed"
    assert observation["timing_order_observed"] == "not_observed"
    assert observation["placeholder_boundary_observed"] == "not_observed"
    assert observation["screenshot_or_visual_evidence_paths"] == []
    assert observation["rendered_video_created"] is False
    assert observation["ymmp_file_created"] is False
    assert observation["production_ymmp_written"] is False
    assert observation["real_input_replaced"] is False
    assert observation["rights_approved"] is False
    assert observation["public_ready"] is False
    assert observation["next_gate"] == "manual_ymm4_import_observation_return"
    assert all(value is False for value in observation["closed_gate_flags"].values())
    assert source_index["ymm4_import_ready_pack_read_only"] is True
    assert source_index["real_input_prep_pack_read_only"] is True
    assert '<html lang="ja"' in html
    assert 'data-ymm4-observation-readback="true"' in html
    assert 'data-region="pipeline-runway"' in html
    assert 'data-region="observation-matrix"' in html
    assert 'data-region="closed-gates"' in html
    assert "実観測は未実行" in html
    assert "card-grid" not in html
    assert "operatorが返す観測5点" in manual
    assert "Do not render/export" in manual
    assert manual.count("\n1.") == 1
    assert manual.count("\n5.") == 1


def test_ymm4_observation_validation_catches_missing_manual_sheet(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_observation_readback_pack"
    build_ymm4_observation_readback_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )
    (output_dir / "manual_ymm4_observation_readback.md").unlink()

    readback = validate_ymm4_observation_readback_pack(output_dir)

    assert readback["validation_status"] == "failed"
    assert "missing_file:manual_ymm4_observation_readback.md" in readback["failed_checks"]


def test_cli_build_ymm4_observation_readback_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_ymm4_observation_readback_pack"

    code = main(
        [
            "build-ymm4-observation-readback-pack",
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
    assert payload["validation_status"] == "passed"
    assert payload["status"] == "blocked"
    assert payload["primary_review_file"].endswith("observation_preview.html")
    assert payload["observation_mode"] == "operator_instruction_only"
    assert payload["actual_ymm4_import_attempted"] is False
    assert payload["actual_ymm4_imported"] is False
    assert payload["cue_count_expected"] == 9
    assert payload["cue_count_observed"] == 0
    assert payload["voice_item_observed"] == "not_observed"
    assert payload["subtitle_item_observed"] == "not_observed"
    assert payload["timing_order_observed"] == "not_observed"
    assert payload["placeholder_boundary_observed"] == "not_observed"
    assert payload["rendered_video_created"] is False
    assert payload["ymmp_file_created"] is False
    assert payload["production_ymmp_written"] is False
    assert payload["real_input_replaced"] is False
    assert payload["rights_approved"] is False
    assert payload["public_ready"] is False


def test_ymm4_observation_readback_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "ymm4_observation_readback_pack"
    build_ymm4_observation_readback_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )

    readback = _load(output_dir / "observation_readback.json")
    assert readback["validation_status"] == "passed"
    assert readback["checks"]["external_dependency_status"] == "none_found"
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["temporary_copy_absent"] is True

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
