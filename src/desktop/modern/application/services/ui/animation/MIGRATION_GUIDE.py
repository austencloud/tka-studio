"""
Migration Guide: From Legacy FadeManager to Modern Fade System

This guide provides step-by-step instructions for migrating from the legacy
FadeManager to the modern dependency-injection-based fade system.
"""

# 1. DEPENDENCY INJECTION SETUP

"""
First, register the fade services in your main DI configuration.
Add this to your main DI setup file (likely in src/core/dependency_injection/).
"""

# In your main DI configuration file:
from desktop.modern.application.services.ui.animation import setup_animation_services

def configure_all_services(container):
    """Configure all application services."""
    # ... your existing service registrations ...
    
    # Add animation services
    setup_animation_services(container)
    
    # ... rest of your configuration ...


# 2. UPDATING UI COMPONENTS

"""
Replace legacy FadeManager usage in your UI components.
"""

# OLD WAY (Legacy):
class OldMainWidget:
    def __init__(self, app_context):
        # Legacy fade manager creation
        from main_window.main_widget.fade_manager.fade_manager import FadeManager
        self.fade_manager = FadeManager(self, app_context)
    
    def some_fade_operation(self):
        # Legacy fade calls
        self.fade_manager.widget_fader.fade_widgets([self.some_widget], True, duration=250)
        self.fade_manager.stack_fader.fade_stack(self.stack, 1)

# NEW WAY (Modern):
class NewMainWidget:
    def __init__(self, container):
        # Get fade orchestrator from DI container
        from desktop.modern.core.interfaces.animation_interfaces import IFadeOrchestrator
        self.fade_orchestrator = container.resolve(IFadeOrchestrator)
    
    async def some_fade_operation(self):
        # Modern fade calls
        await self.fade_orchestrator.fade_widgets_in([self.some_widget], 
                                                   FadeOptions(duration=250))
        await self.fade_orchestrator.fade_stack_transition(self.stack, 1)


# 3. MIGRATION PATTERNS

"""
Common migration patterns for different types of fade operations.
"""

# Pattern 1: Widget Fading
# OLD: fade_manager.widget_fader.fade_widgets(widgets, fade_in, duration=250, callback=None)
# NEW: await fade_orchestrator.fade_widgets_in/out(widgets, FadeOptions(duration=250, callback=callback))

class WidgetFadeMigration:
    def __init__(self, fade_orchestrator):
        self.fade_orchestrator = fade_orchestrator
    
    # OLD VERSION:
    def legacy_fade_widgets(self, fade_manager, widgets):
        fade_manager.widget_fader.fade_widgets(widgets, True, duration=300)
    
    # NEW VERSION:
    async def modern_fade_widgets(self, widgets):
        options = FadeOptions(duration=300)
        await self.fade_orchestrator.fade_widgets_in(widgets, options)

# Pattern 2: Fade and Update
# OLD: fade_manager.widget_fader.fade_and_update(widgets, callback, duration=250)
# NEW: await fade_orchestrator.fade_widgets_and_update(widgets, update_callback, options)

class FadeAndUpdateMigration:
    def __init__(self, fade_orchestrator):
        self.fade_orchestrator = fade_orchestrator
    
    # OLD VERSION:
    def legacy_fade_and_update(self, fade_manager, widgets):
        def update_content():
            # Update logic here
            pass
        fade_manager.widget_fader.fade_and_update(widgets, update_content)
    
    # NEW VERSION:
    async def modern_fade_and_update(self, widgets):
        def update_content():
            # Update logic here
            pass
        await self.fade_orchestrator.fade_widgets_and_update(widgets, update_content)

# Pattern 3: Stack Transitions
# OLD: fade_manager.stack_fader.fade_stack(stack, new_index, duration=300, callback=None)
# NEW: await fade_orchestrator.fade_stack_transition(stack, new_index, options)

class StackMigration:
    def __init__(self, fade_orchestrator):
        self.fade_orchestrator = fade_orchestrator
    
    # OLD VERSION:
    def legacy_stack_transition(self, fade_manager, stack, new_index):
        fade_manager.stack_fader.fade_stack(stack, new_index, duration=400)
    
    # NEW VERSION:
    async def modern_stack_transition(self, stack, new_index):
        options = StackFadeOptions(duration=400)
        await self.fade_orchestrator.fade_stack_transition(stack, new_index, options)

# Pattern 4: Parallel Stack Operations
# OLD: fade_manager.parallel_stack_fader.fade_both_stacks(right_stack, right_index, left_stack, left_index, ratio)
# NEW: await fade_orchestrator.fade_parallel_stack_transition(operation)

class ParallelStackMigration:
    def __init__(self, fade_orchestrator):
        self.fade_orchestrator = fade_orchestrator
    
    # OLD VERSION:
    def legacy_parallel_stacks(self, fade_manager, left_stack, right_stack):
        fade_manager.parallel_stack_fader.fade_both_stacks(
            right_stack, 1, left_stack, 2, (2, 1), duration=350
        )
    
    # NEW VERSION:
    async def modern_parallel_stacks(self, left_stack, right_stack):
        operation = ParallelStackOperation(
            left_stack=left_stack,
            left_new_index=2,
            right_stack=right_stack,
            right_new_index=1,
            layout_ratio=(2, 1),
            options=StackFadeOptions(duration=350)
        )
        await self.fade_orchestrator.fade_parallel_stack_transition(operation)


# 4. HANDLING ASYNC/AWAIT IN QT

"""
Strategies for handling async/await in Qt event handlers and slots.
"""

from PyQt6.QtCore import QObject, pyqtSlot
import asyncio

class AsyncQtIntegration(QObject):
    def __init__(self, fade_orchestrator):
        super().__init__()
        self.fade_orchestrator = fade_orchestrator
    
    # Strategy 1: Fire-and-forget for simple cases
    @pyqtSlot()
    def on_button_clicked(self):
        """Qt slot that starts async fade without waiting."""
        # Start fade but don't wait for completion
        asyncio.create_task(
            self.fade_orchestrator.fade_widget_in(self.some_widget)
        )
    
    # Strategy 2: Use callbacks for completion handling
    @pyqtSlot()
    def on_complex_operation(self):
        """Qt slot with completion callback."""
        def on_fade_complete():
            # Handle completion
            self.update_ui_after_fade()
        
        options = FadeOptions(callback=on_fade_complete)
        asyncio.create_task(
            self.fade_orchestrator.fade_widget_in(self.some_widget, options)
        )
    
    # Strategy 3: Use the sync method for legacy compatibility
    @pyqtSlot()
    def on_legacy_operation(self):
        """Qt slot using sync fade for backward compatibility."""
        # This starts the animation but doesn't block
        self.fade_orchestrator.fade_widget_sync(self.some_widget, fade_in=True)


# 5. GRADUAL MIGRATION STRATEGY

"""
Use the legacy adapter for gradual migration.
"""

class GradualMigrationExample:
    def __init__(self, container):
        # Get both modern orchestrator and legacy adapter
        from desktop.modern.core.interfaces.animation_interfaces import IFadeOrchestrator
        from desktop.modern.application.services.ui.animation import LegacyFadeManagerAdapter
        
        self.fade_orchestrator = container.resolve(IFadeOrchestrator)
        self.legacy_adapter = container.resolve(LegacyFadeManagerAdapter)
    
    def mixed_usage_example(self):
        """Example showing mixed modern and legacy usage."""
        # Use legacy adapter for code that hasn't been migrated yet
        self.legacy_adapter.widget_fader.fade_widgets([self.old_widget], True)
        
        # Use modern API for new code
        asyncio.create_task(
            self.fade_orchestrator.fade_widget_in(self.new_widget)
        )


# 6. SETTINGS INTEGRATION

"""
The new system integrates with your existing settings system.
Make sure these settings exist in your settings configuration.
"""

REQUIRED_SETTINGS = {
    "ui.animations.fades_enabled": True,        # Enable/disable fades
    "ui.animations.default_duration": 250,     # Default animation duration (ms)
    "ui.animations.default_easing": "IN_OUT_QUAD"  # Default easing type
}

class SettingsSetup:
    def __init__(self, settings_coordinator):
        self.settings = settings_coordinator
        self.ensure_animation_settings()
    
    def ensure_animation_settings(self):
        """Ensure animation settings exist with defaults."""
        for key, default_value in REQUIRED_SETTINGS.items():
            if self.settings.get_setting(key) is None:
                self.settings.set_setting(key, default_value)


# 7. TESTING MIGRATION

"""
Steps to test your migration:
"""

def test_migration_checklist():
    """
    Migration testing checklist:
    
    1. ✅ All animation services register correctly in DI container
    2. ✅ Legacy FadeManager references are replaced
    3. ✅ Settings integration works (fades can be enabled/disabled)
    4. ✅ Basic fade operations work (fade in/out)
    5. ✅ Stack transitions work
    6. ✅ Parallel stack operations work
    7. ✅ Legacy adapter works for unmigrated code
    8. ✅ No Qt graphics effect memory leaks
    9. ✅ Performance is acceptable
    10. ✅ Error handling works correctly
    """

# 8. SPECIFIC FILE UPDATES NEEDED

"""
Files that need to be updated during migration:
"""

FILES_TO_UPDATE = [
    # Main DI configuration
    "src/core/dependency_injection/config_registration.py",  # Add animation service registration
    
    # Main window and UI components
    "src/presentation/tabs/*/tab_widget.py",                # Update tab widgets
    "src/presentation/components/*/widget.py",              # Update individual components
    
    # Any direct FadeManager imports
    "**/*widget*.py",                                       # Search for FadeManager imports
    "**/*main*.py",                                         # Search in main files
    
    # Settings files
    "src/application/services/settings/settings_defaults.py",  # Add animation settings
]


# 9. IMPORT UPDATES

"""
Update import statements throughout your codebase:
"""

# OLD IMPORTS (to remove):
# from main_window.main_widget.fade_manager.fade_manager import FadeManager
# from main_window.main_widget.fade_manager.widget_fader import WidgetFader

# NEW IMPORTS (to add):
from desktop.modern.core.interfaces.animation_interfaces import FadeOptions, StackFadeOptions
from desktop.modern.application.services.ui.animation import LegacyFadeManagerAdapter  # For gradual migration


# 10. PERFORMANCE CONSIDERATIONS

"""
The new system should perform as well or better than the legacy system:

- Automatic graphics effect cleanup prevents memory leaks
- Animation caching is handled internally
- Async/await allows better UI responsiveness
- Settings integration reduces redundant checks
"""

class PerformanceNotes:
    """
    Performance improvements in the new system:
    
    1. Better Memory Management:
       - Automatic graphics effect cleanup
       - Tracked effect lifecycles
       - No manual cleanup required
    
    2. Improved Responsiveness:
       - Async operations don't block UI
       - Better animation queuing
       - Smoother transitions
    
    3. Reduced Coupling:
       - Services can be optimized independently
       - Better testability leads to better optimization
       - Clear dependency boundaries
    """
