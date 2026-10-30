@echo off
setlocal
title ALBUS 2.0 - GitHub Uploader
cd /d "%~dp0"

echo.
echo ==========================================
echo        ALBUS 2.0 GitHub Uploader
echo ==========================================
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo Git is not installed.
  echo.
  echo Please install GitHub Desktop from:
  echo https://desktop.github.com/
  echo Then put this BAT file inside your ALBUS folder and run it again.
  start https://desktop.github.com/
  pause
  exit /b 1
)

where gh >nul 2>&1
if errorlevel 1 (
  echo GitHub CLI is not installed. Installing it with Windows Package Manager...
  winget install --id GitHub.cli --source winget
  if errorlevel 1 (
    echo Automatic installation failed.
    echo Install GitHub CLI from https://cli.github.com/
    start https://cli.github.com/
    pause
    exit /b 1
  )
  echo.
  echo GitHub CLI was installed. CLOSE this window and run this BAT again.
  pause
  exit /b 0
)

gh auth status >nul 2>&1
if errorlevel 1 (
  echo.
  echo GitHub sign-in will start now.
  echo Follow the prompts and sign in to HuffleCraft09.
  echo.
  gh auth login -h github.com -p https -w
  if errorlevel 1 (
    echo Sign-in was not completed.
    pause
    exit /b 1
  )
)

echo.
echo Preparing repository...
if not exist ".git" git init
git branch -M main
git remote remove origin >nul 2>&1
git remote add origin https://github.com/HuffleCraft09/ALBUS-2.0.git

echo .env> .gitignore
echo .venv/>> .gitignore
echo __pycache__/>> .gitignore
echo *.pyc>> .gitignore

echo.
echo Uploading ALBUS 2.0...
git add .
git commit -m "Upload ALBUS 2.0 Windows Cloud iPhone build" >nul 2>&1
git push -u origin main

if errorlevel 1 (
  echo.
  echo UPLOAD FAILED.
  echo Send me a screenshot of this window.
  pause
  exit /b 1
)

echo.
echo ==========================================
echo   ALBUS 2.0 UPLOADED SUCCESSFULLY
echo ==========================================
echo.
echo https://github.com/HuffleCraft09/ALBUS-2.0
echo.
pause
