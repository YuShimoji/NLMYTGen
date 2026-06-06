# Codex Worker Orchestration

この文書は、PR なし個人開発で Codex 作業を repo 内の正本に寄せるための
最小基盤を定義する。現在の layer は scaffold / policy gate であり、完全な
Worker runtime loop ではない。Codex 実行、外部通知、release / publish 判断は
まだ接続しない。

## 目的

Codex 作業を次の流れで管理する。

1. `.agent/prompt_catalog/` の固定 Prompt を選ぶ。
2. Worker が作業し、`.agent/schemas/worker_report.schema.json` に合う JSON
   report を返す。
3. `scripts/agent_gate.py` が report を schema と policy で判定する。
4. Gate が続行可能なら次 Worker を選ぶ。
5. Gate が人間確認を要求する場合だけ、実通知ではなく
   `.agent/needs_human.json` と `.agent/logs/notify_stub.log` を生成する。

この初期版は dry-run、report validation、policy gate、notify stub までを担当する。
Codex 実行そのものや外部 notification service 送信は意図的に未実装のままにする。

## Automation / Orchestrator / Codex exec の違い

Codex App Automation は実行タイミングの起点として使えるが、長文 Prompt や
判定ルールの正本にはしない。Automation には短い起動指示だけを置き、詳細は
この repo の catalog、schema、state を読ませる。

Repo-local orchestrator は `scripts/agent_orchestrator.py` で、現時点では次だけを行う。

- `.agent/state.json` を読む。
- `--worker advance|audit|fix|summarize` に対応する prompt の存在を確認する。
- `--dry-run` で将来の `codex exec` execution plan / command argv 案を表示する。
- `--report <path>` で既存 report を gate に渡す。
- `needs_human=true` のときだけ notify stub を呼ぶ。

Future `codex exec` integration は別 slice で行う。現時点では実行しない。

## Repo-local 正本

- `.agent/state.json`: prompt、schema、report、log、gate policy の現在設定
- `.agent/prompt_catalog/*.md`: Worker ごとの固定 Prompt
- `.agent/schemas/worker_report.schema.json`: Worker report の JSON Schema
- `scripts/agent_gate.py`: schema validation と policy gate
- `scripts/agent_notify_stub.py`: 外部通知なしの needs-human stub
- `scripts/agent_orchestrator.py`: prompt 選択、dry-run、report 判定の入口

## Prompt Catalog の使い方

Worker は `advance`、`audit`、`fix`、`summarize` の 4 種類から始める。

- `advance`: bounded slice を進める。
- `audit`: 変更内容、検証、境界違反を確認する。
- `fix`: 前 Worker や gate が示した狭い機械的修正だけを行う。
- `summarize`: report や検証結果を handoff しやすい形にまとめる。

dry-run 例:

```powershell
uv run python scripts/agent_orchestrator.py --worker audit --dry-run
```

このコマンドは prompt catalog の存在を確認し、将来実行する `codex exec`
コマンド案を表示するだけで、Codex 実行は開始しない。

Dry-run の command builder は preview contract だけを持つ。現在の想定 argv は
次の形で、prompt file を `--prompt-file` で渡す前提にはしない。

```powershell
codex exec - --output-schema .agent/schemas/worker_report.schema.json -o .agent/reports/{timestamp}-{worker}.report.json
```

将来の実行 slice では、orchestrator が `.agent/prompt_catalog/{worker}.md` を読み、
その内容を `codex exec -` の stdin に渡す。現時点では stdin へ渡す処理も
`codex exec` の subprocess 起動も実装しない。

## Worker Report Schema

`.agent/schemas/worker_report.schema.json` は Worker が返す JSON の最小契約で、
次の field を必須にする。

- `status`: `pass` / `continue` / `auto_fix` / `needs_human` / `blocked`
- `lane`: `advance` / `audit` / `fix` / `summarize` / `escalate`
- `severity`: `none` / `P3` / `P2` / `P1` / `P0`
- `summary`: 作業結果の短い説明
- `changed_files`: 変更した repo-relative path の配列
- `tests_run`: 実行した検証コマンドの配列
- `tests_status`: `not_run` / `passed` / `failed`
- `risks`: 実際に残っている risk の配列
- `next_recommended_worker`: 次に選ぶ Worker
- `human_question`: 人間判断が必要な場合の質問。不要なら空文字
- `copyable_next_prompt`: 次 Worker や人間に渡せる Prompt。不要なら空文字

`scripts/agent_gate.py` は Python stdlib だけで、この schema の `required`、
`type`、`enum`、array item type、`additionalProperties=false` を軽量検査する。
外部 dependency は追加しない。

Optional check として、将来 `jsonschema` を明示的に導入した場合だけ次のような
外部 validator を併用できる。

```powershell
uv run python -m jsonschema -i .agent/reports/report.json .agent/schemas/worker_report.schema.json
```

この optional command は現在の default path では要求しない。

## Reporting Contract

ユーザーが completion report を要求した場合、完了報告全体は one single
copyable code block として出力する。複数ブロック、ブロック外の補足、分割された
closeout は contract violation とみなす。

Worker がこの契約を満たせない、または前 Worker の completion report が契約違反
だったと判断した場合は、report の `risks` に `format_contract_violation` または
`completion_report_not_single_code_block` を入れる。この risk は gate で
`needs_human` に倒す。

Regression coverage lives in `tests/test_agent_orchestration.py`: both
`format_contract_violation` and `completion_report_not_single_code_block` are
tested as escalation-worthy worker report risks. This does not inspect chat UI
rendering directly; it fixes the report/gate contract that a Worker must use
when the single-code-block completion contract is violated.

## Scope Policy

Gate policy は `.agent/state.json` の `gate_policy` が正本である。code 内に
path policy を固定しない。

許可 scope の例:

- `.agent/state.json`
- `.agent/prompt_catalog/audit.md`
- `docs/AGENT_ORCHESTRATION.md`
- `scripts/agent_gate.py`
- `tests/test_agent_gate.py`
- `samples/_probe/example/report.json`

blocked scope の例:

- `../outside.json`
- `C:/outside/repo.json`
- `.env`
- `.git/config`
- `release/package.json`
- `published/video_metadata.json`
- `samples/production.ymmp`
- `docs/production_candidate_notes.md`

`changed_files` は repo-relative path に限定する。absolute path、`..` traversal、
blocked prefix、blocked pattern、許可 prefix 外の path は `needs_human` になる。

## needs_human 条件

`scripts/agent_gate.py` は report を読み、次のいずれかに該当したら
`needs_human` と判定する。

- report が schema validation に失敗する。
- `severity` が `P1` または `P0`
- `status` が `needs_human` または `blocked`
- `tests_status` が `failed`
- `risks` に `scope`、`rights`、`publish`、`release`、`secret`、
  `destructive`、`production_candidate`、`external_notification`、
  `format_contract_violation`、`completion_report_not_single_code_block` の
  いずれかが含まれる
- `changed_files` に repo-external traversal、blocked path、または許可scope外の
  path が含まれる

Gate は main/master への push、release、publish、rights status 変更、
`production_candidate=true` 相当の判断を自動承認しない。該当しそうな場合は
Worker report 側で risk または human question として明示する。

## Codex exec への接続手順

現時点の `agent_orchestrator.py` は dry-run と report 判定だけを行う。
次段階で実行に接続する場合は、次の順で進める。

1. command builder が返す execution plan を検証する。現時点の preview contract は
   `codex exec - --output-schema <schema> -o <report>` で、prompt は stdin 入力を
   想定する。
2. `--output-schema .agent/schemas/worker_report.schema.json` と
   `-o` / `--output-last-message .agent/reports/{timestamp}-{worker}.report.json`
   が現在の Codex CLI で期待どおり JSON report を保存できることを手動確認する。
3. `.agent/state.json` の `execution_policy.codex_exec_enabled=false`、
   `max_steps=1`、`timeout_seconds=600` を default disabled policy として維持した
   まま、実行 slice の preflight 条件を先に test する。
4. 実行を有効化する場合も、prompt path は `.agent/prompt_catalog/`、schema path は
   `.agent/schemas/`、report path は `.agent/reports/` の下に限定する。
5. 実行結果を `.agent/reports/` に保存する。
6. 保存した report を `scripts/agent_gate.py` に渡す。
7. `needs_human=true` の場合だけ `scripts/agent_notify_stub.py` を呼ぶ。
8. 外部通知を追加する場合も、まず stub の出力 payload を正本にし、API key や
   service token は repo に置かない。

`--prompt-file` や未検証の `--output` 形は、Codex CLI 側で明示確認するまで
primary preview contract にしない。

## Deliberately Unimplemented

- Real `codex exec` execution
- Passing prompt file contents to `codex exec -` stdin
- Runtime worker loop / multi-step execution
- External push notification
- API key / notification service token handling
- main/master への自動 push
- release / publish automation
- rights status automation
- `production_candidate=true` または同等の production readiness 判定
- repo 外ファイルの読み書き

## PR なし個人開発での安全境界

この基盤は個人開発の loop を速くするためのもので、merge authority や release
authority を置き換えない。

- main/master への自動 push を実装しない。
- release、publish、production candidate、rights status 変更を自動化しない。
- repo 外ファイルを読まない、編集しない。
- API key や通知 service token を要求しない。
- 大規模改変より、固定 Prompt、JSON report、gate、local stub の小さい単位を
  優先する。
- 人間判断が必要なときは `.agent/needs_human.json` を見る。

最小運用では、Automation は `agent_orchestrator.py --worker <name> --dry-run`
または `--report <path>` を起点にし、判定結果を repo 内 artifact として残す。
