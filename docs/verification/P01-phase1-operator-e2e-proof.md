# P-01 — Phase 1 運用 E2E 手順（オペレータ向け）

Phase 1（B-18 + C-09）を **1 本の台本**で通すための再現手順。GUI LLM 上の実編集は人間作業のため、ここでは **CLI まで機械再現可能な部分**を正本とする。

## 前提

- リポジトリ root で [uv](https://github.com/astral-sh/uv) が使えること。
- 台本が `normalize` で読める `.txt` または `.csv` であること。

## 手順

### 1. 機械診断（B-18）

```bash
uv run python -m src.cli.main diagnose-script "samples/AI監視が追い詰める生身の労働.txt" ^
  --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" ^
  --format json > _tmp_script_diag.json
```

（PowerShell 以外では `^` を `\` に読み替える。）

- **text** 表示にする場合は `--format text`（省略可）。
- GUI の場合: 「品質診断」タブ → B-18 台本診断 → 台本選択 → Speaker Map 入力 → Diagnose Script。

### 2. GUI LLM（C-09）

1. [S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md) の **LLM への指示**を Custom GPT / Claude Project 等の Instructions に含める。
2. 同ファイルの **入力テンプレート**に、`_tmp_script_diag.json` の内容と **元台本全文**を貼る。
3. 出力の **修正済み台本全文**だけを `refined.txt` 等に保存する（話者ラベル形式を維持）。

### 3. パース確認と CSV（build-csv）

```bash
uv run python -m src.cli.main validate refined.txt
uv run python -m src.cli.main build-csv refined.txt -o _tmp_out.csv ^
  --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" ^
  --max-lines 2 --chars-per-line 40 --reflow-v2 --dry-run
```

（`refined.txt` が元と同じラベルなら `--speaker-map` は実ラベルに合わせる。）

### 4. 効果の記録（任意）

- 修正前後の **手動編集時間**（分）と、**IR 生成時の曖昧さ**（主観メモ）を 1 行でも残す。
- 追記先の例: 本ファイル末尾「記録」、または `project-context.md` の DECISION LOG。

## repo-local 機械確認（2026-04-06 時点）

以下は **C-09 を除く**自動ステップのスモークとして実行済み（開発時）:

- `diagnose-script` on `samples/AI監視が追い詰める生身の労働.txt` → JSON 正常終了（exit 0）。診断内容は [B18-script-diagnostics-ai-monitoring-sample.md](B18-script-diagnostics-ai-monitoring-sample.md) と同型。
- `build-csv` on 上記サンプル（未 refinement）→ 既存パイプラインどおり CSV 生成可能（E2E の「refined 稿」は人間または LLM 出力待ち）。

### ロードマップ実装スライス（2026-04-06）

将来開発プラン（repo: [FUTURE_DEVELOPMENT_ROADMAP.md](../FUTURE_DEVELOPMENT_ROADMAP.md)）に沿い、同サンプルで **CLI 部分を再実行**（exit 0）:

- `diagnose-script` … `--format json`
- `validate` … `OK: 28 utterances parsed`（既知 WARN: row 10 長文）
- `build-csv` … `--dry-run`、111 行相当プレビュー

**C-09（GUI LLM refinement）は未実施**のため、本スライスは「機械パス」の記録に留まる。人間＋ LLM で refined 稿まで進めたら、上表に別行で追記する。

## 記録

### v5 overflow 実害カテゴリ固定（T1/T2）

- 対象カテゴリ: **文末接続句の持ち越しを含む長尺1発話**
- 選定理由: overflow件数 25件の中でも、YMM4上での手修正が「1発話の再分割」になりやすく、編集コストが高い。
- 最小改善: C-09 側で 1 発話を 2 発話に分割（`samples/v5_overflow_minfix_refined.txt`）。

before/after（代表例）:

- before: `今日はリスナーのあなたが私たちに送ってくれたあの膨大なレポートとデータの山を徹底的に解剖していくディープダイブです。あなたが集めてくれたこのリソース本当に素晴らしい視点に溢れていましたよね。`
- after-1: `今日はリスナーのあなたが送ってくれたレポートとデータを徹底解剖するディープダイブです。`
- after-2: `あなたが集めてくれたこのリソース、本当に素晴らしい視点に溢れていましたよね。`

- 計測結果: `samples/v5_t2_diag.json`（warning 0件維持）、`samples/v5_t2_build.txt`（overflow候補 25件は同数、ただし対象発話の実害度は低下）。

### v6 overflow 純減トライ（T1/T2）

- 対象カテゴリ: **文末接続句の持ち越しを含む長尺終盤問いかけ**
- 対象行（v5基準）: row 313 / row 317 / row 356
- 選定理由: 終盤の長尺問いかけは視認負荷と手修正コストが高く、短文化ルールの効果を出しやすい。
- 導入ルール（C-09短文化）: 長尺1発話を「導入文」「主張文」「締め問い」に分割。
- 反映ファイル: `samples/v6_overflow_reduction_refined.txt`
- 計測結果: `samples/v6_t2_diag.json`（warning 0件維持）、`samples/v6_t2_build.txt`（overflow候補 **25→22** に純減）。

### v7 overflow 横展開（T1/T2）

- 対象カテゴリ: **数値+記号混在（% / 数値レンジ）**
- 対象行（v6基準）: row 212 / row 267 / row 9
- 選定理由: 数値句が密な長文は、短文化ルールの再現性を検証しやすく、実制作での視認負荷も高い。
- 横展開ルール: 数値句を含む長文を「前提」「数値主張」「補足」に分割。
- 反映ファイル: `samples/v7_cross_category_refined.txt`
- 計測結果: `samples/v7_t2_diag.json`（warning 0件維持）、`samples/v7_t2_build.txt`（overflow候補 **22→21** に純減）。

### v8 引用句長文化（例えば列挙）横展開（T1/T2）

- 対象カテゴリ: **引用句長文化（例えば列挙・つまり説明の入れ子）**
- 対象行（v7基準）: row 152 / row 154 / row 211（overflow候補に含まれる長尺説明に対応）
- 選定理由: 「例えば」「つまり」で説明が入れ子になると1行の表示幅が膨らみ、YMM4字幕の手修正が増えやすい。
- 横展開ルール: **引用・列挙本体**と**補足・結論句**を別発話に分割する。
- 反映ファイル: `samples/v8_quote_split_refined.txt`
- 計測結果: `samples/v8_t2_diag.json`（warning 0件維持）、`samples/v8_t2_build.txt`（overflow候補 **21→20** に純減）。

### v9 C-09 短文化チェックリスト草案（T1）

v5〜v8 の検証から抽出した **再現用ルール**（意味改変なし・話者ラベル維持が前提）。正本は [docs/S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md) の「字幕overflow対策」節に追記する。

- **長尺1発話の2分割**: 接続句で背伸びした一文は、意味単位で2発話に分ける（v5）。
- **終盤長尺問いかけの3分割**: 「導入」「主張」「締め問い」に分ける（v6）。
- **数値+%密集文の分割**: 「前提」「数値主張」「補足」に分ける（v7）。
- **例えば/つまり入れ子の分割**: 列挙本体と結論・補足を別発話にする（v8）。
- **分割後の確認**: `diagnose-script` で warning を確認し、`build-csv --stats` で overflow 候補の増減を見る。

### v10 否定対比＋地理断定の分離（T1/T2）

- 対象カテゴリ: **フィクション否定と地理・現実断定の同一発話パック**
- 代表行（v9 `build-csv --stats` 基準）: **row 9**（まりさ、`display_width=82`、当時の WARN 一覧で最大）
- 選定理由: v5（接続句長尺）/ v6（終盤問いかけ）/ v7（数値密集）/ v8（例えば・つまり入れ子）のラベルでは切りにくい「Not フィクション＋どこで何が起きているか」の**説明ラッパー**を1型として固定する。
- 短文化ルール: **否定対比フレーム**（〜ではなくって）と**地理＋現実断定**（現在の〜で〜している）を別発話に分ける（意味・事実は変えない）。
- 反映ファイル: `samples/v10_contrast_split_refined.txt`
- 計測結果: `samples/v10_t3_diag.json`（warning 0件維持）、`samples/v10_t3_build.txt`（overflow候補 **20→19** に純減。v9 基準 row 9 / display_width 82 のブロックを解消）。

### v11 因果帰結チェーン＋締め問いの分離（T1/T2）

- 対象カテゴリ: **「常識→帰結→政治リスク」までを一発話に詰めた長尺**
- 代表行（v10 `build-csv --stats` 基準）: **row 216**（れいむ、`display_width=80`、当時の WARN 一覧で最大帯。同一発話が reflow で row 216–217 に跨ぐ塊）
- v10 との差: v10 が **否定対比＋地理断定**だったのに対し、こちらは **因果の畳みかけと締めの問いかけ**が1つに繋がった型（S1 の「終盤問いかけ3分割」に近いが、**中盤の修辞**として独立記録）。
- 短文化ルール: **帰結に至るまで**（〜となって）と**締めの問い**（〜んじゃないですか?）を別発話に分ける。
- 反映ファイル: `samples/v11_chain_split_refined.txt`
- 計測結果: `samples/v11_t3_diag.json`（warning 0件維持）、`samples/v11_t3_build.txt`（overflow候補 **19→18** に純減。v10 基準 row 216 付近の最大幅ブロックを解消）。

### v12 メタ評価＋比喩フレーズ＋総括ラベルの分離（T1/T2）

- 対象カテゴリ: **反応語＋比喩までの塊と、総括ラベル（〜ですよね）の一発話詰め**
- 代表行（v11 `build-csv --stats` 基準）: **row 272**（れいむ、`display_width=80`、当時の WARN 一覧で最大）
- v10/v11 との差: v10 は **否定対比＋地理**、v11 は **因果チェーン＋締め問い**。こちらは **比喩（起爆剤）までの評価**と **総括ラベル（パラダイムシフト）**が1行に重なった型。
- 短文化ルール: **比喩・評価まで**と**締めの総括ラベル**を別発話に分ける。
- 反映ファイル: `samples/v12_meta_eval_split_refined.txt`
- 計測結果: `samples/v12_t3_diag.json`（warning 0件維持）、`samples/v12_t3_build.txt`（overflow候補 **18→17** に純減。v11 基準 row 272 / display_width 80 のブロックを解消）。

### v13 比喩定義（OS）＋ミッション目的句の分離（T1/T2）

- 対象カテゴリ: **具体例列挙→比喩定義（OS）→抽出目的までを一発話に詰めた長尺**
- 代表行（v12 `build-csv --stats` 基準）: **row 22**（れいむ、`display_width=76`、当時の WARN 一覧で最大）
- v10〜v12 との差: 否定対比／因果問い／メタ評価総括ではなく、**聞き手の行動例＋「世界経済の OS」比喩＋「変化を抽出」目的**が連なる型。
- 短文化ルール: **具体例の塊**／**比喩・書き換えの問いかけ**／**抽出目的の宣言**に分け、必要なら **3 発話**まで許容する（意味不変）。
- 反映ファイル: `samples/v13_os_mission_split_refined.txt`
- 参考（v12 時点の実害トップ3, `display_width` 降順）: row **22** / れいむ / **76**；row **79** / れいむ / **74**；row **155** / れいむ / **74**。
- 計測結果: `samples/v13_t3_diag.json`（warning 0件維持）、`samples/v13_t3_build.txt`（overflow候補 **18→17** に純減。同一ミッション宣言を **3発話**に分割し、v12 基準の最大幅帯を解消。364 rows）。

### v14 感想メタ＋造語ラベル英語部の分離（T1/T2）

- 対象カテゴリ: **主観感想の畳みかけと、造語・英語ラベル（固有名詞的フレーズ）を同一発話に詰めた長尺**
- 代表行（v13 `build-csv --stats` 基準）: **row 80**（れいむ、`display_width=74`、当時の WARN 一覧で最大帯。row 156 も同幅だが本サイクルでは片方を代表に固定）
- v10〜v13 との差: 否定対比／因果問い／メタ評価総括／OS ミッション／ドル比喩総括ではなく、**レポート読後の比喩ラベル（日本語部と英語部）**の境目で分割する型。
- 短文化ルール: **日本語の造語ラベルまで**と**英語タイトル風フレーズ＋締め**を別発話に分ける。
- 反映ファイル: `samples/v14_timing_label_split_refined.txt`
- 計測結果: `samples/v14_t3_diag.json`（warning 0件維持）、`samples/v14_t3_build.txt`（`build-csv --stats` の [WARN] 行数 **17→16**、365 rows。v13 基準 row 80 帯を解消）。

| 日付 | 台本 | refined 使用 | 接続判定 | メモ |
|------|------|--------------|----------|------|
| 2026-04-06 | samples/AI監視が追い詰める生身の労働.txt | 未（C-09 未実施） | PASS（CLI） | ロードマップ手順: CLI のみ再スモーク exit 0。refined 稿での E2E は運用者待ち |
| 2026-04-08 | samples/AI監視が追い詰める生身の労働.txt | 未（C-09 未実施） | B-11 途中（改行 Pass / 辞書 0） | B-11 実測パック途中。プラン直前準備は [B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md)（§2 取込後の数値埋め → §3 Gate）。並行で P2 背景アニメは `test_verify_4_bg.ymmp` 経由で YMM4 見え方確認。 |
| 2026-04-09 | samples/AI監視が追い詰める生身の労働.txt | 未（B-11 は生台本→CSV 経路） | PASS（CLI）／B-11 記録参照 | レーン A 準備: repo root で `diagnose-script` と `build-csv --stats` を再実行し CSV 111 行を再生成。B-11 の §5 体裁・代表例・§3 は同ファイル（先頭の検証範囲注記を参照）。フル A（C-09 介在）は別行で追記。 |
| 2026-04-07 | samples/The Amazon Panopticon Surveillance and the Modern Worker.txt | 未（C-09 未実施） | PASS（CLI） | P0 実行: `diagnose-script --unlabeled --format json` -> `samples/p0_phase1_amazon_diag.json`、`validate --unlabeled` -> `samples/p0_phase1_amazon_validate.txt`、`build-csv --unlabeled --max-lines 2 --chars-per-line 40 --reflow-v2 --stats` -> `samples/p0_phase1_amazon_ymm4.csv`。結果: 232 rows、overflow 候補 19 行。 |
| 2026-04-07 | samples/石油消失で書き換わる世界経済のOS.txt | 未（C-09 未実施） | PASS（CLI） | N1 実行: `diagnose-script --speaker-map-file samples/n1_host_speaker_map.json --format json` -> `samples/n1_oil_diag.json`、`validate` -> `samples/n1_oil_validate.txt`、`build-csv --speaker-map-file samples/n1_host_speaker_map.json --max-lines 2 --chars-per-line 40 --reflow-v2 --stats` -> `samples/n1_oil_ymm4.csv`。結果: 358 rows、overflow 候補 25 行（前回 Amazon 19 行より多い）。 |
| 2026-04-07 (`onepass_2026-04-07_c`) | samples/石油消失で書き換わる世界経済のOS.txt | 簡易（C-09 は原稿維持でワンパス接続確認） | PASS（One-Pass） | `diagnose-script` -> `samples/onepass_2026-04-07_c_diag.json`、`validate` -> `samples/onepass_2026-04-07_c_validate.txt`、`build-csv` -> `samples/onepass_2026-04-07_c_ymm4.csv`。結果: 358 rows、overflow 候補 25 行。 |
| 2026-04-08 (`s1_c09_live_2026-04-08_a`) | samples/s1_c09_live_refined.txt | 実投入（C-09 運用反映） | PASS（差分確認） | `diagnose-script` 比較: before=`samples/onepass_2026-04-07_c_diag.json`（warning 2件）, after=`samples/s1_c09_live_diag_before.json`（warning 0件）。`build-csv`=`samples/s1_c09_live_ymm4.csv`（358 rows, overflow 候補 25 行）。 |
| 2026-04-08 (`r1_c09_delta_2026-04-08_b`) | samples/r1_c09_delta_refined.txt | 実投入（C-09 差分追記） | PASS（差分維持） | `diagnose-script`=`samples/r1_c09_delta_diag.json`（warning 0件）、`build-csv`=`samples/r1_c09_delta_ymm4.csv`（358 rows, overflow 候補 25 行）。前run（`s1_c09_live_2026-04-08_a`）と同水準を維持。 |
| 2026-04-08 (`t3_c09_keep_2026-04-08_c`) | samples/t3_c09_keep_refined.txt | 実投入（継続確認） | PASS（差分維持） | `diagnose-script`=`samples/t3_c09_keep_diag.json`（warning 0件）、`build-csv`=`samples/t3_c09_keep_ymm4.csv`（358 rows, overflow 候補 25 行）。C-09 運用差分は維持。 |
| 2026-04-08 (`t3_c09_keep_v4_2026-04-08_d`) | samples/t3_c09_keep_v4_refined.txt | 実投入（継続確認） | PASS（差分維持） | `diagnose-script`=`samples/t3_c09_keep_v4_diag.json`（warning 0件）、`build-csv`=`samples/t3_c09_keep_v4_ymm4.csv`（358 rows, overflow 候補 25 行）。前run と同水準を維持。 |
| 2026-04-08 (`v5_t3_keep_2026-04-08_e`) | samples/v5_t3_keep_refined.txt | 実投入（継続確認） | PASS（差分維持） | `diagnose-script`=`samples/v5_t3_diag.json`（warning 0件）、`build-csv`=`samples/v5_t3_ymm4.csv`（358 rows, overflow 候補 25 行）。v5 の最小改善後も接続安定を維持。 |
| 2026-04-08 (`v6_t3_keep_2026-04-08_f`) | samples/v6_t3_keep_refined.txt | 実投入（純減後の継続確認） | PASS（差分改善） | `diagnose-script`=`samples/v6_t3_diag.json`（warning 0件）、`build-csv`=`samples/v6_t3_ymm4.csv`（357 rows, overflow 候補 22 行）。v5 比で 3 件純減。 |
| 2026-04-08 (`v7_t3_keep_2026-04-08_g`) | samples/v7_t3_keep_refined.txt | 実投入（横展開後の継続確認） | PASS（差分改善） | `diagnose-script`=`samples/v7_t3_diag.json`（warning 0件）、`build-csv`=`samples/v7_t3_ymm4.csv`（356 rows, overflow 候補 21 行）。v6 比で 1 件純減。 |
| 2026-04-08 (`v8_t3_keep_2026-04-08_h`) | samples/v8_t3_keep_refined.txt | 実投入（引用句カテゴリ横展開後） | PASS（差分改善） | `diagnose-script`=`samples/v8_t3_diag.json`（warning 0件）、`build-csv`=`samples/v8_t3_ymm4.csv`（360 rows, overflow 候補 20 行）。v7 比で 1 件純減。 |
| 2026-04-09 (`v9_t3_smoke_local_2026-04-09_a`) | samples/v8_t3_keep_refined.txt | 実投入（S1 チェックリスト追記後の機械再確認） | PASS（ドキュメント変更の非影響） | `diagnose-script`=`samples/v9_t3_smoke_diag.json`（warning 0件）、`build-csv`=`samples/v9_t3_smoke_ymm4.csv`（360 rows, overflow 候補 20 行）。コード・CLI 挙動は v8 継続確認と同水準。 |
| 2026-04-09 (`v10_t3_contrast_split_2026-04-09_a`) | samples/v10_contrast_split_refined.txt | 実投入（v10 否定対比＋地理断定の1分割） | PASS（差分改善） | `diagnose-script`=`samples/v10_t3_diag.json`（warning 0件）、`build-csv`=`samples/v10_t3_ymm4.csv`（361 rows, overflow 候補 19 行）。v9 比で 1 件純減。 |
| 2026-04-10 (`v11_t3_chain_split_2026-04-10_a`) | samples/v11_chain_split_refined.txt | 実投入（v11 因果帰結＋締め問いの1分割） | PASS（差分改善） | `diagnose-script`=`samples/v11_t3_diag.json`（warning 0件）、`build-csv`=`samples/v11_t3_ymm4.csv`（362 rows, overflow 候補 18 行）。v10 比で 1 件純減。 |
| 2026-04-11 (`v12_t3_meta_eval_2026-04-11_a`) | samples/v12_meta_eval_split_refined.txt | 実投入（v12 メタ評価＋比喩と総括ラベルの1分割） | PASS（差分改善） | `diagnose-script`=`samples/v12_t3_diag.json`（warning 0件）、`build-csv`=`samples/v12_t3_ymm4.csv`（363 rows, overflow 候補 17 行）。v11 比で 1 件純減。 |
| 2026-04-12 (`v13_t3_os_mission_2026-04-12_a`) | samples/v13_os_mission_split_refined.txt | 実投入（v13 OS比喩＋ミッション目的の3分割） | PASS（差分改善） | `diagnose-script`=`samples/v13_t3_diag.json`（warning 0件）、`build-csv`=`samples/v13_t3_ymm4.csv`（364 rows。`build-csv --stats` の [WARN] 行数 **18→17**、v12 同条件比）。 |
| 2026-04-13 (`v14_t3_timing_label_2026-04-13_a`) | samples/v14_timing_label_split_refined.txt | 実投入（v14 感想メタ＋造語／英語ラベルの分割） | PASS（差分改善） | `diagnose-script`=`samples/v14_t3_diag.json`（warning 0件）、`build-csv`=`samples/v14_t3_ymm4.csv`（365 rows。[WARN] **17→16**）。 |
| 2026-04-09（レーン C・台本非依存） | — | — | PASS（CLI） | レーン C 準備クローズ: `validate-ir samples/ir_visual_styles_dry_sample.json` + `apply-production … --dry-run`、記録 [LANE-C-operator-prep-2026-04-09.md](LANE-C-operator-prep-2026-04-09.md)。演出パイプの実機系は `runtime-state.md` Evidence（2026-04-05 YMM4）と整合。YMM4 テンプレ実作業は案件開始時に [VISUAL_STYLE_YMM4_CHECKLIST.md](../VISUAL_STYLE_YMM4_CHECKLIST.md)。 |
| （運用者が追記） | | | | |
