"""
Modern Animation System for TKA Desktop Application

This package provides a framework-agnostic animation system with Qt adapters.
The system is designed for enterprise use with proper separation of concerns,
command pattern support, event-driven architecture, and cross-platform portability.

## Architecture

The system consists of three main layers:

1. **Core Layer** (`core.animation`): Framework-agnostic animation engine
   - Animation engine with timing and easing
   - Event system for animation lifecycle
   - Command pattern for operations

2. **Adapter Layer** (`adapters`): Platform-specific implementations
   - Qt adapters for PyQt6/Qt widgets
   - Web adapters (future)
   - Other framework adapters (future)

3. **Orchestrator Layer**: High-level services combining core + adapters
   - Modern async/await API
   - Legacy compatibility wrapper
   - DI integration

## Usage Examples

### Modern API (Recommended)
```python
# Get orchestrator from DI container
orchestrator = container.resolve(IAnimationOrchestrator)

# Fade widget in
await orchestrator.fade_target(my_widget, fade_in=True)

# Animate multiple widgets
await orchestrator.fade_targets([widget1, widget2], fade_in=False)

# Fade and update pattern
await orchestrator.transition_targets(
    widgets=[content_widget],
    update_callback=lambda: content_widget.setText("New content"),
)

# Stack transitions
await orchestrator.fade_stack_transition(stack_widget, new_index=1)
```

### Legacy API (For Migration)
```python
# Get legacy wrapper from DI container
fade_manager = container.resolve(LegacyFadeManagerWrapper)

# Legacy fade calls (compatible with old code)
fade_manager.widget_fader.fade_widgets([widget], True, duration=250)
fade_manager.stack_fader.fade_stack(stack, 1, duration=300)
```

## Key Benefits

1. **Framework Agnostic**: Core logic works across platforms
2. **Event Driven**: Proper event system for animation lifecycle
3. **Command Pattern**: Undo/redo support, better testing
4. **Async/Await**: Modern patterns, better performance
5. **DI Integration**: Proper service architecture
6. **Legacy Compatible**: Smooth migration path
7. **Cross-Platform Ready**: Designed for web portability

## Migration from Legacy FadeManager

1. Add to DI container:
   ```python
   from desktop.modern.application.services.ui.animation import (
       setup_modern_animation_services,
   )

   setup_modern_animation_services(container)
   ```

2. Update components to use new API:
   ```python
   # Old
   fade_manager.widget_fader.fade_widgets([widget], True)

   # New
   await orchestrator.fade_target(widget, fade_in=True)
   ```

3. Or use legacy wrapper during transition:
   ```python
   legacy_wrapper = container.resolve(LegacyFadeManagerWrapper)
   legacy_wrapper.widget_fader.fade_widgets([widget], True)
   ```
"""

# Core interfaces
# Core engine
from __future__ import annotations

from desktop.modern.core.animation.animation_engine import (
    CoreAnimationEngine,
    DefaultSettingsProvider,
    EasingFunctions,
    create_default_animation_engine,
)
from desktop.modern.core.interfaces.animation_core_interfaces import (
    AnimationConfig,
    AnimationState,
    AnimationTarget,
    AnimationType,
    EasingType,
    FadeCommand,
    IAnimationCommand,
    IAnimationEngine,
    IAnimationOrchestrator,
    TransitionCommand,
)

# Qt adapters
from .adapters.qt_adapters import (
    QtAnimationRenderer,
    QtAnimationScheduler,
    QtGraphicsEffectManager,
    QtStackWidgetAdapter,
    QtTargetAdapter,
    create_qt_animation_components,
)

# Main orchestrator
from .animation_orchestrator import (
    LegacyFadeManagerWrapper,
    ModernAnimationOrchestrator,
    create_modern_animation_system,
)

# Legacy animation service removed due to shared dependency issues
# from .animation_service import AnimationService as LegacyAnimationService
# Legacy compatibility (keeping old exports)
from .fade_orchestrator import FadeOrchestrator as LegacyFadeOrchestrator

# DI registration
from .modern_service_registration import (
    ModernAnimationServiceRegistration,
    setup_modern_animation_services,
)


__all__ = [
    "AnimationConfig",
    "AnimationState",
    # Data classes
    "AnimationTarget",
    "AnimationType",
    # Core engine
    "CoreAnimationEngine",
    "DefaultSettingsProvider",
    "EasingFunctions",
    "EasingType",
    # Commands
    "FadeCommand",
    "IAnimationCommand",
    "IAnimationEngine",
    # Main interfaces
    "IAnimationOrchestrator",
    "LegacyFadeManagerWrapper",
    # Legacy compatibility
    "LegacyFadeOrchestrator",
    # Modern orchestrator (primary interface)
    "ModernAnimationOrchestrator",
    "ModernAnimationServiceRegistration",
    "QtAnimationRenderer",
    "QtAnimationScheduler",
    "QtGraphicsEffectManager",
    "QtStackWidgetAdapter",
    # Qt adapters
    "QtTargetAdapter",
    "TransitionCommand",
    "create_default_animation_engine",
    "create_modern_animation_system",
    "create_qt_animation_components",
    # DI setup
    "setup_modern_animation_services",
]

# Version info
__version__ = "2.0.0"
__description__ = "Modern, framework-agnostic animation system for TKA"
