# WORKFLOW: NotebookLM → YMM4 動画

NLMYTGen を使った動画制作の全工程。

---

## 全体フロー

```
S-1  NotebookLM でソースを投入し Audio Overview を生成
S-2  Audio Overview をテキストに書き起こす (文字起こしツール)
S-3  書き起こしテキストを NLMYTGen で YMM4 CSV に変換
S-4  YMM4 で CSV を台本読込
S-5  YMM4 で音声合成・字幕配置・動画レンダリング
```

---

## S-1: NotebookLM Audio Overview 生成

1. https://notebooklm.google.com/ でノートブックを作成
2. ソース素材 (PDF, URL, テキスト等) を投入
3. Audio Overview を生成 (2人のナレーターによる対話形式)
4. 生成された音声を保存

### 出力
- 音声ファイル (mp3)
- 2人のナレーターによる対話 (テンポ・個性は NotebookLM が生成)

---

## S-2: テキスト書き起こし

Audio Overview の音声をテキストに書き起こす。

### 方法

| ツール | 特徴 |
|--------|------|
| NotebookLM のテキスト表示 | 要約であり完全な書き起こしではない場合がある |
| Google ドキュメント音声入力 | 無料、日本語対応 |
| Whisper (ローカル) | 高精度、オフライン可 |

### 注意点
- NotebookLM の Audio Overview 書き起こしは通常**話者ラベルなし**
- 2話者が行ごとに交互発話する形式になる
- 音声認識の精度により誤字・分断が含まれる

### 出力
- `.txt` ファイル (話者ラベルなし or ラベル付き)

---

## S-3: NLMYTGen で CSV 変換

### ラベルなし入力 (実際の NotebookLM 書き起こし)

```bash
# 話者マップを先に生成 (テンプレート)
python -m src.cli.main generate-map input.txt --unlabeled --format json > speaker_map.json

# speaker_map.json を編集: Speaker_A/Speaker_B を YMM4 キャラクター名に変更
# 例: {"Speaker_A": "れいむ", "Speaker_B": "まりさ"}

# CSV 生成
python -m src.cli.main build-csv input.txt \
  --unlabeled \
  --speaker-map-file speaker_map.json \
  -o output.csv

# 確認 (dry-run + stats)
python -m src.cli.main build-csv input.txt \
  --unlabeled \
  --speaker-map-file speaker_map.json \
  --dry-run --stats
```

### ラベル付き入力 (手動で話者タグを付けた場合)

```bash
python -m src.cli.main build-csv input.txt \
  --speaker-map "ナレーター1=れいむ,ナレーター2=まりさ" \
  -o output.csv
```

### オプション

| オプション | 説明 |
|-----------|------|
| `--unlabeled` | ラベルなし入力を行交互で 2 話者に割当 |
| `--speaker-map K=V,...` | 話者名を YMM4 キャラクター名に変換 |
| `--speaker-map-file PATH` | JSON or key=value ファイルから話者マップを読込 |
| `--merge-consecutive` | 同一話者の連続発話を結合 |
| `--dry-run` | プレビューのみ (CSV 書き出しなし) |
| `--stats` | 話者ごとの発話統計を表示 |
| `-o PATH` | 出力 CSV パス (省略時: 入力ファイル名_ymm4.csv) |

### 出力
- YMM4 CSV: 2列 (キャラクター名, テキスト)、ヘッダーなし、UTF-8 (BOM 付き / utf-8-sig)

---

## S-4: YMM4 台本読込

1. YMM4 (ゆっくりMovieMaker4) を起動
2. プロジェクトを新規作成または開く
3. キャラクターを追加 (CSV の話者名と一致させる)
   - 例: 「れいむ」「まりさ」
4. **メニュー: ツール → 台本読み込み** (「ファイル」メニューではない)
5. 台本編集ウィンドウが表示される
6. CSV ファイルを選択して読み込む
7. キャラクター割り当てを確認/調整
8. 「タイムラインに追加」でボイスアイテムとして一括配置

### 注意点
- 台本読込は **ツール** メニューにある。「ファイル → プロジェクトを開く」ではない
- CSV の話者名が YMM4 のキャラクター名と**完全一致**する必要がある
- 不一致の場合は、台本読込 UI でドロップダウンから手動割り当てが可能
- `generate-map` で事前にマップテンプレートを作り、キャラクター名を合わせること

### 対応ファイル形式
| 形式 | 拡張子 | フォーマット |
|------|--------|------------|
| CSV | .csv | `キャラ名,セリフ` |
| TSV | .tsv | `キャラ名[TAB]セリフ` |
| TXT | .txt | `キャラ名「セリフ」` |

---

## S-5: 動画レンダリング

1. YMM4 でタイムライン上の発話を確認
2. 必要に応じて:
   - 発話テキストの修正 (音声認識の誤字)
   - タイミング調整
   - 立ち絵・背景の設定
3. 動画をエンコード・出力

---

## 既知の制限

- `--unlabeled` は 2 話者固定 (Speaker_A / Speaker_B の交互)
- 短い行 (3文字以下) は前の行に自動結合される (音声認識の分断アーティファクト緩和)
- 句読点で終わる相槌 (「はい。」等) は独立発話として保持される (v0.4+)
- 音声認識の誤字は NLMYTGen では修正しない (YMM4 側で修正)
