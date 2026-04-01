# G-02b: ymmp 構造解析メモ (1件限定、研究のみ)

> 対象: `なぜ、何もないではなく、何かがあるのか？.ymmp` (171MB)
> 日付: 2026-04-02
> 制限: 2ブロック以内。自前生成には進まない

## トップレベル構造

```
FilePath: string (プロジェクトファイルパス)
Timeline:
  VideoInfo: {FPS: 30, Hz: 48000, Width: 1920, Height: 1080}
  Items: list[1695]  -- タイムライン上の全アイテム
Characters: list[3]  -- キャラクター定義
CollapsedGroups: (UI状態)
```

## Items の $type 分布

| $type | 件数 | 役割 |
|-------|------|------|
| VoiceItem | 1549 | 音声+字幕 (台本読込で生成) |
| VideoItem | 140 | 背景動画 |
| TachieItem | 2 | 立ち絵 (キャラクター別に1件ずつ) |
| AudioItem | 1 | BGM |
| EffectItem | 1 | 視覚エフェクト |
| GroupItem | 1 | グループ |
| ShapeItem | 1 | 図形 |

## VoiceItem の構造 (IR との対応が最重要)

```
CharacterName: string  -- 話者名 (IR: speaker)
Serif: string  -- セリフテキスト (IR: text)
TachieFaceParameter:  -- この発話時の表情 (IR: face)
  Eyebrow: FilePath  -- 眉パーツ画像
  Eye: FilePath  -- 目パーツ画像
  Mouth: FilePath  -- 口パーツ画像
  Hair: FilePath  -- 髪パーツ画像
  Complexion: null | FilePath  -- 顔色
  EyeAnimation: "Default"  -- 目アニメーション
  MouthAnimation: "Default"  -- 口アニメーション
Frame: int  -- タイムライン上の開始フレーム
Layer: int  -- レイヤー番号
Length: int  -- フレーム数 (音声長に対応)
VoiceLength: string  -- 音声の実時間 (例: "00:00:01.0606250")
VoiceCache: string  -- 音声データ (Base64、これが171MBの主因)
```

**重要な発見:**
- VoiceItem が `TachieFaceParameter` を持つ = **発話ごとに表情が指定される**
- 表情はパーツ画像のファイルパスで指定 (例: `05c.png` = 特定の眉パターン)
- IR の `face` (意味ラベル) → 表情パーツファイルパスのマッピングが接続層で必要

## TachieItem の構造 (立ち絵の初期配置)

```
CharacterName: string
TachieItemParameter:
  $type: AnimationTachie.ItemParameter
  IsHiddenWhenNoSpeech: bool
  Eyebrow/Eye/Mouth/Hair/Complexion/Body: FilePath  -- パーツ画像
X: -737.5 (左側) / 708.6 (右側)  -- ピクセル座標
Y: ~540 (画面下部)
Zoom: 120.0
Frame/Layer/Length: タイムライン配置
```

**重要な発見:**
- TachieItem は動画全体で2件のみ (キャラクターごとに1件)
- X 座標で左右配置: -737 (left), +708 (right)
- IR の `slot=left/right` → X 座標のマッピングが接続層で必要
- 立ち絵はパーツ分解方式 (AnimationTachie)

## VideoItem の構造 (背景動画)

```
FilePath: string  -- 動画ファイルパス
X: 0.0, Y: 0.0, Zoom: 100.0  -- 中央配置
Frame: int  -- 開始フレーム
Layer: 0  -- 最背面レイヤー
Length: int  -- 表示フレーム数
```

**重要な発見:**
- 背景動画は140件 = 頻繁に切り替えている
- Layer=0 で統一 (最背面)
- 座標は (0, 0) 中央固定
- IR の `bg` → VideoItem.FilePath のマッピングが接続層で必要

## Characters の構造

3キャラクター定義。各キャラクターに `TachieCharacterParameter` がある。

## IR → ymmp 接続の考察 (G-06 の判断材料)

### IR フィールドと ymmp キーの対応

| IR フィールド | ymmp の対応 | 接続方法 |
|---|---|---|
| speaker | VoiceItem.CharacterName | 直接対応 (台本読込で設定済み) |
| text | VoiceItem.Serif | 直接対応 (台本読込で設定済み) |
| face | VoiceItem.TachieFaceParameter.{Eyebrow,Eye,Mouth,...} | パーツファイルパスへの変換が必要 |
| bg | VideoItem.FilePath | ファイルパスへの変換が必要 |
| slot | TachieItem.X, TachieItem.Y | 座標への変換が必要 (left=-737, right=+708) |
| motion | VideoEffects 配列 | アニメーション効果の組立が必要 |
| se | AudioItem (別途追加) | 新規アイテム挿入が必要 |
| transition | VideoEffects (フェード等) | エフェクト設定が必要 |
| bg_anim | VideoItem + VideoEffects | パン・ズーム効果の組立が必要 |

### 技術的実現性の評価

**比較的容易 (JSON キー置換レベル):**
- face → TachieFaceParameter のパーツファイルパス差し替え
- bg → VideoItem の FilePath 差し替え + Frame/Length 調整

**中程度 (構造理解が必要):**
- slot → TachieItem の X/Y 座標変更
- se → AudioItem の新規挿入

**困難 (スキーマ非公開部分):**
- motion → VideoEffects 配列の組立 (アニメーション種別ごとの構造が不明)
- bg_anim → VideoEffects でのパン・ズーム設定
- transition → 場面切替エフェクト (具体的な $type と構造が未確認)

### ymmp 編集のリスク

- VoiceCache (Base64 音声データ) が 171MB の主因。台本読込経由でないと生成できない
- スキーマ非公開。YMM4 のバージョンアップで構造変動リスク
- VoiceItem は台本読込で生成済みのため、face の差し替えは「既存 VoiceItem の TachieFaceParameter を書き換える」形になる
- VideoItem (背景) の追加・差し替えは比較的安全 (音声に依存しない)

## 結論

- ymmp は JSON であり、キー構造は読み取り可能
- IR → ymmp の接続で最も実用的なのは **bg (背景) の差し替え** と **face (表情) の差し替え**
- motion / transition / bg_anim は VideoEffects の構造が複雑で、自前構築のコストが高い
- G-06 の判断材料として: 「bg + face の半自動差し替え」が最小実用単位。motion 等は手動配置ガイドで対応
