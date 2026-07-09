from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.real_input_replacement_readiness_pack import (
    DEFAULT_ARTIFACT_ID,
    REQUIRED_INPUT_IDS,
    REQUIRED_REAL_INPUT_REPLACEMENT_FILES,
    build_real_input_replacement_readiness_pack,
    validate_real_input_replacement_readiness_pack,
)
from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_real_input_replacement_readiness_builds_preview_contract_and_readback(tmp_path) -> None:
    output_dir = tmp_path / "real_input_replacement_readiness_pack"

    readback = build_real_input_replacement_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_REAL_INPUT_REPLACEMENT_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "real_input_replacement_manifest.json")
    requirements = _load(output_dir / "replacement_input_requirements.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    html = (output_dir / "real_input_replacement_preview.html").read_text(encoding="utf-8")
    contract = (output_dir / "real_input_replacement_contract.md").read_text(encoding="utf-8")
    dropzone = (output_dir / "input_dropzone" / "README.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-real-input-replacement-readiness-pack"
    assert manifest["episode_id"] == "yukkuri_newsroom_content_spine_002"
    assert manifest["package_type"] == "real_input_replacement_readiness"
    assert manifest["source_episode_pack_reference"].endswith("ymm4_import_ready_pack")
    assert manifest["placeholder_state"] == "sample_diagnostic_only_no_verified_local_input"
    assert manifest["required_local_input_count"] == len(REQUIRED_INPUT_IDS)
    assert manifest["candidate_input_count"] == 0
    assert manifest["actual_real_input_replaced"] is False
    assert manifest["live_fetch_performed"] is False
    assert manifest["external_media_downloaded"] is False
    assert manifest["actual_ymm4_imported"] is False
    assert manifest["rendered_video_created"] is False
    assert manifest["ymmp_file_created"] is False
    assert manifest["rights_approved"] is False
    assert manifest["public_ready"] is False
    assert manifest["next_gate"] == "provide_verified_local_source_and_transcript"
    assert all(value is False for value in manifest["closed_gate_flags"].values())

    required_ids = {row["input_id"] for row in requirements["required_local_inputs"]}
    assert required_ids == set(REQUIRED_INPUT_IDS)
    assert requirements["transcript_alignment_requirements"]["cue_count"] == 9
    assert source_index["ymm4_import_ready_pack_read_only"] is True
    assert source_index["real_input_intake_pack_read_only"] is True
    assert '<html lang="ja"' in html
    assert 'data-real-input-replacement-readiness="true"' in html
    assert 'data-region="pipeline-runway"' in html
    assert 'data-region="input-matrix"' in html
    assert 'data-region="closed-gates"' in html
    assert "実入力置換準備" in html
    assert "未実行" in html
    assert "card-grid" not in html
    assert "source audio/video/document path" in contract
    assert "transcript path" in contract
    assert "Episode 002 cue map" in contract
    assert contract.count("\n1.") == 1
    assert contract.count("\n5.") == 1
    assert "placeholder folder only" in dropzone
    assert "Do not place media files in this commit" in dropzone


def test_real_input_replacement_validation_catches_missing_contract(tmp_path) -> None:
    output_dir = tmp_path / "real_input_replacement_readiness_pack"
    build_real_input_replacement_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )
    (output_dir / "real_input_replacement_contract.md").unlink()

    readback = validate_real_input_replacement_readiness_pack(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:real_input_replacement_contract.md" in readback["failed_checks"]


def test_cli_build_real_input_replacement_readiness_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_real_input_replacement_readiness_pack"

    code = main(
        [
            "build-real-input-replacement-readiness-pack",
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
    assert payload["primary_review_file"].endswith("real_input_replacement_preview.html")
    assert payload["episode_id"] == "yukkuri_newsroom_content_spine_002"
    assert payload["package_type"] == "real_input_replacement_readiness"
    assert payload["required_local_input_count"] == len(REQUIRED_INPUT_IDS)
    assert payload["candidate_input_count"] == 0
    assert payload["actual_real_input_replaced"] is False
    assert payload["live_fetch_performed"] is False
    assert payload["external_media_downloaded"] is False
    assert payload["actual_ymm4_imported"] is False
    assert payload["rendered_video_created"] is False
    assert payload["ymmp_file_created"] is False
    assert payload["rights_approved"] is False
    assert payload["public_ready"] is False
    assert payload["next_gate"] == "provide_verified_local_source_and_transcript"
    assert payload["full_pytest_run"] is False


def test_real_input_replacement_readiness_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "real_input_replacement_readiness_pack"
    build_real_input_replacement_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id=DEFAULT_ARTIFACT_ID,
    )

    readback = _load(output_dir / "validation_readback.json")
    assert readback["status"] == "passed"
    assert readback["checks"]["external_dependency_status"] == "none_found"
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["temporary_copy_absent"] is True
    assert readback["checks"]["candidate_input_count"] == 0
    assert readback["actual_real_input_replaced"] is False
    assert readback["actual_ymm4_imported"] is False
    assert readback["rendered_video_created"] is False
    assert readback["ymmp_file_created"] is False
    assert readback["rights_approved"] is False
    assert readback["public_ready"] is False

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
