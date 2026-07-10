from __future__ import annotations

import importlib.util
import json
from io import StringIO
from pathlib import Path


HOOK_PATH = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "guardrails.py"


def _load_guardrails():
    spec = importlib.util.spec_from_file_location("nlmytgen_guardrails", HOOK_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_main(monkeypatch, payload: dict[str, object]) -> int:
    guardrails = _load_guardrails()
    monkeypatch.setattr(guardrails.sys, "stdin", StringIO(json.dumps(payload)))
    return guardrails.main()


def test_collect_strings_ignores_hook_metadata_paths() -> None:
    guardrails = _load_guardrails()
    payload = {
        "hook_event_name": "Stop",
        "transcript_path": "C:/Users/name/.claude/projects/HoloSync/log.jsonl",
        "last_assistant_message": "NLMYTGen の作業結果です。",
    }

    assert guardrails._collect_strings(payload) == ["NLMYTGen の作業結果です。"]


def test_guardrails_reject_repo_external_reference_without_scope(
    monkeypatch, capsys
) -> None:
    code = _run_main(
        monkeypatch,
        {
            "hook_event_name": "Stop",
            "last_assistant_message": "Open C:/work/HoloSync/docs/runtime-state.md",
        },
    )

    assert code == 2
    assert "repo-external reference" in capsys.readouterr().err


def test_guardrails_reject_external_reference_mixed_with_repo_local_path(
    monkeypatch,
) -> None:
    code = _run_main(
        monkeypatch,
        {
            "hook_event_name": "Stop",
            "last_assistant_message": (
                "Compared C:/Users/PLANNER007/NLMYTGen/README.md with "
                "C:/work/VastCore/README.md."
            ),
        },
    )

    assert code == 2


def test_guardrails_allow_explicit_cross_project_scope(monkeypatch) -> None:
    code = _run_main(
        monkeypatch,
        {
            "hook_event_name": "Stop",
            "last_assistant_message": (
                "The user explicitly requested cross-project cleanup in "
                "C:/work/HoloSync/docs/runtime-state.md."
            ),
        },
    )

    assert code == 0


def test_guardrails_do_not_lint_response_quality(monkeypatch) -> None:
    code = _run_main(
        monkeypatch,
        {
            "hook_event_name": "Stop",
            "last_assistant_message": (
                "判断をお願いします。YMM4で確認してください。背景茶番劇の素材が不足。"
            ),
        },
    )

    assert code == 0


def test_guardrails_ignore_non_response_events(monkeypatch) -> None:
    code = _run_main(
        monkeypatch,
        {
            "hook_event_name": "PreToolUse",
            "message": "C:/work/NarrativeGen/README.md",
        },
    )

    assert code == 0


def test_guardrails_tolerate_invalid_json(monkeypatch) -> None:
    guardrails = _load_guardrails()
    monkeypatch.setattr(guardrails.sys, "stdin", StringIO("not-json"))

    assert guardrails.main() == 0
