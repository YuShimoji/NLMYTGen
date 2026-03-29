# Runtime State — NLMYTGen
# BLOCK SUMMARY のたびに更新する。
# compact 後の再アンカリングではこのファイルを読む。

## 現在位置
- project: NLMYTGen
- lane: Advance
- slice: FEATURE_REGISTRY レビュー → 次の approved 機能の実装
- next_action: ユーザーが FEATURE_REGISTRY の proposed 10件を優先順位付け → approved 機能から実装開始
- 案件モード: CLI artifact

## 主成果物
- active_artifact: 動画制作ワークフロー全体の効率化（FEATURE_REGISTRY 管理下）
- artifact_surface: CLI → CSV → YMM4 → 動画
- last_change_relation: direct (docs 基盤整備 + FEATURE_REGISTRY/AUTOMATION_BOUNDARY 新設)

## カウンター
- blocks_since_user_visible_change: 0
- blocks_since_manual_evidence: 0
- blocks_since_visual_audit: 0

## 量的指標
- test_file_count: 5
- mock_file_count: 0
- impl_file_count: 9
- mock_impl_ratio: 0.00
- open_todo_count: 0

## 最終検証
- last_verification_artifact: 全28テスト PASS + 実データ E2E 2件
- last_verification_date: 2026-03-29

## Evidence（CLI artifact mode）
- evidence_status: 実データ通過（2件の transcript で E2E 確認）
- last_e2e_data: AI監視(51行) + Panopticon(87行)
- external_tool_verification: YMM4 読込成功（2026-03-29、CSV形式は変更なし）
- final_artifact_reached: Yes
- blocking_dependency: なし

## Authority Return Items
- B-10 (--emit-meta) の承認/削除/修正判断: unauthorized として FEATURE_REGISTRY に登録済み
- proposed 10件の優先順位付け
- GUI 技術選定（F-01 分割プレビュー）
- YMM4 .ymmp フォーマット調査の可否（C-03）

## 一時補助物（作ったら登録。統合/削除したら除去）
| ファイル/モジュール | 種別 | 削除条件 | 寿命 |
|---|---|---|---|
| src/pipeline/edit_hints.py | unauthorized 機能 | B-10 が rejected なら削除 | レビュー待ち |
| tests/test_edit_hints.py | unauthorized 機能のテスト | B-10 が rejected なら削除 | レビュー待ち |
