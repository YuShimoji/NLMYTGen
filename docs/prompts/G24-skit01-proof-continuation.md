# G24 skit_01 E2E proof 継続 Prompt

> **用途**: NLMYTGen の G-24 主軸を次セッションで継続するための委任 Prompt。
> user が `YMM4_RESULT` と `YMM4_NG_DETAIL` を埋めてから assistant に渡す。
> **2026-04-20 追記**: この Prompt は workflow breakage 前提の stale 版。`_tmp/skit_01_v2.ymmp` / ManualSample gate を前提にしない。再利用する場合は [skit_01-workflow-breakage-audit-2026-04-20.md](../verification/skit_01-workflow-breakage-audit-2026-04-20.md) を先に読んで更新すること。**更新前のそのまま実行は禁止**。

---

NLMYTGen の次作業を進めます。まず `/mnt/c/Users/PLANNER007/NLMYTGen/AGENTS.md` の再アンカリング手順に従って、この repo 内だけを読んでください。repo docs を正本とし、過去チャット要約より優先してください。

前提:
- 現在の主軸 frontier は `G-24（茶番劇 Group template-first 運用）`
- 直近で assistant 側は `skit_01 E2E proof` に向けた registry/spec/proof 整合を実施済み
- 直近報告の trusted な要点は以下です
  - `samples/registry_template/skit_group_registry.template.json` を v1.1 相当に更新し、`skit_01` proof で実証済みの 5 motion intent (`enter_from_left` / `surprise_oneshot` / `deny_oneshot` / `exit_left` / `nod`) に揃えた
  - `SKIT_GROUP_TEMPLATE_SPEC.md` §3.3 と `docs/verification/skit_01_delivery_dispute_v1_2026-04-19.md` も整合済み
  - 機械検証は `apply-production exit 0 / fatal 0 / face_changes 50 / motion writes 10`
- 旧 gate（**現在は無効**）: user による YMM4 上の `_tmp/skit_01_v2.ymmp` の 4 scene 視覚確認だけ
- 今回の manual result は以下です:
  - `YMM4_RESULT = OK`
  - `YMM4_NG_DETAIL = `（NG 時のみ記入。scene 番号 + 所見を 1-2 行。例: `scene 2: surprise が斜めに見える`）
- 最近持ち込まれた `session 105 / 107 / 109 / 110`、`sections-nav.spec.js`、`ui-mode-consistency.spec.js`、`gadgets-documents-tree.js` などの報告は、この repo の文脈と接続しないため **NLMYTGen の進捗として採用しない**。別案件混入の可能性が高いので quarantine 相当で扱うこと
- repo 外のファイル・memory・docs は読まないこと
- 未承認 feature は増やさないこと
- broad question で止まらないこと

今回のタスク:
- `YMM4_RESULT` を起点に、`skit_01 E2E proof` を前に進める
- `YMM4_RESULT = OK` の場合:
  1. `skit_01 E2E proof` を完了扱いにするための repo 正本同期を行う
  2. 必要な verification / runtime-state / project-context の更新を最小範囲で実施する
  3. `G-24` 主軸との関係が崩れないように、active artifact / bottleneck / next_action を同期する
  4. 変更に対するローカル検証を必要十分だけ実行する
- `YMM4_RESULT = NG` の場合:
  1. `skit_01` の NG を `YMM4_NG_DETAIL` に基づき failure class 単位に切り分ける
  2. approved / done 機能の範囲内で最小修正だけ行う
  3. `apply-production` など機械検証まで通す
  4. 次に user が返すべき確認項目を `OK / NG` で返せる粒度に圧縮して残す
- どちらの場合も、主軸から外れる docs-only 整理や別案件調査には逸れないこと

最初の応答では次の3点だけ簡潔に出してください。
1. `📍 NLMYTGen / 🧩 [現在のスライス] / 🔲 [次のアクション]`
2. trusted な active artifact / bottleneck / change relation
3. 今回このブロックで実行する具体タスク 1 件

その後は停止せずに、実装・関連修正・ローカル検証・必要な正本同期まで継続してください。
破壊的変更、依存追加、DB/認証/API 契約変更、仕様競合がある場合のみ停止してください。

完了報告は簡潔に、以下の3項目だけ述べてください。
- 変更点
- 検証結果
- 残課題
