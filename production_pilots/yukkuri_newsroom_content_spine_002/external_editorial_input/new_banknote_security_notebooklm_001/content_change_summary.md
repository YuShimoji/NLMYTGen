# 承認済みコンテンツの変更要約

## 提出 transcript は使われたか

はい。提出された NotebookLM Audio Overview transcript は、326 logical lines の immutable raw identity と line fingerprint を起点に 182 claim candidates へ整理されました。最終 cue はその raw claim ID を origin として参照します。ただし、raw transcript は factual authority ではなく、長い原文や token 単位の著者推定もこの package には含めません。

## 何が残り、何が除外されたか

数値 funnel は **326 lines → 182 claim candidates → 19 verified-primary → 15 adopted claims → 20 factual units / 21 evidence edges → 9 cues** です。残った内容 family は、発行年、高精細すき入れ、3D hologram、深凹版印刷、micro文字、識別 mark、額面表示・配置・色の工夫です。

claim outcome は次のとおりです。

| 判定 | 件数 | canonical への影響 |
| --- | ---: | --- |
| verified_primary | 19 | うち15 unique claimsを採用 |
| supported_context_only | 11 | 背景のみ、発話には不採用 |
| unresolved_not_used | 31 | 未解決のため不採用 |
| rejected_unsupported | 15 | 一次資料不足で除外 |
| rejected_policy_intent | 10 | 政策意図・cashless誘導の推測を除外 |
| rejected_quantitative_without_exact_source | 18 | exact sourceのない数値を除外 |
| style_or_rhetoric_only | 52 | rhetoricとしてのみ保持 |
| duplicate_not_used | 26 | 重複として不採用 |

verified-primary でも claim_095、claim_158、claim_162、claim_164 は最終発話に採用していません。claim_158 は cue_008 の情報量を抑えるため近接 retention lane に残り、ほかは claim adjudication に残っています。

## Worker が変えたもの

T04 では verified propositions を 2/4/3 scene、れいむ3・まりさ6の9-cue dialogueへ supported-only constrained rewrite しました。これは source quotation ではなく、factual paraphrase と Worker-authored structure / connective / character voice の組合せです。

T05 では opening の question/answer、spoken terminology、cue_008 density、まりさ endings、loupe の具体化を収束させました。cue数は9のまま、factual units は22→20、claim edgesは23→21、unique adopted claimsは17→15になりました。根拠 source identity は変えていません。

## 人が承認したもの

人が新たに本文を書いたとは主張しません。人が行ったのは option A による現在の text、order、scene、casting、CSV projection、claim/source traceability の明示承認です。その exact baseline は `b05eb3867caabda496fb9a0070d230a4e81aea01` と8 file hashesで固定されています。

## 承認を無効にするもの

承認 file の hash、cue text/order/speaker/scene、claim adoption/evidence edge、canonical/derived CSV text/orderのいずれかが変われば承認は無効です。品質向上を理由にした silent fix も認めません。

## 将来変更の出し方

M_MECHANICAL は content hash が不変なら logged validation だけで承認を維持できます。E_EDITORIAL_EVIDENCE_PRESERVING、S_SEMANTIC、U_UPSTREAM は別 revision ID、visible diff、updated ledgerを作り、既存 receipt を上書きせず successor receipt に renewed human approval を記録します。
