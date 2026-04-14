# B-11 オペレータ向けハンズオン & 推奨開発プランの下準備

この文書は次の2つをまとめた正本です。

1. **あなた（オペレータ）が手で行う B-11 実測**の手順（YMM4 取込後まで）
2. **そのあと推奨開発プランを書き直す／更新する**ときに揃えておく材料と記入先

関連: [workflow-proof-template.md](../workflow-proof-template.md)（テンプレ正本）、[B11-manual-checkpoints.md](../B11-manual-checkpoints.md)（確認タイミング）、[B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md)（ゲート判定の要約）。

---

## Part A — B-11 ハンズオン（AI監視サンプルで完走する）

### A-0. 目的を一言で

**同じトランスクリプトについて**、「CLI が出した取込前の数字・警告」と「YMM4 で直した量（4 区分）」を **1 つの Markdown に残す**。それが B-11 の workflow proof です。

今回の記録ファイル（既に取込前まで記入済み）:

- [`B11-workflow-proof-ai-monitoring-labor.md`](B11-workflow-proof-ai-monitoring-labor.md)

取込用 CSV（リポジトリに同梱済みの想定）:

- `samples/AI監視が追い詰める生身の労働_B11_ymm4.csv`

### A-1. 事前確認（5 分）

| 確認項目 | 内容 |
|----------|------|
| 環境 | リポジトリ root で `uv run python -m src.cli.main --help` が動く |
| YMM4 | 台本読み込み用プロジェクト／テンプレが開ける |
| 話者名 | 台本側は `れいむ` / `まりさ`（CSV の1列目）。YMM4 のキャラに **同名で割り当てるか**、テンプレの名前に合わせて **speaker-map 付きで CSV を出し直す** |

CSV を出し直す必要がある場合（例: テンプレのキャラ名が違う）は、**PowerShell** では次のように **1 行**で実行できます（`スピーカー1=…` の右辺をテンプレに合わせて変える）。

```powershell
cd C:\Users\PLANNER007\NLMYTGen
uv run python -m src.cli.main build-csv "samples/AI監視が追い詰める生身の労働.txt" -o "samples/AI監視が追い詰める生身の労働_B11_ymm4.csv" --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" --max-lines 2 --chars-per-line 40 --reflow-v2 --stats --format json
```

- 標準出力の `--- Stats ---` と `[WARN]` 行は、記録ファイルの **§1** と矛盾しないかだけ見れば足ります（既に貼ってある内容と同型でよい）。
- **Dry-run だけ**にしたい場合は `-o` の代わりに `--dry-run` を付け、本番用 CSV は上記の `-o` 付きで再実行する。

### A-2. YMM4 で取り込む（10 分）

1. YMM4 で対象プロジェクトを開く。
2. **台本読み込み**（メニュー名は YMM4 版により異なる）で、`samples/AI監視が追い詰める生身の労働_B11_ymm4.csv` を指定する。
3. インポート後、**話者（キャラ）割当**で `れいむ` / `まりさ` が意図した立ち絵に付いているか確認する（[B11-manual-checkpoints.md](../B11-manual-checkpoints.md) §2 参照）。

### A-3. 通し確認しながら「4 区分」を数える（20〜40 分）

タイムラインの先頭から最後まで **読み上げ＋字幕**を見る（実レンダリングまで必須ではないが、**字幕の見た目と読み**が分かる状態にする）。

次の4つに、**手で直した回数**を分類して数える。1 箇所が複数に当てはまる場合は、**主な理由で1つに寄せる**（迷ったらメモ欄に補足）。

| 区分 | 何を数えるか |
|------|----------------|
| **辞書登録** | 読みがおかしく、YMM4 の辞書（単語登録）で直した |
| **手動改行** | 字幕の改行位置を手で動かした（見た目の折り返し調整） |
| **再分割したい長文** | 1 字幕が長すぎる／話の切れ目とズレているので、**CSV を作り直す・行を分けたい**と感じた（いま直せなくても「あとで分割したい」はここ） |
| **タイミングのみ** | テキストや改行はそのままで、表示タイミングや長さ調整だけした |

**コツ**

- 直したら、その場で **CSV 行番号**（何行目か）と **一言メモ**をメモ帳に残す。後で `B11-workflow-proof-ai-monitoring-labor.md` の「代表例」に貼る。
- CLI が `[WARN] row 22` のように出していた行は、**優先的に**見る（取込前の機械警告と取込後の手修正がつながる）。

### A-4. 記録ファイルに書き込む（10 分）

[`B11-workflow-proof-ai-monitoring-labor.md`](B11-workflow-proof-ai-monitoring-labor.md) を開き、次を埋める。

1. **§2.1** の表に、上で数えた **件数**と短い **メモ**。
2. **§2.2** に代表例を **3〜5 件**（`row 22: …` の形式が望ましい）。
3. **§2.3 判断メモ**に、次のテンプレをそのまま使ってよい。

```text
- 判定: Gate A / Gate B / Gate C のいずれか（[B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md) の Gate 定義に従う）
- 根拠: （4 区分のどれが支配的だったか、1〜2 文）
- 次に触れそうなレイヤー: L2 改行ルール / 運用・GUI 導線 / S-5 辞書・読み（いずれかまたは併記）
```

### A-5. 完了の自己チェック

- [ ] §1（取込前）と §2（取込後）が **同じファイル**にある
- [ ] 4 区分すべてに **数字（0 でも可）**が入っている
- [ ] 代表例が **3 件以上**ある
- [ ] §2.3 に **Gate 名**が書いてある

ここまでできれば、**プラン策定直前**の B-11 条件は満たせます。

---

## Part B — 推奨開発プラン作成のための下準備

B-11 は「字幕・S-5 の手戻りがまだ支配的か」を測るゲートです。推奨プランの正本は常に [`runtime-state.md`](../runtime-state.md) の **「次以降の推奨プラン」** です。プランを見直す／更新する前に、次の **入力セット**をそろえると文章化が速くなります。

### B-1. 必須入力（B-11 完了後に手元に置く）

| 入力 | 入手元 | プランでの使い方 |
|------|--------|------------------|
| 4 区分の件数 | B-11 記録 §2.1 | F-01/F-02 再開要否、L2 投資の優先度 |
| Gate 判定（A/B/C） | B-11 記録 §2.3 | 次四半期の「主戦場」を一文で固定 |
| overflow 警告と実修正の対応 | §1 の WARN 行と §2.2 | 機械警告の当たり率・誤警報の有無 |

### B-2. 既存ロードマップとの接続（コピペ用チェックリスト）

`runtime-state.md` の §優先順位 (正本) と突き合わせるときの目安:

- **Phase 1 Block-A (メンテ層・台本品質の継続観測)**
  - 手順: [`P01-phase1-operator-e2e-proof.md`](P01-phase1-operator-e2e-proof.md)
  - B-11 との関係: Block-A の **YMM4 読込〜** のあとに発生した S-5 負荷を、**同じ台本または別台本**の B-11 で言語化できると、運用改善の効果説明がしやすい。
- **メンテ: H-01 Packaging brief 運用**
  - B-11 とは独立だが、「台本が安定してから packaging の drift 観測」と並行するか整理する。
- **主軸: 演出配置自動化の実戦投入**
  - B-11 が Gate B（運用摩擦）なら、**コードより runbook・registry** 先、など順序を文章で明示できる。
- **据え置き (motion ブランチ・歴史)**
  - [`P2A-motion-branch-operator-decision.md`](P2A-motion-branch-operator-decision.md) に従い、B-11 結果だけで motion を動かさない（必要なら「字幕が例外処理化してから」と書く）。

### B-3. プラン更新時に触るファイル（担当がエンジニア側の場合）

| ファイル | 何を書くか |
|----------|------------|
| [`runtime-state.md`](../runtime-state.md) | 「次以降の推奨プラン」表の行追加・順序変更、`next_action` 1 行 |
| [`OPERATOR_WORKFLOW.md`](../OPERATOR_WORKFLOW.md) | B-11 の判断ゲートに **日付付きで 1 行**（観測サマリ）を足す場合がある |
| [`FEATURE_REGISTRY.md`](../FEATURE_REGISTRY.md) | F-01/F-02 を動かすなら **承認フロー**（台帳更新）を先に。B-11 記録へのリンクを DECISION の根拠にできる |
| [`project-context.md`](../project-context.md) | DECISION LOG に「プラン順序変更」と理由を1行 |

### B-4. P01 表への追記テンプレ（運用 1 本終えたあと）

[`P01-phase1-operator-e2e-proof.md`](P01-phase1-operator-e2e-proof.md) 末尾の「記録」表に、例えば次のように足す。

```markdown
| YYYY-MM-DD | （台本パス） | はい/いいえ | 前___分 / 後___分 | B-11: Gate ___、手動改行___件、再分割___件。メモ: … |
```

### B-5. 「推奨開発プラン」ドラフトのアウトライン（貼ってから埋める）

企画メモ用。最終は `runtime-state.md` に反映する。

1. **前提**: B-11 Gate は A/B/C のどれか（根拠は §2.1 の数字）。
2. **今期の主目標（1 行）**: 例「Phase 1 Block-A を 1 本完走し P01 に実測行を残す」。
3. **やらないこと（1 行）**: 例「F-01/F-02 は B-11 で Gate B 確定まで未承認のまま」。
4. **次の検証単位**: 例「次の新台本 1 本で B-11 をもう 1 回」か「同一台本で Block-A 完走後に B-11 再測定」か。

---

## 関連リンク（再掲）

- [B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md) — いま埋めるべき記録
- [B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md) — Gate A/B/C の短い定義
- [runtime-state.md](../runtime-state.md) — 推奨プラン正本
- [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) — Phase 1 本番の手順と記録表
