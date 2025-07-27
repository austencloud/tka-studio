# TKA - The Kinetic Alphabet

> A comprehensive platform for kinetic movement notation, sequence building, and analysis

## Overview

TKA (The Kinetic Alphabet) is a sophisticated desktop application built with PyQt6 that provides tools for creating, analyzing, and managing kinetic movement sequences. The platform offers both desktop and web interfaces for choreographers, movement analysts, and researchers working with structured movement notation.

### Key Features

- **Sequence Construction**: Interactive tools for building movement sequences with visual feedback
- **Position Management**: Comprehensive start position selection and validation
- **Real-time Analysis**: Live sequence analysis and validation during construction
- **Multi-Platform Support**: Desktop application with web component integration
- **Extensible Architecture**: Modular design supporting plugins and custom workflows

## Quick Start

### Prerequisites

- Python 3.9+ 
- PyQt6
- Node.js (for web components)

### Installation

```bash
# Clone the repository
git clone [repository-url]
cd TKA

# Install Python dependencies
pip install -e .

# Install Node.js dependencies (if needed)
npm install

# Run the application
python main.py
```

## Project Structure

```
TKA/
├── src/                        # Source code
│   ├── desktop/               # Desktop application
│   │   ├── modern/           # Current desktop implementation  
│   │   └── legacy/           # Legacy desktop code
│   ├── shared/               # Shared components
│   ├── web/                  # Web interface components
│   └── infrastructure/       # Core infrastructure
├── tests/                     # Test suites
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── e2e/                  # End-to-end tests
├── data/                     # Application data
├── docs/                     # Documentation
├── scripts/                  # Build and development scripts
└── tools/                    # Development tools
```

## Usage

### Basic Workflow

1. **Launch Application**: Run `python main.py` to start TKA
2. **Navigate to Construct Tab**: [Details to be added]
3. **Select Start Position**: [Details to be added]
4. **Build Sequence**: [Details to be added]
5. **Analyze Results**: [Details to be added]

### Core Concepts

#### Start Positions
[To be documented - explain position notation like "alpha1_alpha1", "beta5_beta5", etc.]

#### Sequence Building
[To be documented - explain the sequence construction workflow]

#### Movement Notation
[To be documented - explain the kinetic alphabet system]

## Development

### Architecture

TKA follows a modern, modular architecture:

- **Desktop Application**: PyQt6-based GUI with modern design patterns
- **Shared Components**: Reusable business logic and data models  
- **Web Integration**: Web components for enhanced functionality
- **Testing Framework**: Comprehensive test suite with unit, integration, and E2E tests

### Development Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run with development mode
python main.py --dev
```

### Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/           # Unit tests
pytest tests/integration/    # Integration tests  
pytest tests/e2e/           # End-to-end tests

# Run with coverage
pytest --cov=src

# Run performance benchmarks
pytest --benchmark-only
```

### Code Quality

The project maintains high code quality standards:

- **Linting**: Pylint configuration in `pyproject.toml`
- **Type Checking**: Pyright/Pylance integration
- **Formatting**: Black code formatter
- **Import Sorting**: isort configuration
- **Testing**: pytest with comprehensive test markers

## Configuration

### Application Configuration

- **Main Config**: `pyproject.toml` - Primary project configuration
- **Environment**: `.env` - Environment-specific settings
- **Development**: `pyrightconfig.json` - Type checking configuration

### Test Configuration

- **pytest**: Configuration in `pyproject.toml`
- **Markers**: Custom test markers for different test types
- **Fixtures**: Reusable test fixtures in `conftest.py` files

## Technical Details

### Dependencies

#### Core Dependencies
- **PyQt6**: Desktop GUI framework
- **Pydantic**: Data validation and settings management
- **SQLAlchemy**: Database ORM
- **Requests**: HTTP client

#### Development Dependencies  
- **pytest**: Testing framework with Qt support
- **Black**: Code formatting
- **Pylint**: Code analysis
- **mypy**: Type checking

#### Testing Dependencies
- **pytest-qt**: PyQt testing support
- **pytest-benchmark**: Performance testing
- **pytest-cov**: Coverage reporting
- **Hypothesis**: Property-based testing

### Platform Support

- **Primary**: Windows, macOS, Linux desktop environments
- **Web**: Modern browsers with ES6+ support
- **Python**: 3.9+ required

## Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Ensure all tests pass
5. Submit a pull request

### Coding Standards

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write tests for new functionality
- Update documentation as needed

### Testing Guidelines

- Write unit tests for isolated functionality
- Add integration tests for component interactions
- Include E2E tests for user workflows
- Maintain test coverage above 80%

## Roadmap

### Current Focus
- [To be documented - current development priorities]

### Planned Features
- [To be documented - upcoming features]

### Long-term Vision
- [To be documented - long-term project goals]

## Troubleshooting

### Common Issues

#### Application Won't Start
[To be documented - common startup issues and solutions]

#### Performance Issues  
[To be documented - performance optimization tips]

#### Testing Issues
[To be documented - common test failures and fixes]

### Getting Help

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Documentation**: Check the `docs/` directory for detailed guides
- **Community**: [To be added - community channels]

## License

[To be added - specify license]

## Acknowledgments

[To be added - credits and acknowledgments]

---

## Development Status

This README is currently being developed section by section. Sections marked with "[To be documented]" or "[To be added]" are placeholders for future content.

### Completion Status
- [x] Project structure and overview
- [x] Installation and quick start
- [x] Development setup
- [x] Testing framework
- [ ] Detailed usage instructions
- [ ] Core concepts explanation  
- [ ] API documentation
- [ ] Troubleshooting guide
- [ ] Contributing guidelines details