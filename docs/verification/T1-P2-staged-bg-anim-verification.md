# P2 背景演出（bg_anim）段階投入 — 機械検証手順（T1）

**スライス**: `T1-P2-DOCSAMPLE`（[CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) §1）  
**目的**: 実案件で `bg_anim` を **1〜2 セクション規模**から載せるときの **validate-ir → apply-production --dry-run** を、repo 固定の入力で再現する。  
**能力マトリクス正本**: [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) の `bg_anim` 行。**本手順は (A) G-14 キーフレーム経路**（`--timeline-profile` なし。ImageItem Layer0 上の X/Y/Zoom）。G-17（VideoEffects + プロファイル）は別手順。

---

## 1. 入力セット（パスは repo root 相対）

| 役割 | パス |
|------|------|
| Micro IR（4 セクション・`bg_anim` 3 種 + `none`） | `samples/p2_bg_anim_small_scope.ir.json` |
| 背景 ImageItem を含む検証用 ymmp | `samples/test_verify_4_bg_p2_small.ymmp` |
| bg ラベル解決 | `samples/bg_map_p2_small_scope.json` |
| G-15 transition 台帳 | `samples/transition_map_p2_small_scope.json` |
| G-17 系ではなく **検証用プレースホルダ**の `bg_anim_map`（ラベル契約の実体は [samples/bg_anim_map_p2_small_scope.json](../../samples/bg_anim_map_p2_small_scope.json)） | `samples/bg_anim_map_p2_small_scope.json` |
| validate-ir 用パレット | `samples/palette.ymmp` |
| 上記一覧のマニフェスト | `samples/p2_staged_bg_anim_verification.bundle.json` |

**注意（bg_map）**: 同梱の `bg_map_p2_small_scope.json` は **開発時の絶対パス**を含む。自分の PC で `apply-production` まで通す場合は、ファイルをコピーし `dark_board` の値を **存在する画像ファイル**に差し替える。`validate-ir` と `--dry-run` のログ再現だけなら、既存サンプルのままでよい。

---

## 2. 手順 A — `validate-ir`（IR ＋パレット）

PowerShell（repo root）:

```powershell
cd "C:\Users\thank\Storage\Media Contents Projects\NLMYTGen"

uv run python -m src.cli.main validate-ir samples/p2_bg_anim_small_scope.ir.json `
  --palette samples/palette.ymmp
```

### 期待（exit code 0）

- 標準出力に `Validation PASSED` を含む（警告は **2 件前後**でよい）。
- `FACE_LATENT_GAP` および `IDLE_FACE_MISSING` が出る構成でも **失敗（exit 2）にならない**ことを確認する。

**期待ログ（抜粋・意味チェック用）**

```text
prompt face contract: ...\docs\S6-production-memo-prompt.md (6 labels)

--- Face Contract ---
  prompt : angry, sad, serious, smile, surprised, thinking
  palette: angry, sad, serious, smile, surprised, thinking

--- Palette Gap Report ---

Validation PASSED with 2 warnings
```

（コンソールのコードページにより人名表示が化ける場合があるが、**PASSED** と **2 warnings** が判別できればよい。）

---

## 3. 手順 B — `apply-production --dry-run`（パッチ影響の数え上げ）

```powershell
uv run python -m src.cli.main apply-production samples/test_verify_4_bg_p2_small.ymmp `
  samples/p2_bg_anim_small_scope.ir.json `
  --bg-map samples/bg_map_p2_small_scope.json `
  --transition-map samples/transition_map_p2_small_scope.json `
  --bg-anim-map samples/bg_anim_map_p2_small_scope.json `
  --dry-run
```

### 期待（exit code 0）

- 標準エラーに `Warning: no --palette or --face-map specified` が出ても **exit code は 0** のまま（本手順は bg / transition / bg_anim の機械カウントが主目的）。
- 次の **数値行**が一致すること（回帰の固定点）。

**期待ログ（抜粋）**

```text
transition_map: samples/transition_map_p2_small_scope.json (2 labels)
bg_anim_map: samples/bg_anim_map_p2_small_scope.json (4 labels)

Timeline adapter: motion=0, transition=4, bg_anim=3
BG removed: 0, BG added: 4
BG anim writes: 3
Transition VoiceItem writes: 4
TachieItem VideoEffects writes: 0
(dry-run: no file written)
```

---

## 4. 手順 C（任意）— YMM4 見え方

`--dry-run` を外し出力 ymmp を得たうえで YMM4 に読み込み、[WORKFLOW.md](../WORKFLOW.md) S-6 に従い **人手で見え方**を確認する。Gate B の運用記録はオペレータ proof 文書へ残す。

---

## 5. 関連ドキュメント

- レーン B の同一コマンド証跡: [LANE-B-execution-record-2026-04-09.md](LANE-B-execution-record-2026-04-09.md) §3 / §7.4  
- production.ymmp 側の契約整理: [P2B-production-timeline-contract-profile.md](P2B-production-timeline-contract-profile.md)

---

*2026-04-11: T1-P2-DOCSAMPLE として追加。*
