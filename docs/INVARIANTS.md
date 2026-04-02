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
- 演出 IR (PRODUCTION_IR_SPEC.md) が視覚配置の中心課題。C-07 系 (演出判断支援) が主系統であり、D-02 (素材取得) は従属的補助論点。D-02 を主軸として扱わない。
- 再開時に「CSV 変換専用ツール」という旧理解に引き戻されないよう、README / CLAUDE.md / WORKFLOW / AUTOMATION_BOUNDARY は演出 IR の役割を反映した状態を維持する。
- patch-ymmp (G-06) は成熟段階モデルで評価する。「研究か実用か」の二択で早期に裁定しない。.ymmp のゼロからの生成 (不可能) と、台本読込後の限定的な後段適用 (patch-ymmp) は明確に区別する。成熟段階: Level 0 構造把握 / Level 1 限定変換器 (face+bg) / Level 2 演出IR適用エンジン / Level 3a face+bg 限定 E2E / Level 3b slot+motion 含む拡張 E2E / Level 4 制作標準装備。現在は Level 1 到達済み、Level 2 形成中。
- IR 語彙に定義済みだが ymmp 適用が未実装のフィールド (motion/transition/overlay/slot/bg_anim) は「境界外」ではなく「正式スコープ内の未実装 frontier」。「未実装」と「境界外」を混同しない。

## Prohibited Interpretations / Shortcuts
- rejected を「その工程は不要」と解釈しない。代替の手動導線は WORKFLOW に残す。
- 汚染バッチ由来の候補を、未再審査のまま normal backlog として扱わない。
- `approved` を「有望そう」「今はこれが一番まし」といった意味で使わない。
- ユーザー未指定の固有名詞、音声エンジン、GUI 技術、素材サイト、API 互換先を勝手に採用しない。
- サムネイルの重要性を軽視して、Python 生成や定型化で代替しようとしない。
- テンプレート素材の「完全自動生成」に踏み込まない。NLMYTGen の責務は提案と仮組立まで。素材の作成・収集は人間の責務。
- YMM4 プラグイン開発 (G-01/G-03) に時間を使う前に、演出 IR 定義 (G-02 done) + IR 出力プロンプト (G-05) を進めること。見通しのない .NET 環境構築を先行しない。
- ymmp のゼロからの生成は禁止。台本読込後の限定的な後段適用 (patch-ymmp による face/bg 差し替え) は Level 1 変換器として許容済み。ただし適用範囲の拡張は成熟段階を上げる判断として扱い、無制限な ymmp 編集には進まない。デッドファイル蓄積を避ける。
- テストスイートの拡張を目的化しない。テストは実装の検証手段であり、テスト設計が開発の主活動にならないこと。
- proof は出力レビューで完了とする。実動画制作や定量計測 (N% 以上が一致等) を proof 要件にしない。
- 研究 (ymmp 解析等) と開発 (build-ymh 等) を混同しない。研究に2ブロック以上費やす場合は一度止まって開発に戻る。

## 運用ルール
- ユーザーが一度説明した非交渉条件は、同一ブロック内でここへ固定する。
- `project-context.md` の DECISION LOG には理由を短く残し、ここには条件そのものを残す。
