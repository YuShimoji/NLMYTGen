"""split_long_utterances の分割ロジックテスト。

B-04 品質改善: 表示幅ベースの分割をテストする。
"""

import pytest

from src.contracts.ymm4_csv_schema import YMM4CsvOutput, YMM4CsvRow
from src.pipeline.assemble_csv import (
    balance_subtitle_lines,
    display_width,
    estimate_display_lines,
    reflow_subtitles,
    reflow_subtitles_v2,
    reflow_utterance,
    reflow_utterance_v2,
    split_long_utterances,
)


class TestDisplayWidth:
    """display_width() のテスト。"""

    def test_fullwidth_only(self):
        """全角文字のみ: 文字数の2倍。"""
        assert display_width("あいうえお") == 10

    def test_halfwidth_only(self):
        """半角英数のみ: 文字数と同じ。"""
        assert display_width("hello") == 5

    def test_mixed(self):
        """全角半角混合。"""
        # "AIの" = A(1) + I(1) + の(2) = 4
        assert display_width("AIの") == 4

    def test_empty(self):
        assert display_width("") == 0

    def test_east_asian_ambiguous(self):
        """East Asian Ambiguous は全角扱い。"""
        # ～ (U+FF5E) は Fullwidth, ~ (U+301C) は Wide
        # ① (U+2460) は Ambiguous → 全角扱い
        assert display_width("①") == 2

    def test_fullwidth_punctuation(self):
        """全角句読点は幅2。"""
        assert display_width("。") == 2
        assert display_width("、") == 2


class TestSplitBackwardCompatibility:
    """display_width=False (デフォルト) で従来と同一動作。"""

    def _make_output(self, *texts: str, speaker: str = "れいむ") -> YMM4CsvOutput:
        return YMM4CsvOutput(rows=tuple(YMM4CsvRow(speaker=speaker, text=t) for t in texts))

    def test_short_text_not_split(self):
        output = self._make_output("短いテキスト。")
        result = split_long_utterances(output, max_length=80)
        assert len(result.rows) == 1

    def test_long_text_split_at_sentence_end(self):
        text = "最初の文です。二番目の文です。三番目の文です。"
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=20)
        assert len(result.rows) >= 2
        # 再結合すると元のテキストになる
        assert "".join(r.text for r in result.rows) == text

    def test_long_single_sentence_inside_multi_sentence_row_is_expanded(self):
        """複数文の先頭にある長文も、文ごとの fallback で再分割する。"""
        text = (
            "私たちが普段「アルゴリズムによる最適化」と聞くと、効率的でクリーンな魔法を想像しがちですが、"
            "もしその計算式に「人間の身体的限界」という変数が最初から欠落していたらどうなるか。"
            "今回の探求では、その裏側に切り込んでいきます。"
        )
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=80, use_display_width=True)
        assert len(result.rows) >= 3
        assert "".join(r.text for r in result.rows) == text

    def test_single_sentence_preserved_without_clause_break(self):
        """節分割候補のない長文はそのまま保持。"""
        text = "a" * 200
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=80)
        assert len(result.rows) == 1
        assert result.rows[0].text == text

    def test_single_sentence_split_at_clause_break(self):
        """句点がなくても読点で節分割する。"""
        text = "前半の説明が長く続き、後半の説明もまだ続いています"
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=28, use_display_width=True)
        assert len(result.rows) == 2
        assert "".join(r.text for r in result.rows) == text

    def test_speaker_preserved(self):
        output = self._make_output("長い文です。もう一つの文です。", speaker="まりさ")
        result = split_long_utterances(output, max_length=10)
        for row in result.rows:
            assert row.speaker == "まりさ"


class TestSplitDisplayWidth:
    """use_display_width=True のテスト。"""

    def _make_output(self, *texts: str, speaker: str = "れいむ") -> YMM4CsvOutput:
        return YMM4CsvOutput(rows=tuple(YMM4CsvRow(speaker=speaker, text=t) for t in texts))

    def test_fullwidth_triggers_split(self):
        """全角80文字 = display_width 160。max_length=120 で分割される。"""
        text = "あ" * 40 + "。" + "い" * 40 + "。"
        output = self._make_output(text)
        # len(text) = 82, but display_width = 164
        result = split_long_utterances(output, max_length=120, use_display_width=True)
        assert len(result.rows) == 2

    def test_fullwidth_no_split_with_len(self):
        """同じテキストが use_display_width=False だと分割されない。"""
        text = "あ" * 40 + "。" + "い" * 40 + "。"
        output = self._make_output(text)
        # len(text) = 82 <= 120
        result = split_long_utterances(output, max_length=120, use_display_width=False)
        assert len(result.rows) == 1

    def test_halfwidth_within_display_limit(self):
        """半角多めで文字数は超過するが表示幅は閾値内 → 分割されない。"""
        text = "a" * 50 + "." + "b" * 50 + "."
        output = self._make_output(text)
        # len = 102, display_width = 102 (all halfwidth)
        result = split_long_utterances(output, max_length=120, use_display_width=True)
        assert len(result.rows) == 1

    def test_reconstruct_original(self):
        """分割後に再結合すると元のテキストになる。"""
        text = "最初の説明文です。次に重要なポイントを述べます。最後にまとめです。"
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=30, use_display_width=True)
        assert "".join(r.text for r in result.rows) == text

    def test_single_sentence_no_split_point(self):
        """文末も節分割候補もない長文は display_width モードでもそのまま保持。"""
        text = "あ" * 100  # no sentence end
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=80, use_display_width=True)
        assert len(result.rows) == 1

    def test_single_sentence_split_before_connector(self):
        """接続句の直前でも節分割できる。"""
        text = "最初に状況を説明しますしかしここから結論に入ります"
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=28, use_display_width=True)
        assert len(result.rows) == 2
        assert result.rows[0].text.endswith("します")
        assert result.rows[1].text.startswith("しかし")
        assert "".join(r.text for r in result.rows) == text

    def test_single_sentence_split_after_quote_phrase(self):
        """通常候補が尽きた残り長文でも、引用句+機能語で節分割できる。"""
        text = "もしその計算式に「人間の身体的限界」という変数が最初から欠落していたらどうなるか。"
        output = self._make_output(text)
        result = split_long_utterances(output, max_length=28, use_display_width=True)
        assert len(result.rows) >= 2
        assert "".join(r.text for r in result.rows) == text


class TestBalanceSubtitleLines:
    """balance_subtitle_lines() のテスト。"""

    def _make_output(self, *texts: str, speaker: str = "れいむ") -> YMM4CsvOutput:
        return YMM4CsvOutput(rows=tuple(YMM4CsvRow(speaker=speaker, text=t) for t in texts))

    def test_inserts_balanced_newline_after_comma(self):
        output = self._make_output("AAAAAA、BBBBBB")
        result = balance_subtitle_lines(output, chars_per_line=8, max_lines=2, use_display_width=True)
        assert result.rows[0].text == "AAAAAA、\nBBBBBB"
        assert estimate_display_lines(result.rows[0].text, 8) == 2

    def test_preserves_text_without_candidate(self):
        text = "ABCDEFGHIJKLMN"
        output = self._make_output(text)
        result = balance_subtitle_lines(output, chars_per_line=8, max_lines=2, use_display_width=True)
        assert result.rows[0].text == text

    def test_no_change_when_already_within_one_line(self):
        text = "短い文。"
        output = self._make_output(text)
        result = balance_subtitle_lines(output, chars_per_line=20, max_lines=2, use_display_width=True)
        assert result.rows[0].text == text

    def test_only_applies_to_two_line_mode(self):
        text = "AAAAAA、BBBBBB"
        output = self._make_output(text)
        result = balance_subtitle_lines(output, chars_per_line=8, max_lines=3, use_display_width=True)
        assert result.rows[0].text == text

    def test_avoids_one_character_second_line(self):
        text = "ABCDEFG、HI"
        output = self._make_output(text)
        result = balance_subtitle_lines(output, chars_per_line=8, max_lines=2, use_display_width=True)
        assert result.rows[0].text == text


class TestReflowUtterance:
    """B-15 reflow_utterance() トップダウン方式のテスト。"""

    def test_short_text_no_split(self):
        result = reflow_utterance("短いテキスト", chars_per_line=40, max_lines=2)
        assert result == ["短いテキスト"]

    def test_bracket_particle_protection(self):
        """閉じ括弧+助詞はセットで保護される (コーパス P1)。"""
        text = "私たちが普段「アルゴリズムによる最適化」と聞くと、効率的でクリーンな魔法を想像しがちですが、"
        result = reflow_utterance(text, chars_per_line=40, max_lines=2)
        joined = "".join(result)
        assert joined == text
        # 「」と」の間で切れていないこと
        for chunk in result:
            assert not chunk.endswith("」")  # 閉じ括弧が行末に孤立しない
            assert not chunk.startswith("と聞")  # 助詞が行頭に孤立しない

    def test_avoids_short_left_side(self):
        """左側が極端に短い分割を避ける (コーパス P2)。"""
        text = "例えば、一定時間アイテムをスキャンしないと、画面上でタイマーが動き始めます"
        result = reflow_utterance(text, chars_per_line=40, max_lines=2)
        joined = "".join(result)
        assert joined == text
        if len(result) > 1:
            # 最初の行が6幅未満にならない
            assert display_width(result[0]) >= 6

    def test_katakana_word_protection(self):
        """カタカナ語の途中で分割されない。"""
        text = "完璧に計算されたアルゴリズムが生身の人間というノイズだらけの現実に衝突した"
        result = reflow_utterance(text, chars_per_line=40, max_lines=2)
        joined = "".join(result)
        assert joined == text
        # 「アルゴリズム」が分断されていない
        for chunk in result:
            assert "アルゴリズ" not in chunk or "アルゴリズム" in chunk

    def test_digit_protection(self):
        """数字連続の途中で分割されない。"""
        text = "2025年から2026年にかけてのデータを分析しています、多くの発見がありました"
        result = reflow_utterance(text, chars_per_line=40, max_lines=2)
        joined = "".join(result)
        assert joined == text
        for chunk in result:
            # 4桁数字が分断されていない
            assert "202" not in chunk or "2025" in chunk or "2026" in chunk

    def test_bracket_pair_not_split(self):
        """括弧ペアの内部で分割されない。"""
        text = "「配送サービスパートナー（DSP）」プログラムに19億ドルを投資し、大きな変革がありました"
        result = reflow_utterance(text, chars_per_line=40, max_lines=2)
        joined = "".join(result)
        assert joined == text
        # 閉じ括弧が行頭に漏出しない
        for chunk in result[1:]:
            assert not chunk.startswith("」")
            assert not chunk.startswith("）")

    def test_preserves_original_text(self):
        """分割後の再結合が元テキストと一致する。"""
        text = "これはディストピアSF映画のワンシーンではなく、完璧に計算されたアルゴリズムが生身の人間というノイズだらけの現実に衝突した時に、今まさに起きている日常なんです"
        result = reflow_utterance(text, chars_per_line=40, max_lines=3)
        assert "".join(result) == text

    def test_long_音_extension_not_split(self):
        """長音符の前後で分割されない。"""
        text = "インターネットのセキュリティーが重要だと言われています、この問題を深く掘り下げます"
        result = reflow_utterance(text, chars_per_line=40, max_lines=2)
        joined = "".join(result)
        assert joined == text
        for chunk in result:
            assert not chunk.endswith("ー")


class TestReflowSubtitles:
    """B-15 reflow_subtitles() 統合テスト。"""

    def _make_output(self, *texts: str, speaker: str = "れいむ") -> YMM4CsvOutput:
        return YMM4CsvOutput(rows=tuple(YMM4CsvRow(speaker=speaker, text=t) for t in texts))

    def test_short_rows_pass_through(self):
        output = self._make_output("短いテキスト。")
        result = reflow_subtitles(output, chars_per_line=40, max_lines=2)
        assert len(result.rows) == 1
        assert result.rows[0].text == "短いテキスト。"

    def test_multi_sentence_split_and_reflow(self):
        """複数文の発話を句点で分割し、各文を reflow する。"""
        text = (
            "私たちが普段「アルゴリズムによる最適化」と聞くと、効率的でクリーンな魔法を想像しがちですが、"
            "もしその計算式に「人間の身体的限界」という変数が最初から欠落していたらどうなるか。"
            "今回の探求では、その裏側に切り込んでいきます。"
        )
        output = self._make_output(text)
        result = reflow_subtitles(output, chars_per_line=40, max_lines=2)
        # 再結合で元テキスト (\n は B-16 行内改行なので除去して比較)
        joined = "".join(r.text.replace("\n", "") for r in result.rows)
        assert joined == text
        # 複数行に分割される
        assert len(result.rows) >= 2

    def test_speaker_preserved(self):
        output = self._make_output("長い文です。もう一つの文です。", speaker="まりさ")
        result = reflow_subtitles(output, chars_per_line=10, max_lines=2)
        for row in result.rows:
            assert row.speaker == "まりさ"


class TestInsertInlineBreaks:
    """B-16 insert_inline_breaks() のテスト。"""

    def test_short_text_no_break(self):
        from src.pipeline.assemble_csv import insert_inline_breaks
        result = insert_inline_breaks("短いテキスト", chars_per_line=40)
        assert "\n" not in result

    def test_inserts_break_at_comma(self):
        """読点で行内改行が挿入される。"""
        from src.pipeline.assemble_csv import insert_inline_breaks
        text = "人間が管理していれば理解できる体調不良も、アルゴリズムにとっては単なる「エラーコード」でしかありません。"
        result = insert_inline_breaks(text, chars_per_line=40)
        assert "\n" in result
        # 改行を除去すると元テキストに戻る
        assert result.replace("\n", "") == text

    def test_preserves_existing_newline(self):
        """既に改行がある場合はそのまま。"""
        from src.pipeline.assemble_csv import insert_inline_breaks
        text = "1行目\n2行目"
        result = insert_inline_breaks(text, chars_per_line=40)
        assert result == text

    def test_bracket_pair_same_line(self):
        """括弧ペア内で改行されない。"""
        from src.pipeline.assemble_csv import insert_inline_breaks
        text = "倉庫労働者の71.4%がハンドスキャナーによって秒単位で生産性を追跡されていると答えています。"
        result = insert_inline_breaks(text, chars_per_line=40)
        # 改行を除去すると元テキストに戻る
        assert result.replace("\n", "") == text

    def test_no_break_in_kanji_run(self):
        """漢字連続の途中で改行されない。"""
        from src.pipeline.assemble_csv import insert_inline_breaks
        text = "パッケージのサイズの違いや加齢による体力の低下といった「現実空間の摩擦」を一切計算に入れていないんです。"
        result = insert_inline_breaks(text, chars_per_line=40)
        # 改行を除去すると元テキストに戻る
        assert result.replace("\n", "") == text
        # 漢字連続の途中で切れていないことを確認
        for line in result.split("\n"):
            assert not line.endswith("計") or "計算" in line  # 「計/算」にならない


class TestReflowUtteranceV2:
    """B-17 reflow_utterance_v2() のテスト。"""

    def test_short_text_single_page(self):
        result = reflow_utterance_v2("短いテキスト", chars_per_line=40, max_lines=3)
        assert result == ["短いテキスト"]

    def test_hai_problem_resolved(self):
        """「はい。」が独立ページにならない。"""
        text = "はい。そこで慌てて助手席のカバンに手を伸ばして吸入器を取り出そうとします。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=3)
        # 最初のページが「はい。」だけにならない
        first_page_width = display_width(result[0].replace("\n", ""))
        assert first_page_width > 10, f"First page too short: {result[0]}"

    def test_preserves_original_text(self):
        """分割後の再結合が元テキストと一致する。"""
        text = "これはテスト文章です。複数の文を含みます。最後の文です。"
        result = reflow_utterance_v2(text, chars_per_line=20, max_lines=2)
        joined = "".join(p.replace("\n", "") for p in result)
        assert joined == text

    def test_page_balance(self):
        """ページ間の文字数バランスが概ね均等。"""
        text = (
            "はい。そこで慌てて助手席のカバンに手を伸ばして"
            "吸入器を取り出そうとします。"
            "その瞬間、ダッシュボードに設置された"
            "AIカメラがあなたをロックオンして"
            "「脇見運転」としてシステムに"
            "自動でフラグを立てるんです。"
        )
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=3)
        page_widths = [display_width(p.replace("\n", "")) for p in result]
        avg = sum(page_widths) / len(page_widths)
        for w in page_widths:
            assert w >= avg * 0.3, f"Page too short: {w} vs avg {avg}"

    def test_bracket_not_split_across_pages(self):
        """括弧ペア内でページ分割されない。"""
        text = "画面上で「タイム・オフ・タスク（タスク離脱時間）」というタイマーがカチカチと動き始めます。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=3)
        joined = "".join(p.replace("\n", "") for p in result)
        assert joined == text

    def test_line_width_best_effort(self):
        """各行が chars_per_line に近い幅で分割される。"""
        text = "長い文章が続きます、句読点もあります。括弧「テスト」もあります。さらに続きます、最後です。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=3)
        for page in result:
            for line in page.split("\n"):
                # 厳密に40以下を強制はしない (候補位置の制約) が、大幅超過はしない
                assert display_width(line) <= 60, f"Line too wide: {line}"

    def test_multi_page_with_inline_breaks(self):
        """複数ページの各ページ内に行内改行が入る。"""
        text = (
            "私たちが普段「アルゴリズムによる最適化」と聞くと、効率的でクリーンな魔法を想像しがちですが、"
            "もしその計算式に「人間の身体的限界」という変数が最初から欠落していたらどうなるか。"
            "今回の探求では、その見えない労働システムの裏側に鋭く切り込んでいきます。"
        )
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=3)
        joined = "".join(p.replace("\n", "") for p in result)
        assert joined == text
        assert len(result) >= 2

    def test_keeps_quote_tail_phrase_together(self):
        """閉じ括弧の直後に続くひらがな句を途中で切らない。"""
        text = "もしその計算式に「人間の身体的限界」という変数が最初から欠落していたらどうなるか。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        rendered = "|".join(result)
        assert "」\n" not in rendered
        assert "」という" in rendered.replace("|", "").replace("\n", "")
        assert "\nいう" not in rendered

    def test_does_not_split_dewanaku_internally(self):
        """ひらがな連結部の内部で切らず、句全体の後ろで調整する。"""
        text = "これはディストピアSF映画のワンシーンではなく、完璧に計算されたアルゴリズムが生身の人間というノイズだらけの現実に衝突した時に、今まさに起きている日常なんです。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        rendered = "|".join(result)
        assert "では\nなく" not in rendered

    def test_keeps_bracketed_program_name_together(self):
        """括弧を含む名称がページ先頭・行頭に漏れない。"""
        text = "Amazonは「配送サービスパートナー（DSP）」プログラムに19億ドルを投資し、顧客がアプリからドライバーに感謝を伝える制度を打ち出しました。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        rendered = "|".join(result)
        assert "（DSP）" in rendered.replace("|", "").replace("\n", "")
        assert "）\n" not in rendered
        assert "\n」" not in rendered


    def test_keeps_quoted_term_and_explanatory_noun_together(self):
        """逶ｴ蠕後→隱ｬ譏弱す繧育比ｸｭ縺ｮ蜿ｯ蜿門ｾ励ｂ蜷後§陦悟・縺ｫ谺ｩ繧九・"""
        text = "繧ゅ＠縺昴・險育ｮ怜ｼ上↓縲御ｺｺ髢薙・霄ｫ菴鍋噪髯千阜縲阪→縺・≧螟画焚縺梧欠闕ｷ縺九ｉ谺｡縺ｨ縺・↑繧九°縲・"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        rendered = "|".join(result)
        assert "縺・≧\n螟画焚" not in rendered


    def test_keeps_number_and_unit_together(self):
        """謨ｰ蟄・→蜊∵悄蜊ｱ菴咲ｽｮ縺ｮ髫ｱ縺ｧ蛻・ｉ縺ｪ縺・・"""
        text = "Amazon縺ｯ螟ｧ險ｳ縺ｪ譁ｹ邏縺ｧ19蜆医ラ繝ｫ繧呈兜雉・＠縺溘→隱・ｦ九ｌ縺ｦ縺・∪縺吶・"
        result = reflow_utterance_v2(text, chars_per_line=30, max_lines=2)
        rendered = "|".join(result)
        assert "19\n蜆・" not in rendered

    def test_avoids_sparse_line_after_comma_intro(self):
        """読点付きの短い導入句だけで1行を使わない。"""
        text = "例えば、一定時間アイテムをスキャンしないと、画面上で警告が表示されます。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        rendered = "|".join(result)
        assert "例えば、\n" not in rendered

    def test_avoids_sparse_line_after_comma_when_tail_fits(self):
        """後続が収まるなら短い読点行で切らない。"""
        text = "その瞬間、ダッシュボードに設置されたAIカメラがあなたを検知します。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        rendered = "|".join(result)
        assert "その瞬間、\n" not in rendered

    def test_prefers_particle_break_over_sparse_intro_line(self):
        """短い導入句の読点より、後ろの助詞境界を優先する。"""
        text = "それに対し、労働組合側は2025年10月の声明で、"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        rendered = "|".join(result)
        assert "それに対し、\n" not in rendered
        assert "労働組合側は\n2025年" in rendered

    def test_prefers_particle_break_after_quoted_term(self):
        """引用語の後ろの説明名詞より、後続の助詞境界を優先する。"""
        text = "しかも、そこに「猛暑」という環境変数が加わるわけですよね。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        rendered = "|".join(result)
        assert "しかも、そこに\n" not in rendered
        assert "という\n環境変数" not in rendered

    @pytest.mark.xfail(reason="B-17 edge case: 長い引用句含む発話の chars_per_line 超過")
    def test_balances_quoted_program_phrase_without_number_split(self):
        """引用付きプログラム名は数字単位を壊さずに均衡させる。"""
        text = "Amazonは「配送サービスパートナー（DSP）」プログラムに19億ドルを投資し、"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        rendered = "|".join(result)
        lines = rendered.replace("|", "\n").split("\n")
        assert "19\n億" not in rendered
        assert max(display_width(line) for line in lines) <= 40

    @pytest.mark.xfail(reason="B-17 edge case: 長い引用句含む発話の chars_per_line 超過")
    def test_balances_long_quoted_program_name_phrase(self):
        """長い引用付き名称は過度な片寄りを避ける。"""
        text = "顧客がアプリからドライバーに感謝を伝える「サンクマイドライバー」というプログラムを展開しています。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        joined = "\n".join(result)
        lines = joined.split("\n")
        assert "感謝を\n伝える" not in joined
        assert max(display_width(line) for line in lines) <= 40

    @pytest.mark.xfail(reason="B-17 edge case: 長い引用句含む発話の chars_per_line 超過")
    def test_balances_long_quoted_timer_label(self):
        """長い引用ラベルがあっても過剰な1行オーバーを避ける。"""
        text = "画面上で「タイム・オフ・タスク（タスク離脱時間）」というタイマーがカチカチと動き始めます。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        lines = "\n".join(result).split("\n")
        assert max(display_width(line) for line in lines) <= 40

    def test_balances_long_metaphor_quote(self):
        """長い比喩引用は前後で均衡させる。"""
        text = "システムは人間を、物理学の授業でよくある「摩擦のない真空状態」のような存在として前提にしているんですね。"
        result = reflow_utterance_v2(text, chars_per_line=40, max_lines=2)
        lines = "\n".join(result).split("\n")
        assert max(display_width(line) for line in lines) <= 40


class TestReflowSubtitlesV2:
    """B-17 reflow_subtitles_v2() 統合テスト。"""

    def _make_output(self, *texts, speaker="れいむ"):
        return YMM4CsvOutput(rows=tuple(YMM4CsvRow(speaker=speaker, text=t) for t in texts))

    def test_short_rows_pass_through(self):
        output = self._make_output("短いテキスト。")
        result = reflow_subtitles_v2(output, chars_per_line=40, max_lines=3)
        assert len(result.rows) == 1

    def test_speaker_preserved(self):
        output = self._make_output("長い文です。もう一つの文です。", speaker="まりさ")
        result = reflow_subtitles_v2(output, chars_per_line=10, max_lines=2)
        for row in result.rows:
            assert row.speaker == "まりさ"

    def test_multi_row_input(self):
        output = self._make_output(
            "最初の発話です。長い内容が続きます。",
            "二番目の発話。こちらも長い。",
        )
        result = reflow_subtitles_v2(output, chars_per_line=20, max_lines=2)
        assert len(result.rows) >= 2
