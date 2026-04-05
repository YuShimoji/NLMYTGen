# PACKAGING_ORCHESTRATOR_SPEC -- Packaging Orchestrator brief 仕様 v0.1

> Feature: H-01
> Status: spec v0.1
> Created: 2026-04-05
> Depends on: transcript, source set, C-07/C-08
> Depended by: H-02 (thumbnail strategy), H-04 (evidence richness), E-02 (metadata)

## 1. 目的

Packaging Orchestrator brief は、動画の **タイトル / サムネイル / 台本の約束** を
1 枚の text-only brief に集約するための正本である。

狙いは以下の 3 点:

1. 台本単体が動画タイトルを越権決定しないようにする
2. サムネイル訴求を「抽象煽り」ではなく「本文根拠のある具体性」に寄せる
3. 後続の C-07 / C-08 / E-02 / H-04 / H-03 が同じ promise を参照できるようにする

## 2. 非目標

Packaging Orchestrator brief は以下を直接は行わない:

- 最終タイトルの決定
- サムネイル画像の生成
- 台本本文の自動書き換え
- YouTube 投稿 metadata の最終確定
- creative judgement の自動代替

brief は「決定の上流条件」を固定するものであり、最終判断の owner は人間である。

## 3. ワークフロー位置

### 入力

- NotebookLM 由来の台本
- 必要に応じて source set / reference links / トピックメモ
- 既知の audience 仮説

### 出力

- C-07 が「どの根拠を視覚的に回収すべきか」を判断するための条件
- C-08 が「何を promise し、何を盛ってはいけないか」を判断するための条件
- H-04 が「promise に対して本文根拠が足りるか」を採点するための条件
- E-02 が metadata を組み立てる際の上流制約

### owner / actor

- owner: user
- actor: assistant / GUI LLM / shared

assistant は brief を整形・提案できるが、最終タイトルや最終サムネイルを
勝手に確定してはならない。

## 4. データモデル

Packaging Orchestrator brief は JSON でも Markdown でもよいが、
意味上は以下のフィールドを持つ。

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `brief_version` | string | 必須 | schema バージョン。初期値は `0.1` |
| `video_id` | string | 必須 | 動画識別子。ファイル名や topic slug ベースでよい |
| `topic_label` | string | 必須 | 今回の動画テーマを 1 行で要約したもの |
| `target_viewer` | string | 必須 | 想定視聴者の関心や入口 |
| `audience_hook` | string | 必須 | 視聴者が最初に引っかかる問い / 不安 / 驚き |
| `title_promise` | string | 必須 | この動画を見ると何が分かるかの約束。最終タイトルではない |
| `thumbnail_promise` | string | 必須 | サムネイルが一目で伝えるべき具体点 |
| `novelty_basis` | list[string] | 必須 | この動画が「見慣れた話」ではなくなる根拠 |
| `required_evidence` | list[EvidenceItem] | 必須 | promise を支える根拠。数値 / 固有名詞 / 逸話 / 学術知 / 最新情報など |
| `missing_or_weak_evidence` | list[string] | 任意 | 現時点で弱い / 足りない根拠 |
| `forbidden_overclaim` | list[string] | 必須 | タイトル・サムネ・台本が言ってはいけない盛り方 |
| `thumbnail_controls` | object | 必須 | H-02 に渡す制約。具体数値優先、抽象煽り blacklist、rotation 軸など |
| `script_opening_commitment` | string | 必須 | 導入で早めに回収すべき根拠や約束 |
| `must_payoff_by_section` | list[string] | 任意 | どの section までに何を回収するか |
| `alignment_check` | list[string] | 必須 | 後続 consumer が yes/no で見る整合チェック |
| `consumer_hints` | object | 任意 | C-07 / C-08 / E-02 / H-04 / H-03 向けの補助ヒント |

### 4.1 `EvidenceItem`

`required_evidence` の各要素は以下の構造を持つ。

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `kind` | enum | 必須 | `number`, `named_entity`, `anecdote`, `case`, `study`, `freshness` |
| `value` | string | 必須 | 実際に見せるべき値や固有名詞 |
| `why_it_matters` | string | 必須 | なぜ promise を支えるのか |
| `must_surface_in` | list[string] | 必須 | `thumbnail`, `opening`, `body`, `metadata` など |
| `status` | enum | 必須 | `confirmed`, `weak`, `missing` |

### 4.2 `thumbnail_controls`

`thumbnail_controls` は H-02 のための制御面であり、最終コピー案そのものではない。

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `prefer_specificity` | bool | 必須 | 数値・年数・人数・割合・金額・固有名詞を優先するか |
| `preferred_specifics` | list[string] | 任意 | 今回の動画でサムネに載せやすい具体項目 |
| `banned_copy_patterns` | list[string] | 必須 | 使い回し禁止の抽象煽りパターン |
| `rotation_axes` | object | 必須 | `layout_family`, `emotion_family`, `color_family`, `copy_family` の 4 軸 |

`rotation_axes` は「今回どの型を使うか」を固定するのではなく、
「固定化を避けるために次で変えられる軸」を記録する目的で使う。

## 5. 推奨フォーマット

GUI LLM でも人手でも扱いやすいよう、初期は Markdown を正本にする。

```md
# Packaging Orchestrator Brief

- brief_version:
- video_id:
- topic_label:
- target_viewer:
- audience_hook:
- title_promise:
- thumbnail_promise:

## novelty_basis
- ...

## required_evidence
- kind:
  value:
  why_it_matters:
  must_surface_in:
  status:

## missing_or_weak_evidence
- ...

## forbidden_overclaim
- ...

## thumbnail_controls
- prefer_specificity:
- preferred_specifics:
- banned_copy_patterns:
- rotation_axes:
  - layout_family:
  - emotion_family:
  - color_family:
  - copy_family:

## script_opening_commitment
- ...

## must_payoff_by_section
- ...

## alignment_check
- ...

## consumer_hints
- for_c07:
- for_c08:
- for_e02:
- for_h04:
- for_h03:
```

## 6. 例

```json
{
  "brief_version": "0.1",
  "video_id": "amazon_ai_monitoring",
  "topic_label": "Amazon配送現場でのAI監視と労働負荷",
  "target_viewer": "社会問題とテックの裏側に関心がある視聴者",
  "audience_hook": "便利な配送の裏で、どこまで人間が削られているのか知りたい",
  "title_promise": "Amazon配送現場でAI監視が労働者の余裕をどう奪ったかを、具体データと制度名で理解できる",
  "thumbnail_promise": "監視の強度と企業の建前のギャップを、割合や金額を使って一目で掴ませる",
  "novelty_basis": [
    "抽象的な労働批判ではなく具体数値から入る",
    "企業PRと現場実態のギャップを同時に見せる"
  ],
  "required_evidence": [
    {
      "kind": "number",
      "value": "71.4%",
      "why_it_matters": "監視強度を即座に伝えられる",
      "must_surface_in": ["thumbnail", "opening", "body"],
      "status": "confirmed"
    },
    {
      "kind": "number",
      "value": "19億ドル",
      "why_it_matters": "企業の建前と投資規模のギャップを示せる",
      "must_surface_in": ["thumbnail", "body"],
      "status": "confirmed"
    },
    {
      "kind": "named_entity",
      "value": "タイム・オフ・タスク",
      "why_it_matters": "抽象論ではなく制度名として刺さる",
      "must_surface_in": ["body"],
      "status": "confirmed"
    }
  ],
  "missing_or_weak_evidence": [
    "個人エピソードが弱く、制度の冷たさを体感できる anecdote が不足"
  ],
  "forbidden_overclaim": [
    "台本にない違法断定をしない",
    "陰謀論方向へ盛らない"
  ],
  "thumbnail_controls": {
    "prefer_specificity": true,
    "preferred_specifics": ["71.4%", "19億ドル", "タイム・オフ・タスク"],
    "banned_copy_patterns": ["衝撃の真実", "知らないと損", "ヤバすぎる"],
    "rotation_axes": {
      "layout_family": "number_left_character_right",
      "emotion_family": "confused_vs_angry",
      "color_family": "dark_blue_red_alert",
      "copy_family": "number_fact"
    }
  },
  "script_opening_commitment": "導入ブロックで 71.4% か制度名のどちらかを早めに出し、抽象論から入らない",
  "must_payoff_by_section": [
    "S1 までに監視強度の数値",
    "S2 までに制度名",
    "S4 までに企業側の建前との対比"
  ],
  "alignment_check": [
    "thumbnail promise を支える具体根拠が opening か body 前半に存在するか",
    "title promise が forbidden overclaim を踏み越えていないか",
    "台本が title を決めるのではなく、brief の promise を本文で回収しているか"
  ],
  "consumer_hints": {
    "for_c07": "数値と制度名は B パターンで可視化し、企業PRとの対比は A か D で補強",
    "for_c08": "数値先頭の copy family を優先し、抽象煽りを避ける",
    "for_e02": "説明文でも 71.4% と制度名を落とさない",
    "for_h04": "anecdote 欠損を warning 扱いにする",
    "for_h03": "数値表示ブロックが少なすぎないかを見る"
  }
}
```

## 7. consumer 連携ルール

### C-07 (演出メモ)

- `required_evidence` にある値は、本文内で視覚的に回収する前提で扱う
- `script_opening_commitment` は導入演出で優先回収する
- `forbidden_overclaim` に反する強い演出は避ける

### C-08 (サムネイルコピー)

- `thumbnail_promise` を第一制約とする
- `preferred_specifics` がある場合は、抽象語より先に検討する
- `banned_copy_patterns` に該当するコピーは候補から除外する

### H-04 (Evidence richness score)

- `required_evidence.status` が `weak` / `missing` のものを減点起点にする
- `title_promise` と `thumbnail_promise` を支える根拠が本文に不足していれば warning

### H-03 (Visual density score)

- `required_evidence` のうち「視覚回収が必要」と指定されたものが演出面で拾えているかを見る
- `consumer_hints.for_h03` は診断観点の seed にできる

## 8. H-01 の受け入れ基準

H-01 を done 扱いに上げる前に、最低限以下を満たす:

1. 1 本の実台本で brief を作れる
2. C-07 / C-08 が brief を上流制約として読める
3. title / thumbnail / script の整合ずれを 1 件以上減らせる
4. 「台本がタイトルを決めてしまう」 drift を operator が減ったと判断できる

