# TKA End-to-End Testing Framework

A comprehensive framework for testing complete user workflows in the TKA application, from UI interactions to data model updates.

## Overview

This framework provides:
- **Reusable base classes** for common E2E test functionality
- **Component discovery** that automatically finds UI components
- **Test isolation** to prevent interference between tests
- **Comprehensive reporting** with detailed success/failure information
- **Extensible architecture** for adding new workflow tests

## Framework Structure

```
tests/e2e/
├── __init__.py                          # Package initialization
├── README.md                            # This documentation
├── base_e2e_test.py                     # Base class for all E2E tests
├── test_runner.py                       # Test execution and reporting
├── test_start_position_transfer.py      # Start position → option picker workflow
└── test_sequence_building_workflow.py   # Complete sequence building workflow
```

## Quick Start

### Running All Tests

```bash
# From the TKA root directory
python tests/e2e/test_runner.py
```

### Running a Specific Test

```bash
# Run just the start position transfer test
python tests/e2e/test_runner.py --test test_start_position_transfer

# Run just the sequence building workflow test
python tests/e2e/test_runner.py --test test_sequence_building_workflow
```

### Listing Available Tests

```bash
python tests/e2e/test_runner.py --list
```

### Running Individual Tests

```bash
# Run a test directly
python tests/e2e/test_start_position_transfer.py
```

## Available Tests

### 1. Start Position Transfer Test (`test_start_position_transfer.py`)

**Purpose**: Validates the workflow from start position selection to option picker population.

**What it tests**:
- Start position selection triggers option picker population
- UI transitions correctly between views
- Data models are updated properly
- Option picker contains valid options

**Key phases**:
1. Analyze initial state
2. Select a start position
3. Verify option picker population
4. Validate UI transitions
5. Verify data model consistency

### 2. Sequence Building Workflow Test (`test_sequence_building_workflow.py`)

**Purpose**: Validates the complete sequence building process from start to finish.

**What it tests**:
- Start position selection
- Multiple option selections to build a sequence
- Workbench updates after each selection
- Sequence data consistency
- Sequence management operations (clear, rebuild)

**Key phases**:
1. Initialize sequence building
2. Build sequence incrementally
3. Validate final sequence
4. Test sequence management

## Creating New Tests

### 1. Inherit from BaseE2ETest

```python
from base_e2e_test import BaseE2ETest

class MyWorkflowTest(BaseE2ETest):
    def __init__(self):
        super().__init__("My Workflow")
    
    def execute_test_logic(self) -> bool:
        # Implement your test logic here
        return True
```

### 2. Implement Test Logic

The `execute_test_logic()` method should contain your test-specific workflow:

```python
def execute_test_logic(self) -> bool:
    try:
        # Phase 1: Setup
        if not self._setup_test_conditions():
            return False
        
        # Phase 2: Execute workflow
        if not self._execute_workflow():
            return False
        
        # Phase 3: Validate results
        if not self._validate_results():
            return False
        
        return True
    except Exception as e:
        logger.error(f"ERROR: Test failed: {e}")
        return False
```

### 3. Add Run Function

```python
def run_my_workflow_test():
    """Run the my workflow test."""
    test = MyWorkflowTest()
    success = test.run_test()
    
    if success:
        print("\nSUCCESS: MY WORKFLOW TEST PASSED!")
    else:
        print("\nFAILED: MY WORKFLOW TEST FAILED!")
    
    return success

if __name__ == "__main__":
    success = run_my_workflow_test()
    sys.exit(0 if success else 1)
```

### 4. Test Discovery

The test runner automatically discovers tests by:
1. Looking for files matching `test_*.py`
2. Finding run functions matching `run_{test_name}_test()`

## Base Class Features

### Application Management
- `setup_application()`: Creates and initializes the TKA application
- `find_construct_tab()`: Navigates to the construct tab
- `discover_components()`: Finds key UI components
- `cleanup()`: Proper resource cleanup

### Component Access
- `self.start_position_picker`: Reference to start position picker
- `self.option_picker`: Reference to option picker  
- `self.workbench`: Reference to sequence workbench
- `self.construct_tab`: Reference to construct tab

### Utility Methods
- `wait_for_ui(milliseconds)`: Wait for UI updates
- `add_cleanup_callback(callback)`: Register cleanup functions

## Component Discovery

The framework uses multiple strategies to find UI components:

1. **Direct class name matching** (e.g., "StartPositionPicker")
2. **Partial name matching** (e.g., "start" + "position" + "picker")
3. **Method/attribute detection** (e.g., `hasattr(widget, 'select_position')`)

This robust discovery ensures tests work even if component names change.

## Error Handling

- **Comprehensive logging** at INFO level for normal operation
- **Detailed error messages** with stack traces for failures
- **Graceful degradation** when components aren't found
- **Proper cleanup** even when tests fail

## Test Isolation

Each test runs in complete isolation:
- Fresh application instance for each test
- Proper cleanup between tests
- No shared state between tests
- Independent result reporting

## Extending the Framework

### Adding New Component Types

To add support for new UI components, extend the base class:

```python
def _find_key_components(self, all_children: List[QObject]):
    super()._find_key_components(all_children)
    
    # Add your component discovery logic
    for widget in all_children:
        if self._is_my_component(widget.__class__.__name__.lower()):
            self.my_component = widget
            logger.info(f"FOUND: My component: {widget.__class__.__name__}")
```

### Adding New Interaction Methods

Add reusable interaction methods to the base class:

```python
def trigger_my_action(self, parameter: str) -> bool:
    """Trigger a custom action with multiple strategies."""
    try:
        # Strategy 1: Direct method
        if hasattr(self.my_component, 'my_action'):
            self.my_component.my_action(parameter)
            return True
        
        # Strategy 2: Signal emission
        if hasattr(self.my_component, 'my_signal'):
            self.my_component.my_signal.emit(parameter)
            return True
        
        # Strategy 3: Fallback
        logger.info(f"SIMULATED: My action with {parameter}")
        return True
        
    except Exception as e:
        logger.error(f"ERROR: Failed to trigger action: {e}")
        return False
```

## Best Practices

1. **Use descriptive test names** that clearly indicate what's being tested
2. **Break tests into logical phases** for easier debugging
3. **Log important state changes** to aid in troubleshooting
4. **Handle missing components gracefully** with fallback strategies
5. **Wait for UI updates** after triggering actions
6. **Validate both UI and data model state** for comprehensive testing
7. **Clean up resources** properly to prevent Qt object warnings

## Troubleshooting

### Common Issues

**Test fails to find components**:
- Check that the application is fully initialized (increase wait time)
- Verify component names haven't changed
- Add debug logging to see what components are found

**Qt object deletion warnings**:
- Ensure proper cleanup in test teardown
- Add cleanup callbacks for custom resources
- Check that components aren't accessed after window closure

**Tests interfere with each other**:
- Verify each test creates a fresh application instance
- Check that cleanup is properly executed
- Ensure no global state is shared between tests

### Debug Logging

Enable more detailed logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

This will show component discovery details and interaction attempts.
