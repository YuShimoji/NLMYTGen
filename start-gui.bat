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

where npx >nul 2>&1
if errorlevel 1 (
  echo [NLMYTGen] npx not found. Reinstall Node.js with npm.
  pause
  exit /b 1
)

where uv >nul 2>&1
if errorlevel 1 goto UvMissing

if defined NLMYTGEN_FORCE_UV_SYNC goto RunUvSync
if exist "%~dp0.venv\Scripts\python.exe" goto UvSkipped

:RunUvSync
echo [NLMYTGen] uv sync...
uv sync
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

REM Local electron is fast; npx resolves each time (slower). One-time: cd gui ^&^& npm install
if exist "node_modules\.bin\electron.cmd" (
  call node_modules\.bin\electron.cmd .
) else (
  npx --yes electron .
)
if errorlevel 1 (
  echo [NLMYTGen] Electron exited with error.
  pause
  exit /b 1
)
exit /b 0
