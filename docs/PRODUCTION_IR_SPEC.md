# PRODUCTION_IR_SPEC -- 演出 IR (中間表現) 仕様 v1.0

> Feature: G-02
> Status: v1.0
> Created: 2026-04-01
> Depends on: なし
> Depended by: G-05 (IR 出力プロンプト), G-06 (IR → YMM4 接続方式)

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

---

## 2. データモデル

### 2.1 Micro IR エントリ (発話単位)

IR の原子単位は **1発話 = 1エントリ**。`build-csv` の1行に対応する。

| フィールド | 型 | 必須/任意 | 説明 |
|-----------|-----|----------|------|
| `index` | int (1-based) | 必須 | 発話番号。`build-csv` 出力の行番号に対応 |
| `speaker` | string | 必須 | 話者名 (マッピング後) |
| `text` | string | 必須 | 発話テキスト (参照用。IR 消費者は text を変更しない) |
| `section_id` | string | 必須 | 所属セクション ID (`S1`, `S2`, ...) |
| `template` | enum | 任意 | 場面テンプレート名 |
| `face` | enum | 任意 | 表情 |
| `bg` | string | 任意 | 背景 (意味ラベル) |
| `bg_anim` | enum | 任意 | 背景アニメーション |
| `slot` | enum | 任意 | 立ち絵の配置位置 |
| `motion` | enum | 任意 | 立ち絵アニメーション |
| `overlay` | string | 任意 | オーバーレイ素材 (意味ラベル) |
| `se` | string | 任意 | 効果音 (意味ラベル) |
| `transition` | enum | 任意 | この発話の開始時に適用するトランジション |

任意フィールドが省略された場合、前の発話の値を継承する (carry-forward)。
`section_id` が変わった場合は継承をリセットし、Macro IR のセクション既定値を適用する。

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

### 3.7 `overlay` -- オーバーレイ素材

自由文字列。テンプレート定義で解決される意味ラベル。

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
2. `section_id` が前の発話と異なる場合、継承をリセットし、Macro IR の `SectionHeader` の既定値 (`default_bg`, `default_face`) を適用する
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

## 6. テンプレート定義との接続点

### 6.1 概念

IR の意味ラベルは抽象的。テンプレート定義 (JSON) が具体的なリソースに解決する。

```
IR: bg=studio_blue
         ↓ テンプレート定義で解決
解決済み: file_path=backgrounds/studio_blue_01.png, x=0, y=0, w=1920, h=1080
```

### 6.2 テンプレート定義の構造 (概念設計)

テンプレート定義は本仕様のスコープ外だが、接続点を明確にするために構造を示す。

```json
{
  "template_version": "1.0",
  "resolution": {"w": 1920, "h": 1080},
  "bg": {
    "studio_blue": {"file": "backgrounds/studio_blue_01.png"},
    "dark_board": {"file": "backgrounds/dark_board.png"}
  },
  "slot": {
    "left": {"x": 300, "y": 220},
    "right": {"x": 1500, "y": 220},
    "center": {"x": 960, "y": 220},
    "off": null
  },
  "face": {
    "neutral": {"tachie_suffix": "normal"},
    "surprised": {"tachie_suffix": "odoroki"}
  },
  "se": {
    "tension_hit": {"file": "se/tension_hit.wav"},
    "punchline": {"file": "se/punchline.wav"}
  },
  "motion": {
    "pop_in": {"type": "scale", "from": 0.5, "to": 1.0, "duration_ms": 200},
    "slide_in": {"type": "translate", "from_x": -200, "to_x": 0, "duration_ms": 300}
  }
}
```

### 6.3 解決のタイミング

IR → テンプレート定義での解決は、G-06 (接続方式決定) の成果物が担う。

| 接続方式 | 解決の実体 |
|---------|-----------|
| ymmp 変換器 (Python) | Python スクリプトが IR + テンプレート定義 → ymmp の部分データを生成 |
| 手動配置ガイド | IR + テンプレート定義 → 人間が読む演出指示書を生成 |

どちらの方式でも、IR 自体は変わらない。

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
