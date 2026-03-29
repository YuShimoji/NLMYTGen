# WORKFLOW: NotebookLM → YMM4 動画

NLMYTGen を使った動画制作の全工程。
各ステップの自動化レベルと今後の自動化候補は [AUTOMATION_BOUNDARY.md](AUTOMATION_BOUNDARY.md) を参照。

---

## 全体フロー

```
ステップ   内容                               操作     自動化レベル
S-1       NotebookLM ソース投入 + Audio生成   手動     L1 (将来: RSS連携)
S-2       台本テキスト取得                    手動     L1 (将来: API連携)
S-3       NLMYTGen CSV変換                   CLI自動  L2 (done)
S-4       YMM4 台本読込                      手動     L3 (YMM4側)
S-5       YMM4 演出・レンダリング             手動     L3 (YMM4内部で完結)
S-6       サムネイル作成                      手動     外部ツール (Python生成は禁止)
S-7       YouTube 投稿                       手動     L4 (将来: API連携)
```

### 高精度台本の取得について
NotebookLM に「音声解説の元の台本を出力してください」と依頼すると、音声書き起こしよりも誤字脱字が少なく、話者ラベル付きのクリーンな台本が得られる。これが現在の主導線 (S-2)。音声書き起こしは fallback。

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

## S-2: 台本テキスト取得

NotebookLM に「音声解説の元の台本を出力してください」と依頼し、台本テキストを取得する。

### 手順

1. Audio Overview が生成済みのノートブックを開く
2. チャットで「音声解説の元の台本を出力してください」と依頼
3. 出力されたテキストをコピーし `.txt` ファイルとして保存

### 出力形式
- 話者ラベル付き: `スピーカー1: テキスト` / `スピーカー2: テキスト`
- コピペ時に句読点や改行が分離することがある（パイプラインが自動結合する）

### 出力
- `.txt` ファイル (話者ラベル付き)

### Fallback: 音声書き起こし

元台本が取得できない場合は、Audio Overview の音声を書き起こす。

| ツール | 特徴 |
|--------|------|
| Google ドキュメント音声入力 | 無料、日本語対応 |
| Whisper (ローカル) | 高精度、オフライン可 |

この場合は話者ラベルなしになるため `--unlabeled` オプションを使用する。

---

## S-3: NLMYTGen で CSV 変換

### ラベル付き入力 (NotebookLM 元台本 — 主導線)

```bash
# CSV 生成（長文分割あり）
python -m src.cli.main build-csv input.txt \
  --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" \
  --max-length 80 \
  -o output.csv

# 確認 (dry-run + stats)
python -m src.cli.main build-csv input.txt \
  --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" \
  --max-length 80 \
  --dry-run --stats
```

### ラベルなし入力 (音声書き起こし fallback)

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
```

### オプション

| オプション | 説明 |
|-----------|------|
| `--unlabeled` | ラベルなし入力を行交互で 2 話者に割当 |
| `--speaker-map K=V,...` | 話者名を YMM4 キャラクター名に変換 |
| `--speaker-map-file PATH` | JSON or key=value ファイルから話者マップを読込 |
| `--merge-consecutive` | 同一話者の連続発話を結合 |
| `--max-length N` | N 文字超の発話を文末で分割 (推奨: 80) |
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

## S-5: YMM4 での演出・レンダリング

1. YMM4 でタイムライン上の発話を確認
2. 必要に応じて:
   - 発話テキストの修正 (音声認識の誤字)
   - タイミング調整
   - 立ち絵・表情の設定
   - 背景動画・画像の配置
   - エフェクト・トランジションの設定
3. 動画をエンコード・出力

### 自動化の余地
- YMM4 プロジェクトテンプレートで立ち絵・背景・レイアウトを定型化 → 毎回の手動設定を削減
- FEATURE_REGISTRY C-02〜C-05 を参照

---

## S-6: サムネイル作成（手動）

1. 動画の内容に合わせたサムネイルを作成
2. 外部ツール（Canva / Photoshop 等）で制作

**注:** Python での画像生成・合成は禁止（FEATURE_REGISTRY D-01: rejected）。サムネイル制作は外部画像ツールの責務。

---

## S-7: YouTube 投稿（手動 / 将来自動化）

1. 動画ファイルを YouTube にアップロード
2. タイトル・説明・タグ・サムネイルを設定
3. 公開設定

### 自動化の余地
- YouTube Data API v3 で投稿自動化 (FEATURE_REGISTRY E-01)
- メタデータのテンプレート生成 (FEATURE_REGISTRY E-02)

---

## 既知の制限

- `--unlabeled` は 2 話者固定 (Speaker_A / Speaker_B の交互)
- 短い行 (3文字以下) は前の行に自動結合される (音声認識の分断アーティファクト緩和)
- 句読点で終わる相槌 (「はい。」等) は独立発話として保持される (v0.4+)
- ラベル付きモードで話者タグにマッチしない行は直前の発話に結合される (コピペ改行崩れ対応)
- `--max-length` は文末 (。！？!?) でのみ分割する。文末のない長文はそのまま保持される
- コピペ由来の `,。` 等のアーティファクトは NLMYTGen では修正しない (YMM4 側で修正)
