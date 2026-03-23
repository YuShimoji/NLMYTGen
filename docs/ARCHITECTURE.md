# ARCHITECTURE

## 三層モデル

```
[入力層: NotebookLM]  →  [変換層: Python]  →  [出力層: YMM4]
  台本品質の源泉           構造化・整形・検証     音声合成・動画レンダリング
```

- **入力層 (NotebookLM)**: Audio Overview → テキスト化。対話構造・テンポ・個性を持つ高品質台本を生成する。Python はこの品質を再現しない。
- **変換層 (Python)**: NotebookLM 出力をパースし、YMM4 が読み込める CSV に変換する。品質を生成しない。品質を通過させる。
- **出力層 (YMM4)**: CSV を読み込み、音声合成・字幕配置・動画レンダリングを行う。

## データフロー

```
NotebookLM transcript (.txt or .csv)
        │
        ▼
┌─────────────────────┐
│ normalize()         │  入力パース (txt/csv 自動判定)
│ → StructuredScript  │  話者名 + テキストの抽出
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ assemble()          │  話者マッピング適用
│ → YMM4CsvOutput     │  プレフィックス除去
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ validate()          │  空フィールドチェック
│ → [Warning, ...]    │  長文警告
└─────────────────────┘
        │
        ▼
YMM4 CSV (2列, ヘッダーなし, UTF-8)
```

## モジュール構成

```
src/
  contracts/                 # データ契約 (frozen dataclass)
    notebooklm_input.py      # 入力契約: RawTranscript
    structured_script.py     # 内部契約: Utterance, StructuredScript
    ymm4_csv_schema.py       # 出力契約: YMM4CsvRow, YMM4CsvOutput
  pipeline/                  # 変換ロジック
    normalize.py             # 入力 → StructuredScript
    assemble_csv.py          # StructuredScript → YMM4CsvOutput
    validate_handoff.py      # 出力前検証
  cli/
    main.py                  # 単一エントリポイント
```

## 各モジュールの責務

| モジュール | 責務 | やらないこと |
|-----------|------|------------|
| `contracts/` | データ構造の定義と不変条件の保証 | ビジネスロジック |
| `pipeline/normalize.py` | 入力ファイルのパースと正規化 | LLM 呼び出し、ネットワークアクセス |
| `pipeline/assemble_csv.py` | 話者マッピングと CSV 組立 | 画像取得、アニメーション割当 |
| `pipeline/validate_handoff.py` | 出力前の整合性チェック | エラー修正、自動補完 |
| `cli/main.py` | 引数解析と実行制御 | 直接的なデータ変換 |

## 禁止される越境

1. **Python が品質を生成する**: 台本内容の創作、対話テンポの改善、個性の付与
2. **Python が動画を生成する**: MoviePy, ffmpeg, Voicevox, TTS の使用
3. **Python が NotebookLM を代替する**: LLM による主台本生成
4. **pipeline が外部 API を呼ぶ**: 画像検索、Web リサーチ、YouTube 連携
5. **CLI が複数エントリポイントを持つ**: main.py 以外の実行スクリプト

## 依存関係

- 外部ライブラリ: なし (Python stdlib のみ)
- 使用する stdlib: `csv`, `re`, `pathlib`, `argparse`, `dataclasses`
