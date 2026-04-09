# feat/phase2-motion-segmentation → master — PR 運用（コア開発）

**状態（2026-04-09）**: PR [#1](https://github.com/YuShimoji/NLMYTGen/pull/1) は **マージ済み**。以降の開発は **`master` を正**とし、新機能用にトピックブランチを切る。

**背景**: [FUTURE_DEVELOPMENT_ROADMAP.md](../FUTURE_DEVELOPMENT_ROADMAP.md)。歴史: [P2A-motion-branch-operator-decision.md](P2A-motion-branch-operator-decision.md)（一括で持ち込まない方針で段階統合した）。

---

## 1. 事前確認

```powershell
cd "C:\Users\PLANNER007\NLMYTGen"
git fetch origin
git checkout feat/phase2-motion-segmentation
git pull origin feat/phase2-motion-segmentation
git log origin/master..HEAD --oneline
```

- **差分が大きい場合**は PR 説明に **変更カテゴリ**（docs / tests / CLI / GUI）を箇条書きする。  
- **コンフリクト**はローカルで `git merge origin/master`（または rebase 方針に従う）して解消してから push。

---

## 2. 回帰（PR オープン前）

```powershell
$env:NLMYTGEN_PYTEST_FULL = "1"
uv run pytest -q --tb=short
Remove-Item Env:NLMYTGEN_PYTEST_FULL -ErrorAction SilentlyContinue
```

---

## 3. PR 作成（GitHub CLI 利用時）

```powershell
gh auth status
gh pr create --base master --head feat/phase2-motion-segmentation `
  --title "feat: phase2 motion segmentation lane + core docs (merge to master)" `
  --body "## 概要`n- feat/phase2-motion-segmentation を master に統合する PR。`n- コア開発手順: verification/CORE-DEV-POST-DELEGATION-INDEX.md`n`n## チェック`n- [ ] NLMYTGEN_PYTEST_FULL=1 pytest 緑`n- [ ] ドキュメントリンク切れなし`n"
```

（タイトル・本文はチーム規約に合わせて編集する。）

---

## 4. マージ後

```powershell
git checkout master
git pull origin master
$env:NLMYTGEN_PYTEST_FULL = "1"
uv run pytest -q --tb=short
```

- [runtime-state.md](../runtime-state.md) の `last_verification_date` を更新。  
- 長寿命ブランチを残す場合は、マージ後に `feat/phase2-motion-segmentation` を削除するか方針を決める。

---

## 5. 変更履歴

- 2026-04-09: 初版。
- 2026-04-09: `feat/phase2-motion-segmentation` → `master` の PR を作成: https://github.com/YuShimoji/NLMYTGen/pull/1
- 2026-04-09: PR #1 を **マージ**（merge commit）。`master` で `NLMYTGEN_PYTEST_FULL=1 uv run pytest` 再実行済み。
