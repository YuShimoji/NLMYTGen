"""B-18 script_diagnostics の単体テスト。"""

from __future__ import annotations

import pytest

from src.contracts.structured_script import StructuredScript, Utterance
from src.pipeline.script_diagnostics import (
    DEFAULT_LONG_RUN_THRESHOLD,
    diagnose_script,
    has_error,
    remap_speakers,
)


def _script(*pairs: tuple[str, str]) -> StructuredScript:
    return StructuredScript(
        utterances=tuple(Utterance(speaker=a, text=b) for a, b in pairs)
    )


def test_remap_speakers() -> None:
    s = _script(("A", "hello"), ("B", "world"))
    m = remap_speakers(s, {"A": "れいむ"})
    assert m.utterances[0].speaker == "れいむ"
    assert m.utterances[1].speaker == "B"


def test_speaker_map_unmapped_and_strict_error() -> None:
    s = _script(("Host1", "a"), ("Host2", "b"))
    sm = {"Host1": "れいむ"}
    r = diagnose_script(s, speaker_map=sm, strict=False)
    codes = [d.code for d in r]
    assert "SPEAKER_MAP_UNMAPPED" in codes
    assert not has_error(r)

    r_strict = diagnose_script(s, speaker_map=sm, strict=True)
    assert has_error(r_strict)
    assert any(d.code == "SPEAKER_MAP_STRICT" for d in r_strict)


def test_three_speakers_skips_role_pair() -> None:
    s = _script(("A", "1"), ("B", "2"), ("C", "3"))
    r = diagnose_script(s, speaker_map={"A": "れいむ", "B": "まりさ", "C": "ナレーター"})
    assert any(d.code == "ROLE_SKIPPED_NOT_TWO_SPEAKERS" for d in r)


def test_nlm_style_marker() -> None:
    s = _script(("Host1", "本エピソードではテストします。"), ("Host2", "はい。"))
    r = diagnose_script(s)
    assert any(d.code == "NLM_STYLE_MARKER" and d.utterance_index == 0 for d in r)


def test_long_run_same_speaker() -> None:
    lines = [("Host1", f"line{i}。") for i in range(DEFAULT_LONG_RUN_THRESHOLD)]
    s = _script(*lines)
    r = diagnose_script(s, long_run_threshold=DEFAULT_LONG_RUN_THRESHOLD)
    assert any(d.code == "LONG_RUN_SAME_SPEAKER" for d in r)


def test_explainer_role_mismatch_when_map_swapped_content() -> None:
    # Host1 が長文・導入寄り → analyze で host になりやすい
    s = _script(
        ("Host1", "というわけで今回は詳しく説明していきます。長い解説の続きです。"),
        ("Host2", "ええ。"),
        ("Host1", "次のポイントも重要です。データによると傾向が見えます。"),
        ("Host2", "なるほど。"),
    )
    sm = {"Host1": "れいむ", "Host2": "まりさ"}
    r = diagnose_script(
        s,
        speaker_map=sm,
        expected_explainer="まりさ",
        expected_listener="れいむ",
    )
    assert any(d.code == "EXPLAINER_ROLE_MISMATCH" for d in r)


def test_no_map_emits_role_skipped_no_map_with_two_speakers() -> None:
    s = _script(("Host1", "短い。"), ("Host2", "というわけで長めの解説を続けます。内容は続きです。"))
    r = diagnose_script(s, speaker_map=None)
    assert any(d.code == "ROLE_SKIPPED_NO_MAP" for d in r)


def test_aligned_map_no_mismatch() -> None:
    s = _script(
        ("Host1", "ええ。"),
        ("Host2", "というわけで今回は解説します。ポイントは三つあります。"),
        ("Host1", "そうなの？"),
        ("Host2", "まず一つ目です。詳しく見ていきましょう。"),
    )
    sm = {"Host1": "れいむ", "Host2": "まりさ"}
    r = diagnose_script(
        s,
        speaker_map=sm,
        expected_explainer="まりさ",
        expected_listener="れいむ",
    )
    assert not any(d.code == "EXPLAINER_ROLE_MISMATCH" for d in r)
    assert not any(d.code == "LISTENER_ROLE_MISMATCH" for d in r)


def test_listener_long_avg_dominance(monkeypatch: pytest.MonkeyPatch) -> None:
    """guest 平均 > host 平均 * ratio の分岐を、ロール推定を差し替えて検証する。"""

    def fake_analyze(_script: StructuredScript) -> dict[str, dict]:
        return {
            "まりさ": {
                "utterances": 1,
                "avg_length": 10.0,
                "short_responses": 0,
                "questions": 0,
                "topic_intros": 0,
                "role": "host",
            },
            "れいむ": {
                "utterances": 1,
                "avg_length": 50.0,
                "short_responses": 0,
                "questions": 0,
                "topic_intros": 0,
                "role": "guest",
            },
        }

    monkeypatch.setattr(
        "src.pipeline.script_diagnostics.analyze_speaker_roles",
        fake_analyze,
    )
    s = _script(("れいむ", "x" * 50), ("まりさ", "short"))
    r = diagnose_script(s, listener_avg_ratio=1.25)
    assert any(d.code == "LISTENER_LONG_AVG_DOMINANCE" for d in r)


@pytest.mark.parametrize(
    "strict,expect_err",
    [(False, False), (True, True)],
)
def test_strict_only_adds_error_flag(strict: bool, expect_err: bool) -> None:
    s = _script(("Host1", "a"), ("Host2", "b"))
    sm = {"Host1": "れいむ"}
    r = diagnose_script(s, speaker_map=sm, strict=strict)
    assert has_error(r) is expect_err
