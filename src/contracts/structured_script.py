"""内部データ契約: 構造化スクリプト。

パイプライン内部で使用する中間表現。
入力フォーマットに依存せず、出力 (YMM4 CSV) に必要な情報のみを保持する。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Utterance:
    """1発話。話者名とテキストのペア。"""

    speaker: str
    text: str

    def __post_init__(self) -> None:
        if not self.speaker or not self.speaker.strip():
            raise ValueError("speaker must not be empty")
        if not self.text or not self.text.strip():
            raise ValueError("text must not be empty")


@dataclass(frozen=True)
class StructuredScript:
    """構造化済み台本。Utterance の順序付きリスト。"""

    utterances: tuple[Utterance, ...]

    def __post_init__(self) -> None:
        if not self.utterances:
            raise ValueError("utterances must not be empty")
