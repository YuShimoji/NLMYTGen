# Canonical Script Review — New Banknote

> **INTERNAL REVIEW — NOT FINAL — NON-PUBLIC — NON-PRODUCTION**

このページがhuman reviewの主画面です。既存のNotebookLM会話から事実の意味単位を検証済みclaimへ結び、公式一次資料で支えられる範囲だけを9キューへ短く整えたうえで、用語・情報密度・掛け合いを編集収束しました。

## いま判断できること

- 公式source capture: 13件。S10/S11はexact、S04は同名の現行公式document（生成時byte同一性は未証明）、S05はexact未解決でofficial equivalentを分離。
- claim adjudication: 182/182。verified-primaryは19件。
- script: 9 cues、S1/S2/S3 = 2/4/3、れいむ/まりさ = 3/6。意味単位から計算したunsupported claimは0件。
- editorial revision: シリーズ記号を発話から外し、cue 8を3事実へ絞り、確認方法をルーペまで具体化。外した検証済みclaimは非発話レーンへ保持。
- CSV: canonicalとYMM4-character derivedの2本。本文と順序は同一で、話者列だけを変換。

## 編集来歴

- 事実部分は claim と official source に接続されています。
- 会話構造、接続、圧縮、話者らしさは editorial synthesis として区別しています。
- current execution contractで現在の9 cueを継続するbounded approvalを記録しています。独立した同時点receiptはなく、将来の silent edit も含みません。
- 以前の user-submitted script の取り込みは、利用可能な repo 証拠からは証明されていません。
- 詳細: [Editorial Provenance](editorial_provenance/README_EDITORIAL_PROVENANCE.md)

## Script

| # | Scene | Speaker | Spoken text |
| ---: | --- | --- | --- |
| 1 | S1 | れいむ | 2024年に発行された新しいお札って、見た目以外にも変わったところがあるの？ |
| 2 | S1 | まりさ | あるぞ。偽造防止では、高精細すき入れや3Dホログラムなど複数の技術を組み合わせている。誰にとっても使いやすいユニバーサルデザインも取り入れたんだ。 |
| 3 | S2 | まりさ | まずは高精細すき入れ。光に透かすと、細かな模様が見えるんだぜ。 |
| 4 | S2 | まりさ | 次は3Dホログラム。角度を変えると、三次元の肖像が回転して見えるぞ。 |
| 5 | S2 | れいむ | 触るとざらざらするのは、額面数字などのインキを高く盛り上げる深凹版印刷なんだね。 |
| 6 | S2 | まりさ | マイクロ文字の『NIPPONGINKO』は、ルーペで確かめられる。カラーコピー機では再現が難しいほど小さい文字なんだ。 |
| 7 | S3 | まりさ | 見分けやすさの工夫では、識別マークを11本の斜線にそろえ、券種ごとに位置を変えているぜ。 |
| 8 | S3 | れいむ | 額面の数字は前のシリーズのお札より大きい。一万円券と千円券ではホログラムの形や位置が違い、千円券の中央には橙色のグラデーションもあるんだね。 |
| 9 | S3 | まりさ | 確かめ方は、透かす、触る、傾ける、ルーペで見る。この四つを覚えておこう。 |

## Reviewの進め方

`operator_review_sheet.md`の5問に沿って、事実の伝わり方、誤解を招く含意、掛け合い、3 sceneの流れ、専門語の難しさを確認してください。

改訂理由と証拠の移動は`canonical_script_editorial_revision.md`にまとめています。

この候補はeditorial acceptanceでもYMM4投入承認でもありません。修正判断後にだけ、次のbounded operator batchへ進めます。
