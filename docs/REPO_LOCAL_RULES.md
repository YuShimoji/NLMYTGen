# REPO_LOCAL_RULES.md — repo-local 運用ルール（正本）

NLMYTGen の **日々の Hard Rules・再開読了予算・Checklist** の正本。長い背景説明ではなく、毎ブロックで効かせる強制ルールだけを置く。vendor-neutral な AI ルールは引き続き `docs/ai/*.md`、非交渉境界は `docs/INVARIANTS.md`。

**`.claude/CLAUDE.md`** は Claude Code 等が慣例で読む入口用の **短いポインタ** に留める（本文の重複を避ける）。

---

## Restart Read Budget

通常再開では、読了対象を増やすこと自体を progress にしない。毎回読むのは次の 3 点まで。

1. `AGENTS.md` — repo 境界・削除禁止・入口責務
2. `docs/REPO_LOCAL_RULES.md` — 本ファイルの Hard Rules / Block-Start Checklist / Ask Hygiene
3. `docs/runtime-state.md` — `slice` / `next_action` / `last_change_relation` / `last_verification`

追加で読むのは、作業接続に必要な場合だけ。

- 迷子対策: `docs/NAV.md`
- handoff / 決定履歴: `docs/project-context.md` の HANDOFF SNAPSHOT または該当 DECISION LOG だけ
- status / backlog: `docs/FEATURE_REGISTRY.md` の該当 ID だけ
- 非交渉境界: `docs/INVARIANTS.md` の該当節だけ
- durable request: `docs/USER_REQUEST_LEDGER.md` の現在有効な要求 / 該当 backlog delta だけ
- workflow pain: `docs/OPERATOR_WORKFLOW.md` の該当工程だけ
- ask / manual verification / template formalism: `docs/INTERACTION_NOTES.md` の該当 failure class だけ
- vendor-neutral rule: `docs/ai/*.md` の該当 gate / workflow 節だけ

フル再アンカリングは `AGENTS.md` の例外手順を使う。全 canonical docs の存在は保つが、全文読了を通常再開の前提にしない。

## Hard Rules

- この repo 以外の file / memory / docs を読まない・書かない。
- HoloSync / NLMandSlideVideoGenerator / NarrativeGen / VastCore への逸脱を禁止。
- repeated visual proof を要求しない。YMM4 visual proof は初回 E2E と最終制作物の品質判断だけ。
- mechanical な確認は GUI の Dry Run または開発時のユニットテストで閉じる。コード変更がないときにテストを回さない。
- `src/` または `gui/` のロジックを変えたブロックの終わりにだけ pytest 結果を示す。ドキュ / runtime-state のみのブロックでは不要。
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

## pytest（最小）

テスト投資の判断は **Block-Start Checklist** と **Quality Priority** に委ね、手順を増やさない。

- 日次・短ループ: `uv run pytest`（`@pytest.mark.integration` は既定でスキップ。`tests/conftest.py`）
- `src/` または CLI 契約を変えたマージ前など: `NLMYTGEN_PYTEST_FULL=1 uv run pytest` を追加で回す（マーカーは `pyproject.toml`）
- 新規 `@pytest.mark.integration` は、ユニットだけでは subprocess 経路の契約が保てないときに限定する。似たケースは既存テストへのケース追加で統合を優先する。
- 手動 E2E proof（`docs/verification/` 等）は Hard Rules の「repeated visual proof を要求しない」に従い、初回・フロンティア・手順変更時に寄せる。
- **git のコミット傾向分析や Playwright を必須ゲートに含めない**（争点時のみ任意でよい）。

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
