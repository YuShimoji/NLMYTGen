# NAV.md — ドキュメント地図（迷子対策）

**役割**: 再開時に「まずどれを読むか」を 1 ファイルに圧縮する。仕様の正本や長い運用ルールは **ここに複製しない**（リンク先を正とする）。

---

## 1. 通常再開の 3 点（最短）

1. [AGENTS.md](../AGENTS.md) — 入口・境界・再アンカリング手順の正本
2. [REPO_LOCAL_RULES.md](REPO_LOCAL_RULES.md) — 短い front-door。Core Rules / Reporting / Ask Hygiene
3. [runtime-state.md](runtime-state.md) — 160 行以内の current capsule。product state / gate / recommended next / hard gates の正本

通常再開はここで止める。フル再アンカリングは、境界不明・drift 検出・user 明示の REANCHOR / REFRESH / AUDIT などの例外時だけ `AGENTS.md` の例外手順を使う。

GitHub 上で現在地だけを読む場合は [PROJECT_COCKPIT.md](PROJECT_COCKPIT.md) を使う。内部正本の `runtime-state.md` と同じ `Project-State-ID` を持つ追跡済みミラーであり、別の状態正本ではない。

**別端末再開**では、上の3点を読んだ後にだけ
[project-context.md](project-context.md) 最上部の「現在の別端末再開ハンドオフ」を開く。
過去の日付付き handoff を現在の指示として使わない。

Current sliceの判断と次の候補は、必要なときだけ
[decision-log.md](decision-log.md) と [idea-ledger.md](idea-ledger.md) を読む。

**Creative slice 例外**: 演出 / motion / 視覚 effect 制作タスクの場合、上記 3 点に加えて以下も必読:

- [MOTION_PRODUCTION_PIPELINE.md](MOTION_PRODUCTION_PIPELINE.md) — workflow 正本（5-phase pipeline + Anti-Shortcut Rules）
- [MOTION_PRESET_LIBRARY_SPEC.md](MOTION_PRESET_LIBRARY_SPEC.md) — emotion → atom data spec（23 ラベル）
- [samples/effect_catalog.json](../samples/effect_catalog.json) — 111 effect の機械可読カタログ

これらを読まずに motion 制作を試みること自体が `MOTION_PRODUCTION_PIPELINE.md` の Anti-Shortcut Rule #1 / #4 違反として扱う。

---

## 2. 正本マップ（仕様・台帳・検証索引）

- [GUI_MINIMUM_PATH.md](GUI_MINIMUM_PATH.md) — **Electron GUI**: 最小ファイル集合・必須/任意・ウィザード範囲（S-3 / S-6b）・L2/L3/creative 検証ラダー
- [TASK_DEVELOPMENT_CYCLE_SPEC.md](TASK_DEVELOPMENT_CYCLE_SPEC.md) — **改善レビューサイクル正本**: タスクごとの review surface / machine proof / human signal / close gate / next artifact。G-27 Real Estate DX、本流/sidequest 境界、Baseball screen plan、GUI/YMM4 の見る場所を統一する
- [INTERACTION_NOTES.md](INTERACTION_NOTES.md) — **対話 failure class**: broad question、manual proof 転送、status drift、形式先行を防ぐ
- [PRODUCTION_PIPELINE_CONTRACT.md](PRODUCTION_PIPELINE_CONTRACT.md) — **量産pipeline契約**: NotebookLM script → Script Beat IR → Visual Direction → Shot Layout → Motion Beat → GUI Review → downstream artifacts の artifact authority / Definition of Done / multi-topic smoke 計画。GUI timeline を primary review surface とし、HTML/PNG/JSON を evidence に限定する
- [G27_ADAPTER_ROUTE_CONTRACT.md](G27_ADAPTER_ROUTE_CONTRACT.md) — **G-27 YMM4 adapter route 契約 (planning zone)**: Real Estate DX の 7 adapter-planning-ready candidates、`RE-02-turn` excluded_until_adjusted、`RE-07D-turn` deferred_blocks_planning、route 分類 (abstract UI / document proxy / property card / risk marker / AI panel)、forbidden representation、preflight report、`output_generation_allowed=false`。adapter output / patch / render / production timing / creative acceptance は範囲外
- [REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md](REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md) — **G-28 参照画像ベース汎用画面 carrier 設計**: G-27 の case-specific lessons を引き継ぎ、参照画像 3-7 枚から構図・密度・余白・色階層・視線誘導・UI感を抽出して SCS mapping / generic carrier archetype / YMM4 item group 案へ落とす。画像丸コピー、raw image/URL/private data commit、`.ymmp` ゼロ生成、render、creative final acceptance は含めない
- [verification/G28-REFERENCE-INPUT-WAIT-HANDOFF-2026-06-04.md](verification/G28-REFERENCE-INPUT-WAIT-HANDOFF-2026-06-04.md) — **G-28 parked / input-wait handoff**: 参照画像待ちの戻る条件、禁止事項、meta-review trigger、ChatGPT copy-block requirement を保存した詳細 handoff。通常再開では読まない
- [PROXY_ASSET_CLASSIFICATION_SCHEMA.md](PROXY_ASSET_CLASSIFICATION_SCHEMA.md) — **proxy / asset 分類 schema**: visual treatment proof の beat を scene decision packet / asset-proxy gap report / YMM4 adapter のどこへ渡すか分類する関所。分類のみで downstream artifact は作らない
- [INT02E_REAL_URL_OPERATOR_SMOKE_GATE.md](INT02E_REAL_URL_OPERATOR_SMOKE_GATE.md) — **INT-02e real URL operator smoke gate**: `baseline / in_progress` 固定。`done` は actual fetch、`source.wav` Python `wave` readback、receipt / sidecar / `material_ledger`、ledger audit、boundary grep、scrub 済み report まで揃ってから。real URL smoke 前に target commit、clean status、`HEAD...origin/main = 0 0` を確認し、`fetch-source-video` / GUI fetch / STT URL / cut-concat / render / Publishing-OAuth へ広げない
- [EPISODE_RUN_PACK.md](EPISODE_RUN_PACK.md) — **1本通し制作パック**: `_tmp/episode_runs/<episode_id>/` の構成、GUI `Episode Pack Root` 導線、既定保存path、YMM4確認と gaps 記録の境界
- [RSS_READER_SYNC_SPEC.md](RSS_READER_SYNC_SPEC.md) — **A-04 RSS Reader Sync**: OPML export を人間側 RSS 一覧と AI 側 `fetch-topics` 対象の共通正本にする。Inoreader は read-only adapter まで実装済み、OAuth/token 永続化は実装しない
- [verification/RSS-LIVE-SMOKE-RUNBOOK-2026-05-26.md](verification/RSS-LIVE-SMOKE-RUNBOOK-2026-05-26.md) — **A-04 RSS live smoke entry**: raw OPML/token 置き場、`rss-smoke` の one-command evidence、OPML/Inoreader smoke コマンド、次の判断表
- [verification/PROJECT_INIT_CHECKLIST.md](verification/PROJECT_INIT_CHECKLIST.md) — **実案件投入**: palette → registry → validate-ir → apply-production の 5 ステップ
- [verification/FAILURE_DIAGNOSIS_MATRIX.md](verification/FAILURE_DIAGNOSIS_MATRIX.md) — ERROR/WARNING 全 64 種の診断マトリクス
- `samples/registry_template/` — 6 種の registry JSON 雛形（overlay/se/bg/slot/face/group_motion_map）
- `samples/effect_catalog.json` — YMM4 v4.51 の VideoEffect カタログ（111 ユニーク、9 カテゴリ）。抽出元 `samples/EffectsSamples_2026-04-15.ymmp` / 再抽出 `scripts/extract_effect_catalog.py`。**用途**: `motion_map` / `tachie_motion_map` / `bg_anim_map` / `group_motion_map` に書くエフェクト名・`$type`・パラメータキーのピックアップ元。運用メモ [samples/EFFECT_CATALOG_USAGE.md](../samples/EFFECT_CATALOG_USAGE.md)
- [TIMELINE_EFFECT_CAPABILITY_ATLAS.md](TIMELINE_EFFECT_CAPABILITY_ATLAS.md) — **Capability Atlas 正本**。`IR -> registry -> ymmp` の接合点で、何が `direct_proven` / `template_catalog_only` / `probe_only` / `unsupported` かを 1 枚で判断する。機械台帳: `python scripts/build_capability_atlas.py` -> `samples/_generated/capability_atlas.json`
- [VISUAL_EFFECT_SELECTION_GUIDE.md](VISUAL_EFFECT_SELECTION_GUIDE.md) — **視覚効果ツール選定**: 4 類 × 3 ルート比較・エフェクト 111 種の用途別再編・テンプレバンドル 5 種案・ハンズオン 5 ステップ。姉妹: [VISUAL_TOOL_DECISION.md](VISUAL_TOOL_DECISION.md)(ユーザー記入)・[MATERIAL_SOURCING_RULES.md](MATERIAL_SOURCING_RULES.md)(素材運用ルール)
- [STEP3_YMM4_TEMPLATE_CHECKLIST.md](STEP3_YMM4_TEMPLATE_CHECKLIST.md) / [STEP3_TACHIE_RENDERING_PIPELINE.md](STEP3_TACHIE_RENDERING_PIPELINE.md) — **視覚効果 slice Step 3 ハンズオン**: 5 種テンプレ各エフェクトの parameter 初期値+チェックリスト / G-22 dual-rendering 経路 B の PNG 書き出し→overlay_map 登録パイプライン
- [BASEBALL_NEWS_PIPELINE_SPEC.md](BASEBALL_NEWS_PIPELINE_SPEC.md) — **野球速報 sidequest 正本**: 本流を置き換えない別レーン。C 詳細インフォグラフィックを正本デザインとして扱い、screen plan で動画全体の画面割り・情報量・YMM4 配置を確認してから PNG/animation export へ進む
- [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md) — **茶番劇 Group テンプレ正本**: 茶番劇を語り手への合いの手ではなく独立した背景小場面として定義し、配達員などの外部素材演者を `speaker_tachie` と分離し、canonical template → 小演出量産 → production での template 解決 + fallback note までを定義
- [PILOT_YUKKURI_THEATER_SCENE_BIBLE.md](PILOT_YUKKURI_THEATER_SCENE_BIBLE.md) — **pilot_yukkuri_theater_v1 背景茶番劇 Scene Bible**: 不動産DXの 7 ブロック time budget / cast continuity / screen placement / props / proof path と、配達短編の setup → complication → reaction → resolution を固定する IR 前の正本
- [BACKGROUND_SKIT_BLUEPRINT_TIMETABLE_WORKFLOW.md](BACKGROUND_SKIT_BLUEPRINT_TIMETABLE_WORKFLOW.md) — **背景茶番劇 Blueprint/Timetable 正本**: IR / 演出指定へ進む前に、総尺・開始/終了時刻・演出秒数・density thresholds/audit・script maturity・asset/control matrix を `background_skit_blueprint` artifact と validator result で固定する

`docs/verification` 直下の個別ファイルが多いときは、先に次の **索引表**だけ読む。

- [verification/README.md](verification/README.md) — 証跡ディレクトリの読み方（現行判断の索引ではない）

---

## 3. 並行作業・手順

- [OPERATOR_PARALLEL_WORK_RUNBOOK.md](OPERATOR_PARALLEL_WORK_RUNBOOK.md) — オペレータ並行。現行 `next_action` と接続する場合だけ参照する
- [verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md) — 立ち絵 複数体×顔差し替え（**G-19 `done` / G-20 `approved`** の準備正本）。茶番劇演者の現行主軸は [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md)
- `samples/registry_template/skit_group_registry.template.json` — **茶番劇 Group 台帳雛形**。canonical group / 派生 template / fallback / manual check を shared registry として記録する。`audit-skit-group` / `patch-ymmp --skit-group-registry` / `apply-production --skit-group-registry` の preflight 入力でもある
- [verification/G22-dual-rendering-tachie-and-png-2026-04-16.md](verification/G22-dual-rendering-tachie-and-png-2026-04-16.md) — **G-22 `hold`**: 立ち絵 TachieItem + YMM4 書き出し PNG の補助経路。現行主軸ではなく、必要時のみ参照
- [prompts/B18-script-diagnostics-observation-prompt.md](prompts/B18-script-diagnostics-observation-prompt.md) / [prompts/B17-reflow-residue-observation-prompt.md](prompts/B17-reflow-residue-observation-prompt.md) — メンテ層の詳細手順。ゆっくり解説本流の `next_action` を押し流さない場合だけ使う

---

## 4. テンプレと状態（混同しやすい点）

汎用 Prompt ハブ・ファイル番号式のコア計画・パケット別短文 Prompt は削除済み。テンプレは状態正本ではなく、`open target` / `create target` / `source object` / `actor` / `acceptance meaning` が接続済みのときだけ、該当する詳細手順ファイルを使う。

**いまどこまで終わっているか**は、次を見る。

- [runtime-state.md](runtime-state.md) の shared state fields / Product Position / Human or External Decision Points
- [TASK_DEVELOPMENT_CYCLE_SPEC.md](TASK_DEVELOPMENT_CYCLE_SPEC.md) の G-27 / 本流-sidequest 境界 / Baseball / GUI-YMM4 review cycle
- [verification/P02-production-adoption-proof.md](verification/P02-production-adoption-proof.md) の G-24 基盤受け入れ・採用記録
- 案件ごとの `*-proof.md` や verification 配下の JSON 証跡

---

## 5. 航海日誌（任意・長大）

- [project-context.md](project-context.md) — DECISION LOG・HANDOFF。**IDE の Markdown プレビューが空白になることがある**場合はエディタのソース表示で開く（`AGENTS.md` 注記どおり）。
