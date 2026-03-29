# CLAUDE.md — NLMYTGen プロジェクト方針
# このファイルはプロジェクトの方針・技術スタック・成功定義を定める。
# 運用ルールは .claude/CLAUDE.md を参照。入口は AGENTS.md を参照。

## プロジェクト概要
NotebookLM の transcript を YMM4 用 CSV に変換し、動画を制作するための CLI パイプライン。

## 技術スタック
- Python
- uv（パッケージ管理・タスクランナー）
- pytest（テスト）
- YMM4（動画レンダリング — 外部ツール）

## 成功定義
1. 任意の NLM transcript を入力し、YMM4 が読み込める CSV を出力できる
2. その CSV を YMM4 に読み込ませ、動画をレンダリングできる
3. 複数の NLM transcript で再現性がある

## 現在の優先順位
1. 別の NLM transcript でのロバスト性検証
2. YMM4 実読込の確認
3. 最小動画1本の完成
4. （後回し）Web UI / API / YouTube 連携

## スコープ外（現時点）
- Web UI
- API サーバー
- YouTube 自動アップロード
- 他プロジェクト（HoloSync / NLMandSlideVideoGenerator 等）との連携
