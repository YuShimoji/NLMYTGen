# Interaction Notes
# 対話・質問・報告を「進行を止める構造リスク」として管理する project-local canonical memo。

## 目的
- このファイルは個人的な反応ラベルを記録しない。対話上の問題を心理化せず、プロジェクトが前に進まなくなる failure mode と予防策として記録する。
- 防ぐ対象は、既知文脈の再説明、broad question による停止、価値経路のない提案、手動検証負荷の押し戻し、priority / status 混同、docs や proof だけの progress laundering。
- 判断軸は常に `active artifact` / `current bottleneck` / `actor` / `owner artifact` / `evidence` / `what becomes possible`。表現の感じの良さではなく、次の制作工程が安全に進むかで評価する。
- `docs/REPO_LOCAL_RULES.md` と `docs/ai/*.md` の強制ルールをここで重複実装しない。このファイルは、対話が原因でそれらのルールが効かなくなる場面を補足する。
- failure class はインシデントごとに増やさない。新しい failure 観測時はまず既存 class で説明できるかを先に確認し、できる場合は class 追加ではなく実行段階で適用する。

## 低品質思考の兆候
- **心理化**: 構造的な非効率を個人の反応ラベルへ変換する。何を防ぐルールなのかが消え、次回の判断に使えなくなる。
- **症状列挙**: 「二択が悪い」「表が読みにくい」だけを並べる。問題は UI 形状そのものではなく、情報圧縮・選択肢品質・責務分離が崩れて判断コストが増えること。
- **原因未分解**: broad question、manual proof、status drift、value-path drift、domain packet collapse を同じ粒度で混ぜる。failure class がないため、再発時に自動で閉じられない。
- **責務混線**: user / assistant / tool / shared の actor と owner artifact を示さない。結果として、人間の creative judgement と機械的 gap report が同じ ask に押し込まれる。
- **証跡代替**: docs 更新、チェックリスト、テスト設計、報告形式を「進捗」に見せる。実際に軽くなった manual step や安全になった artifact path が説明されていなければ progress ではない。
- **反射的同意**: 指摘を受けた直後に根拠を確認せず方針を反転させる。これ自体が judgment の欠落であり、ルール追加では治らない。

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
- `TEMPLATE_FORMALISM`: Prompt、チェックリスト、返却テンプレ、短い OK/NG 形式を、作業接続性より優先する。対象ファイル・作るもの・元にする object・判定主体が欠けたまま形式だけ整い、実作業が接続不能になる。
  - 予防: テンプレを出す前に `open target` / `create or modify target` / `source object` / `actor` / `owner artifact` / `acceptance meaning` / `replan condition` を埋める。1 つでも欠ける場合は、短い返却形式へ圧縮せず、まず欠落項目を repo 内で解決する。
- `FIXED_LABEL_REVIEW_LOCK`: user review を `accept` / `reject` / `revise_once` などの固定ラベル入力に閉じ込め、自由文に含まれる意図・制約・優先度を捨てる。固定語彙は agent 側の内部正規化には有効だが、user 側の必須返答形式にすると review が止まり、実際の判断材料が失われる。
  - 予防: review が必要な場合は、対象・見る点・自由文可・例・agent がどう解釈するか・完了シグナルを含む Review Card を出す。受け取った自由文は `target` / `intent` / `constraints` / `confidence` へ内部 parse し、confidence が medium/high なら reversible な修正・docs 反映・artifact 生成・validation へ進む。low confidence かつ誤解が artifact 方向を変える場合だけ、Review Clarification Card を 1 回だけ出す。
- `FILE_DIFF_CLOSEOUT`: 最終報告が「どのファイルに何を追加したか」の列挙に寄り、ユーザーがファイルを開かないと、実際に何が変わったのか、制作導線上の効果、次に誰が何をするのかを復元できない。これは evidence を explanation と取り違える closeout failure であり、認知負荷を user に押し戻す。
  - 予防: file path / line number は根拠欄に限定し、先に `何が変わったか` / `なぜ効くか` / `これで次に何が可能または禁止になるか` / `まだ残る判断` / `次に誰がどう動くか` を本文で説明する。ユーザーが「詳しく」「手順も」と追加依頼しなくても、通常 closeout にはこの意味層を含める。docs-only 変更でも「どの文章を足した」ではなく「次回からどの挙動が invalid / required になるか」を述べる。
- `CLOSING_CHAIN_BREAK`: 最終応答が「やったこと」だけを述べ、根拠・残リスク・次に動く主体・返答後に閉じる作業のどれかを欠いたまま終わる。結果として、user に作業だけが振られ、次に何を返せば再開できるか、assistant が待機中なのかが分からなくなる。
  - 予防: closeout 前に、完了内容・根拠・残る不確実性・次に動く主体・返答後に閉じる作業が自然文でつながっているか確認する。これは内部チェックであり、固定見出しや英語ラベルを出力する要求ではない。
- `NEXT_WORK_SHORTHAND`: 残作業レビューや次回作業導線が `P0/P1`、commit/test/path、または「こちら側で未処理なし」の短文に縮退し、各作業の目的・効果・必要条件・現在状態・次の動きが本文だけで分からない。ユーザーは何を選ぶと何が軽くなるか判断できず、次回の作業開始がまた status 確認から始まる。
  - 予防: `残作業` / `次回` / `優先順位` / `レビューしてください` が出た場合は、作業ごとに目的、効果、必要条件、現在状態、次の動きを説明する。表は任意であり、固定列名を出す必要はない。assistant が今すぐ動ける候補と user review 待ちを混ぜない。

## Ask Protocol
- 質問前に、repo 内根拠で決められない理由を確認する。理由がない場合は質問せず進める。cross-project 指示がある場合は、明示された他 repo / docs も根拠範囲に含める。
- 質問は高位分岐だけに限定し、1 問 1 intent にする。手動確認依頼と次アクション選択を同じ ask に混ぜない。
- AskUserQuestion の `question` に Markdown テーブルや長い仕様説明を入れない。ただし短い `OK / NG` や `PASS / FAIL` 形式は、作業対象・判定主体・返答の意味が本文で接続済みの場合に限る。未接続なら短縮せず、先に操作内容を具体化する。
- 選択肢は 2〜4 個程度に圧縮し、各選択肢が異なる bottleneck を解く場合だけ提示する。commit / しない、続ける / 止めるだけの yes/no を主軸にしない。`Advance` / `Audit` / `Excise` / `Explore` / `Verify` などは固定メニューではなく、次の返答を誘発する hook として使う。
- 既知文脈を「詳細を教えてください」で再質問しない。必要なら「repo 内で確認した既知情報」と「不足している delta」を明示して、delta だけ聞く。
- Review Card は review が必要な artifact の近く、または Artifacts 節の直後に置く。内容は、target、見る点は最大 3 つ、自由文 review 可、自由文例、agent 側の解釈方法、完了シグナルに絞る。固定 phrase は要求しない。
- user の自由文 review は正本入力として扱う。agent は内部で固定ラベルへ正規化してよいが、user に固定ラベルでの再回答を求めない。

## Manual Verification Protocol
- 手動確認項目は本文で提示し、確認の目的、見る対象、OK 条件、NG 時に返す番号を分ける。返却テンプレは最後に置くラベルであり、手順説明の代替にしない。
- 同じ確認点の YMM4 visual proof を繰り返し要求しない。初回 E2E、手順変更時、最終制作物の creative judgement に必要な場合だけ使う。
- repo 側 handoff が欠落 `_tmp/*.ymmp` を指しているときは、先に assistant 側で tracked artifact / sample / proof を探索し、user に正確なファイル名や ManualSample 再作成を求めない。
- Review Card で自由文を受け取った場合は、まず `target` / `intent` / `constraints` / `confidence` を内部化する。medium/high confidence なら、次の 1〜3 個の reversible な agent-side action を実行してから報告する。low confidence で誤解が artifact 方向を変えるときだけ clarification を 1 回に限定する。

## Report Protocol
- 報告形式は固定見出しではなく安全柵として扱う。必要最小限は、何を変えた / 変えていない、根拠または readback、残るリスクや judgement、次に取り得る hook。
- user が ChatGPT 監修へ貼る前提で単一コードブロック報告を明示要求している場合は、通常文の短い要約に続けて、`BEGIN_COPY_BLOCK_FOR_CHATGPT` から `END_COPY_BLOCK_FOR_CHATGPT` までを 1 つの copyable code block に入れる。ブロック内は自己完結させ、branch / HEAD / clean state / known untracked / active lane / 変更有無 / 検証 / 境界維持 / 欠けている artifact / 次に返すものを含める。ただし raw OPML、URL、token、article body、private data は入れない。
- 報告の主語を file ではなく workflow / behavior / decision に置く。file path はクリック可能な証跡として後ろに置き、読者が開かなくても意味が通る本文を先に書く。
- 報告の深さは `Micro report` / `Slice closeout` / `Handoff` で変える。Micro は短い作業確認でよいが、Slice closeout は差分の焦点、意図的に触っていない範囲、North Star 上の位置、evidence、残存リスク、drift self-check、recommended default、next owner を本文で復元できる必要がある。Handoff はさらに branch / commit / clean state / 次に読む artifact を含める。
- `Drift self-check` は固定見出しとして毎回出す義務ではないが、slice closeout では少なくとも case overfitting、docs-only loop、standalone artifact completion、next-artifact continuity のどれが危ないかを確認してから出す。
- `Recommended default` は「次に何をすべきか」だけでなく、なぜそれが安全か、代替は何か、誰が動くかを含める。assistant が今すぐ進められる候補と user decision 待ちを混ぜない。
- 最終応答では、完了内容、根拠、残る不確実性、次に動く主体、返答後に閉じる作業の論理鎖を切らない。ただし、これらを固定見出しや英語ラベルとして出力しない。
- user 側の入力や確認が次の blocker の場合は、対象 path、必要 artifact、完了判定、NG 時に返す情報、受領後に閉じる検証や生成を本文で分ける。固定ラベルは内部整理に留める。
- Review Card を出した場合や自由文 review を消費した場合は、必要に応じて Freeform Review Intake Result を報告へ含める。これは user に再入力を求めるためではなく、agent がどう解釈し、どの reversible action へ進んだかを見える化するためのもの。
- Review Debt が残る場合は、何をまだ人間が見ればよいかを自然文で示す。固定 phrase required は常に no とし、例はあくまで自由文の例に留める。
- completion 報告では、`changed` / `not changed` / `verified` / `still blocked` の区別を保つ。docs 更新だけの場合は、実制作上の摩擦が何だけ減ったのかを明示する。
- handoff では「何が抜けているか」「次にやってはいけないこと」「再オープン条件」を必要時に残す。ただし固定テンプレの穴埋めを進捗にしない。
- 再開時の repeated context は、まず `docs/ai/*.md` と project-local canonical docs を読んでから扱う。prompt や古い handoff を正本より優先しない。

## Development Drift Guards
- 新しい自動化経路を提案する際は、現行ロードマップと `docs/AUTOMATION_BOUNDARY.md` の段階構成との整合を示す。
- 研究 (ymmp 解析、プラグイン API 調査、外部ツール評価等) と開発 (IR 定義、プロンプト改訂、adapter 実装等) を混同しない。研究が 2 ブロック以上続く場合は、開発へ戻るための artifact path を明示する。
- テスト設計を主活動にしない。テストはコード変更時のみ。docs のみのブロックでは pytest を回さず、completion でも pytest を示さない。
- 外部ツール (YMovieHelper 等) を主軸として採用する提案には、保守性・更新状況・撤退可能性の評価を必須とする。サービス終了済み・更新停止ツールへの依存設計は避ける。

## Maintenance Rule
- このファイルへ追記するときは、原則として `failure mode -> project risk -> prevention / report contract` の形にする。
- 心理・印象語だけでルールを追加しない。必要なら、判断遅延、手戻り、manual proof 増加、artifact path drift のどれを防ぐのかへ翻訳する。
- 仕様境界・責務境界・workflow pain そのものは、必要に応じて `INVARIANTS.md` / `OPERATOR_WORKFLOW.md` / `USER_REQUEST_LEDGER.md` へ同期する。このファイルだけに閉じ込めない。
- インシデント由来の task-specific class は追加しない。同じ問題が 3 回以上、複数 lane で観測された汎用 pattern だけを class 化する。task-specific な傷跡は当該 slice の handoff doc に残す。

## 常設ガード
- `docs/REPO_LOCAL_RULES.md` を毎ブロックの短い入口にする。ここで扱う interaction failure は、その core rules が効かなくなる対話上の失敗を補足する。
