@echo off
setlocal

set "CLEAN_REPO=C:\Users\Dell\Projects\munya-publish"

if not exist "%CLEAN_REPO%\scripts\list_elevenlabs_voices.py" (
  echo Clean publishing repo not found: %CLEAN_REPO%
  pause
  exit /b 1
)

echo This saves your ElevenLabs API key and voice ID on this PC only.
echo The key is not added to the website or committed to GitHub.
echo.
set /p ELEVENLABS_API_KEY=Paste your ElevenLabs API key: 
if "%ELEVENLABS_API_KEY%"=="" (
  echo No API key entered.
  pause
  exit /b 1
)

setx ELEVENLABS_API_KEY "%ELEVENLABS_API_KEY%" >nul
cd /d "%CLEAN_REPO%"

echo.
echo Voices on your ElevenLabs account:
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 scripts\list_elevenlabs_voices.py
) else (
  python scripts\list_elevenlabs_voices.py
)

echo.
set /p ELEVENLABS_VOICE_ID=Paste the voice_id for your cloned voice: 
if "%ELEVENLABS_VOICE_ID%"=="" (
  echo No voice ID entered.
  pause
  exit /b 1
)

setx ELEVENLABS_VOICE_ID "%ELEVENLABS_VOICE_ID%" >nul
echo.
echo ElevenLabs audio is set up. Future double-click posts will generate audio automatically.
echo If this window was already open before setup, close and reopen it before generating audio manually.
pause
