# Runtime State — NLMYTGen
# BLOCK SUMMARY のたびに更新する。
# compact 後の再アンカリングではこのファイルを読む。

## 現在位置
- project: NLMYTGen
- lane: Advance (演出パイプライン E2E)
- slice: G-05 v4 proof 完了 + Multi-Object IR 読み込み対応 + patch-ymmp 接続テスト完了 (2026-04-03)
- next_action: (1) 実制作 ymmp (samples/v4_re.ymmp, 8.5MB, 台本読込済み) で extract-template → face_map/bg_map 生成 → patch-ymmp E2E → (2) Level 3 到達判定
- 案件モード: CLI artifact

## 主成果物
- active_artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー
- artifact_surface: CLI → CSV → YMM4 台本読込 → 演出設定 → レンダリング → サムネイル → 投稿
- last_change_relation: direct (load_ir Multi-Object 対応実装。G-05 v4 proof + CLI 接続テスト完了)

## カウンター
- blocks_since_user_visible_change: 0
- blocks_since_manual_evidence: 0
- blocks_since_visual_audit: 0

## 量的指標
- test_file_count: 9
- test_count: 93
- mock_file_count: 0
- impl_file_count: 15
- mock_impl_ratio: 0.00
- open_todo_count: 0

## 最終検証
- last_verification_artifact: load_ir Multi-Object 対応 + G-05 v4 proof + CLI patch-ymmp dry-run 成功。93 PASS
- last_verification_date: 2026-04-03

## Evidence（CLI artifact mode）
- evidence_status: Custom GPT v4 proof 完了 (28 utterances, 全チェック PASS)。patch-ymmp CLI dry-run 成功 (Multi-Object IR 対応)。台本読込後の実制作 ymmp (v4_re.ymmp, 8.5MB) がローカルに存在
- last_e2e_data: AI監視(57発話) の CSV + Custom GPT v4 IR (28 utterances) + patch-ymmp dry-run
- external_tool_verification: YMM4 読込成功（2026-03-29、CSV形式）。YMM4 テンプレート (ItemSettings.json) 構造確定 (2026-04-03)。台本読込後 ymmp 保存済み (2026-04-03)
- final_artifact_reached: Yes（CSV → YMM4 台本読込のパス）
- blocking_dependency: 実制作 ymmp での face/bg 差し替え E2E (extract-template → patch-ymmp → YMM4 確認)

## FEATURE_REGISTRY 状態サマリ (2026-04-01)

- done: 25件（A-01〜A-02, A-04, B-01〜B-17, C-07 v3→v4, C-08, G-02, G-02b, G-05, G-06）
- approved: 0件
- proposed: 0件
- info: 2件（C-01, C-06）
- hold: 4件（A-03, D-02, E-01, E-02）
- quarantined: 2件（F-01, F-02）
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
- A-04（RSS）は再審査済みで done。D-02（背景動画取得）は quarantined のまま、境界と価値経路の個別再審査が済むまで進めない

## Authority Return Items

- G-02 done。IR 語彙定義 v1.0
- G-02b done。ymmp 構造解析完了。bg+face 差し替えが最小実用単位
- G-05 done (proof 待ち)。v4 プロンプト作成済み。**Custom GPT での proof はユーザー作業**
- G-06 done。patch-ymmp 変換器 + extract-template 実装済み。実機検証 OK
- **次**: Custom GPT で v4 proof → 実台本 E2E → パイプライン実用化
- G-01/G-03: hold (タイムライン操作 API 非公開)
- C-07 v3 done + proof 完了。Custom GPT Instructions は v3 に更新済み
- D-02: hold (C-07 v3 に吸収完了)
- E-01/E-02: hold 継続
- F-01/F-02: quarantined 継続

## 既知の問題

- 直前 handoff は 53f3718 時点の内容で止まっており、後続 commit `8a1c710` で追加された canonical docs とその未充足状態は含んでいなかった
- E-02 は YouTube Studio への手入力をテキストファイル生成に置き換えるだけで、実質的な効率化にならない (E-01 とセットでないと価値が出ない)
- D-02 / F-01 / F-02 は前セッションの汚染バッチ由来で、個別精査前に normal backlog として扱えない
- A-04 は実装済み・再審査済みだが、runtime/context の一部に旧 `quarantined` 記述が残っていたため handoff trust を要再同期
- B-14 後の追加観測では、長すぎる行は大幅に減り、全字幕が 3 行以内に収まる水準まで改善した。残 pain は bulk overflow ではなく、境界ケースの改行品質に移っている
- B-11/B-12/B-13/B-14 により、辞書や timing ではなく字幕改行が支配的な pain だと確認。B-14 後は `ー`、カギ括弧、数値+記号などの individual judgement が主で、次は heuristic を積み増すより corpus-based な例収集へ寄せる方が自然
- 別機能の feasibility を棚卸しした結果、次の本命候補は S-6 LLM adapter。E-01/E-02 は secondary、D-02/F-01/F-02 は引き続き quarantine 境界
- `prompt-resume.md` は作成済みだが、内容の正本は引き続き repo docs 側である

## 一時補助物（作ったら登録。統合/削除したら除去）
| ファイル/モジュール | 種別 | 削除条件 | 寿命 |
|---|---|---|---|
| docs/verification/ymm4-template-measurement.md | 実測手順書 | 実測完了+結果反映済み (2026-04-03)。削除可 | 完了 |
