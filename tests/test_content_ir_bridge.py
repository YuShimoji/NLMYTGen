from __future__ import annotations

import csv
import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.content_ir_bridge import (
    BLOCKED_PUBLIC_ACTIONS,
    REQUIRED_BRIDGE_FILES,
    build_content_ir_bridge_package,
    validate_content_ir_bridge_package,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_001"
SOURCE_PACKAGE_002 = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_002"

FORBIDDEN_COMPLETION_CLAIMS = (
    '"render_completion": true',
    '"production_ready": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"video_generation": true',
    '"thumbnail_image_generated": true',
    '"youtube_uploaded": true',
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _csv_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as file:
        return [row for row in csv.reader(file) if row]


def test_content_ir_bridge_builds_writer_ir_csv_and_readback(tmp_path) -> None:
    bridge_dir = tmp_path / "ir_bridge"

    readback = build_content_ir_bridge_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=bridge_dir,
        artifact_id="test_ir_bridge",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_BRIDGE_FILES:
        assert (bridge_dir / filename).exists(), filename

    manifest = _load(bridge_dir / "bridge_manifest.json")
    episode_bridge = _load(bridge_dir / "episode_bridge.json")
    writer_ir = _load(bridge_dir / "writer_ir_candidate.json")
    cue_packet = _load(bridge_dir / "cue_packet_candidate.json")
    source_reference = _load(bridge_dir / "source_content_spine_reference.json")
    source_index = _load(bridge_dir / "source_artifact_index.json")
    saved_readback = _load(bridge_dir / "validation_readback.json")
    rows = _csv_rows(bridge_dir / "draft_yymm4.csv")

    assert manifest["artifact_kind"] == "content-spine-to-writer-ir-csv-bridge"
    assert episode_bridge["selected_candidate_id"] == "sports_pitch_sequence_p05"
    assert episode_bridge["source_boundary"]["source_name"] == "Synthetic Baseball Feed"
    assert episode_bridge["source_boundary"]["freshness_status"] == "offline_fixture_not_live"
    assert episode_bridge["blocked_public_actions"] == list(BLOCKED_PUBLIC_ACTIONS)
    assert episode_bridge["readiness"]["writer_ir_candidate_status"] == "draft_candidate_generated"
    assert episode_bridge["readiness"]["ymm4_csv_status"] == "draft_preview_generated_not_production"
    assert episode_bridge["readiness"]["production_status"] == "blocked_until_transcript_timing_and_human_review"
    assert writer_ir["schema_version"] == "content_spine_writer_ir_candidate.v1"
    assert writer_ir["compatibility_status"] == "draft_candidate_not_validate_ir_ready"
    assert writer_ir["utterances"]
    assert writer_ir["source_boundary"]["rights_status"] == "sample_only_no_publication"
    assert source_reference["schema_version"] == "content_ir_bridge_source_content_spine_reference.v1"
    assert source_reference["generated_ir_csv_outputs"]["draft_yymm4_csv"].endswith("draft_yymm4.csv")
    assert source_reference["csv_contract"]["header_mode"] == "headerless_yymm4_csv"
    assert source_index["artifact_counts"]["source_required_present"] >= 3
    assert source_index["artifact_counts"]["generated_present"] >= len(REQUIRED_BRIDGE_FILES) - 1
    assert cue_packet["phase"] == "content-spine-bridge-cue-candidate"
    assert len(rows) == readback["draft_csv_rows"]
    assert rows[0] != ["speaker", "text"]
    assert rows[0][0] == "れいむ"
    assert rows[1][0] == "まりさ"
    assert saved_readback["status"] == "passed"
    assert saved_readback["checks"]["all_required_files_present"] is True
    assert saved_readback["checks"]["draft_csv_headerless"] is True


def test_content_ir_bridge_validation_catches_missing_csv(tmp_path) -> None:
    bridge_dir = tmp_path / "ir_bridge"
    build_content_ir_bridge_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=bridge_dir,
        artifact_id="test_ir_bridge",
    )
    (bridge_dir / "draft_yymm4.csv").unlink()

    readback = validate_content_ir_bridge_package(bridge_dir)

    assert readback["status"] == "failed"
    assert "missing_file:draft_yymm4.csv" in readback["failed_checks"]
    assert "draft_csv_too_short" in readback["failed_checks"]


def test_cli_build_content_ir_bridge_json_output(tmp_path, capsys) -> None:
    bridge_dir = tmp_path / "cli_ir_bridge"

    code = main([
        "build-content-ir-bridge",
        "--package",
        str(SOURCE_PACKAGE),
        "--output",
        str(bridge_dir),
        "--artifact-id",
        "test_cli_ir_bridge",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["selected_candidate_id"] == "sports_pitch_sequence_p05"
    assert (bridge_dir / "writer_ir_candidate.json").exists()
    assert (bridge_dir / "draft_yymm4.csv").exists()


def test_content_ir_bridge_builds_second_episode_dry_run_boundaries(tmp_path) -> None:
    bridge_dir = tmp_path / "ir_bridge_002"

    readback = build_content_ir_bridge_package(
        package_dir=SOURCE_PACKAGE_002,
        output_dir=bridge_dir,
        artifact_id="test_ir_bridge_002",
    )

    assert readback["status"] == "passed"
    assert readback["selected_candidate_id"] == "factory_seed_dry_run_002"
    for filename in REQUIRED_BRIDGE_FILES:
        assert (bridge_dir / filename).exists(), filename

    manifest = _load(bridge_dir / "bridge_manifest.json")
    episode_bridge = _load(bridge_dir / "episode_bridge.json")
    source_reference = _load(bridge_dir / "source_content_spine_reference.json")
    source_index = _load(bridge_dir / "source_artifact_index.json")
    saved_readback = _load(bridge_dir / "validation_readback.json")
    rows = _csv_rows(bridge_dir / "draft_yymm4.csv")

    assert manifest["artifact_id"] == "test_ir_bridge_002"
    assert manifest["boundary_status"]["dry_run"] is True
    assert manifest["boundary_status"]["sample_fixture_not_real"] is True
    assert manifest["boundary_status"]["no_real_transcript"] is True
    assert manifest["boundary_status"]["no_yymm4_import"] is True
    assert manifest["boundary_status"]["rights_boundary"] == "sample_only_no_publication"
    assert manifest["boundary_status"]["public_upload_closed"] is True
    assert manifest["boundary_status"]["yymm4_render_closed"] is True

    assert episode_bridge["source_origin"]["source_seed_reference_present"] is True
    assert episode_bridge["source_origin"]["manual_copy_of_original_pilot"] is False
    assert episode_bridge["boundary_status"]["dry_run"] is True
    assert episode_bridge["boundary_status"]["yymm4_import_status"] == "not_run"
    assert episode_bridge["readiness"]["no_yymm4_import"] is True
    assert episode_bridge["source_boundary"]["freshness_status"] == "offline_fixture_not_live"
    assert episode_bridge["source_boundary"]["rights_status"] == "sample_only_no_publication"

    assert source_reference["source_seed_reference_present"] is True
    assert source_reference["manual_copy_of_original_pilot"] is False
    assert source_reference["seed_origin_fields"]["derived_from_episode_seed_id"]
    assert source_reference["inherited_template_defaults"]["csv_header_mode"] == "headerless_yymm4_csv"
    assert source_reference["dry_run_placeholders"]["topic_source_packet"]["source_reality"] == "sample_fixture_not_real"
    assert source_reference["generated_content_spine_outputs"]["topic_candidates"].endswith("topic_candidates.json")
    assert source_reference["generated_ir_csv_outputs"]["episode_bridge"].endswith("episode_bridge.json")
    assert source_reference["boundary_status"]["dry_run"] is True
    assert source_reference["boundary_status"]["public_upload_status"] == "public_upload_closed"

    for key, value in source_reference["required_real_inputs"].items():
        assert value["value"] is None, key

    assert source_index["artifact_counts"]["source_required_present"] == 10
    assert source_index["artifact_counts"]["generated_present"] >= len(REQUIRED_BRIDGE_FILES) - 1
    assert len(rows) == readback["draft_csv_rows"]
    assert rows[0] != ["speaker", "text"]
    assert saved_readback["checks"]["source_origin_separated"] is True
    assert saved_readback["checks"]["dry_run_boundaries_preserved"] is True
    assert saved_readback["checks"]["no_external_references"] is True
    assert saved_readback["checks"]["no_forbidden_completion_claims"] is True


def test_content_ir_bridge_validation_catches_second_episode_real_input_claim(tmp_path) -> None:
    bridge_dir = tmp_path / "ir_bridge_002"
    build_content_ir_bridge_package(
        package_dir=SOURCE_PACKAGE_002,
        output_dir=bridge_dir,
        artifact_id="test_ir_bridge_002",
    )
    source_reference = _load(bridge_dir / "source_content_spine_reference.json")
    source_reference["required_real_inputs"]["real_transcript"]["value"] = "pretend transcript"
    (bridge_dir / "source_content_spine_reference.json").write_text(
        json.dumps(source_reference, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    readback = validate_content_ir_bridge_package(bridge_dir)

    assert readback["status"] == "failed"
    assert "required_real_input_has_value:real_transcript" in readback["failed_checks"]


def test_generated_ir_bridge_text_does_not_claim_forbidden_completion(tmp_path) -> None:
    bridge_dir = tmp_path / "ir_bridge"
    build_content_ir_bridge_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=bridge_dir,
        artifact_id="test_ir_bridge",
    )

    for path in bridge_dir.iterdir():
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
