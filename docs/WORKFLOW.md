# WORKFLOW: NotebookLM → YMM4 ゆっくり解説動画

NLMYTGen を使った動画制作の全工程。
NLMYTGen (Python) は S-3 (CSV変換) を担当し、S-6 の演出設定を演出 IR + LLM プロンプト (C-07/G-05) で支援する。
音声・字幕投入は YMM4 台本読込が不動の主経路。
各ステップの自動化レイヤーは [AUTOMATION_BOUNDARY.md](AUTOMATION_BOUNDARY.md) を参照。

---

## 全体フロー

```
フェーズ       ステップ   内容                             操作           担当
──────────────────────────────────────────────────────────────────────────────
[準備]         S-0       YMM4 テンプレート構築             手動(初回のみ) YMM4
[台本制作]     S-1       NotebookLM ソース投入 + Audio     手動操作       NotebookLM
               S-2       台本テキスト取得                  手動操作       NotebookLM
               S-3       CSV変換                          GUI（NLMYTGen） NLMYTGen
[YMM4取込]     S-4       台本読込                         手動操作       YMM4
[仕上げ]       S-5       読み上げ確認・テキスト修正        手動操作       YMM4
               S-6       背景・演出設定                    手動操作       YMM4
               S-7       最終確認・レンダリング            手動操作       YMM4
[公開]         S-8       サムネイル制作                    手動操作       YMM4 + 外部
               S-9       YouTube 投稿                     手動操作       YouTube
```

### 各ステップで何が起きるか


| ステップ    | ユーザーが行う操作             | ツールが自動処理すること                  |
| ------- | --------------------- | ----------------------------- |
| S-1     | ソース投入 + 生成ボタン         | NotebookLM が対話台本のコンテンツを生成     |
| S-2     | プロンプト入力 + テキストのコピー・保存 | NotebookLM が台本テキストを出力         |
| S-3     | NLMYTGen GUI（CSV 変換タブ） | NLMYTGen が話者分離・マッピング・分割・CSV生成 |
| S-4     | メニュー操作 + ファイル選択 + ボタン | YMM4 が全発話の音声合成 + 字幕配置を一括処理    |
| S-5〜S-9 | 全て手動操作                | --                            |


### NLMYTGen の責務範囲

NLMYTGen は以下を担当する:

- **S-3 (テキスト→CSV変換)**: 台本テキストを YMM4 CSV に変換する (実装済み)
- **S-6 支援 (三層責務構造)**:
  - **Writer IR** (第1層): Custom GPT が台本から演出 IR (scene_preset + override) を出力 (G-05 done)。G-24 skit_group actor を使う発話は `motion_target: "layer:9"` と v1/alias intent を出す
  - **Template Registry** (第2層): 制作環境の再利用資産辞書 (face_map/bg_map/slots/se_map + YMM4 native template 名参照)。skit_group は registry で exact / fallback / manual_note を解決し、template 本体は repo-tracked `.ymmp` template source から読む
  - **YMM4 Adapter** (第3層): IR + Registry → ymmp の接着。face/bg の差し替えに加え、skit_group は template source の GroupItem を対象発話の timeline へ自動配置する。`audit-skit-group` は補助 preflight であり成果本体ではない
  - 詳細: [PRODUCTION_IR_SPEC.md](PRODUCTION_IR_SPEC.md) セクション6、[AUTOMATION_BOUNDARY.md](AUTOMATION_BOUNDARY.md) 三層責務構造

S-0, S-4〜S-9 の実操作は全て YMM4 または外部ツールの手動操作である。
このワークフロー文書は、NLMYTGen のスコープ外であっても動画制作に必要な全工程をカバーする。

---

## S-0: YMM4 プロジェクトテンプレート構築 (初回のみ)

最初に一度だけ行う。以降の動画制作は全てこのテンプレートを複製して開始する。

### a. キャラクター追加

1. YMM4 を起動し、新規プロジェクトを作成
2. キャラクターを追加 (例: 「れいむ」「まりさ」)
3. 各キャラクターのボイス設定:
  - 音声エンジン (VOICEVOX / CoeFont / AquesTalk 等)
  - キャラクター音声の選択
  - 速度・ピッチ・音量の調整
  - 必要に応じてイントネーション調整

### b. 立ち絵設定

1. 立ち絵セットを読み込む (素材配布サイトから入手)
2. 表情パターンの設定:
  - 通常 / 笑顔 / 驚き / 悲しみ / 怒り / 考え中 等
  - 各表情のパーツ組み合わせを登録
3. 立ち絵の表示位置・サイズを調整
  - れいむ: 画面左下
  - まりさ: 画面右下

### c. 字幕スタイル

1. フォント選択 (視認性の高いゴシック系)
2. 文字サイズ (画面に対して適切なサイズ)
3. 文字色 (キャラクターごとに色分け)
4. 縁取り (黒縁等で背景上の視認性を確保)
5. 表示位置 (画面下部中央が標準)
6. 表示幅を確認し、長文がはみ出さない設定にする

### d. プロジェクト設定

- 解像度: 1920x1080 (フルHD)
- FPS: 30
- デフォルト背景画像の設定

### e. BGM テンプレート

- 汎用BGMを配置 (フリー素材等)
- ループ設定
- 音量バランス (ボイスの邪魔にならないレベル)

### f. テンプレートとして保存

- YMM4 のプロジェクトファイルとして保存
- 以降の動画制作では、このファイルを複製して使う
- キャラクター設定・字幕スタイル・立ち絵設定が全て引き継がれる

---

## S-1: NotebookLM Audio Overview 生成

1. [https://notebooklm.google.com/](https://notebooklm.google.com/) でノートブックを作成
2. ソース素材 (PDF, URL, テキスト等) を投入
3. Audio Overview を生成 (2人のナレーターによる対話形式)
4. 生成された音声を保存

### 出力

- 音声ファイル (mp3)
- 2人のナレーターによる対話 (テンポ・個性は NotebookLM が生成)

---

## S-2: 台本テキスト取得

NotebookLM に「音声解説の元の台本を出力してください」と依頼し、台本テキストを取得する。
これが主導線。ただし NotebookLM 出力は低信頼入力として扱う。誤字・誤変換・話者役割の崩れがそのまま CSV / IR に伝播するため、保存後に B-18 `diagnose-script` または C-09 constrained rewrite / manual QC を挟み、未確認のまま直接 IR 化しない。

### 手順

1. Audio Overview が生成済みのノートブックを開く
2. チャットで「音声解説の元の台本を出力してください」と依頼
3. 出力されたテキストをコピーし `.txt` ファイルとして保存
4. `diagnose-script` で話者マップ・NLM臭・役割崩れを確認し、必要なら事実を変えずに誤字・誤変換だけ補正する

### 出力形式

- 話者ラベル付き: `スピーカー1: テキスト` / `スピーカー2: テキスト`
- コピペ時に句読点や改行が分離することがある (パイプラインが自動結合する)

### Fallback: 音声書き起こし

元台本が取得できない場合は、Audio Overview の音声を書き起こす。


| ツール               | 特徴         |
| ----------------- | ---------- |
| Google ドキュメント音声入力 | 無料、日本語対応   |
| Whisper (ローカル)    | 高精度、オフライン可 |


この場合は話者ラベルなしになるため `--unlabeled` オプションを使用する。

---

## S-3: NLMYTGen で CSV 変換

### GUI での操作（制作時の標準手順）

1. NLMYTGen GUI を起動（`start-gui.bat`）
2. CSV 変換タブで台本 `.txt` をドラッグ&ドロップ（またはファイル選択）
3. 設定を確認:
   - **Speaker Map**: `スピーカー1=れいむ,スピーカー2=まりさ`（台本の話者名に合わせる）
   - **Max Lines**: `2`（2行字幕）
   - **Chars/Line**: `20`〜`40`（字幕幅に合わせる）
   - **自然改行（balance-lines）**: ON（Max Lines 指定時のみ有効）
   - **Reflow v2**: ON
4. **Dry Run** で行数・話者・話者統計とはみ出し候補を確認
5. **Build CSV** で書き出し

### CLI リファレンス（開発・デバッグ用）

GUI が標準。コマンド索引・pytest: [dev/CLI_REFERENCE.md](dev/CLI_REFERENCE.md)。手元用 `build-csv` 例:

```bash
python -m src.cli.main build-csv input.txt \
  --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" \
  --max-lines 2 --chars-per-line 40 --balance-lines \
  -o output.csv
```

### オプション


| オプション                     | 説明                                                                                                   |
| ------------------------- | ---------------------------------------------------------------------------------------------------- |
| `--unlabeled`             | ラベルなし入力を行交互で 2 話者に割当                                                                                 |
| `--speaker-map K=V,...`   | 話者名を YMM4 キャラクター名に変換                                                                                 |
| `--speaker-map-file PATH` | JSON or key=value ファイルから話者マップを読込                                                                     |
| `--merge-consecutive`     | 同一話者の連続発話を結合                                                                                         |
| `--max-length N`          | N 文字超の発話を文末で分割 (推奨: 80)                                                                              |
| `--display-width`         | `--max-length` の値を表示幅 (全角=2, 半角=1) で判定                                                               |
| `--max-lines N`           | 表示幅ベースで N 行以内に収まるよう分割 (`--chars-per-line` と併用)                                                       |
| `--chars-per-line N`      | 1行あたりの表示幅 (デフォルト: 40、`--max-lines` 使用時)                                                              |
| `--balance-lines`         | 2行字幕向けに自然な改行を入れつつ、句読点の少ない長文の節分割、短すぎる最終行回避、長い一文の aggressive chunking を行う opt-in 改善 (`--max-lines` 必須) |
| `--dry-run`               | プレビューのみ (CSV 書き出しなし)                                                                                 |
| `--stats`                 | 話者ごとの発話統計 + はみ出し候補警告を表示                                                                              |
| `-o PATH`                 | 出力 CSV パス (省略時: 入力ファイル名_ymm4.csv)                                                                    |


### 出力

- YMM4 CSV: 2列 (キャラクター名, テキスト)、ヘッダーなし、UTF-8 (BOM 付き / utf-8-sig)

---

## S-4: YMM4 台本読込

1. S-0 で作成したテンプレートプロジェクトを**複製**して開く
2. キャラクターが CSV の話者名と一致していることを確認
3. **メニュー: ツール → 台本読み込み** (「ファイル」メニューではない)
4. 台本編集ウィンドウで CSV ファイルを選択して読み込む
5. キャラクター割り当てを確認/調整
6. 「タイムラインに追加」で全発話をボイスアイテムとして一括配置

### 注意点

- 台本読込は **ツール** メニューにある。「ファイル → プロジェクトを開く」ではない
- CSV の話者名が YMM4 のキャラクター名と**完全一致**する必要がある
- 不一致の場合は、台本読込 UI でドロップダウンから手動割り当てが可能
- **ymmp を直接編集しても音声は合成されない。** 音声合成は台本読込時に YMM4 が自動実行する

### 台本読込が対応するファイル形式


| 形式  | 拡張子  | フォーマット         |
| --- | ---- | -------------- |
| CSV | .csv | `キャラ名,セリフ`     |
| TSV | .tsv | `キャラ名[TAB]セリフ` |
| TXT | .txt | `キャラ名「セリフ」`    |


---

## S-5: 読み上げ確認・テキスト修正

台本読込後、音声合成結果を確認し、読み間違いや字幕の問題を修正する。
この工程が動画の聴覚的品質を決める。

### a. 読み間違いの確認と修正

1. タイムラインを再生し、読み間違い箇所をメモする
2. 修正方法:
  - **テキスト修正**: 該当アイテムのテキストを YMM4 上で直接修正 (例: 漢字→ひらがな)
  - **辞書登録**: YMM4 の辞書機能で固有名詞・専門用語の読みを登録 (繰り返し出る語に有効)

### b. 字幕の確認と調整

1. 各発話の字幕が画面内に収まっているか確認する
2. はみ出す場合の対処:
  - 文の途中で改行を入れる
  - 長文を2つのアイテムに分割する
  - 字幕の文字サイズ・表示幅を調整する (S-0 で設定済みの範囲で)
3. 字幕の表示タイミング (音声と字幕のずれがないか) を確認

### c. 不自然な間の修正

- NLMYTGen が分割した箇所で不自然な間が空く場合、アイテム間の空白を調整する
- 同一話者の連続発話間は短め、話者交代時はやや長めが自然

---

## S-6: 背景・演出設定

動画の視覚的品質を決める工程。S-0 のテンプレートをベースに、各動画固有の演出を設定する。

**視覚スタイル（挿絵コマ / 再現PV / 資料パネル）と演出 IR の対応**は [VISUAL_STYLE_PRESETS.md](VISUAL_STYLE_PRESETS.md) を参照。YMM4 側のテンプレ整備手順は [VISUAL_STYLE_YMM4_CHECKLIST.md](VISUAL_STYLE_YMM4_CHECKLIST.md)。

### a. 背景の配置

1. 動画のトピック構成に合わせて背景画像を配置する
2. 背景を切り替えるタイミング: トピックの変わり目、場面転換、強調したい箇所
3. 同じ背景が長時間続かないよう注意 (視聴者の飽き防止)

### b. 背景の Animation

1. 静止画の背景にパン・ズーム (Ken Burns エフェクト) を設定
2. ゆっくりとした動きで単調さを軽減
3. 動きの速度・方向はトピックの雰囲気に合わせる

公式・プラグイン・既知トラブル対策の参照用に、[verification/YMM4-bg-animation-operator-research-2026-04.md](verification/YMM4-bg-animation-operator-research-2026-04.md)（YMM4 オペレーション補遺）を利用できる。

### c. 立ち絵の表情切り替え

1. 発話の内容に合わせて表情を変更 (S-0 で設定したパターンから選択)
2. 全発話に同じ表情を使わない (単調な印象を避ける)
3. 強調・驚き・解説・まとめ等、場面に応じた表情の使い分け

### d. BGM

1. S-0 テンプレートの BGM を動画の雰囲気に合わせて差し替え (必要な場合)
2. フェードイン/フェードアウトの設定
3. 音量バランス: ボイスが明瞭に聞こえるレベルに調整

### e. SE (効果音)

- 場面転換、強調、ツッコミ等に SE を配置 (必要に応じて)
- 多用しすぎると騒がしくなるので注意

### f. skit_group actor template placement

配達員などの外部茶番劇演者を使う場合、実制作 IR の該当 utterance は `motion_target: "layer:9"` を持ち、`motion` は v1 intent または alias intent に限定する。最小入力形は `samples/g24_skit_group_minimal_production_ir.json`。

```bash
python -m src.cli.main patch-ymmp \
  samples/_probe/g24/real_estate_dx_csv_import_base.ymmp \
  samples/_probe/g24/real_estate_dx_skit_group_ir_aligned.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --skit-group-template-source samples/templates/skit_group/delivery_v1_templates.ymmp \
  --skit-group-only \
  -o samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp
```

`exact` / `fallback` は GroupItem 自動配置対象として扱う。`--skit-group-only` は face/bg/transition などの未解決をこの配置スライスから切り離す。YMM4 CSV 読込後に長文が分割される案件では aligned IR の `row_start` / `row_end` を使い、VoiceItem 順の `index` 直置きでズレたまま配置しない。`panic_shake` 等の未登録 intent は通常語彙から除外し、strict validation では ERROR にする。template source に存在しない将来テンプレートは `SKIT_TEMPLATE_SOURCE_MISSING` として fail-fast し、手順票で埋め合わせない。

read-only 確認が必要な場合だけ `audit-skit-group` を使う。ただし preflight PASS は制作成果ではなく、成果認定は patched `.ymmp` に GroupItem が挿入されたこととする。

### g. トランジション

- 背景の切り替え時にトランジション (フェード、スライド等) を設定
- ゆっくり解説では控えめなトランジションが標準

---

## S-7: 最終確認・レンダリング

### a. 全体通しプレビュー

動画を最初から最後まで通して再生し、以下を確認する:

- 読み間違いが残っていないか
- 字幕が全て画面内に収まっているか
- 背景の切り替えタイミングが適切か
- BGM と音声のバランスが良いか
- 不自然な間や無音区間がないか
- 立ち絵の表情が場面に合っているか

### b. レンダリング

1. 出力設定:
  - コーデック: H.264 (YouTube 推奨)
  - 解像度: 1920x1080
  - ビットレート: YouTube の推奨値に準拠
2. エンコードを実行
3. 出力された動画ファイルを再生して最終確認

---

## S-8: サムネイル制作

YouTube 動画のクリック率を最も左右する要素。テンプレートをベースに毎回カスタマイズする。

### 基本方針

- **YMM4 で作成したテンプレートの文字・画像を入れ替えて制作する**
- 機械的に背景画像を設定して文字を入れるだけのものは不可
- 毎回の動画内容に合わせた手動カスタマイズが必要

### ゆっくり解説サムネイルの基本構成

1. **タイトル文字**: 動画の内容を端的に伝えるキャッチコピー (大きく・目立つ色・縁取り)
2. **キャラクター立ち絵**: メインキャラの表情付き立ち絵 (驚き・興味等の目を引く表情)
3. **背景**: トピックに関連する画像 (暗め or ぼかしでタイトル文字の可読性を確保)

### テンプレート運用

再現用の **1 枚チェックリスト**は [THUMBNAIL_ONE_SHEET_WORKFLOW.md](THUMBNAIL_ONE_SHEET_WORKFLOW.md) を参照。

1. YMM4 でサムネイルテンプレートを作成 (本プロジェクトは YMM4 完結方針。Canva は使わない)
2. 動画ごとにテンプレートを開き、以下を入れ替え:
  - タイトル文字
  - キャラクターの表情
  - 背景画像
3. レイアウト・フォント・色使いはテンプレートで統一感を維持

---

## S-9: YouTube 投稿

1. 動画ファイルを YouTube にアップロード
2. タイトル・説明・タグ・サムネイルを設定
3. 公開設定

---

## 既知の制限

- `--unlabeled` は 2 話者固定 (Speaker_A / Speaker_B の交互)
- 短い行 (3文字以下) は前の行に自動結合される (音声認識の分断アーティファクト緩和)
- 句読点で終わる相槌 (「はい。」等) は独立発話として保持される (v0.4+)
- ラベル付きモードで話者タグにマッチしない行は直前の発話に結合される (コピペ改行崩れ対応)
- `--max-length` は文末 (。!?!?) でのみ分割する。文末のない長文はそのまま保持される
- コピペ由来の `,。` 等のアーティファクトは NLMYTGen では修正しない (YMM4 側で修正)
