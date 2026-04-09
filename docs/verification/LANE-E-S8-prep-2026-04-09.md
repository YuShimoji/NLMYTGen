# レーン E — サムネ 1 枚（S-8）準備チェックリスト

> **目的**: [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) のレーン E と [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) トラック E を、**公開直前の 1 枚**まで漏れなく進める。  
> **正本**: 手順 [THUMBNAIL_ONE_SHEET_WORKFLOW.md](../THUMBNAIL_ONE_SHEET_WORKFLOW.md)・全体像 [WORKFLOW.md](../WORKFLOW.md) S-8。コア開発（新規 FEATURE・自動サムネ生成）はスコープ外（PRE-PLAN §1.3）。

---

## 運用クローズ（本サイクル・2026-04-09）

**repo 側の準備**（本ファイル・P03 の `lane_e_prep_2026-04-09_a`・正本チェーンの索引）は完了。**コア開発幹へ復帰**する（[runtime-state.md](../runtime-state.md) の `next_action`）。

公開直前の **実サムネ 1 枚**（YMM4 書き出し・B-5 実同期・上記チェックボックスの実施）は、並行オペレーションとして **P3 / runbook トラック E** で従来どおり実施すればよい。本サイクルにおけるレーン E 起因の**開発ブロックはなし**。

---

## S-0. 初回のみ（YMM4 テンプレと書き出し）

[THUMBNAIL_ONE_SHEET_WORKFLOW.md](../THUMBNAIL_ONE_SHEET_WORKFLOW.md)「事前準備」に対応。

- [ ] **サムネ用 YMM4 テンプレ**を用意した（文字レイヤー・立ち絵差し込み・背景スロットが決まっている）
- [ ] **書き出し解像度**を 1280×720（または運用で固定した解像度）に揃えた
- [ ] 元テンプレを上書きしないよう、**毎回プロジェクト複製**する運用にした

**repo 側の固定**: 上記の要件文は `THUMBNAIL_ONE_SHEET_WORKFLOW.md` が正本。本チェックリストはオペレータ確認用。

---

## B-5 との突き合わせ（C-08 正本）

レーン B の **B-5** を別途実施する（詳細手順は [LANE-B-gui-llm-sync-checklist.md](LANE-B-gui-llm-sync-checklist.md) §B-5）。

**C-08 正本**: [S8-thumbnail-copy-prompt.md](../S8-thumbnail-copy-prompt.md)

- [ ] Custom GPT / Claude Project / 統合プロンプトのいずれかで、S8 正本と **一致**している（[gui-llm-setup-guide.md](../gui-llm-setup-guide.md) Part 4 参照）
- [ ] 今回の案件で **S8 専用ラウンド**と **C-07 v4 Part 4 素案**のどちらを使うか決めた（LANE-B B-5 の表どおり）

---

## 案件入力セット（レーン E 用・デフォルト例）

次のセットは **B-11 実案件台本**と整合しやすい既定例。別案件に差し替える場合は同じ列を埋め直す。

| 項目 | 既定（repo 内パス・ID） |
|------|-------------------------|
| 動画スラッグ（ファイル名用） | `ai_monitoring_labor`（運用で `thumb_ai_monitoring_labor.png` 等） |
| 台本（C-08 入力の根拠テキスト） | [samples/AI監視が追い詰める生身の労働.txt](../../samples/AI監視が追い詰める生身の労働.txt) |
| H-01 brief | **任意**。使う場合は S8 冒頭どおり **先に brief を貼る**。[samples/packaging_brief.template.md](../../samples/packaging_brief.template.md) を複製して案件用に記入 |
| 訴求・禁止パターン（参照） | [THUMBNAIL_STRATEGY_SPEC.md](../THUMBNAIL_STRATEGY_SPEC.md)（H-02） |

- [ ] 上表のスラッグ・台本パス（または差し替え後のパス）を記録した
- [ ] brief を使わない場合も、**タイトル・台本・サムネ**の大きな矛盾がないよう注意すると決めた

---

## E-実行（毎回・YMM4）

[THUMBNAIL_ONE_SHEET_WORKFLOW.md](../THUMBNAIL_ONE_SHEET_WORKFLOW.md)「毎回の手順」に従う。

- [ ] テンプレートプロジェクトを**複製**した
- [ ] タイトル文字・立ち絵／表情・背景を**差し替え**た
- [ ] 必要なら C-08 でキャッチコピー案を出し、テキストを反映した
- [ ] **静止画書き出し**（PNG 推奨）→ ファイル名をスラッグに合わせて保存した
- [ ] **品質チェック**（主張 1 点・具体性・タイトル／内容整合）を通した

---

## 参照アンカー（既存サンプル・机上照合）

YMM4 を持たない環境では新規 PNG を生成できない。レーン E **準備サイクル**では、次の既存成果物を **手順・品質軸の参照アンカー**とする（新規書き出し後は P03 に別 run で追記する）。

| 項目 | 内容 |
|------|------|
| 参照ファイル | `samples/onepass_2026-04-07_c_thumb.png` |
| P03 既存記録 | [P03-thumbnail-one-sheet-proof.md](P03-thumbnail-one-sheet-proof.md) の「One-Pass Run (`onepass_2026-04-07_c`)」 |
| 机上照合 | 主張 1 点・具体性（例: `19億ドル`）・H-01 整合の簡易判定が既存記録と一致すること |

**本リポジトリ作業（2026-04-09 準備実装）**: `THUMBNAIL_ONE_SHEET_WORKFLOW.md` と runbook トラック E の参照関係に矛盾がないことを確認済み。上記サンプルは P03 で pass 済みのため、準備段階の品質軸はこれに紐付けてよい。

---

## 完了後の記録（推奨）

- [P03-thumbnail-one-sheet-proof.md](P03-thumbnail-one-sheet-proof.md) に **run_id・出力パス・判定**を 1 ブロック追記する（本準備サイクルでは `lane_e_prep_2026-04-09_a` を追記済み）。

---

## 変更履歴

- 2026-04-09: 運用クローズ節を追加（本開発幹へ復帰、実サムネは P3・トラック E で並行）。
- 2026-04-09: 初版。PRE-PLAN レーン E・runbook トラック E に対応。
