# New-banknote Content Lineage

> **HUMAN-APPROVED BASELINE — HASH LOCKED — INTERNAL OBSERVATION ONLY**

この page は、提出 transcript から承認済み9-cueと YMM4 CSV までの変換を一か所で確認する primary surface です。提出 transcript は claim discovery と dialogue origin に使われましたが、事実の正本は official primary evidence です。最終文は source quotation ではなく、verified factual paraphrase、Worker editorial connective、character voice、structural roleの組合せです。

## 現在の seal

| 固定対象 | 現在値 | 効く gate |
| --- | --- | --- |
| Approval receipt | `new-banknote-script-option-a-approval-v1` / valid | 変更時は operator preflight 停止 |
| Approved commit | `b05eb3867caabda496fb9a0070d230a4e81aea01` | successor revision の起点 |
| Cue / scenes | 9 / 2-4-3 | order・scene driftを拒否 |
| Speakers | れいむ3 / まりさ6 | alias projection以外の変更を拒否 |
| Evidence | 15 claims / 20 units / 21 edges | semantic・evidence driftを拒否 |
| YMM4 | 9-row derived CSV prepared | import observation は未実施 |

## 読む順序

1. `content_change_summary.md` — transcript利用と変更内容への直接回答
2. `content_transformation_ledger.json` — T00〜T07 の stage ledger
3. `cue_lineage_matrix.json` — cueごとの raw claim / source / editorial / voice 接続
4. `human_script_approval_receipt.json` — exact approval scope と invalidation
5. `content_change_policy.json` — future change class と renewed approval gate
6. `yymm4_operator_batch/README_OPERATOR_BATCH.md` — 後続の user-operated import observation

## 境界

- raw body、source body、private path、NotebookLM link/UUIDは追跡しません。
- token-by-token origin は既存 evidence から証明できないため主張しません。
- T04 pre-editorial bytesは Git commit `a307083891cccb974021d2523a3b30e1b1c60a5c` で回収可能です。
- T06後の wording correction はこの branch へ silent patchせず、successor revision と renewed approvalを要求します。
- YMM4 launch、pronunciation acceptance、render、production、publication、rights approval はこの seal に含まれません。
