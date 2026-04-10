# Asset Brief vs Search Query Brief Comparison (2026-03-31)

## Scope

- purpose: B-16 の収束判断後に、次の `proposed` 候補を `asset brief` と `search query brief` のどちらに寄せるべきか比較する
- mode: feasibility only
- owner: `assistant`

## Why This Comparison Exists

- B-15 は方針メモ化を短縮した
- B-16 は図作成前の planning を短縮した
- それでも S-6 では、素材選定とフリー素材探索が別 bottleneck として残っている
- 次は 1 件だけ narrow feature を `proposed` に上げる方針なので、候補を 2 つに絞って比較する

## Candidate Summary


| candidate          | main pain         | likely output                          | actor helped      | overlap risk      | current attractiveness |
| ------------------ | ----------------- | -------------------------------------- | ----------------- | ----------------- | ---------------------- |
| asset brief        | section ごとの素材選定迷い | 必須モチーフ、素材種別の優先順位、避けたい誤読、静止画/図/動画の向き不向き | S-6 で背景や補助素材を決める人 | B-15 cue memo と近い | strong                 |
| search query brief | フリー素材探索の初動コスト     | 検索語、除外語、探索方針、代替検索軸                     | 素材サイト検索を始める人      | asset brief と部分重複 | medium                 |


## Comparison by Decision Axis


| axis                         | asset brief                | search query brief      | current edge       |
| ---------------------------- | -------------------------- | ----------------------- | ------------------ |
| bottleneck fit               | 「何を見せるべきか」に直接効く            | 「どう探すか」に効く              | asset brief        |
| workflow insertion point     | 素材選定前の判断整理                 | 素材探索開始時の検索補助            | asset brief        |
| dependency on external sites | 低い                         | 検索先や語彙に引っ張られやすい         | asset brief        |
| overlap with existing tools  | B-15 と役割が近い                | B-15 / B-16 とは別役割にしやすい  | search query brief |
| evaluation ease              | operator が「迷いが減ったか」を判断しやすい | 検索結果の当たり外れに左右されやすい      | asset brief        |
| boundary safety              | text-only に閉じやすい           | text-only だが検索先文化へ寄りやすい | asset brief        |


## Asset Brief Shape

### Good Shape

- section ごとに「主背景 / 補助素材 / 図に逃がすべきか / 動画にする必要があるか」を整理する
- `primary_background` より一段具体的に、何が必須で何が不要かを出す
- 誤読しやすい表現や、避けたいノイズを一緒に返す

### Risk

- B-15 cue memo の粒度違いに見えると二重化しやすい
- 単なる背景候補の列挙になると value が弱い

### Safe Boundary

- 許可:
  - 素材種別の優先順位
  - 必須モチーフ
  - 補助素材の役割
  - 静止画 / 図 / 動画の向き不向き
- 禁止:
  - 素材ダウンロード
  - 検索実行
  - YMM4 配置の指定

## Search Query Brief Shape

### Good Shape

- section ごとに「探す語」「避ける語」「代替検索軸」を返す
- フリー素材探索の初手だけを速くする
- 画像 / 動画 / 図解のどれを探すべきかを検索語へ落とす

### Risk

- 素材サイトごとの癖や検索品質に結果が大きく左右される
- 何を見せるべきかが曖昧なまま検索語だけ増えると空振りしやすい

### Safe Boundary

- 許可:
  - 検索語
  - 除外語
  - 代替検索軸
  - 探索時の採用観点
- 禁止:
  - 実検索
  - 素材サイト API 連携
  - 自動取得

## Recommended Order After B-16

1. `asset brief`
2. `search query brief`

## Why Asset Brief Currently Leads

1. ユーザーが強く困っているのは、検索以前に「何を見せるか」を決める工程である
2. 図作成と同様、素材選定前の白紙時間を削る方が workflow proof を取りやすい
3. search query brief は asset brief が弱いまま先に立つと、検索語の妥当性が不安定になりやすい

## What Would Flip The Decision

次のどれかが観測されたら、search query brief を先に上げる余地がある。

1. B-16 rerun 後も「何を見せるか」は決まるが、素材探索だけが極端に遅い
2. operator から「検索語の初手だけ欲しい」という明確なフィードバックが出る
3. asset brief の spec を切ると B-15 との重複が避けられないと判明する

## Recommended Next Step

B-16 rerun が positive なら、次に `proposed` 候補として検討する本命は `asset brief`。

ただし proposal 化の前に、最低限次を 1 文ずつ言えることを確認する。

1. どの workflow step に入るか
2. 何の迷いが減るか
3. B-15 cue memo と何が違うか