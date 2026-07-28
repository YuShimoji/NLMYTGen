@echo off
setlocal
REM ASCII-only. Optional: Shift_JIS if you add non-ASCII messages for cmd.exe.
chcp 932 >nul 2>&1
cd /d "%~dp0"

where node >nul 2>&1
if errorlevel 1 (
  echo [NLMYTGen] Node.js is not in PATH. Install from https://nodejs.org and retry.
  pause
  exit /b 1
)

where npm >nul 2>&1
if errorlevel 1 (
  echo [NLMYTGen] npm not found. Reinstall Node.js with npm.
  pause
  exit /b 1
)

where uv >nul 2>&1
if errorlevel 1 goto UvMissing

if defined NLMYTGEN_FORCE_UV_SYNC goto RunUvSync
if exist "%~dp0.venv\Scripts\python.exe" goto UvSkipped

:RunUvSync
echo [NLMYTGen] uv sync...
uv sync --locked
if errorlevel 1 (
  echo [NLMYTGen] uv sync failed. Check repo root.
  pause
  exit /b 1
)
goto UvAfter

:UvSkipped
goto UvAfter

:UvMissing
echo [NLMYTGen] WARN: uv not in PATH. GUI needs uv for CSV/CLI.

:UvAfter

cd /d "%~dp0gui"
if not exist "package.json" (
  echo [NLMYTGen] gui\package.json not found.
  pause
  exit /b 1
)

if not exist "node_modules\.bin\electron.cmd" (
  echo [NLMYTGen] npm ci...
  call npm ci --no-audit --no-fund
  if errorlevel 1 (
    echo [NLMYTGen] npm ci failed. Check gui\package-lock.json.
    pause
    exit /b 1
  )
)
call node_modules\.bin\electron.cmd .
if errorlevel 1 (
  echo [NLMYTGen] Electron exited with error.
  pause
  exit /b 1
)
exit /b 0
