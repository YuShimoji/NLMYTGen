# Interaction Notes
# 対話・質問・報告を「進行を止める構造リスク」として管理する project-local canonical memo。

## 目的
- このファイルは個人的な反応ラベルを記録しない。対話上の問題を心理化せず、プロジェクトが前に進まなくなる failure mode と予防策として記録する。
- 防ぐ対象は、既知文脈の再説明、broad question による停止、価値経路のない提案、手動検証負荷の押し戻し、priority / status 混同、docs や proof だけの progress laundering。
- 判断軸は常に `active artifact` / `current bottleneck` / `actor` / `owner artifact` / `evidence` / `what becomes possible`。表現の感じの良さではなく、次の制作工程が安全に進むかで評価する。
- `docs/REPO_LOCAL_RULES.md` と `docs/ai/*.md` の強制ルールをここで重複実装しない。このファイルは、対話が原因でそれらのルールが効かなくなる場面を補足する。

## 低品質思考の兆候
- **心理化**: 構造的な非効率を個人の反応ラベルへ変換する。何を防ぐルールなのかが消え、次回の判断に使えなくなる。
- **症状列挙**: 「二択が悪い」「表が読みにくい」だけを並べる。問題は UI 形状そのものではなく、情報圧縮・選択肢品質・責務分離が崩れて判断コストが増えること。
- **原因未分解**: broad question、manual proof、status drift、value-path drift、domain packet collapse を同じ粒度で混ぜる。failure class がないため、再発時に自動で閉じられない。
- **責務混線**: user / assistant / tool / shared の actor と owner artifact を示さない。結果として、人間の creative judgement と機械的 gap report が同じ ask に押し込まれる。
- **証跡代替**: docs 更新、チェックリスト、テスト設計、報告形式を「進捗」に見せる。実際に軽くなった manual step や安全になった artifact path が説明されていなければ progress ではない。

## Interaction Failure Classes
- `REASK_DEBT`: canonical docs にある情報を再質問し、ユーザーに再説明コストを発生させる。
  - 予防: 先に `docs/ai/*.md` と project-local canonical docs を読み、既知情報と不足 delta を分けて報告する。
- `BROAD_STOP`: `判断をお願いします` / `何が足りないか教えてください` で停止する。
  - 予防: 失敗分類、repo 内根拠、次に assistant 側で閉じる作業を先に提示し、高位分岐だけ質問する。
- `OPTION_COLLAPSE`: commit yes/no や不必要な二択など、実質差分のない選択肢で進路を狭める。
  - 予防: option は `Advance` / `Audit` / `Excise` / `Unlock` のどれに効くか、actor、owner artifact、解決する bottleneck を添える。
- `MANUAL_PROOF_TRANSFER`: 機械的に閉じられる確認を YMM4 visual proof や user 作業へ押し戻す。
  - 予防: dry-run / readback / failure class で閉じられるものは assistant / tool 側で閉じ、visual proof は初回 E2E と最終 creative judgement に限定する。
- `VALUE_PATH_DRIFT`: integration point と削減される手動工程を示さず、「テンプレート」「自動化」「GUI」などの名詞へ寄る。
  - 予防: 出力がどの制作工程へ入るか、何の手作業・判断・転記が減るかを先に書く。
- `STATUS_DRIFT`: priority と status、selection と approval、done と proof-only を混同する。
  - 予防: `docs/ai/STATUS_AND_HANDOFF.md` の status semantics に戻し、status 変更には根拠と承認状態を明記する。
- `DOMAIN_PACKET_COLLAPSE`: face / timeline / skit_group などの独立サブクエストを broad frontier に戻す。
  - 予防: packet 名、failure class、readback 結果、creative judgement の残りを分けて報告する。
- `TEMPLATE_FORMALISM`: Prompt、チェックリスト、返却テンプレ、短い OK/NG 形式を、作業接続性より優先する。対象ファイル・作るもの・元にする object・判定主体が欠けたまま形式だけ整い、実作業が接続不能になる。
  - 予防: テンプレを出す前に `open target` / `create or modify target` / `source object` / `actor` / `owner artifact` / `acceptance meaning` / `replan condition` を埋める。1 つでも欠ける場合は、短い返却形式へ圧縮せず、まず欠落項目を repo 内で解決する。
- `COMPLETION_CLAIM_DRIFT`: 「実装完了」報告が test pass / preflight / docs 更新を完了根拠として提示し、その slice の production-value condition (write-route artifact の readback) を demonstrate しない。`uv run pytest PASS` を完了の最上段証跡に置き、実走行 demo を含めずに canonical 状態を「閉じた」へ進める。
  - 予防: 完了報告は `changed` / `not changed` / `verified` / `still blocked` を分け、`verified` 欄に success criterion に対応する readback 結果 (例: G-24 placement なら patched `.ymmp` への GroupItem 挿入の JSON readback、IR index 単位の Layer / Frame 一致) を併記する。実走行 demo が未実施なら「コード骨格完了、demo 未実施」と切り分けて報告する。`INVARIANTS §Production Value North Star` の preflight ≠ 成果ルールを運用補強する。
- `USER_ARTIFACT_DRIFT`: ユーザー authoring artifact (YMM4 native template / sample / IR / registry) の PASS sync を報告するだけで、user-side 元 artifact の path、repo-tracked 取り込み先 path、bridge step (誰が・いつ・どう取り込むか) の trio を併記せず canonical 状態を「閉じた」へ進める。後で artifact が repo に存在せず、user に「自分が作った artifact がリモートに無い、また作る必要があるか」を再発見させる。fail-fast (例: `SKIT_TEMPLATE_SOURCE_MISSING`) を「意図的ブロッカー」と表現することで、coordination 失敗が機能のように見える reframe が起きる。
  - 予防: user authoring の記録は PASS / FAIL ラベルだけでなく上記 trio を必ず併記する。trio が埋まらないなら handoff は incomplete として next_action に残す。fail-fast 自体は維持してよいが、その隣に「user-side 元 artifact が `<path>` に存在 / repo の `<path>` へ未取り込み / bridge step は誰がいつ実行」を併記し、blocker と coordination gap を分離して報告する。
- `CANONICAL_FACT_DRIFT`: canonical docs (`USER_REQUEST_LEDGER` / `runtime-state` / `FEATURE_REGISTRY` / spec docs / verification index) が同じ事実 (件数・ステータス・ファイルパス・取り込み有無) で互いに矛盾し、片方が事実誤認のまま canonical 扱いされる。docs を読んだ user の判断が誤誘導され、未完了の作業が「閉じた」と扱われたり、既に閉じた作業が再依頼される。`STATUS_DRIFT` は category 混同 (priority と status、selection と approval、done と proof-only) であり、こちらは事実値の cross-doc 矛盾なので別 failure class として扱う。
  - 予防: canonical docs を更新する commit では、変更前に他 canonical docs の同一事実箇所を grep で抽出し、矛盾しないことを cross-audit する。件数・状態・パス・「currently」表記 (時間とともに stale 化する snapshot を canonical 表記しない) は特に注意。実装が並行で進む状況では、handoff 履歴エントリは過去時制または明示的 snapshot ラベルにし、現在事実は slice / next_action ブロックを単一の正本にする。
- `TEMPLATE_ANALYSIS_BYPASS`: YMM4 template source を「分析入力」ではなく「完成 timeline の raw clone 元」と扱い、配置の間隔・構図・密度が粗いときに analyzer / placement planner の不足ではなく user のテンプレート作り直しへ戻してしまう。template-first の意図が「少数 reusable template から production placement を自動生成する」から「人間が完成配置に近いテンプレを用意する」へすり替わり、配置自動化の主戦場が消える。
  - 予防: 報告では `template source` / `analyzed placement plan` / `patched .ymmp readback` / `creative acceptance` を分ける。raw clone readback は transport proof であり production acceptance ではない。spacing / composition の問題はまず assistant 側の template analyzer・placement planner・row/timing density の不足として扱い、missing source fact が readback で証明されるまで user にテンプレート再作成を依頼しない。

## Ask Protocol
- 質問前に必ず、repo 内根拠で決められない理由を確認する。理由がない場合は質問せず進める。
- 質問は高位分岐だけに限定し、1 問 1 intent にする。手動確認依頼と次アクション選択を同じ ask に混ぜない。
- AskUserQuestion の `question` に Markdown テーブルや長い仕様説明を入れない。ただし短い `OK / NG` や `PASS / FAIL` 形式は、作業対象・判定主体・返答の意味が本文で接続済みの場合に限る。未接続なら短縮せず、先に操作内容を具体化する。
- 選択肢は 3 個以下に圧縮し、各選択肢が異なる bottleneck を解く場合だけ提示する。commit / しない、続ける / 止めるだけの yes/no を主軸にしない。
- 既知文脈を「詳細を教えてください」で再質問しない。必要なら「repo 内で確認した既知情報」と「不足している delta」を明示して、delta だけ聞く。

## Manual Verification Protocol
- 手動確認項目は本文で提示し、確認の目的、見る対象、OK 条件、NG 時に返す番号を分ける。返却テンプレは最後に置くラベルであり、手順説明の代替にしない。
- 同じ確認点の YMM4 visual proof を繰り返し要求しない。初回 E2E、手順変更時、最終制作物の creative judgement に必要な場合だけ使う。
- repo 側 handoff が欠落 `_tmp/*.ymmp` を指しているときは、先に assistant 側で tracked artifact / sample / proof を探索し、user に正確なファイル名や ManualSample 再作成を求めない。
- YMM4 native template authoring を依頼するときは、最初に「開く `.ymmp`」「新規 `.ymmp` ではない場合の元 object」「作る native template 名」「含める / 含めない item」「返答が承認なのか観察報告なのか」「assistant 側で次に閉じる作業」を明記する。`既存の作業コピー` のような曖昧語や、説明抜きの `OK/NG` だけで始めない。

## Report Protocol
- BLOCK SUMMARY では、まず current bottleneck、change relation、trust assessment、次に何が可能になったかを示す。
- completion 報告では、`changed` / `not changed` / `verified` / `still blocked` を分ける。docs 更新だけの場合は、実制作上の摩擦が何だけ減ったのかを明示する。
- handoff では「何が抜けているか」「次にやってはいけないこと」「再オープン条件」も残す。
- 再開時の repeated context は、まず `docs/ai/*.md` と project-local canonical docs を読んでから扱う。prompt や古い handoff を正本より優先しない。
- 字幕改行の報告では、「長すぎる行が減ったか」と「残りが bulk pain か individual judgement か」を分ける。境界ケース段階では、rule 追加と corpus 収集を混同しない。

## Domain Reporting Contracts
- face 問題は `FACE_UNKNOWN_LABEL` / `PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE_*` / `FACE_MAP_MISS` / `IDLE_FACE_MAP_MISS` / `VOICE_NO_TACHIE_FACE` の failure class 名で報告する。
- face failure class が mechanical に確定しているときは、同じ趣旨の YMM4 visual proof を追加で要求しない。failure class ごとの next action を先に提示する。
- timeline 問題は broad frontier に戻さず、`slot patch` / `native-template measurement` / `overlay-se insertion` / `skit_group template` の packet 名で分ける。
- timeline packet の completion 報告では、visual impression ではなく dry-run / readback の結果を先に根拠として示す。コード変更がないときにテストを回さない。
- mechanical failure と creative judgement を混ぜない。前者は registry gap / write route / readback mismatch として示し、後者は見た目・テンポ・密度の判断として分離する。
- 茶番劇演者については、`speaker_tachie motion` と混同せず `skit_group template` の exact / fallback / manual note で報告する。未自動化を隠すために raw effect 名だけを並べない。

## Development Drift Guards
- 新しい自動化経路を提案する際は、現行ロードマップと `docs/AUTOMATION_BOUNDARY.md` の段階構成との整合を示す。
- 研究 (ymmp 解析、プラグイン API 調査、外部ツール評価等) と開発 (IR 定義、プロンプト改訂、adapter 実装等) を混同しない。研究が 2 ブロック以上続く場合は、開発へ戻るための artifact path を明示する。
- テスト設計を主活動にしない。テストはコード変更時のみ。docs のみのブロックでは pytest を回さず、completion でも pytest を示さない。
- template 資産の不足を、テスト追加や route contract の精密化だけで補ったことにしない。production の bottleneck が template 作成・解決にあるなら、そこを正本に反映する。
- 外部ツール (YMovieHelper 等) を主軸として採用する提案には、保守性・更新状況・撤退可能性の評価を必須とする。サービス終了済み・更新停止ツールへの依存設計は避ける。

## Maintenance Rule
- このファイルへ追記するときは、必ず `failure mode -> project risk -> prevention / report contract` の形にする。
- 心理・印象語だけでルールを追加しない。必要なら、判断遅延、手戻り、manual proof 増加、artifact path drift のどれを防ぐのかへ翻訳する。
- 仕様境界・責務境界・workflow pain そのものは、必要に応じて `INVARIANTS.md` / `OPERATOR_WORKFLOW.md` / `USER_REQUEST_LEDGER.md` へ同期する。このファイルだけに閉じ込めない。

## 常設ガード
- `docs/REPO_LOCAL_RULES.md` の Block-Start Checklist を毎ブロックの入口にする。ここで扱う interaction failure は、その checklist が効かなくなる対話上の失敗を補足する。
- `.claude/hooks/guardrails.py` で機械的に reject できる違反は hook に委ねる。Hook で止められない低品質思考は、本ファイルの failure class と maintenance rule で防ぐ。
