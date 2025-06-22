# Writing TKA Tests

## Overview

This guide covers the standards and best practices for writing tests in the TKA project. Follow these guidelines to ensure consistent, maintainable, and effective tests.

## Directory Placement

### Decision Tree

1. **What platform?**

   - Desktop → `tests/desktop/`
   - Web → `tests/web/`

2. **What version?** (for desktop)

   - Legacy → `tests/desktop/legacy/`
   - Modern → `tests/desktop/modern/`
   - Launcher → `tests/desktop/launcher/`

3. **What type?**
   - Unit → `unit/`
   - Integration → `integration/`
   - Specification → `specification/`

### Examples

```
# Modern desktop unit test
tests/desktop/modern/unit/application/services/test_graph_editor_service.py

# Legacy desktop integration test
tests/desktop/legacy/integration/test_sequence_workflow.py

# Web API integration test
tests/web/integration/test_sequence_api.py

# Launcher unit test
tests/desktop/launcher/test_card_component.py
```

## File Naming Conventions

### Test Files

- **Pattern**: `test_*.py`
- **Descriptive**: Use clear, descriptive names
- **Component-based**: Match the component being tested

```python
# Good
test_graph_editor_service.py
test_sequence_creation_workflow.py
test_beat_frame_layout.py

# Avoid
test_stuff.py
test1.py
my_test.py
```

### Test Functions

- **Pattern**: `test_*`
- **Behavior-focused**: Describe what behavior is being tested
- **Clear and specific**: Anyone should understand what the test does

```python
# Good
def test_beat_selection_updates_graph_editor():
def test_invalid_sequence_length_raises_error():
def test_pictograph_export_creates_correct_file():

# Avoid
def test_function():
def test_case1():
def test_bug_fix():
```

### Test Classes

- **Pattern**: `Test*`
- **Grouped behavior**: Use classes to group related tests
- **Component-focused**: Name after the component being tested

```python
# Good
class TestGraphEditorService:
class TestSequenceCreationWorkflow:
class TestBeatFrameLayout:

# Avoid
class MyTests:
class TestCase1:
```

## Test Structure

### AAA Pattern

Follow the **Arrange, Act, Assert** pattern:

```python
def test_beat_selection_updates_graph_editor():
    # Arrange
    sequence_data = create_test_sequence(length=4)
    graph_editor = GraphEditor(sequence_data)
    target_beat = sequence_data.beats[2]

    # Act
    graph_editor.select_beat(target_beat)

    # Assert
    assert graph_editor.selected_beat == target_beat
    assert graph_editor.is_beat_highlighted(target_beat)
```

### Given-When-Then (for complex tests)

```python
def test_sequence_export_with_custom_layout():
    # Given a sequence with custom beat layouts
    sequence = SequenceBuilder().with_length(4).with_custom_layouts().build()
    exporter = SequenceExporter(format="json")

    # When exporting the sequence
    result = exporter.export(sequence)

    # Then the exported data contains layout information
    assert "custom_layouts" in result
    assert len(result["beats"]) == 4
    assert result["custom_layouts"]["beat_1"]["layout_type"] == "diamond"
```

## Test Types and Standards

### Unit Tests

**Purpose**: Test individual components in isolation

**Standards**:

- Fast execution (< 1 second)
- No external dependencies (files, network, database)
- Mock all dependencies
- Focus on single component

**Markers**: `@pytest.mark.unit`

```python
@pytest.mark.unit
@pytest.mark.modern
@pytest.mark.desktop
def test_graph_editor_service_calculates_beat_positions():
    # Mock dependencies
    mock_layout_service = Mock()
    mock_layout_service.get_beat_layout.return_value = DiamondLayout()

    # Test the service in isolation
    service = GraphEditorService(layout_service=mock_layout_service)
    positions = service.calculate_beat_positions(sequence_length=4)

    assert len(positions) == 4
    assert all(isinstance(pos, Position) for pos in positions)
```

### Integration Tests

**Purpose**: Test component interactions

**Standards**:

- Medium execution time (1-10 seconds)
- Real dependencies within component boundary
- Mock external system dependencies
- Test component collaborations

**Markers**: `@pytest.mark.integration`

```python
@pytest.mark.integration
@pytest.mark.modern
@pytest.mark.desktop
def test_sequence_creation_workflow():
    # Use real services that work together
    container = create_test_container()
    sequence_service = container.resolve(SequenceService)
    beat_service = container.resolve(BeatService)

    # Test the workflow
    sequence = sequence_service.create_sequence(length=4)
    beat = beat_service.create_beat(motion_type="pro")
    sequence_service.add_beat(sequence, beat, position=0)

    assert sequence.length == 4
    assert sequence.beats[0] == beat
```

### Specification Tests

**Purpose**: Verify requirements and contracts

**Standards**:

- Test against documented specifications
- Can be unit or integration style
- Focus on behavior, not implementation
- Include requirement traceability

**Markers**: `@pytest.mark.specification`

```python
@pytest.mark.specification
@pytest.mark.modern
@pytest.mark.desktop
def test_sequence_creation_meets_specification():
    """
    Requirement: SEQ-001 - Sequence Creation
    A sequence must have:
    - A unique identifier
    - A positive integer length
    - An empty beats collection initially
    """
    sequence = SequenceService.create_sequence(length=4)

    # SEQ-001.1: Unique identifier
    assert sequence.id is not None
    assert isinstance(sequence.id, str)
    assert len(sequence.id) > 0

    # SEQ-001.2: Positive integer length
    assert sequence.length == 4
    assert isinstance(sequence.length, int)

    # SEQ-001.3: Empty beats collection
    assert len(sequence.beats) == 0
    assert isinstance(sequence.beats, list)
```

## Test Markers

### Platform Markers

```python
@pytest.mark.desktop    # Desktop application test
@pytest.mark.web        # Web application test
```

### Version Markers

```python
@pytest.mark.legacy     # Legacy desktop test
@pytest.mark.modern     # Modern desktop test
@pytest.mark.launcher   # Launcher test
```

### Type Markers

```python
@pytest.mark.unit           # Unit test
@pytest.mark.integration    # Integration test
@pytest.mark.specification  # Specification test
```

### Special Markers

```python
@pytest.mark.slow       # Slow test (>5 seconds)
@pytest.mark.ui         # UI test requiring display
@pytest.mark.imports    # Import validation test
```

### Combining Markers

```python
@pytest.mark.unit
@pytest.mark.modern
@pytest.mark.desktop
def test_modern_desktop_component():
    pass
```

## Fixtures and Test Data

### Using Shared Fixtures

```python
def test_with_shared_data(sample_sequence_data):
    """Use shared fixture from conftest.py"""
    assert sample_sequence_data.length > 0

def test_with_mock_container(mock_container):
    """Use shared mock container"""
    service = mock_container.resolve(SomeService)
    assert service is not None
```

### Creating Test-Specific Data

```python
def test_with_custom_data():
    """Create data specific to this test"""
    sequence = create_mock_sequence_data(
        length=8,
        beats=[
            create_mock_beat_data(motion_type="pro"),
            create_mock_beat_data(motion_type="anti")
        ]
    )
    assert sequence.length == 8
```

### Loading Test Data Files

```python
def test_with_json_data():
    """Load data from shared test data files"""
    sequences = load_test_data("sample_sequences.json")
    simple_sequence = sequences["simple_sequence"]
    assert simple_sequence["length"] == 2
```

## Mocking Guidelines

### Mock External Dependencies

```python
@patch('src.desktop.modern.services.file_service.FileService')
def test_sequence_save(mock_file_service):
    mock_file_service.save.return_value = True

    service = SequenceService(file_service=mock_file_service)
    result = service.save_sequence(sequence)

    assert result is True
    mock_file_service.save.assert_called_once()
```

### Use Dependency Injection

```python
def test_with_injected_mocks():
    # Create mocks
    mock_repository = Mock()
    mock_validator = Mock()

    # Inject into service
    service = SequenceService(
        repository=mock_repository,
        validator=mock_validator
    )

    # Test with controlled dependencies
    mock_validator.validate.return_value = True
    service.create_sequence(length=4)

    mock_validator.validate.assert_called_once()
```

### Mock Return Values Realistically

```python
def test_with_realistic_mocks():
    mock_service = Mock()

    # Return realistic data structure
    mock_service.get_sequence.return_value = SequenceData(
        id="test_001",
        length=4,
        beats=[]
    )

    # Test with realistic mock
    result = mock_service.get_sequence("test_001")
    assert isinstance(result, SequenceData)
```

## Error Testing

### Test Exception Cases

```python
def test_invalid_sequence_length_raises_error():
    with pytest.raises(ValueError, match="Length must be positive"):
        SequenceService.create_sequence(length=-1)

def test_missing_file_raises_specific_error():
    with pytest.raises(FileNotFoundError) as exc_info:
        SequenceService.load_from_file("nonexistent.json")

    assert "nonexistent.json" in str(exc_info.value)
```

### Test Error Messages

```python
def test_validation_error_message():
    try:
        invalid_sequence = SequenceData(length=0, beats=[])
        SequenceValidator.validate(invalid_sequence)
        pytest.fail("Expected ValidationError")
    except ValidationError as e:
        assert "length must be greater than 0" in str(e)
```

## Performance Testing

### Mark Slow Tests

```python
@pytest.mark.slow
def test_large_sequence_processing():
    """Test that takes more than 5 seconds"""
    large_sequence = create_sequence_with_beats(length=1000)
    result = process_sequence(large_sequence)
    assert result is not None
```

### Performance Assertions

```python
import time

def test_sequence_creation_performance():
    start_time = time.time()

    sequence = SequenceService.create_sequence(length=100)

    end_time = time.time()
    assert end_time - start_time < 1.0  # Should complete in under 1 second
```

## UI Testing (Desktop)

### Using pytest-qt

```python
@pytest.mark.ui
@pytest.mark.desktop
def test_beat_selection_ui(qtbot):
    widget = GraphEditorWidget()
    qtbot.addWidget(widget)

    # Simulate user interaction
    qtbot.mouseClick(widget.beat_frames[0], Qt.LeftButton)

    # Check UI state
    assert widget.selected_beat_index == 0
    assert widget.beat_frames[0].is_selected
```

### Testing Widget State

```python
@pytest.mark.ui
def test_sequence_display_updates(qtbot):
    widget = SequenceWidget()
    qtbot.addWidget(widget)

    # Set up test data
    sequence = create_test_sequence(length=4)

    # Trigger update
    widget.display_sequence(sequence)

    # Verify UI reflects data
    assert widget.length_label.text() == "4"
    assert len(widget.beat_widgets) == 4
```

## Common Patterns

### Builder Pattern for Test Data

```python
class SequenceTestBuilder:
    def __init__(self):
        self.length = 4
        self.beats = []

    def with_length(self, length):
        self.length = length
        return self

    def with_beat(self, beat_data):
        self.beats.append(beat_data)
        return self

    def build(self):
        return SequenceData(
            id=f"test_{uuid.uuid4()}",
            length=self.length,
            beats=self.beats
        )

# Usage
def test_with_builder():
    sequence = (SequenceTestBuilder()
                .with_length(8)
                .with_beat(create_pro_beat())
                .with_beat(create_anti_beat())
                .build())
```

### Parameterized Tests

```python
@pytest.mark.parametrize("length,expected_beats", [
    (2, 2),
    (4, 4),
    (8, 8),
])
def test_sequence_creation_with_various_lengths(length, expected_beats):
    sequence = SequenceService.create_sequence(length=length)
    assert sequence.length == length
    # Additional assertions...
```

### Setup and Teardown

```python
class TestGraphEditor:
    def setup_method(self):
        """Run before each test method"""
        self.container = create_test_container()
        self.service = self.container.resolve(GraphEditorService)

    def teardown_method(self):
        """Run after each test method"""
        self.container.dispose()

    def test_beat_selection(self):
        # Test implementation using self.service
        pass
```

## Documentation in Tests

### Test Docstrings

```python
def test_sequence_export_includes_metadata():
    """
    Test that sequence export includes all required metadata.

    Given a sequence with beats and custom properties,
    when exporting to JSON format,
    then the result should include:
    - Sequence metadata (id, length, created_date)
    - Beat data for each beat
    - Custom properties if present

    Related: REQ-EXPORT-001
    """
    # Test implementation
```

### Inline Comments

```python
def test_complex_workflow():
    # Arrange: Create a sequence with specific beat patterns
    sequence = create_complex_sequence()

    # Act: Process through the workflow
    result = workflow_processor.process(sequence)

    # Assert: Verify each step was completed correctly
    assert result.step1_completed
    assert result.step2_completed
    assert result.final_output is not None
```

## Best Practices Summary

### Do:

- Use descriptive names for tests, files, and classes
- Follow the AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Use appropriate markers
- Test both happy path and error cases
- Keep tests focused and independent
- Use shared fixtures and utilities
- Document complex test logic

### Don't:

- Test implementation details
- Create tests that depend on other tests
- Use hard-coded values without explanation
- Mock everything (some integration is good)
- Write tests that are slower than necessary
- Ignore failing tests
- Test getters/setters without logic
- Create overly complex test setups

### Guidelines:

- One assertion per test (when practical)
- Prefer many small tests over few large tests
- Test edge cases and error conditions
- Use realistic test data
- Make tests readable as documentation
- Refactor tests when code changes
- Maintain test code quality like production code
