# 01 - TKA Architecture Overview

## 🏗️ SOPHISTICATED ARCHITECTURE UNDERSTANDING

TKA is NOT a simple application. It follows enterprise-grade Clean Architecture with sophisticated patterns that AI agents must respect.

## 📐 CLEAN ARCHITECTURE LAYERS

### Core Layer (`src/desktop/modern/src/core/`)
**Purpose**: Framework-agnostic business rules and contracts
- **Dependency Injection**: `di_container.py` - Sophisticated DI with lifecycle management
- **Service Interfaces**: `interfaces/` - Abstract contracts for all services
- **Types**: `types/` - Framework-agnostic geometry and data types
- **Events**: Event-driven architecture with pub/sub patterns
- **Exceptions**: Structured error handling

### Domain Layer (`src/desktop/modern/src/domain/`)
**Purpose**: Pure business logic with immutable data models
- **Models**: `models/` - Complex immutable dataclasses
  - `BeatData` - Motion data with validation
  - `SequenceData` - Immutable sequence with functional operations
  - `MotionData` - Complex motion definitions
  - `PictographData` - Visual representation data
- **Services**: Domain-specific business rules
- **Repositories**: Data access contracts

### Application Layer (`src/desktop/modern/src/application/`)
**Purpose**: Use case orchestration and service implementations
- **Services**: Sophisticated service implementations
  - `SequenceManagementService` - Command pattern with undo/redo
  - `PictographManagementService` - Dataset management and CSV integration
  - Layout, positioning, validation services
- **Orchestrators**: Complex workflow coordination

### Infrastructure Layer (`src/desktop/modern/src/infrastructure/`)
**Purpose**: External concerns and framework integration
- **Storage**: File system and data persistence
- **API**: External service integration
- **Configuration**: Environment-specific settings
- **Test Doubles**: Mock implementations for testing

### Presentation Layer (`src/desktop/modern/src/presentation/`)
**Purpose**: UI components with clean separation
- **Components**: PyQt6 widgets with dependency injection
- **Factories**: UI construction and service wiring

## 🔧 DEPENDENCY INJECTION ARCHITECTURE

### Container System
The DI container is sophisticated with:
- **Service Resolution**: Automatic constructor injection
- **Lifecycle Management**: Singleton and transient scopes
- **Validation**: Interface compliance checking
- **Performance Monitoring**: Resolution time tracking

### Application Factory Pattern
```python
from core.application.application_factory import ApplicationFactory

# Different app configurations for different contexts
test_app = ApplicationFactory.create_test_app()        # Mock services
headless_app = ApplicationFactory.create_headless_app() # Real logic, no UI
production_app = ApplicationFactory.create_production_app() # Full application
```

### Service Registration
```python
# Services are registered with interfaces
container.register_singleton(ISequenceManagementService, SequenceManagementService)
container.register_transient(IPictographFactory, PictographFactory)

# Resolution is automatic with dependency injection
service = container.resolve(ISequenceManagementService)
```

## 📊 IMMUTABLE DATA MODEL PHILOSOPHY

### Core Principle
ALL data models are immutable frozen dataclasses that return new instances on modification.

### Example Pattern
```python
# CORRECT: Immutable operations
beat = BeatData(letter="A", duration=1.0)
updated_beat = beat.update(duration=2.0)  # Returns new instance

sequence = SequenceData(name="Test", beats=[beat])
new_sequence = sequence.add_beat(new_beat)  # Returns new instance

# INCORRECT: Direct mutation (will fail)
beat.duration = 2.0  # Error - frozen dataclass
```

### Why Immutability?
- **Thread Safety**: No race conditions
- **Predictable State**: No unexpected mutations
- **Undo/Redo**: Easy state restoration
- **Testing**: Reliable test assertions

## 🎯 COMMAND PATTERN INTEGRATION

### Existing Command System
TKA already has a sophisticated command pattern in `SequenceManagementService`:

```python
# AI agents should use existing commands, not create new ones
service = container.resolve(ISequenceManagementService)

# Commands with undo/redo
updated_sequence = service.add_beat_with_undo(beat_data, position)
can_undo = service.can_undo()
service.undo_last_operation()
```

### Event-Driven Architecture
Commands publish events:
```python
# Events are automatically published
service.create_sequence_with_events(name, length)
# Publishes: SequenceCreatedEvent

service.add_beat_with_undo(beat, position)  
# Publishes: BeatAddedEvent
```

## 🧪 TESTING ARCHITECTURE

### Test Lifecycle Categories
- **Specification**: Permanent behavioral contracts (NEVER DELETE)
- **Regression**: Bug prevention tests (keep until feature removed)
- **Scaffolding**: Temporary development aids (DELETE after purpose achieved)

### Test Fixtures
```python
# Sophisticated fixtures available
@pytest.fixture
def configured_di_container():
    """DI container with services configured"""
    
@pytest.fixture
def sample_sequence_data():
    """Real SequenceData with BeatData"""
    
@pytest.fixture
def sample_pictograph_data():
    """PictographData with ArrowData and MotionData"""
```

## 🔄 DATA FLOW ARCHITECTURE

### Request Flow
1. **UI Component** (Presentation) receives user input
2. **Service Interface** (Core) defines contract
3. **Service Implementation** (Application) executes business logic
4. **Domain Models** (Domain) enforce business rules
5. **Repository** (Infrastructure) persists data
6. **Events** (Core) notify interested parties

### Example Flow
```
User clicks "Create Sequence" 
→ UI Component calls service
→ SequenceManagementService.create_sequence()
→ Creates SequenceData domain model
→ Validates with domain rules
→ Persists via repository
→ Publishes SequenceCreatedEvent
→ UI updates via event handler
```

## 📋 INTEGRATION PATTERNS

### Service Communication
```python
# Services communicate through interfaces, not implementations
class MyService:
    def __init__(self, 
                 sequence_service: ISequenceManagementService,
                 pictograph_service: IPictographManagementService):
        self._sequence_service = sequence_service
        self._pictograph_service = pictograph_service
```

### Cross-Platform Sharing
```python
# Shared types between desktop and web
from tka_types import MotionType, SharedSequenceType
from tka_constants import ENDPOINTS, API_BASE_URL
```

## 🚨 ARCHITECTURE VIOLATIONS TO AVOID

### NEVER:
- Create services directly (use DI container)
- Mutate domain objects (use .update() methods)
- Put business logic in UI components
- Create competing service implementations
- Mock complex domain objects unnecessarily
- Violate layer boundaries (e.g., Domain calling Infrastructure)

### ALWAYS:
- Use dependency injection for service creation
- Work with immutable domain models
- Delegate business logic to services
- Respect existing sophisticated patterns
- Use appropriate test fixtures
- Follow clean architecture principles

## 📈 PERFORMANCE CONSIDERATIONS

### DI Container
- Services are lazily resolved
- Singletons are cached efficiently
- Resolution performance is monitored

### Domain Models
- Immutable operations are optimized
- Structural sharing where possible
- Validation is cached

### Testing
- Test services execute in microseconds
- Complex setup is handled by fixtures
- Parallel test execution supported

---

## 🎯 KEY TAKEAWAY FOR AI AGENTS

TKA is a sophisticated, enterprise-grade application with:
- Clean Architecture boundaries
- Immutable domain models
- Sophisticated dependency injection
- Existing command pattern with undo/redo
- Comprehensive testing infrastructure

**Work WITH this architecture, not against it.** Understand the existing patterns and extend them rather than recreating them.
