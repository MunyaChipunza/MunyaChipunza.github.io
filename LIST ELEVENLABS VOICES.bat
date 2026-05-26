@echo off
setlocal

set "CLEAN_REPO=C:\Users\Dell\Projects\munya-publish"

if not exist "%CLEAN_REPO%\scripts\list_elevenlabs_voices.py" (
  echo Clean publishing repo not found: %CLEAN_REPO%
  pause
  exit /b 1
)

cd /d "%CLEAN_REPO%"
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 scripts\list_elevenlabs_voices.py
) else (
  python scripts\list_elevenlabs_voices.py
)

echo.
pause
