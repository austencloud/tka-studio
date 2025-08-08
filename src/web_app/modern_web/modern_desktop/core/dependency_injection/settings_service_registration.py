"""
Settings Service Registration for Dependency Injection

Registers all settings services in the DI container following TKA's
clean architecture patterns and service composition principles.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtCore import QSettings

from desktop.modern.application.services.settings.background_settings_manager import (
    BackgroundSettingsManager,
)
from desktop.modern.application.services.settings.beat_layout_settings_manager import (
    BeatLayoutSettingsManager,
)
from desktop.modern.application.services.settings.image_export_settings_manager import (
    ImageExportSettingsManager,
)

# Import service implementations
from desktop.modern.application.services.settings.modern_settings_service import (
    ModernSettingsService,
)
from desktop.modern.application.services.settings.prop_type_settings_manager import (
    PropTypeSettingsManager,
)
from desktop.modern.application.services.settings.user_profile_settings_manager import (
    UserProfileSettingsManager,
)
from desktop.modern.application.services.settings.visibility_settings_manager import (
    VisibilitySettingsManager,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.session_services import ISessionStateTracker
from desktop.modern.core.interfaces.settings_services import (
    IBackgroundSettingsManager,
    IBeatLayoutSettingsManager,
    IImageExportSettingsManager,
    IPropTypeSettingsManager,
    IUserProfileSettingsManager,
    IVisibilitySettingsManager,
)


logger = logging.getLogger(__name__)


def register_settings_services(container: DIContainer) -> None:
    """
    Register all settings services in the DI container.

    This follows the service composition pattern where:
    1. Individual managers are registered first
    2. Main settings service is registered with manager dependencies
    3. All services are properly initialized and connected

    Args:
        container: DI container instance

    Raises:
        Exception: If service registration fails
    """
    try:
        # Create shared QSettings instance
        def create_shared_settings():
            return QSettings("TKA", "KineticConstructor")

        # Register individual settings managers with shared QSettings
        container.register_factory(
            IBackgroundSettingsManager,
            lambda: BackgroundSettingsManager(create_shared_settings()),
        )

        container.register_factory(
            IVisibilitySettingsManager,
            lambda: VisibilitySettingsManager(create_shared_settings()),
        )

        container.register_factory(
            IBeatLayoutSettingsManager,
            lambda: BeatLayoutSettingsManager(create_shared_settings()),
        )

        container.register_factory(
            IPropTypeSettingsManager,
            lambda: PropTypeSettingsManager(create_shared_settings()),
        )

        container.register_factory(
            IUserProfileSettingsManager,
            lambda: UserProfileSettingsManager(create_shared_settings()),
        )

        container.register_factory(
            IImageExportSettingsManager,
            lambda: ImageExportSettingsManager(create_shared_settings()),
        )

        # Register main settings service as singleton
        container.register_factory(
            ModernSettingsService, lambda: _create_settings_service(container)
        )

    except Exception as e:
        logger.error(f"❌ Failed to register settings services: {e}")
        raise


def _create_settings_service(container: DIContainer) -> ModernSettingsService:
    """Create main settings service with all dependencies."""
    try:
        # Get session tracker (should already be registered)
        session_tracker = container.resolve(ISessionStateTracker)

        # Create main settings service
        settings_service = ModernSettingsService(session_tracker)

        return settings_service

    except Exception as e:
        logger.error(f"Failed to create settings service: {e}")
        raise


def validate_settings_registration(container: DIContainer) -> bool:
    """
    Validate that all settings services are properly registered and functional.

    Args:
        container: DI container instance

    Returns:
        True if all services are working, False otherwise
    """
    try:
        # Test main settings service
        settings_service = container.resolve(ModernSettingsService)
        if not settings_service:
            logger.error("Main settings service not found")
            return False

        # Test individual managers
        managers_to_test = [
            (IBackgroundSettingsManager, "background"),
            (IVisibilitySettingsManager, "visibility"),
            (IBeatLayoutSettingsManager, "layout"),
            (IPropTypeSettingsManager, "prop type"),
            (IUserProfileSettingsManager, "user profile"),
            (IImageExportSettingsManager, "image export"),
        ]

        for interface, name in managers_to_test:
            try:
                manager = container.resolve(interface)
                if not manager:
                    logger.error(f"{name} manager not found")
                    return False
                logger.debug(f"✅ {name} manager validated")
            except Exception as e:
                logger.error(f"❌ Failed to resolve {name} manager: {e}")
                return False

        # Test basic functionality
        if not _test_basic_functionality(settings_service, container):
            return False

        logger.info("✅ All settings services validated successfully")
        return True

    except Exception as e:
        logger.error(f"❌ Settings validation failed: {e}")
        return False


def _test_basic_functionality(
    settings_service: ModernSettingsService, container: DIContainer
) -> bool:
    """Test basic functionality of the settings service."""
    try:
        # Test CQRS operations
        test_section = "test"
        test_key = "validation_test"
        test_value = "test_value_123"

        # Test command (write)
        if not settings_service.execute_setting_command(
            test_section, test_key, test_value
        ):
            logger.error("Failed to execute test setting command")
            return False

        # Test query (read)
        retrieved_value = settings_service.query_setting(test_section, test_key)
        if retrieved_value != test_value:
            logger.error(
                f"Test value mismatch: expected {test_value}, got {retrieved_value}"
            )
            return False

        # Test manager access - just verify managers can be resolved directly from container
        try:
            background_manager = container.resolve(IBackgroundSettingsManager)
            if not background_manager:
                logger.error("Background manager not resolvable from container")
                return False
        except Exception as e:
            logger.error(f"Failed to resolve background manager from container: {e}")
            return False

        # Clean up test data
        settings_service.settings.remove(f"{test_section}/{test_key}")
        settings_service.settings.sync()

        logger.debug("✅ Basic functionality test passed")
        return True

    except Exception as e:
        logger.error(f"❌ Basic functionality test failed: {e}")
        return False


def create_configured_settings_container(
    organization_name: str = "TKA", application_name: str = "KineticConstructor"
) -> DIContainer:
    """
    Create a fully configured DI container with all settings services.

    Args:
        organization_name: Organization name for QSettings
        application_name: Application name for QSettings

    Returns:
        Configured DI container instance

    Raises:
        Exception: If configuration fails
    """
    try:
        from desktop.modern.core.dependency_injection.di_container import DIContainer

        container = DIContainer()

        # Register core dependencies first
        from desktop.modern.application.services.core.session_state_tracker import (
            SessionStateTracker,
        )
        from desktop.modern.core.interfaces.core_services import IUIStateManager
        from desktop.modern.infrastructure.file_system.file_system_service import (
            FileSystemService,
        )

        # Register file system service
        container.register_singleton(FileSystemService, FileSystemService)

        # Create mock UI state manager for isolated testing
        class MockUIStateManager(IUIStateManager):
            def __init__(self):
                self._state = {}
                self._settings = {}

            def get_setting(self, key: str, default: Any = None) -> Any:
                return self._settings.get(key, default)

            def set_setting(self, key: str, value: Any) -> None:
                self._settings[key] = value

            def get_tab_state(self, tab_name: str) -> dict[str, Any]:
                return self._state.get(f"tab_{tab_name}", {})

            def get_all_settings(self) -> dict[str, Any]:
                return self._settings.copy()

            def clear_settings(self) -> None:
                self._settings.clear()

            def save_state(self) -> None:
                pass  # Mock implementation

            def load_state(self) -> None:
                pass  # Mock implementation

            def toggle_graph_editor(self) -> bool:
                current = self._settings.get("graph_editor_visible", False)
                self._settings["graph_editor_visible"] = not current
                return not current

            # Legacy methods for compatibility
            def get_ui_state(self, key: str = None):
                return self._state.get(key) if key else self._state.copy()

            def set_ui_state(self, key: str, value):
                self._state[key] = value

            def update_ui_state(self, updates: dict):
                self._state.update(updates)

            def reset_ui_state(self):
                self._state.clear()

            def save_ui_state(self) -> bool:
                return True

            def load_ui_state(self) -> bool:
                return True

        container.register_singleton(IUIStateManager, MockUIStateManager)

        # Register session tracker with proper dependencies
        container.register_factory(
            ISessionStateTracker,
            lambda: SessionStateTracker(
                container.resolve(IUIStateManager), container.resolve(FileSystemService)
            ),
        )

        # Register all settings services
        register_settings_services(container)

        # Validate registration
        if not validate_settings_registration(container):
            raise Exception("Settings service validation failed")

        logger.info(
            f"✅ Created configured settings container for {organization_name}/{application_name}"
        )
        return container

    except Exception as e:
        logger.error(f"❌ Failed to create configured settings container: {e}")
        raise
