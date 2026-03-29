# CLAUDE.md（NLMYTGen repo-local）
# この repo 内での Claude Code の運用ルール。
# global ~/.claude/CLAUDE.md + rules/ が適用されたうえで、この repo 固有の制約を追加する。

---

## プロジェクト境界
- **project root:** このファイルの親ディレクトリの親（NLMYTGen/）
- **案件モード:** CLI artifact mode（常時発火）
- **Active Artifact:** NLM transcript → YMM4 CSV → 動画1本完成への経路
- **Artifact Surface:** CSV ファイル / YMM4 読込結果 / レンダリング結果

---

## 他プロジェクト参照禁止
- HoloSync / NLMandSlideVideoGenerator / NarrativeGen / VastCore 等、この repo 以外のプロジェクトのファイル・memory・docs を参照しないこと。
- 「NLMYTGen 用の project-memory がない」場合は project-memory をスキップする。他 PJ の memory を代用しない。
- AskUserQuestion の選択肢に他 repo への移動を含めない。

---

## 再アンカリング（compact / refresh / 文脈喪失時）
```
1. AGENTS.md を読む → 概要・境界ルール
2. .claude/CLAUDE.md（このファイル）を読む → repo-local ルール
3. docs/runtime-state.md を読む → 現在位置・カウンター
4. docs/project-context.md を読む → DECISION LOG・IDEA POOL
5. 全景確認を出力してから作業を再開する
```

---

## CLI artifact mode（この repo では常時適用）
- Active Artifact は CLI 中間出力（CSV 生成等）で止めない。最終成果物到達経路を書く。
- Evidence は `N/A` で終えない。実データ通過 / 外部ツール読込成功 / 最終成果物到達 / 未検証 を使う。
- 実成果物ゼロ段階では最上位候補を [Advance] 実データ E2E / 最小成果物完成に固定。
- docs / workflow / format 調査は Advance に置かない。
- blocking dependency が特定されたら Authority Return Items として明示し、周辺改善の積み増しを停止する。

---

## Python のスコープ制約（厳守）
Python の責務は**テキスト変換のみ**（CSV + テキストメタデータ文字列）。

**禁止:**
- 画像生成・画像合成（PIL/Pillow 含む）
- .ymmp 生成・操作（音声ファイル参照を含むため外部生成不可能）
- YMM4 テンプレート生成・演出指定（YMM4 内部の責務）
- 動画レンダリング・音声合成・外部 TTS

**根拠:** .ymmp は音声ファイルへの参照を含む。音声は YMM4 が台本読込時に内蔵 TTS で自動合成する。NLMYTGen から音声を生成できないため、.ymmp の外部生成は不可能。この制約により、YMM4 内部操作を Python から制御するアプローチ全般が成り立たない。

**機能提案時の確認事項:** 新機能を提案する際は「Python で何かを生成・レンダリングしていないか」を最初に確認すること。

---

## AskUserQuestion の範囲
- 選択肢はこの repo 内の Advance / Audit / Excise / Unlock に限定。
- 他 repo のタスクを候補に混ぜない。
- 「別セッションで別 PJ」は出さない。

---

## PHASE 1 の安全制御
- git fetch → 差分要約 → git status まで。
- git pull / stash / pop / reset / checkout は明示許可なしに禁止。
- behind していても報告のみ。

---

## docs 参照
# @../docs/project-context.md
# @../docs/runtime-state.md
