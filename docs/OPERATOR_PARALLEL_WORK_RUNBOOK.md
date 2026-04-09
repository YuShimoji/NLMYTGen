# 並行作業 — オペレータ完全手順

本書は **repo 外（Custom GPT / YMM4 / 素材フォルダ）で並行して進める作業**を、漏れなく実行できるよう手順だけに絞った正本である。コマンドは **リポジトリ root** をカレントにして実行する。OS は Windows（PowerShell）想定。`^` は行継続なので、bash では `\` に読み替える。

---

## 0. 全体の進め方

コード側の G-15〜G-18 は **実装済み**。承認記録・履歴は [FUTURE_DEVELOPMENT_ROADMAP.md](FUTURE_DEVELOPMENT_ROADMAP.md) を参照。今後の新規スライスは FEATURE_REGISTRY で管理する。`docs/verification/` 配下の proof・提案メモの読み方と **仕様の正本チェーン**は [verification/README.md](verification/README.md) を参照。

| トラック  | 内容                                               | いつやるか                 |
| ----- | ------------------------------------------------ | --------------------- |
| **A** | Phase 1（台本診断 → 修正 → CSV）                         | 本編のたび・最優先で価値測定したいとき   |
| **B** | GUI LLM（Custom GPT 等）の Instructions を repo 正本に同期 | プロンプトを変えた直後・初回セットアップ時 |
| **C** | 視覚三スタイル用 YMM4 テンプレ・overlay_map・bg_map            | 演出を増やす前・新規プロジェクト時     |
| **D** | H-01 Packaging brief（任意だが推奨）                     | タイトル／サムネ／台本の約束を揃えたいとき |
| **E** | サムネ 1 枚（S-8）                                     | 公開直前                  |
| **F** | Git（コミット・push）                                   | 作業単位の区切りで             |
| **G** | 保留・素材待ち                                          | 無理に詰めない               |


**A と B は独立**。**C は YMM4 作業時間が取れるとき**。**D は brief を運用するときから**。**E は動画 1 本ごと**。

---

## トラック A — Phase 1 運用 E2E（B-18 → C-09 → build-csv）

詳細の根拠: [verification/P01-phase1-operator-e2e-proof.md](verification/P01-phase1-operator-e2e-proof.md)

### A-1. 機械診断（B-18）

PowerShell:

```powershell
cd "C:\Users\thank\Storage\Media Contents Projects\NLMYTGen"

uv run python -m src.cli.main diagnose-script "samples\AI監視が追い詰める生身の労働.txt" `
  --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" `
  --format json | Out-File -Encoding utf8 _tmp_script_diag.json
```

（自分の台本を使う場合はパスを差し替える。）

GUI の場合: NLMYTGen の「品質診断」→ B-18 → 台本選択 → Speaker Map → Diagnose。JSON をコピーしてファイルに保存してもよい。

### A-2. GUI LLM で台本 refinement（C-09）

1. [S1-script-refinement-prompt.md](S1-script-refinement-prompt.md) を開く。
2. Custom GPT / Claude Project の **Instructions** に、同ファイルの「LLM への指示」相当を含めていることを確認（未設定なら貼り付け）。
3. チャットで **入力テンプレート**に従い、**診断 JSON 全文**と**元台本全文**を貼る。
4. 出力の **修正済み台本全文のみ**を `refined.txt`（名前は任意）に保存。話者ラベル形式を維持する。

### A-3. パース確認と CSV

```powershell
uv run python -m src.cli.main validate refined.txt

uv run python -m src.cli.main build-csv refined.txt -o _tmp_out.csv `
  --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" `
  --max-lines 2 --chars-per-line 40 --reflow-v2 --dry-run
```

`--speaker-map` は台本のラベルに合わせる。問題なければ `--dry-run` を外して本番 CSV を出力する。

### A-4. YMM4 へ

[WORKFLOW.md](WORKFLOW.md) の S-4 以降どおり。CSV を読み込む。

### A-5. 効果記録（任意・推奨）

[P01-phase1-operator-e2e-proof.md](verification/P01-phase1-operator-e2e-proof.md) 末尾の表に 1 行追記するか、[project-context.md](project-context.md) の DECISION LOG に 1 行残す（修正前後の手動時間・感想など）。

---

## トラック B — GUI LLM の正本同期（Custom GPT / Claude 等）

### B-1. セットアップの全体像

手順の型は [gui-llm-setup-guide.md](gui-llm-setup-guide.md) を参照（Custom GPT / Claude Project / Gemini の各方式）。漏れなく同期するチェックリストは [verification/LANE-B-gui-llm-sync-checklist.md](verification/LANE-B-gui-llm-sync-checklist.md)。

### B-2. S-1 台本 refinement 用（C-09）

- 正本: [S1-script-refinement-prompt.md](S1-script-refinement-prompt.md)
- **やること**: リモートの Instructions を、上記ファイルの内容（特に「LLM への指示」と入力テンプレ）と一致させる。repo を更新したら **毎回ここを見比べる**。

### B-3. S-6 演出 IR 用（C-07 v4 / G-05）

- 正本: [S6-production-memo-prompt.md](S6-production-memo-prompt.md) の **「v4: 構造化 IR 出力プロンプト」**ブロック（フェンス内の全文）。
- **やること**:
  1. Custom GPT の **Instructions** を、v4 の「プロンプト本体」で **丸ごと置き換え**（v3 と併用する場合はガイドのとおりモード分岐）。
  2. 追補済みの **「視覚スタイル三種」**節が含まれていることを確認（挿絵コマ / 資料パネル / 再現PV の振り分け）。
- 参照: [VISUAL_STYLE_PRESETS.md](VISUAL_STYLE_PRESETS.md)

### B-4. H-01 を使う場合（任意）

- brief の schema: [PACKAGING_ORCHESTRATOR_SPEC.md](PACKAGING_ORCHESTRATOR_SPEC.md)
- **やること**: 動画 1 本につき brief を 1 ファイル（テキスト）で用意し、**C-07 に台本より先に貼る**（S6 の「### H-01 連携 (推奨)」どおり）。v4 プロンプト本体のフェンス内だけを Instructions に貼った場合、**H-01 連携の説明文はフェンス外**にあるため、**同節を v4 の前に連結して Instructions に含める**か、**会話で毎回 brief を先に貼る**運用で上位制約を満たす。

### B-5. サムネコピー（C-08）

- 正本: [S8-thumbnail-copy-prompt.md](S8-thumbnail-copy-prompt.md)
- 使い分け（v4 Part 4 との差）は [gui-llm-setup-guide.md](gui-llm-setup-guide.md) の「使い方（v4 正本）」および [verification/LANE-B-gui-llm-sync-checklist.md](verification/LANE-B-gui-llm-sync-checklist.md) の B-5。

---

## トラック C — 視覚三スタイル（YMM4・レジストリ）

- 方針の正本: [VISUAL_STYLE_PRESETS.md](VISUAL_STYLE_PRESETS.md)
- **やることのチェックリスト**: [VISUAL_STYLE_YMM4_CHECKLIST.md](VISUAL_STYLE_YMM4_CHECKLIST.md) を上から順にチェックする。
- **overlay のパス例**: [samples/visual_styles_overlay_map.example.json](../samples/visual_styles_overlay_map.example.json) をコピーし、自分の PC の絶対パスに書き換えて `overlay_map.json` 等として保存する。
- **dry 確認用 IR**: `validate-ir samples/ir_visual_styles_dry_sample.json --palette samples/palette.ymmp --overlay-map （自分の overlay_map）`（手順は [verification/VISUAL_STYLES_IR_DRY_SAMPLE.md](verification/VISUAL_STYLES_IR_DRY_SAMPLE.md)）。

`apply-production` / `patch-ymmp` を使う場合は [WORKFLOW.md](WORKFLOW.md) S-6b と CLI ヘルプに従う。

---

## トラック D — H-01 Packaging brief（任意だが推奨）

- 正本: [PACKAGING_ORCHESTRATOR_SPEC.md](PACKAGING_ORCHESTRATOR_SPEC.md)
- **手順の詳細**: 上記 [トラック B の B-4](#b-4-h-01を使う場合任意)（brief 1 本を C-07 より先に渡す運用）。
- **やることの要約**: 動画 1 本につき brief を 1 ファイルで用意し、Custom GPT / 演出 IR 生成の上位制約として使う。
- **今回の 1 本（運用固定）**: `samples/The Amazon Panopticon Surveillance and the Modern Worker.txt` に対して `samples/packaging_brief_p0_nextcycle_amazon.md` を作成済み。C-07 / C-08 ともに **1) brief 全文 → 2) 台本全文** の順で入力する。

---

## トラック E — サムネ 1 枚（S-8）

- 正本: [THUMBNAIL_ONE_SHEET_WORKFLOW.md](THUMBNAIL_ONE_SHEET_WORKFLOW.md)
- 全体フロー: [WORKFLOW.md](WORKFLOW.md) の S-8
- **やること**: テンプレ複製 → 文字・画像差し替え → 書き出し（Python 画像生成は使わない）。

---

## トラック F — Git（ローカル）

作業単位ごとに:

```powershell
cd "C:\Users\thank\Storage\Media Contents Projects\NLMYTGen"
git status
git add -A
git commit -m "（内容を日本語で一文）"
git push
```

（push はリモート方針に合わせる。未準備なら commit のみでもよい。）

---

## トラック G — 今すぐ必須ではないもの


| 項目                                  | 内容                                                                                                                                                                                                                                                               |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **feat/phase2-motion-segmentation** | [verification/P2A-phase2-motion-segmentation-branch-review.md](verification/P2A-phase2-motion-segmentation-branch-review.md) 参照。[verification/P2A-motion-branch-operator-decision.md](verification/P2A-motion-branch-operator-decision.md)。一括マージせず、必要なら別スライスで判断。 |
| **SE / AudioItem**                    | **G-18 実装済み**。[verification/G18-se-audioitem-implementation.md](verification/G18-se-audioitem-implementation.md)。追加 readback が必要なら [verification/P2C-se-audioitem-boundary.md](verification/P2C-se-audioitem-boundary.md)（履歴）。                                                                 |
| **G-15〜G-18**                       | [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) で **`done`**。新規 ID は台帳に登録してから。                                                                                                                                                                                          |
| **H-01 の厳密運用**                      | brief 未使用でもパイプラインは回る。導入するときだけ D を足す。                                                                                                                                                                                                                             |
| **字幕 B-17 残差**                      | 急がない（runtime-state のメンテナンス記載どおり）。                                                                                                                                                                                                                                |


---

## 最短の「週 1 回やるなら」チェックリスト

1. **トラック A** を実台本 1 本で最後まで（YMM4 読込まで）。
2. **トラック B-3** で v4 Instructions が repo と一致しているか確認。
3. 余力があれば **トラック C** のチェックリストを 1 セクションだけ進める。
4. 公開前に **トラック E**（サムネ）。

以上。