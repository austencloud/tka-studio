# 05 - TKA Development Patterns

## 🏗️ CODING STANDARDS AND CONVENTIONS

TKA follows sophisticated development patterns with strict conventions for imports, error handling, code organization, and architectural boundaries.

## 📁 CODE ORGANIZATION PATTERNS

### Directory Structure Rules

```
src/desktop/modern/src/
├── core/                    # Framework-agnostic contracts and utilities
│   ├── interfaces/          # Service contracts (ABC classes)
│   ├── dependency_injection/ # DI container and registration
│   ├── types/              # Framework-agnostic data types
│   ├── events/             # Event system (pub/sub)
│   └── exceptions/         # Structured error handling
├── domain/                  # Pure business logic
│   ├── models/             # Immutable dataclasses
│   ├── services/           # Domain-specific business rules
│   └── repositories/       # Data access contracts
├── application/            # Use case orchestration
│   ├── services/           # Service implementations
│   └── orchestrators/      # Complex workflow coordination
├── infrastructure/         # External concerns
│   ├── storage/            # File system and persistence
│   ├── api/               # External service integration
│   └── test_doubles/      # Mock implementations
└── presentation/           # UI components
    ├── components/         # PyQt6 widgets
    └── factories/          # UI construction
```

### File Naming Conventions

```python
# Service implementations
sequence_management_service.py      # PascalCase class, snake_case file
pictograph_management_service.py

# Domain models
core_models.py                      # Multiple related models
pictograph_models.py               # Specific domain area

# Interfaces
core_services.py                   # Service interfaces
workbench_services.py             # Specific interface groups

# Test files
test_sequence_operations.py       # Unit tests
test_ai_agent_integration.py      # Integration tests
```

## 📥 IMPORT PATTERNS

### Context-Aware Import Rules

#### Desktop Internal Code (Clean Imports)

```python
# CORRECT: For code within src/desktop/modern/src/
from domain.models.core_models import BeatData, SequenceData
from core.interfaces.core_services import ILayoutService
from application.services.layout.layout_management_service import LayoutManagementService
from presentation.components.workbench import ModernSequenceWorkbench
```

#### External Code (Full Path Imports)

```python
# CORRECT: For tests, web, shared code
from desktop.domain.models.core_models import BeatData
from desktop.core.interfaces.core_services import ILayoutService
from desktop.application.services.layout.layout_management_service import LayoutManagementService
```

#### Shared/Root Level (Direct Imports)

```python
# CORRECT: For shared types and constants
from tka_types import MotionType, SharedSequenceType
from tka_constants import ENDPOINTS, API_BASE_URL
```

### Import Organization Standards

```python
# 1. Standard library imports
import sys
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

# 2. Third-party imports
import pytest
from PyQt6.QtWidgets import QWidget

# 3. Local application imports - organized by layer
# Core layer
from core.interfaces.core_services import ISequenceManager
from core.dependency_injection.di_container import DIContainer

# Domain layer
from domain.models.core_models import BeatData, SequenceData

# Application layer
from application.services.core.sequence_management_service import SequenceManager

# Infrastructure layer
from infrastructure.storage.sequence_repository import SequenceRepository

# Presentation layer
from presentation.components.sequence_workbench import SequenceWorkbench
```

## 🎯 DEPENDENCY INJECTION PATTERNS

### Service Constructor Pattern

```python
# CORRECT: Constructor injection with interfaces
class PictographEditorService:
    def __init__(self,
                 pictograph_service: IPictographManagementService,
                 validation_service: IValidationService,
                 layout_service: ILayoutService):
        self._pictograph_service = pictograph_service
        self._validation_service = validation_service
        self._layout_service = layout_service

    def edit_pictograph(self, pictograph_data: PictographData) -> PictographData:
        # Use injected services
        if not self._validation_service.validate_pictograph(pictograph_data):
            raise ValidationError("Invalid pictograph data")

        return self._pictograph_service.update_pictograph(pictograph_data)
```

### Service Registration Pattern

```python
# CORRECT: Register with interfaces
def configure_services(container: DIContainer):
    # Register implementations with interface contracts
    container.register_singleton(ISequenceManager, SequenceManager)
    container.register_singleton(IPictographManagementService, PictographManagementService)
    container.register_transient(IPictographEditor, PictographEditorService)

    # Validate registrations
    container.validate_all_registrations()
```

### Service Resolution Pattern

```python
# CORRECT: Resolve through container
class WorkbenchFactory:
    def __init__(self, container: DIContainer):
        self._container = container

    def create_workbench(self) -> SequenceWorkbench:
        # Resolve dependencies
        sequence_service = self._container.resolve(ISequenceManager)
        layout_service = self._container.resolve(ILayoutService)

        return SequenceWorkbench(sequence_service, layout_service)
```

## 🏛️ IMMUTABLE DATA PATTERNS

### Domain Model Update Pattern

```python
# CORRECT: Immutable updates
class SequenceEditor:
    def add_beat_to_sequence(self, sequence: SequenceData, beat: BeatData) -> SequenceData:
        # Validate first
        if not beat.is_valid():
            raise ValidationError("Invalid beat data")

        # Immutable operation
        updated_sequence = sequence.add_beat(beat)

        # Return new instance
        return updated_sequence

    def update_sequence_name(self, sequence: SequenceData, new_name: str) -> SequenceData:
        # Validate
        if not new_name.strip():
            raise ValidationError("Sequence name cannot be empty")

        # Immutable update
        return sequence.update(name=new_name)
```

### Batch Update Pattern

```python
# CORRECT: Efficient batch updates
def apply_multiple_updates(self, sequence: SequenceData, updates: List[Dict]) -> SequenceData:
    current_sequence = sequence

    # Apply updates sequentially
    for update in updates:
        if update['type'] == 'add_beat':
            current_sequence = current_sequence.add_beat(update['beat'])
        elif update['type'] == 'update_name':
            current_sequence = current_sequence.update(name=update['name'])
        elif update['type'] == 'remove_beat':
            current_sequence = current_sequence.remove_beat(update['position'])

    return current_sequence
```

## ⚠️ ERROR HANDLING PATTERNS

### Structured Exception Hierarchy

```python
# Use TKA's structured exceptions
from core.exceptions import (
    TKAException,
    ValidationError,
    ServiceOperationError,
    DependencyInjectionError
)

# CORRECT: Specific exception types
class SequenceService:
    def create_sequence(self, name: str, length: int) -> SequenceData:
        if not name.strip():
            raise ValidationError("Sequence name cannot be empty")

        if length <= 0 or length > 64:
            raise ValidationError("Sequence length must be between 1 and 64")

        try:
            sequence = SequenceData(name=name, beats=[])
            return sequence
        except Exception as e:
            raise ServiceOperationError(f"Failed to create sequence: {e}") from e
```

### Error Handling Decorators

```python
# Use TKA's error handling decorators
from core.decorators import handle_service_errors, monitor_performance

class PictographService:
    @handle_service_errors("create_pictograph")
    @monitor_performance("pictograph_creation")
    def create_pictograph(self, grid_mode: GridMode) -> PictographData:
        # Service logic here
        return PictographData(grid_mode=grid_mode)
```

### Logging Patterns

```python
# CORRECT: Structured logging
from core.logging.structured_logger import get_logger

class ServiceImplementation:
    def __init__(self):
        self.logger = get_logger(__name__)

    def process_sequence(self, sequence: SequenceData) -> None:
        self.logger.info(
            "Processing sequence",
            extra={
                "sequence_id": sequence.id,
                "sequence_name": sequence.name,
                "beat_count": len(sequence.beats)
            }
        )

        try:
            # Process sequence
            self.logger.debug("Sequence processing completed successfully")
        except Exception as e:
            self.logger.error(
                "Sequence processing failed",
                extra={"error": str(e), "sequence_id": sequence.id}
            )
            raise
```

## 🎭 EVENT-DRIVEN PATTERNS

### Event Publishing Pattern

```python
# CORRECT: Event publishing in services
from core.events import get_event_bus, SequenceCreatedEvent

class SequenceManager:
    def __init__(self):
        self.event_bus = get_event_bus()

    def create_sequence_with_events(self, name: str, length: int) -> SequenceData:
        sequence = self.create_sequence(name, length)

        # Publish event
        event = SequenceCreatedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source="SequenceManager",
            sequence_id=sequence.id,
            sequence_name=sequence.name,
            sequence_length=sequence.length
        )

        self.event_bus.publish(event)
        return sequence
```

### Event Subscription Pattern

```python
# CORRECT: Event subscription
from core.events import get_event_bus, SequenceCreatedEvent

class SequenceStatisticsService:
    def __init__(self):
        self.event_bus = get_event_bus()
        self.event_bus.subscribe(SequenceCreatedEvent, self.handle_sequence_created)

    def handle_sequence_created(self, event: SequenceCreatedEvent) -> None:
        # Update statistics
        self.logger.info(f"New sequence created: {event.sequence_name}")
        self.update_sequence_count()
```

## 🧪 TESTING PATTERNS

### Test Class Organization

```python
# CORRECT: Organized test classes
@pytest.mark.specification
@pytest.mark.critical
class TestSequenceDataContract:
    """Permanent specification test - NEVER DELETE"""

    def setup_method(self):
        """Setup for each test method"""
        self.container = ApplicationFactory.create_test_app()
        self.service = self.container.resolve(ISequenceManager)

    def test_sequence_immutability_contract(self):
        """PERMANENT: Sequence operations must return new instances"""
        sequence = SequenceData(name="Test", beats=[])
        beat = BeatData(beat_number=1, letter="A")

        new_sequence = sequence.add_beat(beat)

        assert sequence is not new_sequence
        assert len(sequence.beats) == 0
        assert len(new_sequence.beats) == 1

    def test_sequence_validation_contract(self):
        """PERMANENT: Sequences must enforce business rules"""
        # Test business rule enforcement
        pass
```

### Fixture Usage Pattern

```python
# CORRECT: Use existing sophisticated fixtures
def test_sequence_operations(sample_sequence_data, sample_beat_data):
    """Test with real domain objects"""
    sequence = sample_sequence_data
    beat = sample_beat_data

    # Test with real objects, not mocks
    updated_sequence = sequence.add_beat(beat)
    assert updated_sequence.length == sequence.length + 1

def test_service_integration(configured_di_container):
    """Test with properly configured services"""
    container = configured_di_container
    service = container.resolve(ISequenceManager)

    # Test real service behavior
    sequence = service.create_sequence("Integration Test", 4)
    assert isinstance(sequence, SequenceData)
```

## 📊 PERFORMANCE PATTERNS

### Lazy Loading Pattern

```python
# CORRECT: Lazy service resolution
class WorkbenchController:
    def __init__(self, container: DIContainer):
        self._container = container
        self._sequence_service = None
        self._pictograph_service = None

    @property
    def sequence_service(self) -> ISequenceManager:
        if self._sequence_service is None:
            self._sequence_service = self._container.resolve(ISequenceManager)
        return self._sequence_service

    @property
    def pictograph_service(self) -> IPictographManagementService:
        if self._pictograph_service is None:
            self._pictograph_service = self._container.resolve(IPictographManagementService)
        return self._pictograph_service
```

### Caching Pattern

```python
# CORRECT: Service-level caching
class PictographDatasetService:
    def __init__(self):
        self._pictograph_cache: Dict[str, PictographData] = {}
        self._dataset_index: Dict[str, List[str]] = {}

    def get_pictograph_by_letter(self, letter: str) -> List[PictographData]:
        cache_key = f"letter_{letter}"

        if cache_key not in self._pictograph_cache:
            # Load from dataset
            pictographs = self._load_pictographs_from_dataset(letter)
            self._pictograph_cache[cache_key] = pictographs

        return self._pictograph_cache[cache_key]
```

## 🎨 UI COMPONENT PATTERNS

### Service Injection in UI

```python
# CORRECT: UI components receive services via constructor
class SequenceWorkbench(QWidget):
    def __init__(self,
                 sequence_service: ISequenceManager,
                 layout_service: ILayoutService,
                 parent=None):
        super().__init__(parent)
        self._sequence_service = sequence_service
        self._layout_service = layout_service

        self._setup_ui()

    def _setup_ui(self):
        # UI setup using injected services
        window_size = self._layout_service.get_main_window_size()
        self.resize(window_size.width, window_size.height)

    def create_sequence(self):
        # Delegate to service
        sequence = self._sequence_service.create_sequence("New Sequence", 16)
        self._update_ui_with_sequence(sequence)
```

### Event Handling Pattern

```python
# CORRECT: Clean event handling
class BeatFrameWidget(QWidget):
    def __init__(self, beat_data: BeatData, sequence_service: ISequenceManager):
        super().__init__()
        self._beat_data = beat_data
        self._sequence_service = sequence_service

    def mousePressEvent(self, event):
        """Handle beat frame selection"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._handle_beat_selection()

    def _handle_beat_selection(self):
        # Delegate business logic to service
        self._sequence_service.select_beat(self._beat_data.beat_number)
        self.update()  # Update UI
```

## 🚨 ANTI-PATTERNS TO AVOID

### DON'T:

```python
# ❌ Direct service instantiation
service = SequenceManager()  # Missing dependencies

# ❌ Mutable domain objects
beat.letter = "B"  # Violates immutability

# ❌ Business logic in UI
class BadWidget(QWidget):
    def create_sequence(self):
        sequence = SequenceData(...)  # Business logic in UI

# ❌ Incorrect import patterns
from src.desktop.modern.src.domain.models import BeatData  # Wrong path

# ❌ Missing error handling
def risky_operation():
    return service.create_sequence("", -1)  # No validation

# ❌ Ignoring existing patterns
mock_service = Mock()  # When real test services exist
```

### DO:

```python
# ✅ Use dependency injection
container = ApplicationFactory.create_test_app()
service = container.resolve(ISequenceManager)

# ✅ Immutable operations
beat = beat.update(letter="B")

# ✅ Delegate to services
class GoodWidget(QWidget):
    def create_sequence(self):
        self._sequence_service.create_sequence("New", 16)

# ✅ Correct import patterns
from domain.models.core_models import BeatData

# ✅ Proper error handling
try:
    sequence = service.create_sequence(name, length)
except ValidationError as e:
    logger.error(f"Validation failed: {e}")

# ✅ Use existing infrastructure
helper = TKAAITestHelper()  # Instead of creating mocks
```

## 🎯 KEY TAKEAWAYS FOR AI AGENTS

1. **Follow Import Conventions**: Context-aware imports based on code location
2. **Use Dependency Injection**: Never instantiate services directly
3. **Respect Immutability**: All domain operations return new instances
4. **Handle Errors Properly**: Use structured exceptions and logging
5. **Leverage Event System**: Publish/subscribe for loose coupling
6. **Use Existing Patterns**: Don't recreate what already exists
7. **Organize Code Clearly**: Follow layer boundaries and naming conventions
8. **Test with Real Objects**: Use sophisticated fixtures, not mocks

**These patterns ensure consistency, maintainability, and architectural integrity across the TKA codebase.**
