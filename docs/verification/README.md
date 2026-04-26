# docs/verification — 証跡ディレクトリの読み方

このディレクトリは **検証記録・提案ドラフト・実装メモ・オペレータ proof** の置き場であり、現在位置や次アクションの正本ではない。

## 先に読むもの

通常再開ではここを読まない。まず次の 3 点で止める。

1. [`AGENTS.md`](../../AGENTS.md)
2. [`docs/REPO_LOCAL_RULES.md`](../REPO_LOCAL_RULES.md)
3. [`docs/runtime-state.md`](../runtime-state.md)

特定の検証記録が必要になった場合だけ、このディレクトリの該当ファイルを開く。

## 判断の優先順位

- 現在位置・次アクション: [`runtime-state.md`](../runtime-state.md)
- 機能 status: [`FEATURE_REGISTRY.md`](../FEATURE_REGISTRY.md)
- 仕様: 該当する `docs/*_SPEC.md` / `docs/*_MATRIX.md`
- 意思決定・handoff: [`project-context.md`](../project-context.md) の該当節だけ

`verification/` 配下の古い proof / proposal / checklist が上記と違う場合、上記を優先する。

## ファイル種別

- `*-proof.md`: 実行・観測結果。再実行や受け入れ判断の根拠として読む。
- `*-proposal.md` / `*-draft-*`: 採用前の案。現行仕様へ吸収済みなら判断材料にしない。
- `*-implementation.md` / `*-patch-design.md`: 実装当時の記録。コード・台帳と矛盾する場合は履歴扱い。
- `*-checklist.md`: オペレータ手順。現行 `runtime-state.md` の次アクションと接続する場合だけ使う。

## アーカイブ方針

- 明示 stale / archived / superseded / 削除可で、現行 docs へ吸収済みの文書は削除対象。
- 履歴証跡として残す場合は、先頭注記で「現行判断ではない」ことと参照すべき現行 docs を示す。
- 背景アニメ/S6 など旧軸の記録は、現行 G-24 `delivery_nod_v1` gate の判断に混ぜない。
