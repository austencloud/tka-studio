# TKA AI Agent Quick Start Guide

## 🚀 ESSENTIAL READING - START HERE FIRST

This is the **mandatory primer** for all AI agents working with TKA. Read this before touching any code.

## 🎯 TKA IN 60 SECONDS

TKA is **NOT** a simple application. It's a sophisticated system with:

- **Clean Architecture** with strict layer boundaries
- **Immutable Domain Models** (`BeatData`, `SequenceData`, `MotionData`)
- **Advanced Dependency Injection** with service interfaces
- **Existing Command Pattern** with undo/redo capabilities
- **Comprehensive Testing Infrastructure** with lifecycle management
- **Event-Driven Architecture** with pub/sub patterns

## 🚨 CRITICAL UNDERSTANDING

### YOU MUST NOT:
❌ Recreate existing command patterns  
❌ Create competing service implementations  
❌ Mock complex domain objects  
❌ Violate immutability contracts  
❌ Put business logic in UI components  
❌ Bypass dependency injection  

### YOU MUST:
✅ Use `ApplicationFactory` for different app modes  
✅ Leverage existing sophisticated services  
✅ Work with immutable domain models correctly  
✅ Use `TKAAITestHelper` for testing  
✅ Follow existing architectural patterns  
✅ Respect clean architecture boundaries  

## ⚡ INSTANT START PATTERN

```python
# 1. Understand what's available
from core.application.application_factory import ApplicationFactory
container = ApplicationFactory.create_test_app()
print(f"Available services: {list(container.get_registrations().keys())}")

# 2. Use existing sophisticated services
sequence_service = container.resolve(ISequenceManagementService)
pictograph_service = container.resolve(IPictographManagementService)

# 3. Work with real domain models
from domain.models.core_models import BeatData, SequenceData, MotionData
beat = BeatData(beat_number=1, letter="A", duration=1.0)

# 4. Use AI testing utilities
from core.testing.ai_agent_helpers import TKAAITestHelper
helper = TKAAITestHelper()
result = helper.run_comprehensive_test_suite()
assert result.success
```

## 🧠 ARCHITECTURAL MENTAL MODEL

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION                          │
│  (PyQt6 widgets with dependency injection)              │
└─────────────────────┬───────────────────────────────────┘
                      │ Depends on
┌─────────────────────▼───────────────────────────────────┐
│                   APPLICATION                            │
│  (SequenceManagementService, PictographManagementService)│
└─────────────────────┬───────────────────────────────────┘
                      │ Uses
┌─────────────────────▼───────────────────────────────────┐
│                     DOMAIN                               │
│  (BeatData, SequenceData, MotionData - IMMUTABLE)       │
└─────────────────────┬───────────────────────────────────┘
                      │ Persisted by
┌─────────────────────▼───────────────────────────────────┐
│                 INFRASTRUCTURE                           │
│  (File system, CSV datasets, test doubles)              │
└─────────────────────────────────────────────────────────┘
```

## 🎯 ESSENTIAL SERVICES YOU MUST KNOW

### `ISequenceManagementService` - Already Has Command Pattern!
```python
# Don't recreate this - it exists!
service = container.resolve(ISequenceManagementService)

# Create sequences
sequence = service.create_sequence("Test", 8)

# Command pattern with undo/redo (ALREADY IMPLEMENTED)
updated_sequence = service.add_beat_with_undo(beat_data, position)
can_undo = service.can_undo()
service.undo_last_operation()
```

### `IPictographManagementService` - CSV Dataset Integration!
```python
# Sophisticated dataset management exists
service = container.resolve(IPictographManagementService)

# Get pictographs from CSV data
pictographs = service.get_pictographs_by_letter("A")
specific = service.get_specific_pictograph("A", index=0)

# Create from beat data
pictograph = service.create_from_beat(beat_data)
```

## 🧪 ESSENTIAL TESTING PATTERNS

### Primary Testing Interface
```python
# USE THIS - don't create manual test setup
from core.testing.ai_agent_helpers import TKAAITestHelper

helper = TKAAITestHelper(use_test_mode=True)

# Test real workflows
seq_result = helper.create_sequence("Test", 8)
beat_result = helper.create_beat_with_motions(1, "A")
cmd_result = helper.test_existing_command_pattern()

# Quick validation
result = helper.run_comprehensive_test_suite()
assert result.metadata['success_rate'] > 0.8
```

### One-Line Testing Functions
```python
# For quick validation
from core.testing.ai_agent_helpers import (
    ai_test_tka_comprehensive,
    ai_test_sequence_workflow,
    ai_test_pictograph_workflow
)

# Comprehensive test
result = ai_test_tka_comprehensive()
assert result['overall_success']
```

## 📊 ESSENTIAL DOMAIN MODEL PATTERNS

### Immutable Operations (CRITICAL)
```python
# CORRECT: Returns new instances
beat = BeatData(beat_number=1, letter="A")
updated_beat = beat.update(letter="B")  # New instance

sequence = SequenceData(name="Test", beats=[])
new_sequence = sequence.add_beat(beat)  # New instance

# INCORRECT: Will fail
beat.letter = "B"  # Exception - frozen dataclass
```

### Real Domain Objects
```python
# CORRECT: Complete, valid objects
from domain.models.core_models import MotionType, Location, RotationDirection

motion = MotionData(
    motion_type=MotionType.PRO,
    prop_rot_dir=RotationDirection.CLOCKWISE,
    start_loc=Location.NORTH,
    end_loc=Location.EAST
)

beat = BeatData(
    beat_number=1,
    letter="A",
    blue_motion=motion,
    red_motion=motion
)
```

## 🎯 TESTING LIFECYCLE ESSENTIALS

### Test Categories (CRITICAL)
```python
# SPECIFICATION: Permanent contracts (NEVER DELETE)
@pytest.mark.specification
@pytest.mark.critical
def test_sequence_immutability_contract():
    """PERMANENT: Sequence operations must return new instances"""
    
# REGRESSION: Bug prevention (keep until feature removed)
@pytest.mark.regression
def test_bug_fix_123():
    """REGRESSION: Prevent specific bug from reoccurring"""
    
# SCAFFOLDING: Temporary debugging (DELETE after purpose)
@pytest.mark.scaffolding
def test_debug_performance():
    """
    DELETE_AFTER: 2024-12-31
    PURPOSE: Debug performance issue
    """
```

## 🚀 PERFORMANCE ESSENTIALS

### Fast Testing Pattern
```python
# Fast test services (microsecond execution)
container = ApplicationFactory.create_test_app()

# Slow production services (avoid in tests)
container = ApplicationFactory.create_production_app()
```

### Service Caching
```python
# Cache services, don't resolve repeatedly
class Controller:
    def __init__(self, container: DIContainer):
        self._sequence_service = container.resolve(ISequenceManagementService)
    
    def handle_request(self):
        self._sequence_service.create_sequence("Fast", 8)  # Cached!
```

## 📋 PRE-IMPLEMENTATION CHECKLIST

Before writing ANY code, verify:

### ✅ ARCHITECTURE CHECK:
- [ ] Am I using `ApplicationFactory.create_test_app()`?
- [ ] Am I resolving services via DI container?
- [ ] Am I working with immutable domain models?
- [ ] Am I leveraging existing command pattern?

### ✅ TESTING CHECK:
- [ ] Am I using `TKAAITestHelper`?
- [ ] Am I using existing fixtures?
- [ ] Am I testing contracts, not implementation?
- [ ] Am I using appropriate test lifecycle?

### ✅ DOMAIN CHECK:
- [ ] Am I creating complete domain objects?
- [ ] Am I using proper enum values?
- [ ] Am I respecting immutability?
- [ ] Am I using validation?

### ✅ AVOID CHECK:
- [ ] Am I NOT recreating existing functionality?
- [ ] Am I NOT mocking complex domain objects?
- [ ] Am I NOT violating layer boundaries?
- [ ] Am I NOT putting business logic in UI?

## 🎯 WHEN IN DOUBT

1. **Check existing patterns** in the codebase first
2. **Use `TKAAITestHelper`** for testing
3. **Follow immutable domain model** patterns
4. **Leverage sophisticated services** via DI
5. **Respect clean architecture** boundaries

## 📚 DEEP DIVE DOCUMENTATION

After reading this guide, explore:

1. **[Architecture Overview](./01-architecture-overview.md)** - Clean architecture layers
2. **[Domain Models Guide](./02-domain-models.md)** - Immutable dataclass patterns  
3. **[Service Layer Guide](./03-service-layer.md)** - Existing sophisticated services
4. **[Testing Protocols](./04-testing-protocols.md)** - Testing infrastructure
5. **[Development Patterns](./05-development-patterns.md)** - Coding conventions
6. **[Common Pitfalls](./06-common-pitfalls.md)** - Mistakes to avoid

---

**Remember**: TKA is sophisticated. Respect the architecture, use existing patterns, and work WITH the system, not against it.
