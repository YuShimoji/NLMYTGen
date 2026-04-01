# Development Plan Reset (2026-03-31)

## Purpose

細かい contract 改善が連続したため、ここで次の進め方を再整理する。
主目的は「micro-fix を止める基準」と「次に evidence を取りに行く対象」を明確にすること。

## Current Assessment

| 項目 | 状態 | 判断 |
|---|---|---|
| コア artifact path | NLM transcript → YMM4 CSV → YMM4 読込 | 成立済み |
| S-5 字幕改行 | B-14 までで bulk pain はかなり減少 | 次は heuristic 追加より corpus-first |
| B-15 cue memo | proof positive | 方針メモ化の短縮として value あり |
| B-16 diagram brief | proof positive | diagram planning の白紙時間短縮として value あり |
| 現在の問題 | packet / bundle の微修正が続きやすい | 新しい evidence なしの微調整は一旦止めるべき |
| 残 bottleneck | 素材選定、図作成、フリー素材探索、動画素材の尺つなぎ | B-15/B-16 では一部しか削れていない |

## Stop Rules

次のいずれかがない限り、B-15 / B-16 の細かい contract tweak は止める。

1. 新しい rerun で明確なノイズや欠落が観測された
2. テストや bundle 生成に実害のある不具合が見つかった
3. 次の narrow feature に接続するための boundary 整理が必要になった

## Short Term

次の 1〜2 セッションでは、これだけをやる。

| 優先 | 項目 | actor | owner artifact | 完了条件 |
|---|---|---|---|---|
| 1 | B-16 rerun を 1 回実施し、selected / excluded / better / unchanged / worse を記録する | shared | `samples/*_diagram_*` proof set | rerun 差分が記録され、追加 tweak が必要か判断できる |
| 2 | B-15 / B-16 を「これ以上いじる理由があるか」で再判定する | assistant + user | `runtime-state.md`, `project-context.md` | close / tweak / hold のどれかに整理できる |
| 3 | 字幕改行は corpus-first に固定し、rule 追加は止める | assistant | canonical docs | 個別事例が集まるまで heuristic 実装を増やさない |

## Mid Term

短期の判断が終わったら、次の narrow frontier を 1 件だけ選ぶ。

| 候補 | 解決したい bottleneck | 今の判断 |
|---|---|---|
| asset brief | 素材選定前の整理不足 | strong candidate |
| search query brief | フリー素材探索の初動 | candidate |
| B-15 Phase 2 constrained rewrite | 台本接続 / 役割整合性調整 | 将来有望だが、今すぐではない |

中期の進め方はこれ。

1. B-16 rerun が positive なら、diagram brief は一旦収束候補に置く
2. 残 bottleneck を `asset brief` と `search query brief` のどちらがより直接減らすか比較する
3. 比較後、1 件だけを `proposed` に起こす
4. user approval があるまで実装しない

## Long Term

長期では、次の順で考える。

| 順位 | 項目 | 条件 |
|---|---|---|
| 1 | S-6 残 bottleneck 向けの narrow text-only support | B-16 の収束判断後 |
| 2 | B-15 Phase 2 constrained rewrite | S-6 準備支援が 2 本程度で安定した後 |
| 3 | E-01 / E-02 再評価 | L4 integration point が具体化した後 |
| 4 | quarantined 項目 (D-02 / F-01 / F-02) | 個別再審査の explicit block 後 |

## Session Plan

| セッション | 目的 | この回でやること | この回でやらないこと |
|---|---|---|---|
| 1 | B-16 rerun 回収 | human-side rerun を 1 回回し、差分を proof に書く | packet 文言の追加調整 |
| 2 | B-16 収束判断 | close / tweak / hold を決める | 新規 feature 実装 |
| 3 | 次候補比較 | `asset brief` と `search query brief` を比較する | 2 件同時 proposal |
| 4 | proposal 化 | 1 件だけ `proposed` に上げる | approval 前の実装 |

## Decision Gates

次に user judgement が必要なのは以下だけ。

| タイミング | 必要な判断 |
|---|---|
| B-16 rerun 後 | B-16 を収束扱いにするか、もう 1 回だけ tweak するか |
| 次候補比較後 | `asset brief` と `search query brief` のどちらを `proposed` にするか |
| SDK / 外部依存追加前 | boundary と value path が十分か |

## Recommended Next Action

現時点の推奨はこれ。

1. B-16 rerun の結果を待つ
2. それまでは B-15 / B-16 の微修正を止める
3. 次に備えて `asset brief` と `search query brief` の比較材料だけを整える
