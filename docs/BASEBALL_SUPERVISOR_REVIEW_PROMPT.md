# Baseball Supervisor Review Prompt

Use this prompt when a Codex completion report from the Baseball sidequest needs
review by a supervising AI. This is not an implementation prompt for the next
Codex session.

```text
監修役AIに渡すPrompt（Baseball sidequest報告レビュー用。実装指示ではありません）

以下は Codex が NLMYTGen の Baseball sidequest branch で行った作業報告です。
あなたは実装担当ではなく監修役AIとして、報告内容の妥当性・混線リスク・次回改善点をレビューしてください。

対象:
- repository: https://github.com/YuShimoji/NLMYTGen.git
- lane: Baseball sidequest
- branch: origin/codex/baseball-bn02-visual-data
- mainline: origin/master
- このレビューは報告監査のみです。次Codexへの実装再開Promptではありません。

レビュー対象commit:
1. <commit hash> <title>
   - 目的:
   - 変更範囲:
   - touched files:
   - untouched boundaries:
   - local verification:
2. <commit hash> <title>
   - 目的:
   - 変更範囲:
   - touched files:
   - untouched boundaries:
   - local verification:

Codex報告本文:
<<<
ここに報告本文を貼る
>>>

確認してほしい点:
1. 作業対象が Baseball branch に限定され、origin/master 反映済みと誤認させていないか。
2. 複数commitを扱う場合、各commitの目的・変更範囲・touched files・untouched boundaries が分かれているか。
3. mainline runtime-state.md の next_action を置き換えていないか。
4. branch / development thread / supervisor prompt の分離が明確か。
5. 監修役向けPromptと次Codex向けPromptが混線していないか。
6. human final judgement と assistant/tool の generation / placement preparation / readback / gap report が混線していないか。
7. CLAUDE.md / .claude/CLAUDE.md 削除、docs/GLOSSARY.md 追加、MkDocs docs view 調整について、旧正本の喪失・翻訳・要約・再構成の有無が正直に書かれているか。
8. REPO_LOCAL_RULES.md を残した判断が、front-door / repo-local rule の観点で妥当か。
9. commit / push / clean state / upstream parity / build result が、実行branchとコマンド付きで書かれているか。
10. 本流 master への統合が必要な場合、それが別途 explicit な人間判断として分離されているか。

出力形式:
1. 判定: 問題なし / 要確認 / 要修正
2. 気になる点
3. Codex に返すべき報告修正指示
4. 次回報告Promptの改善案
5. 本流 master へ統合判断が必要か

禁止:
- このレビューから新規実装を開始しない。
- mainline / RSS / G-27 / NotebookLM / publishing の次作業を提案しない。
- 必要なら「別laneの判断」として分離する。
```
