from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.factory_seed_content_spine import (
    FORBIDDEN_COMPLETION_CLAIMS,
    REQUIRED_FACTORY_SEED_CONTENT_SPINE_FILES,
    build_content_spine_from_factory_seed,
    validate_factory_seed_content_spine,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_SEED_PACKAGE = (
    REPO_ROOT
    / "production_pilots"
    / "yukkuri_newsroom_content_spine_001"
    / "factory_seed_dry_run_002"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_factory_seed_content_spine_builds_second_dry_run_package(tmp_path) -> None:
    output_dir = tmp_path / "yukkuri_newsroom_content_spine_002"

    readback = build_content_spine_from_factory_seed(
        seed_package_dir=SOURCE_SEED_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_yukkuri_newsroom_content_spine_002",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_FACTORY_SEED_CONTENT_SPINE_FILES:
        assert (output_dir / filename).exists(), filename

    dry_run_manifest = _load(output_dir / "content_spine_dry_run_manifest.json")
    source_seed = _load(output_dir / "source_seed_reference.json")
    standard_manifest = _load(output_dir / "MANIFEST.json")
    topics = _load(output_dir / "topic_candidates.json")
    dashboard = _load(output_dir / "dashboard_status.json")
    content_readback = _load(output_dir / "content_spine_readback.json")
    source_index = _load(output_dir / "source_artifact_index.json")

    assert dry_run_manifest["artifact_kind"] == "factory-seed-to-content-spine-dry-run"
    assert dry_run_manifest["status"] == "generated"
    assert dry_run_manifest["boundaries"]["dry_run"] is True
    assert dry_run_manifest["boundaries"]["no_manual_copy_of_original_pilot"] is True
    assert dry_run_manifest["boundaries"]["no_real_transcript"] is True
    assert dry_run_manifest["boundary_status"]["dry_run"] is True
    assert dry_run_manifest["boundary_status"]["sample_fixture_not_real"] is True
    assert dry_run_manifest["boundary_status"]["rights_boundary"] == "sample_only_no_publication"
    assert dry_run_manifest["boundary_status"]["public_upload_closed"] is True
    assert dry_run_manifest["boundary_status"]["yymm4_render_closed"] is True
    assert dry_run_manifest["boundary_status"]["no_real_transcript"] is True
    assert source_seed["manual_copy_of_original_pilot"] is False
    assert source_seed["inherited_template_defaults"]["csv_header_mode"] == "headerless_yymm4_csv"
    assert source_seed["dry_run_placeholders"]["topic_source_packet"]["status"] == "dry_run"
    assert source_seed["required_real_inputs"]["topic_or_source_packet"]["value"] is None
    assert source_seed["required_real_inputs"]["real_transcript"]["value"] is None
    assert source_seed["required_real_inputs"]["rights_review"]["value"] is None
    assert source_seed["required_real_inputs"]["human_episode_decision"]["value"] is None
    assert standard_manifest["artifact_kind"] == "content-planning-dashboard-spine"
    assert topics["candidates"][0]["candidate_id"] == "factory_seed_dry_run_002"
    assert topics["candidates"][0]["source_boundary"]["freshness_status"] == "offline_fixture_not_live"
    assert topics["candidates"][0]["source_boundary"]["rights_status"] == "sample_only_no_publication"
    assert topics["candidates"][0]["source_boundary"]["production_status"] == "dry_run_only_not_production"
    assert dashboard["readiness"]["episode_package_status"] == "local_reviewable"
    assert dashboard["readiness"]["ymm4_readiness"] == "planning_ready_csv_ir_not_generated"
    assert content_readback["status"] == "passed"
    assert source_index["artifact_counts"]["source_present"] >= 8
    assert source_index["artifact_counts"]["generated_present"] == len(REQUIRED_FACTORY_SEED_CONTENT_SPINE_FILES)


def test_factory_seed_content_spine_validation_catches_fake_real_input(tmp_path) -> None:
    output_dir = tmp_path / "yukkuri_newsroom_content_spine_002"
    build_content_spine_from_factory_seed(
        seed_package_dir=SOURCE_SEED_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_yukkuri_newsroom_content_spine_002",
    )

    source_seed_path = output_dir / "source_seed_reference.json"
    source_seed = _load(source_seed_path)
    source_seed["required_real_inputs"]["real_transcript"]["value"] = "fake-real-transcript.txt"
    source_seed_path.write_text(json.dumps(source_seed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    readback = validate_factory_seed_content_spine(output_dir, seed_package_dir=SOURCE_SEED_PACKAGE)

    assert readback["status"] == "failed"
    assert "required_real_input_has_value:real_transcript" in readback["failed_checks"]
    assert readback["checks"]["required_real_inputs_separated"] is False


def test_cli_build_content_spine_from_seed_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_yukkuri_newsroom_content_spine_002"

    code = main([
        "build-content-spine-from-seed",
        "--seed-package",
        str(SOURCE_SEED_PACKAGE),
        "--output",
        str(output_dir),
        "--artifact-id",
        "test_cli_yukkuri_newsroom_content_spine_002",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["selected_candidate_id"] == "factory_seed_dry_run_002"
    assert payload["primary_machine_readable"].endswith("content_spine_dry_run_manifest.json")
    assert payload["source_seed_reference_path"].endswith("source_seed_reference.json")
    assert payload["standard_content_spine_manifest"].endswith("MANIFEST.json")
    assert (output_dir / "episode_candidate_001.md").exists()


def test_factory_seed_content_spine_text_does_not_claim_forbidden_completion(tmp_path) -> None:
    output_dir = tmp_path / "yukkuri_newsroom_content_spine_002"
    build_content_spine_from_factory_seed(
        seed_package_dir=SOURCE_SEED_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_yukkuri_newsroom_content_spine_002",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            assert "https://" not in text
            assert "http://" not in text
            assert "<img" not in text.lower()
            assert "<image" not in text.lower()
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
