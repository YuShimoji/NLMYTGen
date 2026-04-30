# User Request Ledger
# ユーザーの継続要望・差分要求・backlog を保持する台帳。

このファイルは現在も判断に効く durable request だけを置く。履歴・時系列の詳細は [`project-context.md`](project-context.md) の DECISION LOG、機能 status は [`FEATURE_REGISTRY.md`](FEATURE_REGISTRY.md)、現在位置は [`runtime-state.md`](runtime-state.md) を正とする。

## 現在有効な要求

- 痛点ドリブンで進める。FEATURE_REGISTRY の候補一覧や done 件数から機械的に次タスクを選ばない。
- ハンドオフに全コンテキストが本当に残っているか検証し、抜け漏れは明示して報告する。
- 実際には未完了なのに完了扱いになっている task、文書だけ存在して実体が弱い項目、古い正本風ドキュメントを継続的に是正する。
- 通常再開の読了対象を増やさない。`AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → `docs/runtime-state.md` で止め、必要な該当節だけ読む。
- project-local canonical docs を先に確認し、既知文脈の再質問を避ける。
- `Prompt` / checklist / `OK` / `NG` / `PASS` / `FAIL` 返却テンプレを作業接続性より優先しない。人間に依頼する手順は、開く対象・作る対象・元 object・判定主体・返答の意味を先に明示する。
- `INTERACTION_NOTES.md` は反応ラベルのメモではなく、既知文脈の再質問・broad question・manual proof 押し戻し・価値経路 drift など、プロジェクトが前に進まない構造的 failure mode の予防策として維持する。
- 茶番劇 G-24 を user-only の配置作業と表現しない。既存 sample / GroupItem / layer / target labeling が揃う案件では、assistant が rough placement・effect 適用・registry 下準備を先行し、user は YMM4 上の意図確認と canonical template authoring に集中できるようにする。
- 手動作成済み YMM4 演出の `Remark` tag、座標、反転、拡大縮小、既存 `VideoEffects` から variation を自動生成できるかを、これ以上 docs-only で先送りしない。まず G-25 `probe-ymmp-variations` のような独立 review artifact で feasibility を見て、production placement への接続は結果を見て別スライスにする。
- G-25 のYMM4確認により、`nudge / scale / rotate / effect_reuse` のような property 差分は、動きのvariationとしては不採用。以後は、うなずき・退場・小ジャンプ・傾きなどを motion primitive として扱い、開始姿勢・終了姿勢・方向意味・reset policy・相性を機械可読化してから候補生成する。傾いたまま退場、傾いた小ジャンプ、反対方向の傾きなどの accidental composition を避ける。
- 手順票に従って人間が配置する作業を「制作自動化」と扱わない。G-24 の成果は、IR + registry + repo-tracked YMM4 template source から `.ymmp` timeline へ GroupItem が自動挿入されること。
- Python 生成へ戻らない。YMM4 を制作基盤とし、Python は CSV / IR / registry / 台本読込後 `.ymmp` patch の接着層に限定する。
- NotebookLM 出力は低信頼入力として扱う。誤字・誤変換・指示無視が後工程に組み込まれるため、CSV / IR 生成前に B-18 `diagnose-script` または C-09 / manual QC を挟む。
- face 関連は独立サブクエストとして閉じ、以後は failure class 単位でのみ再オープンする。
- サムネイルと packaging は、抽象煽りや固定テンプレ連打ではなく、本文根拠のある具体性・pattern rotation・タイトル/サムネ/台本の整合で扱う。
- 手動作業が重くならないよう調整する。微調整や時間計測より、接続成立・失敗分類・差分証跡を優先する。

## 未反映の是正要求

- `approved` は「仕様定義済み + ユーザー承認済み」のみ。priority / selection / status を混同しない。
- E-02 のような「テンプレート作成」という命題に引っ張られず、実際にどこへ入力され何が減るのかから価値検証する。
- NotebookLM / YMM4 / YouTube Studio の実 integration point を曖昧にしたまま仕様を進めない。
- 古い proof / proposal / prompt が正本っぽく見えても、`runtime-state.md` / `FEATURE_REGISTRY.md` / 該当 spec と矛盾する場合は降格・削除する。

## Backlog Delta

- 現行主軸は G-24（茶番劇 Group template-first 運用）であり、v1 planned set 5 件（`enter_from_left` / `surprise_oneshot` / `nod` / `deny_oneshot` / `exit_left`）は user-owned YMM4 author/export または sample proof + manual acceptance の段階で閉じた。repo-tracked placement source `samples/templates/skit_group/delivery_v1_templates.ymmp` は v1 planned set 5/5 同梱済み。`patch-ymmp --skit-group-only` による real estate DX placement は `samples/_probe/g24/real_estate_dx_skit_group_ir_aligned.json` を入力に CSV-imported `.ymmp` copy へ実行済みで、出力は `samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp`。ただしこれは raw clone transport/readback proof であり、user visual check では「置かれているが間隔が広すぎる」ため production acceptance ではない。次の接続点は、テンプレートを作り直すことではなく、template source から構造・基準位置・相対 motion・timing density を分析し、placement planner が normalized plan を生成して `.ymmp` へ再配置すること。`panic_shake` (index 104) は Part 2 JSON 語彙から除外して strict validation を維持する。本ファイルや他 canonical docs を更新するときは件数・取り込み有無・パス・raw clone と analyzed placement の区別を cross-audit し、`CANONICAL_FACT_DRIFT` / `TEMPLATE_ANALYSIS_BYPASS` を再発させない。
- G-24 は「user が全テンプレート/全サンプルを作る」運用ではない。user は少数の reusable motion template を YMM4 native template として author/export し、assistant はそれらを template analyzer / placement planner / registry resolver で production-like `.ymmp` placement へ生成・整理し、user は最終的な意図確認と creative acceptance に集中する。
- 汚染パッチ由来の `rejected` / `hold` を目的ごとの拒否として読まない。旧 `--emit-meta`、Python 画像生成、YMM4 GUI 万能制御、YMM4 表示エミュレーション等は `method-rejected` だが、診断 JSON / IR / manifest / H-01 brief / H-02 thumbnail slot patch / G-24 template placement / metadata draft successor は `goal-allowed` として扱う。
- 外部分析で提案された `Visual Return Contract` は、方向性としては採用する。ただし現時点では新しい broad feature ではなく、既存の route-specific return path（G-24 registry/template source/readback、thumbnail `thumb.*` readback、`build-session-manifest` acceptance slots）で扱う。`delivery_nod_v1` はすでに superseded / direct_proven なので再オープンしない。汎用 `visual_return_manifest` は、G-24 と thumbnail など複数 route で同じ戻り値項目が反復してから、FEATURE_REGISTRY の下位タスクとして起票する。
- G-21 / G-22 は現行主軸ではない。必要時のみ補助経路として再開し、通常 backlog に戻さない。
- 汚染バッチ由来の D-02 / F-01 / F-02 は、個別再審査まで通常 backlog に戻さない。
- S-5 字幕はみ出しは B-15/B-16/B-17 で解決済み。drift が見えたときだけ残差観測として扱う。
- メンテ層は B-18（台本診断）→ H-01/H-02（packaging / thumbnail on demand）→ B-17（drift-only）の順で、主軸を押し流さない範囲で起動する。
