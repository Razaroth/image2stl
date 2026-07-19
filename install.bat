@echo off
REM Auto-install script for Image2STL dependencies
REM This script sets up a virtual environment and installs all required packages

echo ========================================
echo Image2STL - Dependency Auto-Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Check if virtual environment already exists
if exist ".venv\" (
    echo Virtual environment already exists.
    echo Activating virtual environment...
) else (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Warning: Failed to upgrade pip, continuing anyway...
)

echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Virtual environment is located in: .venv\
echo.
echo To activate the environment in the future, run:
echo   .venv\Scripts\activate.bat
echo.
echo To run the GUI app:
echo   python gui.py
echo.
echo To run the CLI:
echo   python -m src.cli.main --help
echo.
echo.
pause
