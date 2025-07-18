# Option Picker Core Architecture Audit

## Overview

This audit examines the `presentation/components/option_picker/core` directory to identify business logic that should be extracted to the `application/services` layer. The codebase has already undergone significant refactoring, but several opportunities remain for better separation of concerns.

## Current Architecture State

### ✅ Well-Architected Components

The following components properly follow presentation layer principles:

1. **`group_widget.py`** - Pure Qt layout management
2. **`option_picker_section_header.py`** - Simple Qt widget composition
3. **`option_picker_section_button.py`** - Pure Qt button behavior and styling

### 🔧 Services Needing Extraction

## 1. **Size Provider Logic** ❗ HIGH PRIORITY

**File:** `option_picker.py`
**Lines:** 62-99 (the `_get_size_provider` method)

**Issue:** Complex main window discovery logic embedded in presentation layer

**Current Code:**

```python
def _get_size_provider(self) -> Callable[[], QSize]:
    """Get size provider for the simplified picker that finds the main window."""
    def size_provider():
        # Complex hierarchy walking logic
        widget = self
        while widget and widget.parent():
            widget = widget.parent()
            # Look for QMainWindow or a widget with "MainWindow" in its class name
            if hasattr(widget, "__class__"):
                class_name = widget.__class__.__name__
                if "MainWindow" in class_name or hasattr(widget, "menuBar"):
                    return widget.size()
        # Fallback logic...
```

**Recommended Service:**

```
application/services/ui/window_discovery_service.py
```

**Service Interface:**

- `find_main_window() -> Optional[QWidget]`
- `get_main_window_size() -> QSize`
- `register_main_window(window: QWidget) -> None`

**Benefits:**

- Centralized window discovery logic
- Testable without UI dependencies
- Reusable across components
- Removes complex hierarchy walking from presentation

---

## 2. **Widget Pool Management** 🔄 MEDIUM PRIORITY

**File:** `pictograph_option_frame.py`
**Lines:** 42-43, 109-111

**Issue:** Direct service location and pool management in presentation component

**Current Code:**

```python
def _setup_ui(self):
    # Direct service location
    pool = get_pictograph_pool()
    self._pictograph_component = pool.checkout_pictograph(parent=self)

def cleanup(self):
    """Return the pictograph component to the pool."""
    if self._pictograph_component:
        pool = get_pictograph_pool()  # Service location again
        pool.checkin_pictograph(self._pictograph_component)
```

**Recommended Service Enhancement:**

```
application/services/option_picker/widget_lifecycle_service.py
```

**Service Interface:**

- `create_pictograph_frame(parent: QWidget) -> PictographOptionFrame`
- `cleanup_pictograph_frame(frame: PictographOptionFrame) -> None`
- `get_frame_pool_stats() -> Dict[str, Any]`

**Benefits:**

- Removes service location from presentation layer
- Centralizes widget lifecycle management
- Better error handling and logging
- Pool statistics and monitoring

---

## 3. **Sizing Calculation Logic** 📏 MEDIUM PRIORITY

**File:** `pictograph_option_frame.py`
**Lines:** 150-169

**Issue:** Business logic for size calculations in presentation layer

**Current Code:**

```python
def resize_option_view(self, main_window_size, option_picker_width, spacing=3):
    """Resize using Legacy sizing strategy."""
    # Legacy formula: max(main_window_width // 16, option_picker_width // 8)
    size_option_1 = main_window_size.width() // 16
    size_option_2 = option_picker_width // 8
    size = max(size_option_1, size_option_2)

    # Calculate border width (Legacy: max(1, int(size * 0.015)))
    border_width = max(1, int(size * 0.015))

    # Adjust for border and spacing (Legacy: size -= 2 * bw + spacing)
    adjusted_size = size - (2 * border_width) - spacing
    adjusted_size = max(adjusted_size, 60)  # Minimum size
```

**Recommendation:**
Enhance existing `application/services/option_picker/option_sizing_service.py`

**Missing Methods:**

- `calculate_frame_size(main_window_size: QSize, picker_width: int, spacing: int) -> int`
- `calculate_border_width(base_size: int) -> int`
- `apply_size_constraints(size: int) -> int`

---

## 4. **Error Handling and Logging** 📊 LOW-MEDIUM PRIORITY

**File:** Multiple files
**Issue:** Inconsistent error handling and debugging output scattered across presentation layer

**Current Examples:**

```python
# From option_picker_scroll.py
print(f"❌ [UI] No options received from service")

# From option_picker_section.py
print(f"🚨 [REGRESSION] Section {self.letter_type} using FALLBACK 800x600 size provider!")
```

**Recommended Service:**

```
application/services/core/component_logging_service.py
```

**Service Interface:**

- `log_component_event(component: str, event: str, level: LogLevel) -> None`
- `log_performance_metric(component: str, metric: str, value: Any) -> None`
- `log_error(component: str, error: Exception, context: Dict) -> None`

---

## 5. **Service Resolution and Dependency Injection** 🔧 HIGH PRIORITY

**File:** `option_picker_widget.py`
**Lines:** 81-122

**Issue:** Complex fallback logic and service resolution in presentation layer

**Current Code:**

```python
def _create_scroll_widget_fallback(self):
    """Create OptionPickerScroll directly without DI container (fallback)."""
    try:
        from core.dependency_injection.di_container import get_container
        fallback_container = get_container()

        # Manual service resolution...
        sequence_service = fallback_container.resolve(SequenceOptionService)
        pool_service = fallback_container.resolve(OptionPoolService)
        # ... more manual resolution
```

**Recommended Service:**

```
application/services/core/component_factory_service.py
```

**Service Interface:**

- `create_option_picker_scroll(parent: QWidget, size_provider: Callable) -> OptionPickerScroll`
- `resolve_required_services() -> Dict[str, Any]`
- `validate_service_dependencies() -> bool`

---

## Architectural Recommendations

### 1. **Service Layer Organization**

```
application/services/
├── ui/
│   ├── window_discovery_service.py    # NEW
│   └── component_lifecycle_service.py # NEW
├── option_picker/
│   ├── widget_lifecycle_service.py    # NEW
│   └── [existing services...]
└── core/
    ├── component_logging_service.py   # NEW
    └── component_factory_service.py   # NEW
```

### 2. **Interface Definitions**

Create interface contracts in:

```
core/interfaces/ui_services.py
```

### 3. **Dependency Injection Enhancement**

- Remove all service location (`get_*()` calls) from presentation layer
- Use constructor injection exclusively
- Create factory services for complex component creation

## Implementation Priority

### Phase 1 (High Priority)

1. Extract window discovery service
2. Enhance dependency injection patterns
3. Remove service location from presentation components

### Phase 2 (Medium Priority)

1. Extract widget lifecycle service
2. Enhance sizing service with frame-specific methods
3. Implement component logging service

### Phase 3 (Low Priority)

1. Create component factory service
2. Add service validation and monitoring
3. Implement comprehensive error handling patterns

## Compliance Assessment

### ✅ Good Separation of Concerns

- UI components properly use injected services
- Business logic delegated to service layer
- Clean Qt widget management

### ⚠️ Areas Needing Improvement

- Size provider logic too complex for presentation layer
- Service location still present in some components
- Inconsistent error handling patterns
- Manual service resolution fallbacks

### 🎯 Target Architecture

- Pure presentation components with zero business logic
- All services injected via constructor
- Centralized component lifecycle management
- Consistent logging and error handling

## Detailed Code Analysis

### Current Service Location Anti-Patterns

**Pattern 1: Direct Service Import and Call**

```python
# ❌ BAD: Direct service location in presentation layer
from application.services.pictograph_pool_manager import get_pictograph_pool

def _setup_ui(self):
    pool = get_pictograph_pool()  # Service location
    self._pictograph_component = pool.checkout_pictograph(parent=self)
```

**Pattern 2: Fallback Service Resolution**

```python
# ❌ BAD: Complex fallback logic in presentation
def _create_scroll_widget_fallback(self):
    from core.dependency_injection.di_container import get_container
    fallback_container = get_container()
    sequence_service = fallback_container.resolve(SequenceOptionService)
    # Manual service resolution...
```

### Recommended Dependency Injection Patterns

**Pattern 1: Constructor Injection**

```python
# ✅ GOOD: Clean constructor injection
class PictographOptionFrame(QFrame):
    def __init__(self,
                 parent=None,
                 pictograph_pool_service: PictographPoolService = None,
                 widget_lifecycle_service: WidgetLifecycleService = None):
        super().__init__(parent)
        self._pool_service = pictograph_pool_service
        self._lifecycle_service = widget_lifecycle_service
```

**Pattern 2: Factory Service Creation**

```python
# ✅ GOOD: Factory service handles complexity
class ComponentFactoryService:
    def create_option_picker_scroll(self, parent: QWidget, size_provider: Callable) -> OptionPickerScroll:
        # Resolve all dependencies
        sequence_service = self._container.resolve(SequenceOptionService)
        pool_service = self._container.resolve(OptionPoolService)
        # Create with proper injection
        return OptionPickerScroll(
            parent=parent,
            sequence_option_service=sequence_service,
            option_pool_service=pool_service,
            # ...
        )
```

### Size Provider Extraction Example

**Current Implementation (❌ BAD):**

```python
# In option_picker.py - Complex hierarchy walking in presentation
def _get_size_provider(self) -> Callable[[], QSize]:
    def size_provider():
        widget = self
        level = 0
        while widget and widget.parent():
            widget = widget.parent()
            level += 1
            if hasattr(widget, "__class__"):
                class_name = widget.__class__.__name__
                if "MainWindow" in class_name or hasattr(widget, "menuBar"):
                    size = widget.size()
                    return size
        # Complex fallback logic...
```

**Recommended Service (✅ GOOD):**

```python
# In application/services/ui/window_discovery_service.py
class WindowDiscoveryService:
    def __init__(self):
        self._main_window: Optional[QWidget] = None

    def register_main_window(self, window: QWidget) -> None:
        """Register the main window during application startup."""
        self._main_window = window

    def get_main_window_size(self) -> QSize:
        """Get main window size with proper fallbacks."""
        if self._main_window:
            return self._main_window.size()

        # Clean fallback logic
        app = QApplication.instance()
        if app and app.activeWindow():
            return app.activeWindow().size()

        # Final fallback
        return QSize(1200, 800)
```

### Widget Lifecycle Management

**Current Pattern (❌ BAD):**

```python
# Scattered pool management in presentation layer
def cleanup(self):
    if self._pictograph_component:
        pool = get_pictograph_pool()  # Service location
        pool.checkin_pictograph(self._pictograph_component)
```

**Recommended Service (✅ GOOD):**

```python
# In application/services/option_picker/widget_lifecycle_service.py
class WidgetLifecycleService:
    def __init__(self, pictograph_pool_service: PictographPoolService):
        self._pool_service = pictograph_pool_service
        self._managed_frames: Dict[int, PictographOptionFrame] = {}

    def create_pictograph_frame(self, parent: QWidget) -> PictographOptionFrame:
        """Create frame with proper pool management."""
        pictograph_component = self._pool_service.checkout_pictograph(parent)
        frame = PictographOptionFrame(parent, pictograph_component)
        frame_id = id(frame)
        self._managed_frames[frame_id] = frame
        return frame

    def cleanup_pictograph_frame(self, frame: PictographOptionFrame) -> None:
        """Clean up frame and return resources to pool."""
        frame_id = id(frame)
        if frame_id in self._managed_frames:
            if hasattr(frame, '_pictograph_component'):
                self._pool_service.checkin_pictograph(frame._pictograph_component)
            del self._managed_frames[frame_id]
```

## Testing Strategy

### Unit Testing Services

```python
# Test window discovery service without Qt dependencies
def test_window_discovery_service():
    service = WindowDiscoveryService()
    mock_window = Mock()
    mock_window.size.return_value = QSize(1920, 1080)

    service.register_main_window(mock_window)
    size = service.get_main_window_size()

    assert size.width() == 1920
    assert size.height() == 1080
```

### Integration Testing

```python
# Test component creation with proper service injection
def test_option_picker_creation_with_services():
    container = DIContainer()
    # Register all required services
    container.register(WindowDiscoveryService)
    container.register(WidgetLifecycleService)

    # Create component through factory
    factory = container.resolve(ComponentFactoryService)
    picker = factory.create_option_picker_scroll(None, lambda: QSize(800, 600))

    assert picker is not None
    assert hasattr(picker, '_sequence_option_service')
```

## Migration Path

### Step 1: Create New Services

1. Create `WindowDiscoveryService` in `application/services/ui/`
2. Create `WidgetLifecycleService` in `application/services/option_picker/`
3. Create `ComponentFactoryService` in `application/services/core/`

### Step 2: Update DI Registration

```python
# In service_registration.py
def register_ui_services(container: DIContainer):
    container.register(WindowDiscoveryService)
    container.register(WidgetLifecycleService)
    container.register(ComponentFactoryService)
```

### Step 3: Refactor Presentation Components

1. Remove service location calls from `PictographOptionFrame`
2. Update `OptionPicker` to use `WindowDiscoveryService`
3. Replace fallback logic in `OptionPickerWidget` with factory service

### Step 4: Update Tests

1. Add unit tests for new services
2. Update integration tests to use proper DI
3. Add regression tests for size provider functionality

## Conclusion

The option picker core has made significant progress toward proper layered architecture. The main remaining issues are:

1. **Complex algorithms in presentation layer** (size provider, sizing calculations)
2. **Service location patterns** that should be dependency injection
3. **Lifecycle management** scattered across components

Implementing the recommended service extractions will complete the separation of concerns and create a fully maintainable, testable architecture.

### Success Metrics

- ✅ Zero service location calls in presentation layer
- ✅ All business logic in service layer
- ✅ 100% constructor injection for dependencies
- ✅ Comprehensive unit test coverage for services
- ✅ Clean separation between Qt UI logic and business logic
