# サムネイル 1 枚ワークフロー（チェックリスト）

YMM4 テンプレを前提に、**Python 画像生成なし**で 1 枚の YouTube サムネを仕上げるための最短手順。全体像は [WORKFLOW.md](WORKFLOW.md) S-8。

## 事前準備（初回のみ）

- S-0 で **サムネ用 YMM4 テンプレート**（文字レイヤー・立ち絵差し込み・背景スロットが決まっている）を作成して保存する。
- 書き出し解像度を **1280×720**（または運用で固定した解像度）に合わせる。
- NLMYTGen で限定 patch したい item には `Remark` を付ける: 文字は `thumb.text.title` / `thumb.text.sub` / `thumb.text.badge_1`、画像は `thumb.image.background` / `thumb.image.reimu` / `thumb.image.marisa` など。

## 毎回の手順

1. [ ] AI 生成時に `thumbnail_design` / H-02 one-sheet が出ている場合、それをサムネ専用の下書きとして参照する（台本本文や本編 Production IR へ混ぜない）。
2. [ ] テンプレートの **プロジェクトを複製**（元テンプレを上書きしない）。
3. [ ] **タイトル文字**を差し替え（改行・文字数は読みやすさ優先。H-02 の banned pattern に注意）。
4. [ ] **立ち絵／表情**を差し替え（テンプレが参照する素材パスを更新）。
5. [ ] **背景**を差し替え（コントラストでタイトルが読めるか確認）。
6. [ ] YMM4 で **静止画書き出し**（PNG 推奨）→ ファイル名を動画スラッグに合わせて保存。
7. [ ] **品質チェック**（下記）。

`thumbnail_design` が無い場合は、[S8-thumbnail-copy-prompt.md](S8-thumbnail-copy-prompt.md)（C-08）と [THUMBNAIL_STRATEGY_SPEC.md](THUMBNAIL_STRATEGY_SPEC.md)（H-02）を使って、サムネ専用のコピー / 構図 / 色 / 表情案を別途作る。

## Template Slot Patch（任意・実装済み最小入口）

YMM4 上で粗配置した template copy に `thumb.*` Remark を付けている場合だけ、既存 item の差し替えを CLI で補助できる。

```bash
python -m src.cli.main audit-thumbnail-template thumb_template.ymmp
python -m src.cli.main patch-thumbnail-template thumb_template.ymmp \
  --patch thumbnail_patch.json \
  -o thumb_patched.ymmp
```

patch JSON の最小形:

```json
{
  "text": {
    "title": {"value": "新コピー", "color": "#FFFFD863", "x": 12, "zoom": 110}
  },
  "image": {
    "background": {"file_path": "C:\\\\path\\\\bg.png", "zoom": 105}
  }
}
```

この CLI は `.ymmp` 内の既存 slot を更新するだけで、画像生成、PNG 書き出し、YMM4 操作、最終デザイン判断は行わない。repo 内にはまだ実サムネ template `.ymmp` が無いため、最初の実運用では `audit-thumbnail-template` の結果を見て TextItem の route を確認する。

## 品質チェック（最低限）

- スマホ縮小想定で **主張が 1 つに絞れている**（情報の詰め込みすぎでない）。
- **具体性**: 可能なら数値・固有名詞・年等、本文根拠のある要素が 1 つ以上入っている（H-02）。
- **サムネとタイトル・動画内容**が大きく矛盾していない（H-01 brief がある場合は alignment を確認）。

## Automation Probe（任意・レーンE）

手動評価を機械記録に残す場合は、[verification/LANE-E-S8-prep-2026-04-09.md](verification/LANE-E-S8-prep-2026-04-09.md) の Probe 契約に従い、`score-thumbnail-s8` を使う。

- 入力: `--scores`（手動採点 0..3）、任意で `--payload`（run_id 等）
- 期待: `pass` は `total_score>=80` かつ warning なし
- 注意: 本 Probe は判定補助であり、最終の creative judgement を置き換えない

## スコープ外（本ドキュメント）

- 自動サムネ生成（Python / API）はプロジェクト方針で禁止。サムネは **YMM4 上で作成**し、将来は NLMYTGen 側で「素材置き換え自動化」機能を別途実装する前提（Canva 等の外部 SaaS への依存は作らない方針）。
- AI 生成時にサムネ設計を同時に出すことは許容するが、サムネ配置済み `.ymmp` の自動生成は現時点のスコープ外。
