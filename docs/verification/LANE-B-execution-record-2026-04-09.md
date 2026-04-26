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

---

## 7. 再検証 2026-04-10（ファイル5 レーンB・Prompt-B）

実施目的: [LANE-B-gui-llm-sync-checklist.md](LANE-B-gui-llm-sync-checklist.md) B-1〜B-5 の維持確認と、当時の「プロンプト同期」観点の証跡更新。

### 7.1 正本参照コミット（repo）

- `git rev-parse HEAD` → `fb0659ad512384e82aaefab9d1ec2ad42b9fd86f`（短縮 `fb0659a`）
- 突合対象ファイル: `docs/S1-script-refinement-prompt.md`、`docs/S6-production-memo-prompt.md`（`### v4 プロンプト本体` フェンス内全文）、`docs/S8-thumbnail-copy-prompt.md`

### 7.2 B-1（セットアップ方針）

- [gui-llm-setup-guide.md](../gui-llm-setup-guide.md) を再確認。**方式 A（Custom GPT）**・**2体分離（S1 専用 + S6 v4 専用）**を継続。2026-04-09 記録からの変更なし。

### 7.3 B-2 機械検証（validate-ir）

```powershell
uv run python -m src.cli.main validate-ir "samples/ir_visual_styles_dry_sample.json" --face-map "samples/face_map.json"
```

- exit code: `0`
- 出力要点: `Validation PASSED`、face 契約表示（prompt/palette/used）確認

### 7.4 B-3 機械検証（apply-production --dry-run）

```powershell
uv run python -m src.cli.main apply-production "samples/test_verify_4_bg_p2_small.ymmp" "samples/p2_bg_anim_small_scope.ir.json" --bg-map "samples/bg_map_p2_small_scope.json" --transition-map "samples/transition_map_p2_small_scope.json" --bg-anim-map "samples/bg_anim_map_p2_small_scope.json" --dry-run
```

- exit code: `0`
- 出力要点: `Timeline adapter: motion=0, transition=4, bg_anim=3` / `BG anim writes: 3` / `Transition VoiceItem writes: 4`（2026-04-09 記録 §3 と一致）

### 7.5 B-4 / B-5（運用方針・再掲）

- **B-4**: 継続して **会話ごとに brief を台本より先に貼る**（S6 v4 本体の最小化）。参照: `docs/PACKAGING_ORCHESTRATOR_SPEC.md`、`samples/packaging_brief.template.md`
- **B-5**: **H-02 準拠が必要な案件**は `docs/S8-thumbnail-copy-prompt.md`（別ラウンドまたは別 GPT）。**素案のみ**は S6 v4 Part 4

### 7.6 repo 正本と Custom GPT Instructions の差分

- **repo 側**: 上記コミット時点の正本のみ。運用方針の差分はなし（§1〜§5 と整合）。
- **GUI 側**: ChatGPT の Instructions は repo に無いため、オペレータは **本節のコミット**でチェックアウトした `docs/S1-script-refinement-prompt.md`（「LLM への指示」＋入力テンプレ）および S6 の v4 フェンス内全文と **目視突合**し、差分があれば貼り替える（[LANE-B-gui-llm-sync-checklist.md](LANE-B-gui-llm-sync-checklist.md) B-2/B-3）。

### 7.7 実施者

- **repo 機械検証・本節の文書更新**: Cursor エージェント（依頼セッション、2026-04-10）
- **Custom GPT Instructions の突合・貼替**: オペレータ（repo 外 UI）。手順は B-2/B-3 および `gui-llm-setup-guide.md` 方式 A

### 7.8 ファイル2 自己照合（プロンプト同期）

- 当時の「プロンプト同期」観点: **repo が正本**／差分は PR で取り込み／状態は **継続監視**。
- 差し戻し §3 項番3（GUI と repo の食い違いを記録なしに放置）に対し、本節で **参照コミット・機械検証結果・GUI 突合手順**を明示した。

---

## 8. 再検証 2026-04-11（ファイル5 レーンB・Prompt-B）

実施目的: [LANE-B-gui-llm-sync-checklist.md](LANE-B-gui-llm-sync-checklist.md) B-1〜B-5 の維持確認と、旧 Prompt-B（B-2/B-3/B-4/B-5・GPT 構成・repo 正本差分）に沿った証跡更新。

### 8.1 正本参照コミット（repo）

- `git rev-parse HEAD` → `927588eb630bd7b50917085a7e6573436479095f`（短縮 `927588e`）
- 突合対象ファイル: `docs/S1-script-refinement-prompt.md`、`docs/S6-production-memo-prompt.md`（`### v4 プロンプト本体` フェンス内全文）、`docs/S8-thumbnail-copy-prompt.md`

### 8.2 B-1（セットアップ方針）

- [gui-llm-setup-guide.md](../gui-llm-setup-guide.md) を前提とし、§7 からの方針を継続: **方式 A（Custom GPT）**・**2体分離（S1 専用 + S6 v4 専用）**。変更なし。

### 8.3 B-2 機械検証（validate-ir）

```powershell
uv run python -m src.cli.main validate-ir "samples/ir_visual_styles_dry_sample.json" --face-map "samples/face_map.json"
```

- exit code: `0`
- 出力要点: `Validation PASSED`、face 契約表示（prompt/palette/used）確認

### 8.4 B-3 機械検証（apply-production --dry-run）

```powershell
uv run python -m src.cli.main apply-production "samples/test_verify_4_bg_p2_small.ymmp" "samples/p2_bg_anim_small_scope.ir.json" --bg-map "samples/bg_map_p2_small_scope.json" --transition-map "samples/transition_map_p2_small_scope.json" --bg-anim-map "samples/bg_anim_map_p2_small_scope.json" --dry-run
```

- exit code: `0`
- 出力要点: `Timeline adapter: motion=0, transition=4, bg_anim=3` / `BG anim writes: 3` / `Transition VoiceItem writes: 4`（§3・§7 と一致）

### 8.5 B-4 / B-5（運用方針・再掲）

- **B-4**: **会話ごとに brief を台本より先に貼る**（S6 v4 本体の最小化）。参照: `docs/PACKAGING_ORCHESTRATOR_SPEC.md`、`samples/packaging_brief.template.md`
- **B-5**: **H-02 準拠が必要な案件**は `docs/S8-thumbnail-copy-prompt.md`（別ラウンドまたは別 GPT）。**素案のみ**は S6 v4 Part 4

### 8.6 repo 正本と Custom GPT Instructions の差分

- **repo 側**: 上記コミット時点の正本のみ。運用方針の差分はなし（§1〜§5・§7 と整合）。
- **GUI 側**: Instructions は repo に無いため、オペレータは **本節のコミット**でチェックアウトした S1「LLM への指示」＋入力テンプレ、および S6 の v4 フェンス内全文と **目視突合**し、差分があれば貼り替える（[LANE-B-gui-llm-sync-checklist.md](LANE-B-gui-llm-sync-checklist.md) B-2/B-3）。

### 8.7 実施者

- **repo 機械検証・本節の文書更新**: Cursor エージェント（依頼セッション、2026-04-11）
- **Custom GPT Instructions の突合・貼替**: オペレータ（repo 外 UI）

### 8.8 ファイル2 自己照合（プロンプト同期）

- 当時の「プロンプト同期」観点: **継続監視**。本節で参照コミット `927588e` と機械検証を再度固定した。
