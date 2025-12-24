@echo off & setlocal

::
:: HelloGUI - PyInstaller Build Script
::
:: Builds a standalone Windows executable (.exe) for HelloGUI using PyInstaller.
::
:: The resulting executable will be in the dist/ folder and can be distributed
:: to users without requiring Python installation.
::
:: Usage:
::   build_exe.bat
::

echo.
echo ============================================================
echo HelloGUI - Building Executable
echo ============================================================
echo.

:: Check if venv exists
if not exist .venv (
    echo ERROR: Virtual environment not found.
    echo Please run quick_start.bat first.
    pause
    exit /b 1
)

:: Activate venv
call ".venv\Scripts\activate.bat"

:: Check if PyInstaller is installed
pip list | findstr /i "pyinstaller" >nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install -q pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller.
        pause
        exit /b 1
    )
)

:: Create build directory if needed
if not exist build mkdir build
if not exist dist mkdir dist

echo.
echo Building executable with PyInstaller...
echo This may take a minute...
echo.

:: Run PyInstaller
pyinstaller --noconfirm ^
    --name HelloGUI ^
    --windowed ^
    --onefile ^
    --icon=src/hello_gui/resources/icons/app.ico ^
    src/hello_gui/app.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed. See output above for details.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Build successful!
echo ============================================================
echo.
echo Executable created: dist\HelloGUI.exe
echo.
echo You can now distribute HelloGUI.exe to other Windows users.
echo No Python installation required on target machines.
echo.

pause
exit /b 0
