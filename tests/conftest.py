"""pytest 共有フック（高速デフォルトスイート用）。"""

from __future__ import annotations

import os

import pytest


def _truthy_env(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


def _invocation_has_path_or_file(args: tuple[str, ...]) -> bool:
    """CLI でテストパス・ファイルが指定されたか（その場合はフィルタを掛けない）。"""
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("-"):
            # -m / --marker / --ignore などはパスとみなさない
            if a in ("-m", "--marker", "-k", "--pyargs"):
                i += 2
                continue
            if "=" in a and a.split("=", 1)[0] in ("-m", "--marker", "-k"):
                i += 1
                continue
            if a.startswith("@"):  # pytest @file.txt
                return True
            i += 1
            continue
        return True
    return False


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """デフォルトでは integration マークをスキップし、日次のループを短縮する。

    全件: 環境変数 NLMYTGEN_PYTEST_FULL=1 を付与する。
    特定ファイル・ディレクトリを指定した場合は常にフィルタしない。
    -m が指定されている場合もフィルタしない（マーカー式に委ねる）。
    """
    if _truthy_env("NLMYTGEN_PYTEST_FULL"):
        return

    markexpr = (config.getoption("markexpr", default="") or "").strip()
    if markexpr:
        return

    argv = tuple(str(a) for a in config.invocation_params.args)
    if _invocation_has_path_or_file(argv):
        return

    skip_integration = pytest.mark.skip(
        reason="integration（全件は NLMYTGEN_PYTEST_FULL=1 またはテストパスを明示）"
    )
    for item in items:
        if item.get_closest_marker("integration"):
            item.add_marker(skip_integration)
