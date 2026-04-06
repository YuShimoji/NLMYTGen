# B-18 dry proof — AI監視 sample（台本機械診断）

## 目的

[samples/AI監視が追い詰める生身の労働.txt](../samples/AI監視が追い詰める生身の労働.txt) に対し `diagnose-script` を実行し、repo-local で再現可能な診断出力を記録する。

## コマンド

```bash
uv run python -m src.cli.main diagnose-script "samples/AI監視が追い詰める生身の労働.txt" \
  --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" \
  --format json
```

（Windows PowerShell でも同様。パスはリポジトリ root 相対で可。）

## 観測結果（要約）

- **utterance_count**: 28（`normalize` 後の発話数）。
- **診断コード**（2026-04-06 実行時）:
  - `EXPLAINER_ROLE_MISMATCH`（warning）: 文量・導入パターン上 `analyze_speaker_roles` が host と判定した話者が、マップ後「れいむ」であり、既定の `--expected-explainer`（まりさ）と不一致。
  - `LISTENER_ROLE_MISMATCH`（warning）: guest 推定が「まりさ」だが `--expected-listener`（れいむ）と不一致。

## 解釈

サンプルでは **スピーカー1（→ れいむ）** に長い解説が多く、**スピーカー2（→ まりさ）** にも長めの説明行が混在する。ゆっくりの「れいむ＝聞き手／まりさ＝解説」という期待と、NLM 出力の話者割当が一致していない典型例として、機械診断が警告を返す。

次のアクションは [S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md)（C-09）による constrained rewrite、または `--speaker-map` の見直し。

## 備考

- 実動画レンダリングや YMM4 は本 proof の対象外（[INVARIANTS.md](../INVARIANTS.md) の proof 方針に準拠）。
- 端末のコードページによって JSON をコンソールに直表示した際に文字化けする場合がある。ファイルリダイレクト（`> out.json`）または GUI の「台本診断」で UTF-8 表示を使う。
