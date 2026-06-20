#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if REPO_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null); then
  :
else
  REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)
fi

TARGET=""
for candidate in "docs/dashboard/index.html" "docs/dashboard.md"; do
  if [ -f "$REPO_ROOT/$candidate" ]; then
    TARGET="$REPO_ROOT/$candidate"
    break
  fi
done

if [ -z "$TARGET" ]; then
  echo "No dashboard file found. Expected docs/dashboard/index.html or docs/dashboard.md." >&2
  exit 1
fi

if [ "${1:-}" = "--print-path" ]; then
  printf '%s\n' "$TARGET"
  exit 0
fi

printf 'Opening NLMYTGen common foundation dashboard:\n  %s\n' "$TARGET"
printf 'If the browser does not open, rerun with --print-path and open the printed file directly.\n'

case "$(uname -s 2>/dev/null || printf unknown)" in
  Darwin*) open "$TARGET" ;;
  MINGW*|MSYS*|CYGWIN*) cmd.exe /c start "" "$TARGET" ;;
  *) xdg-open "$TARGET" >/dev/null 2>&1 || {
    printf 'Open this file manually: %s\n' "$TARGET" >&2
    exit 1
  } ;;
esac
