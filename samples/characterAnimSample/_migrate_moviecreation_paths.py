"""D:\\MovieCreationWorkspace\\... 参照を migrated_tachie 配下の相対パスへ寄せる（ワンオフ）。

元 ymmp が UTF-8 BOM のため、読み書きは utf-8-sig。
パーツ PNG はリポ内の reimu_easy.png を複製したプレースホルダ（見た目は本来素材と一致しない）。
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent
YMMP = BASE / "haitatsuin_2026-04-12.ymmp"
MIGRATED = BASE / "migrated_tachie"
SRC_PNG = BASE / "reimu_easy.png"

MARISA_PREFIX = r"D:\MovieCreationWorkspace\新まりさ"
REIMU_PREFIX = r"D:\MovieCreationWorkspace\新れいむ"

# ymmp 内で参照されていたパス（json.loads 後の Windows パス文字列）
NEEDED: list[tuple[str, str, str]] = [
    ("新まりさ", "他", "00b.png"),
    ("新まりさ", "他", "00o.png"),
    ("新まりさ", "体", "01.png"),
    ("新まりさ", "口", "00.png"),
    ("新まりさ", "目", "00.png"),
    ("新まりさ", "眉", "06c.png"),
    ("新まりさ", "髪", "00o.png"),
    ("新れいむ", "他", "00a.png"),
    ("新れいむ", "他", "00o.png"),
    ("新れいむ", "体", "00.png"),
    ("新れいむ", "口", "00.png"),
    ("新れいむ", "後", "00o.png"),
    ("新れいむ", "目", "00.png"),
    ("新れいむ", "眉", "05c.png"),
    ("新れいむ", "髪", "00o.png"),
]


def main() -> None:
    if not SRC_PNG.is_file():
        raise SystemExit(f"missing {SRC_PNG}")
    for ch, cat, name in NEEDED:
        dest = MIGRATED / ch / cat / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC_PNG, dest)

    data = json.loads(YMMP.read_text(encoding="utf-8-sig"))
    base_res = BASE.resolve()

    def migrate_str(s: str) -> str:
        if s.startswith(MARISA_PREFIX):
            tail = s[len(MARISA_PREFIX) :].lstrip("\\")
            parts = [p for p in tail.split("\\") if p] if tail else []
            tgt = (MIGRATED / "新まりさ").joinpath(*parts) if parts else (MIGRATED / "新まりさ")
            rel = tgt.resolve().relative_to(base_res)
            return str(rel).replace("/", "\\")
        if s.startswith(REIMU_PREFIX):
            tail = s[len(REIMU_PREFIX) :].lstrip("\\")
            parts = [p for p in tail.split("\\") if p] if tail else []
            tgt = (MIGRATED / "新れいむ").joinpath(*parts) if parts else (MIGRATED / "新れいむ")
            rel = tgt.resolve().relative_to(base_res)
            return str(rel).replace("/", "\\")
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

    walk(data)
    YMMP.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8-sig",
    )

    left: list[str] = []

    def collect(o: object) -> None:
        if isinstance(o, dict):
            for v in o.values():
                if isinstance(v, str) and "MovieCreationWorkspace" in v:
                    left.append(v)
                else:
                    collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)

    collect(data)
    print("MovieCreationWorkspace refs left:", len(left))
    if left:
        print("sample:", repr(left[0][:120]))


if __name__ == "__main__":
    main()
