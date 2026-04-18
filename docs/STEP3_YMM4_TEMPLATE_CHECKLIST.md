# Step 3: YMM4 テンプレ 5 種作成チェックリスト

> **位置づけ**: 視覚効果ツール選定 slice の Step 3 の user ハンズオン補助。[VISUAL_EFFECT_SELECTION_GUIDE.md](VISUAL_EFFECT_SELECTION_GUIDE.md) §2.3 のテンプレ 5 種を YMM4 で実際に作成・保存するときに使う作業リスト。
> **前提**: Step 1 (ツール決定) / Step 2 (素材ルール) 記入済。既存立ち絵入り ymmp (例: `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp`) を**別名複製**して開いた状態で作業する。
>
> **アイテム種別ルール (INVARIANTS 準拠)**:
> - `TachieItem` と書かれた箇所は **既存の解説役立ち絵 (ゆっくり霊夢 / ゆっくり魔理沙) を流用**する意味。新キャラの連番アニメ立ち絵を新規セットアップしない
> - 外部素材演者 (配達員等) は `TachieItem` を使わず、`ImageItem` 重ね合わせで構成 (正本: [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md))
> - 本チェックリストのテンプレ 5 種は **解説役の演出** (既存 TachieItem 流用) または **汎用素材 ImageItem** を対象とする。外部茶番劇演者の専用テンプレは G-24 主軸の別系統

## 共通作業

- [ ] YMM4 起動し、既存立ち絵入り ymmp を別名複製 (例: `template_work_2026-04-17.ymmp`) して開く
- [ ] タイムラインに **テンプレ作成用 GroupItem** を並べる (後で削除しやすいよう末尾に)
- [ ] 各テンプレ作成後、**右クリック → テンプレートとして保存** を**必ず**実行 (忘れると `ItemSettings.json` の `Templates` 配列に追加されない)
- [ ] 保存した 5 件が `ItemSettings.json` の `Templates` に並んでいることを YMM4 を閉じる前に確認

---

## テンプレ #1: `skit_reaction_jump` (茶番劇の驚き)

**用途**: キャラクターの驚き・反応 (心の声・ツッコミ)。立ち絵にジャンプ + 小さな回転揺れを重ねる。

### 作成手順

- [ ] GroupItem 作成 → 内部に **既存の解説役 TachieItem** (ゆっくり霊夢 or 魔理沙) を 1 体流用配置 ※新キャラの立ち絵セットアップは行わない
- [ ] GroupItem に `JumpEffect` を追加
  - パラメータ目安:
    - `ジャンプ高さ`: 50〜80 px
    - `ジャンプ回数`: 2
    - `全体の時間`: 発話 1 秒に対し 0.6 秒
- [ ] GroupItem に `RandomRotateEffect` を追加
  - パラメータ目安:
    - `最大回転角`: 3〜5 度
    - `周波数`: 8〜12 Hz
- [ ] GroupItem 長さを **30 フレーム (30fps で 1 秒)** に調整
- [ ] 右クリック → テンプレートとして保存、名前 `skit_reaction_jump`

### よくある失敗

- **立ち絵パスが壊れる**: テンプレ保存時点でパス解決ができていれば OK。視覚表示されないままで保存しても Template 自体は登録されるが、別案件に流用したとき全部空になる
- **エフェクトを TachieItem に直接つけた**: GroupItem に付けないと overlay_map 経由で呼び出したとき動作しない
- **外部茶番劇演者 (配達員等) 用に使おうとした**: このテンプレは解説役専用。外部演者は `ImageItem` 重ね合わせの G-24 skit_group template 系 (別系統) を使う

---

## テンプレ #2: `board_list_entry` (黒板リスト項目)

**用途**: 箇条書き・属性列挙の 1 項目を立ち上げ登場させる。

### 作成手順

- [ ] GroupItem 作成 → 内部に **TextItem** (リスト 1 行分のテキスト) と **ShapeItem** (項目の枠) を配置
- [ ] GroupItem に `InOutGetUpEffect` を追加
  - パラメータ目安:
    - `登場時間`: 0.3 秒
    - `退場時間`: 0.2 秒
- [ ] GroupItem に `GradientEffect` を追加
  - パラメータ目安:
    - 色 1 / 色 2: 黒板風 (濃緑 → 暗灰) または案件の基調色 2 色
    - `向き`: 上 → 下
- [ ] GroupItem 長さを発話長に合わせて可変に (初期は 90 フレーム)
- [ ] 右クリック → テンプレートとして保存、名前 `board_list_entry`

### よくある失敗

- **TextItem を直接 GroupItem 外に置いた**: 登場エフェクトがテキストに効かない
- **Gradient の色を真っ黒にした**: 背景と同化して読めなくなる

---

## テンプレ #3: `map_pan_zoom` (地図のパン・ズーム)

**用途**: 地図・関係図の注目箇所へカメラを動かす (Ken Burns 風)。

### 作成手順

- [ ] GroupItem 作成 → 内部に **ImageItem** (地図画像、`bg_map` 登録済みのパス) を配置
- [ ] GroupItem に `CameraPositionEffect` を追加
  - キーフレーム:
    - 0 フレーム: 画面全体 (ズーム 1.0、中心)
    - 中盤: 注目箇所 (ズーム 1.5〜2.0、座標を注目点に)
    - 終端: 再び全体または別の注目箇所
  - 遷移は Ease In-Out
- [ ] GroupItem 長さは案件依存 (初期 180 フレーム = 6 秒)
- [ ] 右クリック → テンプレートとして保存、名前 `map_pan_zoom`

### よくある失敗

- **ImageItem 単体にカメラをつけた**: GroupItem に付けないと overlay 経由で呼び出したとき素材を差し替えられない
- **ズーム倍率を上げすぎて画像が粗くなる**: 原画解像度 × 1.5 くらいで止める

---

## テンプレ #4: `mood_sepia_blur` (雰囲気回想)

**用途**: 回想・ムード転換。セピア + 軽いぼかしでトーンを切り替える。

### 作成手順

- [ ] GroupItem 作成 → 内部に **ImageItem** (背景写真または立ち絵含むシーン) を配置
- [ ] GroupItem に `SepiaEffect` を追加
  - パラメータ目安:
    - `強度`: 0.7〜0.9
- [ ] GroupItem に `GaussianBlurEffect` を追加
  - パラメータ目安:
    - `半径`: 2〜4 px (読めなくならない程度)
- [ ] GroupItem 長さは案件依存 (初期 60 フレーム)
- [ ] 右クリック → テンプレートとして保存、名前 `mood_sepia_blur`

### よくある失敗

- **ブラーを強くしすぎて立ち絵が判別不能**: 4 px 以上はほぼ霧、回想用途の限界
- **Sepia 後に Blur でなく逆順**: 大差ないが、色味決定を先にしたほうが調整しやすい

---

## テンプレ #5: `intro_punch` (冒頭アタック)

**用途**: 動画冒頭のタイトル・キャラ登場で視聴者を掴む。

### 作成手順

- [ ] GroupItem 作成 → 内部に **TextItem** (タイトル) と **既存の解説役 TachieItem** (ゆっくり霊夢 or 魔理沙を流用) を配置 ※新キャラの立ち絵セットアップは行わない
- [ ] GroupItem に `InOutCrashEffect` を追加
  - パラメータ目安:
    - `登場時間`: 0.15 秒 (瞬発)
    - `衝撃強度`: 中〜強
- [ ] GroupItem に `ZoomEffect` を追加
  - キーフレーム: 0 フレームでズーム 1.2 → 15 フレームで 1.0 に戻す
- [ ] GroupItem 長さを 45 フレーム (1.5 秒)
- [ ] 右クリック → テンプレートとして保存、名前 `intro_punch`

### よくある失敗

- **衝撃強度を上げすぎて音声と不一致**: BGM のアタックと合っていないと安っぽくなる
- **ZoomEffect を逆向き**: 1.0 → 1.2 だと拡大で終わって違和感

---

## 完了確認

- [ ] `ItemSettings.json` の `Templates` 配列に 5 件 (`skit_reaction_jump` / `board_list_entry` / `map_pan_zoom` / `mood_sepia_blur` / `intro_punch`) が並んでいる
- [ ] テンプレ作業用 ymmp は**保存せず閉じる** or 別名保存 (本編ymmp を汚染しないため)
- [ ] 次は Step 3 補助の PNG 書き出し ([STEP3_TACHIE_RENDERING_PIPELINE.md](STEP3_TACHIE_RENDERING_PIPELINE.md)) → Step 4 registry 登録

## 既知の未確定事項 (proof で解消予定)

- 各エフェクトのパラメータ初期値は**目安**。YMM4 実機で試してから案件向けに微調整する想定
- `InOutGetUpEffect` / `InOutCrashEffect` の内部パラメータは YMM4 バージョンによって項目名が揺れる可能性。GUI 上の実名が優先
- テンプレ保存時の名前は `ItemSettings.json` に保存される。後で renaming するときは GUI 経由で
