# TKA UI Testing Framework

A comprehensive testing framework for the TKA application's UI components, designed to test fundamental user workflow functionality and identify/fix UI issues.

## Overview

The TKA UI Testing Framework provides:

- **Comprehensive Button Testing**: Tests all 11 workbench buttons with proper signal handling
- **Graph Editor Testing**: Tests turn controls, orientation pickers, and keyboard shortcuts
- **Hover Event Testing**: Tests mouse enter/leave events, cursor changes, and tooltips
- **Responsive Layout Testing**: Tests component sizing and layout responsiveness
- **AI Agent Integration**: Clear console guidance for AI agents when tests fail
- **Legacy Code Guidance**: Automatic references to legacy implementations for debugging

## Architecture

The framework follows TKA's clean architecture principles:

- **SimpleUITester**: Main testing orchestrator
- **ComponentInitializer**: Initializes UI components with real data
- **ButtonTester**: Tests workbench buttons with legacy guidance
- **GraphEditorTester**: Tests graph editor interactions
- **UITestRunner**: Integration layer for main application
- **CLI Interface**: Command-line interface for testing

## Quick Start

### 1. Run Quick Validation

```bash
# From the testing directory
python ui_test_main.py --quick
```

### 2. Test All Buttons

```bash
python ui_test_main.py --buttons
```

### 3. Test Graph Editor

```bash
python ui_test_main.py --graph-editor
```

### 4. Run Everything

```bash
python ui_test_main.py --all --verbose
```

## Usage from Code

### Basic Usage

```python
from core.testing import quick_ui_test, full_ui_test

# Quick validation
if quick_ui_test():
    print("Basic UI functionality is working")

# Full test suite
if full_ui_test():
    print("All UI tests passed")
```

### Advanced Usage

```python
from core.testing import UITestRunner

runner = UITestRunner(headless=True, verbose=True)

# Run specific test categories
button_success = runner.run_button_tests()
graph_success = runner.run_graph_editor_tests()
comprehensive_success = runner.run_comprehensive_tests()
```

### Direct Component Testing

```python
from core.testing import SimpleUITester

tester = SimpleUITester(headless=True)

# Setup test environment
if tester.setup_test_environment():
    # Test specific components
    button_results = tester.test_workbench_buttons()
    graph_results = tester.test_graph_editor_interactions()
```

## CLI Interface

The framework provides a comprehensive CLI:

```bash
# Test specific button
python -m core.testing.ui_test_cli --button add_to_dictionary

# Test all buttons
python -m core.testing.ui_test_cli --all-buttons

# Test graph editor
python -m core.testing.ui_test_cli --graph-editor

# Run comprehensive tests
python -m core.testing.ui_test_cli --comprehensive

# Validate AI helper
python -m core.testing.ui_test_cli --ai-helper

# Run with verbose output
python -m core.testing.ui_test_cli --comprehensive --verbose
```

## Integration with Main Application

Add UI testing to your main application:

```python
from core.testing import handle_test_ui_command

# In your argument parser
parser.add_argument('--test-ui', action='store_true', help='Run UI tests')

# In your main function
if args.test_ui:
    success = handle_test_ui_command(args)
    if not success:
        sys.exit(1)
```

## Test Results and Reporting

The framework provides detailed test results:

- **Success/Failure Status**: Clear indication of test outcomes
- **Error Messages**: Detailed error information when tests fail
- **Legacy Guidance**: Automatic references to legacy code for debugging
- **Performance Metrics**: Execution time and performance data
- **Metadata**: Additional context about test execution

## Button Testing

Tests all 11 workbench buttons:

- `add_to_dictionary`: Add current sequence to dictionary
- `delete_beat`: Delete selected beat
- `clone_beat`: Clone selected beat
- `mirror_beat`: Mirror selected beat
- `rotate_beat`: Rotate selected beat
- `reset_beat`: Reset selected beat to default
- `generate_beat`: Generate new beat
- `add_beat`: Add new beat to sequence
- `export_image`: Export sequence as image
- `fullscreen`: Toggle fullscreen mode
- `settings`: Open settings dialog

## Graph Editor Testing

Tests core graph editor interactions:

- **Turn Adjustment**: Left/right click turn controls
- **Orientation Picker**: Click to cycle orientations
- **Keyboard Shortcuts**: WASD movement, X/Z/C commands
- **Hover Events**: Mouse enter/leave behavior
- **Focus Management**: Keyboard focus handling

## AI Agent Integration

The framework is designed to work seamlessly with AI agents:

- **Clear Console Output**: Rich, formatted output for AI understanding
- **Legacy Guidance**: Automatic references to legacy implementations
- **Error Context**: Detailed error messages with troubleshooting hints
- **Success Indicators**: Clear success/failure indicators
- **Metadata**: Additional context for AI decision-making

## Testing Strategy

The framework follows a systematic testing approach:

1. **Environment Setup**: Initialize test environment with real data
2. **Component Initialization**: Set up UI components using DI container
3. **Functional Testing**: Test core functionality with real interactions
4. **State Validation**: Verify state changes and proper behavior
5. **Error Handling**: Test error conditions and recovery
6. **Performance Measurement**: Track execution time and performance

## Common Issues and Solutions

### Button Not Responding

```
🔍 LEGACY GUIDANCE for button_name:
   📁 File: presentation/components/workbench/workbench.py
   ⚙️  Method: _on_button_clicked
   🔗 Signal: button.clicked.connect
   🐛 Common Issues:
      • Button not connected to signal
      • Service not resolved via DI
      • Validation failing on data
```

### Graph Editor Issues

```
🔍 CONTROL GUIDANCE for control_name:
   📋 Description: Control description
   🎯 Expected: Expected behavior
   🐛 Common Issues:
      • Control not connected to beat data
      • Immutable update not implemented
      • UI not reflecting changes
```

## Contributing

When adding new tests:

1. Follow TKA architectural patterns
2. Use dependency injection via ApplicationFactory
3. Respect domain model immutability
4. Provide clear AI agent guidance
5. Include legacy code references
6. Add comprehensive error handling

## Files

- `simple_ui_tester.py`: Main testing orchestrator
- `component_initializer.py`: UI component initialization
- `button_tester.py`: Button testing with legacy guidance
- `graph_editor_tester.py`: Graph editor interaction testing
- `ui_test_runner.py`: Integration layer for main application
- `ui_test_cli.py`: Command-line interface
- `ui_test_main.py`: Direct execution script
- `ai_agent_helpers.py`: AI agent testing utilities (existing)

## Requirements

- PyQt6 for UI testing
- TKA core services and domain models
- Existing TKA dependency injection framework
- Python 3.8+

## License

Part of the TKA project. See main project license.
