# HelloGUI - How To Guide

Complete step-by-step instructions from repository download through first run.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Repository Setup](#repository-setup)
3. [First Run (Quickest Way)](#first-run-quickest-way)
4. [Manual Setup (If Quick Start Fails)](#manual-setup-if-quick-start-fails)
5. [Running Tests](#running-tests)
6. [Building Standalone Executable](#building-standalone-executable)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

### Windows
- **Python 3.11+**: Download from [python.org](https://www.python.org/downloads/)
  - ✅ Check "Add Python to PATH" during installation
  - Verify: Open PowerShell and run `python --version`

### macOS / Linux
- **Python 3.11+**: Install via homebrew or package manager
  - Verify: `python3 --version`
- **Git** (optional, if cloning from repository)

---

## Repository Setup

### Option 1: Download ZIP (Windows)
1. Download the HelloGUI repository as ZIP
2. Extract to desired location (e.g., `C:\Projects\HelloGUI`)
3. Note the full path

### Option 2: Clone with Git (All Platforms)
```bash
git clone <repository-url> HelloGUI
cd HelloGUI
```

---

## First Run (Quickest Way)

### Windows with PowerShell (Recommended)
```powershell
# Navigate to project directory
cd C:\Path\To\HelloGUI

# Run PowerShell quick start script
.\scripts\quick_start.ps1
```

**What this does:**
- Creates virtual environment (`.venv/`)
- Installs dependencies from `requirements.txt`
- Installs HelloGUI package in editable mode
- Launches the application

### Windows with Batch (Alternative)
```bash
cd C:\Path\To\HelloGUI
.\scripts\quick_start.bat
```

### macOS / Linux
```bash
cd ~/path/to/HelloGUI
bash scripts/quick_start.sh  # (if available) or follow manual setup below
```

---

## Manual Setup (If Quick Start Fails)

If the quick start scripts fail or you prefer manual control, follow these steps:

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv .venv

# macOS / Linux
python3 -m venv .venv
```

### Step 2: Activate Virtual Environment
```bash
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat

# macOS / Linux (Bash/Zsh)
source .venv/bin/activate
```

After activation, your prompt should show `(.venv)` prefix.

### Step 3: Upgrade pip (Recommended)
```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

Expected output: "Successfully installed PySide6, matplotlib, numpy, pytest, pyinstaller..."

### Step 5: Install HelloGUI Package
```bash
pip install -e .
```

This installs HelloGUI in "editable mode," allowing changes to be reflected immediately.

### Step 6: Run the Application

#### PowerShell / Bash
```bash
python -m hello_gui.app
```

#### OR with explicit PYTHONPATH (if above fails)
```bash
# Windows PowerShell
$env:PYTHONPATH="src"; python -m hello_gui.app

# Windows CMD
set PYTHONPATH=src && python -m hello_gui.app

# macOS / Linux Bash
PYTHONPATH=src python -m hello_gui.app
```

#### Expected Result
A window should appear titled **"HelloGUI - Python Data Stream Visualization"** with:
- **Dashboard tab** (selected): Plot area, controls, status bar
- **Config tab**: Waveform and parameter settings

---

## Using HelloGUI

### Dashboard Tab
1. **Click Resume** to start the data stream
2. Watch the plot update in real-time
3. Adjust axis labels in the text fields
4. **Click Pause** to stop without clearing data
5. **Click Save Data** to save current dataset to CSV
6. **Click Load Data** to load previously saved CSV

### Config Tab
1. Select waveform type: Sine, Square, or Random Walk
2. Adjust parameters:
   - **Amplitude**: Peak height (0.01 to 100)
   - **Frequency**: Oscillations per unit (0 to 10 Hz)
   - **Noise**: Random variation (0 to 1)
   - **X-Step**: Sampling interval (0.001 to 1)
   - **Max Points**: Buffer size (10 to 100,000)
3. **Click Apply** to activate changes
4. **Click Reset Defaults** to restore factory settings

### Save/Load Workflow
```
1. Enter file path: output/my_experiment.csv
2. Click Save Data
3. CSV created with columns: x, y
4. Later: Enter same path and click Load Data
5. Previous data loaded and plotted
```

---

## Running Tests

### Quick Test Run
```bash
# Activate venv first (see Step 2 above)
pytest tests/ -v
```

### Expected Output
```
collected 23 items

tests/test_data_stream.py::TestSineWave::test_sine_at_zero PASSED        [  4%]
tests/test_data_stream.py::TestSineWave::test_sine_at_quarter_period PASSED [  8%]
...
tests/test_io_manager.py::TestReadCsv::test_roundtrip PASSED            [100%]

======================== 23 passed in 10.07s =========================
```

### Run Specific Test
```bash
# Test only CSV I/O
pytest tests/test_io_manager.py -v

# Test only data stream
pytest tests/test_data_stream.py -v

# Run single test function
pytest tests/test_data_stream.py::TestSineWave::test_sine_at_zero -v
```

### Or Use Batch Script (Windows)
```bash
scripts\run_tests.bat
```

---

## Building Standalone Executable

Convert HelloGUI to a standalone `.exe` for distribution (Windows only).

### One-Click Build
```bash
scripts\build_exe.bat
```

### Manual Build
```bash
# Activate venv
.venv\Scripts\activate.bat  # Windows

# Install PyInstaller (if not already installed)
pip install pyinstaller

# Build executable
pyinstaller --noconfirm \
    --name HelloGUI \
    --windowed \
    --onefile \
    src/hello_gui/app.py
```

### Result
- **Location**: `dist/HelloGUI.exe`
- **Size**: ~200 MB (includes all dependencies)
- **Distribution**: Copy `HelloGUI.exe` to any Windows computer
  - ✅ No Python installation required
  - ✅ No dependencies needed
  - ✅ Ready to run

### Run Executable
```bash
# From PowerShell / CMD
.\dist\HelloGUI.exe

# Or double-click the file in Explorer
```

---

## Troubleshooting

### Issue: "Python is not installed or not recognized"

**Cause**: Python not in system PATH

**Solution**:
1. Uninstall Python
2. Reinstall from [python.org](https://www.python.org/)
3. ✅ **Important**: Check "Add Python to PATH" during installation
4. Restart terminal/PowerShell
5. Verify: `python --version`

---

### Issue: "Virtual environment activation fails"

**Cause**: Path contains spaces or special characters

**Solution** (Windows PowerShell):
```powershell
# Use dot-sourcing syntax
. ".\.venv\Scripts\Activate.ps1"
```

**Solution** (Windows CMD):
```batch
.venv\Scripts\activate.bat
```

**Solution** (macOS/Linux):
```bash
source .venv/bin/activate
```

---

### Issue: "ModuleNotFoundError: No module named 'hello_gui'"

**Cause**: Package not installed or PYTHONPATH not set

**Solution 1** (Recommended):
```bash
pip install -e .
python -m hello_gui.app
```

**Solution 2** (Temporary workaround):
```powershell
# PowerShell
$env:PYTHONPATH="src"
python -m hello_gui.app

# CMD
set PYTHONPATH=src && python -m hello_gui.app
```

---

### Issue: "No module named 'PySide6'" or "No module named 'matplotlib'"

**Cause**: Dependencies not installed

**Solution**:
```bash
# Ensure venv is activated (should show (.venv) in prompt)
pip install -r requirements.txt

# Verify installation
python -c "import PySide6; import matplotlib; print('✓ All imports OK')"
```

---

### Issue: Application starts but plots don't appear or freeze

**Cause**: Graphics driver or Qt compatibility issue

**Solution 1**: Update drivers
- Update GPU drivers (NVIDIA/AMD/Intel)
- Update Windows

**Solution 2**: Use software rendering
```bash
$env:QT_QPA_PLATFORM="offscreen"  # PowerShell
python -m hello_gui.app
```

**Solution 3**: Check logs
```bash
# Examine debug log
Get-Content logs/hellogui.log -Tail 50
```

---

### Issue: "Permission denied" or file save fails

**Cause**: Output directory doesn't exist or lacks write permissions

**Solution**:
```bash
# Create output directory manually
mkdir output

# Ensure it's writable
```

When saving, use paths like: `output/data.csv` or `.\output\data.csv`

---

### Issue: PyInstaller build fails

**Cause**: PyInstaller not installed or path issues

**Solution**:
```bash
# Install PyInstaller in venv
pip install pyinstaller

# Try build again
scripts\build_exe.bat

# Or manually:
pyinstaller --noconfirm --name HelloGUI --windowed --onefile src/hello_gui/app.py
```

If build succeeds but `.exe` doesn't run:
1. Check `logs/hellogui.log` for errors
2. Ensure all required DLLs are in `dist/` directory
3. Try building without `--onefile` flag for debugging

---

### Issue: Tests fail with import errors

**Cause**: PYTHONPATH not set for pytest

**Solution 1** (Recommended):
```bash
pip install -e .
pytest tests/ -v
```

**Solution 2** (Temporary):
```powershell
$env:PYTHONPATH="src"
pytest tests/ -v
```

---

## Getting Help

### Examine Logs
```bash
# View recent log entries
Get-Content logs/hellogui.log -Tail 100  # PowerShell
tail -100 logs/hellogui.log              # macOS/Linux

# Search for errors
Select-String "ERROR" logs/hellogui.log  # PowerShell
grep ERROR logs/hellogui.log             # macOS/Linux
```

### Check System Info
```bash
# Python version and location
python -c "import sys; print(sys.version); print(sys.executable)"

# Installed packages
pip list | grep -E "PySide|matplotlib|numpy"

# Virtual env info
python -c "import site; print(site.getsitepackages())"
```

### Common Debug Commands
```bash
# Verify all imports
python -c "from hello_gui.app import main; from hello_gui.main_window import MainWindow; print('✓ OK')"

# Test Qt functionality
python -c "from PySide6.QtCore import QT_VERSION_STR; print(f'Qt version: {QT_VERSION_STR}')"

# Test Matplotlib
python -c "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; print('✓ Matplotlib OK')"
```

---

## Next Steps

After successful first run:

1. **Explore Config Tab** - Try different waveforms and parameters
2. **Save/Load Samples** - Use `tests/data/sample1.csv` and `sample2.csv`
3. **Read Documentation** - See `docs/README.md` and `docs/ARCHITECTURE.md`
4. **Run Tests** - Verify everything works: `pytest tests/ -v`
5. **Customize** - Modify UI, add new waveforms, or extend functionality
6. **Package for Distribution** - Build `.exe` or wheel package

---

## Quick Reference Commands

```bash
# Activate venv
.\.venv\Scripts\Activate.ps1              # PowerShell
.venv\Scripts\activate.bat                # CMD
source .venv/bin/activate                 # macOS/Linux

# Run application
python -m hello_gui.app

# Run tests
pytest tests/ -v

# Build executable
scripts\build_exe.bat                      # Windows
pyinstaller --name HelloGUI --windowed --onefile src/hello_gui/app.py

# Install/upgrade packages
pip install -r requirements.txt            # Install all
pip install -e .                           # Install HelloGUI editable
pip install --upgrade PySide6              # Upgrade package

# View logs
Get-Content logs/hellogui.log -Tail 50     # PowerShell
tail -50 logs/hellogui.log                 # macOS/Linux

# Deactivate venv
deactivate
```

---

**Version**: 1.0  
**Last Updated**: December 2025  
**Compatible With**: Python 3.11+, Windows/macOS/Linux
