"""pytest 共有フック（高速デフォルトスイート用）。"""

from __future__ import annotations

import os
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


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


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """ローカル証跡を分類し、通常の integration 短縮規則も維持する。"""
    for item in items:
        marker = item.get_closest_marker("requires_local_evidence")
        if marker is None:
            continue
        if not marker.args:
            raise pytest.UsageError(
                f"{item.nodeid}: requires_local_evidence needs an artifact class"
            )
        artifact_class = str(marker.args[0])
        locators = tuple(str(value) for value in marker.args[1:])
        if not locators:
            raise pytest.UsageError(
                f"{item.nodeid}: requires_local_evidence needs exact locators"
            )
        missing = [
            locator
            for locator in locators
            if not (REPO_ROOT / locator).exists()
        ]
        if missing:
            item.add_marker(
                pytest.mark.skip(
                    reason=(
                        f"requires_local_evidence:{artifact_class}:"
                        f"missing={','.join(missing)}"
                    )
                )
            )

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
