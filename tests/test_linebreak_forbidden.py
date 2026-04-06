"""Reflow v2 構造分割禁止位置 (_forbidden_structural_split) の回帰テスト。"""

from src.pipeline.assemble_csv import _forbidden_structural_split


def test_forbidden_digit_before_year_or_kanji() -> None:
    assert _forbidden_structural_split("2023年の話", 4)
    assert _forbidden_structural_split("1失点に抑えた", 1)


def test_forbidden_cjk_before_geminate_tsu() -> None:
    assert _forbidden_structural_split("見間違った", 3)


def test_forbidden_cjk_single_okurigana() -> None:
    assert _forbidden_structural_split("入り込む", 3)


def test_forbidden_tilde_before_dewa() -> None:
    # pos は「右片の先頭インデックス」。「では」の直前で切るなら ～ の直後 = index 6
    assert _forbidden_structural_split("サンプル～～では、続き", 6)


def test_forbidden_cjk_before_eru() -> None:
    assert _forbidden_structural_split("抑える投手", 1)


def test_aruiwa_not_forbidden_after_aru() -> None:
    assert not _forbidden_structural_split("対策あるいは見送り", 2)


def test_particle_ha_after_cjk_allowed_for_single_mora_rule() -> None:
    assert not _forbidden_structural_split("問題は別だ", 2)
