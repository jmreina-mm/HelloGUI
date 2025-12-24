@echo off & setlocal

::
:: HelloGUI - Quick Start Script for Windows
::
:: This script sets up the Python environment and runs HelloGUI for the first time.
::
:: Usage:
::   quick_start.bat
::

echo.
echo ============================================================
echo HelloGUI - Quick Start
echo ============================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

:: Step 1: Create virtual environment
echo Step 1: Creating virtual environment...
if exist .venv (
    echo Virtual environment already exists.
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
)

echo.

:: Step 2: Activate virtual environment
echo Step 2: Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo Virtual environment activated.

echo.

:: Step 3: Install dependencies
echo Step 3: Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo Dependencies installed successfully.

echo.

:: Step 4: Run the application
echo Step 4: Launching HelloGUI...
echo.
python -m src.hello_gui.app

if errorlevel 1 (
    echo ERROR: Application failed to start.
    pause
    exit /b 1
)

exit /b 0
