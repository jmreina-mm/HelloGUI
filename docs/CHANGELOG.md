# Changelog

## [1.0.0] - 2025-12-23

### Initial Release

#### Added
- **Dashboard Tab**:
  - Real-time XY plot with Matplotlib FigureCanvas
  - Configurable axis labels
  - Pause/Resume/Clear controls for data stream
  - Save and Load CSV functionality
  - Status bar showing point count and latest (x, y)
  - Dataset name and file path inputs

- **Config Tab**:
  - Amplitude, Frequency, Noise, X-Step spinboxes
  - Waveform type selector (sine, square, randomwalk)
  - Max points buffer size control
  - Apply and Reset Defaults buttons

- **Data Stream**:
  - Qt QTimer-based point generator
  - Configurable interval (100ms default)
  - Three waveform types:
    - Sine wave with phase and amplitude
    - Square wave based on frequency
    - Random walk with bounded steps
  - Gaussian noise addition to all waveforms
  - Pause/resume capability
  - Signal emissions for point generation

- **File I/O**:
  - CSV write with automatic directory creation
  - CSV read with comprehensive validation
  - Error handling and user-friendly messages
  - Roundtrip consistency (write → read)

- **Data Models**:
  - ConfigModel with validation and defaults
  - DatasetModel with automatic buffer management
  - Type hints and comprehensive docstrings

- **Logging**:
  - Rotating file handler (logs/hellogui.log)
  - Console output with formatting
  - 10 MB file limit, 5 backup files
  - Debug and Info level separation

- **Tests**:
  - test_io_manager.py: CSV operations, edge cases
  - test_data_stream.py: Waveform generation, validation

- **Documentation**:
  - README.md with quick start and usage guide
  - ARCHITECTURE.md with component diagrams and patterns
  - Comprehensive docstrings throughout codebase

- **VS Code Integration**:
  - settings.json: Black formatting, Flake8 linting
  - launch.json: Debug configuration
  - tasks.json: venv setup, install, run, test, build

- **Windows Scripts**:
  - quick_start.bat: One-click venv setup and run
  - run_tests.bat: Run pytest suite
  - build_exe.bat: PyInstaller build for standalone executable

### Features

- **Type Safety**: Full type hints on all public functions
- **Educational**: Detailed inline comments and module docstrings
- **Professional**: Error handling, validation, logging throughout
- **Testable**: Pure functions for math, separable concerns
- **Extensible**: Clear extension points for new waveforms, data sources

### Testing

- 20+ test cases covering:
  - CSV roundtrip operations
  - Invalid file handling
  - Waveform generation accuracy
  - Noise distribution
  - Configuration validation
  - Edge cases (empty files, bad headers, non-numeric values)

---

**Project Start**: December 2025  
**Version**: 1.0.0  
**Status**: Stable, Reference Quality
