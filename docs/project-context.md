# Project Context — NLMYTGen

## PROJECT CONTEXT
- プロジェクト名: NLMYTGen
- 環境: Python / uv / CLI
- ブランチ戦略: master
- 現フェーズ: コアパイプライン完成。機能管理基盤整備済み。次機能の選定待ち
- 直近の状態 (2026-03-30):
  - docs/FEATURE_REGISTRY.md 新設 — 全26機能の一覧台帳（done 11 / proposed 10 / hold 2 / unauthorized 1）
  - docs/AUTOMATION_BOUNDARY.md 新設 — YMM4内部/外部の自動化境界を L1〜L4+GUI で定義
  - B-10 (--emit-meta) を unauthorized としてマーク。未承認で混入した機能
  - WORKFLOW.md に S-6 サムネイル / S-7 YouTube投稿を追加、自動化レベルを明示
  - transcript 要求ループの原因（docs 不整合）を修正済み

---

## ACTIVE ARTIFACT
- Active Artifact: 動画制作ワークフロー全体の効率化（FEATURE_REGISTRY 管理下）
- Artifact Surface: CLI → CSV → YMM4 → 動画
- 現在のスライス: FEATURE_REGISTRY レビュー → 次の approved 機能の実装
- 成功状態: FEATURE_REGISTRY の proposed 機能がユーザー承認され、実装が開始される

---

## CURRENT LANE
- 主レーン: Advance
- 今このレーンを優先する理由: 機能管理基盤が整った。次はユーザーが優先順位を決め、承認された機能から実装する

---

## DECISION LOG

| 日付 | 決定事項 | 選択肢 | 決定理由 |
|------|----------|--------|----------|
| 2025 | CLI パイプラインとして構築 | CLI / Web UI / Electron | 最小構成で検証可能 |
| 2025 | IP-01 No-Go | Go / No-Go | 要件未充足 |
| 2025 | Web UI / API / YouTube 連携は後回し | 優先 / 後回し | ロバスト性検証が先 |
| 2026-03-29 | YMM4編集支援メタデータをサイドカーJSONで実装 | CSV拡張列 / サイドカーJSON / YMM4プロジェクト直接生成 | CSV互換性を壊さない（ただし未承認で混入。レビュー待ち） |
| 2026-03-30 | FEATURE_REGISTRY + AUTOMATION_BOUNDARY で機能管理 | 台帳管理 / ad-hoc | 未承認機能混入の再発防止。開発方向のぼやけを解消 |
| 2026-03-30 | 自動化レイヤーを L1〜L4+GUI の5層で定義 | 5層 / 3層 / フラット | YMM4内部/外部の境界を明確化するため |

---

## IDEA POOL

FEATURE_REGISTRY.md に統合済み。機能候補は FEATURE_REGISTRY で管理する。

| ID | 旧アイデア | 移行先 |
|----|----------|--------|
| IP-02 | Web UI 化 | CLAUDE.md スコープ外 |
| IP-03 | YouTube 自動アップロード | FEATURE_REGISTRY E-01 (hold) |

---

## HANDOFF SNAPSHOT
- Active Artifact: 動画制作ワークフロー全体の効率化（FEATURE_REGISTRY 管理下）
- Artifact Surface: CLI → CSV → YMM4 → 動画
- Last Change Relation: direct (docs 基盤整備)
- Evidence: 全28テスト PASS、実データ E2E 2件通過
- 案件モード: CLI artifact
- 現在の主レーン: Advance
- Authority Return Items:
  - B-10 (--emit-meta) の承認/削除/修正判断
  - proposed 10件の優先順位付け
  - GUI 技術選定（F-01 分割プレビュー）
  - YMM4 .ymmp 調査の可否（C-03）
- 次回最初に確認すべきファイル: docs/FEATURE_REGISTRY.md
- 未確定の設計論点: GUI 技術選定、YMM4 .ymmp フォーマット対応の可否
- Expansion Risk: なし
