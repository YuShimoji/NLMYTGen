# Task Development Cycle Spec

この文書は、NLMYTGen でタスクごとに **改善 → レビュー → 判断 → 次 artifact** を回すための正本である。

目的は、仕様・proof・YMM4 確認・GUI 操作が散逸し、何を見れば次に進めるか分からなくなる状態を防ぐこと。新しい実装を増やす前に、各タスクがどの surface で判断され、どの artifact で次へ進むかを固定する。

## レーン優先度

NLMYTGen の本流は、ゆっくり解説動画の制作ワークフローである。つまり、台本診断、CSV、YMM4 台本読込、Production IR、演出配置、茶番劇、サムネイル、投稿準備を、ゆっくり解説の完成動画へ接続することを主軸とする。

Baseball Info / `sports_news` は大きなサイドクエストであり、本流の `runtime-state.md` `Recommended-Next` を置き換えない。Baseball を進める場合は、チャットで明示的に Baseball sidequest として依頼する。専用 Prompt md は作らず、本書と Baseball 正本 docs の境界に従う。

サイドクエスト中でも、共通サイクルは本書を使う。ただし closeout では、本流へ戻すものと Baseball lane に閉じるものを分けて記録する。

## 共通サイクル

| 段階 | 目的 | 必須 artifact | 見る場所 | 次に進める条件 |
| --- | --- | --- | --- | --- |
| `0. product direction check` | 高コストな visible product artifact の方向を先に決める | 2〜3 案の低fi比較 + creative decision record | wireframe / representative frame | 採用方向・避ける方向・固定条件が明確。bug fix や承認済み system 内変更では省略可 |
| `1. plan` | 何を改善するかを狭める | task brief / screen plan / scene bible | Markdown / YAML / JSON | 目的・対象範囲・見ないものが明確 |
| `2. build review surface` | 良し悪しを見える形にする | review memo / preview / `.ymmp` / readback | GUI または YMM4 のどちらか一方 | 判断対象が場面・画面・区間単位に分かれている |
| `3. machine proof` | 接続・構造・禁則を確認する | validator result / readback JSON / parse result | CLI / GUI result panel | failure class または pass が機械的に読める |
| `4. human signal` | creative / editorial 判断を受ける | reviewer-facing memo | Markdown / YMM4 final check | 違和感・不足・優先度・弱い仮定を自然文で返せる |
| `5. close gate` | 次 artifact を決める | close decision record | runtime-state / lane doc | `proceed / revise / split / cut / blocked` のいずれか |

レビュー surface は「HTML も JSON も `.ymmp` も全部見てください」ではなく、毎回 1 つを primary にする。補助 artifact は evidence として扱い、判断導線の代替にしない。

### Visible product の Direction Check と集約修正

この節は layout、表示言語、content format、animation などの product design をレビューする方法であり、AI Worker の実行権限や停止条件を定義しない。

- 新しい layout / visual language / i18n 方針 / content format / animation system は、約 10% の低fi 2〜3 案を先に比較する。比較軸を同質化させず、各案で何が可能になるかを示す。
- 採用後は代表 1 画面・1 区間を約 40% の fidelity で確認し、問題がなければ token / component / layout rule として横展開する。
- 完成面の feedback は `direction mismatch` / `usable defect` / `polish` / `future idea` に整理し、must-fix を一回の revision batch にする。
- 方向 mismatch は局所修正で吸収しない。Direction Check へ戻る。polish と future idea は、現在の acceptance を壊さない限り次 slice 候補へ分ける。
- 同じ局所修正が 2 回続いた場合、3 回目は system debt として設計を見直す。

## 茶番劇 / Real Estate DX

G-24 は `skit_group` の template-first 基盤で閉じる。Real Estate DX 固有の素材不足、proxy 採否、場面ごとの良し悪し判断は G-27 の範囲とする。

### G-27 のサイクル

| 段階 | artifact | 判断 |
| --- | --- | --- |
| scene bible | block ごとの line range / cast continuity / props / screen placement | 背景劇が語り手リアクションではなく独立小場面になっているか |
| validator | `background_skit_blueprint.json` + `validate-background-skit-blueprint` result | `passed` 以外は cast motion IR / production timing へ進めない |
| GUI Review Console | `review_packet` を GUI で台本概略・全体構成・台本抜粋付きカード化し、`review_decisions` を保存 | 画面内物語として意味が通るか、修正・統合・proxy 整理へ回すか |
| asset decision | `production template exists` / `accepted proxy` / `cut from plan` | 各場面を production に残すか、proxy で進めるか、削るか |
| revised blueprint | asset decision を反映した blueprint / gap report | validator 再実行または明示 blocked closeout へ進めるか |

G-27 の close gate は、全場面が次のいずれかに分類された状態である。

- `production template exists`: production 用 template / props が存在し、readback 可能。
- `accepted proxy`: proxy で進める理由、弱い仮定、後で置換する条件が明示済み。
- `cut from plan`: 情報価値・素材負荷・画面密度の観点で削る判断が記録済み。

`validator: blocked` は失敗ではない。ただし、その状態で許可されるのは validator の `allowed_next_actions` に明記された review artifact だけであり、YMM4 creative acceptance / production timing / cast motion IR へ進めない。

## Baseball Info / sports_news

Baseball Info は InfoGraphics 駆動で進めるが、最初のレビュー単位は renderer や export ではなく **screen plan** とする。台本から動画全体の画面・情報量・構成が見えるまで、PNG export や YMM4 placement を最終 proof として扱わない。

この節は、本流の現在タスクではなく、明示的に起動した Baseball sidequest の review cycle である。Baseball 側の変更は原則として `lanes/sports_news/`、`BaseballInfoGraphics/`、および Baseball 正本 docs に閉じ、本流の G-27 / ゆっくり解説制作導線を押し流さない。

### screen plan の最低項目

| 項目 | 内容 |
| --- | --- |
| segment id | 台本内の区間 ID |
| script range | 台本行または秒数範囲 |
| viewer question | 視聴者に何を理解させる場面か |
| card sequence | 使う card type の順序 |
| information budget | 主要数値・固有名・比較・反応の上限 |
| primary screen | BaseballInfoGraphics / card template / YMM4-only のいずれか |
| duration | 表示秒数または voice 区間 |
| YMM4 placement | `ImageItem` / `VideoItem` / text-only note のいずれか |
| review signal | どこが過密・不足・退屈・誤読になりそうか |

### YMM4 placement 方針

- React / HTML を直接 YMM4 に入れない。
- Phase 1 は 1280x720 PNG を専用 layer の `ImageItem` として配置する。
- Phase 2 は deterministic animated clip を `VideoItem` として配置する。
- `BaseballInfoGraphics/` は design source であり、production proof ではない。
- 別出力の prototype が必要な場合だけ、`BaseballInfoGraphics/` 配下に review-only prototype を作る。

## GUI / YMM4 レビュー統一

GUI は artifact 作成、dry run、validator/readback の確認に使う。YMM4 は template 登録、全素材後の配置、明示 creative acceptance に使う。レビューごとに primary surface を 1 つ決める。

| タスク種別 | GUI で見るもの | YMM4 で見るもの | YMM4 を開かない条件 |
| --- | --- | --- | --- |
| CSV / 台本診断 | CSV result / stats / diagnostic JSON | なし | 機械結果だけで判断できる |
| IR / patch | validate / dry run / apply JSON / readback | final composition だけ | failure class が GUI で読める |
| 茶番劇 review | GUI Review Console / review packet / validator | accepted proxy 後の composition | validator が blocked |
| Baseball screen plan | screen plan / card order / information budget | PNG/clip placement proof | screen plan が未レビュー |
| Thumbnail | design JSON / slot audit / patch readback | final thumbnail composition | 実 template が存在しない |

CLI だけでしか確認できない操作が production loop に残った場合は、標準運用として固定せず、GUI 補完タスクとして起票する。

## Closeout contract

各タスクの closeout は、ファイル一覧ではなく次を本文で説明する。

- 何を改善したか。
- primary review surface は何か。
- machine proof は何を保証し、何を保証しないか。
- human signal は何を返せば次に進めるか。
- 次 artifact は assistant / user / both のどちらが作るか。
- production へ進めない場合、どの gate で止めたか。

この contract を満たさない報告は、完了ではなく review-loop 未接続として扱う。
