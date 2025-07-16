# TKA Comprehensive Test Runner Guide

## 🎯 Overview

The TKA Comprehensive Test Runner is a bulletproof test execution system designed specifically for the TKA PyQt6 project. It addresses all the previous pytest configuration and test discovery issues while providing both command-line and GUI interfaces.

## ✨ Features

- **Universal Test Discovery**: Finds ALL test files across the entire codebase
- **Single Command Execution**: Run all tests with one simple command
- **Dual Interface Options**: Command-line and optional GUI interface
- **PyQt6 Optimized**: Properly configured for PyQt6 applications
- **Performance Optimized**: Targets <5 second execution with parallel processing
- **Comprehensive Reporting**: Clear feedback with detailed error reporting

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
python install_test_runner.py

# Validate installation
python install_test_runner.py --validate-only
```

### 2. Basic Usage

```bash
# Discover all tests
python tka_test_runner.py --discover

# Run all tests (command-line)
python tka_test_runner.py

# Launch GUI interface
python tka_test_runner.py --gui

# Quick start scripts (after installation)
./run_tests.sh        # Unix/Linux/Mac
run_tests.bat          # Windows
```

## 📋 Command-Line Interface

### Basic Commands

```bash
# Run all tests
python tka_test_runner.py

# Run only fast tests (<2 seconds)
python tka_test_runner.py --fast

# Run tests in parallel
python tka_test_runner.py --parallel

# Run specific test categories
python tka_test_runner.py --unit
python tka_test_runner.py --integration

# Get JSON output
python tka_test_runner.py --output json
```

### Advanced Options

```bash
# Discover tests without running
python tka_test_runner.py --discover

# Show help
python tka_test_runner.py --help

# Combine options
python tka_test_runner.py --fast --parallel --unit
```

## 🖥️ GUI Interface

The GUI interface provides:

- **Visual Test Discovery**: Tree view of all discovered tests organized by category
- **Real-time Progress**: Progress bar and current test display
- **Interactive Selection**: Check/uncheck individual tests or categories
- **Results Visualization**: Summary statistics and detailed output
- **Export Capabilities**: Save results to text files

### GUI Features

- **Test Filtering**: Filter by category (Unit, Integration, GUI, Regression)
- **Execution Options**: Fast-only mode and parallel execution
- **Progress Tracking**: Real-time updates during test execution
- **Error Reporting**: Detailed error display with context
- **Export Results**: Save test results and output to files

## 🔧 Configuration

### pytest.ini Configuration

The test runner uses an optimized pytest.ini configuration:

```ini
[pytest]
qt_api = pyqt6

addopts =
    --tb=short
    --disable-warnings
    --maxfail=1000
    --strict-markers
    --strict-config
    --continue-on-collection-errors
    --capture=no
    -v

pythonpath =
    .
    src
    src/desktop/modern/src
    src/desktop/modern
    src/desktop/legacy/src
    src/desktop/legacy
    launcher
    packages

testpaths =
    .
    src/desktop/modern/tests
    src/desktop/legacy/tests
    launcher/tests
```

### Environment Setup

The test runner automatically configures:

- **PYTHONPATH**: All necessary project directories
- **QT_QPA_PLATFORM**: Set to "offscreen" for headless testing
- **Test Discovery**: Comprehensive search across all directories

## 📊 Test Categories

Tests are automatically categorized:

- **unit**: Unit tests (fast, isolated)
- **integration**: Integration tests (component interactions)
- **specification**: Specification tests (requirements verification)
- **end_to_end**: End-to-end tests (complete workflows)
- **regression**: Regression tests (bug prevention)
- **gui**: GUI tests (PyQt6 widgets)
- **services**: Service layer tests
- **components**: Component tests
- **positioning**: Positioning system tests
- **other**: Uncategorized tests

## ⚡ Performance Optimizations

### Parallel Execution

```bash
# Enable parallel execution
python tka_test_runner.py --parallel
```

The test runner groups tests by category to avoid Qt application conflicts while maximizing parallelization.

### Fast Test Mode

```bash
# Run only tests estimated to take <2 seconds
python tka_test_runner.py --fast
```

### Test Prioritization

Tests are prioritized by:
1. Category importance (unit → integration → gui → e2e)
2. Critical test markers
3. Estimated execution time

## 🔍 Test Discovery

The discovery engine searches:

- `src/desktop/modern/tests/`
- `src/desktop/legacy/tests/`
- `launcher/tests/`
- `tests/`
- Root directory test files

### Discovery Patterns

- `test_*.py`
- `*_test.py`

### Exclusions

- Virtual environments (`.venv`, `venv`)
- Node modules (`node_modules`)
- Cache directories (`__pycache__`)
- Git directories (`.git`)

## 🛠️ Troubleshooting

### Common Issues

#### 1. PyQt6 Import Errors

```bash
# Install PyQt6
pip install PyQt6

# Validate installation
python install_test_runner.py --validate-only
```

#### 2. Test Discovery Issues

```bash
# Check discovered tests
python tka_test_runner.py --discover

# Verify pytest configuration
python -m pytest --collect-only
```

#### 3. GUI Not Available

```bash
# Check PyQt6 installation
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"

# Use command-line interface instead
python tka_test_runner.py
```

#### 4. Permission Errors

```bash
# Make shell script executable (Unix/Linux/Mac)
chmod +x run_tests.sh

# Run with proper permissions
sudo python install_test_runner.py
```

### Debug Mode

For debugging test discovery or execution issues:

```python
# Enable debug output in the test runner
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Integration with Development Workflow

### IDE Integration

The test runner works with:

- **VS Code**: Use the integrated terminal
- **PyCharm**: Configure as external tool
- **Command Line**: Direct execution

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Run TKA Tests
  run: |
    python install_test_runner.py
    python tka_test_runner.py --output json > test_results.json
```

### Pre-commit Hooks

```bash
# Add to .git/hooks/pre-commit
#!/bin/bash
python tka_test_runner.py --fast
```

## 🔬 Research Citations

This implementation is based on industry best practices:

1. **pytest-qt Documentation**: https://pytest-qt.readthedocs.io/
2. **PyQt6 Testing Guide**: https://doc.qt.io/qt-6/qttest-index.html
3. **pytest Configuration**: https://docs.pytest.org/en/stable/reference/customize.html
4. **Python Testing Best Practices**: https://docs.python-guide.org/writing/tests/

## 📝 Example Output

### Command-Line Output

```
🔍 Discovering tests across TKA codebase...
📋 Found 47 test files
🚀 Running tests...

============================================================
📊 TEST RESULTS
============================================================
Total Tests: 47
Passed:      45
Failed:      2
Skipped:     0
Success:     ❌ NO
Time:        3.42 seconds

❌ Errors (2):
  • test_positioning_baseline.py::test_arrow_placement FAILED
  • test_gui_integration.py::test_widget_creation FAILED
```

### JSON Output

```json
{
  "success": false,
  "total_tests": 47,
  "passed": 45,
  "failed": 2,
  "skipped": 0,
  "execution_time": 3.42,
  "errors": [
    "test_positioning_baseline.py::test_arrow_placement FAILED",
    "test_gui_integration.py::test_widget_creation FAILED"
  ]
}
```

## 🎯 Next Steps

1. **Run Installation**: `python install_test_runner.py`
2. **Discover Tests**: `python tka_test_runner.py --discover`
3. **Execute Tests**: `python tka_test_runner.py`
4. **Try GUI**: `python tka_test_runner.py --gui`
5. **Integrate into Workflow**: Add to your development routine

The TKA Test Runner eliminates the previous pytest configuration issues and provides a reliable, comprehensive testing solution for the entire TKA project.
