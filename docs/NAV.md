# NAV.md — ドキュメント地図（迷子対策）

**役割**: 再開時に「まずどれを読むか」を 1 ファイルに圧縮する。仕様の正本や長い運用ルールは **ここに複製しない**（リンク先を正とする）。

---

## 1. 通常再開の 3 点（最短）

1. [AGENTS.md](../AGENTS.md) — 入口・境界・再アンカリング手順の正本
2. [REPO_LOCAL_RULES.md](REPO_LOCAL_RULES.md) — Hard Rules・再開読了予算・Checklist の正本
3. [runtime-state.md](runtime-state.md) — 現在位置・`next_action`・カウンターの正本

通常再開はここで止める。フル再アンカリングは、境界不明・drift 検出・user 明示の REANCHOR / REFRESH / AUDIT などの例外時だけ `AGENTS.md` の例外手順を使う。

**Creative slice 例外**: 演出 / motion / 視覚 effect 制作タスクの場合、上記 3 点に加えて以下も必読:

- [MOTION_PRODUCTION_PIPELINE.md](MOTION_PRODUCTION_PIPELINE.md) — workflow 正本（5-phase pipeline + Anti-Shortcut Rules）
- [MOTION_PRESET_LIBRARY_SPEC.md](MOTION_PRESET_LIBRARY_SPEC.md) — emotion → atom data spec（23 ラベル）
- [samples/effect_catalog.json](../samples/effect_catalog.json) — 111 effect の機械可読カタログ

これらを読まずに motion 制作を試みること自体が `MOTION_PRODUCTION_PIPELINE.md` の Anti-Shortcut Rule #1 / #4 違反として扱う。

---

## 2. 正本マップ（仕様・台帳・検証索引）

- [GUI_MINIMUM_PATH.md](GUI_MINIMUM_PATH.md) — **Electron GUI**: 最小ファイル集合・必須/任意・ウィザード範囲（S-3 / S-6b）・L2/L3/creative 検証ラダー
- [verification/PROJECT_INIT_CHECKLIST.md](verification/PROJECT_INIT_CHECKLIST.md) — **実案件投入**: palette → registry → validate-ir → apply-production の 5 ステップ
- [verification/FAILURE_DIAGNOSIS_MATRIX.md](verification/FAILURE_DIAGNOSIS_MATRIX.md) — ERROR/WARNING 全 64 種の診断マトリクス
- `samples/registry_template/` — 6 種の registry JSON 雛形（overlay/se/bg/slot/face/group_motion_map）
- `samples/effect_catalog.json` — YMM4 v4.51 の VideoEffect カタログ（111 ユニーク、9 カテゴリ）。抽出元 `samples/EffectsSamples_2026-04-15.ymmp` / 再抽出 `scripts/extract_effect_catalog.py`。**用途**: `motion_map` / `tachie_motion_map` / `bg_anim_map` / `group_motion_map` に書くエフェクト名・`$type`・パラメータキーのピックアップ元。運用メモ [samples/EFFECT_CATALOG_USAGE.md](../samples/EFFECT_CATALOG_USAGE.md)
- [TIMELINE_EFFECT_CAPABILITY_ATLAS.md](TIMELINE_EFFECT_CAPABILITY_ATLAS.md) — **Capability Atlas 正本**。`IR -> registry -> ymmp` の接合点で、何が `direct_proven` / `template_catalog_only` / `probe_only` / `unsupported` かを 1 枚で判断する。機械台帳: `python scripts/build_capability_atlas.py` -> `samples/_generated/capability_atlas.json`
- [VISUAL_EFFECT_SELECTION_GUIDE.md](VISUAL_EFFECT_SELECTION_GUIDE.md) — **視覚効果ツール選定**: 4 類 × 3 ルート比較・エフェクト 111 種の用途別再編・テンプレバンドル 5 種案・ハンズオン 5 ステップ。姉妹: [VISUAL_TOOL_DECISION.md](VISUAL_TOOL_DECISION.md)(ユーザー記入)・[MATERIAL_SOURCING_RULES.md](MATERIAL_SOURCING_RULES.md)(素材運用ルール)
- [STEP3_YMM4_TEMPLATE_CHECKLIST.md](STEP3_YMM4_TEMPLATE_CHECKLIST.md) / [STEP3_TACHIE_RENDERING_PIPELINE.md](STEP3_TACHIE_RENDERING_PIPELINE.md) — **視覚効果 slice Step 3 ハンズオン**: 5 種テンプレ各エフェクトの parameter 初期値+チェックリスト / G-22 dual-rendering 経路 B の PNG 書き出し→overlay_map 登録パイプライン
- [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md) — **茶番劇 Group テンプレ正本**: 配達員などの外部素材演者を `speaker_tachie` と分離し、canonical template → 小演出量産 → production での template 解決 + fallback note までを定義

`docs/verification` 直下の個別ファイルが多いときは、先に次の **索引表**だけ読む。

- [verification/README.md](verification/README.md) — 証跡ディレクトリの読み方（現行判断の索引ではない）

---

## 3. 並行作業・手順

- [OPERATOR_PARALLEL_WORK_RUNBOOK.md](OPERATOR_PARALLEL_WORK_RUNBOOK.md) — オペレータ並行。現行 `next_action` と接続する場合だけ参照する
- [verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md) — 立ち絵 複数体×顔差し替え（**G-19 `done` / G-20 `approved`** の準備正本）。茶番劇演者の現行主軸は [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md)
- `samples/registry_template/skit_group_registry.template.json` — **茶番劇 Group 台帳雛形**。canonical group / 派生 template / fallback / manual check を shared registry として記録する。`audit-skit-group` / `patch-ymmp --skit-group-registry` / `apply-production --skit-group-registry` の preflight 入力でもある
- [verification/G22-dual-rendering-tachie-and-png-2026-04-16.md](verification/G22-dual-rendering-tachie-and-png-2026-04-16.md) — **G-22 `hold`**: 立ち絵 TachieItem + YMM4 書き出し PNG の補助経路。現行主軸ではなく、必要時のみ参照
- [prompts/B18-script-diagnostics-observation-prompt.md](prompts/B18-script-diagnostics-observation-prompt.md) / [prompts/B17-reflow-residue-observation-prompt.md](prompts/B17-reflow-residue-observation-prompt.md) — メンテ層の詳細手順。主軸 G-24 を押し流さない場合だけ使う

---

## 4. テンプレと状態（混同しやすい点）

汎用 Prompt ハブ・ファイル番号式のコア計画・パケット別短文 Prompt は削除済み。テンプレは状態正本ではなく、`open target` / `create target` / `source object` / `actor` / `acceptance meaning` が接続済みのときだけ、該当する詳細手順ファイルを使う。

**いまどこまで終わっているか**は、次を見る。

- [runtime-state.md](runtime-state.md) の `next_action` / `parallel_replan_*`
- [verification/P02-production-adoption-proof.md](verification/P02-production-adoption-proof.md) の G-24 受け入れ・採用記録
- 案件ごとの `*-proof.md` や verification 配下の JSON 証跡

---

## 5. 航海日誌（任意・長大）

- [project-context.md](project-context.md) — DECISION LOG・HANDOFF。**IDE の Markdown プレビューが空白になることがある**場合はエディタのソース表示で開く（`AGENTS.md` 注記どおり）。
