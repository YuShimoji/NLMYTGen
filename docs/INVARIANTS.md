# Invariants
# 破ってはいけない条件・責務境界・UX不変量を保持する正本。

## Systemic Diagnosis
- この repo の失敗は「未承認実装」そのものより、status 語彙の崩れと value path 不在が静かに混入することにある。
- 「テンプレートを作る」「GUI を作る」といった命題先行は、実ワークフローの bottleneck を見失わせやすい。

## UX / Algorithmic Invariants
- NotebookLM が主台本品質の源泉であり、Python/LLM は主台本を生成しない。
- ただし、NotebookLM 由来の既存台本を前提にした constrained rewrite（2本の台本の接続、聞き手/解説役の整合性調整、再編集指示の自動化）は検討対象に含めてよい。ゼロからの主台本生成とは区別する。
- `build-csv` の既定動作は後方互換を保つ。表示幅ベース分割は opt-in で有効化する。
- 優先度と status は分離する。項目を「先に見る」ことは implementation approval を意味しない。
- canonical rules が repo 内にある場合は、`docs/ai/*.md` を tool-specific helper docs や prompt より先に読む。

## Responsibility Boundaries
- Python の責務はテキスト変換のみ。CSV とテキストメタデータ文字列までに限定する。
- 音声合成・字幕配置・演出指定・レンダリング・サムネイル最終判断は YMM4 または人間の責務。
- `.ymmp` を直接編集しても音声合成は成立しない。音声合成は YMM4 の台本読込経由でのみ行う。
- YMM4 / `.ymmp` の直接編集や画面効果の自動注入は高リスクなため、LLM や Automation を使う場合も、まずはテキスト補助・コピペ用メモ・プリセット候補提示に留める。direct edit は workflow proof なしに採用しない。
- GUI/API/SDK 追加は、value path と境界違反の有無を確認し、必要なら ADR を通してから扱う。
- YMM4 自動化の主経路は「演出 IR 定義 → テンプレート資産蓄積 → 接続方式判断」の段階的アプローチ。特定の外部ツールを主軸にしない。
- 新しい自動化経路を提案する際は、現行ロードマップ (YMM4-AUTOMATION-RESEARCH.md セクション4) の段階構成との整合を示すこと。根拠なしに経路を増やさない。
- YMovieHelper は参照実装 (設計思想の観察対象)。「YMovieHelper を使う」「YMovieHelper に接続する」とは書かない。

## Prohibited Interpretations / Shortcuts
- rejected を「その工程は不要」と解釈しない。代替の手動導線は WORKFLOW に残す。
- 汚染バッチ由来の候補を、未再審査のまま normal backlog として扱わない。
- `approved` を「有望そう」「今はこれが一番まし」といった意味で使わない。
- ユーザー未指定の固有名詞、音声エンジン、GUI 技術、素材サイト、API 互換先を勝手に採用しない。
- サムネイルの重要性を軽視して、Python 生成や定型化で代替しようとしない。
- テンプレート素材の「完全自動生成」に踏み込まない。NLMYTGen の責務は提案と仮組立まで。素材の作成・収集は人間の責務。
- YMM4 プラグイン開発 (G-01/G-03) に時間を使う前に、YMovieHelper 連携 (G-02/G-05) の評価を完了すること。見通しのない .NET 環境構築を先行しない。
- ymmp 直接編集は控える。完成品の解析からの再現可能性の研究までが許容範囲。編集によるデッドファイル蓄積を避ける。
- テストスイートの拡張を目的化しない。テストは実装の検証手段であり、テスト設計が開発の主活動にならないこと。
- proof は出力レビューで完了とする。実動画制作や定量計測 (N% 以上が一致等) を proof 要件にしない。
- 研究 (ymmp 解析等) と開発 (build-ymh 等) を混同しない。研究に2ブロック以上費やす場合は一度止まって開発に戻る。

## 運用ルール
- ユーザーが一度説明した非交渉条件は、同一ブロック内でここへ固定する。
- `project-context.md` の DECISION LOG には理由を短く残し、ここには条件そのものを残す。
