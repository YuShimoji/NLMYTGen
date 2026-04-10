# T1-H01 — packaging template 差分のバグ修正ゲート記録

**目的**: `src/pipeline/packaging_brief_template.py` と `tests/test_emit_packaging_brief_template.py` の差分が、未承認 FEATURE 実装ではなく **H-01（approved）範囲の明確なバグ修正**であることを機械的に記録する。  
**判定対象**: `rotation_axes` / `consumer_hints` の必須キーを JSON テンプレに含める修正と、その検証テスト。  
**根拠正本**: [PACKAGING_ORCHESTRATOR_SPEC.md](../PACKAGING_ORCHESTRATOR_SPEC.md) §5（推奨フォーマット）。

---

## 1. 仕様との差分（修正前）

- 仕様 §5 では `thumbnail_controls.rotation_axes` に `layout_family` / `emotion_family` / `color_family` / `copy_family` が必須。
- 同じく `consumer_hints` に `for_c07` / `for_c08` / `for_e02` / `for_h04` / `for_h03` が定義される。
- 修正前テンプレは `consumer_hints` を空オブジェクトで返しており、上記キーの欠落を検出できない状態だった。

判定: **仕様追従の不足（バグ）**

## 2. 修正内容（最小）

- `minimal_json_brief()` の `consumer_hints` に仕様キーを空文字で初期化して追加。
- `REQUIRED_ROTATION_AXES_KEYS` / `REQUIRED_CONSUMER_HINT_KEYS` を追加し、`_validate_json_brief_schema()` で存在検証を追加。
- 既存テストにキー検証を追補し、CLI 出力 JSON でも同キーが落ちないことを確認可能にした。

判定: **仕様欠落の補正に限定（新機能なし）**

## 3. FEATURE_REGISTRY 境界確認

- H-01 は [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) で `approved`。  
- 今回の変更は H-01 の「テンプレ生成」範囲内で、外部連携や自動注入など未承認拡張には踏み込んでいない。  
- 新規 FEATURE ID の追加、既存 `quarantined` 項目の復活、新しい UI 機能追加はなし。

判定: **T1 許容（承認済み範囲のバグ修正）**

---

## 4. 最終判定

結論: 本差分は **未承認 FEATURE 実装ではなく、H-01 仕様欠落のバグ修正**として T1 境界に適合。
