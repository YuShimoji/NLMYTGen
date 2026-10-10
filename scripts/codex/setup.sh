#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.."

if [[ "$(uname -s)" != Linux ]]; then
  echo 'Cloud setup requires Linux; use the Windows commands in docs/CODEX_CLOUD.md locally.' >&2
  exit 2
fi
command -v uv >/dev/null || { echo 'Install uv before running Cloud setup.' >&2; exit 2; }
node -e 'if (Number(process.versions.node.split(".")[0]) < 22) throw new Error("Node.js 22 or newer is required")'

uv sync --locked --extra dev --python 3.11
npm ci --prefix gui --no-audit --no-fund
bash scripts/codex/check.sh
