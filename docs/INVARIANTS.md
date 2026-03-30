# Invariants
# 破ってはいけない条件・責務境界・UX不変量を保持する正本。

## Systemic Diagnosis
- この repo の失敗は「未承認実装」そのものより、status 語彙の崩れと value path 不在が静かに混入することにある。
- 「テンプレートを作る」「GUI を作る」といった命題先行は、実ワークフローの bottleneck を見失わせやすい。

## UX / Algorithmic Invariants
- NotebookLM が主台本品質の源泉であり、Python/LLM は主台本を生成しない。
- `build-csv` の既定動作は後方互換を保つ。表示幅ベース分割は opt-in で有効化する。
- 優先度と status は分離する。項目を「先に見る」ことは implementation approval を意味しない。
- canonical rules が repo 内にある場合は、`docs/ai/*.md` を tool-specific helper docs や prompt より先に読む。

## Responsibility Boundaries
- Python の責務はテキスト変換のみ。CSV とテキストメタデータ文字列までに限定する。
- 音声合成・字幕配置・演出指定・レンダリング・サムネイル最終判断は YMM4 または人間の責務。
- `.ymmp` を直接編集しても音声合成は成立しない。音声合成は YMM4 の台本読込経由でのみ行う。
- GUI/API/SDK 追加は、value path と境界違反の有無を確認し、必要なら ADR を通してから扱う。

## Prohibited Interpretations / Shortcuts
- rejected を「その工程は不要」と解釈しない。代替の手動導線は WORKFLOW に残す。
- 汚染バッチ由来の候補を、未再審査のまま normal backlog として扱わない。
- `approved` を「有望そう」「今はこれが一番まし」といった意味で使わない。
- ユーザー未指定の固有名詞、音声エンジン、GUI 技術、素材サイト、API 互換先を勝手に採用しない。
- サムネイルの重要性を軽視して、Python 生成や定型化で代替しようとしない。

## 運用ルール
- ユーザーが一度説明した非交渉条件は、同一ブロック内でここへ固定する。
- `project-context.md` の DECISION LOG には理由を短く残し、ここには条件そのものを残す。
