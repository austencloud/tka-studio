# Running TKA Tests

## Quick Start

### Prerequisites

```bash
# Install TKA package with test dependencies
pip install -e .[test]

# Or if using development requirements
pip install -r requirements-dev.txt
```

### Basic Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run with verbose output
pytest -v

# Run and generate HTML coverage report
pytest --cov=src --cov-report=html
```

## Test Categories

### By Platform

```bash
# All desktop tests (legacy + modern + launcher)
pytest tests/desktop/

# Web application tests
pytest tests/web/

# Shared utility tests
pytest tests/shared/
```

### By Desktop Version

```bash
# Legacy desktop application
pytest tests/desktop/legacy/

# Modern desktop application
pytest tests/desktop/modern/

# Launcher application
pytest tests/desktop/launcher/

# Cross-version integration
pytest tests/desktop/integration/
```

### By Test Type

```bash
# Unit tests only (fast)
pytest -m unit

# Integration tests only
pytest -m integration

# Specification tests only
pytest -m specification

# UI tests (requires display)
pytest -m ui
```

### By Speed

```bash
# Fast tests only (excludes slow tests)
pytest -m "not slow"

# Slow tests only
pytest -m slow

# Unit and fast integration tests
pytest -m "unit or (integration and not slow)"
```

## Advanced Filtering

### Combining Markers

```bash
# Modern desktop unit tests
pytest -m "unit and modern and desktop"

# All launcher tests (any type)
pytest -m launcher

# Legacy integration tests only
pytest -m "integration and legacy"

# Web unit tests excluding slow ones
pytest -m "unit and web and not slow"
```

### By File Pattern

```bash
# Specific test file
pytest tests/desktop/modern/unit/test_graph_editor.py

# All tests in a directory
pytest tests/desktop/modern/integration/

# Pattern matching
pytest tests/desktop/*/unit/
```

### By Test Name

```bash
# Specific test function
pytest tests/desktop/modern/unit/test_graph_editor.py::test_beat_selection

# Test class
pytest tests/desktop/modern/unit/test_graph_editor.py::TestGraphEditor

# Pattern matching in test names
pytest -k "graph_editor"
pytest -k "not slow_test"
```

## Development Workflows

### Pre-commit Testing

```bash
# Quick smoke test (unit tests only)
pytest -m unit

# Component-specific testing
pytest tests/desktop/modern/unit/application/

# Integration verification
pytest tests/desktop/modern/integration/ -m "not slow"
```

### Feature Development

```bash
# When working on a specific component
pytest tests/desktop/modern/unit/presentation/components/

# When changing service interfaces
pytest tests/desktop/modern/integration/

# When adding new features
pytest tests/desktop/modern/specification/
```

### Bug Investigation

```bash
# Run failing test with debugging
pytest tests/desktop/modern/unit/test_failing.py --pdb

# Verbose output for troubleshooting
pytest tests/desktop/modern/unit/test_failing.py -v -s

# Run with print statements visible
pytest tests/desktop/modern/unit/test_failing.py -s
```

### Performance Testing

```bash
# Show test durations
pytest --durations=10

# Profile slow tests
pytest --durations=0 -m slow

# Memory profiling (if pytest-memprof installed)
pytest --memprof tests/desktop/modern/integration/
```

## Continuous Integration

### GitHub Actions / CI Pipeline

```bash
# Full test suite
pytest tests/ --cov=src --cov-report=xml

# Desktop tests only
pytest tests/desktop/ --cov=src/desktop

# Web tests only
pytest tests/web/ --cov=src/web
```

### Parallel Execution

```bash
# Run tests in parallel (if pytest-xdist installed)
pytest -n auto

# Run specific number of workers
pytest -n 4

# Parallel by test type
pytest tests/desktop/modern/unit/ -n auto
```

## Coverage Reporting

### Basic Coverage

```bash
# Terminal coverage report
pytest --cov=src

# Skip covered lines in report
pytest --cov=src --cov-report=term-missing

# HTML coverage report
pytest --cov=src --cov-report=html
# View report: open htmlcov/index.html
```

### Coverage by Component

```bash
# Desktop coverage only
pytest tests/desktop/ --cov=src/desktop

# Modern architecture coverage
pytest tests/desktop/modern/ --cov=src/desktop/modern

# Launcher coverage
pytest tests/desktop/launcher/ --cov=launcher
```

### Coverage Thresholds

```bash
# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=80

# Branch coverage
pytest --cov=src --cov-branch
```

## Debugging Failed Tests

### Interactive Debugging

```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger on first failure
pytest --pdb -x

# Use ipdb instead of pdb
pytest --pdbcls=IPython.terminal.debugger:Pdb
```

### Verbose Output

```bash
# Show all output (don't capture)
pytest -s

# Very verbose
pytest -vv

# Show local variables in traceback
pytest --tb=long

# Show shortest traceback
pytest --tb=short
```

### Test Environment Debugging

```bash
# Show test collection without running
pytest --collect-only

# Show available fixtures
pytest --fixtures

# Show markers
pytest --markers
```

## Common Issues and Solutions

### Import Errors

```bash
# If imports fail, check package installation
pip install -e .

# Verify pytest can find tests
pytest --collect-only tests/

# Check Python path issues
python -c "import sys; print(sys.path)"
```

### Qt/UI Test Issues

```bash
# If Qt tests fail on headless systems
xvfb-run pytest -m ui

# Skip UI tests
pytest -m "not ui"

# Qt backend issues
export QT_QPA_PLATFORM=minimal
pytest -m ui
```

### Performance Issues

```bash
# Skip slow tests
pytest -m "not slow"

# Run tests with timeout (if pytest-timeout installed)
pytest --timeout=60

# Memory issues
pytest --maxfail=1  # Stop after first failure
```

### Fixture Issues

```bash
# Debug fixture dependency issues
pytest --setup-show

# Show fixture values
pytest --fixtures-per-test

# Skip fixture caching
pytest --cache-clear
```

## Test Output Formats

### JUnit XML (for CI)

```bash
pytest --junitxml=results.xml
```

### JSON Report

```bash
# If pytest-json-report installed
pytest --json-report --json-report-file=report.json
```

### HTML Report

```bash
# If pytest-html installed
pytest --html=report.html --self-contained-html
```

## Best Practices

### Test Selection

- Use specific markers rather than running everything
- Start with unit tests, then integration
- Use `not slow` for quick feedback during development

### Debugging

- Use `pytest -x` to stop on first failure
- Add `--pdb` only when investigating specific failures
- Use `-s` to see print statements

### CI/CD

- Always run full test suite in CI
- Use parallel execution for faster CI builds
- Separate fast and slow test stages

### Coverage

- Aim for high coverage but focus on meaningful tests
- Use coverage to find untested code, not as a goal itself
- Exclude test files and generated code from coverage

## Configuration Files

- **pytest.ini**: Main pytest configuration
- **pyproject.toml**: Modern Python project configuration
- **.coveragerc**: Coverage configuration (if using separate file)
- **conftest.py**: Test fixtures and setup
