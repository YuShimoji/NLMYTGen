# Current Basis Review Contract

現行 `runtime-state` を production path の入口へ投影し、既知の Evidence / Rule で閉じられる確認を人へ戻さないための NLMYTGen 固有契約。機械可読 projection は `episode-intake-current-basis.json`、表示先は Electron GUI の「自動動画生成」先頭である。

## 現行分類

| 分類 | 現行判断 | workflow への効果 |
| --- | --- | --- |
| Evidence / Rule で閉じる | production と最終 creative confirmation は YMM4、Python は accepted input の validation / connection に限定 | Python 代替成果物やゼロ生成 YMMP を選択肢にしない |
| Evidence / Rule で閉じる | successor episode の topic、script、material、visual language、template は未採用 | 過去 proof や benchmark を default として再利用しない |
| Evidence / Rule で閉じる | unchanged mechanical checks は readback で閉じ、YMM4 human review は changed surface と最終 creative judgement に限定 | 同じ technical confirmation の再依頼をしない |
| 人に残す | viewer outcome の三択から一件を選ぶ | 新 episode identity と downstream intake を初めて束縛できる |
| 後段まで発行しない | script の premise / audience / conclusion / factual direction、creative visual treatment、最終 YMM4 composition / subtitle | content goal が無い段階で複数質問を混ぜない |
| 旧様式として退役 | prior accepted manifest を現行 default にする導線、完成 script + IR を最初に要求する handoff、旧 review queue、benchmark style 継承 | closed identity の復活と先回り production を防ぐ |

退役は artifact の削除を意味しない。旧 manifest、proof、queue 由来の tracked evidence と dirty / ignored residue は保持し、successor authority としてだけ使用しない。

## 実行 gate

GUI main process は projection を各入口で再読する。projection が missing、malformed、または `downstream_execution_allowed=false` の場合は `CURRENT_BASIS_BLOCKED` として manifest load、runtime doctor の production preflight、legacy CSV / IR / episode-pack / packet writes、batch queue restore / plan / resume / execute、dry-run、render start を停止する。renderer の disabled state だけに依存しない。

projection は `docs/runtime-state.md` の read-only machine projection であり、別の product-state authority ではない。content goal が accepted された後も、同じ file の boolean だけを手で反転して production を許可してはならない。新 episode identity、format requirements、accepted NotebookLM script identity、material locators、YMM4 template identity、subtitle invariants が一つの user-visible intake として束縛された契約へ更新し、focused test を通す。

## 現在の停止条件

この修復は content generation、candidate generation、YMM4 output、render、rights、production、publication、upload、Board mutation を行わない。現行 human judgment は次の一件のみである。

> 次の動画で、視聴後に視聴者が得るものをどれにしますか？

回答は「一つのテーマを初見でも理解できる説明」「複数の出来事を時系列で追える整理」「資料や主張を比較して判断できる検証」のいずれか。回答後に初めて downstream intake を作る。
