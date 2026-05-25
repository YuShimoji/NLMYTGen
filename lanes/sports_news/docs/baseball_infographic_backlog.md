# baseball infographic backlog

Status: BN-01 initial implementation slice

この backlog は `BaseballInfoGraphics/` の C 詳細デザインを、野球速報系ゆっくり解説で使う original broadcast/data infographic へ育てるための短期タスク台帳である。

## BN-01A sample compliance cleanup

- State: implemented in initial slice.
- Goal: repo-local mock から実在チーム風・実在選手風の固有名を外す。
- Done when:
  - `BaseballInfoGraphics/data.js` が架空 team/player のみを使う。
  - mock 固有名が、実在チーム・実在選手・既存リーグの証跡に見えない。
  - 素材由来や publish gate の判断は、C 詳細の layout / animation 改善タスクへ混入しない。

## BN-01B scoreboard hierarchy

- State: implemented in initial slice.
- Goal: 最初に `EAG 3 - 4 FAL` 型のスコアが読める。
- Done when:
  - score が inning/status より大きい。
  - inning/status は `7回表 · 1 OUT · B2-S2` のようにラベル付きで補助情報として読める。

## BN-01C one-screen-one-claim card structure

- State: implemented in initial slice.
- Goal: 1画面に1つの解釈見出しを置く。
- Done when:
  - `visual.claim` または current pitch の `claim` が C 詳細の主見出しとして表示される。
  - pitch event の主張が strike zone / velocity / count と矛盾しない。

## BN-01D side-panel readability

- State: implemented in initial slice.
- Goal: 左右パネルを major values 最大5個までに絞る。
- Done when:
  - pitcher panel は throws / ERA / PC / K / IP を優先する。
  - batter panel は bats / AVG / OPS / TODAY / vsP を優先する。
  - detailed mode の補足は主表示を押し流さない。

## BN-01E deterministic animation control

- State: implemented in initial slice.
- Goal: PNG capture / animation capture の開始状態を URL で固定する。
- Done when:
  - `pitch=0..n-1` で初期 pitch が固定できる。
  - `autoplay=0|1` で静止 capture と自動更新を切り替えられる。
  - `stepMs=250..10000` で pitch 更新間隔を固定できる。
  - `window.__BASEBALL_INFOGRAPHICS_STATE__` で現在状態を readback できる。

## BN-01F ambientBackdrop preview sample

- State: implemented in follow-up slice.
- Goal: 背景 slot を禁止対象ではなく、由来記録付きのデザイン機能として実表示できる。
- Done when:
  - `BaseballInfoGraphics/data.js` が `visual.ambientBackdrop.imageUrl` を持つ。
  - preview sample は repo-generated SVG と同階層の `LICENSE.csv` で provenance を示す。
  - 未設定時の暗色グリッド fallback と、設定時の雰囲気背景表示の両方が仕様上説明されている。

## BN-01G screen plan review unit

- State: draft review unit added.
- Goal: renderer / PNG export / YMM4 proof の前に、短尺野球ニュース全体のカード順・情報量・配置方式をレビューできる形にする。
- Done when:
  - `lanes/sports_news/screen_plans/baseball_pitch_event_screen_plan_v1.yaml` が、segment ごとに viewer question / card sequence / information budget / primary screen / YMM4 placement / reviewer signal を持つ。
  - `docs/runtime-state.md` の primary `next_action` を Baseball に置き換えない。
  - 出力は screen plan review unit であり、renderer implementation / PNG export proof / YMM4 creative acceptance ではない。

## BN-02 baseball visual data contract

- State: implemented in BN-02 slice.
- Goal: `lanes/sports_news` の episode dict から `BaseballInfoGraphics` が読める visual data JSON を作る。
- Done when:
  - `lanes/sports_news/schemas/baseball_visual_data.schema.json` が `baseball_visual_data.v1` の必須 top-level を固定する。
  - `src/pipeline/baseball_visual_data.py` が dict input から C 詳細用 dict output を生成・検証する。
  - `lanes/sports_news/examples/baseball_pitch_event_visual_data_sample.json` が sample-only の変換結果として置かれる。
  - `BaseballInfoGraphics/data.js` が `window.BASEBALL_VISUAL_DATA` を任意 override として受け、未設定時は fallback sample を表示する。
  - PNG export / animation export / YMM4 placement proof は BN-03 以降に残す。

## Next candidates

- BN-03: 1280x720 PNG export と render manifest を deterministic にする。
- BN-04: animation capture 用の frame sequence / clip export contract を作る。
- BN-05: YMM4 placement note の最小 contract を作る。
