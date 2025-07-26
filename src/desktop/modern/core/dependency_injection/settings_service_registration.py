"""
Settings Service Registration for Dependency Injection

Registers all settings services in the DI container following TKA's
clean architecture patterns and service composition principles.
"""

import logging
from typing import Optional

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.settings_services import (
    IBackgroundSettingsManager,
    IVisibilitySettingsManager,
    IBeatLayoutSettingsManager,
    IPropTypeSettingsManager,
    IUserProfileSettingsManager,
    IImageExportSettingsManager,
)
from desktop.modern.core.interfaces.session_services import ISessionStateTracker

# Import service implementations
from desktop.modern.application.services.settings.modern_settings_service import ModernSettingsService
from desktop.modern.application.services.settings.background_settings_manager import BackgroundSettingsManager
from desktop.modern.application.services.settings.visibility_settings_manager import VisibilitySettingsManager
from desktop.modern.application.services.settings.beat_layout_settings_manager import BeatLayoutSettingsManager
from desktop.modern.application.services.settings.prop_type_settings_manager import PropTypeSettingsManager
from desktop.modern.application.services.settings.user_profile_settings_manager import UserProfileSettingsManager
from desktop.modern.application.services.settings.image_export_settings_manager import ImageExportSettingsManager

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
        logger.info("🔧 Registering settings services...")
        
        # Register individual settings managers as factories to ensure proper QSettings sharing
        container.register_factory(
            IBackgroundSettingsManager,
            lambda: _create_background_manager(container)
        )
        
        container.register_factory(
            IVisibilitySettingsManager,
            lambda: _create_visibility_manager(container)
        )
        
        container.register_factory(
            IBeatLayoutSettingsManager,
            lambda: _create_layout_manager(container)
        )
        
        container.register_factory(
            IPropTypeSettingsManager,
            lambda: _create_prop_manager(container)
        )
        
        container.register_factory(
            IUserProfileSettingsManager,
            lambda: _create_user_manager(container)
        )
        
        container.register_factory(
            IImageExportSettingsManager,
            lambda: _create_export_manager(container)
        )
        
        # Register main settings service as singleton
        container.register_factory(
            ModernSettingsService,
            lambda: _create_settings_service(container)
        )
        
        logger.info("✅ Settings services registered successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to register settings services: {e}")
        raise


def _create_background_manager(container: DIContainer) -> BackgroundSettingsManager:
    """Create background settings manager with shared QSettings."""
    try:
        settings_service = _get_or_create_settings_service(container)
        return BackgroundSettingsManager(settings_service.settings)
    except Exception as e:
        logger.error(f"Failed to create background manager: {e}")
        raise


def _create_visibility_manager(container: DIContainer) -> VisibilitySettingsManager:
    """Create visibility settings manager with shared QSettings."""
    try:
        settings_service = _get_or_create_settings_service(container)
        return VisibilitySettingsManager(settings_service.settings)
    except Exception as e:
        logger.error(f"Failed to create visibility manager: {e}")
        raise


def _create_layout_manager(container: DIContainer) -> BeatLayoutSettingsManager:
    """Create layout settings manager with shared QSettings."""
    try:
        settings_service = _get_or_create_settings_service(container)
        return BeatLayoutSettingsManager(settings_service.settings)
    except Exception as e:
        logger.error(f"Failed to create layout manager: {e}")
        raise


def _create_prop_manager(container: DIContainer) -> PropTypeSettingsManager:
    """Create prop type settings manager with shared QSettings."""
    try:
        settings_service = _get_or_create_settings_service(container)
        return PropTypeSettingsManager(settings_service.settings)
    except Exception as e:
        logger.error(f"Failed to create prop manager: {e}")
        raise


def _create_user_manager(container: DIContainer) -> UserProfileSettingsManager:
    """Create user profile settings manager with shared QSettings."""
    try:
        settings_service = _get_or_create_settings_service(container)
        return UserProfileSettingsManager(settings_service.settings)
    except Exception as e:
        logger.error(f"Failed to create user manager: {e}")
        raise


def _create_export_manager(container: DIContainer) -> ImageExportSettingsManager:
    """Create image export settings manager with shared QSettings."""
    try:
        settings_service = _get_or_create_settings_service(container)
        return ImageExportSettingsManager(settings_service.settings)
    except Exception as e:
        logger.error(f"Failed to create export manager: {e}")
        raise


def _create_settings_service(container: DIContainer) -> ModernSettingsService:
    """Create main settings service with all dependencies."""
    try:
        # Get session tracker (should already be registered)
        session_tracker = container.resolve(ISessionStateTracker)
        
        # Create main settings service
        settings_service = ModernSettingsService(session_tracker)
        
        # Register all managers with the settings service
        _register_managers_with_service(container, settings_service)
        
        return settings_service
        
    except Exception as e:
        logger.error(f"Failed to create settings service: {e}")
        raise


def _register_managers_with_service(container: DIContainer, settings_service: ModernSettingsService) -> None:
    """Register all individual managers with the main settings service."""
    try:
        # Register background manager
        background_manager = container.resolve(IBackgroundSettingsManager)
        settings_service.register_background_manager(background_manager)
        
        # Register visibility manager
        visibility_manager = container.resolve(IVisibilitySettingsManager)
        settings_service.register_visibility_manager(visibility_manager)
        
        # Register layout manager
        layout_manager = container.resolve(IBeatLayoutSettingsManager)
        settings_service.register_layout_manager(layout_manager)
        
        # Register prop manager
        prop_manager = container.resolve(IPropTypeSettingsManager)
        settings_service.register_prop_manager(prop_manager)
        
        # Register user manager
        user_manager = container.resolve(IUserProfileSettingsManager)
        settings_service.register_user_manager(user_manager)
        
        # Register export manager
        export_manager = container.resolve(IImageExportSettingsManager)
        settings_service.register_export_manager(export_manager)
        
        logger.debug("All managers registered with settings service")
        
    except Exception as e:
        logger.error(f"Failed to register managers with settings service: {e}")
        raise


def _get_or_create_settings_service(container: DIContainer) -> ModernSettingsService:
    """Get existing settings service or create a minimal one for manager creation."""
    try:
        # Try to get existing settings service
        try:
            return container.resolve(ModernSettingsService)
        except:
            # Create minimal settings service for manager creation
            from desktop.modern.application.services.core.session_state_tracker import SessionStateTracker
            from desktop.modern.infrastructure.file_system.file_system_service import FileSystemService
            from desktop.modern.core.interfaces.core_services import IUIStateManager
            
            # Create minimal dependencies
            file_system_service = FileSystemService()
            
            # Create a mock UI state manager for testing
            class MockUIStateManager(IUIStateManager):
                def get_ui_state(self, key: str = None): return {}
                def set_ui_state(self, key: str, value): pass
                def update_ui_state(self, updates: dict): pass
                def reset_ui_state(self): pass
                def save_ui_state(self) -> bool: return True
                def load_ui_state(self) -> bool: return True
            
            ui_state_manager = MockUIStateManager()
            
            # Create session tracker
            session_tracker = SessionStateTracker(ui_state_manager, file_system_service)
            
            # Create minimal settings service
            return ModernSettingsService(session_tracker)
            
    except Exception as e:
        logger.error(f"Failed to get or create settings service: {e}")
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
        logger.info("🔍 Validating settings service registration...")
        
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
        if not _test_basic_functionality(settings_service):
            return False
        
        logger.info("✅ All settings services validated successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Settings validation failed: {e}")
        return False


def _test_basic_functionality(settings_service: ModernSettingsService) -> bool:
    """Test basic functionality of the settings service."""
    try:
        # Test CQRS operations
        test_section = "test"
        test_key = "validation_test"
        test_value = "test_value_123"
        
        # Test command (write)
        if not settings_service.execute_setting_command(test_section, test_key, test_value):
            logger.error("Failed to execute test setting command")
            return False
        
        # Test query (read)
        retrieved_value = settings_service.query_setting(test_section, test_key)
        if retrieved_value != test_value:
            logger.error(f"Test value mismatch: expected {test_value}, got {retrieved_value}")
            return False
        
        # Test manager access
        background_manager = settings_service.get_background_manager()
        if not background_manager:
            logger.error("Background manager not accessible from settings service")
            return False
        
        # Clean up test data
        settings_service.settings.remove(f"{test_section}/{test_key}")
        settings_service.settings.sync()
        
        logger.debug("✅ Basic functionality test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Basic functionality test failed: {e}")
        return False


def create_configured_settings_container(organization_name: str = "TKA", 
                                        application_name: str = "KineticConstructor") -> DIContainer:
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
        from desktop.modern.application.services.core.session_state_tracker import SessionStateTracker
        from desktop.modern.infrastructure.file_system.file_system_service import FileSystemService
        from desktop.modern.core.interfaces.core_services import IUIStateManager
        
        # Register file system service
        container.register_singleton(FileSystemService, FileSystemService)
        
        # Create mock UI state manager for isolated testing
        class MockUIStateManager(IUIStateManager):
            def __init__(self):
                self._state = {}
            
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
        
        # Register session tracker
        container.register_singleton(ISessionStateTracker, SessionStateTracker)
        
        # Register all settings services
        register_settings_services(container)
        
        # Validate registration
        if not validate_settings_registration(container):
            raise Exception("Settings service validation failed")
        
        logger.info(f"✅ Created configured settings container for {organization_name}/{application_name}")
        return container
        
    except Exception as e:
        logger.error(f"❌ Failed to create configured settings container: {e}")
        raise
