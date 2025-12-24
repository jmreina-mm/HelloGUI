# HelloGUI - Quick Start Script for Windows PowerShell
#
# This script sets up the Python environment and runs HelloGUI for the first time.
#
# Usage:
#   .\scripts\quick_start.ps1

Write-Host ""
Write-Host "============================================================"
Write-Host "HelloGUI - Quick Start"
Write-Host "============================================================"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found Python: $pythonVersion"
}
catch {
    Write-Host "ERROR: Python is not installed or not in PATH."
    Write-Host "Please install Python 3.11+ from https://www.python.org/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 1: Create virtual environment
Write-Host "Step 1: Creating virtual environment..."
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists."
}
else {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment."
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "Virtual environment created successfully."
}

Write-Host ""

# Step 2: Activate virtual environment
Write-Host "Step 2: Activating virtual environment..."
& ".\.venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment."
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Virtual environment activated."

Write-Host ""

# Step 3: Install dependencies
Write-Host "Step 3: Installing dependencies..."
pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install requirements."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Installing HelloGUI package..."
pip install -q -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install HelloGUI package."
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Dependencies installed successfully."

Write-Host ""

# Step 4: Run the application
Write-Host "Step 4: Launching HelloGUI..."
Write-Host ""
$env:PYTHONPATH = "src"
python -m hello_gui.app

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Application failed to start."
    Read-Host "Press Enter to exit"
    exit 1
}

exit 0
