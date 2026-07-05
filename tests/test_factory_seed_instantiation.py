from __future__ import annotations

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.factory_seed_instantiation import (
    FORBIDDEN_COMPLETION_CLAIMS,
    REQUIRED_FACTORY_SEED_INSTANTIATION_FILES,
    instantiate_episode_factory_seed,
    validate_factory_seed_instantiation,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_REGISTRY = (
    REPO_ROOT
    / "production_pilots"
    / "yukkuri_newsroom_content_spine_001"
    / "episode_factory_template_registry"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_factory_seed_instantiation_builds_second_episode_dry_run_package(tmp_path) -> None:
    output_dir = tmp_path / "factory_seed_dry_run_002"

    readback = instantiate_episode_factory_seed(
        registry_dir=SOURCE_REGISTRY,
        output_dir=output_dir,
        artifact_id="test_factory_seed_instantiation",
        episode_id="test_yukkuri_newsroom_episode_002_seed",
    )

    assert readback["status"] == "passed"
    for filename in REQUIRED_FACTORY_SEED_INSTANTIATION_FILES:
        assert (output_dir / filename).exists(), filename

    manifest = _load(output_dir / "seed_instantiation_manifest.json")
    episode_seed = _load(output_dir / "episode_seed.json")
    dry_run_packet = _load(output_dir / "dry_run_topic_source_packet.json")
    required_inputs = _load(output_dir / "required_real_inputs.json")
    carried_defaults = _load(output_dir / "carried_template_defaults.json")
    planned_steps = _load(output_dir / "planned_pipeline_steps.json")
    boundary = _load(output_dir / "boundary_status.json")
    readiness = _load(output_dir / "init_readiness_summary.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    content_candidate = _load(output_dir / "content_spine_input_candidate.json")

    assert manifest["artifact_kind"] == "factory-seed-instantiation-dry-run"
    assert manifest["status"] == "dry_run_seed_instantiated"
    assert manifest["boundaries"]["dry_run"] is True
    assert manifest["boundaries"]["no_manual_copy_of_original_pilot"] is True
    assert episode_seed["status"] == "dry_run"
    assert episode_seed["source_reality"] == "sample_fixture_not_real"
    assert episode_seed["inherited_defaults"]["csv_header_mode"] == "headerless_yymm4_csv"
    assert episode_seed["synthetic_dry_run_placeholders"]["placeholder_status"] == "sample_fixture_not_real"
    assert dry_run_packet["status"] == "dry_run"
    assert dry_run_packet["source_boundary"]["freshness_status"] == "offline_fixture_not_live"
    assert dry_run_packet["source_boundary"]["rights_status"] == "sample_only_no_publication"
    assert dry_run_packet["source_boundary"]["network_required"] is False
    assert required_inputs["state"] == "required_real_inputs_only"
    assert required_inputs["required_real_inputs"]["topic_or_source_packet"]["value"] is None
    assert required_inputs["required_real_inputs"]["real_transcript"]["value"] is None
    assert required_inputs["required_real_inputs"]["rights_review"]["value"] is None
    assert required_inputs["required_real_inputs"]["human_episode_decision"]["value"] is None
    assert carried_defaults["state"] == "inherited_defaults_only"
    assert carried_defaults["not_real_inputs"]
    assert planned_steps["execution_policy"] == "plan_only_no_downstream_execution"
    assert not any(step["execution_status"] == "executed_downstream" for step in planned_steps["steps"])
    assert boundary["dry_run"] is True
    assert boundary["sample_fixture_not_real"] is True
    assert boundary["rights_boundary"] == "sample_only_no_publication"
    assert boundary["public_upload_closed"] is True
    assert boundary["yymm4_render_closed"] is True
    assert readiness["deterministic_seed_instantiation_path"] is True
    assert readiness["init_status"]["can_initialize_seed_from_registry_offline"] is True
    assert readiness["init_status"]["used_manual_copy_of_original_pilot"] is False
    assert readiness["init_status"]["can_run_downstream_pipeline_now"] is False
    assert content_candidate["schema_version"] == "content_spine_source_manifest.v1"
    assert content_candidate["candidates"][0]["freshness_status"] == "offline_fixture_not_live"
    assert content_candidate["candidates"][0]["rights_status"] == "sample_only_no_publication"
    assert source_index["artifact_counts"]["source_present"] >= 10
    assert source_index["artifact_counts"]["generated_present"] == len(REQUIRED_FACTORY_SEED_INSTANTIATION_FILES)


def test_factory_seed_instantiation_validation_catches_fake_real_input(tmp_path) -> None:
    output_dir = tmp_path / "factory_seed_dry_run_002"
    instantiate_episode_factory_seed(
        registry_dir=SOURCE_REGISTRY,
        output_dir=output_dir,
        artifact_id="test_factory_seed_instantiation",
    )

    required_path = output_dir / "required_real_inputs.json"
    required_inputs = _load(required_path)
    required_inputs["required_real_inputs"]["topic_or_source_packet"]["value"] = {
        "fake": "do not treat this dry-run value as real"
    }
    required_path.write_text(json.dumps(required_inputs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    readback = validate_factory_seed_instantiation(output_dir, registry_dir=SOURCE_REGISTRY)

    assert readback["status"] == "failed"
    assert "required_real_input_has_dry_run_value:topic_or_source_packet" in readback["failed_checks"]
    assert readback["checks"]["required_real_inputs_separated"] is False


def test_cli_instantiate_episode_factory_seed_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_factory_seed_dry_run_002"

    code = main([
        "instantiate-episode-factory-seed",
        "--registry",
        str(SOURCE_REGISTRY),
        "--output",
        str(output_dir),
        "--artifact-id",
        "test_cli_factory_seed_instantiation",
        "--episode-id",
        "test_cli_yukkuri_newsroom_episode_002_seed",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["episode_id"] == "test_cli_yukkuri_newsroom_episode_002_seed"
    assert payload["primary_machine_readable"].endswith("seed_instantiation_manifest.json")
    assert payload["episode_seed_path"].endswith("episode_seed.json")
    assert payload["topic_source_packet_path"].endswith("dry_run_topic_source_packet.json")
    assert payload["content_spine_input_candidate_path"].endswith("content_spine_input_candidate.json")
    assert (output_dir / "episode_seed.json").exists()


def test_factory_seed_instantiation_text_does_not_claim_forbidden_completion(tmp_path) -> None:
    output_dir = tmp_path / "factory_seed_dry_run_002"
    instantiate_episode_factory_seed(
        registry_dir=SOURCE_REGISTRY,
        output_dir=output_dir,
        artifact_id="test_factory_seed_instantiation",
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
