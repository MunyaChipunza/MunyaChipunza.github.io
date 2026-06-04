@echo off
setlocal

set "CLEAN_REPO=C:\Users\Dell\Projects\munya-publish"
set "GOOGLE_DRIVE_TARGET=G:\My Drive\100. Zee\Munyachipunza.com"

if not exist "%CLEAN_REPO%\scripts\generate_audio.py" (
  echo Clean publishing repo not found: %CLEAN_REPO%
  pause
  exit /b 1
)

echo This will use ElevenLabs credits for every post that does not already have audio.
choice /M "Continue"
if errorlevel 2 exit /b 0

cd /d "%CLEAN_REPO%"

if "%ELEVENLABS_API_KEY%"=="" (
  for /f "tokens=2,*" %%A in ('reg query HKCU\Environment /v ELEVENLABS_API_KEY 2^>nul') do set "ELEVENLABS_API_KEY=%%B"
)
if "%ELEVENLABS_VOICE_ID%"=="" (
  for /f "tokens=2,*" %%A in ('reg query HKCU\Environment /v ELEVENLABS_VOICE_ID 2^>nul') do set "ELEVENLABS_VOICE_ID=%%B"
)

git switch main
if not "%ERRORLEVEL%"=="0" (
  echo Could not switch to main.
  pause
  exit /b 1
)

git pull --ff-only origin main
if not "%ERRORLEVEL%"=="0" (
  echo Could not update from GitHub.
  pause
  exit /b 1
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 scripts\generate_audio.py --missing
  if not "%ERRORLEVEL%"=="0" goto failed
  py -3 scripts\generate_writing.py
  if not "%ERRORLEVEL%"=="0" goto failed
) else (
  python scripts\generate_audio.py --missing
  if not "%ERRORLEVEL%"=="0" goto failed
  python scripts\generate_writing.py
  if not "%ERRORLEVEL%"=="0" goto failed
)

git status --porcelain > "%TEMP%\munya-audio-status.txt"
for %%A in ("%TEMP%\munya-audio-status.txt") do if %%~zA==0 (
  echo No new audio changes to publish.
  del "%TEMP%\munya-audio-status.txt" >nul 2>nul
  pause
  exit /b 0
)
del "%TEMP%\munya-audio-status.txt" >nul 2>nul

git add --all
git commit -m "Add post audio files"
if not "%ERRORLEVEL%"=="0" goto failed

git push origin main
if not "%ERRORLEVEL%"=="0" goto failed

if exist "%GOOGLE_DRIVE_TARGET%" (
  robocopy "%CLEAN_REPO%" "%GOOGLE_DRIVE_TARGET%" /MIR /XJ /XD .git __pycache__ reports /XF *.log *.pyc /R:2 /W:2 /NFL /NDL /NP
  if errorlevel 8 goto failed
)

echo Audio files published. GitHub Pages may take a minute to refresh.
pause
exit /b 0

:failed
echo Audio publishing failed. Check the message above.
pause
exit /b 1
