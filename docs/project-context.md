# Project Context — NLMYTGen

## PROJECT CONTEXT
- プロジェクト名: NLMYTGen
- 環境: Python / uv / CLI
- ブランチ戦略: master
- 現フェーズ: コアパイプライン完成。スコープ整理完了。次機能の選定・承認待ち
- 直近の状態 (2026-03-30):
  - Python のスコープを「テキスト変換のみ」に確定。画像合成・.ymmp生成・演出指定は全て rejected
  - FEATURE_REGISTRY: done 11 / proposed 5 / hold 2 / rejected 8
  - B-10 (--emit-meta): コード除去済み。docs からも stale 記述を除去
  - E-02 (YouTube メタデータ生成): 仕様未定義のまま提案されていた。入力・出力・テンプレート管理の設計が必要
  - 外部メディア取得（A-04/D-02）: 取得と受け取りを分離すれば OK。最終的に自動化する方針

---

## ACTIVE ARTIFACT
- Active Artifact: NLM transcript → YMM4 CSV → 動画制作ワークフロー効率化
- Artifact Surface: CLI → CSV → YMM4 台本読込 → 動画
- 現在のスライス: proposed 5件の優先順位付け → approved → 実装
- 成功状態: ユーザーが承認した機能が実装され、ワークフローの摩擦が減る

---

## CURRENT LANE
- 主レーン: Advance
- 今このレーンを優先する理由: コアパイプラインは完成・E2E 検証済み。次の前進はワークフロー効率化機能の追加

---

## DECISION LOG

| 日付 | 決定事項 | 選択肢 | 決定理由 |
|------|----------|--------|----------|
| 2025 | CLI パイプラインとして構築 | CLI / Web UI / Electron | 最小構成で検証可能 |
| 2025 | IP-01 No-Go | Go / No-Go | 要件未充足 |
| 2025 | Web UI / API / YouTube 連携は後回し | 優先 / 後回し | ロバスト性検証が先 |
| 2026-03-29 | B-10 (--emit-meta) を未承認で混入 | — | 未承認。後に rejected → コード除去 |
| 2026-03-30 | FEATURE_REGISTRY + AUTOMATION_BOUNDARY で機能管理 | 台帳管理 / ad-hoc | 未承認機能混入の再発防止 |
| 2026-03-30 | 自動化レイヤーを L1〜L4+GUI の5層で定義 | 5層 / 3層 / フラット | YMM4内部/外部の境界を明確化 |
| 2026-03-30 | Python での生成・レンダリングを全面禁止 | 全面禁止 / 部分許容 | .ymmp は音声ファイル参照を含み外部生成不可能。この教訓を拡大適用。Python の責務はテキスト変換（CSV / テキストメタデータ文字列）のみに限定。rejected: B-10, C-02, C-03, C-04, C-05, D-01, F-03 |
| 2026-03-30 | 外部メディア取得は分離設計で OK | L1拡張許容 / L2専念 | 取得機能と受け取り機能を分離すれば NLMYTGen に含めてよい。最終的に自動化する方針 |

---

## Python のスコープ（確定事項 — 2026-03-30）

**許可:**
- テキストファイルの変換（transcript → CSV）
- テキストメタデータの生成（タイトル・説明・タグ等の文字列）
- 入力テキストの検証・分析
- 外部ソースからのテキスト/メディア取得（L1、取得と受け取りを分離する設計で）

**禁止:**
- 画像生成・画像合成（PIL/Pillow 含む）
- .ymmp 生成・操作（音声ファイル参照を含むため外部生成不可能）
- YMM4 テンプレート生成・演出指定（YMM4 内部の責務）
- YMM4 出力の模倣・プレビュー
- 動画レンダリング・音声合成
- 外部 TTS（Voicevox 等）

**根拠:**
YMM4 の .ymmp プロジェクトファイルは音声ファイル（WAV 等）への参照を含む。その音声は YMM4 が台本 CSV を読み込む際に内蔵 TTS で自動合成するもの。NLMYTGen から音声ファイルを生成できないため、完全な .ymmp を外部から作ることは原理的に不可能。この制約から、YMM4 内部の操作（テンプレート・演出・素材配置）を Python から制御するアプローチ全般が成り立たない。

---

## IDEA POOL

FEATURE_REGISTRY.md に統合済み。機能候補は FEATURE_REGISTRY で管理する。

| ID | 旧アイデア | 移行先 |
|----|----------|--------|
| IP-02 | Web UI 化 | CLAUDE.md スコープ外 |
| IP-03 | YouTube 自動アップロード | FEATURE_REGISTRY E-01 (hold) |

---

## HANDOFF SNAPSHOT
- Active Artifact: NLM transcript → YMM4 CSV → 動画制作ワークフロー効率化
- Artifact Surface: CLI → CSV → YMM4 台本読込 → 動画
- Last Change Relation: cleanup (スコープ整理 — rejected 7件 + docs stale 除去)
- Evidence: 全16テスト PASS、実データ E2E 2件通過、YMM4 読込成功(2026-03-29)
- 案件モード: CLI artifact
- 現在の主レーン: Advance
- Authority Return Items:
  - proposed 5件の優先順位付け（A-04, D-02, E-02, F-01, F-02）
  - GUI 技術選定（F-01/F-02）
  - E-02 の仕様定義（入力/出力/テンプレート管理が未定義）
- 解決済み:
  - B-10 (--emit-meta): rejected → コード除去済み → docs stale 記述除去済み
  - C-02/C-03/C-04/C-05/D-01/F-03: rejected — Python での生成・レンダリング全面禁止
- 既知の問題:
  - E-02 は仕様が未定義（入力・出力・テンプレート管理・実際の価値が未検証）
  - proposed 5件は全て前セッション（B-10 混入時）に一括生成された提案
- 次回最初に確認すべきファイル: docs/FEATURE_REGISTRY.md, docs/runtime-state.md
- 未確定の設計論点: GUI 技術選定、E-02 の仕様
- Expansion Risk: なし
