# TKA Modern Image Export Testing Framework

## Overview

This comprehensive testing framework is designed to detect visual regressions, service registration failures, and UI workflow inconsistencies in the Modern image export system. It addresses specific issues that have been problematic:

- **Font sizing problems**: "humongous" word labels and difficulty labels due to incorrect beat_scale calculations
- **Missing visual elements**: grids, props, and arrows not rendering due to service registration gaps
- **Beat positioning inaccuracies**: in exported images
- **Container switching issues**: where pictograph scenes can't access required services

## Framework Architecture

### 1. UI Automation (`ui_automation/`)

Provides automated UI interaction and validation capabilities:

- **`PickerNavigator`**: Automate StartPositionPicker and OptionPicker interactions
- **`BeatFrameValidator`**: Validate BeatFrame state and pictograph rendering
- **`WorkbenchController`**: Orchestrate complete workflow automation

### 2. Visual Regression Detection (`visual_regression/`)

Comprehensive visual regression detection capabilities:

- **`ImageComparator`**: Pixel-perfect Legacy vs Modern comparison
- **`FontSizeValidator`**: Specific font size regression prevention
- **`VisualElementDetector`**: Detection of grids, props, arrows, and other elements

### 3. Service Validation (`service_validation/`)

Service container and registration validation:

- **`ContainerInspector`**: Verify service registration completeness
- **`ServiceRegistrationValidator`**: Validate service resolution and availability

## Quick Start

### Basic Usage

```python
import pytest
from tests.framework.ui_automation import WorkbenchController, SequenceSpec
from tests.framework.visual_regression import FontSizeValidator, ImageComparator
from tests.framework.service_validation import ContainerInspector

# Test font sizing regression
def test_font_sizing():
    font_validator = FontSizeValidator(tolerance_percentage=10.0)
    
    # Validate word label size is within expected range
    is_valid = font_validator.validate_word_label_size(
        "exported_image.png", 
        expected_range=(50, 150)
    )
    assert is_valid, "Font size out of expected range"

# Test service registration
def test_service_registration():
    inspector = ContainerInspector()
    report = inspector.verify_export_services_registered(container)
    
    assert report.all_required_services_present, \
        f"Missing services: {report.missing_services}"

# Test complete workflow
def test_complete_workflow():
    controller = WorkbenchController(workbench_widget)
    
    sequence_spec = SequenceSpec(
        start_position="alpha1_alpha1",
        beats=[{"motion": "pro"}, {"motion": "anti"}],
        word="TEST"
    )
    
    result = controller.execute_complete_workflow(sequence_spec)
    assert result.success, f"Workflow failed: {result.errors}"
```

### Running the Comprehensive Test

```bash
# Run the comprehensive regression test
pytest tests/regression/test_comprehensive_export_regression.py -v

# Run specific test categories
pytest tests/regression/ -k "font_sizing" -v
pytest tests/regression/ -k "service_registration" -v
pytest tests/regression/ -k "visual_element" -v
```

## Test Categories

### 1. Font Sizing Regression Tests

Prevents "humongous" text issues by validating font sizes:

```python
def test_font_sizing_by_beat_count():
    """Test font scaling for different sequence lengths."""
    test_cases = [
        (1, (50, 90)),    # 1 beat: smallest fonts
        (2, (80, 130)),   # 2 beats: medium fonts  
        (4, (150, 200)),  # 4+ beats: full size fonts
    ]
    
    for beat_count, expected_range in test_cases:
        # Create and export sequence
        # Validate font sizes are within expected range
```

### 2. Service Registration Tests

Validates all required services are available:

```python
def test_export_services_available():
    """Ensure all export services are registered and resolvable."""
    required_services = [
        "IImageExportService",
        "IPictographRenderingService", 
        "IArrowPositioningOrchestrator",
        "IGridRenderingService",
        "IPropRenderingService"
    ]
    
    for service in required_services:
        assert container.can_resolve(service)
```

### 3. Visual Element Detection Tests

Ensures all visual elements are rendered:

```python
def test_visual_elements_present():
    """Verify grids, props, and arrows are rendered."""
    detector = VisualElementDetector()
    report = detector.detect_all_elements("exported_image.png")
    
    assert report.grids_detected, "Grids not detected in export"
    assert report.props_detected, "Props not detected in export"  
    assert report.arrows_detected, "Arrows not detected in export"
```

## Configuration

### Font Size Validation

Configure expected font size ranges based on sequence length:

```python
font_validator = FontSizeValidator(tolerance_percentage=10.0)

# Override expected ranges
font_validator.expected_ranges = {
    'word_label': {
        1: (40, 80),    # Custom range for 1 beat
        2: (70, 120),   # Custom range for 2 beats
        3: (140, 190),  # Custom range for 3+ beats
    }
}
```

### Image Comparison

Configure pixel comparison tolerance:

```python
comparator = ImageComparator(tolerance_percentage=5.0)
comparator.difference_threshold = 15  # Color difference threshold (0-255)
```

### Service Validation

Configure required services:

```python
inspector = ContainerInspector()

# Add custom required services
inspector.required_export_services.extend([
    "ICustomRenderingService",
    "ISpecialEffectsService"
])
```

## Dependencies

### Required
- PyQt6 (for UI automation and image handling)
- pytest (for test framework)

### Optional (Enhanced Features)
- PIL/Pillow (for advanced image comparison)
- OpenCV (for visual element detection)
- pytesseract (for OCR-based font size measurement)

### Installation

```bash
# Required dependencies
pip install PyQt6 pytest

# Optional dependencies for enhanced features
pip install Pillow opencv-python pytesseract
```

## Best Practices

### 1. Test Organization

- Use descriptive test names that indicate what regression is being prevented
- Group related tests in the same test class
- Use fixtures for common setup (containers, test data)

### 2. Assertion Messages

- Provide detailed assertion messages with actual vs expected values
- Include diagnostic information in failure messages

### 3. Test Data

- Use realistic sequence data that represents actual user workflows
- Test edge cases (1 beat, many beats, empty sequences)
- Include both simple and complex pictograph data

### 4. Performance

- Use session-scoped fixtures for expensive setup (QApplication, containers)
- Cache test images and reuse when possible
- Run visual regression tests separately from unit tests

## Troubleshooting

### Common Issues

1. **QApplication not found**: Ensure pytest-qt is installed and QApplication fixture is used
2. **Service resolution failures**: Check that all required services are registered in test container
3. **Image comparison failures**: Verify image paths exist and are readable
4. **Font size detection low confidence**: Install OCR dependencies for better text detection

### Debug Mode

Enable detailed logging for debugging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run tests with verbose output
pytest tests/regression/ -v -s --log-cli-level=DEBUG
```

## Contributing

When adding new tests to the framework:

1. Follow the existing patterns for test organization
2. Add comprehensive docstrings explaining what regression is being prevented
3. Include both positive and negative test cases
4. Update this README with new capabilities

## Future Enhancements

- Integration with CI/CD pipelines for automated regression detection
- Visual diff reporting with highlighted differences
- Performance benchmarking for export operations
- Automated baseline image generation and management
