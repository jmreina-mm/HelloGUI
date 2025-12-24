@echo off & setlocal

::
:: HelloGUI - Test Runner Script
::
:: Runs the pytest test suite for HelloGUI.
::
:: Usage:
::   run_tests.bat
::

echo.
echo ============================================================
echo HelloGUI - Running Tests
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

:: Run tests
echo Running pytest...
echo.
pytest tests/ -v

if errorlevel 1 (
    echo.
    echo Tests failed. See output above for details.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo All tests passed!
echo ============================================================
echo.

exit /b 0
