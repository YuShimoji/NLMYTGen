"""B-15 cue packet tests."""

import json
import subprocess
import sys

import pytest

from src.contracts.structured_script import StructuredScript, Utterance
from src.pipeline.cue_packet import build_cue_packet_payload, render_cue_packet_markdown


def test_build_cue_packet_payload_includes_constraints_and_transcript():
    script = StructuredScript(utterances=(
        Utterance(speaker="Speaker_A", text="というわけで今回はAI監視を見ていきます。"),
        Utterance(speaker="Speaker_B", text="なるほど、どこが問題なんですか？"),
    ))

    payload = build_cue_packet_payload(
        script,
        source_name="sample.txt",
        speaker_map={"Speaker_A": "れいむ", "Speaker_B": "まりさ"},
    )

    assert payload["feature_id"] == "B-15"
    assert payload["phase"] == "phase1-cue-memo-only"
    assert payload["source_name"] == "sample.txt"
    assert payload["context"]["speaker_map"]["Speaker_A"] == "れいむ"
    assert payload["transcript"][0]["mapped_speaker"] == "れいむ"
    assert payload["context"]["section_seeds"]
    assert payload["response_preferences"]["operator_todos_max"] == 4
    assert any("Do not generate a new primary script" in item for item in payload["constraints"])


def test_render_cue_packet_markdown_mentions_boundary_and_roles():
    script = StructuredScript(utterances=(
        Utterance(speaker="Speaker_A", text="というわけで今回はAI監視を見ていきます。"),
        Utterance(speaker="Speaker_B", text="はい。"),
    ))
    payload = build_cue_packet_payload(script, source_name="sample.txt")

    text = render_cue_packet_markdown(payload)

    assert "# B-15 Cue Memo Request Packet" in text
    assert "Do not rewrite the transcript." in text
    assert "Role analysis" in text
    assert "Suggested section seeds" in text
    assert "Response Preferences" in text
    assert "[Speaker_A | src=Speaker_A]" in text


@pytest.mark.integration
def test_cli_build_cue_packet_writes_json(tmp_path):
    input_txt = tmp_path / "in.txt"
    input_txt.write_text(
        "Speaker_A: 今回は監視労働の話です\n"
        "Speaker_B: それは気になりますね\n",
        encoding="utf-8",
    )
    out_json = tmp_path / "packet.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli.main",
            "build-cue-packet",
            str(input_txt),
            "--format",
            "json",
            "-o",
            str(out_json),
        ],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["feature_id"] == "B-15"
    assert data["transcript"][0]["speaker"] == "Speaker_A"
    assert data["output_contract"]["sections"][0]["section_id"] == "S1"
    assert "primary_background" in data["output_contract"]["sections"][0]
    assert "sound_cue_optional" in data["output_contract"]["sections"][0]


@pytest.mark.integration
def test_cli_build_cue_packet_bundle_writes_three_files(tmp_path):
    input_txt = tmp_path / "in.txt"
    input_txt.write_text(
        "Speaker_A: まず最初の論点です\n"
        "Speaker_B: はい\n"
        "Speaker_A: 次に二つ目の論点です\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "bundle"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli.main",
            "build-cue-packet",
            str(input_txt),
            "--bundle-dir",
            str(out_dir),
        ],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert (out_dir / "in_cue_packet.md").exists()
    assert (out_dir / "in_cue_packet.json").exists()
    assert (out_dir / "in_cue_workflow_proof.md").exists()


@pytest.mark.integration
def test_cli_build_cue_packet_bundle_preserves_existing_proof_log(tmp_path):
    input_txt = tmp_path / "in.txt"
    input_txt.write_text(
        "Speaker_A: まず最初の論点です\n"
        "Speaker_B: はい\n"
        "Speaker_A: 次に二つ目の論点です\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "bundle"
    out_dir.mkdir()
    proof_path = out_dir / "in_cue_workflow_proof.md"
    proof_path.write_text("existing proof\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli.main",
            "build-cue-packet",
            str(input_txt),
            "--bundle-dir",
            str(out_dir),
        ],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert proof_path.read_text(encoding="utf-8") == "existing proof\n"


def _project_root():
    from pathlib import Path
    return Path(__file__).resolve().parent.parent
