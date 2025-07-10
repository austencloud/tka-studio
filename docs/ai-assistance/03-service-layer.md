# 03 - TKA Service Layer Guide

## 🏢 SOPHISTICATED SERVICE ARCHITECTURE

TKA has enterprise-grade service implementations with command patterns, event publishing, and advanced business logic. AI agents must understand and use these existing services.

## 🎯 CORE SERVICE INTERFACES

### `ISequenceManager` - Sequence Operations

**Location**: `core/interfaces/core_services.py`
**Implementation**: `application/services/core/sequence_management_service.py`

This service already has a sophisticated command pattern with undo/redo:

```python
# Basic CRUD operations
def create_sequence(self, name: str, length: int = 16) -> SequenceData
def add_beat(self, sequence: SequenceData, beat: BeatData, position: int) -> SequenceData
def remove_beat(self, sequence: SequenceData, position: int) -> SequenceData
def generate_sequence(self, sequence_type: str, length: int, **kwargs) -> SequenceData
def apply_workbench_operation(self, sequence: SequenceData, operation: str, **kwargs) -> SequenceData

# Command pattern with undo/redo (ALREADY IMPLEMENTED)
def create_sequence_with_events(self, name: str, length: int = 16) -> SequenceData
def add_beat_with_undo(self, beat: BeatData, position: Optional[int] = None) -> SequenceData
def remove_beat_with_undo(self, position: int) -> SequenceData
def update_beat_with_undo(self, beat_number: int, field_name: str, new_value: Any) -> SequenceData

# Undo/Redo operations (ALREADY IMPLEMENTED)
def undo_last_operation(self) -> Optional[SequenceData]
def redo_last_operation(self) -> Optional[SequenceData]
def can_undo(self) -> bool
def can_redo(self) -> bool
def get_undo_description(self) -> Optional[str]
def get_redo_description(self) -> Optional[str]

# State management
def set_current_sequence(self, sequence: SequenceData) -> None
def get_current_sequence(self) -> Optional[SequenceData]
```

**Usage Example**:

```python
# Get service via DI
container = ApplicationFactory.create_test_app()
service = container.resolve(ISequenceManager)

# Use existing command pattern
sequence = service.create_sequence("Test Sequence", 8)
service.set_current_sequence(sequence)

# Add beat with undo capability
beat_data = BeatData(beat_number=1, letter="A")
updated_sequence = service.add_beat_with_undo(beat_data, 0)

# Test undo functionality
if service.can_undo():
    service.undo_last_operation()
    print(f"Undid: {service.get_undo_description()}")
```

### `IPictographManagementService` - Pictograph Operations

**Location**: `core/interfaces/core_services.py`
**Implementation**: `application/services/core/pictograph_management_service.py`

This service has sophisticated dataset management and CSV integration:

```python
# Basic operations
def create_pictograph(self, grid_mode: GridMode = GridMode.DIAMOND) -> PictographData
def create_from_beat(self, beat_data: BeatData) -> PictographData
def update_pictograph_arrows(self, pictograph: PictographData, arrows: Dict[str, ArrowData]) -> PictographData
def search_dataset(self, query: PictographSearchQuery) -> List[PictographData]

# Dataset management (SOPHISTICATED FEATURES)
def get_pictographs_by_letter(self, letter: str) -> List[BeatData]
def get_specific_pictograph(self, letter: str, index: int = 0) -> Optional[BeatData]
def get_start_position_pictograph(self, position_key: str, grid_mode: str = "diamond") -> Optional[BeatData]
def load_csv_data(self, file_path: Path, category: str = "user_created") -> List[PictographData]

# Context management
def configure_for_context(self, pictograph: PictographData, context: PictographContext) -> PictographData
def get_glyph_for_pictograph(self, pictograph: PictographData) -> Optional[str]
def add_to_dataset(self, pictograph: PictographData, category: str = "user_created") -> str
```

**Advanced Usage**:

```python
# CSV dataset integration (ALREADY WORKING)
service = container.resolve(IPictographManagementService)

# Get pictographs from CSV data
pictographs_for_A = service.get_pictographs_by_letter("A")
specific_pictograph = service.get_specific_pictograph("A", index=0)

# Create pictograph from beat data
beat_data = BeatData(beat_number=1, letter="A", blue_motion=motion_data)
pictograph = service.create_from_beat(beat_data)

# Search dataset
query = {"letter": "A", "motion_type": "pro", "max_results": 10}
results = service.search_dataset(query)
```

### `ILayoutService` - Layout Management

**Location**: `core/interfaces/core_services.py`
**Implementation**: `application/services/layout/layout_management_service.py`

Unified interface for all layout operations:

```python
# Basic layout
def get_main_window_size(self) -> Size
def get_workbench_size(self) -> Size
def get_picker_size(self) -> Size
def get_layout_ratio(self) -> tuple[int, int]
def set_layout_ratio(self, ratio: tuple[int, int]) -> None
def calculate_component_size(self, component_type: str, parent_size: Size) -> Size

# Advanced layout calculations
def calculate_beat_frame_layout(self, sequence: Any, container_size: Tuple[int, int]) -> Dict[str, Any]
def calculate_responsive_scaling(self, content_size: Tuple[int, int], container_size: Tuple[int, int]) -> float
def get_optimal_grid_layout(self, item_count: int, container_size: Tuple[int, int]) -> Tuple[int, int]
def calculate_component_positions(self, layout_config: Dict[str, Any]) -> Dict[str, Tuple[int, int]]
```

### Other Important Services

#### `IValidationService`

```python
def validate_sequence(self, sequence_data: Dict[str, Any]) -> bool
def validate_beat(self, beat_data: Dict[str, Any]) -> bool
def validate_motion(self, motion_data: Dict[str, Any]) -> bool
def get_validation_errors(self, data: Dict[str, Any]) -> List[str]
```

#### `IArrowManagementService`

```python
def calculate_arrow_position(self, arrow_data: Any, pictograph_data: Any) -> Tuple[float, float, float]
def should_mirror_arrow(self, arrow_data: Any) -> bool
def apply_beta_positioning(self, beat_data: Any) -> Any
def calculate_all_arrow_positions(self, pictograph_data: Any) -> Any
```

## 🏭 APPLICATION FACTORY INTEGRATION

### Service Resolution Pattern

```python
# CORRECT: Use ApplicationFactory
from core.application.application_factory import ApplicationFactory

# For AI testing
container = ApplicationFactory.create_test_app()
sequence_service = container.resolve(ISequenceManager)
pictograph_service = container.resolve(IPictographManagementService)

# For production
container = ApplicationFactory.create_production_app()
layout_service = container.resolve(ILayoutService)

# For headless processing
container = ApplicationFactory.create_headless_app()
validation_service = container.resolve(IValidationService)
```

### Available Service Configurations

#### Test Mode Services

- Mock implementations for fast testing
- In-memory storage
- Predictable behavior
- No external dependencies

```python
test_container = ApplicationFactory.create_test_app()
# Contains: MockLayoutService, InMemorySequenceDataService, etc.
```

#### Production Mode Services

- Full implementations with PyQt UI
- File-based persistence
- Real CSV dataset integration
- Complete functionality

```python
prod_container = ApplicationFactory.create_production_app()
# Contains: LayoutManagementService, FileSequenceDataService, etc.
```

#### Headless Mode Services

- Real business logic
- No UI dependencies
- Server-side processing capable
- Performance optimized

```python
headless_container = ApplicationFactory.create_headless_app()
# Contains: Real services without UI components
```

## 🎯 ADVANCED SERVICE PATTERNS

### Event-Driven Architecture

Services publish events automatically:

```python
# Events are published by service operations
service.create_sequence_with_events("Test", 8)
# Publishes: SequenceCreatedEvent

service.add_beat_with_undo(beat_data, 0)
# Publishes: BeatAddedEvent

# Subscribe to events (if event system available)
if hasattr(service, 'event_bus'):
    service.event_bus.subscribe(SequenceCreatedEvent, handle_sequence_created)
```

### Repository Pattern Integration

Services use repositories for persistence:

```python
# Services automatically handle persistence
sequence = service.create_sequence("Test", 8)
# Automatically saved via SequenceRepository

# Access current sequence from storage
current = service.get_current_sequence_from_storage()
service.set_current_sequence_in_storage(sequence.id)
```

### Workbench Operations

Sophisticated transformation operations:

```python
# Available workbench operations
operations = [
    "color_swap",
    "horizontal_reflection",
    "vertical_reflection",
    "rotation_90",
    "rotation_180",
    "rotation_270",
    "reverse_sequence"
]

# Apply transformations
transformed = service.apply_workbench_operation(sequence, "color_swap")
rotated = service.apply_workbench_operation(sequence, "rotation_90")
```

### Sequence Generation Algorithms

Multiple generation strategies available:

```python
# Generation types
generation_types = [
    "freeform",      # Random valid motions
    "circular",      # End connects to beginning
    "auto_complete", # Pattern recognition
    "mirror",        # Palindromic pattern
    "continuous"     # Flowing transitions
]

# Generate sequences
freeform_seq = service.generate_sequence("freeform", 16)
circular_seq = service.generate_sequence("circular", 12)
```

## 🧪 SERVICE TESTING PATTERNS

### AI Agent Testing

```python
# Use TKAAITestHelper for simplified access
from core.testing.ai_agent_helpers import TKAAITestHelper

helper = TKAAITestHelper(use_test_mode=True)

# Test sequence operations
result = helper.create_sequence("Test", 8)
assert result.success

# Test existing command pattern
cmd_result = helper.test_existing_command_pattern()
assert cmd_result.metadata['command_pattern_available']

# Test pictograph operations
picto_result = helper.test_pictograph_from_beat()
assert picto_result.success
```

### Direct Service Testing

```python
# For more control, use services directly
container = ApplicationFactory.create_test_app()
service = container.resolve(ISequenceManager)

# Test with real domain models
sequence = service.create_sequence("Direct Test", 4)
assert isinstance(sequence, SequenceData)
assert sequence.length == 4

# Test command pattern
if hasattr(service, 'add_beat_with_undo'):
    beat = BeatData(beat_number=1, letter="A")
    updated = service.add_beat_with_undo(beat, 0)
    assert service.can_undo()
```

## 🚨 SERVICE USAGE WARNINGS

### DON'T:

```python
# ❌ Create service instances directly
service = SequenceManager()  # Missing dependencies

# ❌ Mock complex services unnecessarily
mock_service = Mock(spec=ISequenceManager)  # Use real test services

# ❌ Ignore existing command pattern
service.add_beat(sequence, beat, 0)  # When add_beat_with_undo exists

# ❌ Bypass validation
service.save_invalid_sequence(bad_data)  # Services validate automatically
```

### DO:

```python
# ✅ Use dependency injection
container = ApplicationFactory.create_test_app()
service = container.resolve(ISequenceManager)

# ✅ Use existing sophisticated features
service.add_beat_with_undo(beat, position)  # Uses command pattern
service.undo_last_operation()  # Uses existing undo

# ✅ Leverage dataset integration
pictographs = pictograph_service.get_pictographs_by_letter("A")

# ✅ Use appropriate app mode for context
test_container = ApplicationFactory.create_test_app()      # For testing
prod_container = ApplicationFactory.create_production_app()  # For real usage
```

## 📊 SERVICE PERFORMANCE

### Test Services

- Execute in microseconds
- In-memory operations
- Predictable performance
- No I/O overhead

### Production Services

- File system integration
- CSV dataset loading
- UI component interaction
- Event publishing overhead

### Headless Services

- Real business logic
- Optimized for batch processing
- No UI rendering overhead
- Suitable for automation

## 🎯 KEY TAKEAWAYS FOR AI AGENTS

1. **Sophisticated Services Exist**: Don't recreate what's already implemented
2. **Command Pattern Available**: Use existing undo/redo functionality
3. **Dataset Integration Working**: Leverage CSV pictograph data
4. **Multiple App Modes**: Choose appropriate mode for your use case
5. **Validation Built-in**: Services automatically validate domain objects
6. **Event System Available**: Services publish events for state changes
7. **Repository Pattern**: Persistence is handled automatically

**Use these sophisticated services through dependency injection and leverage their advanced features rather than working around them.**
