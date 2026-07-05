from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.episode_factory_template_registry import (
    REQUIRED_EPISODE_FACTORY_TEMPLATE_REGISTRY_FILES,
    REQUIRED_TEMPLATE_IDS,
    build_episode_factory_template_registry,
    validate_episode_factory_template_registry,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = REPO_ROOT / "production_pilots" / "yukkuri_newsroom_content_spine_001"

FORBIDDEN_COMPLETION_CLAIMS = (
    '"production_ready": true',
    '"creative_final_acceptance": true',
    '"publish_gate": true',
    '"youtube_uploaded": true',
    '"external_media_download_required": true',
    '"media_download_required": true',
    '"oauth_required": true',
    '"payment_required": true',
    '"yymm4_gui_launched": true',
    '"yymm4_import_completed": true',
    '"yymm4_render_completed": true',
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_episode_factory_template_registry_builds_reusable_templates_and_seed(tmp_path) -> None:
    output_dir = tmp_path / "episode_factory_template_registry"

    readback = build_episode_factory_template_registry(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_episode_factory_registry",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_EPISODE_FACTORY_TEMPLATE_REGISTRY_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "template_registry_manifest.json")
    templates = _load(output_dir / "episode_factory_templates.json")
    seed = _load(output_dir / "next_episode_seed_sample.json")
    readiness = _load(output_dir / "init_readiness_summary.json")
    source_index = _load(output_dir / "source_artifact_index.json")

    template_ids = {item["template_id"] for item in templates["templates"]}

    assert manifest["artifact_kind"] == "episode-factory-template-registry"
    assert manifest["selected_candidate_id"] == "sports_pitch_sequence_p05"
    assert set(REQUIRED_TEMPLATE_IDS).issubset(template_ids)
    assert manifest["boundary_status"]["transcript_status"] == "sample_fixture_not_real"
    assert manifest["boundary_status"]["template_status"] == "draft_offline"
    assert manifest["boundary_status"]["rights_boundary"] == "sample_only_no_publication"
    assert manifest["boundary_status"]["public_upload_status"] == "public_upload_closed"
    assert manifest["boundary_status"]["yymm4_render_status"] == "yymm4_render_closed"
    assert seed["status"] == "draft_offline_seed_sample"
    assert seed["required_inputs"]["topic_or_source_packet"]["state"] == "required_for_real_episode"
    assert seed["required_inputs"]["real_transcript"]["state"] == "required_before_production"
    assert seed["required_inputs"]["rights_review"]["state"] == "required_before_public_use"
    assert seed["required_inputs"]["human_episode_decision"]["state"] == "required_before_yymm4_import"
    assert seed["carried_defaults"]["csv_header_mode"] == "headerless_yymm4_csv"
    assert seed["boundary_status"]["public_upload_status"] == "public_upload_closed"
    assert seed["boundary_status"]["yymm4_render_status"] == "yymm4_render_closed"
    assert readiness["deterministic_generation_path"] is True
    assert readiness["init_status"]["can_create_seed_sample_without_external_input"] is True
    assert readiness["init_status"]["can_claim_production_readiness"] is False
    assert source_index["artifact_counts"]["source_present"] >= 20

    for template_id in REQUIRED_TEMPLATE_IDS:
        payload = _load(output_dir / f"{template_id}.json")
        assert payload["required_fields_for_real_episode"], template_id
        assert payload["carried_from_template"], template_id


def test_episode_factory_template_registry_validation_catches_missing_seed(tmp_path) -> None:
    output_dir = tmp_path / "episode_factory_template_registry"
    build_episode_factory_template_registry(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_episode_factory_registry",
    )
    (output_dir / "next_episode_seed_sample.json").unlink()

    readback = validate_episode_factory_template_registry(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:next_episode_seed_sample.json" in readback["failed_checks"]
    assert "next_episode_seed_sample_json_invalid" in readback["failed_checks"]


def test_cli_build_episode_factory_template_registry_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_episode_factory_template_registry"

    code = main([
        "build-episode-factory-template-registry",
        "--package",
        str(SOURCE_PACKAGE),
        "--output",
        str(output_dir),
        "--artifact-id",
        "test_cli_episode_factory_registry",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["selected_candidate_id"] == "sports_pitch_sequence_p05"
    assert payload["template_count"] == len(REQUIRED_TEMPLATE_IDS)
    assert payload["primary_machine_readable"].endswith("template_registry_manifest.json")
    assert payload["primary_human_review"].endswith("template_usage.md")
    assert (output_dir / "next_episode_seed_sample.json").exists()


def test_generated_episode_factory_registry_text_does_not_claim_forbidden_completion(tmp_path) -> None:
    output_dir = tmp_path / "episode_factory_template_registry"
    build_episode_factory_template_registry(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_episode_factory_registry",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            assert "https://" not in text
            assert "<img" not in text.lower()
            assert "<image" not in text.lower()
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
