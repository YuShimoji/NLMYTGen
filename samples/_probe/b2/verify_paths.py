import json, re, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
data = json.loads(open('samples/characterAnimSample/haitatsuin_2026-04-12.ymmp', encoding='utf-8-sig').read())
pat = re.compile(r'(Mat|migrated_tachie|[\u65b0][\u307e\u308c]).*\.png')
seen = set()
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and len(v) < 300 and pat.search(v):
                seen.add(v)
            elif not isinstance(v, str):
                walk(v)
    elif isinstance(o, list):
        for x in o: walk(x)
walk(data)
missing = 0
base = pathlib.Path('samples/characterAnimSample')
for p in sorted(seen):
    rel = p.replace(chr(92), '/')
    resolved = (base / rel).resolve()
    ok = resolved.exists()
    if not ok:
        missing += 1
    print(f"{'OK' if ok else 'MISS'}  {p}")
print(f"Total: {len(seen)}, Missing: {missing}")
