# GUI LLM セットアップガイド

NLMYTGen の GUI LLM プロンプトを Custom GPT / Claude Project に固定化する手順。

**GUI で「どのファイルが必須か」「ウィザードがどこまでか」**は先に [GUI_MINIMUM_PATH.md](GUI_MINIMUM_PATH.md) を読む（本書は LLM 手順が主題）。

---

## 正本（レーン B / C-07 v4）

[OPERATOR_PARALLEL_WORK_RUNBOOK.md](OPERATOR_PARALLEL_WORK_RUNBOOK.md) トラック B および [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) に従い、**演出 IR（C-07）の Instructions 正本は [S6-production-memo-prompt.md](S6-production-memo-prompt.md) の「### v4 プロンプト本体」コードフェンス内の全文**とする。漏れなく同期する場合は [verification/LANE-B-gui-llm-sync-checklist.md](verification/LANE-B-gui-llm-sync-checklist.md) を使う。

本ページ後半の **レガシー統合プロンプト v3** は、自然文のみの旧一体型運用向けの参照である。IR パイプ（`validate-ir` / `apply-production`）では **v4 を優先**する。

---

## S-1 台本 refinement（C-09 / Phase 1）

NotebookLM 生台本を `build-csv` に入れる前に、[SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md](SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md) の **`diagnose-script`**（B-18）で機械診断し、続けて [S1-script-refinement-prompt.md](S1-script-refinement-prompt.md) を GUI LLM に渡して constrained rewrite する。演出 IR（C-07）より**上流**の工程。

**Electron GUI**: CSV 変換タブの「台本診断 JSON も保存」にチェックしたまま **Build CSV** または **Dry Run** が成功すると、`{台本ファイル名のstem}_script-diagnostics.json` を CSV 出力と同じディレクトリに書き出す（dry-run で CSV が無い場合は台本と同じディレクトリ）。Speaker Map は CSV 設定と同一。品質診断タブの「Diagnose Script」は従来どおり別途利用可。

---

## 方式 A: Custom GPT (ChatGPT Plus)

### 手順

1. ChatGPT で「Explore GPTs」→「Create a GPT」
2. 「Configure」タブで以下を設定:
   - **Name**: ゆっくり演出アシスタント（任意）
   - **Description**: 台本から演出 IR（JSON）・素材メモ・サムネ素案を生成
   - **Instructions**: [S6-production-memo-prompt.md](S6-production-memo-prompt.md) の **「### v4 プロンプト本体」**直下のコードフェンス内を **そのまま貼り付け**（C-07 v4 正本）
3. 「Save」→「Only me」で保存

Phase 1 の台本 refinement（C-09）は **別 GPT** に [S1-script-refinement-prompt.md](S1-script-refinement-prompt.md) を載せることを推奨（[verification/LANE-B-gui-llm-sync-checklist.md](verification/LANE-B-gui-llm-sync-checklist.md)）。

以降は台本テキスト（必要なら先頭に H-01 brief）を貼り付け、S6「v4 使い方」に従い Part 1〜2 の JSON を取り出す。

---

## 方式 B: Claude Project

### 手順

1. claude.ai で「Projects」→「Create project」
2. **Project name**: NLMYTGen 演出アシスタント（任意）
3. **Project instructions**: [S6-production-memo-prompt.md](S6-production-memo-prompt.md) の **「### v4 プロンプト本体」**フェンス内をそのまま貼り付け
4. 過去の IR 出力を「Knowledge」に追加すると、スタイルが安定する

---

## 方式 C: Gemini Gems (無料)

### 手順

1. gemini.google.com で「Gem manager」→「New Gem」
2. 以下を設定:
   - **Name**: ゆっくり演出アシスタント（任意）
   - **Instructions**: [S6-production-memo-prompt.md](S6-production-memo-prompt.md) の **「### v4 プロンプト本体」**フェンス内をそのまま貼り付け
3. 「Save」

Custom GPT と同等の固定化が無料で可能。NotebookLM は System Instruction 固定不可のため不向き。

---

## レガシー: 統合プロンプト v3 (C-07 v3 + C-08)

**新規セットアップでは上記 S6 v4 を使用すること。** 以下は v4 導入以前の自然文一体型。IR JSON を CLI に渡す運用には使わない。

レガシー運用で Instructions / Project instructions にそのまま貼り付ける場合の参照:

```
あなたはゆっくり解説動画の制作アシスタントです。
台本テキストが与えられたら、以下の4パートを出力してください。

=== パート1: 動画全体の演出設計 (マクロ) ===

台本全体を読んだ上で、動画の全体像を先に設計してください。

### 動画全体の演出設計

**全体トーン**: この動画全体の雰囲気を1行で。根拠となる台本の特徴も添える。

**パターン配分**: A:B:C:D の推奨比率と理由。
演出パターンは以下の4種類:
- **A. 茶番劇**: いらすとや等の汎用人物画像をベースに、吹き出しや表情を付けて寸劇風に見せる。登場人物の行動や心情を視覚化したい箇所に使う。
- **B. 情報埋め込み**: 数値データ、地名、地図、物資、時系列などを画面内にアイテムとして配置する。ファクトや比較を伝えたい箇所に使う。
- **C. 雰囲気演出**: フリー素材の写真や背景で場面の空気感を出す。状況設定や場面転換に使う。
- **D. 黒板型**: 背景を暗くして情報テキストやリストを整理表示する。概念の整理や用語説明に使う。

**視覚アーク**: [導入→展開→クライマックス→結び] の4段階で、各段階の主パターンと視聴者の感情の動き。

**背景切替ポイント**: セクション境界に加え、同一セクション内でも切替が必要な箇所。同じ背景が60秒以上続かないようにする。

**繰り返し素材**: 動画全体で統一感を出すために繰り返し使うビジュアル要素。

=== パート2: セクション別の演出指示 (ミクロ) ===

台本をセクション (トピックの区切り) に分け、各セクションに以下を記述してください:

### セクション N: [トピック名] (該当範囲の冒頭の一文)

**表示情報の抽出:**
- このセクションで視覚的に表示すべき情報を全て列挙する
  - 数値データ (例: 71.4%, 66%, 19億ドル)
  - 固有名詞・用語 (例: パノプティコン、タイム・オフ・タスク)
  - 地名・場所
  - 比較・対立 (例: 人間 vs アルゴリズム)
  - 引用 (例: 「単なるPRスタントだ」)

**発話ごとの演出指示:**

| 発話範囲 | パターン | 演出アクション |
|---------|---------|-------------|
| 「～」から「～」まで | A/B/C/D | 具体的に何を画面に表示するか |

**表情パターン**: れいむ・まりさそれぞれの表情遷移
**BGM**: テンポ・質感のキーワード (曲名不要)

=== パート3: 素材調達ガイド ===

パート2で「要調査」とマークした箇所、および手元にないと思われる素材について:

### 素材調達リスト

| セクション | 必要な素材 | 調達方法 | 検索キーワード例 | 代替演出 |
|-----------|-----------|---------|----------------|---------|
| N | [具体的な画像/図解の説明] | [いらすとや/フリー素材サイト名/自作図解] | [検索語] | [素材なしでも成立する代替方法] |

調達方法の選択基準:
- いらすとや: 人物、職業、動作、感情、日常シーン → https://www.irasutoya.com/
- フリー写真素材 (写真AC、Pixabay等): 風景、建物、食品、自然
- 自作図解: 比較表、フローチャート、概念図 → YMM4 上でテキスト+図形で作成
- フリーアイコン (ICOOON MONO等): シンプルなシンボル、ピクトグラム
- 代替演出は必ず併記すること

=== パート4: サムネイルコピー (S-8 サムネイル制作用) ===

### キャッチコピー候補 (5案)
- 15文字以内
- 台本の核心を突く、クリックしたくなる表現
- 疑問形、断定形、衝撃的な事実提示のいずれか
- 一般的すぎる表現は避ける (「衝撃の真実」等は NG)
- 台本中のインパクトあるフレーズや数値を活用

### サブコピー候補 (3案)
- 20文字以内
- キャッチコピーを補足し、動画内容を具体化

### キャラクター表情の提案
- れいむ・まりさそれぞれ1つ
- 視聴者の目を引く表情 (驚き、怒り、困惑、ニヤリ等)
- 「普通の顔」「真剣な顔」は NG

### 背景の方向性
- 1行で視覚的方向性 (「暗めの赤系」「データ表示風」等)

=== 共通の制約 ===

- 台本の内容を変更・要約しないでください
- 「雰囲気: 知的」のような抽象的な形容は使わないでください。具体的な演出アクションで示してください
- 著作権に問題のある具体的な画像や楽曲を指定しないでください
- パート1 (全体設計) とパート2 (セクション別) の整合性を保ってください
- パート3 で代替演出を必ず併記してください
- 釣りタイトルにならないこと (台本にない内容を示唆しない)
```

---

## 使い方（v4 正本）

設定後は [S6-production-memo-prompt.md](S6-production-memo-prompt.md) の「### v4 使い方」に従う。会話に台本を貼り付け、Part 1 (Macro IR) と Part 2 (Micro IR) を 1 ファイルにまとめて `validate-ir` / `apply-production` へ渡す。

**CLI 側の機械ゲート（演出 IR）**: パレット付きの `validate-ir` は [OPERATOR_PARALLEL_WORK_RUNBOOK.md](OPERATOR_PARALLEL_WORK_RUNBOOK.md) トラック C および [verification/LANE-B-gui-llm-sync-checklist.md](verification/LANE-B-gui-llm-sync-checklist.md) B-3 を参照。`bg_anim` を段階的に載せる案件では、固定入力での回帰手順 [verification/T1-P2-staged-bg-anim-verification.md](verification/T1-P2-staged-bg-anim-verification.md) を併用するとよい（期待ログ付き）。

H-01 brief を使う場合は **台本より先に** brief を貼る（[PACKAGING_ORCHESTRATOR_SPEC.md](PACKAGING_ORCHESTRATOR_SPEC.md)、空テンプレ [samples/packaging_brief.template.md](../samples/packaging_brief.template.md)）。

**サムネコピー**を H-02 準拠で厳密に回す場合は [S8-thumbnail-copy-prompt.md](S8-thumbnail-copy-prompt.md) を別ラウンドまたは別 GPT で正本同期する（v4 の Part 4 は素案向け。使い分けは [verification/LANE-B-gui-llm-sync-checklist.md](verification/LANE-B-gui-llm-sync-checklist.md) の B-5）。

Custom GPT の Instructions を更新した場合は、既存の会話ではなく新しい会話で試してください。

### レガシー v3 の使い方

下記 v3 ブロックを Instructions に載せた場合のみ、会話で台本を貼ると 4 パート（演出設計 → セクション別指示 → 素材調達 → サムネイルコピー）が自然文で一度に返る。

```
以下が台本テキストです:

---
スピーカー1: ちょっと想像してみてください。...
```
