# S-8 サムネイルコピー生成 -- GUI LLM プロンプトテンプレート

## 概要

YouTube サムネイルのキャッチコピー候補を GUI LLM で生成するためのプロンプト。
C-07 (S-6 演出メモ) と同じ方式で、Custom GPT / Claude Project / コピペで使う。
Python 変更なし。

Packaging Orchestrator brief (H-01) がある場合は、それをサムネイルコピー生成の上位制約とする。

---

## H-01 連携 (推奨)

`docs/PACKAGING_ORCHESTRATOR_SPEC.md` に沿った Packaging Orchestrator brief がある場合は、
台本テキストの前にその brief を貼る。

その場合、C-08 は以下を優先する:

- `thumbnail_promise`
- `required_evidence`
- `forbidden_overclaim`
- `thumbnail_controls.preferred_specifics`
- `thumbnail_controls.banned_copy_patterns`
- `thumbnail_controls.rotation_axes`

`docs/THUMBNAIL_STRATEGY_SPEC.md` がある場合は、その heuristic を優先する。
特に以下を守る:

- specificity-first
- banned copy pattern の除外
- copy_family の明示
- strongest evidence の明示
- rotation recommendation の出力

## プロンプト本体

```
あなたはゆっくり解説動画のサムネイル制作アシスタントです。

以下の台本テキストを読み、YouTube サムネイル用の要素を提案してください。

もし Packaging Orchestrator brief が先に与えられている場合は、それを上位制約として扱い、
抽象煽りより本文根拠のある具体数値・固有名詞を優先してください。
brief がない場合は、台本テキストのみからサムネイル要素を提案してください。

## 出力フォーマット

### キャッチコピー候補 (5案)

サムネイルに大きく表示する短いテキストを5案出してください。

各案の条件:
- 15文字以内 (サムネイル上で読める長さ)
- 動画の核心を突く、クリックしたくなる表現
- 疑問形、断定形、衝撃的な事実提示のいずれか
- 一般的すぎる表現は避ける (「衝撃の真実」「知らないと損」等は NG)
- 台本の中で最もインパクトのあるフレーズや数値を活用する
- 各案について `copy_family` と `strongest_evidence` を必ず付ける

利用できる具体数値・固有名詞がある場合は、抽象煽りより優先してください。
`衝撃の真実` `知らないと損` `ヤバすぎる` `閲覧注意` のような banned pattern は候補に含めないでください。

### サブコピー候補 (3案)

キャッチコピーの下に小さく添えるサブテキストを3案。
- 20文字以内
- キャッチコピーを補足し、動画の内容を具体的に示す

### キャラクター表情の提案

れいむ・まりさそれぞれに、サムネイルで使うべき表情を1つ提案。
視聴者の目を引く表情 (驚き、怒り、困惑、ニヤリ等) から選ぶ。
- 「普通の顔」「真剣な顔」は NG (目を引かない)

### 背景の方向性

サムネイル背景として適切な方向性を1行で。
- 具体的な検索キーワードではなく、「暗めの赤系」「データ表示風」等の視覚的方向性

### Rotation Recommendation

今回の動画で推奨する rotation 軸を示してください。
- `layout_family`
- `emotion_family`
- `color_family`
- `copy_family`

### Rejected Patterns

今回は採用しないコピー型や候補があれば、短く理由を示してください。

## 制約

- 台本の内容を正確に反映してください
- 釣りタイトルにならないこと (台本にない内容を示唆しない)
- ゆっくり解説動画のサムネイルの慣習を踏まえてください
```

---

## 入力例

プロンプトの後に台本テキストを貼り付ける (C-07 と同じ台本でよい)。

---

## 期待される出力例

```
### キャッチコピー候補 (5案)

1. 「吸入器で違反」AIが決める
   - copy_family: case_hook
   - strongest_evidence: 喘息の吸入器を取ろうとして脇見運転フラグ
2. あなたの注文が事故を生む
   - copy_family: contrast_fact
   - strongest_evidence: 配送圧力と危険運転の構造
3. 71.4%が秒単位で監視される
   - copy_family: number_fact
   - strongest_evidence: 71.4%
4. 感謝ボタンは免罪符だった
   - copy_family: contrast_fact
   - strongest_evidence: 19億ドルPR戦略と感謝ボタン
5. 気温+1度で違反率9%増
   - copy_family: number_fact
   - strongest_evidence: 気温+1度で9%増

### サブコピー候補 (3案)

1. Amazon配送の裏で何が起きているか
2. アルゴリズムが消した「人間の限界」
3. 19億ドルのPR戦略の正体

### キャラクター表情の提案

- れいむ: 困惑 (「これが現実なのか」という表情)
- まりさ: 怒り (構造的問題への憤り)

### 背景の方向性

暗めの青〜黒基調、監視カメラ風の四角枠やデータUIの残像を薄く重ねる

### Rotation Recommendation

- layout_family: number_left_character_right
- emotion_family: confused_vs_angry
- color_family: dark_blue_red_alert
- copy_family: number_fact

### Rejected Patterns

- 「ヤバすぎる監視社会」
  - why_rejected: abstract hype で、本文根拠の strongest evidence が見えない
```

---

## C-07 との併用

C-07 の演出メモと同じ台本を入力するため、以下の運用が可能:

1. C-07 で演出メモを生成 (S-6 作業用)
2. Packaging Orchestrator brief がある場合は先に貼り、その後に同じ会話で「サムネイルも」と追加依頼
3. または S-8 専用として別途このプロンプトを使用
