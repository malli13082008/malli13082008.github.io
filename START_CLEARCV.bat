@echo off
setlocal
cd /d "%~dp0"
title ClearCV - Smart Resume Analyzer

echo ==========================================
echo   ClearCV - Smart Resume Analyzer
echo ==========================================
echo.

if not exist "app.py" if exist "%~dp0ClearCV_Capstone\app.py" cd /d "%~dp0ClearCV_Capstone"

if not exist "app.py" (
  echo ERROR: app.py was not found.
  echo This launcher needs the full project folder beside it.
  echo Download and extract ClearCV_Capstone_Submission.zip, then open the
  echo ClearCV_Capstone folder and double-click START_CLEARCV.bat there.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating a private Python environment...
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3 -m venv .venv
  ) else (
    where python >nul 2>nul
    if errorlevel 1 (
      echo ERROR: Python 3 was not found. Install Python 3.10 or newer from python.org,
      echo enable "Add python.exe to PATH", and run this file again.
      pause
      exit /b 1
    )
    python -m venv .venv
  )
  if errorlevel 1 (
    echo ERROR: Could not create the Python environment.
    pause
    exit /b 1
  )
)

echo Installing or checking required packages...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo ERROR: Package installation failed. Check your internet connection and try again.
  pause
  exit /b 1
)

set "PORT=8000"
set "SECRET_KEY=local-clearcv-development-key"
set "RESUME_ANALYZER_DATA=%LOCALAPPDATA%\ClearCV\data"
if not exist "%RESUME_ANALYZER_DATA%" mkdir "%RESUME_ANALYZER_DATA%"

echo.
echo Keep this window open while using the website.
echo Wait until Flask prints "Running on http://127.0.0.1:8000", then open that address in Chrome or Edge.
echo Press Ctrl+C in this window to stop the website.
echo.
".venv\Scripts\python.exe" app.py
echo.
echo ClearCV has stopped.
pause
