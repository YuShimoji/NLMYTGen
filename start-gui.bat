@echo off
setlocal
REM IMPORTANT: Keep this file Shift_JIS (CP932). UTF-8 or UTF-8-BOM breaks cmd.exe.
REM CP932: Japanese Windows cmd parses this script as Shift_JIS (no UTF-8 BOM).
chcp 932 >nul 2>&1
cd /d "%~dp0"

where node >nul 2>&1
if errorlevel 1 (
  echo [NLMYTGen] Node.js �� PATH �ɂ���܂���BLTS �� https://nodejs.org �������Ă���Ď��s���Ă��������B
  pause
  exit /b 1
)

where npx >nul 2>&1
if errorlevel 1 (
  echo [NLMYTGen] npx ���g���܂���BNode.js �� npm �����C���X�g�[�����m�F���Ă��������B
  pause
  exit /b 1
)

where uv >nul 2>&1
if not errorlevel 1 (
  echo [NLMYTGen] �ˑ��֌W�𓯊����Ă��܂��iuv sync�j...
  uv sync
  if errorlevel 1 (
    echo [NLMYTGen] uv sync �Ɏ��s���܂����B���|�W�g�������Ŏ蓮�m�F���Ă��������B
    pause
    exit /b 1
  )
) else (
  echo [NLMYTGen] ����: uv �� PATH �ɂ���܂���BGUI �� CSV/CLI �� uv �����ł͓����Ȃ��ꍇ������܂��B
)

cd /d "%~dp0gui"
echo [NLMYTGen] Electron ���N�����Ă��܂�...
npx --yes electron .
set ERR=%ERRORLEVEL%
if not "%ERR%"=="0" (
  echo [NLMYTGen] �I���R�[�h %ERR%
  pause
)
exit /b %ERR%
