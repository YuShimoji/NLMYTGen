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
    assert cue_packet["phase"] == "content-spine-bridge-cue-candidate"
    assert len(rows) == readback["draft_csv_rows"]
    assert rows[0][0] == "れいむ"
    assert rows[1][0] == "まりさ"
    assert saved_readback["status"] == "passed"
    assert saved_readback["checks"]["all_required_files_present"] is True


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
