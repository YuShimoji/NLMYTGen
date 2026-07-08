from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.real_input_intake_readiness_pack import (
    REQUIRED_CONTRACT_FIELDS,
    REQUIRED_REAL_INPUT_INTAKE_FILES,
    build_real_input_intake_readiness_pack,
    validate_real_input_intake_readiness_pack,
)
from src.pipeline.split_view_decision_evidence_prototype import (
    EXTERNAL_REF_MARKERS,
    FORBIDDEN_TRUE_CLAIMS,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_real_input_intake_readiness_builds_contract_and_panel(tmp_path) -> None:
    output_dir = tmp_path / "real_input_intake_readiness"

    readback = build_real_input_intake_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_real_input_intake_readiness_pack",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_REAL_INPUT_INTAKE_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "real_input_intake_manifest.json")
    schema = _load(output_dir / "source_transcript_contract.schema.json")
    source_template = _load(output_dir / "local_source_manifest_template.json")
    transcript_template = _load(output_dir / "transcript_template.json")
    provenance_template = _load(output_dir / "provenance_receipt_template.json")
    validation_plan = _load(output_dir / "intake_validation_plan.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    html = (output_dir / "real_input_intake_panel.html").read_text(encoding="utf-8")
    dropzone = (output_dir / "DROPZONE_README.md").read_text(encoding="utf-8")
    rights = (output_dir / "rights_usage_checklist.md").read_text(encoding="utf-8")
    replacement = (output_dir / "real_input_replacement_plan.md").read_text(encoding="utf-8")

    assert manifest["artifact_kind"] == "episode-real-input-intake-readiness-pack"
    assert manifest["parallel_lane"] == "input_api_hub"
    assert manifest["input_contract_status"] == "schema_ready_template_only"
    assert manifest["transcript_template_status"] == "placeholder_only_no_real_transcript"
    assert manifest["provenance_template_status"] == "template_only_not_verified"
    assert manifest["dropzone_status"] == "instructions_ready_no_files_required_now"
    assert manifest["replacement_plan_status"] == "planned_not_executed"
    assert manifest["invented_real_content"] is False
    assert manifest["rights_acceptance_claimed"] is False
    assert manifest["real_source_transcript_ingested"] is False
    assert manifest["gui_lane_files_touched"] == []
    assert manifest["output_template_files_touched"] == []
    assert manifest["thread_registry_updated"] is True
    assert manifest["shared_docs_touched"] is True
    assert set(schema["required"]) >= set(REQUIRED_CONTRACT_FIELDS)
    assert set(schema["properties"]) >= set(REQUIRED_CONTRACT_FIELDS)
    assert source_template["source"]["local_file_path"] == "<required-local-path-inside-real_input-dropzone>"
    assert source_template["invented_real_content"] is False
    assert transcript_template["transcript"]["actual_segments_present"] is False
    assert transcript_template["transcript"]["invented_real_content"] is False
    assert provenance_template["receipt_status"] == "template_only_not_verified"
    assert validation_plan["invented_real_content"] is False
    assert validation_plan["rights_acceptance_claimed"] is False
    assert source_index["output_template_context_read_only"] is True
    assert source_index["gui_lane_context_read_only"] is True
    assert 'data-real-input-intake="true"' in html
    assert 'data-region="intake-checklist"' in html
    assert 'data-region="contract-map"' in html
    assert 'data-region="provenance-flow"' in html
    assert 'data-region="replacement-strip"' in html
    assert "real_input/source/" in dropzone
    assert "real_input/transcript/" in dropzone
    assert "not legal acceptance" in rights
    assert "output_template_readiness_pack" in replacement


def test_real_input_intake_validation_catches_missing_contract(tmp_path) -> None:
    output_dir = tmp_path / "real_input_intake_readiness"
    build_real_input_intake_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_real_input_intake_readiness_pack",
    )
    (output_dir / "source_transcript_contract.schema.json").unlink()

    readback = validate_real_input_intake_readiness_pack(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:source_transcript_contract.schema.json" in readback["failed_checks"]


def test_cli_build_real_input_intake_readiness_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_real_input_intake_readiness"

    code = main(
        [
            "build-real-input-intake-readiness-pack",
            "--package",
            str(SOURCE_PACKAGE),
            "--output",
            str(output_dir),
            "--artifact-id",
            "test_cli_real_input_intake_readiness_pack",
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["primary_review_file"].endswith("real_input_intake_panel.html")
    assert payload["input_contract_status"] == "schema_ready_template_only"
    assert payload["transcript_template_status"] == "placeholder_only_no_real_transcript"
    assert payload["provenance_template_status"] == "template_only_not_verified"
    assert payload["dropzone_status"] == "instructions_ready_no_files_required_now"
    assert payload["replacement_plan_status"] == "planned_not_executed"
    assert payload["invented_real_content"] is False
    assert payload["rights_acceptance_claimed"] is False
    assert payload["gui_lane_files_touched"] == []
    assert payload["output_template_files_touched"] == []
    assert payload["thread_registry_updated"] is True
    assert payload["shared_docs_touched"] is True
    assert payload["full_pytest_run"] is False
    assert payload["launcher_or_open_command"]


def test_real_input_intake_is_local_and_claims_stay_closed(tmp_path) -> None:
    output_dir = tmp_path / "real_input_intake_readiness"
    build_real_input_intake_readiness_pack(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_real_input_intake_readiness_pack",
    )

    readback = _load(output_dir / "validation_readback.json")
    assert readback["status"] == "passed"
    assert readback["checks"]["external_dependency_status"] == "none_found"
    assert readback["checks"]["forbidden_true_claims_absent"] is True
    assert readback["checks"]["temporary_copy_absent"] is True
    assert readback["checks"]["invented_real_content"] is False
    assert readback["checks"]["rights_acceptance_claimed"] is False
    assert readback["checks"]["real_source_transcript_ingested"] is False

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
