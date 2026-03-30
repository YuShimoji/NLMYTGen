# PIPELINE SPEC

## 入力仕様

### 受け付けるフォーマット

#### CSV (.csv)
- 2列: 話者名, テキスト
- ヘッダー行なし (ヘッダーがある場合は自動スキップ)
- UTF-8 エンコーディング (BOM 付き utf-8-sig も自動対応)
- カンマ区切り

```csv
Host1,こんにちは、今日はAI技術について解説します
Host2,よろしくお願いします
```

#### テキスト (.txt) — ラベル付き
- 話者タグ付き対話テキスト
- 以下のパターンを認識:

```
# タイムスタンプ付き
[00:00] ナレーター1: こんにちは
[00:15] ナレーター2: よろしくお願いします

# シンプル (半角コロン)
Host1: こんにちは
Host2: よろしくお願いします

# シンプル (全角コロン)
ナレーター1：こんにちは
ナレーター2：よろしくお願いします

# NotebookLM 元台本形式
スピーカー1: こんにちは
スピーカー2: よろしくお願いします
```

話者名の判定: コロン前の文字列が 30 文字以内の場合に話者タグとみなす。30 文字超の場合は通常テキストとして扱う。

#### 継続行の結合

話者タグにマッチしない行は、直前の発話の継続行として結合する。これにより、コピペ時の改行崩れ（句読点が次行に分離する等）を吸収する。

```
# 入力（コピペで句点が分離）
スピーカー1: これは最初の文です
。そしてこれは続きです
。

# → 結合結果: 「これは最初の文です。そしてこれは続きです。」
```

#### テキスト (.txt) — ラベルなし (`--unlabeled`)
- 話者タグのない生テキスト (NotebookLM Audio Overview の書き起こし等)
- 行ごとに Speaker_A / Speaker_B を交互に割り当て
- 短い行 (3文字以下かつ句読点で終わらないもの) は前の行に自動結合 (音声認識の分断アーティファクト緩和)
- 句読点 (。！？!?) で終わる短行は完全な発話 (相槌等) として保持
- `--speaker-map` で Speaker_A/Speaker_B を YMM4 キャラクター名に変換

```
あの、普段私たちが世界地図を見る時って...    → Speaker_A
ええ、国境線とかあるいは...                   → Speaker_B
はい。まるで自宅の配管設備みたいに...          → Speaker_A
```

### バリデーション

- ファイルが存在すること
- UTF-8 で読み取り可能であること
- 空でないこと (10 文字以上)
- 1 つ以上の発話が抽出できること

---

## 内部表現: StructuredScript

```python
@dataclass(frozen=True)
class Utterance:
    speaker: str   # non-empty
    text: str      # non-empty

@dataclass(frozen=True)
class StructuredScript:
    utterances: tuple[Utterance, ...]  # non-empty
```

- 全フィールド immutable
- 入力フォーマットに依存しない中間表現
- タイムスタンプ、キーポイント等の付加情報は持たない (YMM4 CSV に不要)

---

## 出力仕様: YMM4 CSV

### フォーマット

- 2列、ヘッダーなし
- UTF-8 (BOM 付き / utf-8-sig)
- カンマ区切り
- 列1: YMM4 キャラクター名 (例: "れいむ")
- 列2: 発話テキスト

```csv
れいむ,こんにちは、今日はAI技術について解説します
まりさ,よろしくお願いします
```

このフォーマットは YMM4 の「台本読込」機能が直接読み込める形式。

### 話者マッピング

CLI の `--speaker-map` オプションで入力側の話者名を YMM4 キャラクター名に変換する:

```
--speaker-map Host1=れいむ,Host2=まりさ
```

マッピングが提供されない場合、入力側の話者名がそのまま出力される。

### 話者マッピングファイル

`--speaker-map-file` で JSON またはテキストファイルからマッピングを読み込める:

```json
{"Host1": "れいむ", "Host2": "まりさ"}
```

```text
# key=value 形式 (1行1エントリ、# でコメント)
Host1=れいむ
Host2=まりさ
```

`--speaker-map` と `--speaker-map-file` を同時に指定した場合、ファイルを先に読み込み、コマンドラインの値で上書きする。

### 話者プレフィックス除去

テキスト内に含まれる話者プレフィックス (`Host1: テキスト` の `Host1: ` 部分) は自動除去する。
これは speaker 列と text 列の重複を防ぐため。

### 長文分割 (`--max-length`, `--display-width`, `--max-lines`, `--balance-lines`)

`--max-length N` を指定すると、N 文字を超える発話を文末（。！？!?）で分割し、同じ話者の複数行に展開する。

- 分割は文末区切りのみ。文の途中では切らない
- 単一文が N 文字を超える場合はそのまま保持する
- 分割後の各行は同じ話者名を持つ
- NotebookLM 元台本は 1 発話が長くなる傾向があるため、YMM4 での音声合成に適した粒度に分割する用途を想定
- `--display-width` を併用すると、`--max-length` を文字数ではなく表示幅（全角=2, 半角=1, Ambiguous=2）として解釈する
- `--max-lines N --chars-per-line M` を使うと、`M * N` の表示幅を閾値として分割し、`--stats` では推定はみ出し候補も警告する
- `--balance-lines` を併用すると、2行字幕向けに読点・句点・カギカッコ付近を候補にした自然改行を opt-in で挿入する
- `--balance-lines` は、句点がない長文に対して `、` や接続句で節分割する fallback、1文字だけの最終行を避ける widow/orphan guard、複数文発話の中にある単一長文をより積極的に複数字幕へ落とす aggressive clause chunking を含む
- `--balance-lines` は `--max-lines` 前提の best-effort 改善で、本文の削除は行わない

```bash
# 80 文字で分割
python -m src.cli.main build-csv input.txt --max-length 80 -o output.csv

# 2 行 * 40 幅を基準に表示幅で分割
python -m src.cli.main build-csv input.txt --max-lines 2 --chars-per-line 40 --stats

# 2 行字幕向けに自然改行も入れる
python -m src.cli.main build-csv input.txt --max-lines 2 --chars-per-line 40 --balance-lines --stats
```

---

## バリデーション (pre-handoff)

出力前に以下をチェックする。全て Warning (非致命的):

| チェック | 条件 | 重要度 |
|---------|------|--------|
| 空話者名 | speaker が空文字 | ERROR (書き出し中止) |
| 空テキスト | text が空文字 | ERROR (書き出し中止) |
| 長文警告 | text が 200 文字超 | WARNING |
| 未マッピング話者 | speaker_map 指定時に未変換の話者 (CLI が assembly 前に検出) | WARNING |

---

## fetch-topics サブコマンド (A-04)

RSS 2.0 / Atom 1.0 フィードからトピック候補（エントリタイトル）を取得する。
取得したタイトルは NotebookLM の検索クエリや台本テーマ候補として使用する想定。

### 使用方法

```bash
python -m src.cli.main fetch-topics <URL>... [-n 20] [--after YYYY-MM-DD] [--format text|json] [--timeout 10] [-o output.txt]
```

### 引数

| 引数 | 必須 | 既定値 | 説明 |
|------|------|--------|------|
| URL | 必須 | — | RSS/Atom フィード URL（複数指定可） |
| -n, --limit | 任意 | 20 | 表示するエントリ数の上限 |
| --after | 任意 | — | この日付以降のエントリのみ抽出（YYYY-MM-DD 形式） |
| --format | 任意 | text | 出力形式（text / json） |
| --timeout | 任意 | 10 | HTTP タイムアウト秒数 |
| -o, --output | 任意 | stdout | 出力先ファイルパス |

### 内部表現: FeedEntry

```python
@dataclass(frozen=True)
class FeedEntry:
    title: str
    published: str | None = None   # ISO 8601 日付文字列
    source_url: str | None = None  # フィード URL
```

### 出力仕様

#### text 形式（既定）

```
# Source: https://example.com/feed.xml (2026-03-30)
記事タイトル1
記事タイトル2
```

ソース URL ごとにヘッダーコメント行を出力し、その後にエントリタイトルを1行ずつ出力する。

#### json 形式

```json
[
  {"title": "記事タイトル1", "published": "2026-03-30", "source": "https://example.com/feed.xml"},
  {"title": "記事タイトル2", "published": "2026-03-29", "source": "https://example.com/feed.xml"}
]
```

### 対応フィード形式

- RSS 2.0（`<channel>/<item>/<title>`, `<pubDate>`）
- Atom 1.0（`<feed>/<entry>/<title>`, `<published>` or `<updated>`）

### エラーハンドリング

- フィード取得失敗: stderr にエラーを出力し、残りの URL を継続処理
- 日付形式不正: エラー終了（exit code 1）
- エントリ 0 件: stderr に "No entries found." を出力（exit code 0）

---

## スコープ外

以下は PIPELINE_SPEC の対象外。機能の管理は FEATURE_REGISTRY.md を参照。

- YMM4 プロジェクトファイル (.ymmp) の直接生成 (rejected: C-03)
- LLM による構造化補助 (IP-01 No-Go)
- 画像パス列・アニメーション種別列 (YMM4 CSV 3列目以降の拡張は未検討)
