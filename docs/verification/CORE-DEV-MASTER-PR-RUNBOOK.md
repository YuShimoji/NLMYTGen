# feat/phase2-motion-segmentation → master — PR 運用（コア開発）

**状態（2026-04-09）**: PR [#1](https://github.com/YuShimoji/NLMYTGen/pull/1) は **マージ済み**。以降の開発は `**master` を正**とし、新機能用にトピックブランチを切る。

**背景**: [FUTURE_DEVELOPMENT_ROADMAP.md](../FUTURE_DEVELOPMENT_ROADMAP.md)。歴史: [P2A-motion-branch-operator-decision.md](P2A-motion-branch-operator-decision.md)（一括で持ち込まない方針で段階統合した）。

---

## 1. 事前確認

```powershell
cd "C:\Users\PLANNER007\NLMYTGen"
git fetch origin
git checkout master
git pull origin master
# 新規作業は master からトピックブランチを切る
git checkout -b feat/topic-name
```

- **差分が大きい場合**は PR 説明に **変更カテゴリ**（docs / tests / CLI / GUI）を箇条書きする。  
- **コンフリクト**はローカルで `git merge origin/master`（または rebase 方針に従う）して解消してから push。

---

## 2. 回帰（PR オープン前）

`src/` または `tests/` を変更したブロックの終わりにのみ実施する（GUI/docs のみの変更では不要）。integration テストは `conftest.py` で default-skip されているため、通常は下記のみで良い:

```powershell
uv run pytest -q --tb=short
```

integration 込みで走らせたい局面（パイプライン全経路の疎通確認など）では `$env:NLMYTGEN_PYTEST_FULL = "1"` を一時的に付ける。

---

## 3. PR 作成（GitHub CLI 利用時）

```powershell
gh auth status
gh pr create --base master --head feat/topic-name `
  --title "scope: summary" `
  --body "## 概要`n- master 起点トピックブランチの変更を統合。`n- コア開発手順: verification/CORE-DEV-POST-DELEGATION-INDEX.md`n`n## チェック`n- [ ] ドキュメントリンク切れなし`n"
```

（タイトル・本文はチーム規約に合わせて編集する。pytest の実施有無は §2 の条件に従う。）

---

## 4. マージ後

```powershell
git checkout master
git pull origin master
```

- [runtime-state.md](../runtime-state.md) の `last_verification_date` は §2 で回帰を走らせた場合のみ更新する。
- マージ後の pytest 再実行は不要（§2 で済んでいる）。

---

## 5. 変更履歴

- 2026-04-14: §2-4 から「PR ごとの `NLMYTGEN_PYTEST_FULL=1` 全件実行」要求を除去。`OPERATOR_WORKFLOW.md` L120 の「Python 変更時のみテスト」方針と整合させた。
- 2026-04-10: 以後の手順を `master` 起点トピックブランチ向けに一般化。
- 2026-04-09: 初版。
- 2026-04-09: `feat/phase2-motion-segmentation` → `master` の PR を作成: [https://github.com/YuShimoji/NLMYTGen/pull/1](https://github.com/YuShimoji/NLMYTGen/pull/1)
- 2026-04-09: PR #1 を **マージ**（merge commit）。

