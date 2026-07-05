from __future__ import annotations

import csv
import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.transcript_substitution import (
    REQUIRED_TRANSCRIPT_SUBSTITUTION_FILES,
    build_transcript_substitution_package,
    validate_transcript_substitution_package,
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


def test_transcript_substitution_uses_sample_fixture_when_no_real_input(tmp_path) -> None:
    output_dir = tmp_path / "transcript_substitution_readiness"

    readback = build_transcript_substitution_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_transcript_substitution",
    )

    assert readback["status"] == "passed"
    assert readback["source_mode"] == "sample_fixture_generated"
    assert readback["transcript_status"] == "sample_fixture_not_real"
    for filename in REQUIRED_TRANSCRIPT_SUBSTITUTION_FILES:
        assert (output_dir / filename).exists(), filename
    assert (output_dir / "real_input" / "README.md").exists()
    assert (output_dir / "sample_inputs" / "notebooklm_like_sample.txt").exists()

    manifest = _load(output_dir / "substitution_manifest.json")
    probe = _load(output_dir / "transcript_source_probe.json")
    episode_bridge = _load(output_dir / "regenerated_episode_bridge.json")
    writer_ir = _load(output_dir / "regenerated_writer_ir_candidate.json")
    cue_readiness = _load(output_dir / "cue_packet_readiness.json")
    source_context = _load(output_dir / "source_context_reference.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    rows = _csv_rows(output_dir / "regenerated_draft_yymm4.csv")

    assert manifest["artifact_kind"] == "real-transcript-substitution-readiness"
    assert manifest["boundaries"]["sample_fixture_is_not_real_transcript"] is True
    assert probe["sample_fixture_used"] is True
    assert probe["access_reality"]["sample_fixture_is_real_transcript"] is False
    assert episode_bridge["source_boundary"]["source_name"] == "Synthetic Baseball Feed"
    assert episode_bridge["transcript_substitution"]["transcript_boundary"]["source_name"] == "NLMYTGen local sample transcript fixture"
    assert episode_bridge["readiness"]["production_status"] == "blocked_until_transcript_timing_and_human_review"
    assert episode_bridge["readiness"]["audio_status"] == "no_audio_generated_or_imported"
    assert writer_ir["compatibility_status"] == "transcript_substitution_candidate_not_validate_ir_ready"
    assert cue_readiness["external_llm_called"] is False
    assert source_context["schema_version"] == "transcript_substitution_source_context_reference.v1"
    assert source_context["transcript_placeholders"]["sample_fixture_used"] is True
    assert source_index["artifact_counts"]["generated_present"] >= len(REQUIRED_TRANSCRIPT_SUBSTITUTION_FILES) - 1
    assert len(rows) == readback["regenerated_csv_rows"]
    assert len(rows) == len(writer_ir["utterances"])


def test_transcript_substitution_accepts_explicit_transcript(tmp_path) -> None:
    transcript = tmp_path / "provided_transcript.txt"
    transcript.write_text(
        "Host1: 今日は速球とスライダーの見え方を確認します。\n"
        "Host2: 155キロのあとに140キロだと、体感が変わるんですね。\n"
        "Host1: ここでは外低めのストライク結果までをサンプルとして扱います。\n",
        encoding="utf-8",
    )
    output_dir = tmp_path / "provided_readiness"

    readback = build_transcript_substitution_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        transcript_path=transcript,
        artifact_id="test_provided_transcript",
        speaker_map={"Host1": "まりさ", "Host2": "れいむ"},
    )

    assert readback["status"] == "passed"
    assert readback["source_mode"] == "provided_transcript"
    assert readback["transcript_status"] == "local_transcript_unverified"

    contract = _load(output_dir / "transcript_input_contract.json")
    writer_ir = _load(output_dir / "regenerated_writer_ir_candidate.json")
    rows = _csv_rows(output_dir / "regenerated_draft_yymm4.csv")

    assert contract["speaker_mapping"]["mapped_speakers"] == ["まりさ", "れいむ"]
    assert contract["speaker_mapping"]["unmapped_speakers"] == []
    assert rows[0] == ["まりさ", "今日は速球とスライダーの見え方を確認します。"]
    assert writer_ir["utterances"][1]["speaker"] == "れいむ"


def test_cli_build_transcript_substitution_json_output(tmp_path, capsys) -> None:
    output_dir = tmp_path / "cli_transcript_substitution"

    code = main([
        "build-transcript-substitution",
        "--package",
        str(SOURCE_PACKAGE),
        "--output",
        str(output_dir),
        "--artifact-id",
        "test_cli_transcript_substitution",
        "--format",
        "json",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "passed"
    assert payload["source_mode"] == "sample_fixture_generated"
    assert (output_dir / "regenerated_writer_ir_candidate.json").exists()
    assert (output_dir / "regenerated_draft_yymm4.csv").exists()


def test_transcript_substitution_builds_second_episode_sample_readiness(tmp_path) -> None:
    output_dir = tmp_path / "transcript_substitution_readiness_002"

    readback = build_transcript_substitution_package(
        package_dir=SOURCE_PACKAGE_002,
        output_dir=output_dir,
        artifact_id="test_transcript_substitution_002",
    )

    assert readback["status"] == "passed"
    assert readback["selected_candidate_id"] == "factory_seed_dry_run_002"
    assert readback["source_mode"] == "sample_fixture_generated"
    assert readback["transcript_status"] == "sample_fixture_not_real"
    for filename in REQUIRED_TRANSCRIPT_SUBSTITUTION_FILES:
        assert (output_dir / filename).exists(), filename
    assert (output_dir / "real_input" / "README.md").exists()
    assert (output_dir / "sample_inputs" / "notebooklm_like_sample.txt").exists()

    manifest = _load(output_dir / "substitution_manifest.json")
    probe = _load(output_dir / "transcript_source_probe.json")
    episode_bridge = _load(output_dir / "regenerated_episode_bridge.json")
    writer_ir = _load(output_dir / "regenerated_writer_ir_candidate.json")
    source_context = _load(output_dir / "source_context_reference.json")
    source_index = _load(output_dir / "source_artifact_index.json")
    saved_readback = _load(output_dir / "validation_readback.json")
    rows = _csv_rows(output_dir / "regenerated_draft_yymm4.csv")

    assert manifest["artifact_id"] == "test_transcript_substitution_002"
    assert manifest["boundaries"]["dry_run"] is True
    assert manifest["boundaries"]["sample_fixture_not_real"] is True
    assert manifest["boundaries"]["no_real_transcript"] is True
    assert manifest["boundaries"]["no_yymm4_import"] is True
    assert manifest["boundary_status"]["public_upload_closed"] is True
    assert manifest["boundary_status"]["yymm4_render_closed"] is True
    assert manifest["boundary_status"]["rights_boundary"] == "sample_only_no_publication"

    assert probe["sample_fixture_used"] is True
    assert probe["access_reality"]["notebooklm_api_used"] is False
    assert episode_bridge["selected_candidate_id"] == "factory_seed_dry_run_002"
    assert episode_bridge["boundary_status"]["dry_run"] is True
    assert episode_bridge["boundary_status"]["no_yymm4_import"] is True
    assert episode_bridge["readiness"]["no_yymm4_import"] is True
    assert episode_bridge["source_boundary"]["freshness_status"] == "offline_fixture_not_live"
    assert writer_ir["compatibility_status"] == "transcript_substitution_candidate_not_validate_ir_ready"

    assert source_context["source_seed_reference_present"] is True
    assert source_context["ir_bridge_reference_present"] is True
    assert source_context["manual_copy_of_original_pilot"] is False
    assert source_context["seed_origin_fields"]["derived_from_episode_seed_id"]
    assert source_context["inherited_template_defaults"]["csv_header_mode"] == "headerless_yymm4_csv"
    assert source_context["dry_run_placeholders"]["topic_source_packet"]["source_reality"] == "sample_fixture_not_real"
    assert source_context["generated_ir_csv_outputs"]["episode_bridge"].endswith("episode_bridge.json")
    assert source_context["transcript_placeholders"]["sample_fixture_used"] is True
    assert source_context["transcript_placeholders"]["sample_fixture_is_real_transcript"] is False
    assert source_context["generated_transcript_outputs"]["regenerated_draft_yymm4_csv"].endswith(
        "regenerated_draft_yymm4.csv"
    )
    for key, value in source_context["required_real_inputs"].items():
        assert value["value"] is None, key

    assert source_index["artifact_counts"]["source_required_present"] == 10
    assert source_index["artifact_counts"]["generated_present"] >= len(REQUIRED_TRANSCRIPT_SUBSTITUTION_FILES) - 1
    assert len(rows) == readback["regenerated_csv_rows"]
    assert len(rows) == len(writer_ir["utterances"])
    assert saved_readback["checks"]["source_origin_separated"] is True
    assert saved_readback["checks"]["transcript_placeholders_separated"] is True
    assert saved_readback["checks"]["dry_run_boundaries_preserved"] is True
    assert saved_readback["checks"]["no_external_references"] is True
    assert saved_readback["checks"]["no_forbidden_completion_claims"] is True


def test_transcript_substitution_validation_catches_second_episode_real_input_claim(tmp_path) -> None:
    output_dir = tmp_path / "transcript_substitution_readiness_002"
    build_transcript_substitution_package(
        package_dir=SOURCE_PACKAGE_002,
        output_dir=output_dir,
        artifact_id="test_transcript_substitution_002",
    )
    source_context = _load(output_dir / "source_context_reference.json")
    source_context["required_real_inputs"]["real_transcript"]["value"] = "pretend transcript"
    (output_dir / "source_context_reference.json").write_text(
        json.dumps(source_context, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    readback = validate_transcript_substitution_package(output_dir)

    assert readback["status"] == "failed"
    assert "required_real_input_has_value:real_transcript" in readback["failed_checks"]


def test_transcript_substitution_validation_catches_missing_csv(tmp_path) -> None:
    output_dir = tmp_path / "transcript_substitution_readiness"
    build_transcript_substitution_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_transcript_substitution",
    )
    (output_dir / "regenerated_draft_yymm4.csv").unlink()

    readback = validate_transcript_substitution_package(output_dir)

    assert readback["status"] == "failed"
    assert "missing_file:regenerated_draft_yymm4.csv" in readback["failed_checks"]
    assert "regenerated_csv_too_short" in readback["failed_checks"]


def test_generated_transcript_substitution_text_does_not_claim_completion(tmp_path) -> None:
    output_dir = tmp_path / "transcript_substitution_readiness"
    build_transcript_substitution_package(
        package_dir=SOURCE_PACKAGE,
        output_dir=output_dir,
        artifact_id="test_transcript_substitution",
    )

    for path in output_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_COMPLETION_CLAIMS:
                assert forbidden not in text, (path.name, forbidden)
