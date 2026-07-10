# User Copypaste Blocks

このファイルは、監修AIから開発AIへ渡す現行の一括 Prompt だけを保持する。
current state、再開マニュアル、案件別 handoff の置き場ではない。2026-07-10 より
前の案件別 Resume / stop / report blocks は stale branch・絶対 path・旧 gate を再注入
するため削除した。必要な履歴は Git history（`99477a0` 以前）から参照する。

## Supervisor → Developer Outcome Packet

監修AIは `<>` を repo 根拠で埋め、一つの review 可能な成果スライスとして
開発AIへ渡す。調査・実装・テスト・報告を別 Prompt にしない。意味契約は
`docs/TASK_DEVELOPMENT_CYCLE_SPEC.md` を正とする。

```text
NLMYTGen の <slice name> を一つの成果スライスとして完了してください。

state_ref:
- branch / base commit: <branch> / <commit>
- base_state_id: <現在の Project-State-ID>
- target_state_id: <この成果スライス完了時の新しい Project-State-ID>
- active artifact / primary surface: <artifact>

goal_and_bottleneck:
- 完成させる workflow 上の結果: <result>
- 今回解く摩擦: <bottleneck>

scope:
- must change: <required behavior/artifact>
- may change: 完了に必要な局所設計、同じ failure class の関連修正、fixture、限定テスト、説明・current-state 同期
- do not change: <true product/external boundaries>

autonomy:
- repo 調査、実装、関連修正、比例的なローカル検証、docs/runtime-state と docs/PROJECT_COCKPIT の同期、commit/push まで続けてよい。
- repo 根拠で決められる mechanical choice は質問しない。合理的な仮定は報告で明示する。

mode:
- <direct_development | creative_explore>
- creative_explore の場合は、高忠実度実装前に layout / language / color-type / motion / adjacent content のうち有効な軸で 2〜3 案を比較し、推奨を一つ示す。方向 signal 後は direct_development の一括 packet へ移る。
- creative_explore は product 実装・通常 commit/push を行わない。ユーザーが明示した場合だけ、採用方向の decision record / low-fi review artifact を追跡する。

stop_if:
- destructive operation、依存追加、DB/auth/API 契約変更、外部公開・権利・支払い、仕様衝突、承認済み creative direction の変更。

acceptance:
- primary review surface: <one surface>
- machine checks: <narrow checks>
- human judgement: <none or one real decision>
- replan when: <condition that changes direction>

closeout:
- ファイル一覧だけでなく、workflow/decision がどう変わったか、保証できること・できないこと、次の入口を説明する。
- runtime capsule と project cockpit の共有 state fields を target state へ更新し、`uv run python scripts/check_project_state_sync.py --expected-state-id <target_state_id>` を通す。
- validated direct_development slice は commit/push と upstream parity まで閉じる。
```

明示 `AUDIT` はこの build packet を使わず read-only phase として扱う。audit 中は
mutation、state sync、commit、push を行わず、実装へ進む Outcome Packet の delta
だけを返す。

## Follow-up delta

追撃 Prompt は方向・acceptance・hard boundary を変える情報だけに絞る。

```text
前の Outcome Packet は維持し、次の delta だけ反映してください: <delta>。
これは <direction mismatch | usable defect | polish | future idea> です。
方向 mismatch でなければ must-fix を一括修正し、同じ acceptance と closeout まで続けてください。
```
