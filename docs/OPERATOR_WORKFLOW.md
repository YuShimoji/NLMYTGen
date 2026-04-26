# Operator Workflow

人間オペレーターの実ワークフロー・痛点・品質目標を保持する正本。

**並行して進める自分用の作業（Phase1・GUI LLM 同期・YMM4・サムネ・Git）の完全手順**は [OPERATOR_PARALLEL_WORK_RUNBOOK.md](OPERATOR_PARALLEL_WORK_RUNBOOK.md) に集約した。

## 全体フロー
- S-0（YMM4テンプレート構築）: 初回のみ
- S-1（ソース投入・Audio Overview生成）: NotebookLM にソース投入、Audio Overview 生成
- S-2（台本テキスト取得）: 元台本テキスト取得、または音声書き起こし fallback
- S-3（CSV変換）: NLMYTGen で CSV 変換、必要に応じて分割・統計確認
- S-4（台本読込）: YMM4 で台本読込、キャラクター割当確認
- S-5（読み上げ確認・字幕修正）: 読み上げ確認、字幕はみ出し修正、辞書登録
- S-6（背景・演出設定）: 背景・演出・BGM・表情差し替え
  - S-6a（手動IR取得）: Custom GPT に台本テキストを貼り付けて IR JSON を取得
  - S-6b（GUI演出適用）: GUI の演出適用タブで Production ymmp + IR JSON + 必要なファイルを指定して Apply Production を実行（face_map 抽出 + row-range 自動付与 + patch を一括実行。row-range mismatch / prompt drift / active gap / fatal face issue は書き出し前に停止）
  - S-6c（手動微調整）: YMM4 で output.ymmp を開き、表情・背景・BGM を確認・微調整
- S-7（通し確認・レンダリング）: 通し確認とレンダリング
- S-8（サムネイル制作）: サムネイルをテンプレートベースで手動調整
- S-9（YouTube投稿）: YouTube Studio で投稿作業

## 工程ごとの痛点
- 最も重いのは S-5（読み上げ確認・字幕修正）と S-6（背景・演出設定）。
- S-5（読み上げ確認）の字幕はみ出しは YMM4 で都度直せるが、S-3（CSV変換）の分割品質が低いと手戻りが増える。
- S-6（背景・演出設定）は人間の判断が中心で、単純なパターンマッチでは省力化になりにくい。
- E-02 単体の metadata template は、YouTube Studio への手入力が残るため bottleneck 解消として弱い。

## 品質目標
- S-3（CSV変換）の出力を YMM4 に読み込んだ時点で、話者名の不一致や極端な長文が少なく、修正が「例外処理」に留まる。
- 字幕は通常ケースで 2 行以内に収まり、はみ出し候補は事前警告で把握できる。
- 人間が行うのは、読み・演出・サムネイルなど創造判断を要する工程に寄る。

## 現在の workflow proof 条件
- B-11 を approved frontier とし、S-5 の pain を「YMM4 取込前にどこまで減らせるか」を先に実証する。
- proof は Python 側の改善余地と YMM4 手動修正の境界を見極めることが目的であり、YMM4 の自動操作を作ることではない。
- proof は少なくとも 1 件の transcript で、GUI の CSV 変換（Max lines 2・Chars/Line 40・balance-lines ON）の結果と、YMM4 取込後の残修正量を同じ記録に残す。
- 記録フォーマットの正本は [workflow-proof-template.md](workflow-proof-template.md)。`docs/verification/` にコピーして案件ごとに記入する。リポジトリ内の記入例: [verification/B11-workflow-proof-sample-example-dialogue.md](verification/B11-workflow-proof-sample-example-dialogue.md)。
- 手動確認のタイミング一覧: [B11-manual-checkpoints.md](B11-manual-checkpoints.md)。
- 観測ログ（移管）: [project-context.md#b-11-workflow-proof-chronicle-archive](project-context.md#b-11-workflow-proof-chronicle-archive)。現行条件は本節の bullets。
- proof が成功とみなせる条件は、S-5 の修正が「例外処理」に留まり、全面的な手直しや GUI 欲求だけで次 frontier を決めないこと。
- 残修正は最低でも「辞書登録」「手動改行」「再分割したい長文」「タイミングのみ」の 4 区分で分類する。

## Actor Boundaries (三層責務構造対応)
- `user`: NotebookLM 操作、Custom GPT で Writer IR 生成 (第1層)、Template Registry のラベル付け・素材準備 (第2層)、YMM4 内の判断・微調整、サムネイル、投稿判断、YMM4 native template の登録
- `assistant`: CSV 変換、IR 語彙定義 (PRODUCTION_IR_SPEC)、YMM4 Adapter 実装 (第3層: patch-ymmp)、Template Registry の JSON 構造、台帳整備、仕様化
- `tool`: 分割、統計、入力検証、speaker-map 生成、警告表示、extract-template、patch-ymmp (YMM4 Adapter)
- `shared`: どの pain を次に削るかの優先判断、frontier の approval、三層の責務境界の更新

## 手動工程 / 自動化禁止工程
- YMM4 内の演出指定、背景配置、表情切り替え、BGM/SE の最終判断 (Adapter で face/bg は半自動化するが、最終判断は人間)
- サムネイルの訴求判断と最終デザイン
- 実機での読み上げ確認、通しプレビュー、公開判断
- GUI やテンプレートを作ること自体を目的化して、手動工程の本質的判断を隠さない
- YMM4 native template の登録はユーザーが行う。Python で native template を再発明しない
- 表情ラベル (`serious` / `thinking` 等) は、パーツ番号から機械的に決めず、YMM4 上で見え方を確認したテンプレートをもとに人間が命名する
- `extract-template` の出力キー (`face_01_...`, `bg_01_...`) は棚卸し用の仮ラベル。production 用 registry は visual review 後の意味ラベルへ手動で整える

## palette 更新が必要になるケース
- `FACE_UNKNOWN_LABEL` / `FACE_ACTIVE_GAP` が出た → palette にそのラベルの表情を追加し再抽出
- `FACE_PROMPT_PALETTE_GAP` が出た → Custom GPT の face 許可リストと palette の差分を解消する
- `FACE_PROMPT_PALETTE_EXTRA` が出た → prompt が palette の実在ラベルより狭くなっていないか確認する
- 連続 run が多い → palette のラベル間のパーツ差が小さすぎる可能性。パーツ組み合わせを見直す

## face サブクエストの completion criteria
- `validate-ir` / `apply-production` が face 関連の mechanical failure を failure class 付きで止められること
- current IR に必要な face / idle_face が palette で解決できない場合、`FACE_ACTIVE_GAP` として書き出し前に停止すること
- prompt の face 契約と palette の drift が `FACE_PROMPT_PALETTE_GAP` / `FACE_PROMPT_PALETTE_EXTRA` / `FACE_LATENT_GAP` で可視化されること
- row-range の不整合が `ROW_RANGE_MISSING` / `ROW_RANGE_INVALID` / `ROW_RANGE_OVERLAP`、または annotate の unmatched / uncovered として止まること
- patch-time にしか分からない ymmp 側の欠陥 (`VOICE_NO_TACHIE_FACE` / `FACE_MAP_MISS` / `IDLE_FACE_MAP_MISS`) でも partial output を書かないこと
- 上記が clean なら、face は「完成済みサブシステム」として扱い、次の主 frontier を止めないこと

## face で人間が判断する範囲
- palette の各ラベル名 (`serious` / `thinking` 等) が YMM4 上の見え方として妥当か
- 新しい表情ラベルを増やす価値があるか、既存ラベルの再命名で足りるか
- 実制作物でその表情が内容に対して十分かどうかという creative quality
- 初回 E2E と最終制作物での「見え方の良し悪し」。同じ mechanical failure を疑うための repeated visual proof は不要

## face を再度触る条件
- `FACE_UNKNOWN_LABEL`
- `PROMPT_FACE_DRIFT`
- `FACE_ACTIVE_GAP`
- `ROW_RANGE_MISSING` / `ROW_RANGE_INVALID` / `ROW_RANGE_OVERLAP`
- row-range annotate の unmatched / uncovered
- `FACE_MAP_MISS` / `IDLE_FACE_MAP_MISS`
- `VOICE_NO_TACHIE_FACE`
- 最終制作物で「今の label inventory 自体が足りない」と判断された場合

## motion: G-17 と Phase2（CLI の使い分け）

- **`--timeline-profile` を付ける場合（G-17）**: `motion` / `transition` / `bg_anim` のうち、契約に含まれるものを **`--motion-map`**（各ラベル → `video_effect` 辞書）、`--transition-map`、`--bg-anim-map` で書き込む。サンプル: [samples/motion_map_g17.example.json](samples/motion_map_g17.example.json)。このとき **Phase2 の `TachieItem` 区間分割は実行されない**。
- **プロファイルを付けない場合の motion（Phase2）**: **`--tachie-motion-map`** でラベル → **VideoEffects オブジェクトの配列**を渡し、発話アンカーに合わせて `TachieItem` を分割する。サンプル: [samples/tachie_motion_map.example.json](samples/tachie_motion_map.example.json)。
- **`validate-ir`**: 台帳ラベル検証は **`--motion-map` と `--tachie-motion-map` のキーを併用**できる（和集合で `MOTION_MAP_UNKNOWN_LABEL` を抑止）。
- **重要な境界**: `motion` の既定対象は `speaker_tachie`（ゆっくり立ち絵）。`motion_target` / `group_motion` は補助経路であり、G-24 茶番劇演者の主経路ではない。茶番劇演者は [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md) の **GroupItem テンプレ運用**を優先する。route 選択で迷ったら [TIMELINE_EFFECT_CAPABILITY_ATLAS.md](TIMELINE_EFFECT_CAPABILITY_ATLAS.md) を先に見る。

## 茶番劇テンプレ運用

### 開発段階

- 1 つの **canonical skit_group template** を YMM4 上で作る
- canonical から `surprise_jump` / `panic_shake` 等の **小演出テンプレート**を派生させる
- assistant 側は template registry 台帳・命名・fallback・manual check を整備する
- 成果物は **YMM4 native template 資産**であり、JSON の direct write route を増やすことではない

### skit_group 配下アイテム構成 (構造的制約)

- **配下は `ImageItem` のみ**: body `ImageItem` (1 枚画像) + 顔 `ImageItem` (1 枚画像) + (任意で装飾 `ImageItem`)
- **`TachieItem` は配下に含めない**。`TachieItem` (連番アニメ + TachieFaceParameter) は解説役のゆっくり立ち絵専用
- 新キャラの立ち絵セットアップ (AnimationTachie プラグイン設定 / パーツ分解 / 表情マッピング) は**行わない**。運用コスト過大で非採用決定済
- 顔の感情差し替えは **`ImageItem.Source` パス置換**で行う (例: `reimu_easy.png` → `reimu_surprised.png`)。`TachieFaceParameter` は使わない
- 既存の解説役 (ゆっくり霊夢 / ゆっくり魔理沙 の `TachieItem`) は GroupItem の外に独立配置し、skit_group に流用しない

### 実制作

- IR 要求はまず **template 解決**する
- exact template がなければ fallback を返す
- 汎用テンプレで吸収できない場合は **未自動化理由 + 手動確認ポイント**を注記する
- `motion` の direct write 拡張を先に増やすのではなく、既存 template 資産の再利用を優先する

### 役割分担

- `speaker_tachie`: 既存 `face` / `idle_face` / `slot` / `motion`
- `skit_group`: 外部素材演者の GroupItem テンプレ
- `overlay_render`: YMM4 書き出し PNG を使う補助経路

### これにより止めること

- 配達員の body/head を `motion` の主対象として設計すること
- GroupItem / ImageItem / TachieItem を 1 つの feature として混ぜること
- route contract やテストが通っただけで production 演出まで成立したと扱うこと

## timeline edit サブクエストの境界
- route 選択の正本: [TIMELINE_EFFECT_CAPABILITY_ATLAS.md](TIMELINE_EFFECT_CAPABILITY_ATLAS.md)（何が `direct_proven` / `template_catalog_only` / `probe_only` / `unsupported` かを先に判断する）
- IR 語彙と `patch-ymmp` 実装の対応（何が自動で書き込まれるか）の正本: [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md)
- assistant / tool が先に閉じる対象は G-11 slot patch、G-12 motion/transition/bg_anim の write route 測定、G-13 overlay/se の timing anchor 付き挿入設計、G-14 bg_anim（ImageItem X/Y/Zoom プリセット）patch
- `slot` は mechanical 対象。unknown slot label / slot registry gap / character default slot drift は YMM4 手動確認より前に止める
- `motion` / `transition` / `bg_anim` は creative choice ではなく、まず「どの write route が安全か」を測る subquest として扱う。native template 参照か key 書き換えかを実測で確定するまでは manual frontier に押し戻さない。Atlas ではこの状態差を `direct_proven` / `probe_only` / `unsupported` で明示する
- G-12 の測定は `measure-timeline-routes` を起点に行い、まず ymmp の `VideoEffects` / transition key / template candidate route を readback で把握する。期待 route が決まったら `--expect` で contract miss を先に止める
- 運用: `samples/` 等に新しい ymmp サンプルが追加され、timeline 系の期待 route を広げる場合は、該当カテゴリの `measure-timeline-routes` 記録（contract）を同じタイミングで更新する（sample dependency の解消単位）
- `TIMELINE_ROUTE_MISS` は「その演出がダメ」という意味ではなく、「その ymmp には期待 route が存在しない」という mechanical failure として扱う
- repo-local corpus に route 自体が 0 件なら、それは operator の visual judgement 待ちではなく sample dependency として扱う。現状では `template` と non-fade / template-backed `transition` family のみがこれに該当する
- `overlay` / `se` は意味ラベル → registry → timing anchor の deterministic 経路ができるまでは manual judgement に残すが、設計・dry-run・readback は assistant 側で先に閉じる
- `overlay` は assistant-owned mechanical scope として閉じている。`--overlay-map` があれば deterministic な `ImageItem` 挿入まで自動で行い、unknown label / map miss / timing anchor 不在 / spec 不正は visual review 前に failure class で止める
- `se` は意味ラベル → registry → timing anchor を assistant 側で閉じ、**G-18** から `--se-map` と IR の `se` に基づき `AudioItem` を挿入する（既存タイムラインの `AudioItem` をテンプレにできなければコード内最小骨格を使用）
- 人間が残す判断は「どのテンプレートが見た目として良いか」「どのタイミングが気持ちいいか」「音量・密度・テンポが最終制作物として十分か」という creative quality のみ

## timeline edit サブクエストの completion criteria
- G-11: completed。`slot` が registry で解決でき、`validate-ir` が `SLOT_UNKNOWN_LABEL` / `SLOT_REGISTRY_GAP` / `SLOT_CHARACTER_DRIFT` / `SLOT_DEFAULT_DRIFT` を事前検出し、`patch-ymmp` / `apply-production` が TachieItem X/Y/Zoom と `off` hide を deterministic に反映できる
- G-12: `motion` / `bg_anim` の write route が repo-local corpus ベースで固定され、fade-family `transition` route も mechanical に確認済みで、残る route 不在カテゴリは non-fade / template-backed family の sample dependency として明示され、dry-run/readback で mechanical failure を再現できる
- G-13: completed。`overlay` は label 解決、timing anchor、挿入先構造が固定され、creative density judgement と mechanical insertion failure が分離された。`se` は label/timing を解決し、G-18 で `AudioItem` 挿入まで mechanical（旧 `SE_WRITE_ROUTE_UNSUPPORTED` は廃止）
- 上記を満たした packet は、それぞれ独立 failure class 単位で扱い、broad な timeline retry loop に戻さない

## 検証の境界
- パイプラインの機械的動作はユニットテスト + GUI の Dry Run で検証する。YMM4 visual proof を繰り返し要求しない
- YMM4 を開くのは **(1) テンプレ用素材の登録時** と **(2) 全素材を集め終わって配置・書き出すとき** の 2 つだけ。増分変更のたびに中間確認で開かない
- テストや検証が開発のブロッカーにならないようにする。品質ゲートは開発速度を優先して柔軟に運用する

## L2（Python変換工程）字幕変更と YMM4 実機の切り分け
- **CSV・字幕リフロー（B-11〜B-17 系）のみの変更**は L2（Python変換工程）。コードを変更したときだけユニットテストを実行する。**増分のたびに YMM4 通しを要求しない**（上記「検証の境界」と同じ精神）。
- **patch / IR 契約・timeline adapter**の変更は L3（YMM4内部工程）。GUI の Dry Run を優先し、YMM4 通しは**契約や経路が変わったマイルストーン時**に限定する。
- **制作工程は全て GUI で完結させる。** GUI に不足している機能がある場合は、GUI に実装すべき課題として扱う（[GUI_MINIMUM_PATH.md](GUI_MINIMUM_PATH.md) 基本方針）。

## 運用ルール
- 一度説明された workflow pain はここへ固定する
- 「本制作へ進む前に workflow proof が必要」な案件では、その proof 条件もここへ残す
