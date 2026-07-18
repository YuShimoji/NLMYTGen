# Existing YMM4 Evidence Revalidation — Limitations

このpackageが受け入れるのは、既存same-machine import evidenceとcurrent
approval/content-lineage lockの互換性だけです。

| debt | state | impact | owner / revisit trigger |
| --- | --- | --- | --- |
| pronunciation / rhythm / clipping | unknown | structural import successを音声受入に拡張できない | human audio reviewer when the successor integration requires audio acceptance |
| divergent visual/provenance branch | not integrated | visual decisionへ直接進めない | future `new-banknote-successor-integration-audit-v1` |
| S04 generation-time binary / exact S05 identity | unresolved | historical provenance precisionが限定される | provenance owner when exact source identity appears |
| token-level authorship | unavailable | clause/meaning-unitを越えるauthorship比率を主張できない | only revisit with new contemporaneous evidence |

YMM4 rerun、render、production、rights、publication、master integrationは
このrevalidationに含まれません。
