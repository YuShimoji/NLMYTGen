# REPO_LOCAL_RULES.md — repo-local 運用ルール（正本）

NLMYTGen の **日々の Hard Rules・Read Order・Checklist** の正本。長い背景説明ではなく、毎ブロックで効かせる強制ルールだけを置く。vendor-neutral な AI ルールは引き続き `docs/ai/*.md`、非交渉境界は `docs/INVARIANTS.md`。

**`.claude/CLAUDE.md`** は Claude Code 等が慣例で読む入口用の **短いポインタ** に留める（本文の重複を避ける）。

---

## Read Order

以下は `AGENTS.md` の再アンカリング手順ステップ 1〜5 と同じファイル列。ルート `CLAUDE.md` は方針・スタック・成功定義のみ。エディタがルート `CLAUDE.md` だけ読んだ場合は、続けて本ファイルと `docs/INVARIANTS.md` を読むこと。`docs/ai/WORKFLOWS_AND_PHASES.md` の「Recommended read order」は `docs/ai` から入る **resume 用サブセット**であり、フル再アンカリングの代替にはならない。

1. `AGENTS.md`
2. `docs/ai/CORE_RULESET.md`
3. `docs/ai/DECISION_GATES.md`
4. `docs/ai/STATUS_AND_HANDOFF.md`
5. `docs/ai/WORKFLOWS_AND_PHASES.md`
6. `docs/INVARIANTS.md`
7. `docs/USER_REQUEST_LEDGER.md`
8. `docs/OPERATOR_WORKFLOW.md`
9. `docs/INTERACTION_NOTES.md`
10. `docs/runtime-state.md`
11. `docs/project-context.md`
12. `docs/FEATURE_REGISTRY.md`
13. `docs/AUTOMATION_BOUNDARY.md`

## Hard Rules

- この repo 以外の file / memory / docs を読まない・書かない。
- HoloSync / NLMandSlideVideoGenerator / NarrativeGen / VastCore への逸脱を禁止。
- repeated visual proof を要求しない。YMM4 visual proof は初回 E2E と最終制作物の品質判断だけ。
- mechanical な確認は test / CLI / dry-run / static analysis で閉じる。
- 修正を指摘されたら止まらない。次を同じブロックで自分で確定して進める。
  - 何が誤りだったか
  - 何を修正するか
  - 修正後にどう検証するか
- `判断をお願いします` `何が足りないか教えてください` のような broad question で止まらない。
- user に聞く前に、repo 内根拠で決められない理由を自分で確認する。
- `assistant 側でやることがない` と安易に結論しない。まず次を検討する。
  - fail-fast
  - gap report
  - quality gate
  - drift detection
  - docs sync
  - operator の手動負荷削減

## Block-Start Checklist

各ブロックで次を短く確定してから進める。

1. 今の bottleneck は何か
2. これからやる作業はその bottleneck に直接効くか
3. user に新しい manual proof を頼まずに閉じられるか
4. user に聞く前に repo 内根拠で決められないか

この 4 つに yes と言えない作業は、まず理由を明文化してから進める。

## Ask Hygiene

- 質問は高位分岐だけ。
- 質問が必要でも、3 個以下の実質差分がある選択肢まで圧縮する。
- 「別 repo へ移動」「別 PJ の memory を参照」は選択肢に含めない。

## Quality Priority

- 進捗は「新機能が増えたか」ではなく、次で評価する。
  - quality を落とす入力を早期に止められるか
  - empty hit / unknown label / drift を可視化できるか
  - operator の反復作業が減ったか
  - artifact の品質に近づくか

## Hooks

機械的に判定できる違反は `.claude/hooks/guardrails.py` で reject する。対象:

- repo 外逸脱
- broad question による停止
- repeated visual proof の反復要求

Hook で止められない低価値作業は、本ファイルの checklist で防ぐ。
