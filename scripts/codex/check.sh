#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.."
project_python="${NLMYTGEN_PYTHON:-.venv/bin/python}"
export PYTHONUTF8=1
if [[ ! -x "$project_python" ]]; then
  echo 'Python environment is missing. Run bash scripts/codex/setup.sh first.' >&2
  exit 2
fi

"$project_python" -B -m src.cli.main --help >/dev/null
"$project_python" -B -m pytest \
  tests/test_ir_validate.py \
  tests/test_linebreak_forbidden.py \
  tests/test_notebooklm_input_contract.py \
  tests/test_portable_review_bundle.py
node --check gui/main.js
node --test gui/batch_observability.test.js
git diff --check
echo 'NLMYTGen Cloud development checks passed (CLI, fixture tests, GUI logic).'
