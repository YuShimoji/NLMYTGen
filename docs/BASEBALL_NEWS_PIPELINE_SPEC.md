# Baseball News Pipeline Spec

Status: draft lane boundary (2026-05-07)

この文書は、NLMYTGen 内で新しく扱う **野球速報系ゆっくり解説動画** レーンの正本仕様である。
既存の「ゆっくり解説」制作パイプラインを再利用するが、題材・映像素材・データ契約はスポーツニュース向けに分離する。

## 目的

- 野球速報・試合解説・選手ニュースを、ゆっくり解説形式の動画として制作する。
- `BaseballInfoGraphics/` の C 詳細デザインを、野球ニュース用の正本インフォグラフィックとして育てる。
- 静止 PNG だけでなく、ブラウザアプリ側のアニメーションを活かした映像素材化を前提にする。
- 既存の background skit / skit_group / thumbnail / Episode Pack の概念と混線しないよう、用語と責務を固定する。

## 認識の分離

| 概念 | このレーンでの意味 | 混同してはいけないもの |
| --- | --- | --- |
| 野球速報レーン | スポーツニュース特化の動画制作パイプライン | 既存の不動産 DX / 汎用解説動画の続き |
| ゆっくり解説 | 語り口・音声・台本形式 | 題材が汎用解説であるという意味 |
| C 詳細デザイン | 野球インフォグラフィックの正本デザイン | A/B/minimal/standard などの廃止済み案 |
| インフォグラフィック | 試合状況・投球・選手・スコアを視覚化するニュース素材 | background skit の演者・茶番劇テンプレート |
| デザインソース | HTML/React/Babel の編集・プレビュー用アプリ | YMM4 に直接入れる最終素材 |
| 静止 PNG | 任意時点の 1280x720 フレーム | アニメーション全体の代替 |
| アニメーション素材 | ブラウザアプリの状態遷移・投球更新を録画/連番化した映像素材 | Python で画像合成した疑似プレビュー |
| 野球データ JSON | 試合・選手・投球・スコアなどの機械可読データ | ナレーション台本そのもの |
| ニュース台本 | 視聴者へ伝える構成・論旨・コメント | 投球ログや成績表の生データ |

## 現在の正本デザイン

- Source folder: `BaseballInfoGraphics/`
- Entry point: `BaseballInfoGraphics/Baseball Infographic.html`
- Canonical variant: `BaseballInfoGraphics/variants/detailed.jsx`
- Deprecated variants: A minimal / B standard は削除済み。今後の検討で復活させず、C 詳細を改善する。
- Current purpose: 1280x720 の野球ニュース用分析カード。投手・打者・投球・スコア・履歴を同時に見せる。

## 制作フロー

```text
news topic / game facts
  -> sports news brief
  -> ゆっくり解説 script / segment plan
  -> baseball visual data JSON
  -> BaseballInfoGraphics preview
  -> PNG frame or animated capture
  -> YMM4 import / placement
  -> final sports-news video
```

## 入力 artifact

| Artifact | State | 役割 |
| --- | --- | --- |
| sports news brief | future | 速報の論点、試合状況、なぜ今見るべきかをまとめる |
| narration script | existing pipeline reuse | ゆっくり解説として喋らせる完成台本 |
| baseball visual data JSON | future | チーム、選手、スコア、投球、成績を UI に渡す |
| render config | future | 色、表示密度、静止/動画、開始投球、尺、fps などを指定する |
| exported visual asset | future | PNG / animated video / image sequence のいずれか |
| YMM4 placement note | future | どのタイムライン位置に何秒置くかを決める |

## sports_news lane artifact bundle

`lanes/sports_news/` は、この仕様をスポーツニュース全般へ拡張するための MVP artifact bundle として扱う。初期内容は schema / sample / card template / closed topics / visual language であり、renderer 実装・network 取得・外部素材取得・AI 画像生成は含めない。

- `lanes/sports_news/README.md` — text/data/source driven lane の境界
- `lanes/sports_news/schemas/` — source / fact / reaction / rights / episode contracts
- `lanes/sports_news/examples/baseball_pitch_event_sample.yaml` — 架空データによる野球 pitch event sample
- `lanes/sports_news/templates/cards/` — self-made broadcast card UI のテンプレート仕様

## 出力 artifact

| Output | 用途 | 最低条件 |
| --- | --- | --- |
| static PNG | 一枚絵の解説カード、サムネ以外の動画内 overlay | 1280x720、クロップなし、主要文字が読める |
| animated clip | 投球更新・カウント変化・速報感のある動画内素材 | 尺/fps/開始終了状態が deterministic |
| render manifest | どの入力データから何を出したかの記録 | source path、data hash、variant、export settings を含む |
| YMM4 import note | 手動または半自動配置の接続情報 | 配置先、尺、NG時の返却内容が明確 |

## Animation-first policy

このレーンでは PNG 書き出しだけを最終目標にしない。現在のアプリは投球状態を一定間隔で更新するため、速報・試合解説ではアニメーションを制作価値として扱う。

- Phase 1: C 詳細の静止 PNG export を安定させる。
- Phase 2: 投球インデックス、再生状態、開始/終了フレームを外部から固定できるようにする。
- Phase 3: ブラウザ描画を動画素材または連番フレームとして export する。
- Phase 4: YMM4 へ動画素材として読み込み、ナレーション区間に配置する。

Python 側が画像を生成・合成するのではなく、ブラウザのデザインソースを正として render/capture する。Python/CLI は data validation、manifest、YMM4 接続補助を担当する。

## 現在の既知リスク

- C 詳細は見栄えの方向性は良いが、情報密度・安全余白・ニュース動画内での可読性は未検証。
- 現在のデータは mock であり、実試合データ schema はまだ未定義。
- HTML は CDN/Babel 依存のプロトタイプで、production renderer ではない。
- ブラウザ表示と artboard export は別物なので、通常スクリーンショットを production proof にしない。
- アニメーション export 方式は未実装。PNG 書き出しだけでレーン完了扱いにしない。
- YMM4 での animated clip 読み込み、尺合わせ、音声との同期はまだ proof なし。

## 初期タスク

| ID | Task | 完了条件 |
| --- | --- | --- |
| BN-00 | レーン境界と用語を固定する | 本 spec と `BaseballInfoGraphics/README.md` が存在する |
| BN-01 | C 詳細デザイン改善 audit | 可読性、余白、情報優先度、スポーツニュースらしさの改善リストを作る |
| BN-02 | baseball visual data schema | mock data から実入力 JSON contract を分離する |
| BN-03 | static PNG export contract | 1280x720 PNG と manifest を deterministic に出せる |
| BN-04 | animation export contract | duration / fps / state sequence を固定して clip か連番を出せる |
| BN-05 | YMM4 import/placement contract | PNG/clip の配置先、尺、manual proof の返却形式を決める |
| BN-06 | sports news script segmentation | ニュース導入、事実、分析、見どころ、締めを台本構造へ落とす |
| BN-07 | operator workflow | GUI/CLI で何を押せば素材ができるかを短い導線にする |

## Acceptance gates

- Design gate: C 詳細が 1280x720 の最終表示で読める。クロップ、過密、意味の重複がない。
- Data gate: 未知チーム・未知選手・欠損投球・矛盾スコアを fail-fast できる。
- Animation gate: 同じ入力から同じ尺・同じ状態遷移の animated asset が再生成できる。
- YMM4 gate: PNG または animated asset が YMM4 に入り、ナレーション区間に合わせて確認できる。
- Editorial gate: ニュース台本とデータ表示が矛盾せず、速報性と解説性が分離されている。

## 今後の扱い

このレーンは現時点では draft frontier であり、既存の background skit / Real Estate DX レーンを置き換えない。
ただし、このスレッド内では BN 系タスクを主対象として扱い、C 詳細デザインの改善・データ契約・PNG/animation export・YMM4 接続へ進める。
