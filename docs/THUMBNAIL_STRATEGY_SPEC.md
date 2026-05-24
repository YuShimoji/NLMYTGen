# THUMBNAIL_STRATEGY_SPEC -- Thumbnail strategy v2 仕様 v0.1

> Feature: H-02
> Status: spec v0.1
> Created: 2026-04-06
> Depends on: H-01 Packaging Orchestrator brief, C-08
> Depended by: C-08 prompt refinement, E-02 metadata, future thumbnail review packet

## 1. 目的

Thumbnail strategy v2 は、ゆっくり解説動画のサムネイル訴求を
「抽象煽りの反復」から「本文根拠のある具体性と variation 管理」へ移すための正本である。

主目的は以下の 3 点:

1. 数値・年数・人数・割合・金額・固有名詞を優先して click promise を作る
2. banned copy pattern を明示し、抽象煽りテンプレ依存を減らす
3. 構図 / 表情 / 配色 / コピー型の rotation を管理し、固定パターン連打を避ける

## 2. 非目標

この spec は以下を直接は行わない:

- サムネイル画像の自動生成
- サムネイル用 `.ymmp` の自動生成
- 台本本文へのサムネイル指示の混入
- 本編 Production IR へのサムネイル指示の混入
- CTR の自動最適化
- 特定 platform の rule 判定の断定
- 最終デザインの自動決定

ここで扱うのは、**コピーと visual direction の戦略制約** である。

## 2.1 仕様状態の整理（2026-04-28）

これまで repo 内に存在していたサムネイル周りの仕様は、**コピー戦略・判断支援・手動制作手順**が中心だった。つまり「サムネイルをどう生成し、台本 / 本編演出 / YMM4 配置とどう分けるか」は、2026-04-28 時点まで明示が薄かった。

既存仕様で定義済みだったもの:

- H-01: title / thumbnail / script の上位 promise と禁止表現
- C-08 / H-02: サムネコピー候補、表情、背景方向性、rotation recommendation
- H-03 / H-04: 本文側でサムネ / タイトル promise を回収できているかの手動スコア集約
- H-05: 完成サムネに対する手動採点の CLI 集約
- `THUMBNAIL_ONE_SHEET_WORKFLOW`: YMM4 テンプレを人間が複製し、文字・立ち絵・背景を差し替えて PNG 書き出しする手順

未定義または未実装だったもの:

- `thumbnail_design` の machine-readable schema
- サムネ用 YMM4 `.ymmp` template source / slot registry の repo 管理
- ShapeItem の readback と限定 patch route
- サムネ配置済み `.ymmp` の自動生成
- サムネ制作物の多様な repo-local corpus

2026-04-28 追補: 最小の YMM4 template copy 差し替え入口として、`audit-thumbnail-template` と `patch-thumbnail-template` を追加した。対象は既存 item の `Remark` が `thumb.text.<id>` / `thumb.image.<id>` の slot のみで、文字列、画像 `FilePath`、既存の `Color` route、`X` / `Y` / `Zoom` / `Rotation` の先頭値だけを patch する。repo 内に実サムネ `.ymmp` template はまだ無いため、実制作 template の TextItem route 固定と視覚 acceptance は未完了。

したがって現行整理では、サムネイルは **台本本文でも Production IR でもなく、H-01 から分岐する sibling artifact** として扱う。

```text
H-01 Packaging Brief
├─ 台本 / refined script
├─ 本編 Production IR
└─ thumbnail_design / H-02 one-sheet
```

AI 生成のタイミングは同じでよい。1 回の LLM セッションで「台本手直し」「本編 Production IR」「thumbnail_design 下書き」を出してよいが、出力 block / 保存 artifact は分ける。`thumbnail_design` は台本本文を書き換えず、`validate-ir` / `apply-production` に渡さない。

YMM4 上のサムネ実作業は別タイミングで行う。現状は、H-02 / `thumbnail_design` を見ながら user がサムネ用 YMM4 テンプレを複製し、文字・立ち絵・背景を差し替えて PNG 書き出しする。テンプレ側に `thumb.*` Remark slot がある場合のみ、NLMYTGen は既存テンプレ内の named slot を限定 patch できる。画像生成、PNG 書き出し、最終デザイン判断は行わない。

## 3. 基本原則

### 3.1 Specificity First

可能な限り、以下の順で具体情報を優先する。

1. 数値: 割合、金額、年数、人数、増減率
2. 固有名詞: 制度名、企業名、製品名、地域名
3. 具体事例: 1 つの象徴エピソード
4. 強い比較: `A vs B`, `建前 vs 実態`, `前後差`
5. 抽象命題: 問題意識や一般化

抽象命題はゼロにしないが、上位 1〜4 があるならそれを先に使う。

### 3.2 Promise Must Be Payable

サムネイルコピーは本文の strongest evidence で回収できるものだけを使う。

以下は NG:

- 本文にない数値を足す
- 本文にない違法断定をする
- 本文にない陰謀論方向へ盛る
- 「全部そうだ」と一般化しすぎる

### 3.3 Variation Over Repetition

毎回同じ構図・同じ色・同じ感情・同じコピー型を繰り返さない。

variation は「毎回バラバラにする」ことではなく、
**rotation axis を記録し、直近の固定化を避ける** ことで達成する。

## 4. Copy Heuristics

### 4.1 推奨コピー型

| 型 | 説明 | 例 |
|---|---|---|
| `number_fact` | 数値を前面に出し、驚きや重さを即伝達する | `71.4%が監視` |
| `named_mechanism` | 制度名や仕組みを前面に出す | `タイム・オフ・タスク` |
| `contrast_fact` | 建前と実態の対比で引く | `感謝ボタンは免罪符か` |
| `case_hook` | 象徴エピソードを導入フックにする | `吸入器で違反判定` |
| `question_with_anchor` | 具体項目つきの問い | `19億ドルの裏で何が起きた?` |

### 4.2 banned copy pattern

以下は原則 banned とする。

- `衝撃の真実`
- `知らないと損`
- `ヤバすぎる`
- `閲覧注意`
- `絶対見て`
- `完全終了`
- `◯◯がヤバい`

補足:

- banned pattern は完全一致だけでなく、同型の抽象煽りにも適用する
- 例外を認める場合も、本文根拠のある具体項目を併置できる時に限る

### 4.3 コピー候補の優先順位

コピー候補は以下の順に評価する。

1. specificity が高い
2. thumbnail_promise に近い
3. title_promise と矛盾しない
4. opening か body 前半で回収できる
5. banned pattern に落ちない
6. 直近の copy_family と被りすぎない

## 5. Visual Direction Heuristics

### 5.1 layout_family

| family | 説明 |
|---|---|
| `number_left_character_right` | 左に大きな数値、右にキャラ |
| `character_center_alert` | 中央キャラ + 周囲に警告UIや記号 |
| `split_contrast` | 左右で建前 / 実態を対比 |
| `object_closeup` | 象徴物を前面に出し、キャラを補助に置く |

### 5.2 emotion_family

| family | 説明 |
|---|---|
| `confused_vs_angry` | 困惑と怒りの対比 |
| `surprised_vs_serious` | 驚きと深刻さ |
| `skeptical_vs_explanatory` | 疑いと解説の対比 |
| `fear_vs_cool_analysis` | 危機感と冷静分析 |

### 5.3 color_family

| family | 説明 |
|---|---|
| `dark_blue_red_alert` | 緊張・監視・警告向け |
| `yellow_black_hazard` | 危険・注意向け |
| `dark_green_terminal` | データ・管理UI向け |
| `white_red_newspaper` | 社会問題・報道感向け |

## 6. Rotation Policy

rotation は 4 軸を持つ:

- `layout_family`
- `emotion_family`
- `color_family`
- `copy_family`

### 6.1 運用ルール

1. 直近 2 本で同じ 4 軸が完全一致していたら、次は最低 2 軸を変える
2. 同じ `copy_family` が 3 本連続したら warning
3. 同じ `color_family` + `layout_family` の組み合わせが 3 本連続したら warning
4. 具体数値が使える動画で、3 本連続で abstract hook に逃げたら warning

## 7. C-08 への要求

C-08 は最終的に以下を出せるべきである。

1. main copy 5案
2. sub copy 3案
3. character expression proposal
4. background direction
5. 各 main copy の `copy_family`
6. 各 main copy が依拠する strongest evidence
7. rotation 上の推奨軸
8. banned pattern に落ちた候補を除外したことの明示

### 7.1 workflow proof 用の追加要求

H-02 を workflow proof する間は、C-08 の出力に以下も含める。

1. `specificity_ledger`
2. `banned_pattern_check`
3. `brief_compliance_check`

目的は「良さそうに見えるコピー」ではなく、
brief の制約が実際に消費されたかを repo 内 artifact から読めるようにすること。

#### `specificity_ledger`

- `preferred_specifics` のうち、どれを main copy に使ったか
- 使わなかった具体項目がある場合は、なぜ採用しなかったか
- `strongest_evidence` が abstract phrase ではなく、本文根拠に結びついているか

#### `banned_pattern_check`

- banned pattern に落ちた候補を 1 件以上明示して除外理由を書く
- 「今回は banned に当たらない」とだけ書いて済ませない

#### `brief_compliance_check`

- `thumbnail_promise` に沿っているか
- `forbidden_overclaim` を踏み越えていないか
- `preferred_specifics` が使えるのに abstract hype へ逃げていないか

### 7.2 specificity-first の proof rule

`preferred_specifics` が与えられている場合、main copy 5案のうち
少なくとも 3 案はそのいずれかを明示的に含むことを推奨ルールとする。

満たせない場合は、モデルが「なぜ具体項目より別の型を優先したか」を
説明しなければならない。

## 8. 推奨出力フォーマット

```md
### Main Copy Candidates

1. [copy]
   - copy_family:
   - strongest_evidence:
   - why_it_works:

### Sub Copy Candidates

1. [copy]

### Character Direction

- reimu:
- marisa:

### Background Direction

- ...

### Rotation Recommendation

- layout_family:
- emotion_family:
- color_family:
- copy_family:

### Rejected Patterns

- [rejected copy or pattern]:
  - why_rejected:

### Specificity Ledger

- preferred_specific_used:
- preferred_specific_not_used:
- strongest_evidence_coverage:

### Brief Compliance Check

- thumbnail_promise_respected:
- forbidden_overclaim_respected:
- specificity_first_respected:
```

## 9. Sample Strategy (AI監視)

| 観点 | 推奨 |
|---|---|
| preferred specifics | `71.4%`, `19億ドル`, `9%増`, `タイム・オフ・タスク`, `吸入器で違反判定` |
| preferred copy family | `number_fact`, `case_hook`, `contrast_fact` |
| avoid | `抽象的な労働問題`, `社会の闇`, `ヤバい監視社会` |
| layout_family | `number_left_character_right` または `split_contrast` |
| emotion_family | `confused_vs_angry` |
| color_family | `dark_blue_red_alert` |

## 10. H-02 の受け入れ基準

H-02 を done に上げる前に、最低限以下を満たす:

1. C-08 が `copy_family` と `strongest_evidence` を出せる
2. banned copy pattern に落ちた候補を除外できる
3. Packaging brief の `preferred_specifics` を優先できる
4. rotation recommendation を 4 軸で返せる
5. 実台本 1 本で「abstract hype から specificity-first へ寄った」と判断できる

### dry proof の合格目安

strict な GUI rerun proof の前段として、repo-local dry proof では以下を満たす。

1. sample brief から `preferred_specifics` / banned pattern / rotation 軸を読める
2. good candidate / rejected candidate を sample 単位で記述できる
3. `specificity_ledger` と `brief_compliance_check` の出力契約が C-08 prompt に埋め込まれている
