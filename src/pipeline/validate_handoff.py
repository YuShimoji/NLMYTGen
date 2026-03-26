"""Handoff 前検証: YMM4CsvOutput の整合性チェック。

全チェックは Warning ベース。致命的エラー (空フィールド) のみ書き出しを中止する。
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from src.contracts.ymm4_csv_schema import YMM4CsvOutput

TEXT_LENGTH_WARN_THRESHOLD = 200


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class ValidationResult:
    """検証結果の 1件。"""

    severity: Severity
    row_index: int
    message: str


def validate(output: YMM4CsvOutput) -> list[ValidationResult]:
    """YMM4CsvOutput を検証する。

    Returns:
        検証結果のリスト。空なら問題なし。
    """
    results: list[ValidationResult] = []

    for i, row in enumerate(output.rows):
        if not row.speaker or not row.speaker.strip():
            results.append(
                ValidationResult(Severity.ERROR, i, "empty speaker")
            )
        if not row.text or not row.text.strip():
            results.append(
                ValidationResult(Severity.ERROR, i, "empty text")
            )
        if len(row.text) > TEXT_LENGTH_WARN_THRESHOLD:
            results.append(
                ValidationResult(
                    Severity.WARNING,
                    i,
                    f"text length {len(row.text)} exceeds {TEXT_LENGTH_WARN_THRESHOLD}",
                )
            )

    return results


def has_errors(results: list[ValidationResult]) -> bool:
    """致命的エラーが含まれるか判定する。"""
    return any(r.severity == Severity.ERROR for r in results)
