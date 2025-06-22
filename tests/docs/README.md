# TKA Test Organization

## Overview

This directory contains the complete test suite for the TKA (The Kinetic Alphabet) project, organized into a clean, hierarchical structure that supports both legacy and modern architectures.

## Directory Structure

```
tests/
├── desktop/                     # Desktop application tests
│   ├── legacy/                  # Legacy desktop tests
│   │   ├── unit/               # Legacy unit tests
│   │   ├── integration/        # Legacy integration tests  
│   │   └── specification/      # Legacy specification tests
│   ├── modern/                 # Modern desktop tests
│   │   ├── unit/               # Modern unit tests
│   │   ├── integration/        # Modern integration tests
│   │   │   └── workflows/      # Workflow integration tests
│   │   └── specification/      # Modern specification tests
│   │       └── domain/         # Domain specification tests
│   ├── launcher/               # Launcher application tests
│   ├── integration/            # Cross-version integration tests
│   └── shared/                 # Desktop shared test utilities
├── web/                        # Web application tests
│   ├── unit/                   # Web unit tests
│   ├── integration/            # Web integration tests
│   └── e2e/                    # End-to-end web tests
├── shared/                     # Cross-platform shared resources
│   ├── fixtures/               # Reusable test fixtures
│   ├── utilities/              # Test helper functions
│   ├── data/                   # Sample data for tests
│   └── dev_utilities/          # Development/debugging scripts
└── docs/                       # Test documentation
```

## Test Types

### Unit Tests (`unit/`)
- **Purpose**: Test individual components in isolation
- **Execution**: Fast (< 1 second each)
- **Dependencies**: Mock all external dependencies
- **Marker**: `@pytest.mark.unit`

### Integration Tests (`integration/`)
- **Purpose**: Test component interactions
- **Execution**: Medium speed (1-10 seconds)
- **Dependencies**: May use real dependencies within component boundary
- **Marker**: `@pytest.mark.integration`

### Specification Tests (`specification/`)
- **Purpose**: Test against defined specifications and requirements
- **Execution**: Variable (can be unit or integration style)
- **Dependencies**: Based on what's being specified
- **Marker**: `@pytest.mark.specification`

## Platform Categories

### Desktop Tests (`tests/desktop/`)
- **Legacy**: Tests for the original PyQt5-based desktop application
- **Modern**: Tests for the refactored PyQt6-based desktop application
- **Launcher**: Tests for the application launcher/selector
- **Integration**: Tests that verify legacy ↔ modern compatibility

### Web Tests (`tests/web/`)
- **Unit**: Frontend component tests
- **Integration**: API integration tests
- **E2E**: End-to-end browser tests

## Quick Start

### Install Dependencies
```bash
pip install -e .[test]
```

### Run All Tests
```bash
pytest
```

### Run Specific Categories
```bash
# Platform-specific
pytest tests/desktop/
pytest tests/web/

# Version-specific
pytest tests/desktop/legacy/
pytest tests/desktop/modern/
pytest tests/desktop/launcher/

# Type-specific
pytest -m unit
pytest -m integration
pytest -m specification
```

### Common Test Combinations
```bash
# Fast tests only
pytest -m "unit or (integration and not slow)"

# Modern desktop unit tests
pytest -m "unit and modern and desktop"

# All launcher tests
pytest -m launcher

# Integration tests excluding slow ones
pytest -m "integration and not slow"
```

## Development Workflow

### Before Committing
1. Run relevant tests for your changes:
   ```bash
   pytest tests/desktop/modern/unit/  # If you changed modern components
   ```

2. Run integration tests if you changed interfaces:
   ```bash
   pytest tests/desktop/modern/integration/
   ```

3. For major changes, run the full suite:
   ```bash
   pytest
   ```

### Writing New Tests
1. Place tests in the appropriate directory based on:
   - **Platform**: `desktop/` or `web/`
   - **Version**: `legacy/`, `modern/`, or `launcher/`
   - **Type**: `unit/`, `integration/`, or `specification/`

2. Use appropriate markers:
   ```python
   @pytest.mark.unit
   @pytest.mark.modern
   @pytest.mark.desktop
   def test_my_component():
       pass
   ```

3. Follow naming conventions:
   - Files: `test_*.py`
   - Functions: `test_*`
   - Classes: `Test*`

## Configuration

- **pytest.ini**: Main pytest configuration
- **tests/conftest.py**: Root-level fixtures and configuration
- **tests/desktop/conftest.py**: Desktop-specific fixtures
- **tests/web/conftest.py**: Web-specific fixtures

## Shared Resources

### Test Utilities (`tests/shared/utilities/`)
- `test_helpers.py`: Common helper functions
- Functions for creating mock data, assertions, etc.

### Test Data (`tests/shared/data/`)
- `sample_sequences.json`: Sample sequence data for testing
- Other JSON files with test data

### Fixtures (`tests/shared/fixtures/`)
- Reusable pytest fixtures
- Common mock objects and test data

## Troubleshooting

### Import Errors
If you get import errors, ensure:
1. You've installed the package: `pip install -e .`
2. You're running tests from the project root
3. The `conftest.py` files are properly configured

### Test Discovery Issues
```bash
# Check what tests pytest can find
pytest --collect-only

# Run with verbose output to see discovery process
pytest -v
```

### Performance Issues
```bash
# Run only fast tests
pytest -m "not slow"

# Profile test execution
pytest --durations=10
```

## Migration Notes

This structure was created by consolidating tests from multiple locations:
- `src/desktop/modern/tests/` → `tests/desktop/modern/`
- `launcher/tests/` → `tests/desktop/launcher/`
- `src/desktop/legacy/` (scattered) → `tests/desktop/legacy/`

All import paths have been updated to work with the new structure.

## Contributing

1. Follow the established directory structure
2. Use appropriate test markers
3. Add tests to the relevant category based on what you're testing
4. Update documentation if you add new test patterns or utilities
5. Ensure all tests pass before submitting changes

For detailed testing guidelines, see `tests/docs/writing-tests.md`.
