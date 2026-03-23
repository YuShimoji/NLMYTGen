# ADR-0003: No Direct Video Generation in v1

## Status
Accepted

## Context
旧プロジェクトでは Python + MoviePy + Voicevox で直接動画を完成まで持っていく Path B が存在した。
YMM4 が提供する音声合成・動画レンダリング・字幕配置を Python で再実装する形になっており、
品質面でも開発効率面でも車輪の再発明だった。

## Decision
v1 では Python による直接動画生成を行わない。

禁止対象:
- MoviePy
- ffmpeg (動画合成目的)
- Voicevox / 任意の TTS
- PIL / Pillow によるスライド生成
- 独自動画レンダリングエンジン

Python の出力は CSV ファイルまで。音声合成・動画レンダリングは YMM4 の責務。

## Consequences
- 動画の完成には YMM4 での手動操作が必要 (意図的な設計)
- Python の依存関係が最小限に保たれる
- 動画品質は YMM4 の機能に依存する
- 将来 Python 側で動画生成が必要になった場合は、新しい ADR を起草してから判断する
