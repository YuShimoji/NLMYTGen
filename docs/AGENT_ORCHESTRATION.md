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
- `--pre-execution-dry-run` で plan、preflight、preflight preview card、人間の次判断を
  Markdown で表示して止める。
- `--report <path>` で既存 report を gate に渡す。
- `needs_human=true` のときだけ notify stub を呼ぶ。

Future `codex exec` integration は別 slice で行う。現時点では実行しない。

## Repo-local 正本

- `.agent/state.json`: prompt、schema、report、log、gate policy の現在設定
- `.agent/repo_adapter.json`: current repo を reference host として記述する inert adapter 設定
- `.agent/prompt_catalog/*.md`: Worker ごとの固定 Prompt
- `.agent/schemas/worker_report.schema.json`: Worker report の JSON Schema
- `scripts/agent_gate.py`: schema validation と policy gate
- `scripts/agent_notify_stub.py`: 外部通知なしの needs-human stub
- `scripts/agent_orchestrator.py`: prompt 選択、dry-run、pre-execution preview、report 判定の入口
- `scripts/agent_operator_surface.py`: 既存 flow JSON から operator review card を出す
  read-only renderer
- `docs/AGENT_OPERATOR_SURFACE.md`: card の読み方と deterministic example

## Common Core / Repo Adapter

Common core は repo をまたいでも変えない契約だけを持つ。

- Worker report schema
- Gate の fail-closed 判定
- `needs_human` notification stub の payload shape
- dry-run command preview
- disabled execution preflight
- live repo status JSON input contract
- Worker lane の抽象名

Repo adapter は repo ごとの差分だけを持つ。現在は
`.agent/repo_adapter.json` が NLMYTGen reference host の adapter である。
この file は inert configuration であり、この slice では runtime decision に使わない。
現行の gate / preflight の runtime policy source は引き続き `.agent/state.json` である。

Adapter に置く repo-specific 情報は次のようなものに限定する。

- authority docs と read order
- known untracked allowlist
- allowed / blocked change roots
- forbidden automation domains
- worker group の構成
- report artifact policy
- mainline resume boundary
- portability notes

NLMYTGen は最初の reference host であり、universal common core ではない。YMM4、
`.ymmp`、`rights_status`、`production_candidate`、diagnostic proof / visual proof
のような NLMYTGen-specific artifact vocabulary は adapter 側の語彙として扱う。

ClipPipeGen portability は設計目標に留める。ClipPipeGen adapter、ClipPipeGen
prompt catalog、ClipPipeGen runtime policy はこの repo ではまだ実装しない。

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

Dry-run には disabled-by-default real runner preflight preview も含める。
これは将来の実行可否を構造化して返すだけで、実行はしない。dry-run preview
と fake runner helper flow は `allowed=true` になり得るが、
`safe_to_start_real_runner=false` のままにする。future real runner mode だけは、
`.agent/state.json` の `execution_policy.codex_exec_enabled=true` と explicit
human real-execution authority と clear notification policy が揃わない限り
`safe_to_start_real_runner=true` にならない。`max_steps` は loop semantics を別設計
するまで `1` だけを許可し、`timeout_seconds` は正の integer でなければ blocked に
する。

Preflight は mode、worker、prompt path、schema path、report path、command argv
shape、prompt source、repo state policy、authority、notification policy を
fail-closed で確認する。tracked dirty state、staged files、明示 allowlist 外の
untracked files、既存 report output の上書き、shell string command shape、
prompt source ambiguity、notification ambiguity は、実行前に止める。Preflight
自体は常に `codex_execution_started=false` と `real_subprocess_started=false` を
返し、runner を起動しない。

pre-execution dry-run preview 例:

```powershell
uv run python scripts/agent_orchestrator.py --worker audit --pre-execution-dry-run --repo-status-clean
```

この preview は `build_execution_plan`、`build_execution_preflight`、既存の
`render_preflight_preview_card` を組み合わせ、Markdown を stdout に出すだけで止まる。
outer preview は output location を stdout only と明示し、real execution が起きなかった
理由も preview rendering 後に停止する flow であることとして表示する。
`--repo-status-clean` は operator が直前に確認した clean 状態を明示するための入力であり、
stdout でも operator-provided assertion であって CLI が Git check した結果ではないと
表示する。CLI 自身は Git subprocess を起動しない。必要なら `--repo-status-json <repo-local-json>` で
事前に作った repo status object を渡せる。どちらの場合も `.agent/reports`、
`.agent/logs`、`.agent/needs_human.json` は作らず、worker report の gate 評価にも進まない。
planned report path は予定 path として表示されるだけで、この preview では書き込まない。
outer preview は would-be worker run の plan-level review、embedded preflight card は raw
preflight result の表示として分けて読む。表示される `safe_to_start_real_runner` と
preflight allowed は review / eligibility signal であり、実行許可ではない。
operator-provided input に credential-like 文字列が混じった場合、outer preview と
preflight card の表示では raw value を redaction する。

Future live repo status JSON is defined by
`docs/verification/LIVE-REPO-STATUS-JSON-PRODUCER-DESIGN-2026-06-13.md`.
The repo-status input audit and exact operator/preflight field mapping are
defined by
`docs/verification/COMMON-FOUNDATION-STATUS-INPUT-AUDIT-DESIGN-2026-06-15.md`.
That design replaces a bare `--repo-status-clean` assertion with a
machine-collected status object containing branch, HEAD, upstream parity,
tracked / staged / untracked state, known-untracked allowlist matching, runtime
artifact state, needs-human presence, inspected paths, command provenance,
timestamp, source provenance, adapter id, and confidence / trust boundary. The
producer is only an observer and serializer. It cannot grant real-runner
permission, cannot set `safe_to_start_real_runner=true`, and cannot write
runtime reports, logs, or needs-human state. Unknown, missing, parse-error, or
command-failure state must fail closed as `needs_human` or `blocked`.

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

## Operator Review Surface

`scripts/agent_operator_surface.py` renders an existing orchestration flow JSON
as a Markdown operator card. It is a read-only review surface: it can print a
deterministic example with `--example`, or render a JSON file that already
exists inside this repo, but it does not run Codex, start the fake runner, start
any real process, pipe stdin, create a worker loop, or send external
notifications.

The card must let a non-implementer see what was attempted, which
worker/scenario ran, whether preflight passed, whether the runner started, what
the gate decided, whether human action is required, which artifacts to inspect,
what is explicitly not happening, and the next safe action. The human-readable
contract and example live in `docs/AGENT_OPERATOR_SURFACE.md`.

The renderer also has a standalone preflight preview card for raw preflight
results. It shows whether the preflight is blocked or allowed, whether
`safe_to_start_real_runner` is true, which paths were inspected, the authority
summary, and the execution boundary. This preview adapter is read-only: it does
not run Codex, start the fake runner, create runtime artifacts, validate a worker
report, or grant permission by itself. A real runner still requires a separate
authorized execution slice after a reviewed preflight result.

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

現時点の `agent_orchestrator.py` は dry-run、pre-execution dry-run preview、report 判定だけを行う。
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

`.agent/reports/*.report.json` は local runtime artifact として扱い、default では
commit しない。durable な例が必要な場合は runtime report ではなく、明示的な
fixture または docs example として置く。

## Fake Runner Scaffold

`scripts/agent_orchestrator.py` には tests-only の fake runner helper と、tests-only
の single fake execution flow helper がある。single fake flow は `ExecutionPlan` を
作り、explicit `repo_status` 付きの `build_execution_preflight` を通過した場合だけ
fake runner を呼ぶ。fake runner は `ExecutionPlan.report_path` に synthetic report
を書き、valid report は必ず `scripts/agent_gate.py` で判定する。`needs_human=true`
の場合だけ local notify stub を呼ぶ。

Fake runner は次の失敗形を fail-closed で再現するための scaffold であり、real
`codex exec` 実行経路ではない。

- valid pass report
- valid needs-human report
- valid blocked report
- invalid JSON
- missing report
- nonzero exit
- timeout

Fake runner / single fake flow でも `codex_execution_started=false` と
`real_subprocess_started=false` を返す。これらは runtime loop ではなく、
real `codex exec` を有効化しない pre-real-execution safety scaffold である。
`subprocess.run`、stdin piping、runtime worker loop、外部通知 service はまだ実装しない。
Fake runner helper flow の preflight は local simulation の開始可否だけを判定し、
real runner start permission ではないため `safe_to_start_real_runner=false` のまま
である。

## Runtime Artifact Retention

`.agent/reports/` と `.agent/logs/` は runtime output の置き場であり、directory
placeholder だけを repo に残す。

- `.agent/reports/.gitkeep`: tracked placeholder
- `.agent/logs/.gitkeep`: tracked placeholder
- `.agent/reports/*.report.json`: local runtime artifact。default では commit しない
- `.agent/needs_human.json`: local runtime state。default では commit しない
- `.agent/logs/notify_stub.log`: local runtime output。default では commit しない

Durable な report example や fixture が必要な場合は `.agent/reports/` ではなく、
`tests/fixtures/agent_orchestration/` のような明示的な fixture path に置く。

Local runtime artifact を掃除する PowerShell 例:

```powershell
Remove-Item -Force .agent/needs_human.json, .agent/logs/notify_stub.log -ErrorAction SilentlyContinue; Get-ChildItem .agent/reports -Force | Where-Object { $_.Name -ne '.gitkeep' } | Remove-Item -Recurse -Force
```

## Deliberately Unimplemented

- Real `codex exec` execution
- Passing prompt file contents to `codex exec -` stdin
- Real subprocess runner
- Runtime worker loop / multi-step execution
- Migrating runtime decisions from `.agent/state.json` to `.agent/repo_adapter.json`
- ClipPipeGen adapter implementation
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

最小運用では、Automation は `agent_orchestrator.py --worker <name> --dry-run`、
`--pre-execution-dry-run`、または `--report <path>` を起点にする。preview-only path は
stdout の確認面であり、repo 内 runtime artifact は残さない。
