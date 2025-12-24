# HelloGUI - Python Data Stream Visualization

A comprehensive, **professional-grade reference implementation** of a Python GUI application demonstrating best practices in software architecture, testing, and documentation.

## Overview

**HelloGUI** is a real-time data stream visualization tool built with:
- **PySide6** (Qt6) for cross-platform GUI
- **Matplotlib** for scientific XY plotting
- **Real-time data generation** with configurable waveforms (sine, square, random walk)
- **CSV file I/O** for data persistence
- **Type hints, docstrings, and comprehensive logging** for educational value

This project is ideal as a **reference architecture** for Python GUI developers learning professional development practices.

## Key Features

### Dashboard Tab
- **Live XY Plot**: Matplotlib FigureCanvas displaying real-time data stream
- **Stream Controls**: Pause, Resume, Clear buttons
- **File I/O**: Save/Load CSV datasets
- **Status Display**: Point count, latest (x, y), and operation status
- **Axis Labels**: Customizable X and Y axis labels

### Config Tab
- **Waveform Selection**: Sine, Square, Random Walk
- **Parameters**: Amplitude, Frequency, Noise, Sampling Interval
- **Buffer Size**: Configurable max points in memory
- **Apply/Reset**: Apply new config or reset to defaults

### Data Stream
- **Timer-based**: Qt QTimer generates points at configurable interval
- **Realistic Noise**: Gaussian noise addition to base signal
- **Pause/Resume**: Stop without clearing data; continue from last point
- **Efficient Updates**: Matplotlib blitting for responsive UI

## Project Structure

```
HelloGUI/
├── src/hello_gui/
│   ├── __init__.py
│   ├── app.py                    # Entry point & Qt bootstrap
│   ├── main_window.py            # Main window orchestration
│   │
│   ├── core/                     # Business logic
│   │   ├── __init__.py
│   │   ├── state.py              # AppState management
│   │   ├── data_stream.py        # Timer-driven data generator
│   │   ├── io_manager.py         # CSV read/write
│   │   └── logging_setup.py      # Rotating file logger
│   │
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   ├── config_model.py       # ConfigModel dataclass
│   │   └── dataset_model.py      # DatasetModel dataclass
│   │
│   ├── ui/                       # UI tabs
│   │   ├── __init__.py
│   │   ├── dashboard_tab.py      # Plot + controls tab
│   │   └── config_tab.py         # Configuration tab
│   │
│   ├── plot/                     # Visualization
│   │   ├── __init__.py
│   │   └── plot_widget.py        # Matplotlib FigureCanvas widget
│   │
│   └── resources/
│       └── icons/                # Placeholder for icons
│
├── tests/
│   ├── __init__.py
│   ├── test_io_manager.py        # CSV I/O tests
│   ├── test_data_stream.py       # Data generation tests
│   └── data/
│       ├── sample1.csv           # Test dataset
│       └── sample2.csv           # Test dataset
│
├── scripts/
│   ├── quick_start.bat           # Windows quick setup
│   ├── run_tests.bat             # Run pytest suite
│   └── build_exe.bat             # Build .exe with PyInstaller
│
├── docs/
│   ├── README.md                 # This file
│   ├── ARCHITECTURE.md           # Component diagrams
│   └── CHANGELOG.md              # Version history
│
├── logs/                         # Auto-created; rotating log files
│
├── pyproject.toml                # Project metadata & build config
├── requirements.txt              # Dependencies
├── .gitignore                    # Git ignore rules
├── .editorconfig                 # Code style
└── .vscode/                      # VS Code settings
    ├── settings.json             # Format on save, linting
    ├── launch.json               # Debug configuration
    └── tasks.json                # Build/run/test tasks
```

## Quick Start

### 1. Clone or Extract the Repository

```bash
cd HelloGUI
```

### 2. Quick Start (Easiest)

**Windows PowerShell** (Recommended):
```powershell
.\scripts\quick_start.ps1
```

**Windows Batch**:
```bash
scripts\quick_start.bat
```

**macOS/Linux**:
Follow manual setup below.

### 3. Manual Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate              # Windows
source .venv/bin/activate           # macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run the application
python -m hello_gui.app
```

### 4. Run Tests

```bash
pytest tests/ -v
```

### 5. Build Executable (Windows)

```bash
scripts\build_exe.bat
```

---

**For detailed setup instructions, see [HOWTO.md](../HOWTO.md)**

## Usage Guide

### Dashboard Tab

1. **Configuring the Stream**:
   - Go to the **Config** tab
   - Adjust amplitude, frequency, noise, and waveform type
   - Click **Apply** to activate new settings

2. **Running the Stream**:
   - Click **Resume** to start generating data
   - Data points appear in real-time on the plot
   - Status bar shows point count and latest (x, y)

3. **Pausing the Stream**:
   - Click **Pause** to stop without clearing data
   - Click **Resume** to continue from the last point

4. **Clearing Data**:
   - Click **Clear** to remove all points and reset the plot

5. **Saving Data**:
   - Enter a file path (e.g., `output/my_data.csv`)
   - Click **Save Data**
   - CSV file is created with headers "x,y"

6. **Loading Data**:
   - Enter a file path (e.g., `tests/data/sample1.csv`)
   - Click **Load Data**
   - Previous data is replaced; plot updates

### Config Tab

- **Waveform Type**: 
  - **sine**: y = amplitude × sin(2π × frequency × x) + noise
  - **square**: ±amplitude based on frequency
  - **randomwalk**: Random steps bounded by amplitude

- **Parameters**:
  - **Amplitude**: Peak value of waveform (0.01 to 100.0)
  - **Frequency**: Oscillations per unit X (0.0 to 10.0 Hz)
  - **Noise**: Gaussian noise standard deviation (0.0 to 1.0)
  - **X-Step**: Increment per sample (0.001 to 1.0)
  - **Max Points**: Buffer size before oldest point is discarded

- **Actions**:
  - **Apply**: Validate and apply new configuration
  - **Reset Defaults**: Revert to factory defaults

## Saving/Loading CSV Files

### CSV Format

The application uses a simple CSV format with header row:

```csv
x,y
0.0,0.1234
0.05,0.2456
0.1,0.3421
```

### Example Workflow

1. Let the app collect data (click Resume on Dashboard)
2. Enter file path: `output/experiment_001.csv`
3. Click **Save Data**
4. Later, load it back: enter path and click **Load Data**
5. Plot shows previously saved data

## Architecture Overview

### Signal Flow

```
DataStream (QTimer) 
  → emits new_point(x, y)
    → MainWindow slot on_new_point()
      → AppState.dataset.add_point()
      → PlotWidget.append_point()
      → UI status updates
```

### Component Roles

- **AppState**: Central state holder (config, dataset, running flag)
- **DataStream**: Qt timer-based point generator with signals
- **PlotWidget**: Matplotlib integration for Qt
- **DashboardTab/ConfigTab**: UI presentation
- **io_manager**: Stateless CSV read/write functions
- **ConfigModel/DatasetModel**: Simple data containers

### Key Design Principles

1. **Separation of Concerns**: 
   - UI logic separated from data generation
   - Pure functions for math (waveform, noise)
   - Qt signals decouple components

2. **Type Hints**: 
   - All functions include parameter and return type hints
   - Enables IDE autocomplete and type checking

3. **Documentation**: 
   - Module-level docstrings explain purpose
   - Function docstrings with Args/Returns sections
   - Inline comments for non-obvious logic

4. **Testability**: 
   - Data generation extracted to pure functions
   - I/O operations testable without GUI
   - Configuration validation separate from application

5. **Error Handling**: 
   - CSV errors return (success, message) tuples
   - Configuration validation before application
   - User-facing error dialogs for I/O failures

## Logging

The application logs to:

- **Console**: INFO and above (real-time feedback)
- **File**: `logs/hellogui.log` (DEBUG and above)
  - Rotating handler: 10 MB max, 5 backups
  - Useful for troubleshooting and audit trail

Example log output:

```
2025-12-23 14:30:15,123 - hellogui - INFO - ============================================================
2025-12-23 14:30:15,124 - hellogui - INFO - HelloGUI Application Starting
2025-12-23 14:30:15,125 - hellogui - INFO - MainWindow initialized
2025-12-23 14:30:22,456 - hellogui - INFO - Data stream started
2025-12-23 14:30:25,789 - hellogui - INFO - Saved 150 points to output/data.csv
```

## Building an Executable (Windows)

Use PyInstaller to create a standalone `.exe`:

```bash
scripts\build_exe.bat
```

This generates:
- `dist/HelloGUI.exe`: Single executable (portable)
- Includes all dependencies bundled

Distribute the `.exe` file to users without requiring Python installation.

## Testing

The project includes unit tests for core logic:

### Test Coverage

- **test_io_manager.py**:
  - CSV write/read roundtrip
  - Invalid file paths
  - Malformed CSV (bad headers, non-numeric values)
  - Empty files and large datasets

- **test_data_stream.py**:
  - Sine wave generation and amplitude scaling
  - Square wave period and polarity
  - Random walk bounds
  - Noise addition
  - Configuration validation

### Running Tests

```bash
# All tests
pytest

# Verbose output
pytest -v

# Specific test file
pytest tests/test_io_manager.py

# Specific test function
pytest tests/test_data_stream.py::TestSineWave::test_sine_at_zero
```

## Dependencies

- **PySide6**: Qt6 Python bindings (GUI framework)
- **matplotlib**: Scientific plotting library
- **numpy**: Numerical computing (used by matplotlib)
- **pytest**: Testing framework
- **pyinstaller**: Build executable (optional)

See `requirements.txt` for pinned versions.

## System Requirements

- **Python**: 3.11 or later
- **OS**: Windows, macOS, or Linux
- **RAM**: 100 MB minimum
- **Disk**: ~200 MB (with dependencies)

## VS Code Integration

### Launch Configuration

Press `F5` to debug or use **Run → Start Debugging** menu:
- Automatically starts `src/hello_gui/app.py`
- Can set breakpoints and inspect variables

### Tasks

**Terminal → Run Task** provides:
- **Setup: venv**: Create virtual environment
- **Install: deps**: Install requirements
- **Run: HelloGUI**: Start application
- **Test: pytest**: Run test suite
- **Build: EXE**: Create standalone executable

### Code Formatting

On file save:
- **Black** formats code
- **Flake8** shows linting issues
- **Pylance** provides type checking

## Troubleshooting

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'PySide6'`

**Solution**: Ensure venv is activated and requirements installed:
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### Plot Not Updating

**Symptoms**: Data stream running but plot stays empty

**Solution**: 
- Check that "Resume" button was clicked
- Verify config is valid (no error dialog)
- Check `logs/hellogui.log` for exceptions

### CSV Load Fails

**Error**: "CSV file is empty" or "expected header ['x', 'y']"

**Solution**:
- Ensure CSV has header row with exactly "x" and "y"
- Check that values are valid floating-point numbers
- Use sample files in `tests/data/` as reference

### High CPU Usage

**Symptoms**: Application consuming significant CPU

**Cause**: Plot redraw interval too aggressive

**Solution**:
- Reduce point generation frequency (increase X-Step in Config)
- Close other applications

## Future Enhancements

- Real data source input (sensors, network streams)
- Multiple simultaneous plots
- Data filtering and FFT analysis
- Export to image/PDF
- Dark mode theme
- Keyboard shortcuts and hotkeys

## Contributing

This is a demonstration project. To extend or modify:

1. Follow the existing code style (type hints, docstrings)
2. Add tests for new features in `tests/`
3. Update documentation in `docs/`
4. Use VS Code formatting on save

## License

[Specify your license here, e.g., MIT, Apache 2.0]

## References

- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Matplotlib for PySide6](https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_qt_agg.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pytest Documentation](https://docs.pytest.org/)

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Author**: HelloGUI Development Team
