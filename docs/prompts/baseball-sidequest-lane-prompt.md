# Baseball Sidequest Lane Prompt

この Prompt は、Baseball / `sports_news` を NLMYTGen の本流から分離して進めるための依頼テンプレートである。

NLMYTGen の本流は、ゆっくり解説動画の制作ワークフローである。Baseball は大きなサイドクエストとして扱い、本流の `runtime-state.md` `next_action` を置き換えない。

## Copy Prompt

```text
この依頼は NLMYTGen の本流（ゆっくり解説動画制作ワークフロー / 現行 G-27 Real Estate DX / 茶番劇 review cycle）ではなく、Baseball / sports_news のサイドクエストです。

目的:
- Baseball Info / sports_news を本流から分離したレーンとして進める。
- 最初のレビュー単位は renderer / export / YMM4 proof ではなく screen plan にする。
- 台本セグメントごとの card sequence、information budget、画面目的、秒数、YMM4 placement を見える化する。

読む正本:
- docs/REPO_LOCAL_RULES.md
- docs/runtime-state.md
- docs/TASK_DEVELOPMENT_CYCLE_SPEC.md
- docs/BASEBALL_NEWS_PIPELINE_SPEC.md
- lanes/sports_news/README.md

作業境界:
- NLMYTGen の本流 next_action を Baseball に置き換えない。
- G-27 / Real Estate DX / 茶番劇の current task を Baseball の進捗で上書きしない。
- 変更は原則として lanes/sports_news/、BaseballInfoGraphics/、docs/BASEBALL_NEWS_PIPELINE_SPEC.md、関連する Baseball docs に閉じる。
- runtime-state.md を更新する場合は、Baseball を「sidequest / explicit lane」として記録し、主軸変更として扱わない。
- React / HTML を直接 YMM4 に入れない。Phase 1 は 1280x720 PNG を ImageItem、Phase 2 は deterministic animated clip を VideoItem とする。

今回作る artifact:
- まず screen plan を作る。
- screen plan には segment id、script range、viewer question、card sequence、information budget、primary screen、duration、YMM4 placement、review signal を含める。
- 必要な場合だけ BaseballInfoGraphics 配下に review-only prototype を作る。

検証:
- docs / YAML / JSON 中心なら pytest は実行しない。
- Markdown 差分は git diff --check で確認する。
- screen plan sample を作る場合は YAML/JSON parse を確認する。

closeout:
- Baseball sidequest で何が進んだかを本流と分けて説明する。
- 本流に戻すもの、Baseball lane に閉じるもの、まだ YMM4 acceptance へ進めないものを分ける。
- 次に assistant が作る artifact と、user が見る primary review surface を明示する。
```

## When To Use

- Baseball Info / sports_news の設計、screen plan、データ schema、InfoGraphics、PNG/animation export、YMM4 配置方式を進めるとき。
- 本流のゆっくり解説制作タスクと混ぜず、別スレッド・別ブランチ・別作業単位へ切り出したいとき。

## Do Not Use

- G-27 Real Estate DX の scene decision packet を作るとき。
- 汎用ゆっくり解説の CSV / IR / YMM4 / 茶番劇 / サムネイル導線を進めるとき。
- Baseball を現行 `next_action` に昇格させる意図がないのに、runtime-state の主軸を書き換えるとき。
