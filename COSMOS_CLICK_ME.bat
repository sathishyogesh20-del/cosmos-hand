@echo off
title COSMOS — Auto Setup & Launch
color 0B
cls
echo.
echo  =====================================================
echo        COSMOS HAND CONTROLLER — AUTO SETUP
echo  =====================================================
echo.
echo  Setting everything up for you automatically...
echo  Please wait, do NOT close this window!
echo.

:: STEP 1: CHECK PYTHON
echo  [1/3] Checking Python...
python --version >nul 2>&1
if %errorlevel% == 0 goto :packages

echo        Python not found. Installing automatically...
winget --version >nul 2>&1
if %errorlevel% == 0 (
    winget install Python.Python.3.11 --accept-package-agreements --accept-source-agreements --silent
    goto :packages
)
powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile '%TEMP%\py_install.exe' -UseBasicParsing"
"%TEMP%\py_install.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
timeout /t 15 /nobreak >nul
for /f "tokens=*" %%a in ('powershell -Command "[System.Environment]::GetEnvironmentVariable(\"PATH\",\"User\")"') do set "PATH=%PATH%;%%a"

:packages
:: STEP 2: INSTALL PACKAGES
echo  [2/3] Installing required packages...
python -m pip install websockets pyautogui --quiet --upgrade
echo        Packages ready!

:: STEP 3: LAUNCH
echo  [3/3] Starting COSMOS...
echo.
color 0A
echo  =====================================================
echo   WHAT HAPPENS NEXT (automatic):
echo.
echo   1. Your browser will open automatically to:
echo      http://localhost:7860
echo.
echo   2. Click the "Connect" button on the page
echo.
echo   3. Your hand controls the ENTIRE PC!
echo  =====================================================
echo.
echo  Keep this window open while using COSMOS.
echo  Press Ctrl+C here to stop.
echo.
python cosmos_controller.py
pause
