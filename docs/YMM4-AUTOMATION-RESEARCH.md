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

## 2. 自動化戦略

### 2.1 二段階アプローチ

**Phase A: プラグイン API 経由 (推奨、先行)**

IToolPlugin で「演出適用ツール」を作成し、YMM4 内部から実行する方式。

```
[C-07 v3 演出メモ] → [演出適用ツール (IToolPlugin)] → [YMM4 タイムライン]
```

- C-07 v3 の出力 (JSON/テキスト) をツールプラグインが読み込む
- プラグイン内から YMM4 の内部機能にアクセスできる範囲で適用
- タイムライン直接操作 API がなくても、WPF UI オートメーションや
  IPC で外部プロセスと連携する余地がある

**Phase B: ymmp 直接編集 (補完、後続)**

プラグイン API でカバーできない部分を ymmp 編集で補完する。

```
[台本読込 (YMM4)] → [ymmp 保存] → [Python スクリプトで背景/表情差し替え] → [YMM4 で開き直し]
```

- 台本読込後の ymmp を Python で開き、背景画像パスや表情パラメータを差し替え
- 音声は台本読込時に生成済みなので、差し替え後も音声は維持される
- スキーマ変更リスクがあるため、バージョン検出 + バリデーションを組み込む

### 2.2 対応する手動工程と自動化可能性

| S-6 工程 | 手動作業 | Phase A (プラグイン) | Phase B (ymmp 編集) |
|----------|---------|---------------------|-------------------|
| **S-6a 背景配置** | トピックに合う背景画像を探し配置 | C-07 v3 の素材調達ガイドを表示 | 背景画像パスを ymmp に書き込み |
| **S-6b Animation** | Ken Burns の方向・速度設定 | エフェクトパラメータの自動設定 | エフェクト JSON を ymmp に追記 |
| **S-6c 表情切替** | 発話内容に応じた表情選択 | C-07 v3 の表情指示を表示 | TachieItem のパラメータ差し替え |
| **S-6d BGM** | 雰囲気に合う BGM 選定 | BGM キーワード表示 | BGM ファイルパスを ymmp に追記 |
| **S-6e SE** | 効果音配置 | -- | SE アイテムを ymmp に追加 |
| **S-6f トランジション** | 背景切替時のフェード設定 | ITransitionPlugin で自動適用 | トランジション JSON を追記 |

---

## 3. 開発ロードマップ

### 全体像

| 優先度 | ID | 内容 | 経路 | 規模 | 前提 |
|--------|----|------|------|------|------|
| **1** | G-01 | YMM4 プラグイン feasibility spike | プラグイン API | 小 | .NET 10 SDK 環境構築 |
| **2** | G-02 | ymmp 構造解析 + スキーマ文書化 | ymmp 直接編集 | 小 | ユーザーから .ymmp サンプル提供 |
| **3** | G-03 | 演出適用ツール (IToolPlugin) | プラグイン API | 中 | G-01 の結果次第 |
| **4** | G-04 | ymmp 背景/表情自動差し替えスクリプト | ymmp + Python | 中 | G-02 の構造解析完了 |
| **5** | E-01+E-02 | YouTube 投稿 + メタデータ自動化 | YouTube API | 中 | stdlib 緩和 ADR |
| **6** | B-17+ | 字幕リフロー微調整 | 既存 Python | 小 | なし |

### G-01: YMM4 プラグイン feasibility spike (最優先)

**目的:** IToolPlugin で何ができるかを実機検証する。

**成果物:**
- 最小限の IToolPlugin (.NET / C#) をビルドし、YMM4 にロードして動作確認
- タイムラインへのアクセス可否を確認
- IPC 経由で Python プロセスと通信できるか確認
- C-07 v3 の演出メモを読み込んで表示する最小プロトタイプ

**判断:**
- タイムライン操作が可能 → G-03 (演出適用ツール) へ進む
- タイムライン操作が不可能 → G-02 (ymmp 直接編集) を主経路に切り替え

### G-02: ymmp 構造解析 + スキーマ文書化

**目的:** ymmp の JSON 構造を完全に把握し、Python から安全に編集できるようにする。

**成果物:**
- 台本読込後の ymmp サンプルから全フィールドを抽出
- VoiceItem, ImageItem, VideoItem, TachieItem の完全スキーマ
- 背景画像差し替えの PoC (Python スクリプト)
- 表情パラメータ差し替えの PoC

### G-03: 演出適用ツール (IToolPlugin)

**目的:** C-07 v3 の演出メモを YMM4 内で読み込み、半自動で適用するツール。

**想定フロー:**
1. Custom GPT で演出メモを生成 (既存)
2. 演出メモを JSON 形式でエクスポート
3. YMM4 のツールメニューから「演出適用」を選択
4. プラグインが演出メモを読み込み、背景/表情/BGM の候補を提示
5. ユーザーが確認 → 一括適用

### G-04: ymmp 背景/表情自動差し替え

**目的:** 台本読込後の ymmp を Python で開き、C-07 v3 の指示に基づいて背景/表情を差し替え。

**想定フロー:**
1. YMM4 で台本読込 → 音声生成 → ymmp 保存
2. Python: ymmp を読み込み + C-07 v3 演出メモを読み込み
3. Python: 各セクション境界で背景 ImageItem を挿入
4. Python: 各発話の TachieItem パラメータを表情指示に合わせて変更
5. YMM4 で ymmp を開き直し → 確認 → 微調整

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
