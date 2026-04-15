# G20 Group制御・素材配置自動化 包括レビュー（2026-04）

## 1. 結論サマリ

- 現行の A案（既存 GroupItem の `X/Y/Zoom` 更新）は、**中央基準テンプレ運用が守られる限り**実運用可能。
- いまの主ボトルネックは「Group の生成ロジック不足」よりも、**テンプレ品質と命名規約の運用ばらつき**。
- 次スライスは B案（Group 自動生成）ではなく、**A案の失敗安全性と運用規約を先に強化**するのが、短期価値と保守性のバランスが最も良い。

## 2. 現行ベースライン（できること / できないこと）

### 2.1 できること

- `validate-ir --group-motion-map` で `group_motion` の未知ラベルを検知できる。
- `patch-ymmp --group-motion-map` で既存 GroupItem に `X/Y/Zoom` を適用できる。
- `group_target` 未指定時は GroupItem が1件なら自動適用できる。
- `measure-timeline-routes` と `timeline_route_contract` で `GroupItem.X/Y/Zoom` 経路を契約化できる。

### 2.2 できないこと

- GroupItem の新規生成やレイヤー再配置（B案）は未実装。
- 複数 GroupItem 環境で `group_target` 省略時の曖昧解決はできない。
- Group 幾何は `X/Y/Zoom` に限定され、反転/回転/複合キーフレームは未対応。

## 3. リスク評価（warning/error と運用依存）

### 3.1 失敗モード分類

- **Error（事前検知）**
  - `GROUP_MOTION_UNKNOWN_LABEL`
  - `GROUP_MOTION_INVALID_TYPE`
  - `GROUP_TARGET_INVALID_TYPE`
- **Warning（適用時）**
  - `GROUP_MOTION_NO_GROUP_ITEM`
  - `GROUP_MOTION_TARGET_MISS`
  - `GROUP_MOTION_TARGET_AMBIGUOUS`
  - `GROUP_MOTION_DRIFT`
  - `GROUP_MOTION_VALUE_INVALID`

### 3.2 運用依存ボトルネック

- `group_target` 命名（通常 `Remark`）の不統一。
- テンプレごとの Group 構造差（単一 Group 前提が崩れる）。
- 中央基準テンプレの徹底不足（ズーム時の再現性低下）。
- 素材側（頭/体/装飾）相対配置が不安定なテンプレ混在。

## 4. 優先候補（3-5件）

### High

1. **`group_target` 運用規約の lint 強化（validate側）**  
   - 目的: 曖昧適用・命名揺れを事前に止める。  
   - 影響: `src/pipeline/ir_validate.py`, `src/cli/main.py`, tests, docs。

2. **Group適用 warning の一部を条件付き fatal 化**  
   - 目的: 「適用されたつもり」を防ぐ。  
   - 候補: `NO_GROUP_ITEM` / `TARGET_MISS` / `TARGET_AMBIGUOUS`。  
   - 影響: `src/cli/main.py` の fatal 判定、運用ドキュメント、回帰テスト。

### Medium

3. **テンプレ監査チェックの標準化（Group中央基準 + 命名確認）**  
   - 目的: 実装より先にテンプレ品質を均質化。  
   - 影響: `docs/verification/*`（runbook/checklist）中心、コード影響小。

4. **`face_map_bundle` / `group_target` の事前整合チェックを一体化**  
   - 目的: 素材配置とGroup適用の前提不一致を早期発見。  
   - 影響: validate系ロジックとテスト。

### Low（deferred）

5. **B案（Group自動生成）検討**  
   - 理由: レイヤー再配置・衝突回避・既存アイテム保全の複雑性が高く、今の価値対コストが低い。

## 5. 次スライス推奨（1件）

**推奨着手:** `group_target` / `group_motion` の失敗安全性強化（High-1 + High-2 を1スライス化）

- 実施範囲（最小）
  - `validate-ir` に命名規約チェックを追加（曖昧運用を検知）。
  - `patch-ymmp` 実行結果で Group 適用失敗 warning を条件付き fatal 化。
  - 既存成功パス（単一 Group・明示 target）は挙動変更なし。
- 見送り
  - B案（Group生成）
  - 回転/反転/複合キーフレーム
  - 素材自動再配置（テンプレ再編込みの大規模化）

## 7. 実施結果（次スライス反映）

- `GROUP_MOTION_NO_GROUP_ITEM`
- `GROUP_MOTION_TARGET_MISS`
- `GROUP_MOTION_TARGET_AMBIGUOUS`

上記3クラスを warning から **fatal（書き出し前停止）**へ昇格した。  
`patch-ymmp` と `apply-production` の両経路で同一判定を適用する。

**追記（G-20 スライス1・2026-04-14）**: 台帳 G-20 を `approved` に更新。`validate-ir`（`src/pipeline/ir_validate.py`）で `group_target` の **空・前後空白・改行含有**を `GROUP_TARGET_EMPTY` / `GROUP_TARGET_SURROUNDING_WHITESPACE` / `GROUP_TARGET_NEWLINE` として事前エラー化。単体テストは `tests/test_ymmp_motion_patch.py`（`test_validate_ir_group_target_*`）。

**追記（G-20 スライス2・2026-04-15）**: `group_motion_map` に **`mode: "relative"`**（相対オフセット）を追加。`absolute`（既定・従来互換）は絶対値書き込み、`relative` は GroupItem の現在値に加算。`_load_group_motion_map` でモード値バリデーション。テスト 7 件追加。`samples/group_motion_map.example.json` に `nudge_left` / `nudge_right` / `zoom_in_relative` サンプル。

## 8. 残スライス候補（レガシー化防止・起票）

以下はスライス1/2 の包括レビューで特定された中優先候補。実案件で価値が確認されたタイミングで個別スライスに昇格する。

### 候補C: `face_map_bundle` と `group_target` の事前整合チェック

- **目的**: 素材配置（face_map_bundle のキャラ・body 構成）と Group 適用（group_target の命名）の前提不一致を、`validate-ir` 段階で早期発見する。
- **影響範囲**: `src/pipeline/ir_validate.py`（チェック追加）、テスト。プロダクトコードの挙動変更なし。
- **昇格トリガー**: 実案件で `face_map_bundle` と `group_target` の不一致が原因の手戻りが発生したとき。
- **状態**: proposed（値検証待ち）

### 候補D: テンプレ監査チェックの標準化（Group 中央基準 + 命名確認）

- **目的**: テンプレごとの Group 構造差（単一 Group 前提の崩れ、中央基準のずれ）を運用ルールとして明文化し、新テンプレ投入時のチェックリストを標準化する。
- **影響範囲**: `docs/verification/` のチェックリスト・runbook 中心。コード変更は最小（チェック自動化する場合のみ）。
- **昇���トリガー**: テンプレ追加・差し替え時に Group 構造の不一致で適用失敗が頻発したとき。
- **状態**: proposed（値検証待ち）

## 6. 包括見直しの判断基準（���回継続用）

- テンプレ監���で `group_target` 命名一致率が十分か。
- Group��用失敗の発生頻度が fatal 化後に許���範囲か。
- 1本あた��手動修正時間がどれだけ減ったか（定��）。
- **候補C/D の昇格判断**: 上記トリガーに該当する手戻りが出たら、本節 §8 から個別スライスに昇格する。
