# G-26 Visual Acceptance Pack — 2026-04-30

## Purpose

G-26 の Slice 3 / Slice 4 本線と競合しないよう、この文書は **visual acceptance / QA pack** だけを扱う。対象は既存の review artifact を YMM4 で目視確認し、各 recipe を `proposed` から昇格可能か分類するための受入手順である。

この作業では recipe 生成ロジック、production placement、registry promotion は行わない。

## Active Review Target

| Role | Path | Notes |
| --- | --- | --- |
| Review `.ymmp` | `_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1.ymmp` | YMM4 で開く主対象 |
| Readback | `_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1_readback.json` | 機械検証の正本 |
| Manifest | `_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1_manifest.md` | recipe 意図・route 値の参照 |
| Inventory | `_tmp/g26/acceptance_pack/recipe_inventory.json` | 目視確認用の棚卸し |
| Acceptance Sheet | `_tmp/g26/acceptance_pack/visual_acceptance_sheet.md` | frame 順チェックシート |
| Promotion Log Template | `_tmp/g26/acceptance_pack/promotion_log.template.json` | 昇格記録のテンプレート |

## Comparison Corpus

以下は候補コーパス / 履歴として読む。単体では acceptance evidence ではない。

| Corpus | Path | Role |
| --- | --- | --- |
| Composition palette v2 | `_tmp/g26/composition/演出_palette_v2.ymmp` | 比較的良い composition palette。候補コーパス扱い |
| Recipe lab history | `_tmp/g26/recipe_lab/g26_goal_motion_recipe_lab.ymmp` | 旧 lab / chain 試作の履歴 |

## Machine Readback Baseline

`g26_motion_recipe_review_v1_readback.json` の baseline は以下で固定する。

| Check | Expected | Result |
| --- | ---: | ---: |
| `recipe_count` | 12 | 12 |
| `recipe_group_count` | 12 | 12 |
| `recipe_image_count` | 24 | 24 |
| `posix_asset_paths` | 0 | 0 |
| `blank_asset_paths` | 0 | 0 |
| `openability.success` | `true` | `true` |

Known warning:

- `CameraShakeEffect` is community-plugin dependent. 未導入環境で読めない場合は recipe failure ではなく `community plugin missing` に分類する。

## Frame Review Table

YMM4 では下表の frame を順に確認する。全 recipe は開始時点では `proposed` であり、目視判定なしに `accepted_candidate` へ昇格しない。

| Frame | Recipe | Goal | Initial Status |
| ---: | --- | --- | --- |
| 0 | `nod_clear` | 明確な頷き | `proposed` |
| 140 | `nod_subtle` | 小さな頷き / 相槌 | `proposed` |
| 280 | `nod_double` | 強めの二回頷き | `proposed` |
| 420 | `jump_small` | 小ジャンプ | `proposed` |
| 560 | `jump_high` | 高いジャンプ | `proposed` |
| 700 | `jump_emphasis` | 着地沈み込み付きジャンプ | `proposed` |
| 840 | `panic_crash` | パニック衝撃 | `proposed` |
| 980 | `shocked_jump` | 驚きジャンプ | `proposed` |
| 1120 | `surprised_chromatic` | 色ズレ込みの驚き | `proposed` |
| 1260 | `anger_outburst` | 怒りの震え / 爆発 | `proposed` |
| 1400 | `shobon_droop` | しょんぼり沈む | `proposed` |
| 1540 | `lean_curious` | 気になる / 身を乗り出す | `proposed` |

## Acceptance Classes

判定値は以下のいずれかに固定する。

- `pass`: 意図した動きとして読める。body/face drift がなく、screen spacing も許容範囲。
- `wrong motion`: 目標演出と別の動きに見える。
- `body-face drift`: body と face の追従が崩れる。
- `too subtle`: 意図が弱すぎて伝わらない。
- `too strong`: 動きが過剰で用途に対して強すぎる。
- `screen spacing`: 画面内位置・余白・はみ出しに問題がある。
- `asset path`: 画像参照や asset path に問題がある。
- `openability`: YMM4 で開けない、または project canvas として読めない。
- `community plugin missing`: community plugin 依存 effect が未導入で確認できない。

## Promotion Rules

| From | To | Condition |
| --- | --- | --- |
| `proposed` | `accepted_candidate` | 単体 recipe が YMM4 目視で `pass` |
| `proposed` | stays `proposed` | `pass` 以外。failure class と memo を記録 |
| `accepted_candidate` | `compatibility_evidence` | YMM4 上の chain / 連続動作として読めることを別途確認 |

`compatible_after` / `forbidden_after` は chain を実 clip として観測してから記録する。単体 recipe の `pass` だけで compatibility を推測しない。

## Operator Workflow

1. YMM4 で `_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1.ymmp` を開く。
2. `_tmp/g26/acceptance_pack/visual_acceptance_sheet.md` の frame 順に 12 recipe を確認する。
3. 各 recipe を acceptance class のいずれかで分類し、短い memo を残す。
4. `promotion_log.template.json` をコピーして、`result`, `operator_note`, `checked_frame`, `evidence_source` を埋める。
5. `pass` の単体 recipe だけを `accepted_candidate` 候補にする。
6. chain / compatibility は、連続動作として YMM4 で読めたものだけ `compatibility_evidence` 候補にする。

## Non-Conflict Boundary

この acceptance pack lane では以下を編集しない。

- `src/pipeline/motion_recipe.py`
- `docs/MOTION_PRODUCTION_PIPELINE.md`
- `docs/MOTION_RECIPE_LOOP_TIMING.md`
- `docs/S5-motion-brief-prompt.md`

また、以下も範囲外とする。

- G-24 production placement 接続
- `FEATURE_REGISTRY` の昇格更新
- recipe generator / effect shortlist logic の変更
- Python preview / rendering

## Next Evidence

この pack の完了条件は、12 recipe の目視分類が埋まり、`pass` と failure class が分離されること。`accepted_candidate` が増えた後にのみ、chain review と `compatibility_evidence` への昇格を別スライスで扱う。
