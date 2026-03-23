# ADR-0001: Single Path A

## Status
Accepted

## Context
旧プロジェクト (NLMandSlideVideoGenerator) では、Path A (NotebookLM → CSV → YMM4) と
Path B (Python + MoviePy + Voicevox → 直接動画生成) が共存していた。
Path B の撤去に 10+ revert cycles を要し、コードの密結合が設計全体を不安定にした。

## Decision
v2 では Path A のみを実装する。代替パイプラインは作らない。

パイプラインは 1 本:
```
NotebookLM transcript → Python (parse/normalize/assemble) → YMM4 CSV
```

## Consequences
- 直接動画生成 (MoviePy, ffmpeg, Voicevox) のコードを含めない
- 「将来 Path B を追加する」ための抽象化レイヤーを設けない
- 別パイプラインが必要になった場合は、新しい ADR を起草してから判断する
