# レーン B（GUI LLM 正本同期）実施記録

> 対象: レーン B（B-1〜B-5）  
> 実施日: 2026-04-09  
> 構成: **ChatGPT Custom GPT / 2体分離（S1専用 + S6専用）**

---

## 1. 固定した運用方針（B-1）

- プラットフォームは **ChatGPT Custom GPT** を採用。
- GPT 構成は **2体分離**（S1/C-09 と S6/C-07 v4 を分離）を採用。
- 正本参照は以下に固定:
  - `docs/S1-script-refinement-prompt.md`
  - `docs/S6-production-memo-prompt.md`（`### v4 プロンプト本体` のコードフェンス内全文）
  - `docs/S8-thumbnail-copy-prompt.md`
  - `docs/verification/LANE-B-gui-llm-sync-checklist.md`

---

## 2. S1 同期・検証手順（B-2）

S1 用 GPT は `docs/S1-script-refinement-prompt.md` の「LLM への指示」節を正本として同期する。

最小検証（repo 側で再現可能な機械検証）:

```powershell
uv run python -m src.cli.main validate-ir "samples/ir_visual_styles_dry_sample.json" --face-map "samples/face_map.json"
```

実行結果（要点）:
- `Validation PASSED`
- v4 の face 契約整合を確認（prompt/palette/used の表示）

---

## 3. S6 v4 同期・検証手順（B-3）

S6 用 GPT は `docs/S6-production-memo-prompt.md` の `### v4 プロンプト本体` フェンス内全文で丸ごと置換する。  
v3 断片の混在は不可。

最小検証（`apply-production --dry-run`）:

```powershell
uv run python -m src.cli.main apply-production "samples/test_verify_4_bg_p2_small.ymmp" "samples/p2_bg_anim_small_scope.ir.json" --bg-map "samples/bg_map_p2_small_scope.json" --transition-map "samples/transition_map_p2_small_scope.json" --bg-anim-map "samples/bg_anim_map_p2_small_scope.json" --dry-run
```

実行結果（要点）:
- exit code `0`
- `Timeline adapter: motion=0, transition=4, bg_anim=3`
- `BG anim writes: 3`
- `Transition VoiceItem writes: 4`

---

## 4. H-01 連携方式（B-4）

今回の固定方針は **「会話ごとに brief を台本より先に貼る」** を採用する。  
理由: S6 v4 本体を最小で保ち、Instructions 側の肥大化と誤同期リスクを下げるため。

参照:
- `docs/PACKAGING_ORCHESTRATOR_SPEC.md`
- `samples/packaging_brief.template.md`

---

## 5. サムネ運用方式（B-5）

今回の固定方針:
- **H-02 準拠が必要な案件**: `docs/S8-thumbnail-copy-prompt.md` を別ラウンド（または別 GPT）で使用
- **高速な素案のみ必要な案件**: S6 v4 の Part 4 を使用

これにより、厳密運用と速度優先運用を案件単位で切り替える。

---

## 6. 差分有無と受け渡し

- repo 正本（S1/S6/S8/チェックリスト）に対する運用差分: **なし（方針固定のみ）**
- 外部 GUI（Custom GPT）への貼り付け作業: **オペレータ実施**
- 本記録は、レーン B の運用判断と最小機械検証を repo 側で再現可能な形で残すための証跡
