# GraphEditorHotkeyService Refactoring

## Problem

The original `GraphEditorHotkeyService` inherited from `QObject` and used PyQt signals, which broke TKA's service separation principles by tightly coupling the service to the Qt framework.

```python
# BEFORE: Violates service separation
class GraphEditorHotkeyService(QObject):  # ❌ Inherits from QObject
    arrow_moved = pyqtSignal(str, int, int)  # ❌ Uses PyQt signals

    def __init__(self, graph_service: "IGraphEditorService", parent=None):
        super().__init__(parent)  # ❌ Qt dependency
```

## Solution: Adapter Pattern

We implemented the **Adapter Pattern** to separate concerns:

1. **Pure Service Layer** (`GraphEditorHotkeyService`)
   - Framework-agnostic business logic
   - Uses callback protocol instead of signals
   - No Qt dependencies

2. **Qt Adapter Layer** (`GraphEditorHotkeyAdapter`)
   - Handles Qt-specific signal emissions
   - Bridges between service callbacks and PyQt signals
   - Maintains Qt integration where needed

## Architecture

```
┌─────────────────────────────────────┐
│           Qt Components             │
│  ┌─────────────────────────────────┐│
│  │    GraphEditorHotkeyAdapter     ││  ← Qt Layer
│  │  - Inherits QObject             ││
│  │  - Emits PyQt signals           ││
│  │  - Handles Qt integration       ││
│  └─────────────────────────────────┘│
└──────────────┬──────────────────────┘
               │ Delegates to
               ▼
┌─────────────────────────────────────┐
│    GraphEditorHotkeyService         │  ← Pure Service Layer
│  - No Qt dependencies              │
│  - Uses callback protocol          │
│  - Framework-agnostic logic        │
│  - Testable in isolation           │
└─────────────────────────────────────┘
```

## Benefits

### ✅ Service Separation

- Core service logic is completely framework-agnostic
- No Qt dependencies in the service layer
- Follows TKA's architectural principles

### ✅ Flexibility

- Can use pure service in non-Qt contexts
- Can use adapter in Qt contexts
- Easy to mock and test

### ✅ Maintainability

- Clear separation of concerns
- Qt-specific code isolated to adapter
- Business logic in pure service

### ✅ Backward Compatibility

- Adapter maintains same signal interface
- Existing Qt components can use adapter unchanged
- Migration path for existing code

## Usage Patterns

### For Qt Components (Use Adapter)

```python
from .graph_editor_hotkey_adapter import GraphEditorHotkeyAdapter

# Create adapter with Qt signal support
hotkey_adapter = GraphEditorHotkeyAdapter(graph_service)

# Connect to Qt signals as before
hotkey_adapter.arrow_moved.connect(self.handle_arrow_moved)
hotkey_adapter.rotation_override_requested.connect(self.handle_rotation)

# Handle key events
hotkey_adapter.handle_key_event(key_event)
```

### For Non-Qt Components (Use Pure Service)

```python
from .graph_editor_hotkey_service import GraphEditorHotkeyService

class MyCallbackHandler:
    def on_arrow_moved(self, arrow_id: str, delta_x: int, delta_y: int):
        # Handle arrow movement without Qt
        pass

    def on_rotation_override_requested(self, arrow_id: str):
        # Handle rotation override without Qt
        pass

# Create pure service with callbacks
callback_handler = MyCallbackHandler()
hotkey_service = GraphEditorHotkeyService(graph_service, callback_handler)

# Handle key events
hotkey_service.handle_key_event(key_event)
```

## Implementation Details

### Callback Protocol

```python
class IHotkeyCallbacks(Protocol):
    """Protocol defining callbacks for hotkey actions"""

    def on_arrow_moved(self, arrow_id: str, delta_x: int, delta_y: int) -> None: ...
    def on_rotation_override_requested(self, arrow_id: str) -> None: ...
    def on_special_placement_removal_requested(self, arrow_id: str) -> None: ...
    def on_prop_placement_override_requested(self, arrow_id: str) -> None: ...
```

### Adapter Bridge

```python
class HotkeyCallbackHandler:
    """Bridges service callbacks to Qt signals"""

    def __init__(self, adapter: GraphEditorHotkeyAdapter):
        self.adapter = adapter

    def on_arrow_moved(self, arrow_id: str, delta_x: int, delta_y: int) -> None:
        self.adapter.arrow_moved.emit(arrow_id, delta_x, delta_y)
```

## Testing Benefits

### Pure Service Testing

```python
def test_hotkey_service():
    # Mock callback handler
    mock_callbacks = Mock(spec=IHotkeyCallbacks)

    # Test pure service without Qt
    service = GraphEditorHotkeyService(mock_graph_service, mock_callbacks)

    # Verify behavior without Qt dependencies
    service.handle_key_event(mock_key_event)
    mock_callbacks.on_arrow_moved.assert_called_once()
```

### Adapter Testing

```python
def test_hotkey_adapter():
    # Test Qt signal emissions
    adapter = GraphEditorHotkeyAdapter(mock_graph_service)

    with QSignalSpy(adapter.arrow_moved) as spy:
        adapter.handle_key_event(mock_key_event)
        assert len(spy) == 1
```

## Migration Guide

### For Existing Code Using Signals

```python
# OLD: Direct service usage
hotkey_service = GraphEditorHotkeyService(graph_service)
hotkey_service.arrow_moved.connect(handler)

# NEW: Use adapter (drop-in replacement)
hotkey_adapter = GraphEditorHotkeyAdapter(graph_service)
hotkey_adapter.arrow_moved.connect(handler)  # Same interface!
```

### For New Code

- Use `GraphEditorHotkeyAdapter` for Qt components
- Use `GraphEditorHotkeyService` for pure logic/testing
- Implement `IHotkeyCallbacks` for custom handling

## Conclusion

This refactoring successfully addresses the service separation violation while maintaining backward compatibility and improving testability. The Adapter Pattern provides a clean bridge between the Qt presentation layer and the pure service layer, following TKA's architectural principles.
