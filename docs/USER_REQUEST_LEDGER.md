# User Request Ledger
# ユーザーの継続要望・差分要求・backlog を保持する台帳。

## 現在有効な要求
- かなり先送りになった機能、実際には未完了なのに完了扱いになっている task、文書だけ存在して実体が弱い項目を包括的に是正する。
- ハンドオフに全コンテキストが本当に残っているか検証し、抜け漏れは明示して報告する。
- 痛点ドリブンで進める。FEATURE_REGISTRY の候補一覧から機械的に次タスクを選ばない。
- `docs/ai/*.md` が存在するなら、tool-specific helper docs より先に canonical rules として扱う。
- project-local canonical docs を先に読んで、既知文脈の再質問を避ける。

## 未反映の是正要求
- `approved` は「仕様定義済み + ユーザー承認済み」のみ。priority と status を混同しない。
- E-02 のような「テンプレート作成」という命題に引っ張られず、実際にどこへ入力され何が減るのかから価値検証する。
- NotebookLM / YMM4 / YouTube Studio の実 integration point を曖昧にしたまま仕様を進めない。

## Backlog Delta
- S-5 字幕はみ出しは、YMM4 手作業だけでなく S-3 出力品質改善でも削減する。
- S-6 トピック分析は、stdlib 内のパターンマッチではなく LLM アダプター方式を検討する。ただし approval と SDK 境界整理が前提。
- 汚染バッチ由来の D-02 / F-01 / F-02 は、個別再審査まで通常 backlog に戻さない。

## 今後明文化すべきこと
- LLM アダプター方式を本当に次 frontier にするかどうかの approval 条件
- 素材取得系 (D-02 中心) の権利・取得元・受け取り境界
- GUI 候補 (F-01 / F-02) が workflow bottleneck を本当に減らすかの workflow proof

## 運用ルール
- 会話で一度出た要求のうち、次回以降も効くものをここへ残す。
- 単なる感想ではなく、仕様・設計・backlog に効くものを優先する。
