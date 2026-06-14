@echo off
title COSMOS Hand Controller
color 0B
echo.
echo  ============================================
echo   COSMOS HAND CONTROLLER - PC CONTROL MODE
echo  ============================================
echo.
echo  Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Python not found!
    echo  Please install Python from https://python.org
    echo  IMPORTANT: Check "Add Python to PATH" during install
    echo.
    pause
    exit
)
echo  Python found!
echo.
echo  Installing/updating required packages...
pip install websockets pyautogui --quiet --upgrade
echo  Packages ready!
echo.
echo  ============================================
echo   Starting COSMOS Controller on port 8765
echo  ============================================
echo.
echo  NEXT STEPS:
echo  1. Open your COSMOS app in the browser
echo  2. Click the "Connect" button at the top
echo  3. Your hand now controls this PC!
echo.
echo  SAFETY: Move mouse to TOP-LEFT corner of
echo  screen anytime to instantly stop control.
echo.
echo  Press Ctrl+C here to stop the controller.
echo  ============================================
echo.
python cosmos_controller.py
pause
