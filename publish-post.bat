@echo off
setlocal

set "BUTTON_FOLDER=%~dp0"
set "CLEAN_REPO=C:\Users\Dell\Projects\munya-publish"
set "DRAFT_FILE=%BUTTON_FOLDER%PASTE NEW POST IN HERE.txt"
set "LOCAL_TEMPLATE=%BUTTON_FOLDER%NEW-POST-TEMPLATE.txt"
set "BUNDLED_PYTHON=C:\Users\Dell\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

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
  echo Paste your post into that file, save it, then double-click DOUBLE CLICK TO ACTIVATE NEW POST.bat again.
  start notepad "%DRAFT_FILE%"
  pause
  exit /b 1
)

cd /d "%CLEAN_REPO%"

git switch main
if not "%ERRORLEVEL%"=="0" (
  echo Could not switch the clean publishing repo to main.
  pause
  exit /b 1
)

git pull --ff-only origin main
if not "%ERRORLEVEL%"=="0" (
  echo Could not update the clean publishing repo from GitHub.
  pause
  exit /b 1
)

if exist "%BUNDLED_PYTHON%" (
  "%BUNDLED_PYTHON%" scripts\publish_post.py --draft "%DRAFT_FILE%"
) else (
  where py >nul 2>nul
  if %ERRORLEVEL%==0 (
    py -3 scripts\publish_post.py --draft "%DRAFT_FILE%"
  ) else (
    where python >nul 2>nul
    if %ERRORLEVEL%==0 (
      python scripts\publish_post.py --draft "%DRAFT_FILE%"
    ) else (
      echo Python was not found.
      echo Expected bundled Python at:
      echo %BUNDLED_PYTHON%
      pause
      exit /b 1
    )
  )
)

set RESULT=%ERRORLEVEL%
echo.
if not "%RESULT%"=="0" (
  echo Publishing failed. The draft was left in PASTE NEW POST IN HERE.txt so it can be retried.
  pause
  exit /b %RESULT%
)

echo Publishing complete.
pause
