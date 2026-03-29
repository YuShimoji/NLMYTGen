# Project Context — NLMYTGen

## PROJECT CONTEXT
- プロジェクト名: NLMYTGen
- 環境: Python / uv / CLI
- ブランチ戦略: main
- 現フェーズ: Phase 0〜4 完了。ロバスト性検証フェーズ
- 直近の状態: IP-01 No-Go 判定。話者ロール推定追加。validate_handoff / normalize 改善。speaker-map-file / BOM / ヘッダースキップ対応。uv 導入で pytest 実行可能化

---

## ACTIVE ARTIFACT
- Active Artifact: NLM transcript → YMM4 CSV → 動画1本完成への経路
- Artifact Surface: CSV ファイル → YMM4 読込 → レンダリング結果
- 現在のスライス: ロバスト性検証（別 NLM transcript で通す）
- 成功状態: 別の NLM transcript で build-csv → CSV 生成 → YMM4 読込成功

---

## CURRENT LANE
- 主レーン: Advance
- 今このレーンを優先する理由: 実成果物到達（E2E）がまだ1パターンのみ

---

## DECISION LOG

| 日付 | 決定事項 | 選択肢 | 決定理由 |
|------|----------|--------|----------|
| 2025 | CLI パイプラインとして構築 | CLI / Web UI / Electron | 最小構成で検証可能 |
| 2025 | IP-01 No-Go | Go / No-Go | 要件未充足 |
| 2025 | Web UI / API / YouTube 連携は後回し | 優先 / 後回し | ロバスト性検証が先 |

---

## IDEA POOL

| ID | アイデア | 状態 | 関連領域 | 再訪トリガー |
|----|----------|------|----------|--------------|
| IP-02 | Web UI 化 | hold | Unlock | ロバスト性検証完了後 |
| IP-03 | YouTube 自動アップロード | hold | Unlock | 動画制作パイプライン確立後 |

---

## HANDOFF SNAPSHOT
- Active Artifact: NLM transcript → YMM4 CSV → 動画1本完成への経路
- Artifact Surface: CSV / YMM4 読込 / レンダリング
- Last Change Relation: direct
- Evidence: sample transcript で Phase 0〜4 通過。別 transcript / YMM4 実読込は未検証
- 案件モード: CLI artifact
- 現在の主レーン: Advance
- Authority Return Items: 別 NLM transcript 提供（ユーザー操作）/ YMM4 読込確認（ユーザー操作）
- 次回最初に確認すべきファイル: src/cli/main.py / tests/
- 未確定の設計論点: なし
- Expansion Risk: なし
