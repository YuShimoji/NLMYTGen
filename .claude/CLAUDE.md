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
