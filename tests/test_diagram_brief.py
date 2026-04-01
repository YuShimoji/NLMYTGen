"""B-16 diagram brief packet tests."""

import json
import subprocess
import sys

from src.contracts.structured_script import StructuredScript, Utterance
from src.pipeline.diagram_brief import build_diagram_brief_payload, render_diagram_brief_markdown


def test_build_diagram_brief_payload_includes_contract_and_section_seeds():
    script = StructuredScript(utterances=(
        Utterance(speaker="Speaker_A", text="まず最初に監視の仕組みを見ていきます。"),
        Utterance(speaker="Speaker_B", text="図で見ると分かりやすそうですね。"),
    ))

    payload = build_diagram_brief_payload(
        script,
        source_name="sample.txt",
        speaker_map={"Speaker_A": "れいむ", "Speaker_B": "まりさ"},
    )

    assert payload["feature_id"] == "B-16"
    assert payload["phase"] == "diagram-brief-only"
    assert payload["context"]["speaker_map"]["Speaker_A"] == "れいむ"
    assert payload["context"]["section_seeds"]
    assert payload["response_preferences"]["operator_todos_max"] == 4
    assert payload["response_preferences"]["avoid_repeating_b15_cue_memo"] is True
    assert "diagram_briefs" in payload["output_contract"]


def test_render_diagram_brief_markdown_mentions_text_only_boundary():
    script = StructuredScript(utterances=(
        Utterance(speaker="Speaker_A", text="まず最初に監視の仕組みを見ていきます。"),
        Utterance(speaker="Speaker_B", text="図で見ると分かりやすそうですね。"),
    ))
    payload = build_diagram_brief_payload(script, source_name="sample.txt")

    text = render_diagram_brief_markdown(payload)

    assert "# B-16 Diagram Brief Request Packet" in text
    assert "Do not generate images, diagram files, or YMM4 direct edits." in text
    assert "Skip sections that would be better handled by B-15 style background cues alone." in text
    assert "Role analysis" in text
    assert "Response Preferences" in text
    assert "[Speaker_A | src=Speaker_A]" in text


def test_cli_build_diagram_packet_writes_json(tmp_path):
    input_txt = tmp_path / "in.txt"
    input_txt.write_text(
        "Speaker_A: まず監視の構造を見ていきます\n"
        "Speaker_B: 図だと整理しやすそうですね\n",
        encoding="utf-8",
    )
    out_json = tmp_path / "packet.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli.main",
            "build-diagram-packet",
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
    assert data["feature_id"] == "B-16"
    assert data["transcript"][0]["speaker"] == "Speaker_A"
    assert "diagram_briefs" in data["output_contract"]
    assert "must_include" in data["output_contract"]["diagram_briefs"][0]


def test_cli_build_diagram_packet_bundle_writes_rerun_helpers_too(tmp_path):
    input_txt = tmp_path / "in.txt"
    input_txt.write_text(
        "Speaker_A: まず監視の構造を見ていきます\n"
        "Speaker_B: 図だと整理しやすそうですね\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "bundle"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli.main",
            "build-diagram-packet",
            str(input_txt),
            "--bundle-dir",
            str(out_dir),
        ],
        capture_output=True,
        text=True,
        cwd=str(_project_root()),
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert (out_dir / "in_diagram_packet.md").exists()
    assert (out_dir / "in_diagram_packet.json").exists()
    assert (out_dir / "in_diagram_workflow_proof.md").exists()
    assert (out_dir / "in_diagram_rerun_prompt.txt").exists()
    assert (out_dir / "in_diagram_rerun_diff_template.md").exists()
    assert (out_dir / "in_diagram_quickstart.md").exists()
    assert (out_dir / "in_diagram_baseline_notes.md").exists()


def _project_root():
    from pathlib import Path
    return Path(__file__).resolve().parent.parent
