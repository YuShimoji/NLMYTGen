# YMM4 自動化調査 + 開発ロードマップ

> 2026-04-01 作成

## 目的

YMM4 (ゆっくりMovieMaker4) の手動工程を減らし、NLMYTGen パイプラインの自動化範囲を拡大する。
YMM4 以外の動画制作パイプラインは検討対象外。

---

## 1. YMM4 の自動化経路: 調査結果

### 1.1 プラグイン API (公式)

YMM4 は v4.20.0.0 以降、公式プラグイン API を提供している。

**公式ドキュメント:** https://ymmapi.pages.dev/

**開発環境:**
- .NET 10 SDK + WPF
- Visual Studio / VSCode / Rider
- 参照 DLL: `YukkuriMovieMaker.Plugin.dll`, `YukkuriMovieMaker.Controls.dll`

**プラグインの種類 (13種):**

| 種類 | インターフェース | 用途 |
|------|----------------|------|
| 映像エフェクト | `VideoEffectBase` | 映像への効果追加 |
| 音声エフェクト | `AudioEffectBase` | 音声への効果追加 |
| 図形 | `IShapePlugin` | カスタム図形 |
| 立ち絵 | `ITachiePlugin` | キャラクター立ち絵の読込 |
| 波形 | `IAudioSpectrumPlugin` | 音声波形表示 |
| 場面切り替え | `ITransitionPlugin` | トランジション |
| 画像読み込み | `IImageFileSourcePlugin` | 画像フォーマット対応 |
| 動画読み込み | `IVideoFileSource` | 動画フォーマット対応 |
| 音声読み込み | `IAudioFileSourcePlugin` | 音声フォーマット対応 |
| 動画出力 | `IVideoFileWriterPlugin` | 出力フォーマット対応 |
| 音声合成 | `IVoicePlugin` | TTS エンジン連携 |
| テキスト補完 | `ITextCompletionPlugin` | AI テキスト補完 |
| **ツール** | **`IToolPlugin`** | **ツールメニューからの独自処理** |

**IToolPlugin (ツールプラグイン) の特性:**
- YMM4 のツールメニューから呼び出せる独自ウィンドウを作成可能
- View (UserControl) + ViewModel の WPF パターン
- IPC 通信で外部プロセスとの連携が可能
- ただし、**タイムラインやアイテムの直接操作 API は公開されていない**
- YMM4 内部 API へのアクセスは限定的 (バージョン情報、ディレクトリ、ログ、翻訳リソース程度)

**利用可能な内部クラス:**
- `AppVersion` -- バージョン情報
- `AppDirectories` -- YMM4 のディレクトリパス
- `Log` -- ログ出力
- `IMainViewModel` -- メインウィンドウ判定
- WPF コントロール群 (FrameNumberEditor, EnumComboBox, TextEditor 等)

**制約:**
- IToolPlugin はタイムライン操作を想定していない (独立したツールとしての設計)
- 複数プラグインでのライブラリバージョン競合問題あり
- 通信処理を含むとウイルス誤判定のリスク

### 1.2 .ymmp 直接編集 (非公式だが実績あり)

**ファイル形式:** JSON (UTF-8 BOM)

**JSON 構造 (判明分):**

```
{
  "Timeline": {
    "VideoInfo": { "FPS": 30, "Hz": 48000, "Width": 1920, "Height": 1080 },
    "Items": [ ... ],           // タイムライン上の全アイテム
    "LayerVisibilities": [...],  // レイヤー表示/非表示
    "Length": "...",             // タイムライン長
    "MaxLayer": N
  },
  "Characters": [ ... ]         // キャラクター情報
}
```

**アイテムタイプ (判明分):**

| タイプ | $type 値 | 主要プロパティ |
|--------|---------|---------------|
| VoiceItem | `YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker` | CharacterName, Serif, Hatsuon, VoiceLength, Frame, Length, Decorations |
| ImageItem | `YukkuriMovieMaker.Project.Items.ImageItem, YukkuriMovieMaker` | FilePath |
| VideoItem | `YukkuriMovieMaker.Project.Items.VideoItem, YukkuriMovieMaker` | FilePath |

**既存の参考実装:**

| プロジェクト | 言語 | 内容 |
|-------------|------|------|
| [AutoYukkuri](https://github.com/akazdayo/AutoYukkuri) | Python | Whisper 音声認識 → ymmp 自動生成。VoiceItem のみ対応 |
| [KuchiPaku](https://github.com/InuInu2022/KuchiPaku) | C# | リップシンク用の口パク自動生成 |
| [YMM4ObjectListPlugin](https://github.com/InuInu2022/YMM4ObjectListPlugin) | C# | タイムラインオブジェクト一覧表示 |

**ymmp 直接編集の利点:**
- Python (json モジュール) で読み書き可能。外部依存なし
- VoiceItem の追加は実績あり (AutoYukkuri)
- 台本読込後の ymmp を開いて、背景/表情を差し替えることが理論的に可能

**ymmp 直接編集の制約:**
- **音声ファイルは台本読込時に YMM4 が生成する。外部から ymmp を作っても音声は生成されない**
- スキーマが非公開。YMM4 のバージョンアップで構造が変わるリスク
- ImageItem, TachieItem (立ち絵/表情) の詳細構造は未文書化

### 1.3 コマンドライン / 外部起動

**調査結果: 確認できず。**
YMM4 のコマンドライン引数、台本読込の外部実行、バッチ処理用の CLI は公式ドキュメントに記載なし。

---

## 2. YMM4 周辺ツール群: 第二次調査結果

### 2.1 既存ツール一覧 (実在確認済み)

| ツール | 開発者 | 機能 | NLMYTGen との接点 |
|--------|--------|------|-----------------|
| **YMovieHelper** | だんご | CSV 台本 → ymmp 生成。**立ち絵表情変更 + 動画切り替えに対応** | C-07 v3 の演出指示を入力形式に変換すれば背景/表情の自動配置が可能 |
| **AoiSupport** | Mrs.ニードルマウス | 音声合成ソフト → YMM4 自動投入 | NLMYTGen の責務外 (音声は YMM4 台本読込で生成) |
| **YMM4 自動SE挿入** | -- | AI 感情推定 → 効果音自動挿入 | S-6e の自動化。NLMYTGen 側の対応不要 |
| **AutoYukkuri** | akaz | Whisper → ymmp 自動生成 (VoiceItem のみ) | ymmp JSON 構造の参考実装 |
| **KuchiPaku** | InuInu | .lab → 口パクアニメーション自動生成 | NLMYTGen の責務外 |
| **ゆっくり自動化ツール** | SS | 台本 → 画像素材自動収集/配置 | 有償 (5万円)。技術的仕組みは非公開 |
| **MaterialFinder** | -- | プロジェクト内の素材パスを一括取得 | 素材管理の参考 |
| **YMMProjectManager** | -- | リンク切れ素材の自動探索・修復 | 素材管理の参考 |
| **ジェットカットプラグイン** | -- | 無音区間を自動検出してカット | S-5 後工程の効率化 |

### 2.2 YMM4 の公式自動化経路 (4系統)

| 系統 | 方式 | 堅牢性 | NLMYTGen の対応 |
|------|------|--------|----------------|
| **1. 台本/字幕インポート** | CSV/TXT/SRT → YMM4 台本読込 | 高 | **build-csv で対応済み** |
| **2. プロジェクト事前構築** | CSV → YMovieHelper → ymmp | 中 | **C-07 v3 → YMovieHelper 入力形式変換が鍵** |
| **3. 外部音声連携** | AoiSupport 等 → YMM4 | 高 | NLMYTGen の責務外 |
| **4. プラグイン拡張** | IToolPlugin 等 | 低 (API 制限) | タイムライン操作 API 非公開。優先度最下位 |

### 2.3 構造的な注意点

YMM4 は「ヘッドレスな完全自動レンダラ」ではない。CLI 一括レンダリングは公式に確認できず、動画出力は GUI 操作が必要。完全無人化の最後の 1 マイルには人手介入が残る。

---

## 3. 自動化戦略 (再設計)

### 3.1 方針転換

**旧方針 (廃止):** IToolPlugin spike を最優先 → タイムライン操作 API が非公開で見通しが立たない

**新方針:** 既存ツール (YMovieHelper) の活用 + NLMYTGen 出力形式の最適化

### 3.2 三層モデル

| 構成 | 内容 | 壊れやすさ | NLMYTGen の役割 |
|------|------|-----------|----------------|
| **軽量** | 台本 → CSV/SRT → YMM4 台本読込 → 人手演出 | 低 | **現在ここ (build-csv done)** |
| **中量** | 台本 → YMovieHelper 入力 → ymmp 生成 → YMM4 確認 | 中 | **次の目標 (build-ymh 新規)** |
| **重量** | 自作 ymmp 生成 + プラグイン + 自動レンダリング | 高 | 長期的な研究対象 |

### 3.3 想定パイプライン (中量構成)

```
[台本テキスト]
    | NLMYTGen build-csv
    v
[YMM4 CSV] -----------> [YMM4 台本読込] -> 音声生成 + 字幕配置
    | NLMYTGen C-07 v3 (Custom GPT)
    v
[演出メモ]
    | NLMYTGen build-ymh (新規)
    v
[YMovieHelper 入力] ---> [YMovieHelper] -> ymmp 生成 (背景 + 表情 + 動画切替)
                                              |
                                         [YMM4 で開く]
                                              |
                                         [人手: 確認 + 微調整]
                                              |
                                         [動画出力]
```

### 3.4 ymmp 直接編集の位置づけ

ymmp 直接編集は**控える**。理由:
- 過去に音声生成の仕組みを理解せずに進め、デッドファイルが積み上がった経験あり
- 「完成品 ymmp の解析からの再現可能性の研究」までが許容範囲
- 研究に没頭して開発から逸れるリスクがある

---

## 4. 開発ロードマップ (再設計)

### 全体像

| 優先度 | ID | 内容 | 経路 | 前提 |
|--------|----|------|------|------|
| **1** | G-02 | YMovieHelper の入力形式・機能の詳細調査 | 既存ツール活用 | YMovieHelperLocal を起動 |
| **2** | G-05 | C-07 v3 → YMovieHelper 入力形式変換 (build-ymh) | NLMYTGen Python | G-02 の結果 |
| **3** | G-02b | 完成品 ymmp の構造解析 (研究のみ、編集しない) | 解析のみ | ymmp サンプル提供 |
| **4** | E-01+E-02 | YouTube 投稿 + メタデータ自動化 | YouTube API | stdlib 緩和 ADR |
| **5** | B-17+ | 字幕リフロー微調整 | 既存 Python | なし |
| 最下位 | G-01 | IToolPlugin spike (代替経路) | プラグイン API | .NET 10 環境構築 |

### G-02: YMovieHelper 詳細調査

**目的:** YMovieHelper の CSV 入力仕様を把握し、NLMYTGen の出力と接続できるか評価する。

**確認事項:**
1. CSV のどの列で表情/背景/動画を指定するか
2. 生成される ymmp の構造 (特に背景・表情の配置方法)
3. テンプレート機能の有無と使い方
4. C-07 v3 の演出指示をマッピングできるか

### G-05: build-ymh サブコマンド (新規)

**目的:** C-07 v3 の演出メモと build-csv の出力を組み合わせ、YMovieHelper の入力形式に変換する。

**想定フロー:**
1. build-csv で YMM4 CSV を生成 (既存)
2. C-07 v3 (Custom GPT) で演出メモを生成 (既存)
3. `build-ymh` で演出メモ + CSV → YMovieHelper 入力形式に変換 (新規)
4. YMovieHelper で ymmp を生成
5. YMM4 で確認 + 微調整

### G-01: IToolPlugin spike (代替経路、最下位)

YMovieHelper 連携で十分な自動化が達成できない場合にのみ検討。
タイムライン操作 API が非公開であるため、.NET 環境構築の投資対効果が不明。

---

## 4. NotebookLM 自動化について

### ユーザー方針との整合

| 段階 | 内容 | 状態 | NLMYTGen の対応 |
|------|------|------|----------------|
| 1 | 台本ファイルを自前で用意 | 済み | A-01, A-02, build-csv |
| 1-2 | Claude Cowork 等で台本準備を自動化 | NLMYTGen 外 | -- |
| 2 | RSS 記事選定の自動化 | A-04 done | fetch-topics |
| 3 | NotebookLM Automation (別システム) | 未着手 | NLMYTGen 外。動画制作が回り始めてから |

### 調査の結論

- NotebookLM の Web UI RPA は壊れやすく製品基幹に不向き
- NotebookLM 代替 (Gemini API + TTS multi-speaker) は技術的に可能だが大規模
- **折衷案 (前処理自動化 + NotebookLM は読解/音声化のみ) が現時点で最も筋がよい**
- NLMYTGen は「台本ができた後」の工程に専念する。台本入手の自動化は別システム

### 今 NLMYTGen で伸ばすべき方針

| 方針 | NLMYTGen 担当部分 | 優先度 |
|------|-------------------|--------|
| 台本ファイル整形 (動画化のための再編集) | build-csv の後段処理 | 中 |
| **アニメーション自動化** | **G-01~G-04 (YMM4 プラグイン + ymmp 編集)** | **高** |
| 字幕クオリティ向上 | B-17 微調整 | 低 |
| YT 投稿 API 自動化 | E-01 + E-02 | 中 |

---

## 5. 作業時間の実態

| 工程 | 10分動画あたり | 自動化後の見込み |
|------|-------------|----------------|
| S-3 CSV 変換 | 5分 (CLI 実行) | 変わらず |
| S-4 台本読込 | 5分 (手動操作) | 変わらず |
| S-5 読み上げ確認 | 30分~1時間 | B-17 で改善済み |
| **S-6 背景・演出設定** | **3~5日 (最大ボトルネック)** | **G-03/G-04 で半自動化目標** |
| S-7 最終確認 | 30分 | 変わらず |
| S-8 サムネイル | 1~2時間 | C-08 で判断支援済み |
| S-9 YouTube 投稿 | 15分 (手動) | E-01 で自動化目標 |

**S-6 が制作時間の 70%以上を占めている。ここの自動化が最も効果が大きい。**

---

## 6. テンプレート戦略

### 6.1 テンプレートとは

場面タイプに対して、背景/表情/BGM/SE のプリセットを定義したもの。台本の各行にテンプレート名を指定するだけで、演出要素が一括付与される。映像編集版の CSS に相当する。

例:

| テンプレート名 | 背景 | 表情 | BGM | SE |
|--------------|------|------|-----|-----|
| intro | studio_blue.png | neutral | main_loop.mp3 | -- |
| crisis | alert_red.png | serious | tension_loop.mp3 | alert.wav |
| joke | comedy_bg.png | smile | comedy_loop.mp3 | punchline.wav |
| data | dark_board.png | explain | calm_loop.mp3 | -- |
| closing | studio_blue.png | neutral | main_loop.mp3 | -- |

### 6.2 テンプレート資産の蓄積モデル

| 制作回数 | テンプレート資産 | 効果 |
|---------|----------------|------|
| 1本目 | ゼロから作成 | 制作時間そのまま |
| 5本目 | 主要5種が揃う | 新規作成は例外場面のみ |
| 10本目 | 大半の場面をカバー | 10分あたりの摩擦が逓減 |

テンプレート資産が積み上がるほど、C-07 v3 の演出指示 → テンプレート選定の自動化精度も上がる。

### 6.3 自動化パイプライン詳細

```
[台本テキスト]
    | NLMYTGen build-csv
    v
[YMM4 CSV (キャラ名, セリフ)]
    |
    | NLMYTGen C-07 v3 (Custom GPT)
    v
[演出メモ (セクション別: パターン A/B/C/D, 表情, BGM, 素材調達)]
    |
    | NLMYTGen build-ymh (G-05, 新規)
    |   - 演出メモのパターン → テンプレート名にマッピング
    |   - テンプレート定義ファイルから背景/表情/BGM/SE を解決
    |   - YMovieHelper 入力形式 (CSV) に変換
    v
[YMovieHelper 入力 CSV (キャラ名, セリフ, 表情, 背景, BGM, SE)]
    |
    | YMovieHelper
    v
[ymmp (仮組立済み: 背景配置 + 表情設定 + BGM/SE)]
    |
    | YMM4 で開く
    v
[人手: 確認 + 微調整 (タイミング, カメラワーク, 即興演出)]
    |
    v
[動画出力]
```

### 6.4 NLMYTGen の責務境界

| 工程 | 担当 | 自動/手動 |
|------|------|----------|
| テンプレート定義の管理 | NLMYTGen (JSON ファイル) | ユーザーが定義を追加・編集 |
| 演出パターン → テンプレート名のマッピング | NLMYTGen (build-ymh) | 自動 |
| テンプレートから背景/表情/BGM/SE の解決 | NLMYTGen (build-ymh) | 自動 |
| YMovieHelper 入力形式への変換 | NLMYTGen (build-ymh) | 自動 |
| ymmp の生成 | YMovieHelper | 自動 |
| **素材ファイルの作成・収集** | **人間** | **手動** |
| **テンプレートの新規設計** | **人間** | **手動 (C-07 v3 が候補提案)** |
| **仮組立後の微調整** | **人間** | **手動** |

NLMYTGen はテンプレートの「提案と仮組立」までを担い、素材の「完全自動生成」には踏み込まない。

### 6.5 テンプレート管理方式 (G-02 結果で決定)

| 方式 | 内容 | 利点 | 欠点 |
|------|------|------|------|
| JSON 定義ファイル | `templates.json` にテンプレート名 → パスのマッピング | バージョン管理可能、Python で読み書き容易 | テンプレート追加時にファイル編集が必要 |
| ディレクトリ規約 | `templates/intro/`, `templates/crisis/` のフォルダ構造 | 直感的、素材ファイルも同梱 | 構造が大きくなりやすい |

YMovieHelper 側のテンプレート機構が存在すれば、それに乗る形が最も自然。G-02 の調査で判明する。

### 6.6 第二 (外部事前構築) と第四 (プラグイン) の使い分け

| 方式 | 役割 | 先着順 |
|------|------|--------|
| **第二 (外部事前構築)** | YMM4 を開く前に骨格を組む。テンプレート適用、素材パス解決、レイヤー配置 | **先に導入** (データ設計の問題、YMM4 本体を壊さない) |
| 第四 (プラグイン) | YMM4 内の反復作業を削る。無音カット、素材リンク修復、一括表示 | 後から足す (第二で足りない部分のみ) |

第二はデータ設計の問題なので失敗しても YMM4 を壊さない。第四は YMM4 内部に入るため保守が重い。従って第二を先に固める。

---

## Sources

- [YMM4 API Documentation](https://ymmapi.pages.dev/)
- [YMM4 Plugin Samples (GitHub)](https://github.com/manju-summoner/YukkuriMovieMaker4PluginSamples)
- [YMM4 Plugin Community (GitHub)](https://github.com/manju-summoner/YukkuriMovieMaker.Plugin.Community)
- [YMM4 Plugin 制作メモ (Zenn)](https://zenn.dev/inuinu/scraps/287c1d83e7f67c)
- [YMM4 プラグイン機構について (Gist)](https://gist.github.com/yuma140902/c0951ff8bc6ce824b5413c268ce4a83e)
- [AutoYukkuri - ymmp 自動生成 (GitHub)](https://github.com/akazdayo/AutoYukkuri)
- [KuchiPaku - リップシンク (GitHub)](https://github.com/InuInu2022/KuchiPaku)
- [YMM4 公式サイト](https://manjubox.net/ymm4/)
- [YMM4 Plugin Catalog](https://modurili.github.io/YMM4Plugin/)
- [YMM4 セリフ入力自動化 (Qiita)](https://qiita.com/akazdayo/items/946f76978935dda3e569)
