# P2 READY 入力テンプレ（分岐C）

目的: 分岐C（ハイブリッド）で `P2` を **OPEN → READY** に昇格できるかを、最小入力で判定する。

---

## 1. 記録フォーマット（1 件 2 行）

```text
- YMM4見え方: OK|NG - <一言メモ>
- S6§2(5条件): 充足|未充足 - <不足項目 or 根拠リンク>
```

---

## 2. 記入例

```text
- YMM4見え方: OK - test_verify_4_bg.ymmp で背景アニメの破綻なし
- S6§2(5条件): 未充足 - PoC合格条件の機械判定ログ未添付
```

---

## 3. 記録先（統一）

- 正本は [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) の **P2/S6 観測** 行を更新する。
- 詳細メモが必要な場合のみ、本ファイル末尾に追記し、チェックリストからリンクする。

---

## 4. 判定ルール

- 2 行とも埋まっている:
  - `YMM4見え方=OK` かつ `S6§2(5条件)=充足` → **READY**
  - それ以外 → **OPEN 継続**
- 空欄がある場合は自動的に **OPEN 継続**。

## 4.1 再判定手順（YMM4 実測後）

1. `YMM4見え方` の 1 行目だけを `OK|NG` の実測値で更新する（2 行目は維持）。
2. 2 行目 `S6§2(5条件)` の状態を再確認する（`充足|未充足`）。
3. 以下の判定表で `READY` または `OPEN 継続` を確定する。
4. 判定結果を [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) の P2/S6 行へ反映する。

### 判定表

| YMM4見え方 | S6§2(5条件) | 判定 |
|---|---|---|
| OK | 充足 | READY |
| OK | 未充足 | OPEN 継続 |
| NG | 充足 | OPEN 継続 |
| NG | 未充足 | OPEN 継続 |

### 追記テンプレ（判定結果）

```text
判定: READY（OK + 5条件充足）
```

```text
判定: OPEN 継続（理由: <OK未達 or 5条件未充足>）
```

---

## 5. 変更履歴

- 2026-04-10: §6 を最新状態へ同期。条件4/5は充足済み、OPEN理由は YMM4 実測待ちの1点に統一。
- 2026-04-10: 初版。分岐Cの READY 入力テンプレを追加。

---

## 6. 入力ログ（2026-04-10）

- YMM4見え方: NG - 未実施（環境制約: この端末では YMM4 リソース非共有）。
- S6§2(5条件): 充足 - 条件4/5の根拠は `docs/verification/P2-CONDITION45-PRECHECK-TEMPLATE.md` に記録。OPEN理由は YMM4 実測待ち。
- 補足（ymmp 変化有無）:
  - `samples/test_verify_4_bg.ymmp`（2026-04-05 追加）以降、更新コミットなし。
  - `samples/test_verify_4_bg_p2_small_v3.ymmp`（2026-04-08 追加）以降、更新コミットなし。
  - `samples/test_verify_4_bg_p2_expand_clean.ymmp`（2026-04-08 追加）以降、更新コミットなし。
  - 現在ワークツリーでも `.ymmp` 未コミット差分なし。
- 判定: READY 条件 `OK + 5条件充足` を未達のため **OPEN 継続**。

### OPEN理由の単一化（運用固定）

- 条件4（機械判定ログ）: 充足（`P2-CONDITION45-PRECHECK-TEMPLATE.md` の 2026-04-10 実績）
- 条件5（既存運用接続点）: 充足（同ファイル §2 の接続点記録）
- よって現在の **OPEN理由は `YMM4見え方` 実測待ちの1点のみ**。
- 再判定時は 1 行目だけを更新し、2 行目は根拠リンクを維持する。
