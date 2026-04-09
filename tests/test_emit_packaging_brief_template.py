"""emit-packaging-brief-template の内容が仕様と整合するか。"""

import json

from src.pipeline.packaging_brief_template import (
    emit_json_text,
    emit_markdown,
    minimal_json_brief,
)


def test_markdown_template_has_required_headers() -> None:
    md = emit_markdown()
    assert "# Packaging Orchestrator Brief" in md
    assert "## required_evidence" in md
    assert "brief_version:" in md


def test_minimal_json_roundtrip_and_keys() -> None:
    data = minimal_json_brief()
    assert data["brief_version"] == "0.1"
    assert data["video_id"] == "replace_me"
    assert isinstance(data["required_evidence"], list)
    parsed = json.loads(emit_json_text())
    assert parsed["brief_version"] == data["brief_version"]
