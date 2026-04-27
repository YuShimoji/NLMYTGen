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

- 現行主軸は G-24（茶番劇 Group template-first 運用）であり、v1 planned set 5 件（`enter_from_left` / `surprise_oneshot` / `nod` / `deny_oneshot` / `exit_left`）は user-owned YMM4 author/export または sample proof + manual acceptance により閉じた。次の接続点は実制作 IR の template 解決が S-6（背景・演出設定）の選択負荷を減らすかの確認。新しい動きは production gap が出た時だけ再起票する。
- G-24 は「user が全テンプレート/全サンプルを作る」運用ではない。user は少数の reusable motion template を YMM4 native template として author/export し、assistant はそれらの組み合わせ・registry・ノウハウから production-like sample / exact-fallback-manual note を生成・整理し、user が結果を確認する。
- G-21 / G-22 は現行主軸ではない。必要時のみ補助経路として再開し、通常 backlog に戻さない。
- 汚染バッチ由来の D-02 / F-01 / F-02 は、個別再審査まで通常 backlog に戻さない。
- S-5 字幕はみ出しは B-15/B-16/B-17 で解決済み。drift が見えたときだけ残差観測として扱う。
- メンテ層は B-18（台本診断）→ H-01/H-02（packaging / thumbnail on demand）→ B-17（drift-only）の順で、主軸を押し流さない範囲で起動する。
