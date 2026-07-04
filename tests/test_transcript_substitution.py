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
