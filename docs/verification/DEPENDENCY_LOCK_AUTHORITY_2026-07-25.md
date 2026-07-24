# Dependency Lock Authority Verification — 2026-07-25 JST

Scope: `portable-dependency-lock-authority-v1`

Required base:
`c9c5f4bd50b86edd72cd3dc92254dc7ea02bee7e`

Outcome commit: resolve from the tip of
`origin/codex/nlmytgen-portable-dependency-lock-authority-v1`.

## Result

`DEPENDENCY_LOCKS_LOCAL_ONLY` is resolved. The existing valid local lockfiles
were preserved byte-for-byte, removed from ignore rules, added to tracked Git
authority, and proven in an isolated tracked-only Windows checkout.

| Authority | SHA-256 | Result |
| --- | --- | --- |
| `uv.lock` | `40e64f793775f0b0181f5ba8972c17842717dbe14bc8c0a6c0cabd14442435d0` | tracked, public PyPI only, unchanged after setup |
| `gui/package-lock.json` | `81b060f37fd2c7c4151fcf6fc402b554476d4ea6785022c8eef01aaaa9ff4a73` | tracked, public npm HTTPS only, unchanged after setup |
| `pyproject.toml` | `7b9ce97035187e00e396c50aa5d79862fce06c0404cc272435f93136b1efd51d` | byte-exact to required base |
| `gui/package.json` | `a180ad8bbbba3a28e72576181259510bb42e119dd920f8995056936ffab251a2` | byte-exact to required base |

The npm manifest range remains `^35.0.0`; the lock and clean install resolve
Electron exactly 35.7.5. No dependency upgrade or manifest normalization was
performed.

## Tracked-only setup proof

The staged candidate tree was materialized without `.git`, source `.venv`,
source `gui/node_modules`, ignored media, browser profiles, YMM4 projects, or
private run outputs.

Commands:

```powershell
uv sync --extra dev --locked
uv run python -c "import pytest; import src.cli.main"
npm --prefix gui ci
npm --prefix gui ls --depth=0
node -p "require('./gui/node_modules/electron/package.json').version"
```

Results:

- Python 3.13.3 isolated `.venv`: created successfully.
- pytest 8.4.2 and `src.cli.main`: import smoke passed.
- npm clean install: 70 packages installed from the tracked lock.
- npm readback: only direct `electron@35.7.5`.
- Electron readback: `35.7.5`.
- Both lock hashes matched before and after install.
- The short-path verification workspace was removed.

The first attempt used a longer OS TEMP path and hit Win32 filename-length
limits while materializing existing deep tracked paths. Its partial workspace
was removed. Repeating the same tracked-only proof at `C:\nla1` passed. This was
a temporary checkout path constraint, not a dependency graph failure.

## Focused regression contract

`tests/test_dependency_lock_authority.py` contains seven checks:

- both locks exist, are tracked, and are not ignored;
- both protected manifests remain byte-exact;
- `uv.lock` has no private or machine-local dependency source;
- npm root dependency authority matches `gui/package.json`;
- Electron resolves exactly to 35.7.5;
- npm sources are public HTTPS without credentials or local references;
- README uses locked setup commands and accepted-cut authority hashes remain
  unchanged.

The focused suite passed before commit. After the outcome commit, the exact
commit is materialized and the Python/npm proof is repeated before push.
Canonical Regression Integrity is also run once against the committed tracked
set and must retain 0 failures / 0 errors, a valid declared-locator skip
contract, Git three-surface integrity, and temporary workspace cleanup.

## Changed and preserved boundaries

Changed:

- `.gitignore`
- `README.md`
- `uv.lock`
- `gui/package-lock.json`
- `tests/test_dependency_lock_authority.py`
- compact state, handoff, and this verification report

Preserved:

- `pyproject.toml` and `gui/package.json`
- Electron 35.7.5
- accepted MP4, generated project, receipts, script, media, YMM4, visual,
  timing, subtitle, rights, and publication state
- pre-existing untracked `.playwright-mcp/`, `artifacts/`, and
  `phase-e-01-contact-acquired*.png`
- ignored `.venv/`, `gui/node_modules/`, private media, browser profiles, and
  run archives

Electron's known direct high-severity audit finding remains successor debt.
Tracking the lockfile does not resolve it. Electron 43 was not installed or
tested. YMM4, render, GUI/window launch, audio/video playback, public-media
access, rights, production, publication, PR, merge, and master mutation were
not performed.
