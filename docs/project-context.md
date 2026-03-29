# Project Context — NLMYTGen

## PROJECT CONTEXT
- プロジェクト名: NLMYTGen
- 環境: Python / uv / CLI
- ブランチ戦略: main
- 現フェーズ: 成功定義 3/3 達成。次フェーズ選定
- 直近の状態 (2026-03-29): ロバスト性検証完了（2件目 transcript E2E + YMM4 読込成功）。成功定義全達成。IP-01 No-Go。話者ロール推定・speaker-map・BOM・unlabeled 対応済み

---

## ACTIVE ARTIFACT
- Active Artifact: NLM transcript → YMM4 CSV + 編集支援メタデータ → 動画制作効率化
- Artifact Surface: CSV ファイル + sidecar JSON → YMM4 読込 → 編集作業支援
- 現在のスライス: YMM4編集支援メタデータ PoC
- 成功状態: build-csv --emit-meta で sidecar JSON が生成され、発話時間推定・セグメント区切り・表情ヒントが含まれる

---

## CURRENT LANE
- 主レーン: Advance
- 今このレーンを優先する理由: コアパイプライン完成（成功定義3/3）。YMM4編集支援機能で visible value を追加する

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
- Evidence: 2件の transcript で E2E 通過 + YMM4 読込成功（2026-03-29）
- 案件モード: CLI artifact
- 現在の主レーン: Advance
- Authority Return Items: なし（全 blocking 解消）
- 次回最初に確認すべきファイル: src/cli/main.py / tests/
- 未確定の設計論点: なし
- Expansion Risk: なし
