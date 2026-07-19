@echo off
REM Image2STL Application Launcher for Windows
REM Double-click this file to launch the GUI application

echo.
echo ========================================
echo   Image2STL Application Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found
    echo You may need to install dependencies with: pip install -r requirements.txt
)

REM Run the application
python run.py
pause
