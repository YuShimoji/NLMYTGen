# G-27 Compact Review Candidate Gate 2026-05-26

この記録は、G-27 Real Estate DX の次工程を `.ymmp` 書き出しへ進める前に、7 ready candidates の compact review gate と operator 境界を固定するためのもの。Feed / RSS reader 連携、Baseball / sports_news、Python CLI、GUI、DB / API、依存関係、FEATURE status はこの gate の対象外。

## Gate で固定する判断面

Primary evidence は `samples/_probe/g24/real_estate_dx_adapter_ir_dry_run.json`。既存の `samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json` は reference evidence として参照するが、この slice では再生成・昇格しない。ここで固定するのは「次に compact review へ載せてよい候補集合」であり、YMM4 adapter output や `.ymmp` patch ではない。

| 候補 | 表示意図 | layer / duration | placeholder / primitive | この gate での扱い |
| --- | --- | --- | --- | --- |
| `RE-02-beginning` | 公開検索が薄れ、背後の汎用業者 DB パネルが見える | layer 7 / 360 frames | `generic_public_search_panel + broker_db_shadow_panel` | compact review 候補として固定 |
| `RE-02-development` | 業者 DB から公開ポータルへ物件カードが流れる | layer 7 / 360 frames | `broker_db_panel + public_portal_card + property_card_flow` | compact review 候補として固定 |
| `RE-06-beginning` | 物件カード群が上部に密集し、字幕帯を空ける | layer 7 / 360 frames | `property_card_overload_cluster` | compact review 候補として固定 |
| `RE-06-development` | ノイズの中から選択物件と drawback marker が残る | layer 7 / 360 frames | `selected_property_sheet + drawback_marker` | compact review 候補として固定 |
| `RE-06-turn` | 物件ドキュメント比較で推薦の編集性を見せる | layer 7 / 360 frames | `property_document_editorial_comparison` | compact review 候補として固定 |
| `RE-07D-beginning` | AI 推薦パネルが物件カードを confident match として強調する | layer 7 / 360 frames | `abstract_ai_recommendation_panel + property_card` | compact review 候補として固定 |
| `RE-07D-development` | 境界・相続・近隣リスク marker を背後に出す | layer 7 / 360 frames | `boundary_inheritance_neighborhood_risk_markers` | compact review 候補として固定 |

`RE-02-turn` は opacity-layer adjustment が route candidate に反映されるまで混入させない。`RE-07D-turn` は specialist / cast / silhouette 方針が決まるまで deferred のままにする。この 2 件を混ぜないことが、次の `.ymmp` write 可否判断を汚さないための最重要条件。

## Operator 向けの短い禁止境界

この gate で許可されるのは、dry-run / compact review evidence を読み、7 件の候補集合と除外 2 件の境界を記録し、consistency check を通すことだけ。まだ production output ではなく、YMM4 上の見え方を新規に受け入れたわけでもない。

| いま許可 | まだ禁止 | 禁止を外すために必要な次 gate |
| --- | --- | --- |
| adapter IR dry-run の review | YMM4 adapter output | adapter output の対象・item 仕様・戻し条件を別 gate で固定 |
| compact review candidate set の記録 | YMM4 patch / `.ymmp` write | 書き込み対象ファイル、差分許容範囲、readback 成功条件を別 gate で固定 |
| 既存 compact review artifact の参照 | render / preview capture | `.ymmp` write 後に初めて preview / render gate を開く |
| route / authorization / review packet consistency check | production timing / creative acceptance | timing と creative acceptance は YMM4 proof 後に別判断 |

この短い境界により、dry-run で `ready` と言っている状態を「すぐ書き出してよい」と読み違えないようにする。

## `RE-02-turn` を戻すための route adjustment 条件

`RE-02-turn` は accepted-with-adjustment の方向性があるが、現時点では 7 candidates の route candidate に反映されていない。次に戻すなら、wall / gate / locked-room 系の literal boundary に寄せず、公開ポータルと業者 DB の opacity-layer transition として表現する。

| 条件 | 目的 | 満たすと可能になること |
| --- | --- | --- |
| abstract UI / opacity-layer primitive として再定義 | 閉じ込め・壁・鍵の誤読を避ける | 8 件目候補として route preflight に戻せる |
| subtitle safe area を侵入しない item 配置にする | 既存 G-27 layout proof と矛盾させない | compact review の同一基準で比較できる |
| official UI / brand / REINS 画面を出さない | 権利・実在画面誤認のリスクを避ける | 汎用 placeholder として production gate に残せる |
| candidate id / readiness / blocked reason を artifact 側に反映 | dry-run と compact review の集合差を消す | 7 件 gate から 8 件 gate へ拡張判断できる |

推奨は、`.ymmp` write gate の前にこの修正を急がず、まず 7 件で compact review 判断面を閉じること。`RE-02-turn` は次の route adjustment slice で扱う方が、候補集合の揺れを抑えられる。

## `RE-07D-turn` の policy decision packet

`RE-07D-turn` は specialist / cast / silhouette の扱いが未決のため、今回の compact review gate には入れない。次に扱う場合は、どの representation policy を選ぶかで必要素材と判断責任が変わる。

| 選択肢 | 摩擦が減る工程 | 代償 / 注意点 | 推奨度 |
| --- | --- | --- | --- |
| keep deferred | 7 件 compact review をすぐ進められる | `RE-07D-turn` は引き続き欠番 | 高: いまの主軸を止めない |
| cut from plan | specialist 表現の未決を消せる | beat の説明力が落ちる可能性 | 中: 台本上なくても成立するなら有効 |
| abstract silhouette | 実素材なしで「専門家らしさ」を置ける | human-like silhouette の誤読・既存 mediator 失敗に注意 | 中: SCS / YMM4 proof が必要 |
| real asset / cast | 最も具体的で production に近い | 素材調達・権利・キャラ設計判断が必要 | 低: 今すぐの gate には重い |

この slice の推奨は keep deferred。`RE-07D-turn` は compact review gate の外に置き、次に policy decision を開く場合だけ上表から選ぶ。

## 低負荷並行候補としての H-02

H-02 実サムネ proof は、G-27 の判断待ちが発生した場合だけ低負荷で起動する。実 template がある場合に限り slot audit / patch proof を確認し、G-27 の候補集合や `.ymmp` write 判断とは混ぜない。

## この gate の完了条件

- 7 ready candidates だけが compact review candidate set として記録されている。
- `RE-02-turn` は blocked、`RE-07D-turn` は deferred のまま残る。
- 既存 compact review artifact は reference evidence のままで、再生成・昇格されていない。
- YMM4 patch、`.ymmp` write、render、production timing、creative acceptance はまだ禁止として読める。
- G-27 gate 系チェックと `git diff --check` が通る。

## 検証結果

2026-05-26 のこの slice では、`node scripts/build_g27_adapter_ir_dry_run.js`、`node scripts/check_g27_adapter_authorization_gate.js`、`node scripts/check_g27_adapter_route_preflight.js`、`node scripts/check_g27_review_packet.js`、`git diff --check` が通過した。`src/` / `gui/` を触っていないため `uv run pytest` は実行していない。
