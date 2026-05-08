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
  - 予防: user authoring の記録は PASS / FAIL ラベルだけでなく上記 trio を completion の最小情報に含める。trio が埋まらないなら handoff は incomplete として next_action に残す。fail-fast 自体は維持してよいが、その隣に「user-side 元 artifact が `<path>` に存在 / repo の `<path>` へ未取り込み / bridge step は誰がいつ実行」を併記し、blocker と coordination gap を分離して報告する。
- `CANONICAL_FACT_DRIFT`: canonical docs (`USER_REQUEST_LEDGER` / `runtime-state` / `FEATURE_REGISTRY` / spec docs / verification index) が同じ事実 (件数・ステータス・ファイルパス・取り込み有無) で互いに矛盾し、片方が事実誤認のまま canonical 扱いされる。docs を読んだ user の判断が誤誘導され、未完了の作業が「閉じた」と扱われたり、既に閉じた作業が再依頼される。`STATUS_DRIFT` は category 混同 (priority と status、selection と approval、done と proof-only) であり、こちらは事実値の cross-doc 矛盾なので別 failure class として扱う。
  - 予防: canonical docs を更新する commit では、変更前に他 canonical docs の同一事実箇所を grep で抽出し、矛盾しないことを cross-audit する。件数・状態・パス・「currently」表記 (時間とともに stale 化する snapshot を canonical 表記しない) は特に注意。実装が並行で進む状況では、handoff 履歴エントリは過去時制または明示的 snapshot ラベルにし、現在事実は slice / next_action ブロックを単一の正本にする。
- `TEMPLATE_ANALYSIS_BYPASS`: YMM4 template source を「分析入力」ではなく「完成 timeline の raw clone 元」と扱い、配置の間隔・構図・密度が粗いときに analyzer / placement planner の不足ではなく user のテンプレート作り直しへ戻してしまう。template-first の意図が「少数 reusable template から production placement を自動生成する」から「人間が完成配置に近いテンプレを用意する」へすり替わり、配置自動化の主戦場が消える。
  - 予防: 報告では `template source` / `analyzed placement plan` / `patched .ymmp readback` / `creative acceptance` を分ける。raw clone readback は transport proof であり production acceptance ではない。spacing / composition の問題はまず assistant 側の template analyzer・placement planner・row/timing density の不足として扱い、missing source fact が readback で証明されるまで user にテンプレート再作成を依頼しない。
- `OWNERSHIP_HANDOFF_BLUR`: 完了報告の末尾に「次は人間側作業」とだけ書き、assistant が本当に停止しているのか、並行してできる調査があるのか、user がどの artifact をどこへ置けばよいのか、返答後に assistant が何を閉じるのかを曖昧にする。ユーザーが「こちらの作業で止まっていますか？」と再確認する摩擦が発生する。
  - 予防: user-owned step を出すときは、`assistant status` / `user action` / `assistant next after user action` の 3 点を本文で短く書く。hands-on が必要そうな手順なら、先に見る path、置く path、完了判定、NG 時の返し方を添える。例: `assistant status: blocked on material input; user action: put source script / base .ymmp / Production IR / maps into <pack>; assistant next: validate manifest, run pack checks, then patch/generate the next artifact`。
- `MATERIAL_HANDOFF_GAP`: `素材投入` / `入力artifact` / `必要ファイル` などの総称で user-owned step を渡し、何をどこへ置くか、どの順に GUI を押すか、NG 時に何を返すかが直後に列挙されない。結果として user が「素材とは何か」を再質問する。
  - 予防: handoff では必須ファイルと任意ファイルを分け、各ファイルについて `state`（既存 / missing / 後続生成）/ `purpose` / `target path` / `created by or generated by` / `used by GUI button or command` を最低限示す。既存 pack や README を参照する場合でも、本文に初回入力の exact path を再掲する。`置く: <path>` だけの列挙はこの failure class として扱い、`source script` / `Production IR` / `base .ymmp` / `map` へ展開する。Episode Pack の `base .ymmp` は、既に存在する場合を除き、`Build CSV` 後に YMM4 で生成・保存する後続 artifact と明記する。
- `SCRIPT_INPUT_AMBIGUITY`: `新しい台本が必要` / `台本を用意` とだけ言い、既存完成台本を使えるのか、台本本文とは何か、形式、同一episodeに固定する理由を説明しない。ユーザーは「新規創作が必要なのか」「どのファイルを使えばいいのか」を再質問する。
  - 予防: Episode Pack の source script 依頼では、`既存完成台本があれば新規作成不要`、`動画で喋らせる完成会話台本でありIR/READMEではない`、`UTF-8 .txt / 話者付き行推奨`、`CSV / IR row-range / YMM4 base / manifest を同じ台本へ結びつけるため` を同じ本文に入れる。
- `BACKGROUND_SKIT_ROLE_DRIFT`: 茶番劇を語り手台本への合いの手 / 反応トラックとして扱い、発話行に合わせて突然キャラが出てリアクションするだけの配置へ寄せる。これは背景茶番劇の本来用途（語り手とは並行する独立した視覚ストーリーで、動画テーマに説得力を足す）とズレる。
  - 予防: skit_group / background skit を進める前に、`語り手とは別レイヤー`、`合いの手ではない`、`台本行を理解して反応するのではない`、`独立した小場面として成立する` を明記する。例: 物件検索の話では「ベッドで物件情報を眺める人物」、REINS の話では「不動産業者がPCで業務データベースを扱う場面」。機械配置 proof は production quality / creative acceptance と分け、役割理解がズレた artifact は YMM4 確認待ちにしない。
  - ペナルティ: scene bible 不在、または発話行リアクション型の cue 表だけで作った artifact は `BACKGROUND_SKIT_ROLE_UNSPECIFIED` / `BACKGROUND_SKIT_ROLE_DRIFT` として closeout 不成立。`transport/readback proof only` に降格し、同じブロックで gap report と scene bible 作成へ戻す。ユーザーに creative acceptance を頼んではいけない。
- `BACKGROUND_SKIT_UNDERSPECIFIED_ACK`: 「茶番劇は合いの手ではない」という認識共有はできているが、time budget・cast continuity・screen placement・休ませる区間・登場人物・全体整合性・背景・props・素材有無・owner・proof path まで落とさず、設計未満の認識説明で止まる。これは説明としては前進だが、制作投入の handoff としては未完。
  - 予防: 認識説明の同じ返答内に、不動産DXの 7 ブロック scene bible、配達の mini bible、asset/proof matrix、assistant next を含める。未確定を認める場合でも、次に assistant が scene bible 由来の gap report を作ると明示し、IR / YMM4 placement / creative acceptance には進めない。
- `BACKGROUND_SKIT_DESIGN_OVERCLAIM`: 設計図として概略は出ているが、script line range、block proof path、intent/template 分離を欠いたまま「このまま IR / YMM4 確認に接続できる」と言う。これは読んだ側に、gap report と compact review を飛ばしてよいと誤認させる。
  - 予防: 自己完結設計の返答では、7ブロック表に script line range と block proof path を入れる。`intent` 欄には `enter_from_left` 等だけを書き、`delivery_enter_from_left_v1` 等は `template_name` 欄へ分ける。次工程は必ず `asset/proof gap report + template/proxy classification` から始める。
- `BACKGROUND_SKIT_TIMETABLE_BYPASS`: IR / 演出指定の話なのに、総尺・開始/終了時刻・演出秒数・density audit・script maturity を出さず、構成比や雰囲気だけで「設計図」と呼ぶ。結果としてタイムラインがスカスカか、脚本が杭だけか、下流が何を完成させる前提なのかが見えない。
  - 予防: IR 前の返答は `total duration` / `mm:ss start-end` / `duration sec` / `intentional rest` / `unexplained empty` / `visual states per min` / `script diagnostic` / `ideal-script delta` を実数値で含める。項目名列挙は不可。未確定なら `estimated` と書くだけでなく、source / formula / confidence / readback 後の再計算条件を添える。台本行範囲には `script_source` / `line_count` / `range_basis` を付ける。IR/YMM4 へ接続する場合は `background_skit_blueprint` artifact と `validate-background-skit-blueprint` の validator result を添える。
  - ペナルティ: `総尺 / mm:ss / 演出秒数が必要` と言うだけ、`lines 1-12` を根拠なしに置く、validator result のない数値入り表、`舞台監督の香り` などの雰囲気語で closeout する返答は `BACKGROUND_SKIT_TIMETABLE_BYPASS` として無効。assistant は同じブロックで `TIMETABLE_BLOCKED_*` か、validator 付き artifact を出し直す。
- `DOC_ROUTE_LAUNDERING`: user-owned hands-on を `.md` / README / manifest への参照へ転嫁し、`手順の正本は <file>.md:<line>` のように書くことで導線が接続済みだと誤認する。Codex / GUI / 現在の表示面から referenced file を開けない、または user が本文だけで次動作を実行できない場合、これは「補足参照」ではなく route break であり、manual step のたらい回しになる。
  - 予防: file placement / GUI operation / YMM4 check を user に渡すときは、応答本文に必須ファイル、任意ファイル、exact path、操作順、成功出力、NG返却、assistant next を再掲する。docs は根拠・背景・後で assistant が読む場所としてだけ扱い、user action の実行本文を置き換えない。検出した場合は severe interaction failure として、その handoff を無効化し、同じブロックで self-contained packet へ修正する。機械的に検出できる文面は `.claude/hooks/guardrails.py` で reject する。
- `FILE_DIFF_CLOSEOUT`: 最終報告が「どのファイルに何を追加したか」の列挙に寄り、ユーザーがファイルを開かないと、実際に何が変わったのか、制作導線上の効果、次に誰が何をするのかを復元できない。これは evidence を explanation と取り違える closeout failure であり、認知負荷を user に押し戻す。
  - 予防: file path / line number は根拠欄に限定し、先に `何が変わったか` / `なぜ効くか` / `これで次に何が可能または禁止になるか` / `まだ残る判断` / `次 owner と assistant next` を本文で説明する。ユーザーが「詳しく」「手順も」と追加依頼しなくても、通常 closeout にはこの意味層を含める。docs-only 変更でも「どの文章を足した」ではなく「次回からどの挙動が invalid / required になるか」を述べる。
- `CLOSING_CHAIN_BREAK`: 最終応答が「やったこと」だけを述べ、根拠・残リスク・次の owner・user 返答後に assistant が閉じる作業のどれかを欠いたまま終わる。結果として、user に作業だけが振られ、次に何を返せば再開できるか、そもそも assistant が停止しているのかが分からなくなる。
  - 予防: closeout 前に `summary -> evidence -> risk -> next owner -> assistant next` の鎖を確認する。鎖が切れている場合は、曖昧な「確認してください」で終えず、assistant 側で閉じる gap report / drift detection / fail-fast / docs sync を先に検討する。user action が必要なら、停止理由と返答後の assistant 作業を同じ段落で接続する。

## Ask Protocol
- 質問前に、repo 内根拠で決められない理由を確認する。理由がない場合は質問せず進める。cross-project 指示がある場合は、明示された他 repo / docs も根拠範囲に含める。
- 質問は高位分岐だけに限定し、1 問 1 intent にする。手動確認依頼と次アクション選択を同じ ask に混ぜない。
- AskUserQuestion の `question` に Markdown テーブルや長い仕様説明を入れない。ただし短い `OK / NG` や `PASS / FAIL` 形式は、作業対象・判定主体・返答の意味が本文で接続済みの場合に限る。未接続なら短縮せず、先に操作内容を具体化する。
- 選択肢は 2〜4 個程度に圧縮し、各選択肢が異なる bottleneck を解く場合だけ提示する。commit / しない、続ける / 止めるだけの yes/no を主軸にしない。`Advance` / `Audit` / `Excise` / `Explore` / `Verify` などは固定メニューではなく、次の返答を誘発する hook として使う。
- 既知文脈を「詳細を教えてください」で再質問しない。必要なら「repo 内で確認した既知情報」と「不足している delta」を明示して、delta だけ聞く。

## Manual Verification Protocol
- 手動確認項目は本文で提示し、確認の目的、見る対象、OK 条件、NG 時に返す番号を分ける。返却テンプレは最後に置くラベルであり、手順説明の代替にしない。
- 同じ確認点の YMM4 visual proof を繰り返し要求しない。初回 E2E、手順変更時、最終制作物の creative judgement に必要な場合だけ使う。
- repo 側 handoff が欠落 `_tmp/*.ymmp` を指しているときは、先に assistant 側で tracked artifact / sample / proof を探索し、user に正確なファイル名や ManualSample 再作成を求めない。
- YMM4 native template authoring を依頼するときは、最初に「開く `.ymmp`」「新規 `.ymmp` ではない場合の元 object」「作る native template 名」「含める / 含めない item」「返答が承認なのか観察報告なのか」「assistant 側で次に閉じる作業」を明記する。`既存の作業コピー` のような曖昧語や、説明抜きの `OK/NG` だけで始めない。

## Report Protocol
- 報告形式は固定見出しではなく安全柵として扱う。必要最小限は、何を変えた / 変えていない、根拠または readback、残るリスクや judgement、次に取り得る hook。
- 報告の主語を file ではなく workflow / behavior / decision に置く。file path はクリック可能な証跡として後ろに置き、読者が開かなくても意味が通る本文を先に書く。
- 最終応答では `summary -> evidence -> risk -> next owner -> assistant next` の論理鎖を切らない。見出し名は任意だが、次の作業が user に渡る場合でも assistant が次に何を閉じるかまで書く。
- user action が次の blocker の場合は、`assistant status`（停止中 / 並行作業あり）・`user action`（対象 path と必要 artifact）・`assistant next after user action`（受領後に閉じる検証や生成）を分ける。
- user action が file placement / GUI operation の場合は、本文中に必須ファイル・任意ファイル・操作順・成功出力・NG返却ファイルを置く。README や manifest へのリンクだけで初回手順説明を代替しない。
- `.md` / README / manifest への参照は、user action の実行導線ではなく裏付けに限定する。`手順の正本は ...` と書いて本文を薄くする報告は closeout 不成立として扱う。
- completion 報告では、`changed` / `not changed` / `verified` / `still blocked` の区別を保つ。docs 更新だけの場合は、実制作上の摩擦が何だけ減ったのかを明示する。
- completion 報告で `検証 pass` と `未追跡ファイル` を出す場合は、そこで止めない。未追跡が正式追加対象なら `next owner`、stage/commit の扱い、user が見るべき差分、OK/NG 後の assistant next を添える。
- user が「解説」「手順」「詳しく」を明示しない場合でも、closeout は最低限の意味説明を省略しない。短くてよいが、file diff だけで閉じるのは禁止。
- handoff では「何が抜けているか」「次にやってはいけないこと」「再オープン条件」を必要時に残す。ただし固定テンプレの穴埋めを進捗にしない。
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
- このファイルへ追記するときは、原則として `failure mode -> project risk -> prevention / report contract` の形にする。
- 心理・印象語だけでルールを追加しない。必要なら、判断遅延、手戻り、manual proof 増加、artifact path drift のどれを防ぐのかへ翻訳する。
- 仕様境界・責務境界・workflow pain そのものは、必要に応じて `INVARIANTS.md` / `OPERATOR_WORKFLOW.md` / `USER_REQUEST_LEDGER.md` へ同期する。このファイルだけに閉じ込めない。

## 常設ガード
- `docs/REPO_LOCAL_RULES.md` の Block-Start Checklist を毎ブロックの入口にする。ここで扱う interaction failure は、その checklist が効かなくなる対話上の失敗を補足する。
- `.claude/hooks/guardrails.py` で機械的に reject できる違反は hook に委ねる。Hook で止められない低品質思考は、本ファイルの failure class と maintenance rule で防ぐ。
