# Runtime State — NLMYTGen
# BLOCK SUMMARY のたびに更新する。
# compact 後の再アンカリングではこのファイルを読む。

## 現在位置
- project: NLMYTGen
- lane: Audit
- slice: docs-only resume packet 整備 + handoff 固定
- next_action: docs packet を起点に quarantined/hold 項目を workflow pain ベースで個別再審査し、approved next frontier を確定する
- 案件モード: CLI artifact

## 主成果物
- active_artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー
- artifact_surface: CLI → CSV → YMM4 台本読込 → 演出設定 → レンダリング → サムネイル → 投稿
- last_change_relation: cleanup (docs-only で再開できる状態への整備)

## カウンター
- blocks_since_user_visible_change: 0
- blocks_since_manual_evidence: 0
- blocks_since_visual_audit: 0

## 量的指標
- test_file_count: 5
- mock_file_count: 0
- impl_file_count: 8
- mock_impl_ratio: 0.00
- open_todo_count: 0

## 最終検証
- last_verification_artifact: `python3 -m src.cli.main --help` OK、`build-csv ... --display-width --dry-run --stats` 実データ確認 OK。`pytest` / `uv` は現シェルに未導入で再実行不能
- last_verification_date: 2026-03-30

## Evidence（CLI artifact mode）
- evidence_status: 実データ通過（2件の transcript で CSV E2E 確認済み）
- last_e2e_data: AI監視(51行) + Panopticon(87行) — CSV 生成確認
- external_tool_verification: YMM4 読込成功（2026-03-29、CSV形式）
- final_artifact_reached: Yes（CSV → YMM4 台本読込のパス）
- blocking_dependency: なし

## FEATURE_REGISTRY 状態サマリ (2026-03-30)

- done: 11件（A-01〜A-02, B-01〜B-09）
- info: 2件（C-01, C-06）
- hold: 3件（A-03, E-01, E-02）
- quarantined: 4件（A-04, D-02, F-01, F-02）
- rejected: 7件（B-10, C-02, C-03, C-04, C-05, D-01, F-03）

## Python のスコープ制約（2026-03-30 確定）
Python の責務はテキスト変換のみ（CSV + テキストメタデータ）。
以下は全て禁止（rejected として記録済み）:
- 画像生成・画像合成（PIL/Pillow 含む）
- .ymmp 生成・操作（音声ファイル参照を含むため外部生成不可能）
- YMM4 テンプレート生成・演出指定
- YMM4 出力の模倣・プレビュー
- 動画レンダリング・音声合成

## 外部メディア取得の方針（2026-03-30）
- 取得機能（acquisition）と受け取り機能（receiving）は分離する
- 最終的に自動化したい（ユーザー指示）
- A-04（RSS）と D-02（背景動画取得）は quarantined。境界と価値経路の個別再審査が済むまで進めない

## Authority Return Items

- S-6 トピック分析の LLM アダプター方式: まだ approved next frontier ではない。進めるなら value path 再確認、プロバイダー選定、SDK/stdlib 境界の ADR が必要
- 「stdlib のみ」制約の緩和: LLM SDK 追加には ADR が必要
- E-02 (YouTube メタデータ生成): hold。単体では価値が薄く、E-01 または別 integration point とセットで再検討
- quarantined 項目 (A-04, D-02, F-01, F-02): 通常候補に戻す前に個別再審査が必要
- GUI 技術選定は F-01/F-02 の価値証明後に行う

## 既知の問題

- 直前 handoff は 53f3718 時点の内容で止まっており、後続 commit `8a1c710` で追加された canonical docs とその未充足状態は含んでいなかった
- E-02 は YouTube Studio への手入力をテキストファイル生成に置き換えるだけで、実質的な効率化にならない (E-01 とセットでないと価値が出ない)
- A-04 / D-02 / F-01 / F-02 は前セッションの汚染バッチ由来で、個別精査前に normal backlog として扱えない
- `pytest` / `uv` が現シェルで利用できず、前回の 31 PASS をこの場で再現できていない
- `prompt-resume.md` は作成済みだが、内容の正本は引き続き repo docs 側である

## 一時補助物（作ったら登録。統合/削除したら除去）
| ファイル/モジュール | 種別 | 削除条件 | 寿命 |
|---|---|---|---|
| (なし) | | | |
