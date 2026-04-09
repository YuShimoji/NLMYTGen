"""運用コーパス由来の forbidden 位置を JSON でデータ駆動検証する."""

import json
from pathlib import Path

import pytest

from src.pipeline.assemble_csv import _forbidden_structural_split

_DATA = Path(__file__).resolve().parent / "data" / "linebreak_forbidden_corpus.json"


@pytest.mark.parametrize(
    "case",
    json.loads(_DATA.read_text(encoding="utf-8")),
    ids=lambda c: c.get("note", c["text"][:8]),
)
def test_linebreak_forbidden_corpus(case: dict) -> None:
    text = case["text"]
    pos = case["pos"]
    expected = case["expected_forbidden"]
    assert _forbidden_structural_split(text, pos) is expected
