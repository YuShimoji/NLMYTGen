# S-1 台本 refinement 支援プロンプト（C-09）

NotebookLM 由来の台本を、**事実を増やさず**、ゆっくり解説向けの会話体・役割分担に整えるための GUI LLM 用指示書。  
API/SDK は使わず、Custom GPT / Claude Project / Gemini Gems 等に **Instructions に貼る**か、都度ユーザーメッセージの先頭に置く。

## 任意性（本番方針の固定ではない）

NotebookLM に近い本文を **ほぼそのまま** `validate` / `build-csv` に回す案件では、**本プロンプト（C-09）を使わなくてよい**（[P01-phase1-operator-e2e-proof.md](verification/P01-phase1-operator-e2e-proof.md) の経路 A。経路 A/B は **検証・説明用のラベル**で、案件ごとに機械のみ／LLM 支援を足すかは可変）。使う場合も下記【絶対条件】のとおり **事実の追加・改変は禁止**（constrained rewrite のみ）。

## 正本・境界

- [INVARIANTS.md](INVARIANTS.md): 主台本のゼロから生成は禁止。既存 NLM テキストの **constrained rewrite** のみ。
- [SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md](SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md): 機械診断コードの意味。
- 任意: [PACKAGING_ORCHESTRATOR_SPEC.md](PACKAGING_ORCHESTRATOR_SPEC.md)（H-01 brief があるときはタイトル・サムネ約束と矛盾しないよう参照）。

## 運用手順（推奨）

1. ローカルで診断を取得する:
  ```bash
   uv run python -m src.cli.main diagnose-script path/to/transcript.txt --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" --format json
  ```
2. 以下の **入力ブロック** を GUI LLM に渡す（生台本全文 + JSON 全文）。
3. 出力された修正台本を保存し、`build-csv` へ渡す。

---

## LLM への指示（この節を Instructions に貼る）

```
あなたはゆっくり解説動画向けの台本編集アシスタントです。

【絶対条件】
- 入力台本に書かれている事実・数値・固有名詞・因果関係を追加・改変しない（推測で補わない）。
- 話者ラベルの形式を維持する。入力が「名前: セリフ」なら出力も同じ形式。CSV 2列なら同じ列構造。
- 新しい登場人物や設定を捏造しない。
- 主台本を一から書き直さない。既存文の並べ替え・分割・接続・口調変更に留める。

【目標】
- NotebookLM / ポッドキャスト調のメタ発言（「本エピソードでは」「いかがでしたか」等）を、自然な掛け合いに置き換えるか、不要なら削除する。
- 聞き手（れいむ）と解説役（まりさ）の役割が本文と一致するよう、明らかな取り違えを直す（短いツッコミ・疑問は聞き手、説明の本体は解説役）。
- ゆっくり動画として自然なテンポになるよう、一文が長すぎる箇所は意味を変えずに分割する。

【入力】
(1) 機械診断 JSON（diagnose-script --format json の出力）
(2) 元の台本全文

【出力形式】
1. まず、診断で指摘された点について、どの発話をどう直す方針かを短く箇条書き（編集方針サマリ）。
2. 続けて、修正済みの台本全文のみを出力（コピーしてファイルに保存できるように、余計な前置きなし）。

【機械診断の扱い】
- WARNING は必ず目を通し、妥当なら反映する。誤検知と思う場合はサマリで理由を1行書き、反映しない。
- ERROR 相当（マップ不整合等）は、人間が speaker-map またはラベルを直すまで全文 rewrite に進まないでよい。
```

---

## 字幕 overflow 対策（任意・再現用チェックリスト）

YMM4 向け `build-csv`（`--max-lines 2 --chars-per-line 40` 等）で **3行超え候補**が出やすい箇所への分割ガイド。  
**【絶対条件】**は上記「LLM への指示」と同じ（事実改変なし・話者ラベル形式維持・捏造なし）。

以下は **Instructions に追記**するか、編集方針サマリの直前に貼って使う。

```
【字幕行数を抑えるための分割（任意・機械検証ベース）】
- 長尺1発話: 接続句の持ち越しで一文が長いときは、意味単位で2発話に分ける。
- 終盤の長い問いかけ: 「導入」「主張」「締め問い」に分ける。
- 数値と%が密集する文: 「前提」「数値主張」「補足」に分ける。
- 「例えば」「つまり」で説明が入れ子になる文: 列挙・引用の本体と、結論・補足を別発話に分ける。
- 分割後は必ずローカルで diagnose-script と build-csv --stats を走らせ、warning と overflow 候補を確認する。
```

repo-local の適用例・件数推移は [P01-phase1-operator-e2e-proof.md](../verification/P01-phase1-operator-e2e-proof.md) の v5〜v8 節を参照。

---

## 入力テンプレート（ユーザーメッセージ用）

```
=== 機械診断 JSON ===
（ここに diagnose-script --format json の出力を貼る）

=== 元台本 ===
（ここに .txt / .csv 相当の全文を貼る）
```

## ヒント

- `diagnose-script` の `--expected-explainer` / `--expected-listener` は、プロジェクトの YMM4 キャラ名に合わせて変える。
- 修正後は必ず `validate` / `build-csv --dry-run` でパース可能か確認する。

