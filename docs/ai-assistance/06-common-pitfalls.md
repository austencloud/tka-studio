# 06 - TKA Common Pitfalls

## 🚨 CRITICAL MISTAKES TO AVOID

TKA's sophisticated architecture can be easily broken by AI agents who don't understand its patterns. This guide prevents common mistakes that violate architectural principles.

## 🏗️ ARCHITECTURAL VIOLATIONS

### CRITICAL ERROR: Recreating Existing Systems
```python
# ❌ WRONG: Creating competing command pattern
class AICommandExecutor:  # DON'T DO THIS
    def execute_sequence_command(self, command):
        # TKA already has SequenceManagementService with commands!
        pass

# ✅ CORRECT: Use existing sophisticated system
container = ApplicationFactory.create_test_app()
service = container.resolve(ISequenceManagementService)
# Service already has add_beat_with_undo, undo_last_operation, etc.
updated_sequence = service.add_beat_with_undo(beat_data, position)
```

### CRITICAL ERROR: Ignoring Dependency Injection
```python
# ❌ WRONG: Direct service instantiation
from application.services.core.sequence_management_service import SequenceManagementService

service = SequenceManagementService()  # Missing dependencies!
sequence = service.create_sequence("Test", 8)  # Will fail

# ✅ CORRECT: Use DI container
container = ApplicationFactory.create_test_app()
service = container.resolve(ISequenceManagementService)  # All dependencies injected
sequence = service.create_sequence("Test", 8)  # Works perfectly
```

### CRITICAL ERROR: Violating Immutability
```python
# ❌ WRONG: Trying to mutate frozen dataclasses
beat = BeatData(beat_number=1, letter="A")
beat.letter = "B"  # EXCEPTION: Cannot mutate frozen dataclass
beat.duration = 2.0  # EXCEPTION: Cannot mutate frozen dataclass

# ❌ WRONG: Modifying collections directly
sequence = SequenceData(name="Test", beats=[beat1, beat2])
sequence.beats.append(beat3)  # VIOLATES IMMUTABILITY
sequence.beats[0] = new_beat  # VIOLATES IMMUTABILITY

# ✅ CORRECT: Immutable updates
beat = beat.update(letter="B")  # Returns new instance
sequence = sequence.add_beat(beat3)  # Returns new instance
```

### CRITICAL ERROR: Business Logic in UI
```python
# ❌ WRONG: Business logic in UI components
class BadSequenceWidget(QWidget):
    def create_sequence_button_clicked(self):
        # DON'T PUT BUSINESS LOGIC HERE
        beats = []
        for i in range(16):
            beat = BeatData(beat_number=i+1)  # Business logic in UI!
            beats.append(beat)
        sequence = SequenceData(name="New", beats=beats)  # Business logic in UI!

# ✅ CORRECT: Delegate to services
class GoodSequenceWidget(QWidget):
    def __init__(self, sequence_service: ISequenceManagementService):
        super().__init__()
        self._sequence_service = sequence_service
    
    def create_sequence_button_clicked(self):
        # Delegate to service
        sequence = self._sequence_service.create_sequence("New", 16)
        self._update_ui_with_sequence(sequence)
```

## 🧪 TESTING VIOLATIONS

### CRITICAL ERROR: Creating Unnecessary Mocks
```python
# ❌ WRONG: Mocking complex domain objects
from unittest.mock import Mock

mock_sequence = Mock(spec=SequenceData)
mock_sequence.name = "Test"
mock_sequence.length = 8
# This loses all domain validation and behavior!

# ❌ WRONG: Mocking sophisticated services
mock_service = Mock(spec=ISequenceManagementService)
mock_service.create_sequence.return_value = mock_sequence
# TKA has real test implementations!

# ✅ CORRECT: Use real test objects and services
container = ApplicationFactory.create_test_app()
service = container.resolve(ISequenceManagementService)  # Real service with mock backend
sequence = service.create_sequence("Test", 8)  # Real SequenceData object
assert isinstance(sequence, SequenceData)  # Real validation
```

### CRITICAL ERROR: Ignoring Test Infrastructure
```python
# ❌ WRONG: Manual test setup
def test_sequence_creation():
    # Manual, error-prone setup
    container = DIContainer()
    container.register_singleton(ISequenceDataService, MockSequenceDataService)
    container.register_singleton(IValidationService, MockValidationService)
    # ... 20 lines of manual registration

# ✅ CORRECT: Use existing test infrastructure
def test_sequence_creation():
    helper = TKAAITestHelper(use_test_mode=True)
    result = helper.create_sequence("Test", 8)
    assert result.success
    # All services pre-configured!
```

### CRITICAL ERROR: Testing Implementation Details
```python
# ❌ WRONG: Testing internal implementation
def test_sequence_service_internals():
    service = container.resolve(ISequenceManagementService)
    sequence = service.create_sequence("Test", 8)
    
    # DON'T TEST PRIVATE STATE
    assert service._current_sequence == sequence  # Implementation detail!
    assert len(service._cleanup_handlers) == 1   # Implementation detail!

# ✅ CORRECT: Testing behavioral contracts
def test_sequence_service_contract():
    service = container.resolve(ISequenceManagementService)
    sequence = service.create_sequence("Test", 8)
    
    # TEST PUBLIC CONTRACTS
    assert sequence.name == "Test"
    assert sequence.length == 8
    assert isinstance(sequence, SequenceData)
```

## 📊 DOMAIN MODEL VIOLATIONS

### CRITICAL ERROR: Incomplete Domain Objects
```python
# ❌ WRONG: Creating incomplete domain objects
beat = BeatData()  # Missing required data
sequence = SequenceData()  # Missing required data
# These objects won't pass validation!

# ❌ WRONG: Invalid enum usage
motion = MotionData(
    motion_type="invalid_type",  # Not a valid MotionType enum!
    prop_rot_dir="spin",        # Not a valid RotationDirection enum!
    start_loc="top",            # Not a valid Location enum!
    end_loc="bottom"            # Not a valid Location enum!
)

# ✅ CORRECT: Complete, valid domain objects
from domain.models.core_models import MotionType, RotationDirection, Location

motion = MotionData(
    motion_type=MotionType.PRO,
    prop_rot_dir=RotationDirection.CLOCKWISE,
    start_loc=Location.NORTH,
    end_loc=Location.EAST,
    turns=0.5
)

beat = BeatData(
    beat_number=1,
    letter="A",
    blue_motion=motion,
    red_motion=motion,
    duration=1.0
)
```

### CRITICAL ERROR: Ignoring Validation
```python
# ❌ WRONG: Skipping validation
def create_sequence_without_validation(name, length):
    # Just create without checking business rules
    sequence = SequenceData(name=name, beats=[])
    return sequence  # Might violate business rules!

# ✅ CORRECT: Use built-in validation
def create_sequence_safely(name, length):
    container = ApplicationFactory.create_test_app()
    service = container.resolve(ISequenceManagementService)
    
    try:
        sequence = service.create_sequence(name, length)
        # Service validates automatically
        return sequence
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        raise
```

## 🔧 SERVICE LAYER VIOLATIONS

### CRITICAL ERROR: Layer Boundary Violations
```python
# ❌ WRONG: Domain calling Infrastructure
from domain.models.core_models import SequenceData
from infrastructure.storage.file_repository import FileRepository

class BadSequenceData(SequenceData):  # DON'T EXTEND DOMAIN MODELS
    def save_to_file(self):
        repo = FileRepository()  # DOMAIN CALLING INFRASTRUCTURE!
        repo.save(self)

# ✅ CORRECT: Service orchestrates layers
class SequenceService:
    def __init__(self, repository: ISequenceRepository):
        self._repository = repository
    
    def save_sequence(self, sequence: SequenceData) -> bool:
        # SERVICE orchestrates domain and infrastructure
        if sequence.is_valid:
            return self._repository.save(sequence)
        return False
```

### CRITICAL ERROR: Bypassing Service Interfaces
```python
# ❌ WRONG: Using concrete implementations directly
from application.services.core.sequence_management_service import SequenceManagementService

service = SequenceManagementService()  # Bypasses DI and interfaces!

# ❌ WRONG: Importing implementation in tests
from application.services.core.pictograph_management_service import PictographManagementService

def test_pictograph_creation():
    service = PictographManagementService()  # Wrong!

# ✅ CORRECT: Use interfaces through DI
from core.interfaces.core_services import ISequenceManagementService

container = ApplicationFactory.create_test_app()
service = container.resolve(ISequenceManagementService)  # Interface-based!
```

## 📥 IMPORT VIOLATIONS

### CRITICAL ERROR: Wrong Import Patterns
```python
# ❌ WRONG: Incorrect path structure
from src.desktop.modern.src.domain.models.core_models import BeatData  # Too long!
from desktop.modern.src.domain.models.core_models import BeatData      # Wrong structure!
from tka.desktop.domain.models.core_models import BeatData             # Wrong namespace!

# ✅ CORRECT: Context-aware imports
# For code within src/desktop/modern/src/:
from domain.models.core_models import BeatData

# For external code (tests, web):
from desktop.domain.models.core_models import BeatData
```

### CRITICAL ERROR: Circular Import Dependencies
```python
# ❌ WRONG: Circular imports
# In sequence_service.py:
from pictograph_service import PictographService  # Creates circular dependency!

# In pictograph_service.py:
from sequence_service import SequenceService      # Creates circular dependency!

# ✅ CORRECT: Use interfaces to break cycles
# In sequence_service.py:
from core.interfaces.core_services import IPictographManagementService

class SequenceService:
    def __init__(self, pictograph_service: IPictographManagementService):
        self._pictograph_service = pictograph_service
```

## 🚀 PERFORMANCE VIOLATIONS

### CRITICAL ERROR: Inefficient Service Resolution
```python
# ❌ WRONG: Resolving services repeatedly
class BadController:
    def handle_request(self):
        service = container.resolve(ISequenceManagementService)  # Expensive!
        service.create_sequence("Test", 8)
    
    def handle_another_request(self):
        service = container.resolve(ISequenceManagementService)  # Expensive again!
        service.create_sequence("Another", 16)

# ✅ CORRECT: Cache resolved services
class GoodController:
    def __init__(self, container: DIContainer):
        self._sequence_service = container.resolve(ISequenceManagementService)
    
    def handle_request(self):
        self._sequence_service.create_sequence("Test", 8)  # Fast!
    
    def handle_another_request(self):
        self._sequence_service.create_sequence("Another", 16)  # Fast!
```

### CRITICAL ERROR: Creating Expensive Objects in Tests
```python
# ❌ WRONG: Complex setup in every test
def test_sequence_operation_1():
    # Expensive setup repeated
    container = ApplicationFactory.create_production_app()  # Slow!
    service = container.resolve(ISequenceManagementService)

def test_sequence_operation_2():
    # Expensive setup repeated again
    container = ApplicationFactory.create_production_app()  # Slow!
    service = container.resolve(ISequenceManagementService)

# ✅ CORRECT: Use test mode and fixtures
@pytest.fixture
def sequence_service():
    container = ApplicationFactory.create_test_app()  # Fast test services!
    return container.resolve(ISequenceManagementService)

def test_sequence_operation_1(sequence_service):
    # Uses cached, fast service
    
def test_sequence_operation_2(sequence_service):
    # Uses cached, fast service
```

## 🎯 EVENT SYSTEM VIOLATIONS

### CRITICAL ERROR: Synchronous Event Handling
```python
# ❌ WRONG: Blocking event handlers
def slow_event_handler(event: SequenceCreatedEvent):
    time.sleep(5)  # BLOCKS THE ENTIRE SYSTEM!
    process_sequence(event.sequence_id)

# ✅ CORRECT: Asynchronous event handling
async def fast_event_handler(event: SequenceCreatedEvent):
    await asyncio.create_task(process_sequence_async(event.sequence_id))
```

### CRITICAL ERROR: Event Handler Side Effects
```python
# ❌ WRONG: Modifying event data
def bad_event_handler(event: SequenceCreatedEvent):
    event.sequence_name = "Modified"  # DON'T MODIFY EVENTS!
    event.metadata["processed"] = True  # DON'T MODIFY EVENTS!

# ✅ CORRECT: Read-only event handling
def good_event_handler(event: SequenceCreatedEvent):
    # Only read event data
    logger.info(f"Sequence created: {event.sequence_name}")
    update_statistics(event.sequence_id)
```

## 📝 DOCUMENTATION VIOLATIONS

### CRITICAL ERROR: Missing Test Lifecycle Metadata
```python
# ❌ WRONG: Unlabeled test without lifecycle
def test_sequence_creation():
    """Some sequence test"""  # WHAT LIFECYCLE? WHEN TO DELETE?
    pass

# ✅ CORRECT: Proper lifecycle documentation
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce sequence immutability contract
PERMANENT: Immutability is fundamental to TKA architecture
AUTHOR: @ai-agent
"""

@pytest.mark.specification
@pytest.mark.critical
def test_sequence_immutability_contract():
    """PERMANENT: Sequence operations must return new instances"""
    pass
```

## 🔒 SECURITY AND SAFETY VIOLATIONS

### CRITICAL ERROR: Unsafe Type Casting
```python
# ❌ WRONG: Unsafe casting without validation
def unsafe_conversion(data: Dict) -> BeatData:
    return BeatData(**data)  # Could crash with invalid data!

# ✅ CORRECT: Safe conversion with validation
def safe_conversion(data: Dict) -> BeatData:
    try:
        beat = BeatData.from_dict(data)  # Uses built-in validation
        if not beat.is_valid():
            raise ValidationError("Invalid beat data")
        return beat
    except Exception as e:
        raise ValidationError(f"Failed to create BeatData: {e}") from e
```

## 🎯 QUICK REFERENCE: MAJOR PITFALLS

### ❌ ARCHITECTURAL VIOLATIONS:
1. Recreating existing command patterns
2. Bypassing dependency injection
3. Violating immutability contracts
4. Putting business logic in UI
5. Violating layer boundaries

### ❌ TESTING VIOLATIONS:
1. Creating unnecessary mocks
2. Ignoring test infrastructure
3. Testing implementation details
4. Missing test lifecycle metadata
5. Using production services in tests

### ❌ DOMAIN VIOLATIONS:
1. Creating incomplete domain objects
2. Using invalid enum values
3. Ignoring validation rules
4. Mutating frozen dataclasses
5. Bypassing business rules

### ❌ SERVICE VIOLATIONS:
1. Direct service instantiation
2. Circular import dependencies
3. Inefficient service resolution
4. Using concrete implementations
5. Layer boundary violations

### ❌ PERFORMANCE VIOLATIONS:
1. Repeated expensive operations
2. Synchronous event handling
3. Memory leaks in tests
4. Using production mode for testing
5. Creating objects instead of using fixtures

## 🎯 PREVENTION CHECKLIST

Before implementing any changes, ask:

1. **Am I recreating existing functionality?**
   - Check for existing services and patterns first

2. **Am I using dependency injection correctly?**
   - Services should be resolved from container

3. **Am I respecting immutability?**
   - Use `.update()` methods, never direct mutation

4. **Am I following layer boundaries?**
   - Domain shouldn't call Infrastructure

5. **Am I using the right test infrastructure?**
   - Use `TKAAITestHelper` and existing fixtures

6. **Am I testing contracts, not implementation?**
   - Test public behavior, not private state

7. **Am I using proper import patterns?**
   - Context-aware imports based on code location

8. **Am I handling errors appropriately?**
   - Use structured exceptions and validation

**When in doubt, check existing patterns in the codebase and follow them consistently.**
