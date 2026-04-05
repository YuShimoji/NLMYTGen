"""IR 品質 gate: apply-production の前に品質問題を事前検出する.

face 偏り、unknown labels、連続 run、idle_face 未指定、bg 未設定を検出。
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field


@dataclass
class IRValidationResult:
    """IR 品質検証の結果."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)
    face_distribution: dict[str, int] = field(default_factory=dict)
    unknown_labels: list[str] = field(default_factory=list)
    longest_face_run: int = 0
    longest_face_run_label: str = ""
    idle_face_coverage: float = 0.0

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0


def validate_ir(
    ir_data: dict,
    known_face_labels: set[str] | None = None,
    *,
    serious_threshold: float = 0.40,
    max_consecutive_run: int = 4,
) -> IRValidationResult:
    """IR の品質問題を検出する.

    Parameters
    ----------
    ir_data : dict
        load_ir() 後の IR データ
    known_face_labels : set[str] | None
        palette に存在する face ラベル。None なら unknown label チェックをスキップ
    serious_threshold : float
        serious の許容上限割合 (0.40 = 40%)
    max_consecutive_run : int
        同一 face の連続許容数

    Returns
    -------
    IRValidationResult
    """
    result = IRValidationResult()
    utterances = ir_data.get("utterances", [])
    sections = ir_data.get("macro", {}).get("sections", [])

    if not utterances:
        result.errors.append("IR has no utterances")
        return result

    # carry-forward を解決して face 分布を取得
    from src.pipeline.ymmp_patch import _resolve_carry_forward
    resolved = _resolve_carry_forward(ir_data)

    # --- face distribution ---
    face_counts: Counter = Counter()
    for entry in resolved:
        face = entry.get("face", "")
        if face:
            face_counts[face] += 1
    total = sum(face_counts.values())
    result.face_distribution = dict(face_counts)

    # serious 偏り
    if total > 0:
        serious_pct = face_counts.get("serious", 0) / total
        if serious_pct > serious_threshold:
            result.warnings.append(
                f"face 'serious' is {serious_pct:.0%} of utterances"
                f" (threshold: {serious_threshold:.0%})"
            )

    # unknown labels
    if known_face_labels is not None:
        unknown = sorted(set(face_counts.keys()) - known_face_labels)
        if unknown:
            result.unknown_labels = unknown
            for label in unknown:
                count = face_counts[label]
                result.errors.append(
                    f"unknown face label '{label}' used {count} times"
                    f" (not in palette)"
                )

    # 連続 run
    run_label = ""
    run_len = 0
    max_run = 0
    max_run_label = ""
    max_run_start = 0
    for i, entry in enumerate(resolved):
        face = entry.get("face", "")
        if face == run_label:
            run_len += 1
        else:
            if run_len > max_run:
                max_run = run_len
                max_run_label = run_label
                max_run_start = i - run_len + 1
            run_label = face
            run_len = 1
    if run_len > max_run:
        max_run = run_len
        max_run_label = run_label
        max_run_start = len(resolved) - run_len + 1
    result.longest_face_run = max_run
    result.longest_face_run_label = max_run_label

    if max_run > max_consecutive_run:
        result.warnings.append(
            f"face '{max_run_label}' runs {max_run} consecutive"
            f" utterances (from utt {max_run_start},"
            f" max allowed: {max_consecutive_run})"
        )

    # idle_face 未指定
    idle_count = sum(1 for e in resolved if e.get("idle_face"))
    if total > 0:
        result.idle_face_coverage = idle_count / total
    if idle_count == 0:
        result.warnings.append(
            "idle_face is not specified in any utterance"
        )

    # bg 未設定
    bg_labels = [s.get("default_bg", "") for s in sections]
    bg_set = {b for b in bg_labels if b}
    if not bg_set:
        result.warnings.append(
            "no bg labels defined in macro.sections"
        )

    # row_start 未付与
    has_row = sum(1 for u in utterances if u.get("row_start") is not None)
    if has_row == 0 and len(utterances) > 0:
        result.info.append(
            "row_start/row_end not set."
            " Use annotate-row-range or apply-production --csv"
        )

    return result
