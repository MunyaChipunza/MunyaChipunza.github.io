@echo off
setlocal

set "BUTTON_FOLDER=%~dp0"
set "CLEAN_REPO=C:\Users\Dell\Projects\munya-publish"
set "DRAFT_FILE=%BUTTON_FOLDER%new-post.txt"
set "LOCAL_TEMPLATE=%BUTTON_FOLDER%NEW-POST-TEMPLATE.txt"

if not exist "%CLEAN_REPO%\scripts\publish_post.py" (
  echo Clean publishing repo not found: %CLEAN_REPO%
  echo The site publisher needs that folder to commit and deploy safely.
  pause
  exit /b 1
)

if not exist "%DRAFT_FILE%" (
  if exist "%LOCAL_TEMPLATE%" (
    copy "%LOCAL_TEMPLATE%" "%DRAFT_FILE%" >nul
  ) else (
    copy "%CLEAN_REPO%\NEW-POST-TEMPLATE.txt" "%DRAFT_FILE%" >nul
  )
  echo Created %DRAFT_FILE%.
  echo Paste your post into that file, save it, then double-click publish-post.bat again.
  start notepad "%DRAFT_FILE%"
  pause
  exit /b 1
)

cd /d "%CLEAN_REPO%"

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 scripts\publish_post.py --draft "%DRAFT_FILE%"
) else (
  python scripts\publish_post.py --draft "%DRAFT_FILE%"
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
