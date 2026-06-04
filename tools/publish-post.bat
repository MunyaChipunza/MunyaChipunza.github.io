@echo off
setlocal EnableExtensions

set "TOOLS_FOLDER=%~dp0"
for %%I in ("%TOOLS_FOLDER%..") do set "SITE_ROOT=%%~fI"
set "CLEAN_REPO=C:\Users\Dell\Projects\munya-publish"
set "REPO_URL=https://github.com/MunyaChipunza/MunyaChipunza.github.io.git"
set "DRAFT_FILE=%SITE_ROOT%\PASTE NEW POST IN HERE.txt"
set "LOCAL_TEMPLATE=%SITE_ROOT%\docs\NEW-POST-TEMPLATE.txt"
set "BUNDLED_PYTHON=C:\Users\Dell\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
set "LOG_DIR=%SITE_ROOT%\reports"
set "LOG_FILE=%LOG_DIR%\last-publish-run.log"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%" >nul 2>nul
echo MunyaChipunza.com publish run started at %DATE% %TIME% > "%LOG_FILE%"
echo Site folder: %SITE_ROOT%>> "%LOG_FILE%"
echo Draft file: %DRAFT_FILE%>> "%LOG_FILE%"
echo Clean repo: %CLEAN_REPO%>> "%LOG_FILE%"
echo.>> "%LOG_FILE%"

echo MunyaChipunza.com publisher
echo Draft: %DRAFT_FILE%
echo Log: %LOG_FILE%
echo.

where git >nul 2>nul
if not "%ERRORLEVEL%"=="0" (
  echo Git was not found. Install Git for Windows, then try again.
  echo Git was not found.>> "%LOG_FILE%"
  goto fail
)

if not exist "%CLEAN_REPO%\.git" (
  echo Clean publishing repo missing. Cloning it now...
  echo Clean publishing repo missing. Cloning from %REPO_URL%.>> "%LOG_FILE%"
  if not exist "C:\Users\Dell\Projects" mkdir "C:\Users\Dell\Projects" >nul 2>nul
  git clone "%REPO_URL%" "%CLEAN_REPO%" >> "%LOG_FILE%" 2>&1
  if not "%ERRORLEVEL%"=="0" (
    echo Could not clone the clean publishing repo.
    goto fail
  )
)

if not exist "%CLEAN_REPO%\scripts\publish_post.py" (
  echo Clean publishing repo is present but missing scripts\publish_post.py.
  echo Clean publishing repo is present but missing scripts\publish_post.py.>> "%LOG_FILE%"
  goto fail
)

if not exist "%DRAFT_FILE%" (
  if exist "%LOCAL_TEMPLATE%" (
    copy "%LOCAL_TEMPLATE%" "%DRAFT_FILE%" >nul
  ) else (
    copy "%CLEAN_REPO%\docs\NEW-POST-TEMPLATE.txt" "%DRAFT_FILE%" >nul
  )
  echo Created %DRAFT_FILE%.
  echo Paste your post into that file, save it, then double-click the root DOUBLE CLICK TO ACTIVATE NEW POST.bat again.
  start notepad "%DRAFT_FILE%"
  goto fail
)

cd /d "%CLEAN_REPO%"

git switch main
if not "%ERRORLEVEL%"=="0" (
  echo Could not switch the clean publishing repo to main.
  echo Could not switch the clean publishing repo to main.>> "%LOG_FILE%"
  goto fail
)

git pull --ff-only origin main >> "%LOG_FILE%" 2>&1
if not "%ERRORLEVEL%"=="0" (
  echo Could not update the clean publishing repo from GitHub.
  goto fail
)

if exist "%BUNDLED_PYTHON%" (
  echo Publishing now. This can take a few minutes while GitHub Pages deploys and subscribers are notified.
  "%BUNDLED_PYTHON%" scripts\publish_post.py --draft "%DRAFT_FILE%" >> "%LOG_FILE%" 2>&1
) else (
  where py >nul 2>nul
  if %ERRORLEVEL%==0 (
    py -3 scripts\publish_post.py --draft "%DRAFT_FILE%" >> "%LOG_FILE%" 2>&1
  ) else (
    where python >nul 2>nul
    if %ERRORLEVEL%==0 (
      python scripts\publish_post.py --draft "%DRAFT_FILE%" >> "%LOG_FILE%" 2>&1
    ) else (
      echo Python was not found.
      echo Expected bundled Python at:
      echo %BUNDLED_PYTHON%
      echo Python was not found.>> "%LOG_FILE%"
      goto fail
    )
  )
)

set RESULT=%ERRORLEVEL%
echo.
if not "%RESULT%"=="0" (
  echo Publishing failed. The draft was left in PASTE NEW POST IN HERE.txt so it can be retried.
  echo Publishing failed with exit code %RESULT%.>> "%LOG_FILE%"
  echo See the log: %LOG_FILE%
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Content -LiteralPath '%LOG_FILE%' -Tail 80"
  if not "%MUNYA_NO_PAUSE%"=="1" pause
  exit /b %RESULT%
)

echo Publishing complete.
echo Publishing complete.>> "%LOG_FILE%"
if not "%MUNYA_NO_PAUSE%"=="1" pause
exit /b 0

:fail
echo.
echo Publishing setup failed. See the log: %LOG_FILE%
if not "%MUNYA_NO_PAUSE%"=="1" pause
exit /b 1
