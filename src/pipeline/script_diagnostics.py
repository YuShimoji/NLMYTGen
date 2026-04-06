"""B-18: NotebookLM 由来台本の機械診断（ゆっくり向け手直し前段）。

ヒューリスティックは偽陽性を許容する。拡張点は NLM_MARKER_PATTERNS と本モジュール内コメント。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from src.contracts.structured_script import StructuredScript, Utterance
from src.pipeline.assemble_csv import find_unmapped_speakers
from src.pipeline.normalize import analyze_speaker_roles

DEFAULT_EXPLAINER = "まりさ"
DEFAULT_LISTENER = "れいむ"
DEFAULT_LONG_RUN_THRESHOLD = 6
DEFAULT_LISTENER_AVG_RATIO = 1.25


class DiagSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class ScriptDiagnostic:
    code: str
    severity: DiagSeverity
    utterance_index: int | None
    message: str
    hint: str


# --- NLM / 番組調フレーズ（拡張点: 誤検知が出たら個別に弱める・削除） ---
NLM_MARKER_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"本日はお聞きいただき"),
    re.compile(r"それでは次回"),
    re.compile(r"いかがでしたでしょうか"),
    re.compile(r"いかがでしたか"),
    re.compile(r"今回の(ポッドキャスト|エピソード|番組)"),
    re.compile(r"本エピソードでは"),
    re.compile(r"最後までお付き合い"),
    re.compile(r"チャンネル登録"),
    re.compile(r"高評価お願いします"),
)


def remap_speakers(script: StructuredScript, speaker_map: dict[str, str]) -> StructuredScript:
    """話者名だけ speaker_map で置換した新しい StructuredScript を返す。"""
    if not speaker_map:
        return script
    mapped = tuple(
        Utterance(speaker=speaker_map.get(u.speaker, u.speaker), text=u.text)
        for u in script.utterances
    )
    return StructuredScript(utterances=mapped)


def diagnose_script(
    script: StructuredScript,
    *,
    speaker_map: dict[str, str] | None = None,
    expected_explainer: str = DEFAULT_EXPLAINER,
    expected_listener: str = DEFAULT_LISTENER,
    long_run_threshold: int = DEFAULT_LONG_RUN_THRESHOLD,
    listener_avg_ratio: float = DEFAULT_LISTENER_AVG_RATIO,
    strict: bool = False,
) -> list[ScriptDiagnostic]:
    """StructuredScript に対する診断結果のリスト（安定した順: マップ → 連続 → マーカー → ロール）。"""
    out: list[ScriptDiagnostic] = []
    sm = speaker_map or {}
    remapped = remap_speakers(script, sm)

    if sm:
        unmapped = find_unmapped_speakers(script, sm)
        for name in sorted(unmapped):
            out.append(
                ScriptDiagnostic(
                    code="SPEAKER_MAP_UNMAPPED",
                    severity=DiagSeverity.WARNING,
                    utterance_index=None,
                    message=f"入力話者「{name}」が speaker_map に無い（そのままのラベルで解析）",
                    hint="generate-map または手編集でマップに追加するか、意図した綴りか確認する",
                )
            )

    distinct = sorted({u.speaker for u in remapped.utterances})

    _emit_long_runs(remapped, long_run_threshold, out)
    _emit_nlm_markers(remapped, out)

    if len(distinct) != 2:
        out.append(
            ScriptDiagnostic(
                code="ROLE_SKIPPED_NOT_TWO_SPEAKERS",
                severity=DiagSeverity.INFO,
                utterance_index=None,
                message=f"マップ後の話者数が {len(distinct)}（2 以外）。れいむ/まりさロール整合チェックをスキップ",
                hint="話者マップで 2 キャラに寄せるか、手動で台本を整理する",
            )
        )
        return _maybe_append_strict_error(out, strict, sm)

    roles_data = analyze_speaker_roles(remapped)
    speakers = list(roles_data.keys())
    if len(speakers) != 2:
        return _maybe_append_strict_error(out, strict, sm)

    host_sp = next((s for s in speakers if roles_data[s]["role"] == "host"), None)
    guest_sp = next((s for s in speakers if roles_data[s]["role"] == "guest"), None)
    if host_sp is None or guest_sp is None:
        return _maybe_append_strict_error(out, strict, sm)

    ha = roles_data[host_sp]["avg_length"]
    ga = roles_data[guest_sp]["avg_length"]
    if ha > 0 and ga >= ha * listener_avg_ratio:
        out.append(
            ScriptDiagnostic(
                code="LISTENER_LONG_AVG_DOMINANCE",
                severity=DiagSeverity.WARNING,
                utterance_index=None,
                message=(
                    f"聞き手寄り（guest）と推定された「{guest_sp}」の平均発話長 {ga:.1f} が、"
                    f"解説寄り（host）「{host_sp}」の {ha:.1f} の {listener_avg_ratio} 倍以上"
                ),
                hint="聞き手に長い解説が寄っていないか、話者ラベルと役割の取り違えがないか確認する",
            )
        )

    if not sm:
        out.append(
            ScriptDiagnostic(
                code="ROLE_SKIPPED_NO_MAP",
                severity=DiagSeverity.INFO,
                utterance_index=None,
                message="話者マップなしのため、期待名との一致（EXPLAINER/LISTENER）はスキップ",
                hint="れいむ/まりさへのマップ後に再実行すると、役割とキャラ名の整合を機械チェックできる",
            )
        )
        return _maybe_append_strict_error(out, strict, sm)

    if host_sp != expected_explainer:
        out.append(
            ScriptDiagnostic(
                code="EXPLAINER_ROLE_MISMATCH",
                severity=DiagSeverity.WARNING,
                utterance_index=None,
                message=(
                    f"文量・導入パターン上の host は「{host_sp}」だが、"
                    f"--expected-explainer は「{expected_explainer}」"
                ),
                hint="NotebookLM の Host/解説が聞き手側キャラに付いていないか確認する",
            )
        )
    if guest_sp != expected_listener:
        out.append(
            ScriptDiagnostic(
                code="LISTENER_ROLE_MISMATCH",
                severity=DiagSeverity.WARNING,
                utterance_index=None,
                message=(
                    f"質問・短応答寄りの guest は「{guest_sp}」だが、"
                    f"--expected-listener は「{expected_listener}」"
                ),
                hint="話者マップの左右が逆になっていないか、台本の役割が崩れていないか確認する",
            )
        )

    return _maybe_append_strict_error(out, strict, sm)


def _maybe_append_strict_error(
    items: list[ScriptDiagnostic],
    strict: bool,
    speaker_map: dict[str, str],
) -> list[ScriptDiagnostic]:
    """--strict かつ未マップ話者があるときだけ ERROR を追加。"""
    if not strict or not speaker_map:
        return items
    if not any(d.code == "SPEAKER_MAP_UNMAPPED" for d in items):
        return items
    dup = list(items)
    dup.append(
        ScriptDiagnostic(
            code="SPEAKER_MAP_STRICT",
            severity=DiagSeverity.ERROR,
            utterance_index=None,
            message="話者マップに未登録の入力話者がある（--strict では失敗）",
            hint="全話者をマップに含めるか --strict を外す",
        )
    )
    return dup


def _emit_long_runs(
    script: StructuredScript,
    threshold: int,
    out: list[ScriptDiagnostic],
) -> None:
    if threshold < 2:
        return
    run_start = 0
    current = script.utterances[0].speaker if script.utterances else None
    for i in range(1, len(script.utterances)):
        sp = script.utterances[i].speaker
        if sp != current:
            length = i - run_start
            if length >= threshold and current is not None:
                out.append(
                    ScriptDiagnostic(
                        code="LONG_RUN_SAME_SPEAKER",
                        severity=DiagSeverity.WARNING,
                        utterance_index=run_start,
                        message=(
                            f"話者「{current}」が {length} 発話連続 "
                            f"(index {run_start}〜{i - 1})"
                        ),
                        hint="ラベル貼り間違いや、NLM のブロック貼り付けで聞き手行が抜けていないか確認する",
                    )
                )
            run_start = i
            current = sp
    if script.utterances and current is not None:
        length = len(script.utterances) - run_start
        if length >= threshold:
            out.append(
                ScriptDiagnostic(
                    code="LONG_RUN_SAME_SPEAKER",
                    severity=DiagSeverity.WARNING,
                    utterance_index=run_start,
                    message=(
                        f"話者「{current}」が {length} 発話連続 "
                        f"(index {run_start}〜{len(script.utterances) - 1})"
                    ),
                    hint="ラベル貼り間違いや、NLM のブロック貼り付けで聞き手行が抜けていないか確認する",
                )
            )


def _emit_nlm_markers(script: StructuredScript, out: list[ScriptDiagnostic]) -> None:
    for i, u in enumerate(script.utterances):
        for pat in NLM_MARKER_PATTERNS:
            if pat.search(u.text):
                out.append(
                    ScriptDiagnostic(
                        code="NLM_STYLE_MARKER",
                        severity=DiagSeverity.WARNING,
                        utterance_index=i,
                        message="NLM/番組調フレーズの可能性（正規表現マッチ）",
                        hint="ゆっくり口調・会話体に書き換えるか、カットする（C-09 プロンプト参照）",
                    )
                )
                break


def diagnostics_to_jsonable(
    diagnostics: list[ScriptDiagnostic],
    *,
    meta: dict[str, object],
) -> dict[str, object]:
    """CLI / GUI 用の JSON シリアライズ可能な dict。"""
    return {
        "meta": meta,
        "diagnostics": [
            {
                "code": d.code,
                "severity": d.severity.value,
                "utterance_index": d.utterance_index,
                "message": d.message,
                "hint": d.hint,
            }
            for d in diagnostics
        ],
    }


def has_error(diagnostics: list[ScriptDiagnostic]) -> bool:
    return any(d.severity == DiagSeverity.ERROR for d in diagnostics)
