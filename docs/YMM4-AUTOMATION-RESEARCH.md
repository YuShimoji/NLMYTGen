# YMM4 自動化調査 + 開発ロードマップ

> 2026-04-01 作成 / 2026-04-01 全面改訂 (第三次)

## 改訂メタ情報

このドキュメントは3回の調査と方針転換を経ている。今後のドリフトを防ぐため、経緯を明記する。

| 版 | 日付 | 主軸 | 転換理由 |
|----|------|------|---------|
| 初版 | 2026-04-01 | G-01 IToolPlugin spike | タイムライン操作 API が非公開で見通しが立たなかった |
| 第二次 | 2026-04-01 | YMovieHelper 連携 (G-02/G-05) | 既存ツール活用が現実的と判断 |
| **第三次 (現行)** | 2026-04-01 | **演出 IR + テンプレート資産** | YMovieHelper がサービス終了済み Web アプリで主軸に不適。ツール非依存の設計に転換 |

**現行方針:** 特定ツールに依存せず、NLMYTGen 独自の演出 IR (中間表現) を定義し、テンプレート資産の蓄積で制作を加速する。YMM4 への接続方式は IR 定義後に決定する。

---

## 目的

YMM4 の手動工程のうち、S-6 (背景/演出設定、制作時間の 70%以上) を減らす。
音声+字幕は build-csv + YMM4 台本読込で解決済み。残る課題は**背景/立ち絵/素材画像のタイムライン配置**。

YMM4 以外の動画制作パイプラインは検討対象外。

---

## 1. YMM4 の自動化経路: 調査結果

### 1.1 プラグイン API (公式)

YMM4 は v4.20.0.0 以降、公式プラグイン API を提供。

**公式ドキュメント:** https://ymmapi.pages.dev/

**プラグインの種類 (13種):** 映像エフェクト, 音声エフェクト, 図形, 立ち絵, 波形, 場面切り替え, 画像読込, 動画読込, 音声読込, 動画出力, 音声合成, テキスト補完, ツール (IToolPlugin)

**IToolPlugin の制約:**
- 独自ウィンドウは作成可能だが、**タイムラインやアイテムの直接操作 API は公開されていない**
- 内部 API アクセスは限定的 (バージョン情報, ディレクトリ, ログ程度)
- 開発環境に .NET 10 SDK + WPF が必要

**結論:** IToolPlugin は「YMM4 の中で動く独立ツール」であり、「タイムラインを操作する API」ではない。優先度最下位。

### 1.2 .ymmp 直接編集 (非公式だが実績あり)

**ファイル形式:** JSON (UTF-8 BOM)

**判明している構造:**

| タイプ | $type 値 | 主要プロパティ |
|--------|---------|---------------|
| VoiceItem | `...VoiceItem, YukkuriMovieMaker` | CharacterName, Serif, Hatsuon, Frame, Length |
| ImageItem | `...ImageItem, YukkuriMovieMaker` | FilePath |
| VideoItem | `...VideoItem, YukkuriMovieMaker` | FilePath |
| TachieItem | (未文書化) | (未確認) |

**参考実装:** AutoYukkuri (Python, VoiceItem のみ), KuchiPaku (C#, リップシンク)

**制約:**
- 音声は台本読込時に YMM4 が生成。外部から ymmp を作っても音声は生成されない
- スキーマ非公開。バージョンアップで構造変動リスク
- **ymmp 直接編集は控える** (過去にデッドファイルが蓄積した経験あり。完成品の解析研究のみ許容)

### 1.3 コマンドライン / 外部起動

**確認できず。** CLI 一括レンダリングも公式に記載なし。動画出力は GUI 操作が必要。

---

## 2. YMM4 周辺ツール群

### 2.1 既存ツール一覧

| ツール | 機能 | 位置づけ |
|--------|------|---------|
| **YMovieHelper** | CSV → ymmp 生成 (表情+動画切替対応) | **参照実装** (後述) |
| AoiSupport | 音声合成ソフト → YMM4 自動投入 | NLMYTGen 責務外 |
| YMM4 自動SE挿入 | AI 感情推定 → SE 自動挿入 | NLMYTGen 側対応不要 |
| AutoYukkuri | Whisper → ymmp 自動生成 (VoiceItem のみ) | ymmp 構造の参考 |
| ゆっくり自動化ツール | 台本 → 画像素材自動収集/配置 | 有償 (5万円)。技術非公開 |
| ジェットカット | 無音区間自動カット | 後工程効率化 |

### 2.2 YMovieHelper の位置づけ (重要: 勘違い防止)

YMovieHelper は調査の過程で「主軸候補」→「参照実装」へ二度格下げされた。混同を防ぐため経緯を明記する。

**事実:**
- YMM4 公式サイトで「CSV 台本から ymmp を生成、立ち絵表情変更・動画切替に対応」と紹介されている
- YMovieHelperLocal (ローカル版) は GitHub に存在する (https://github.com/itkmaingit/YMovieHelperLocal)

**問題:**
- 元サービスは **2024年5月31日にサービス終了**
- ローカル版は **Web アプリ** (Docker + WSL + Go + TypeScript、localhost:3000 でブラウザアクセス)。CLI ツールではない
- 7 stars / 16 commits。メンテナンスはほぼ停止
- 具体的な CSV 入力形式・ymmp 生成ロジックの詳細は確認できていない

**結論:**
- **採用対象ではない。** サービス終了済み Web アプリを NLMYTGen の主軸にするリスクは高すぎる
- **参照実装として扱う。** 「文字列で演出を指定し、テンプレート化して ymmp を生成する」という設計思想は回収する価値がある
- ツール自体への依存は作らない。NLMYTGen 独自の演出 IR を定義し、接続先はその後に決める

**今後のドキュメントで YMovieHelper に言及する際のルール:**
- 「YMovieHelper を使う」「YMovieHelper に接続する」とは書かない
- 「YMovieHelper の設計思想を参考にする」「参照実装として観察する」と書く
- build-ymh (YMovieHelper 入力変換) は廃止。代わりに build-ir (演出 IR 生成) を検討する

### 2.3 YMM4 公式自動化経路

| 系統 | 方式 | 堅牢性 | NLMYTGen の対応 |
|------|------|--------|----------------|
| 1. 台本インポート | CSV/TXT → YMM4 台本読込 | 高 | **build-csv で対応済み** |
| 2. 外部事前構築 | 演出 IR → (変換器) → ymmp | 未確定 | **演出 IR 定義が先** |
| 3. 外部音声連携 | AoiSupport 等 → YMM4 | 高 | NLMYTGen 責務外 |
| 4. プラグイン拡張 | IToolPlugin | 低 | 優先度最下位 |

---

## 3. 自動化戦略: 演出 IR + テンプレート

### 3.1 演出 IR (中間表現) とは

台本から抽出した演出指示を、YMM4 にも特定ツールにも依存しない構造化データとして表現するもの。

**語彙:**

| フィールド | 意味 | 例 |
|-----------|------|-----|
| template | 場面テンプレート名 | intro, crisis, joke, data, closing |
| face | 表情 | neutral, serious, surprised, smile, angry |
| bg | 背景 | studio_blue, dark_board, oil_map |
| slot | 配置位置 (意味ラベル) | right, left, center |
| motion | アニメーション | pop_in, slide_in, shake_small |
| overlay | オーバーレイ素材 | arrow_red, flash_red |
| se | 効果音 | tension_hit, punchline |

**設計原則:**
- LLM は意味ラベル (slot=right, face=surprised) だけを出力する。ピクセル座標 (x=1432) は出さない
- 座標変換はテンプレート定義側で解決する (slot=right → x=1500, y=220)
- テンプレート名で背景/表情/BGM/SE をまとめて呼び出す (映像編集版 CSS)

### 3.2 LLM の役割

| LLM が担当 | LLM が担当しない |
|-----------|----------------|
| 台本 → 演出タグ列の抽出 (分類問題) | ピクセル単位の配置 |
| テンプレートの選定 | YMM4 固有構造の正確な生成 |
| 表情/BGM/SE の判断 | ymmp の直接出力 |

**C-07 v3 → IR 出力への進化:**
現在の C-07 v3 は自然文の演出メモを出力。これを構造化 IR (CSV/JSON) に進化させることで、変換器やテンプレートエンジンが処理可能になる。

### 3.3 テンプレート資産の蓄積

| 制作回数 | テンプレート資産 | 効果 |
|---------|----------------|------|
| 1本目 | ゼロから作成 | 制作時間そのまま |
| 5本目 | 主要5種が揃う | 新規作成は例外場面のみ |
| 10本目 | 大半の場面をカバー | 10分あたりの摩擦が逓減 (約25%/10分) |

### 3.4 パイプライン

```
[台本テキスト]
    | NLMYTGen build-csv
    v
[YMM4 CSV] ---------> [YMM4 台本読込] -> 音声生成 + 字幕配置
    |
    | C-07 v4 (Custom GPT, 将来)
    v
[演出 IR (構造化 CSV/JSON)]
    |
    | テンプレート定義 (JSON) でスロット→座標、テンプレート名→素材パスを解決
    v
[解決済み演出データ]
    |
    | 接続方式 (ymmp 変換器 or 手動配置ガイド) -- 段階5で決定
    v
[YMM4 プロジェクト (背景+表情+素材 配置済み)]
    |
    v
[人手: 確認 + 微調整]
```

### 3.5 責務境界

| 工程 | 担当 | 自動/手動 |
|------|------|----------|
| 演出 IR の語彙定義 | NLMYTGen | 開発者 |
| 台本 → 演出 IR の生成 | LLM (Custom GPT) | 自動 |
| テンプレート定義の管理 | NLMYTGen (JSON) | ユーザーが追加・編集 |
| IR → YMM4 への接続 | 未決定 (段階5で判断) | -- |
| **素材ファイルの作成・収集** | **人間** | **手動** |
| **テンプレートの新規設計** | **人間** | **手動** |
| **仮組立後の微調整** | **人間** | **手動** |

---

## 4. 開発ロードマップ

| 段階 | 内容 | 成果物 | 前提 | 沼リスク |
|------|------|--------|------|---------|
| **1** | 演出 IR の語彙定義 | `docs/PRODUCTION_IR_SPEC.md` | なし | なし |
| **2** | YMM4 テンプレート資産の棚卸し | 既存素材一覧 (立ち絵差分, 背景, モーション) | ユーザー作業 | なし |
| **3** | 完成品 ymmp を1件解析 | ImageItem/TachieItem のキー構造メモ (1ページ) | ymmp サンプル1つ | **2ブロック制限** |
| **4** | C-07 v4: IR 出力プロンプト | Custom GPT が構造化 IR を出力 | 段階1 | なし |
| **5** | IR → YMM4 接続方式の決定 | ymmp 変換器を作るか手動配置維持かの判断 | 段階3,4 | 判断のみ |
| **6** | 変換器実装 or 手動配置最適化 | 段階5の判断による | 段階5 | 段階5で制御 |

### 成熟段階モデル (2026-04-02 追加)

開発ロードマップの段階1-6は「何を作るか」の順序。成熟段階は「どこまで動くか」の位相。

| Level | 名称 | 定義 | 現状 |
|-------|------|------|------|
| 0 | 構造把握 | ymmp の可変点を把握する研究段階 | **完了** (G-02b) |
| 1 | 限定変換器 | 安全な属性 (face/bg) のみを差し替える限定実用 | **到達済み** (G-06 実機検証 OK) |
| 2 | 演出IR適用エンジン | IR の全フィールドを系統的に ymmp へ解決する | **形成中** (IR v1.0 done / 適用 partial / proof 未実施) |
| 3a | face+bg 限定 E2E | build-csv → Custom GPT → IR → patch-ymmp → YMM4 が1本の台本で通る | **次の目標** |
| 3b | 拡張 E2E | slot/motion/transition を含む全パイプラインが通る | frontier |
| 4 | 制作標準装備 | 複数ケースで安定し、微修正中心で回る | 未到達 |

task 提案や feature 提案は、どの Level を拡張/形成/proof するのかをラベル付けすること。

### 各段階の詳細

**段階1 (演出 IR 語彙定義):** template / face / bg / slot / motion / overlay / se の最小語彙を定義。YMM4 にもツールにも依存しない。Python コード変更なし。

**段階2 (テンプレート資産棚卸し):** ユーザー作業。既存の立ち絵差分、背景画像、モーションセットを列挙し、段階1の語彙にマッピング。

**段階3 (ymmp 解析):** 完成品 ymmp を1件だけ開き、ImageItem / TachieItem のキー構造を確認。「背景と表情がどのキーで記述されているか」を1ページ以内にまとめる。自前生成には進まない。INVARIANTS の2ブロック制限を適用。

**段階4 (C-07 v4):** C-07 v3 の自然文演出メモを、構造化 IR (CSV/JSON) 出力に進化させる。Custom GPT の Instructions 更新。

**段階5 (接続方式決定):** 段階3の ymmp 構造と段階4の IR 出力を照合し、「IR → ymmp 変換器を Python で作れるか」を判断。作れるなら段階6で実装。作れない (構造が複雑すぎる / リスクが高い) なら、手動配置ガイドとして IR を活用する。

**段階6 (実装):** 段階5の判断に従う。

---

## 5. 作業時間の実態

| 工程 | 10分動画あたり | 自動化後の見込み |
|------|-------------|----------------|
| S-3 CSV 変換 | 5分 | 変わらず |
| S-4 台本読込 | 5分 | 変わらず |
| S-5 読み上げ確認 | 30分~1時間 | B-17 で改善済み |
| **S-6 背景・演出設定** | **3~5日** | **演出 IR + テンプレートで半自動化目標** |
| S-7 最終確認 | 30分 | 変わらず |
| S-8 サムネイル | 1~2時間 | C-08 で判断支援済み |
| S-9 YouTube 投稿 | 15分 | E-01 で自動化目標 |

---

## 6. NotebookLM 自動化について

NLMYTGen は「台本ができた後」の工程に専念。台本入手の自動化は別システム。
詳細は project-context.md の DECISION LOG を参照。

---

## 7. YMM4 機能の実測/推測/未確認 棚卸し (2026-04-02)

三者分担 (Writer IR / Template Registry / YMM4 Adapter) の設計前提を確認するための棚卸し。
「確認できた事実」と「まだ仮説にすぎないこと」を混在させない。

### 実測済み (事実として確定)

- ymmp は JSON (UTF-8 BOM)。Timeline.Items[] にフラットなアイテムリスト
- VoiceItem が TachieFaceParameter を持ち、発話ごとに表情パーツファイルパスで指定 (G-02b)
- face パーツ (Eye/Mouth/Body) の Python 書き換えで YMM4 が正常動作 (G-06 実機検証 2026-04-02)
- bg (ImageItem/VideoItem Layer 0) の差し替え + Frame/Length 再配置が正常動作 (G-06)
- TachieItem は動画全体でキャラごとに1件。X: -737 (left) / +708 (right) で配置
- ymmp 内にテンプレート参照キーは存在しない。展開後の値が格納される
- YMM4 のアイテムテンプレートはグローバル設定 (`YMM4フォルダ/user/setting/`)
- テンプレートのインポート/エクスポートボタンが存在 (v4.29.0.0)
- テンプレートにショートカットキー割り当て可能 (v4.18.0.0)
- テンプレートのフォルダ分け管理が可能 (v3.9.9.147)
- 表情アイテムという独立アイテム種別が存在。ボイスアイテムから自動作成も可能 (v4.16.0.0)
- 台本読込 (CSV/TSV/TXT) でボイスアイテム一括生成
- 字幕ファイル (.srt/.sub) からアイテム一括追加が可能
- アイテム種別: VoiceItem, TextItem, VideoItem, ImageItem, AudioItem, 図形, 表情アイテム, EffectItem, GroupItem

### 推測だが有力

- テンプレートファイルは JSON 形式 (YMM4 の設定全般が JSON であるため)
- テンプレートに複数アイテムをバンドルできる (公式 FAQ に「テンプレートからアイテムを追加」の記述あり)
- エクスポートしたテンプレートファイルを Python で読み書きできる可能性が高い
- テンプレートダブルクリックでタイムラインに追加 (v4.29.0.0 リリースノート)

### 未確認なので実測が必要

| 項目 | 影響範囲 | 優先度 |
|------|---------|--------|
| テンプレートファイルのエクスポート形式 (拡張子、内部構造) | Adapter の責務範囲が確定しない。native template に委ねられる範囲が不明 | **最優先** |
| テンプレートに含められるアイテムの種類と構成 | scene_preset バンドルの実現可能性 | 高 |
| 表情アイテムの ymmp JSON 構造 | face 差し替えの代替経路 (TachieFaceParameter 直接 vs 表情アイテム挿入) | 高 |
| VideoEffects 配列の $type ごとの内部構造 | motion/transition/bg_anim を Adapter で解決できるかの判断 | 中 |
| GroupItem の内部構造 | バンドル生成時のグループ化可能性 | 低 |

---

## Sources

- [YMM4 API Documentation](https://ymmapi.pages.dev/)
- [YMM4 Plugin Samples (GitHub)](https://github.com/manju-summoner/YukkuriMovieMaker4PluginSamples)
- [YMM4 Plugin 制作メモ (Zenn)](https://zenn.dev/inuinu/scraps/287c1d83e7f67c)
- [AutoYukkuri (GitHub)](https://github.com/akazdayo/AutoYukkuri)
- [YMovieHelperLocal (GitHub)](https://github.com/itkmaingit/YMovieHelperLocal) -- 参照実装。採用対象ではない
- [YMM4 公式サイト](https://manjubox.net/ymm4/)
- [YMM4 Plugin Catalog](https://modurili.github.io/YMM4Plugin/)
- [YMM4 セリフ入力自動化 (Qiita)](https://qiita.com/akazdayo/items/946f76978935dda3e569)
