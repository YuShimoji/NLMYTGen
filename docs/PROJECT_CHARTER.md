# PROJECT CHARTER

## NLMYTGen v2 -- なぜ新規リポジトリを作るのか

### プロジェクトの目的

NotebookLM の出力を YMM4 用 CSV に変換する、単一導線のパイプラインを構築する。

### 原則

1. **Path A only**: NotebookLM → 構造化 → CSV → YMM4 の 1 本だけ
2. **NotebookLM is upstream**: 台本品質は NotebookLM が生成する。Python は品質を生成しない
3. **LLM は構造化専任**: 内部 LLM は台本の新規創作をしない
4. **最小骨格から始める**: 将来のための汎用抽象化を先回りで入れない
5. **README と docs と実装で同じ真実を持つ**: 文書間の矛盾を作らない

---

## Why v2 -- 旧プロジェクトで何が壊れていたか

以下は NLMandSlideVideoGenerator (旧リポジトリ) で観測された失敗の記録。
v2 の成立理由を説明するものであり、現行仕様の本体ではない。

### 1. NotebookLM → Gemini サイレントドリフト

旧プロジェクトは "NLM" = NotebookLM を名前に冠しているが、NotebookLM の役割が暗黙的に放棄された。

- 2025-11-26 (commit `b78d25e`): Gemini が「NotebookLM の代替」として導入
- この時点で DECISION LOG に「NotebookLM を放棄する」という記録は作られなかった
- 以後、Gemini がプロンプト駆動で台本を「生成」する設計に暗黙移行
- 2026-03-19: ドリフトが初めて検出され、分析された (`docs/notebooklm_drift_analysis.md`)
- 2026-03-22: 根本ワークフローとして NotebookLM 起点を復元 (`docs/DESIGN_FOUNDATIONS.md`)

**根本原因**: NotebookLM の API が利用不可だったため、暫定的な Gemini 実装が恒久化した。
放棄の決定が明示的に記録されなかったため、ドリフトが不可視になった。

### 2. Path B (MoviePy / 直接動画生成) の混入と撤去

- Python + MoviePy + Voicevox で直接動画を生成する Path B が存在していた
- Path B の撤去に 10+ revert cycles を要した (provided historical evidence)
- commits: `4f01896`, `c620472`, `1a255c5`, `8653def`, `28ccd69`, `1bedfe8`, `05da637`, `4254a80` 等

**根本原因**: Path A (YMM4) と Path B (MoviePy) のコードが密結合しており、分離が困難だった。

### 3. テスト件数と出力品質の乖離

- 最終的に 1,241 テストが存在 (provided historical evidence)
- 全テスト合格だが、実際の動画出力は YouTube 公開水準に未達
- セグメント粒度が粗い (43-64秒/セグメント vs 推奨 3-10秒)
- PIL によるテキストスライドが品質不足
- テスト件数の増加が品質向上と錯覚された

**根本原因**: テストはコードの動作を検証していたが、出力の品質は検証していなかった。

### 4. 仕様の肥大化と設計の忘却

- 53 仕様書 (41 done + 8 partial + 2 draft + 1 archived + 1 superseded)
- 448 commits (provided historical evidence)
- 37 DECISION LOG エントリ (active) + 27 (archived)
- 三層モデル (NotebookLM / Python / YMM4) が `docs/DESIGN_FOUNDATIONS.md` に復元されるまで忘却されていた

**根本原因**: セッション間で設計コンテキストが継承されず、仕様書が実装の実態から乖離した。

### 5. 車輪の再発明

- PIL によるスライド生成 (708行) → Google Slides API / NotebookLM スライド機能で代替可能だった
- Brave Search によるリサーチ → NotebookLM のソース投入で代替可能だった
- 独自アニメーション割当 → YMM4 側の責務だった

**根本原因**: Python 変換層に品質生成の責務を持たせてしまった。

---

## 再発防止原則

| 旧 PJ の失敗 | v2 の対策 |
|-------------|----------|
| NotebookLM の暗黙放棄 | ADR-0002 で NotebookLM upstream を固定 |
| Path B 混入 | ADR-0001 で Path A only を固定。直接動画生成は ADR-0003 で禁止 |
| テスト膨張 | テスト 10-20 本の少数精鋭。契約テスト優先 |
| 仕様肥大化 | 仕様書は最小限。README + ARCHITECTURE + PIPELINE_SPEC + ADR のみ |
| 車輪の再発明 | Python は構造化・整形・検証のみ。品質生成しない |
| 文書間矛盾 | 1 つの真実を 1 箇所に。重複展開しない |

---

## 数値的根拠の扱い

- commit hash: 旧リポジトリの git log から取得。`b78d25e` は confirmed。
- テスト件数 (1,241): provided historical evidence
- commit 総数 (448): provided historical evidence
- 仕様数 (53): provided historical evidence
- DECISION LOG entries (37 active + 27 archived): provided historical evidence
- Path B revert cycles (10+): provided historical evidence, specific commits listed above
- 未確認の数値は本文書に含めない
