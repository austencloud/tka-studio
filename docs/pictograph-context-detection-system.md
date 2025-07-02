# Pictograph Context Detection System

## Overview

The TKA pictograph context detection system has been redesigned to replace brittle string matching with a robust, service-based architecture that follows TKA's clean architecture principles.

## Problem Solved

### Previous Issues
- **Brittle String Matching**: The old system used string matching against parent class names (`"grapheditor" in class_name.lower()`)
- **Silent Failures**: Context detection broke silently during refactoring when class names changed
- **Inconsistent Behavior**: Arrow items were selectable in all contexts instead of only in the graph editor
- **Maintenance Burden**: Adding new contexts required updating string matching patterns
- **Architectural Violation**: Used implementation details (class names) instead of explicit contracts

### Current Solution
- **Explicit Context Declaration**: Components explicitly declare their rendering context
- **Service-Based Architecture**: Uses dependency injection and service interfaces
- **Type Safety**: Uses enums and formal contracts instead of string matching
- **Refactor-Safe**: Survives class name changes and component restructuring
- **Clear Error Handling**: Provides meaningful feedback when context cannot be determined

## Architecture

### Core Components

#### 1. RenderingContext Enum
```python
class RenderingContext(Enum):
    GRAPH_EDITOR = "graph_editor"
    BEAT_FRAME = "beat_frame"
    OPTION_PICKER = "option_picker"
    PREVIEW = "preview"
    SEQUENCE_VIEWER = "sequence_viewer"
    UNKNOWN = "unknown"
```

#### 2. IPictographContextService Interface
```python
class IPictographContextService(ABC):
    @abstractmethod
    def register_context_provider(self, component_id: str, context: RenderingContext) -> None:
        """Register a component with its explicit context."""
        pass
    
    @abstractmethod
    def get_context_for_component(self, component_id: str) -> RenderingContext:
        """Get the rendering context for a specific component."""
        pass
    
    @abstractmethod
    def determine_context_from_scene(self, scene: Any) -> RenderingContext:
        """Determine context from a pictograph scene."""
        pass
```

#### 3. PictographContextService Implementation
- Manages component context registration
- Provides robust context detection with fallbacks
- Integrates with TKA's dependency injection container

#### 4. Updated ArrowItem
- Uses service-based context detection
- Configures behavior based on RenderingContext enum
- Maintains backward compatibility

## Usage Patterns

### 1. Explicit Context Declaration (Recommended)
```python
from application.services.ui.pictograph_context_service import create_context_aware_scene
from application.services.ui.context_aware_scaling_service import RenderingContext

# Create scene with explicit context
scene = create_context_aware_scene(
    RenderingContext.GRAPH_EDITOR,
    PictographScene,
    *args, **kwargs
)
```

### 2. Context Provider Interface
```python
class GraphEditorWidget(QWidget, IPictographContextProvider):
    def get_rendering_context(self) -> RenderingContext:
        return RenderingContext.GRAPH_EDITOR
```

### 3. Service Registration
```python
# Register component context
container = ApplicationFactory.create_production_app()
context_service = container.resolve(IPictographContextService)
context_service.register_context_provider("my_component", RenderingContext.BEAT_FRAME)
```

## Arrow Behavior by Context

| Context | Selectable | Hover Events | Cursor | Use Case |
|---------|------------|--------------|--------|----------|
| GRAPH_EDITOR | ✅ Yes | ✅ Yes | Pointing Hand | Interactive arrow selection |
| BEAT_FRAME | ❌ No | ❌ No | Arrow | Display only |
| OPTION_PICKER | ❌ No | ❌ No | Arrow | Display only |
| PREVIEW | ❌ No | ❌ No | Arrow | Display only |
| SEQUENCE_VIEWER | ❌ No | ❌ No | Arrow | Display only |
| UNKNOWN | ❌ No | ❌ No | Arrow | Safe default |

## Migration Guide

### For New Components
1. Implement `IPictographContextProvider` interface
2. Use `create_context_aware_scene()` factory function
3. Register context with service during initialization

### For Existing Components
1. The system provides backward compatibility
2. Legacy string-based detection still works as fallback
3. Gradually migrate to explicit context declaration
4. Remove dependency on class name patterns

### Example Migration
```python
# OLD: Relies on class name detection
class GraphEditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.scene = PictographScene()  # Context detected via class name

# NEW: Explicit context declaration
class GraphEditorWidget(QWidget, IPictographContextProvider):
    def __init__(self):
        super().__init__()
        self.scene = create_context_aware_scene(
            RenderingContext.GRAPH_EDITOR,
            PictographScene
        )
    
    def get_rendering_context(self) -> RenderingContext:
        return RenderingContext.GRAPH_EDITOR
```

## Testing

### Validation Script
Run `python validate_context_system.py` to verify the system is working correctly.

### Test Coverage
- Service registration and resolution
- Context detection functionality
- Arrow behavior integration
- TKA infrastructure integration
- Backward compatibility
- Error handling and robustness

### Integration with TKAAITestHelper
```python
from core.testing.ai_agent_helpers import TKAAITestHelper

helper = TKAAITestHelper(use_test_mode=True)
context_service = helper.container.resolve(IPictographContextService)

# Test context registration
context_service.register_context_provider("test", RenderingContext.GRAPH_EDITOR)
context = context_service.get_context_for_component("test")
assert context == RenderingContext.GRAPH_EDITOR
```

## Benefits

### Architectural Benefits
- **Clean Architecture Compliance**: Follows TKA's dependency injection patterns
- **Single Responsibility**: Context detection is handled by dedicated service
- **Type Safety**: Uses enums instead of string constants
- **Testability**: Easy to mock and test in isolation

### Maintenance Benefits
- **Refactor-Safe**: Survives class name changes and restructuring
- **Explicit Contracts**: Clear interfaces instead of implicit assumptions
- **Error Visibility**: Clear logging and error messages
- **Future-Proof**: Easy to add new contexts without breaking existing code

### Performance Benefits
- **Fast Lookups**: O(1) context retrieval from registry
- **Minimal Overhead**: Service resolution cached per component
- **Lazy Loading**: Context service only loaded when needed

## Backward Compatibility

The system maintains full backward compatibility:
- Legacy `_determine_component_type()` method still works
- String return values preserved for existing code
- Fallback detection for components not yet migrated
- No breaking changes to existing APIs

## Future Enhancements

1. **Context Validation**: Validate that components use appropriate contexts
2. **Context Metrics**: Track context usage for optimization
3. **Dynamic Context**: Support for context changes at runtime
4. **Context Inheritance**: Automatic context propagation to child components
5. **Context-Aware Styling**: Automatic styling based on context

## Conclusion

The new pictograph context detection system provides a robust, maintainable solution that eliminates the brittleness of string matching while maintaining full backward compatibility. It follows TKA's architectural principles and provides a foundation for future enhancements to the pictograph rendering system.
