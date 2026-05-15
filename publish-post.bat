@echo off
setlocal
cd /d "%~dp0"

if not exist "new-post.txt" (
  copy "NEW-POST-TEMPLATE.txt" "new-post.txt" >nul
  echo Created new-post.txt.
  echo Paste your post into new-post.txt, save it, then double-click publish-post.bat again.
  start notepad "new-post.txt"
  pause
  exit /b 1
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 scripts\publish_post.py
) else (
  python scripts\publish_post.py
)

set RESULT=%ERRORLEVEL%
echo.
if not "%RESULT%"=="0" (
  echo Publishing failed. The draft was left in new-post.txt so it can be retried.
  pause
  exit /b %RESULT%
)

echo Publishing complete.
pause
