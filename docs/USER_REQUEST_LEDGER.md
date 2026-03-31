# User Request Ledger
# ユーザーの継続要望・差分要求・backlog を保持する台帳。

## 現在有効な要求
- かなり先送りになった機能、実際には未完了なのに完了扱いになっている task、文書だけ存在して実体が弱い項目を包括的に是正する。
- ハンドオフに全コンテキストが本当に残っているか検証し、抜け漏れは明示して報告する。
- 痛点ドリブンで進める。FEATURE_REGISTRY の候補一覧から機械的に次タスクを選ばない。
- `docs/ai/*.md` が存在するなら、tool-specific helper docs より先に canonical rules として扱う。
- project-local canonical docs を先に読んで、既知文脈の再質問を避ける。
- 次 frontier は S-5 workflow proof を先に進める。字幕はみ出し pain を、YMM4 自動化ではなく workflow proof と Python 側の事前警告改善で詰める。
- LLM は主台本のゼロ生成には使わない。一方で、NotebookLM 由来の既存台本どうしの接続、聞き手/解説役の整合性調整、再編集指示の自動化は将来候補として調査対象に含める。
- GPT の Automation 機能など、repo 外の補助自動化は value path があり廉価化に効くなら許容する。ただし YMM4 / `.ymmp` の直接編集は原則避け、まずはテキスト補助やプリセット再利用を優先する。

## 未反映の是正要求
- `approved` は「仕様定義済み + ユーザー承認済み」のみ。priority と status を混同しない。
- E-02 のような「テンプレート作成」という命題に引っ張られず、実際にどこへ入力され何が減るのかから価値検証する。
- NotebookLM / YMM4 / YouTube Studio の実 integration point を曖昧にしたまま仕様を進めない。

## Backlog Delta
- S-5 字幕はみ出しは、YMM4 手作業だけでなく S-3 出力品質改善でも削減する。
- S-6 トピック分析は、stdlib 内のパターンマッチではなく LLM アダプター方式を検討する。ただし approval と SDK 境界整理が前提。
- 汚染バッチ由来の D-02 / F-01 / F-02 は、個別再審査まで通常 backlog に戻さない。
- 字幕改行の境界ケース (`「」`, 引用符, 括弧, 数値+記号, 連続カタカナ, 漢字かな境界, 早め折り返しが有利なケース) は、次の heuristic 即実装候補ではなく corpus / 評価観点として先に蓄積する。
- B-15 Phase 1 は value あり。次改善は SE を必須項目のように扱わないことと、背景候補を絞り込みやすい cue contract への圧縮を優先する。
- 素材取得・図作成・フリー素材探索は、cue memo とは別の bottleneck として扱う。B-15 の成果を過大評価してそこまで解決したことにしない。
- 次に候補化するなら、自動取得より先に「asset / diagram brief」のような text-only 補助を優先して比較する。
- `diagram brief` は B-16 として approved に進み、初手実装済み。次の判断は workflow proof を取るかどうか。
- B-16 rerun で絞り込みが改善したため、次候補は `asset brief` を本命に、`search query brief` を対抗に比較する段階へ進んだ。2 件同時 proposal にはしない。

## 今後明文化すべきこと
- B-15 Phase 1 の収束条件と、次に切り出す narrow feature の problem statement
- 素材取得系 (D-02 中心) の権利・取得元・受け取り境界
- GUI 候補 (F-01 / F-02) が workflow bottleneck を本当に減らすかの workflow proof

## 運用ルール
- 会話で一度出た要求のうち、次回以降も効くものをここへ残す。
- 単なる感想ではなく、仕様・設計・backlog に効くものを優先する。
