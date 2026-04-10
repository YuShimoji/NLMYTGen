"""emit-packaging-brief-template の内容が仕様と整合するか。"""

import json
from pathlib import Path

from src.cli.main import main
from src.pipeline.packaging_brief_template import (
    REQUIRED_JSON_KEYS,
    REQUIRED_MARKDOWN_SECTIONS,
    emit_json_text,
    emit_markdown,
    minimal_json_brief,
)


def test_markdown_template_has_required_headers() -> None:
    md = emit_markdown()
    assert "# Packaging Orchestrator Brief" in md
    assert "## required_evidence" in md
    assert "brief_version:" in md
    for section in REQUIRED_MARKDOWN_SECTIONS:
        assert section in md
    assert md.endswith("\n")


def test_minimal_json_roundtrip_and_keys() -> None:
    data = minimal_json_brief()
    assert data["brief_version"] == "0.1"
    assert data["video_id"] == "replace_me"
    assert isinstance(data["required_evidence"], list)
    for key in REQUIRED_JSON_KEYS:
        assert key in data
    parsed = json.loads(emit_json_text())
    assert parsed["brief_version"] == data["brief_version"]
    assert isinstance(parsed["thumbnail_controls"], dict)
    assert "rotation_axes" in parsed["thumbnail_controls"]


def test_cli_emit_packaging_brief_template_json(capsys) -> None:
    code = main(["emit-packaging-brief-template", "--format", "json"])
    assert code == 0
    out = capsys.readouterr().out
    parsed = json.loads(out)
    for key in REQUIRED_JSON_KEYS:
        assert key in parsed


def test_cli_emit_packaging_brief_template_markdown_to_file(tmp_path: Path) -> None:
    out_path = tmp_path / "h01_template.md"
    code = main([
        "emit-packaging-brief-template",
        "--format",
        "markdown",
        "--output",
        str(out_path),
    ])
    assert code == 0
    text = out_path.read_text(encoding="utf-8")
    assert text.startswith("# Packaging Orchestrator Brief")
    assert "## alignment_check" in text
