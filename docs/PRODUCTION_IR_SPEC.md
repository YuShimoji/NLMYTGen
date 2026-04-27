# PRODUCTION_IR_SPEC -- 演出 IR (中間表現) 仕様 v1.0

> Feature: G-02
> Status: v1.0
> Created: 2026-04-01
> Depends on: なし
> Depended by: G-05 (IR 出力プロンプト), G-06 (IR → YMM4 接続方式)

関連（視覚方針）: [VISUAL_STYLE_PRESETS.md](VISUAL_STYLE_PRESETS.md)（挿絵コマ / 再現PV / 資料パネルと IR・patch 制約の対応表）

## 1. 目的

YMM4 にもツールにも依存しない演出中間表現 (Production IR) の語彙とフォーマットを定義する。

- Custom GPT / Claude が IR を直接出力できるようにする (G-05 の基盤)
- テンプレート定義 (JSON) が IR の意味ラベルを座標・ファイルパスに解決する接続点を作る
- ymmp 変換器 or 手動配置ガイド (G-06) の判断材料を提供する

## 設計原則

1. **意味ラベルのみ**: LLM はピクセル座標やファイルパスを出力しない。`slot=right`, `face=surprised` のような意味ラベルだけを扱う
2. **ツール非依存**: YMM4, YMovieHelper, ffmpeg, 特定の素材サイトに依存しない
3. **二層構造**: Macro IR (動画全体) + Micro IR (発話単位) の二層で構成する
4. **CSV/JSON 二重表現**: 同一データを CSV (人間が確認しやすい) と JSON (プログラムが処理しやすい) の両方で表現できる
5. **最小限で実用的**: 初期語彙は S-6 の6つの手動工程をカバーする最小セットとする
6. **段階的拡張**: 語彙追加ルールに従い、実制作の feedback で育てる

**語彙と自動適用の際限:** 本書に登場する全フィールドが、`apply-production` / `patch-ymmp` で ymmp に書き込まれるわけではない。対照表の正本は [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md)。

---

## 2. データモデル

### 2.1 Micro IR エントリ (発話単位)

IR の原子単位は **1発話 = 1エントリ**。意味的な発話単位であり、YMM4 の VoiceItem とは 1:1 とは限らない。

| フィールド | 型 | 必須/任意 | 説明 |
|-----------|-----|----------|------|
| `index` | int (1-based) | 必須 | 発話番号 (IR 内の連番) |
| `speaker` | string | 必須 | 話者名 (マッピング後) |
| `text` | string | 必須 | 発話テキスト (参照用。IR 消費者は text を変更しない) |
| `section_id` | string | 必須 | 所属セクション ID (`S1`, `S2`, ...) |
| `row_start` | int (1-based) | 任意 | この発話が対応する YMM4 VoiceItem 範囲の開始行 |
| `row_end` | int (1-based) | 任意 | この発話が対応する YMM4 VoiceItem 範囲の終了行 (inclusive) |
| `template` | enum | 任意 | 場面テンプレート名 |
| `face` | enum | 任意 | 表情 |
| `idle_face` | enum | 任意 | 待機中表情 (この発話の間、発話していない側のキャラに適用) |
| `body_id` | string | 任意 | 体バリアント ID (G-19)。`--face-map-bundle` 使用時に対応する body の face_map を選択する。carry-forward する。シーンレベル (V1 では全キャラ共通) |
| `bg` | string | 任意 | 背景 (意味ラベル) |
| `bg_anim` | enum | 任意 | 背景アニメーション |
| `slot` | enum | 任意 | 立ち絵の配置位置 |
| `motion` | enum | 任意 | 立ち絵アニメーション |
| `motion_target` | string \| object \| array | 任意 | motion の適用先。省略または `"speaker"` で speaker の TachieItem (既定)。`"layer:N"` または `{"layer": N}` で指定レイヤーの ImageItem/GroupItem に適用。配列 (`["layer:10","layer:11"]` など) で複数レイヤーに同一 motion を同時適用 |
| `group_target` | string | 任意 | 操作対象の GroupItem 識別子（通常は GroupItem.Remark） |
| `group_motion` | string | 任意 | GroupItem 幾何アクションの意味ラベル（`group_motion_map` で解決） |
| `overlay` | string \| string[] | 任意 | オーバーレイ素材 (意味ラベル)。単一または同一発話に複数 ImageItem (G-16) |
| `se` | string | 任意 | 効果音 (意味ラベル) |
| `transition` | enum | 任意 | この発話の開始時に適用するトランジション |

任意フィールドが省略された場合、前の発話の値を継承する (carry-forward)。
`section_id` が変わった場合は継承をリセットし、Macro IR のセクション既定値を適用する。

**row-range (v1.1 追加):**
`row_start` / `row_end` は Writer IR の意味単位 (28 発話等) と YMM4 の VoiceItem (60 行等) の粒度差を吸収する。
- 両方指定: `patch-ymmp` は `row_start`..`row_end` の全 VoiceItem にその utterance の face を適用
- 両方省略: 従来の位置ベース (i番目の utterance → i番目の VoiceItem)
- `row_start` / `row_end` は carry-forward しない (各 utterance 固有の値)

**idle_face (v1.1 追加):**
`idle_face` は「この発話の間、発話していない側のキャラが表示する表情」を指定する。
- `patch-ymmp` は utterance ごとに、speaker 以外の全キャラに対して `TachieFaceItem` を挿入する
- `idle_face` は carry-forward する (省略時は前の発話の値を継承)
- face_map で解決される (character-scoped map の場合、各キャラ固有のパーツに解決)

**motion_target (v1.2 追加 / v1.3 で配列対応):**
`motion_target` は `motion` の VideoEffects 適用先を指定する。
- 省略または `"speaker"`: 既定動作。speaker の TachieItem に適用 (`_apply_motion_to_tachie_items`)
- `"layer:N"` (文字列) または `{"layer": N}` (オブジェクト): 指定レイヤーの ImageItem/GroupItem に適用 (`_apply_motion_to_layer_items`)
- **配列** (`["layer:10","layer:11"]` / `[{"layer":10},{"layer":11}]`): 複数レイヤーに同一 motion を同時適用。body + 顔の同期など「演者全体の所作」を 1 発話で表現するための短期ブリッジ (canonical template 完成までの補助)
- `motion_target` は carry-forward **しない** (各 utterance 固有の値)
- 配列の要素に不正が 1 つでも含まれる場合、validator は `MOTION_TARGET_INVALID` で要素位置付きで reject
- 今回対象外: `"group:<remark>"` 指定 / speaker と layer の混在配列 (例: `["speaker","layer:10"]`)
- `tachie_motion_effects_map` (G-23 プリセット) を共用する。VideoEffects の JSON 構造は item type に依存しない
- **G-24 skit_group actor**: 配達員などの外部茶番劇演者を production IR に出す場合は、repo-tracked YMM4 template source の GroupItem を対象発話へ配置するため `motion_target: "layer:9"` を utterance ごとに明示する。省略時は speaker_tachie とみなされ、skit_group placement の対象外になる。配置限定スライスでは `patch-ymmp --skit-group-only` を使い、face/bg 未解決を配置成果から切り離す。

### 2.2 Macro IR (動画全体)

動画全体の演出方針を定義する。Micro IR のセクション既定値と整合性チェックの基準になる。

| フィールド | 型 | 必須/任意 | 説明 |
|-----------|-----|----------|------|
| `video_id` | string | 必須 | 動画識別子 (ファイル名ベース) |
| `ir_version` | string | 必須 | IR 仕様バージョン (`1.0`) |
| `tone` | string | 必須 | 全体トーン (1行の自由テキスト) |
| `pattern_mix` | string | 必須 | A:B:C:D の推奨比率 (例: `3:4:2:1`) |
| `visual_arc` | list[ArcPhase] | 必須 | 4段階の視覚アーク |
| `recurring_motif` | string | 任意 | 繰り返し素材の説明 |
| `default_bgm` | string | 任意 | 動画全体の既定 BGM トーン |
| `sections` | list[SectionHeader] | 必須 | セクション一覧と既定値 |

**ArcPhase:**

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `phase` | enum: `intro`, `develop`, `climax`, `closing` | アーク段階 |
| `primary_pattern` | enum: `A`, `B`, `C`, `D` | 主に使うパターン |
| `emotion_flow` | string | 視聴者の感情の流れ (例: `共感→不安`) |

**SectionHeader:**

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `section_id` | string | セクション ID (`S1`, `S2`, ...) |
| `topic` | string | トピック名 |
| `start_index` | int | 開始発話番号 |
| `end_index` | int | 終了発話番号 |
| `default_bg` | string | セクション既定背景 |
| `default_face` | string | セクション既定表情 |
| `default_body_id` | string | セクション既定体バリアント (G-19)。省略時はバンドルレジストリの `characters[char].default_body` |
| `bgm` | string | セクション BGM トーン |
| `arc_phase` | enum | このセクションが属するアーク段階 |

---

## 3. 語彙の初期セット

### 3.1 `template` -- 場面テンプレート

C-07 v3 の4演出パターンに intro/closing を加えた6値。

| 値 | 意味 | 典型的な使い方 |
|----|------|-------------|
| `intro` | 導入 | 動画冒頭、掴み |
| `skit` | 茶番劇 (パターン A) | 人物の行動・心情を寸劇風に |
| `data` | 情報埋め込み (パターン B) | 数値・地名・比較をアイテム配置 |
| `mood` | 雰囲気演出 (パターン C) | 写真・背景で場面の空気感 |
| `board` | 黒板型 (パターン D) | 暗背景にテキスト/リスト整理 |
| `closing` | 結び | まとめ・チャンネル登録誘導 |

**オペレータが画像例から言語化した「再現目標」**（立ち絵＋フキダシ、列挙・黒板、地図整理、雰囲気ストック等）と上表の対応は [C07-visual-pattern-operator-intent.md](C07-visual-pattern-operator-intent.md) を正本とする（過去セッション文脈の回収用）。

### 3.2 `face` -- 表情

| 値 | 意味 |
|----|------|
| `neutral` | 通常 |
| `smile` | 笑顔 |
| `serious` | 真剣 |
| `surprised` | 驚き |
| `sad` | 悲しみ |
| `angry` | 怒り |
| `thinking` | 考え中 |

### 3.3 `bg` -- 背景

自由文字列 (enum ではなく string)。テンプレート定義で解決される意味ラベル。

**初期推奨ラベル:**

| 値 | 意味 |
|----|------|
| `studio_blue` | 標準スタジオ (青系) |
| `studio_green` | 標準スタジオ (緑系) |
| `dark_board` | 暗い黒板背景 |
| `photo_outdoor` | フリー写真: 屋外 |
| `photo_indoor` | フリー写真: 室内 |
| `photo_city` | フリー写真: 都市 |
| `map_world` | 世界地図 |
| `map_region` | 地域地図 |
| `diagram` | 図解用の白/薄背景 |

ユーザーが独自のラベルを追加可能。テンプレート定義に対応エントリを作れば解決される。

### 3.4 `bg_anim` -- 背景アニメーション

S-6b (パン・ズーム / Ken Burns) に対応。

| 値 | 意味 |
|----|------|
| `none` | 静止 |
| `pan_left` | 左パン |
| `pan_right` | 右パン |
| `zoom_in` | ズームイン |
| `zoom_out` | ズームアウト |
| `ken_burns` | ケンバーンズ (ゆっくりズーム+パン) |

### 3.5 `slot` -- 配置位置

| 値 | 意味 |
|----|------|
| `left` | 画面左 |
| `right` | 画面右 |
| `center` | 画面中央 |
| `off` | 立ち絵非表示 |

### 3.6 `motion` -- 立ち絵アニメーション

> **重要な境界:** `motion` の既定対象は **speaker_tachie（ゆっくり立ち絵）**。`motion_target` / `group_motion` は補助経路であり、配達員などの **外部素材ベースの茶番劇演者**を直接動かす主経路ではない。茶番劇演者は [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md) の **GroupItem テンプレ運用**を優先する。

| 値 | 意味 |
|----|------|
| `none` | アニメーションなし |
| `pop_in` | ポップイン (拡大して登場) |
| `slide_in` | スライドイン |
| `shake_small` | 小さく揺れる |
| `shake_big` | 大きく揺れる |
| `bounce` | バウンス |
| `fade_in` | フェードイン |
| `fade_out` | フェードアウト |

**G-24 skit_group actor 用 template intent:**

配達員などの skit_group actor を production IR で扱う場合、`motion` は raw effect 名ではなく template 解決用の intent として使い、同じ utterance に `motion_target: "layer:9"` を入れる。

| intent | 解決 |
|----|----|
| `enter_from_left` | exact: `delivery_enter_from_left_v1` |
| `surprise_oneshot` | exact: `delivery_surprise_oneshot_v1` |
| `nod` | exact: `delivery_nod_v1` |
| `deny_oneshot` | exact: `delivery_deny_oneshot_v1` |
| `exit_left` | exact: `delivery_exit_left_v1` |
| `surprise_jump` | fallback alias: `delivery_surprise_oneshot_v1` |
| `deny_shake` | fallback alias: `delivery_deny_oneshot_v1` |

新しい skit_group intent は実制作 gap が出た時だけ registry 側で起票する。通常の IR 生成では上表以外を作らない。`panic_shake` など未登録ラベルは strict validation で `SKIT_GROUP_UNKNOWN_INTENT` として止め、必要なら自然文メモ側で新テンプレ候補に分類する。

**patch-ymmp（G-16 Phase2 / G-17）:** **Phase2**（`--timeline-profile` を付けないとき）: `none` は `TachieItem.VideoEffects` を空配列にクリアする。それ以外の語彙は CLI の **`--tachie-motion-map`**（JSON）で `motion` ラベル → YMM4 効果オブジェクトの**配列**を定義する（[samples/tachie_motion_map.example.json](../samples/tachie_motion_map.example.json)）。発話アンカー（`row_start`/`row_end` 優先、未指定時 `index`）で `TachieItem` を区間分割し、区間ごとに `VideoEffects` を割り当てる。連続する同一 `motion` 区間は結合する。**G-17**（`--timeline-profile` 指定時）: Phase2 の区間分割は走らず、`--motion-map`（各ラベル → `video_effect` 辞書）で既存 `TachieItem` に効果を追記する（[samples/motion_map_g17.example.json](../samples/motion_map_g17.example.json)）。詳細は [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md)。

### 3.6b `group_target` / `group_motion` -- GroupItem 幾何制御（A案）

- `group_target`: 既存 GroupItem を識別するラベル。通常は GroupItem の `Remark` を使う。
- `group_motion`: `group_motion_map` で `X/Y/Zoom` に解決される意味ラベル。
- 本項は **幾何補助**であり、茶番劇演者の感情モーション主経路ではない。配達員等の茶番劇演者については [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md) の template-first 運用を優先する。

**運用前提:**
- GroupItem はテンプレート側に事前配置する（A案）。
- Group の基準点は中央に固定し、配下アイテムは相対配置で保存する。
- patch 側で GroupItem を新規生成する方式（B案）は本仕様の対象外。
- `group_motion` ラベルは `--group-motion-map` で解決する（例: [samples/group_motion_map.example.json](../samples/group_motion_map.example.json)）。

### 3.7 `overlay` -- オーバーレイ素材

自由文字列、またはその配列。テンプレート定義で解決される意味ラベル。
配列のときは順に複数のオーバーレイを同一発話アンカーに挿入する (順序は `overlay_map` の各エントリに従う)。

**初期推奨ラベル:**

| 値 | 意味 |
|----|------|
| `arrow_red` | 赤い矢印 |
| `arrow_blue` | 青い矢印 |
| `circle_red` | 赤い丸 (強調) |
| `flash_red` | 赤いフラッシュ |
| `text_box` | テキストボックス |
| `speech_bubble` | 吹き出し |

### 3.8 `se` -- 効果音

自由文字列。テンプレート定義で解決される意味ラベル。

**初期推奨ラベル:**

| 値 | 意味 |
|----|------|
| `tension_hit` | 緊張感のヒット音 |
| `punchline` | オチ (ツッコミ) |
| `surprise` | 驚き音 |
| `transition` | 場面転換音 |
| `correct` | 正解音 |
| `incorrect` | 不正解音 |
| `click` | クリック/ポイント音 |

### 3.9 `transition` -- トランジション

S-6f に対応。

| 値 | 意味 |
|----|------|
| `none` | トランジションなし |
| `fade` | フェード |
| `slide_left` | 左スライド |
| `slide_right` | 右スライド |
| `wipe` | ワイプ |
| `cut` | カット (即切替) |

**G-15（Adapter）**: 現行の `patch_ymmp` / `validate-ir` が機械処理するのは **`none`** と **`fade`** のみ。上記のその他の値を IR に含める場合、**書き出し前に `validate-ir` が ERROR** となる（YMM4 手動または将来 FEATURE）。

---

## 4. フォーマット仕様

### 4.1 JSON 形式 (正規表現)

JSON が IR の正規形式。Macro IR と Micro IR を1ファイルに格納する。

```json
{
  "ir_version": "1.0",
  "video_id": "AI監視が追い詰める生身の労働",
  "macro": {
    "tone": "社会問題告発系。前半は驚きで引き込み、後半で怒りと問題提起",
    "pattern_mix": "3:4:2:1",
    "visual_arc": [
      {"phase": "intro", "primary_pattern": "A", "emotion_flow": "共感→不安"},
      {"phase": "develop", "primary_pattern": "B", "emotion_flow": "驚き→理解"},
      {"phase": "climax", "primary_pattern": "A", "emotion_flow": "怒り→問題意識"},
      {"phase": "closing", "primary_pattern": "D", "emotion_flow": "思考→行動喚起"}
    ],
    "recurring_motif": "監視カメラのアイコンを各セクション冒頭に配置",
    "default_bgm": "鼓動感のある低音",
    "sections": [
      {
        "section_id": "S1",
        "topic": "導入 -- 吸入器に手を伸ばした瞬間",
        "start_index": 1,
        "end_index": 8,
        "default_bg": "photo_outdoor",
        "default_face": "serious",
        "bgm": "圧迫系低音",
        "arc_phase": "intro"
      }
    ]
  },
  "utterances": [
    {
      "index": 1,
      "speaker": "れいむ",
      "text": "ちょっと想像してみてください",
      "section_id": "S1",
      "template": "skit",
      "face": "serious",
      "bg": "photo_outdoor",
      "bg_anim": "ken_burns",
      "slot": "left",
      "motion": "fade_in",
      "overlay": null,
      "se": null,
      "transition": "fade"
    },
    {
      "index": 2,
      "speaker": "まりさ",
      "text": "え、何の話？",
      "section_id": "S1",
      "template": "skit",
      "face": "surprised",
      "slot": "right",
      "motion": "pop_in"
    }
  ]
}
```

### 4.2 CSV 形式 (簡易表現)

Micro IR のみを CSV で表現する。Macro IR は CSV では表現しない (JSON のみ)。

- エンコーディング: UTF-8 (BOM 付き)
- 区切り: カンマ
- ヘッダー行: あり (1行目)
- 空セルは省略 (carry-forward 適用)

```csv
index,speaker,text,section_id,template,face,bg,bg_anim,slot,motion,overlay,se,transition
1,れいむ,ちょっと想像してみてください,S1,skit,serious,photo_outdoor,ken_burns,left,fade_in,,,fade
2,まりさ,え、何の話？,S1,skit,surprised,,,,pop_in,,,
3,れいむ,配送ドライバーがね…,S1,skit,serious,,,,,,tension_hit,
```

### 4.3 carry-forward ルール

1. 省略された任意フィールドは、直前の発話の値を継承する
2. `section_id` が前の発話と異なる場合、継承をリセットし、Macro IR の `SectionHeader` の既定値 (`default_bg`, `default_face`, `default_body_id`) を適用する
3. `null` (JSON) または空文字列 (CSV) は「このフィールドを無効にする」を意味する。`overlay=null` は「オーバーレイなし」
4. 最初の発話 (index=1) では全必須フィールドを明示する

---

## 5. Macro IR と Micro IR の関係

### 5.1 情報の流れ

```
Macro IR (1動画に1つ)
├── tone, pattern_mix: 動画全体の方針。LLM が一貫性を保つための参照
├── visual_arc[4]: 段階ごとの主パターンと感情フロー
└── sections[N]: セクション既定値
     ├── default_bg: セクション開始時の背景
     ├── default_face: セクション開始時の表情
     ├── bgm: セクション BGM
     └── arc_phase: 視覚アークのどの段階か

Micro IR (発話ごとに1つ)
├── section_id: どのセクションに属するか (Macro の sections と紐付く)
├── template, face, bg, ...: 発話レベルの演出指示
└── 省略時は carry-forward → セクション既定値 → 無指定
```

### 5.2 解決の優先順位

1. Micro IR に明示された値 (最優先)
2. carry-forward (前の発話から継承)
3. Macro IR のセクション既定値 (section_id の変更でリセットされた場合)
4. テンプレート定義の全体既定値 (IR の外、解決層で適用)

### 5.3 整合性ルール

- `pattern_mix` は推奨比率であり、Micro IR の `template` 分布が大きく乖離する場合は LLM に再考を促す (G-05 のプロンプトで制御)
- `visual_arc` の `arc_phase` と `sections` の `arc_phase` は一致すること
- 同じ `bg` が連続する発話が60秒相当 (約8-10発話) を超える場合は警告対象 (G-05 プロンプトの制約として組み込む)

---

## 6. 三層アーキテクチャと責務分担

### 6.1 工程分離の原則

演出パイプラインは2つの独立工程に分離する:

- **Writer 工程** (演出スクリプト生成): LLM が台本から IR を出力する。「何を表示するか」の判断。品質はフィードバック駆動で改善し、scope を区切る
- **Editor 工程** (テンプレート解決 + ymmp 適用): IR の意味ラベルを具体的なリソースとYMM4 操作に解決する。「どう配置するか」の実行。品質は複雑さ・汎用性・拡張性に依存

### 6.2 三層アーキテクチャ

```
第1層: Writer IR (演出スクリプト)
  LLM が出力する高水準の演出指示。
  scene_preset / face / bg 等の意味ラベルを選ぶ。
  逐次属性は optional override。

第2層: Template Registry (テンプレート辞書)
  ユーザーの制作環境で使う素材・プリセットの辞書。
  IR の意味ラベルと、具体的なリソース / YMM4 テンプレート名を紐付ける。

第3層: YMM4 Adapter (Post-Processor)
  IR + Template Registry → ymmp の接着層。
  YMM4 ネイティブに解決できるものはテンプレート参照へ寄せ、
  ネイティブで届かない部分だけを後段で補正する。
```

### 6.3 責務分担

| 処理 | 担当層 | 方法 |
|------|--------|------|
| 音声合成 + 字幕配置 | YMM4 ネイティブ | 台本読込 (CSV) |
| エフェクト / アニメーション / 場面テンプレート | YMM4 ネイティブ | YMM4 のアイテムテンプレート (インポート/エクスポート対応) |
| face パーツ差し替え (発話ごと) | YMM4 Adapter (patch-ymmp) | VoiceItem.TachieFaceParameter の書き換え |
| bg 画像差し替え (セクションごと) | YMM4 Adapter (patch-ymmp) | ImageItem/VideoItem の FilePath + Frame/Length |
| slot 座標変更 | YMM4 Adapter (patch-ymmp) | TachieItem の X/Y (実測後) |
| motion | YMM4 Adapter (patch-ymmp) | `TachieItem.VideoEffects`（Phase2: `--tachie-motion-map`。[G-16](FEATURE_REGISTRY.md)。G-17: `--timeline-profile` + `--motion-map`。[G-17](FEATURE_REGISTRY.md)） |
| transition | YMM4 Adapter (patch-ymmp) | `VoiceItem` Voice/Jimaku フェード（G-15、`none` / `fade` のみ）。G-17 プロファイル経路あり |
| bg_anim | YMM4 Adapter (patch-ymmp) | Layer0 のキーフレームプリセット（G-14、micro bg 連動）および G-17 の `VideoEffects` 追記（プロファイル + `bg_anim_map`） |
| se / overlay | YMM4 Adapter (patch-ymmp) | `--se-map` / `--overlay-map` 経由で `AudioItem` / `ImageItem` 挿入（G-13/G-18）。対照: [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md) |
| skit_group placement | YMM4 Adapter (patch-ymmp) | `--skit-group-registry` + `--skit-group-template-source` + `--skit-group-only` で repo-tracked `.ymmp` template library の GroupItem を対象発話に挿入 |

### 6.4 Template Registry の構造

```json
{
  "registry_version": "1.0",
  "project": {
    "resolution": {"w": 1920, "h": 1080},
    "fps": 30
  },

  "scene_presets": {
    "skit": {
      "description": "茶番劇。人物の行動・心情を寸劇風に",
      "ymm4_template": "演出/茶番劇",
      "defaults": {
        "bg": "photo_indoor", "bg_anim": "none",
        "slot": "left", "motion": "pop_in",
        "overlay": "speech_bubble", "se": null
      }
    },
    "data": {
      "description": "情報埋め込み。数値・地名・比較をアイテム配置",
      "ymm4_template": "演出/データ表示",
      "defaults": {
        "bg": "diagram", "bg_anim": "none",
        "slot": "right", "motion": "none",
        "overlay": "text_box", "se": null
      }
    },
    "board": {
      "description": "黒板型。暗背景にテキスト/リスト整理",
      "ymm4_template": "演出/黒板",
      "defaults": {
        "bg": "dark_board", "bg_anim": "none",
        "slot": "off", "motion": "none",
        "overlay": null, "se": null
      }
    }
  },

  "characters": {
    "れいむ": {
      "default_slot": "left",
      "face_map": {
        "neutral":   {"Eyebrow": "...", "Eye": "...", "Mouth": "..."},
        "serious":   {"Eyebrow": "...", "Eye": "...", "Mouth": "..."},
        "surprised": {"Eyebrow": "...", "Eye": "...", "Mouth": "..."}
      }
    }
  },

  "bg_map": {
    "studio_blue": "backgrounds/studio_blue_01.png",
    "dark_board": "backgrounds/dark_board.png",
    "photo_outdoor": "backgrounds/outdoor_01.jpg"
  },

  "slots": {
    "left":   {"x": -737, "y": 540, "zoom": 120},
    "right":  {"x":  708, "y": 540, "zoom": 120},
    "center": {"x":    0, "y": 540, "zoom": 120},
    "off":    null
  },

  "se_map": {
    "tension_hit": "se/tension_hit.wav",
    "punchline": "se/punchline.wav"
  }
}
```

**設計の要点:**
1. `scene_presets` の `ymm4_template` フィールドで YMM4 ネイティブテンプレートを名前参照。YMM4 テンプレートにアニメーション/エフェクト/複合アイテムをバンドルしておけば、一括適用できる
2. `defaults` は IR で省略された場合のフォールバック。IR に明示されたフィールドが優先 (override)
3. `characters` 軸で face_map を持つ。同じ `face=serious` でもキャラごとにパーツ構成が異なることを吸収
4. `bg_map` / `slots` / `se_map` は現在の face_map / bg_map の拡張

**運用上の重要事項:**
- `face=serious` / `face=thinking` などの意味ラベルは、ファイル名やパーツ番号から自動推定しない
- YMM4 上で人間が見え方を確認し、「この組み合わせを serious と呼ぶ」と決めたテンプレートを Template Registry に登録する
- `extract-template` は既存 ymmp から「使われているパーツ組み合わせ」を棚卸しする補助であり、意味ラベルを推論するツールではない
- 実装上の `face_map.json` / `bg_map.json` の自動キー (`face_01_...`, `bg_01_...`) は仮キー。ユーザーが visual review 後に IR ラベルへリネームして使う
- 複数キャラ案件では、最終的に `face_map` はキャラ軸を持つ必要がある。現行 `patch-ymmp` のフラット辞書は単一キャラ proof 向けの暫定形

### 6.5 解決の優先順位 (v1.0 からの変更)

1. Micro IR に明示された値 (最優先)
2. carry-forward (前の発話から継承)
3. **scene_preset の defaults** (template フィールドで参照されたプリセットの既定値)
4. Macro IR のセクション既定値 (section_id の変更でリセットされた場合)
5. Template Registry の全体既定値

### 6.6 YMM4 ネイティブ機能の活用方針

YMM4 のアイテムテンプレートはグローバル設定として `ItemSettings.json` の `Templates` 配列に保存される。ymmp 内にはテンプレート参照ではなく展開後の値が格納される。

**実測結果 (2026-04-03):**

- テンプレートは独立ファイルではなく、`YMM4フォルダ/user/setting/{version}/YukkuriMovieMaker.Settings.ItemSettings.json` 内の JSON オブジェクト
- テンプレートの `Items` 配列は ymmp の `Items` と同一構造。Adapter のロジックがテンプレートにも再利用可能
- ImageItem テンプレートに VideoEffects (StripeGlitchNoise, RectangleGlitchNoise, RandomRotateEffect) が完全保持される
- VoiceItem テンプレートに VoiceCache (音声キャッシュ) が保持される
- テンプレート名 (`Name`) で YMM4 GUI から呼び出せる。IR の `scene_preset` がテンプレート名を参照値として使える
- 保存先は YMM4 バージョンごとのフォルダ (`user/setting/4.51.0.1/` 等)

**活用方針:**
- motion / transition / bg_anim 等の複雑なエフェクトは、YMM4 のアイテムテンプレートに登録して一括適用するのが最も安全で堅牢
- Python 側 (Adapter) は face / bg / slot 等の「JSON キー置換レベル」の差し替えに集中する
- Template Registry の `ymm4_template` フィールドは ItemSettings.json 内のテンプレート名を参照する。Python がテンプレートを直接生成する経路は、ItemSettings.json の `Templates` 配列への追記として技術的に実現可能だが、YMM4 起動中のファイル書き換えリスクがあるため慎重に評価する
- 表情アイテム (ボイスアイテムとは別の表情変更専用アイテム) の活用も検討する
- Group 制御を使うテンプレートは **中央基準 GroupItem** を事前配置し、配下アイテムを相対配置で保存する。使い捨て Group 化は標準運用にしない（A案前提）

**残りの実測項目:**

- 複数アイテムをバンドルしたテンプレート (Items: list[2+]) の実例
- 表情アイテムの ymmp JSON 構造
- GroupItem の内部構造（実運用で使う `X/Y/Zoom/GroupRange` は観測済みだが、完全な契約化は継続）
- VideoEffects の $type ごとのパラメータ構造
- テンプレートのインポート/エクスポート機能の具体的な出力形式

---

## 7. 拡張ルール

### 7.1 語彙追加の手順

1. **実制作で不足を確認する**: 仮定や理論ではなく、実際の動画制作で「この演出を IR で表現できない」と判明した場合に追加を検討する
2. **既存語彙で代用できないか確認する**: 類似の既存ラベルとの重複を避ける
3. **意味ラベルの命名規則に従う**: 英小文字 + アンダースコア、8文字以内推奨、YMM4 固有語を避ける
4. **PRODUCTION_IR_SPEC.md を更新する**: 語彙テーブルに行を追加し、`ir_version` のマイナー番号を上げる
5. **テンプレート定義に対応エントリを追加する**: IR ラベルとリソースのマッピングを追加する

### 7.2 フィールド追加の手順

新しい任意フィールドを追加する場合:

1. S-6 のどの手動工程に対応するか、または新しい工程かを明示する
2. Micro IR (発話単位) か Macro IR (動画単位) かを決める
3. 型を定義する (enum の場合は初期値セットも)
4. carry-forward ルールを定義する
5. CSV 列の追加位置を決める (末尾に追加が原則)
6. `ir_version` のマイナー番号を上げる

### 7.3 バージョニング

- `MAJOR.MINOR` 形式
- MINOR: 語彙追加、任意フィールド追加 (後方互換)
- MAJOR: 必須フィールド変更、carry-forward ルール変更、CSV 列順変更 (非互換)

### 7.4 命名規則

| 対象 | ルール | 例 |
|------|--------|-----|
| フィールド名 | snake_case, 英字のみ | `bg_anim`, `section_id` |
| enum 値 | snake_case, 英字+数字 | `pan_left`, `studio_blue` |
| 自由文字列ラベル | snake_case 推奨、日本語不可 | `photo_outdoor`, `map_world` |
| section_id | `S` + 連番 | `S1`, `S2`, `S12` |

---

## 8. S-6 手動工程カバレッジ

| S-6 工程 | IR フィールド | カバー状況 |
|---------|-------------|-----------|
| a. 背景配置 | `bg` | カバー済み |
| b. 背景 Animation | `bg_anim` | カバー済み |
| c. 立ち絵表情切り替え | `face`, `slot`, `motion` | カバー済み |
| d. BGM | `bgm` (Macro SectionHeader) | カバー済み (セクション単位) |
| e. SE | `se` | カバー済み |
| f. トランジション | `transition` | カバー済み |

---

## 関連ドキュメント

- [YMM4-AUTOMATION-RESEARCH.md](YMM4-AUTOMATION-RESEARCH.md) セクション3: 演出 IR の背景と戦略
- [S6-production-memo-prompt.md](S6-production-memo-prompt.md): C-07 v3 プロンプト (IR 出力の前身)
- [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md): G-02, G-05, G-06 の登録
