# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-current-lineage-yymm4-evidence-revalidated-v1
State-Revision: 2026-07-19.1
Updated: 2026-07-19 JST
Product-State: new-banknote-existing-yymm4-import-evidence-current-lineage-compatible
Product-Gate: new-banknote-successor-branch-integration-audit
Recommended-Next: audit-and-integrate-new-banknote-successor-branches
External-State: public-repo-feature-branch
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0
Tracked-Worktree: clean; intentional ignored evidence retained

このページは public repository で現在地を読むための追跡済み Markdown です。
短期 capsule は [runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task 経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipeline は
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd) にあります。

## いまの一文

人が option A で承認した新紙幣9-cue scriptとT00–T07 lineageを変更せず、
同端末の既存ignored YMM4 project/result/batch stateをread-onlyで再検証しました。
current approval/hash/text/order/timingとの互換性をsanitized tracked receiptで固定済みで、
次は分岐したsuccessor branchesのG1 integration auditです。

## 判断に使える現在地

| 対象 | 現在状態 | 次の gate で確認すること |
| --- | --- | --- |
| Approval | `b05eb386…`、9 cues、2/4/3、Reimu/Marisa 3/6、8 hashesをreceiptで固定。変更なし | branch側のhash、text/order、speaker/scene、claim/evidence、CSV driftを拒否 |
| Lineage | T00–T07、15 adopted claims、20 units、21 edges、unsupported spoken claims 0 | lineage authorityとsuccessor branch provenanceの重複・競合を分類 |
| Existing YMM4 evidence | 既存3ファイルを非破壊再読取。9/3/6、exact text/order、4415 frames、73.583333秒、timing一致 | tracked receiptを維持したままcompatible commitsだけを統合 |
| Immutability | 生成前後の存在・size・mtime・SHA-256一致。YMM4再実行なし | G1でもignored source evidenceに書かない |
| Audio quality | pronunciation / rhythm / clippingは`unknown` | audio acceptanceが必要な時だけhuman reviewを別gate化 |
| Privacy | tracked packageにprivate path、local binary、NotebookLM URL/UUID、raw/source bodyなし | 統合候補にも同じ境界を適用 |
| Divergence | visual/provenance branch未統合 | ancestry、write set、authority、A/B/C成果物、validation planを先に監査 |

Primary surface:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_EXISTING_YMM4_EVIDENCE_REVALIDATION.md`

## 次の入口

G1ではnew-banknote successor branchesをread-firstで監査し、branch ancestry、write set、
content authority、provenance、visual-direction artifacts、current approval locksを比較します。
互換commitと検証計画が確定するまでmerge/rebase/cherry-pickは行いません。

## 公開・実行境界

このsliceではapproved contentを変更せず、YMM4 launch/rerun、Computer Use、NotebookLM、
web fetch、render/media生成、production、public/rights action、master integrationを
行っていません。構造的import互換性は発音・visual・production・publicationの承認ではありません。
