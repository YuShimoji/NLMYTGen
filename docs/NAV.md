# NAV.md — ドキュメント地図（迷子対策）

**役割**: 再開時に「まずどれを読むか」を 1 ファイルに圧縮する。仕様の正本や長い運用ルールは **ここに複製しない**（リンク先を正とする）。

---

## 1. 再開の 3 枚（最短）

1. [AGENTS.md](../AGENTS.md) — 入口・境界・再アンカリング手順の正本
2. [REPO_LOCAL_RULES.md](REPO_LOCAL_RULES.md) — Hard Rules・Read Order の正本
3. [runtime-state.md](runtime-state.md) — 現在位置・`next_action`・カウンターの正本

フル再アンカリングは `AGENTS.md` のステップ 1〜5 どおり。省略しない。

---

## 2. 正本マップ（仕様・台帳・検証索引）

`docs/verification` 直下の個別ファイルが多いときは、先に次の **索引表**だけ読む。

- [verification/README.md](verification/README.md) — **現行正本**一覧（FEATURE_REGISTRY・IR 仕様・runtime-state・ファイル10 等への誘導）

---

## 3. 並行作業・Prompt・検収

- [OPERATOR_PARALLEL_WORK_RUNBOOK.md](OPERATOR_PARALLEL_WORK_RUNBOOK.md) — オペレータ並行（ファイル4）
- [verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md](verification/CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md) — **ファイル10**: コピペ用 Prompt 全文・検収・親チャット返却テンプレ
- [verification/CORE-DEV-POST-DELEGATION-INDEX.md](verification/CORE-DEV-POST-DELEGATION-INDEX.md) — コア移譲後ドキュメントの索引（ファイル2〜）
- [verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md) — 立ち絵 複数体×顔差し替え（**G-19/G-20 `proposed`**・別スレッド用 Prompt 同梱）
- [verification/CORE-LANE-PARALLEL-PROMPT-PACK.md](verification/CORE-LANE-PARALLEL-PROMPT-PACK.md) — 即実行 Prompt の運用原則・早見（ファイル9）。全文はファイル10を先に更新する運用

---

## 4. テンプレと状態（混同しやすい点）

次の節は **消えない依頼文（コピペ用テンプレ）**であり、タスク完了と連動して削除・打ち消し線には **しない**。

- [verification/CORE-LANE-PARALLEL-PROMPT-PACK.md](verification/CORE-LANE-PARALLEL-PROMPT-PACK.md) §3（即実行 Prompt）
- [verification/VISUAL-QUALITY-PACKETS.md](verification/VISUAL-QUALITY-PACKETS.md) §4（パケット別の短文 Prompt）

**いまどこまで終わっているか**は、次を見る。

- [runtime-state.md](runtime-state.md) の `next_action` / `parallel_replan_*`
- [verification/CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](verification/CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)（ファイル2）の PASS / 継続
- 案件ごとの `*-proof.md` や verification 配下の JSON 証跡

---

## 5. 航海日誌（任意・長大）

- [project-context.md](project-context.md) — DECISION LOG・HANDOFF。**IDE の Markdown プレビューが空白になることがある**場合はエディタのソース表示で開く（`AGENTS.md` 注記どおり）。
