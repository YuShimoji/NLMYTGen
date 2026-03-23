"""入力データ契約: NotebookLM 由来のテキスト。

NotebookLM の Audio Overview transcript や手動テキスト化の結果を受け取る。
バリデーション済みの生テキストを保持する。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

MIN_TEXT_LENGTH = 10


@dataclass(frozen=True)
class RawTranscript:
    """NotebookLM から得たテキスト。"""

    text: str
    source_path: Path | None = None

    def __post_init__(self) -> None:
        if not self.text or not self.text.strip():
            raise ValueError("text must not be empty")
        if len(self.text.strip()) < MIN_TEXT_LENGTH:
            raise ValueError(
                f"text must be at least {MIN_TEXT_LENGTH} characters, "
                f"got {len(self.text.strip())}"
            )


def load_transcript(path: Path) -> RawTranscript:
    """ファイルから RawTranscript を読み込む。"""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    text = path.read_text(encoding="utf-8")
    return RawTranscript(text=text, source_path=path)
