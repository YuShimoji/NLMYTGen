# REPO_LOCAL_RULES.md — repo-local 運用ルール（正本）

NLMYTGen の **日々の Hard Rules・再開読了予算・Checklist** の正本。長い背景説明ではなく、毎ブロックで効かせる強制ルールだけを置く。vendor-neutral な AI ルールは引き続き `docs/ai/*.md`、非交渉境界は `docs/INVARIANTS.md`。

**`.claude/CLAUDE.md`** は Claude Code 等が慣例で読む入口用の **短いポインタ** に留める（本文の重複を避ける）。

---

## Restart Read Budget

通常再開では、読了対象を増やすこと自体を progress にしない。毎回読むのは次の 3 点まで。

1. `AGENTS.md` — repo 境界・入口責務
2. `docs/REPO_LOCAL_RULES.md` — 本ファイルの Hard Rules / Block-Start Checklist / Ask Hygiene
3. `docs/runtime-state.md` — `slice` / `next_action` / `last_change_relation` / `last_verification`

追加で読むのは、作業接続に必要な場合だけ。

- 迷子対策: `docs/NAV.md`
- handoff / 決定履歴: `docs/project-context.md` の HANDOFF SNAPSHOT または該当 DECISION LOG だけ
- status / backlog: `docs/FEATURE_REGISTRY.md` の該当 ID だけ
- 非交渉境界: `docs/INVARIANTS.md` の該当節だけ
- durable request: `docs/USER_REQUEST_LEDGER.md` の現在有効な要求 / 該当 backlog delta だけ
- workflow pain: `docs/OPERATOR_WORKFLOW.md` の該当工程だけ
- ask / manual verification / template formalism: `docs/INTERACTION_NOTES.md` の該当 failure class だけ
- vendor-neutral rule: `docs/ai/*.md` の該当 gate / workflow 節だけ

フル再アンカリングは `AGENTS.md` の例外手順を使う。全 canonical docs の存在は保つが、全文読了を通常再開の前提にしない。

## Hard Rules

- Git follow-through is assistant-owned by default. When a slice is validated and the recommended next Git action is non-destructive, run `git add` / `git commit` / `git push` without waiting for user approval. Stop only for destructive operations, pushed-history rewrites, ambiguous large deletions, cross-repo publication, or explicit user prohibition.
- 通常はこの repo 以外の file / memory / docs を読まない・書かない。ユーザーが cross-project / 他 repo 作業を明示した場合は、その明示範囲だけ扱う。
- HoloSync / NLMandSlideVideoGenerator / NarrativeGen / VastCore への逸脱は通常禁止。明示された cross-project scope に含まれる場合だけ例外にする。
- repeated visual proof を要求しない。YMM4 visual proof は初回 E2E と最終制作物の品質判断だけ。
- mechanical な確認は GUI の Dry Run または開発時のユニットテストで閉じる。コード変更がないときにテストを回さない。
- `src/` または `gui/` のロジックを変えたブロックの終わりにだけ pytest 結果を示す。ドキュ / runtime-state のみのブロックでは不要。
- 修正を指摘されたら止まらない。次を同じブロックで自分で確定して進める。
  - 何が誤りだったか
  - 何を修正するか
  - 修正後にどう検証するか
- `判断をお願いします` `何が足りないか教えてください` のような broad question で止まらない。
- user に聞く前に、repo 内根拠で決められない理由を自分で確認する。
- `assistant 側でやることがない` と安易に結論しない。まず次を検討する。
  - fail-fast
  - gap report
  - quality gate
  - drift detection
  - docs sync
  - operator の手動負荷削減
- `skit_group` / background skit / 茶番劇を扱うときは、語り手への合いの手ではなく、並行する独立小場面であることを scene bible で先に固定する。台本行ごとのリアクション cue だけで `.ymmp` を作った場合、その artifact は transport/readback proof に降格し、creative acceptance / production quality / YMM4 確認待ちへ渡してはいけない。scene bible 不在、または time budget / cast continuity / screen placement が無い handoff は **invalid handoff** として同じブロックで gap report に戻す。
- 茶番劇の認識説明で「未確定」「設計表を作るべき」「素材面が未整理」と言うだけで終えない。概念共有に加えて `scene bible + time budget + cast continuity`（script line range / 登場人物 / 配置 / 背景 / props / 休ませる区間 / 既存素材 / 不足素材 / owner / proof path）を assistant-owned next action として接続する。これが無い closeout は **BACKGROUND_SKIT_UNDERSPECIFIED_ACK** として未完扱い。
- 茶番劇の設計図 closeout で `script line range` を省かない。7 ブロックの概略や time budget 表だけでは self-contained ではない。各 block の proof path と、IR intent / template_name の分離も同じ返答内に含める。
- 茶番劇を IR / 演出指定へ進める場合、構成比や項目名だけで止めない。`total duration` / `mm:ss start-end` / `duration sec` / `density audit` / `sparse risk` / `script maturity` は **実数値** を入れる。`総尺 / mm:ss / 演出秒数が必要` は未完。総尺が未確定なら `estimated timetable` として、source / formula / confidence / revision trigger を明記する。値を計算できない場合は `TIMETABLE_BLOCKED_*` と exact missing source を返す。
- 茶番劇の数値入り表だけでは IR / YMM4 / production timing に進めない。`background_skit_blueprint.json` 相当の source-backed artifact を作り、`validate-background-skit-blueprint` の `status` / `errors` / `blockers` / `derived_metrics` を closeout に含める。`passed` 以外は cast motion IR / YMM4 creative acceptance / production timing 生成不可。ただし `blocked` でも `allowed_next_actions` に `overlay_only_compact_review` がある場合だけ overlay/card-only compact review に進める。`failed` / `blocked` は、捏造せず止まった診断としてのみ有効。
- overlay/card-only compact review を生成した closeout は、人間向け言い換えではなく `artifact path: ...` / `readback result: ...` / `allowed_next_actions: [overlay_only_compact_review]` / `forbidden_next_actions: [cast_motion_ir, ymm4_creative_acceptance, production_timing]` / `remaining blockers: [...]` / `not creative acceptance` を literal key として同じ本文に含める。これが無い生成報告は integration review に渡さない。
- `lines 1-12` のような台本行範囲を使う場合、`script_source` / `line_count` / `range_basis` / readback evidence を同じ表に入れる。行範囲だけの設計図は arbitrary estimate とみなし、IR / YMM4 / creative acceptance へ進めない。
- 台本が構造未成熟なら、演出で取り繕わない。`script_diagnostic` と `ideal-script delta` を先に出し、どの台本なら理想だったか、どの行範囲に thesis / causality / visual anchor / evidence / payoff が欠けているかを返す。
- 茶番劇 closeout では `舞台監督の香り` などの雰囲気語、励まし、感想で設計を代替しない。必要なのは values / blockers / deltas / source-backed gaps である。
- 茶番劇の次工程を `このまま IR / YMM4 確認に接続できる` と過大表現しない。正しい順序は `scene bible → asset/proof gap report → template/proxy 分類 → revised skit_group IR案 → compact review → creative acceptance → production timing`。
- adapter / Python の説明を「既存 GroupItem を配置するだけ」に矮小化しない。素材アート生成はしないが、IR validation / registry 解決 / template source 解析 / `.ymmp` patch / readback / gap report は assistant-owned である。
- user-owned step を出すときは、`素材投入` / `入力を置く` / `GUIで進める` のような総称だけで止めない。最低限、assistant が停止中か、user が扱う必須ファイル・任意ファイルの exact path、各ファイルの現在状態（既存 / missing / GUI・YMM4で後続生成）、何のファイルか、作成元または生成手順、作成/選択の順番、成功時にできる出力、NG時に返す JSON / 文面、受領後に assistant が閉じる検証を同じ handoff に含める。
- `置く: <path>` / `put: <path>` の列挙だけで user action を渡すのは禁止。各行または直後に `what / create / used by / state` 相当がない場合、その handoff は invalid として同じブロックで書き直す。特に Episode Pack の `ymmp/<episode_id>_base.ymmp` は通常「最初に置くファイル」ではなく、`Build CSV` 後に YMM4 で CSV を読み込んで Save As する後続生成物として説明する。
- `新しい台本を用意してください` のように、台本要求を単独で渡すのは禁止。Episode Pack では `source script` が「この動画で喋らせる完成会話台本」であること、既存完成台本があれば新規作成不要であること、UTF-8 `.txt` / 話者付き行などの受け入れ形式、CSV / Production IR row-range / YMM4 base / manifest を同じ台本に結びつける理由を同じ handoff に含める。
- user-owned step を `.md` / README / manifest への参照で成立扱いしない。`手順の正本は <file>.md:<line>` のような官僚的 handoff は **invalid handoff** として扱い、接続済み `next_action` / closeout に数えない。docs は補足根拠であり、user が実行する導線ではない。
- Codex / GUI / 現在の表示面から referenced `.md` を開けるか不明な場合、その導線は **開けないもの** として扱う。file placement / GUI operation / YMM4 check を user に渡すなら、本文だけで実行できる必須ファイル、exact path、操作順、成功出力、NG返却、assistant next を再掲する。
- 最終報告で file path / line / commit / test 名の列挙を、説明の代替にしない。file list は証跡であり説明ではない。ユーザーがファイルを開かなくても、何が変わったか、なぜ効くか、これで次に何が可能/禁止になるか、次に誰が何をするかが本文だけで分かるようにする。
- 最終応答は `やったこと` だけで閉じない。根拠 / 残リスク / 次の owner / user 返答後に assistant が閉じる作業まで論理的に接続する。接続できない場合は、まず assistant 側の gap report / drift detection / fail-fast / docs sync を検討する。
- `検証 pass` と `未追跡ファイル` だけを列挙して止まらない。未追跡が正式追加対象なら、stage/commit の owner、user が見るべき差分、OK/NG 後に assistant が何をするかまで書く。

## pytest（最小）

テスト投資の判断は **Block-Start Checklist** と **Quality Priority** に委ね、手順を増やさない。

- 日次・短ループ: `uv run pytest`（`@pytest.mark.integration` は既定でスキップ。`tests/conftest.py`）
- `src/` または CLI 契約を変えたマージ前など: `NLMYTGEN_PYTEST_FULL=1 uv run pytest` を追加で回す（マーカーは `pyproject.toml`）
- 新規 `@pytest.mark.integration` は、ユニットだけでは subprocess 経路の契約が保てないときに限定する。似たケースは既存テストへのケース追加で統合を優先する。
- 手動 E2E proof（`docs/verification/` 等）は Hard Rules の「repeated visual proof を要求しない」に従い、初回・フロンティア・手順変更時に寄せる。
- **git のコミット傾向分析や Playwright を必須ゲートに含めない**（争点時のみ任意でよい）。

## Block-Start Checklist

各ブロックで次を短く確定してから進める。

1. 今の bottleneck は何か
2. これからやる作業はその bottleneck に直接効くか
3. user に新しい manual proof を頼まずに閉じられるか
4. user に聞く前に repo 内根拠で決められないか
5. user-owned step を出す場合、assistant が停止しているのか・user が何を置く/返すのか・受領後に assistant が何をするのかが一読で分かるか
6. `素材` や `artifact` という総称を使う場合、その内訳・置き先・戻り値・現在状態・作成元が直後に列挙されているか
7. `.md` / README / manifest 参照を、user が実行する手順本文の代替にしていないか
8. 茶番劇を扱う場合、`合いの手ではない` / `別レイヤー` / `独立小場面` / `scene bible` が固定され、台本行リアクションだけで acceptance に進んでいないか
9. 茶番劇の認識説明で、`script line range` / `time budget` / `cast continuity` / `screen placement` / `block proof path` / `asset-proof matrix` と assistant-owned next action まで接続しているか
10. 茶番劇を IR / 演出指定へ進める場合、`total duration` / `mm:ss start-end` / `duration sec` / `density audit` / `script maturity` が実数値で揃っているか
11. 茶番劇の数値表を出す場合、`validate-background-skit-blueprint` の validator result があり、`derived_metrics` と照合済みか
12. 台本行範囲を使う場合、`script_source` / `line_count` / `range_basis` があり、任意の line range を置いていないか
13. 最終報告が file list だけでなく、読まなくても分かる意味・効果・次動作を含んでいるか

この 13 個に yes と言えない作業は、まず理由を明文化してから進める。

## Block-End Closeout Contract

ブロック終端の報告は固定テンプレートではなく、次の作業を破綻なく再開するための最低契約として扱う。少なくとも次の鎖を本文内で保つ。

- `summary`: 完了したこと / 意図的に触っていないこと。
- `evidence`: 検証・readback・確認した根拠、または確認しなかった理由。
- `risk`: 残る不確実性、古い証跡、creative judgement。
- `next owner`: 次に動くのが assistant / user / both のどれか。
- `assistant next`: user 返答後に assistant が見る JSON / readback / gap、生成または修正する artifact。
- `meaning`: file path を開かなくても分かる、今回の変更で実際に変わった挙動・制約・制作導線上の効果。

この鎖を埋められないまま `確認してください` `次をお願いします` で終えない。file path / line number は根拠として添えるだけで、`meaning` の代替にしない。

## User-Owned Handoff Contract

user が次に動く必要がある場合は、短くても次を 1 セットで出す。

- `assistant status`: blocked / parallel work available のどちらか。
- `user action`: 必須 artifact、任意 artifact、置き先 path、GUI 操作順、完了判定。
- `file contract`: 各 artifact について `state`（exists / missing / generated later）、`what`（何のファイルか）、`create`（作成元または生成手順）、`used by`（どの GUI ボタン / CLI が使うか）を省略しない。
- `assistant next`: 受領後に見る JSON / readback / gap、次に生成または修正する artifact。
- `do not`: NG 時に手編集してはいけない出力、まだ開かない YMM4 確認、混ぜてはいけない別 lane。
- `doc route`: docs / README / manifest は裏付けとして添えてよいが、そこへ手順を転嫁しない。user action が必要な handoff は、この応答本文だけで実行できなければ invalid。

例外なく、`素材` は file-kind ではなく説明語として扱う。`source script` / `Production IR` / `base .ymmp` / `bg_map` / `skit_group_registry` のように、実ファイル種別へ展開してから user へ渡す。

## Ask Hygiene

- 質問は高位分岐だけ。
- 質問が必要でも、2〜4 個程度の実質差分がある選択肢まで圧縮する。固定メニューではなく、異なる bottleneck を解く hook として出す。
- 通常は「別 repo へ移動」「別 PJ の memory を参照」を選択肢に含めない。ユーザーが cross-project 作業を明示した場合だけ、その範囲内で候補にする。

## Quality Priority

- 進捗は「新機能が増えたか」ではなく、次で評価する。
  - quality を落とす入力を早期に止められるか
  - empty hit / unknown label / drift を可視化できるか
  - operator の反復作業が減ったか
  - artifact の品質に近づくか

## Hooks

機械的に判定できる違反は `.claude/hooks/guardrails.py` で reject する。対象:

- 明示 scope なしの repo 外参照
- broad question による停止
- repeated visual proof の反復要求
- `.md` / README / manifest を user-owned 手順本文の代替にする handoff laundering

Hook で止められない低価値作業は、本ファイルの checklist で防ぐ。
