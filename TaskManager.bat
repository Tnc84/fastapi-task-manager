@echo off
title Task Manager - Desktop App
color 0A

echo ================================================
echo    Task Manager - Desktop Application
echo ================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.11+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

python --version
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found.
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check if requirements are installed
echo Checking dependencies...
pip show pywebview >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Launch the application
echo Starting Task Manager...
echo.
python launch_desktop.py

REM Cleanup
echo.
echo Application closed.
pause

