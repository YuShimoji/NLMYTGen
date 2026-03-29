# AGENTS.md — NLMYTGen 入口ファイル
# このファイルは repo の運用入口であり、状態スナップショットの複製ではない。
# Claude Code / Web版Claude がこの repo で作業を開始するとき、最初にここを読む。

---

## このプロジェクトについて
- **プロジェクト名:** NLMYTGen
- **プロジェクト root:** このファイルがある repo のルート
- **種別:** CLI パイプライン（CLI artifact mode 適用）
- **最終成果物到達経路:** NLM transcript → YMM4 CSV → 動画1本完成
- **Artifact Surface:** CSV ファイル → YMM4 読込 → レンダリング結果

---

## 再アンカリング手順（この repo で作業を開始・再開するとき）
以下の順で読むこと。この repo 以外のファイルは読まない。

```
1. このファイル（AGENTS.md）を読む → プロジェクト概要・境界ルール
2. .claude/CLAUDE.md を読む → repo-local の運用ルール
3. docs/runtime-state.md を読む → 現在位置・カウンター・状態値
4. docs/project-context.md を読む → DECISION LOG・IDEA POOL・HANDOFF SNAPSHOT
5. 全景確認を出力:
   📍 NLMYTGen / 🧩 [現在のスライス] / 🔲 [次のアクション]
   🏷️ 案件モード: CLI artifact
```

---

## 境界ルール（厳守）

### 他プロジェクトへの逸脱禁止
- **この repo 以外のプロジェクトのファイルを読み書きしない。**
- HoloSync / NLMandSlideVideoGenerator / NarrativeGen / VastCore 等のファイル・memory・docs を参照しない。
- 「NLMYTGen 用の memory がない」場合は**スキップする。他 PJ の memory を代用しない。**
- AskUserQuestion の選択肢に「別プロジェクトへ移動」を含めない。
- 別 repo への移動はユーザーが明示的に指示した場合のみ。

### AskUserQuestion の範囲制限
- 選択肢はこの repo 内の Advance / Audit / Excise / Unlock に限定すること。
- 他 repo のタスクを候補に混ぜない。
- 「別セッションで別 PJ」の提案はこの repo の判断としては出さない。

### 運用ファイルの削除禁止
- AGENTS.md / .claude/CLAUDE.md / docs/runtime-state.md / docs/project-context.md は
  「重複」として削除しない。それぞれ異なる責務を持つ入口ファイルである。

---

## ファイルの責務分担

| ファイル | 責務 | 更新タイミング |
|---------|------|--------------|
| AGENTS.md | 入口。概要・境界・再アンカリング手順 | PJ 構成変更時のみ |
| .claude/CLAUDE.md | repo-local 運用ルール。global runbook への依存を減らす | ルール変更時のみ |
| docs/runtime-state.md | 現在位置。カウンター・状態値・active_artifact | 毎ブロック終端 |
| docs/project-context.md | 航海日誌。DECISION LOG・IDEA POOL・HANDOFF SNAPSHOT | セッション終端・HANDOFF 時 |
| CLAUDE.md (ルート) | プロジェクト方針・技術スタック・成功定義 | 方針変更時のみ |

---

## 現在の状況（概要のみ。詳細は docs/ を参照）
- 成功定義 3/3 達成（2026-03-29）。コアパイプライン完成
- 次フェーズ: script-first 導線確立（NotebookLM 元台本出力 → NLMYTGen → YMM4）
- 音声書き起こし(S-2)は fallback へ降格予定。元台本の直接取得が主導線
- Web UI / API / YouTube 連携はまだ優先しない
