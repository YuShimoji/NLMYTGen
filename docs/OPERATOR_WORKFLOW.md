# Operator Workflow

人間オペレーターの実ワークフロー・痛点・品質目標を保持する正本。

## 全体フロー
- S-0: YMM4 テンプレート構築 (初回のみ)
- S-1: NotebookLM にソース投入、Audio Overview 生成
- S-2: 元台本テキスト取得、または音声書き起こし fallback
- S-3: NLMYTGen で CSV 変換、必要に応じて分割・統計確認
- S-4: YMM4 で台本読込、キャラクター割当確認
- S-5: 読み上げ確認、字幕はみ出し修正、辞書登録
- S-6: 背景・演出・BGM・表情差し替え
  - S-6a (手動): Custom GPT に台本テキストを貼り付けて IR JSON を取得
  - S-6b (CLI): `apply-production production.ymmp ir.json --palette palette.ymmp --csv reflow.csv --bg-map bg_map.json -o output.ymmp` (face_map 抽出 + row-range 自動付与 + patch を 1 コマンドで実行。row-range mismatch / prompt drift / active gap / fatal face issue は書き出し前に停止)
  - S-6c (手動): YMM4 で output.ymmp を開き、表情・背景・BGM を確認・微調整
- S-7: 通し確認とレンダリング
- S-8: サムネイルをテンプレートベースで手動調整
- S-9: YouTube Studio で投稿作業

## 工程ごとの痛点
- 最も重いのは S-5 (読み上げ確認・字幕修正) と S-6 (背景・演出設定)。
- S-5b の字幕はみ出しは、YMM4 で都度直せるが、S-3 の分割品質が低いと手戻りが増える。
- S-6 は人間の判断が中心で、単純なパターンマッチでは省力化になりにくい。
- E-02 単体の metadata template は、YouTube Studio への手入力が残るため bottleneck 解消として弱い。

## 品質目標
- S-3 の出力を YMM4 に読み込んだ時点で、話者名の不一致や極端な長文が少なく、修正が「例外処理」に留まる。
- 字幕は通常ケースで 2 行以内に収まり、はみ出し候補は事前警告で把握できる。
- 人間が行うのは、読み・演出・サムネイルなど創造判断を要する工程に寄る。

## 現在の workflow proof 条件
- B-11 を approved frontier とし、S-5 の pain を「YMM4 取込前にどこまで減らせるか」を先に実証する。
- proof は Python 側の改善余地と YMM4 手動修正の境界を見極めることが目的であり、YMM4 の自動操作を作ることではない。
- proof は少なくとも 1 件の transcript で、`build-csv --max-lines 2 --chars-per-line 40 --stats` の事前警告と、YMM4 取込後の残修正量を同じ記録に残す。
- proof が成功とみなせる条件は、S-5 の修正が「例外処理」に留まり、全面的な手直しや GUI 欲求だけで次 frontier を決めないこと。
- 残修正は最低でも「辞書登録」「手動改行」「再分割したい長文」「タイミングのみ」の 4 区分で分類する。
- 2026-03-31 の初回観測では、辞書登録 0 / タイミングのみ 0 に対して、手動改行・再分割したい長文が約 30 箇所と支配的だった。次の L2 改善は読みではなく字幕改行のバランス改善を優先する。
- 2026-03-31 の B-12 再観測では、手動改行 10 / 再分割したい長文 15 / 不自然な単語分割 5。`。` での改行は効いたが、句読点の少ない長文と 1 文字最終行が残り、次の主 pain は clause-aware split と widow/orphan guard だと判明した。
- 2026-03-31 の B-13 実装では、`--balance-lines` の内部改善として clause-aware split fallback と widow/orphan guard を追加した。sample dry-run では 57 発話 → 62 行に再編され、次に必要なのは YMM4 取込後の fresh visual evidence である。
- 2026-03-31 の B-13 再観測では、手動改行 5 / 再分割したい長文 10 / 不自然な単語分割 5。減りはしたが「まだ多い」という operator judgement で、特に長い一文が 1 字幕に残るケースは未解決だった。次の主 pain は aggressive clause chunking に移った。
- 2026-03-31 の B-14 実装では、複数文発話の中にある単一長文も sentence ごとに再展開し、通常候補が尽きた残り長文には aggressive clause chunking fallback を追加した。sample dry-run では 57 発話 → 95 行、overflow candidates は 3 件まで減少したため、次に必要なのは YMM4 上で「再分割負荷が減ったか」と「細かく切れすぎていないか」を同時に見る post-import visual evidence である。
- 2026-03-31 の追加観測では、`、` 起点の分割強化により長すぎる行はかなり減り、全字幕が 3 行以内には収まる水準まで改善した。残課題は bulk overflow ではなく、`ー`、カギ括弧 `「」`、数値や記号を含む `202/4` のような折り返しなど、個別ケースの良し悪しを集めて傾向化する段階に移った。ここから先は rule の複雑化が急速に進むため、heuristic を足し続ける前に「改行すべき/すべきでない例」の corpus を集める value path が強い。
- 2026-03-31 の B-15 初期コーパス収集では、`AI監視が追い詰める生身の労働_balance_lines_ymm4.csv` から 14 件 (bad-split 10, good 4) を抽出した。傾向パターン: P1=閉じ括弧直後+助詞で不自然分割 (5件)、P2=左側が極端に短い (3件)。P1/P2 はいずれもルール候補 (3件以上)。対策案と初期コーパスの妥当性について手動検証待ち。
- 2026-04-01 の B-15 第1回手動検証: ユーザーが YMM4 取込後に確認。報告: 漢字途中切断 (`事情は完/全に`, `身体的限/界`)、カタカナ途中 (`評価スコ/アが`)、単語途中 (`働/き続ける`, `路上/へと`)、次頁区切りの違和感 (`ロックオン/して`)。原因は小区切り(文字種境界)の誤発動と候補不足時の強制切断。修正: 大区切り限定方式に変更、漢字連続を禁止位置に追加。
- 2026-04-01 の B-15 第2回手動検証: 第1回報告の7パターン全て解消。4行またがりなし。若干の違和感は残るが「明らかなバランス偏りはなくなっている」。追加フィードバック: 漢字→ひらがな境界の小区切りは外すべき (`単/なる`, `見間違/った` 類)。文字種境界より行長精度を優先する方針を確認。小区切り候補から文字種境界を除去。
- 2026-04-01 の B-15 第3回手動検証: ページ間分割はだいぶ改善。行内折り返し (YMM4自動折り返し) の違和感は残存。「1行/1ページの最大文字数から逆算する外殻」が必要で、B-16 として分離。B-15 done。
- 2026-04-01 の C-07 v1 proof: セクション分割 OK、作業時間削減 OK、背景候補 NG。ストック素材検索は方向が違う。必要なのは茶番劇アニメ+図解の演出指示。
- 2026-04-01 の C-07 v2 proof: 4演出パターン (茶番劇/情報埋め込み/雰囲気演出/黒板型) + 発話単位指示 + 表示情報抽出 + 要調査明示。3基準全て OK。C-07 done。
- 2026-04-03 の production-slice patch-ymmp proof では、実IR先頭11発話を既存 ymmp に適用して face 13 / bg 2 変更を確認した。一方で 11 VoiceItem 中 4 件は `TachieFaceParameter` を持たず、face 差し替え対象外だった。full E2E 前に、台本読込後 ymmp の対象キャラ発話が表情パラメータを保持していることを operator 側で確認する必要がある。
- 2026-04-05 の face completion hardening で、この種の partial apply は `VOICE_NO_TACHIE_FACE` として mechanical failure に昇格した。以後は broad な visual retry loop ではなく、failure class に応じて対処する。

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

## face サブクエストの completion criteria (2026-04-05 固定)
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

## timeline edit サブクエストの境界 (2026-04-06 固定)
- assistant / tool が先に閉じる対象は G-11 slot patch、G-12 motion/transition/bg_anim の write route 測定、G-13 overlay/se の timing anchor 付き挿入設計
- `slot` は mechanical 対象。unknown slot label / slot registry gap / character default slot drift は YMM4 手動確認より前に止める
- `motion` / `transition` / `bg_anim` は creative choice ではなく、まず「どの write route が安全か」を測る subquest として扱う。native template 参照か key 書き換えかを実測で確定するまでは manual frontier に押し戻さない
- G-12 の測定は `measure-timeline-routes` を起点に行い、まず ymmp の `VideoEffects` / transition key / template candidate route を readback で把握する。期待 route が決まったら `--expect` で contract miss を先に止める
- `TIMELINE_ROUTE_MISS` は「その演出がダメ」という意味ではなく、「その ymmp には期待 route が存在しない」という mechanical failure として扱う
- repo-local corpus に route 自体が 0 件なら、それは operator の visual judgement 待ちではなく sample dependency として扱う。2026-04-06 時点では `template` と non-fade / template-backed `transition` family のみがこれに該当する
- `overlay` / `se` は意味ラベル → registry → timing anchor の deterministic 経路ができるまでは manual judgement に残すが、設計・dry-run・readback は assistant 側で先に閉じる
- 2026-04-06 時点で `overlay` は assistant-owned mechanical scope として閉じた。`--overlay-map` があれば deterministic な `ImageItem` 挿入まで自動で行い、unknown label / map miss / timing anchor 不在 / spec 不正は visual review 前に failure class で止める
- `se` は意味ラベル → registry → timing anchor までは assistant 側で閉じた。repo-local corpus に `AudioItem` write route が無い間は creative judgement 待ちではなく `SE_WRITE_ROUTE_UNSUPPORTED` として fail-fast し、新 sample が入った時だけ再測定する
- 人間が残す判断は「どのテンプレートが見た目として良いか」「どのタイミングが気持ちいいか」「音量・密度・テンポが最終制作物として十分か」という creative quality のみ

## timeline edit サブクエストの completion criteria
- G-11: completed。`slot` が registry で解決でき、`validate-ir` が `SLOT_UNKNOWN_LABEL` / `SLOT_REGISTRY_GAP` / `SLOT_CHARACTER_DRIFT` / `SLOT_DEFAULT_DRIFT` を事前検出し、`patch-ymmp` / `apply-production` が TachieItem X/Y/Zoom と `off` hide を deterministic に反映できる
- G-12: `motion` / `bg_anim` の write route が repo-local corpus ベースで固定され、fade-family `transition` route も mechanical に確認済みで、残る route 不在カテゴリは non-fade / template-backed family の sample dependency として明示され、dry-run/readback で mechanical failure を再現できる
- G-13: completed。`overlay` は label 解決、timing anchor、挿入先構造が固定され、creative density judgement と mechanical insertion failure が分離された。`se` は label/timing を解決し、write route 不在は `SE_WRITE_ROUTE_UNSUPPORTED` で mechanical failure として扱う
- 上記を満たした packet は、それぞれ独立 failure class 単位で扱い、broad な timeline retry loop に戻さない

## 検証の境界 (2026-04-05 固定)
- パイプラインの機械的動作はユニットテスト + CLI dry-run で検証する。YMM4 visual proof を繰り返し要求しない
- ユーザーへの visual proof 依頼は「初回 E2E」と「最終制作物の品質判断」のみ。増分変更 (idle_face 追加、bg proof、再現 run) では不要
- 「確認してほしいポイント」の列挙が毎回同じ内容 (表情が切り替わっているか) なら、それは確認ではなく作業の自己目的化

## 運用ルール
- 一度説明された workflow pain はここへ固定する
- 「本制作へ進む前に workflow proof が必要」な案件では、その proof 条件もここへ残す
