# ADR-0002: NotebookLM Is Upstream

## Status
Accepted

## Context
旧プロジェクトは "NLM" (NotebookLM) を名前に冠していたが、NotebookLM の API が利用不可だったため、
Gemini がプロンプト駆動で台本を「生成」する設計に暗黙移行した。
この移行は DECISION LOG に記録されず、2026-03-19 まで検出されなかった。

## Decision
NotebookLM は upstream source であり、内部 LLM はその代替をしない。

- 台本品質は NotebookLM が生成する
- Python は NotebookLM の出力を構造化・整形・検証する
- 内部 LLM (Gemini 等) を使う場合、責務は構造化補助に限定する
- 内部 LLM が主台本を創作する機能は実装しない

## Consequences
- NotebookLM の手動操作 (ソース投入 → Audio Overview → テキスト化) がワークフローの前提
- パイプラインの入力は NotebookLM 由来のテキストファイル
- LLM 統合を追加する場合は、「構造化補助」の範囲内であることを確認してから実装する
- NotebookLM API が利用可能になった場合は、自動化を検討する (別 ADR)
