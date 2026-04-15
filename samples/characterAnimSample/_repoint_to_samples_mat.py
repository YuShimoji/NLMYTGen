"""立ち絵参照を migrated_tachie/ → ../Mat/ (samples/Mat/) に書き換える。

migrated_tachie/ 配下は reimu_easy.png の placeholder クローン (2026-04-13 migration の副作用)。
samples/Mat/ には実パーツが既に存在 (2026-04-14 追加、e22bf75)。
本スクリプトは haitatsuin ymmp のパーツパスを samples/Mat/ へ向け直す (復旧 B)。

元 ymmp が UTF-8 BOM のため、読み書きは utf-8-sig。
"""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent  # samples/characterAnimSample
YMMP = BASE / "haitatsuin_2026-04-12.ymmp"
OLD_PREFIX = "migrated_tachie"
NEW_REL = r"..\Mat"  # from characterAnimSample/ → ../Mat


def migrate_str(s: str) -> str:
    # migrated_tachie\新まりさ\... → ..\Mat\新まりさ\...
    if s.startswith(OLD_PREFIX + "\\"):
        tail = s[len(OLD_PREFIX) :]  # e.g. \新まりさ\他\00b.png
        return NEW_REL + tail
    return s


def walk(o: object) -> None:
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if isinstance(v, str):
                o[k] = migrate_str(v)
            else:
                walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


def main() -> None:
    data = json.loads(YMMP.read_text(encoding="utf-8-sig"))
    walk(data)
    YMMP.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8-sig",
    )

    left: list[str] = []

    def collect(o: object) -> None:
        if isinstance(o, dict):
            for v in o.values():
                if isinstance(v, str) and OLD_PREFIX in v:
                    left.append(v)
                else:
                    collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)

    collect(data)
    print(f"migrated_tachie refs left: {len(left)}")
    if left:
        print("sample:", repr(left[0][:200]))


if __name__ == "__main__":
    main()
