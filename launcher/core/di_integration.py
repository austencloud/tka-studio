"""
Dependency Injection Integration for TKA Launcher.

Integrates launcher services with TKA's DI container following
clean architecture patterns and service registration conventions.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional, TYPE_CHECKING, Any

# CRITICAL: Set up TKA path IMMEDIATELY to handle VS Code debugger
# The debugger changes import resolution, so we must fix paths first
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent  # launcher -> TKA
modern_src = project_root / "src" / "desktop" / "modern" / "src"

if modern_src.exists() and str(modern_src) not in sys.path:
    sys.path.insert(0, str(modern_src))

from desktop.modern.core.interfaces import (
    IApplicationLaunchService,
    IApplicationService,
    ILauncherStateService,
    IScreenService,
)

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

# Import TKA's DI container (now that path is set up)
try:
    # Try to import TKA DI directly (path should be available now)
    from desktop.modern.core.dependency_injection.di_container import (
        DIContainer,
        get_container,
    )
    TKA_DI_AVAILABLE = True
except ImportError:
    # Fallback for standalone launcher operation
    TKA_DI_AVAILABLE = False
    DIContainer = None
    get_container = None


from desktop.modern.core.interfaces import ISettingsService
from services.launcher_state_service import LauncherStateService
from services.application_service import ApplicationService
from services.settings_service import SettingsService
from services.screen_service import ScreenService
from services.application_launch_service import ApplicationLaunchService

logger = logging.getLogger(__name__)


class LauncherDIContainer:
    """
    Launcher-specific DI container that integrates with TKA's main container.

    Provides service registration and resolution for launcher components
    while maintaining compatibility with TKA's architecture.
    """

    def __init__(self, use_tka_container: bool = True):
        """Initialize the launcher DI container."""
        self._use_tka_container = use_tka_container and TKA_DI_AVAILABLE
        self._container: Optional["DIContainer"] = None
        self._services = {}
        self._singletons = {}

        if self._use_tka_container:
            try:
                self._container = get_container()
            except Exception as e:
                logger.warning(f"Failed to get TKA container, using standalone: {e}")
                self._use_tka_container = False

        # Register launcher services
        self._register_launcher_services()

    def register_singleton(self, interface, implementation):
        """Register a service as singleton."""
        if self._use_tka_container and self._container:
            try:
                self._container.register_singleton(interface, implementation)
                logger.debug(f"Registered in TKA container: {interface.__name__}")
            except Exception as e:
                logger.error(f"Failed to register in TKA container: {e}")
                self._services[interface] = implementation
        else:
            self._services[interface] = implementation
            logger.debug(f"Registered in launcher container: {interface.__name__}")

    def register_instance(self, interface, instance):
        """Register a specific instance."""
        if self._use_tka_container and self._container:
            try:
                self._container.register_instance(interface, instance)
                logger.debug(
                    f"Registered instance in TKA container: {interface.__name__}"
                )
            except Exception as e:
                logger.error(f"Failed to register instance in TKA container: {e}")
                self._singletons[interface] = instance
        else:
            self._singletons[interface] = instance
            logger.debug(
                f"Registered instance in launcher container: {interface.__name__}"
            )

    def register_factory(self, interface, factory_func):
        """Register a factory function."""
        if self._use_tka_container and self._container:
            try:
                self._container.register_factory(interface, factory_func)
                logger.debug(
                    f"Registered factory in TKA container: {interface.__name__}"
                )
            except Exception as e:
                logger.error(f"Failed to register factory in TKA container: {e}")
                self._services[interface] = factory_func
        else:
            self._services[interface] = factory_func
            logger.debug(
                f"Registered factory in launcher container: {interface.__name__}"
            )

    def resolve(self, interface):
        """Resolve a service instance."""
        if self._use_tka_container and self._container:
            try:
                return self._container.resolve(interface)
            except Exception as e:
                logger.warning(f"Failed to resolve from TKA container: {e}")
                # Fall back to local resolution

        # Local resolution
        if interface in self._singletons:
            return self._singletons[interface]

        if interface in self._services:
            service_or_factory = self._services[interface]

            # If it's a callable factory
            if callable(service_or_factory) and not hasattr(
                service_or_factory, "__name__"
            ):
                instance = service_or_factory()
            else:
                # It's a class, create instance
                instance = self._create_instance(service_or_factory)

            # Store as singleton
            self._singletons[interface] = instance
            return instance

        raise ValueError(f"Service {interface.__name__} is not registered")

    def _create_instance(self, implementation_class):
        """Create instance with basic dependency injection."""
        try:
            # Try to create with no arguments first
            return implementation_class()
        except TypeError:
            # Try to inject dependencies
            import inspect

            signature = inspect.signature(implementation_class.__init__)
            kwargs = {}

            for param_name, param in signature.parameters.items():
                if param_name == "self":
                    continue

                param_type = param.annotation
                if param_type != inspect.Parameter.empty:
                    try:
                        dependency = self.resolve(param_type)
                        kwargs[param_name] = dependency
                    except ValueError:
                        # Optional dependency
                        if param.default != inspect.Parameter.empty:
                            kwargs[param_name] = param.default
                        else:
                            kwargs[param_name] = None

            return implementation_class(**kwargs)

    def _register_launcher_services(self):
        """Register all launcher services."""
        # Register settings service first (no dependencies)
        self.register_singleton(ISettingsService, SettingsService)

        # Register state service as singleton (depends on settings)
        def create_state_service():
            settings_service = self.resolve(ISettingsService)
            return LauncherStateService(settings_service)

        self.register_factory(ILauncherStateService, create_state_service)

        # Register application service as singleton (depends on state)
        def create_application_service():
            state_service = self.resolve(ILauncherStateService)
            return ApplicationService(state_service)

        self.register_factory(IApplicationService, create_application_service)

        # Register screen service (no dependencies)
        self.register_singleton(IScreenService, ScreenService)

        # Register application launch service as singleton (depends on state)
        def create_launch_service():
            state_service = self.resolve(ILauncherStateService)
            return ApplicationLaunchService(state_service)

        self.register_factory(IApplicationLaunchService, create_launch_service)

        logger.info("")

    def get_settings_service(self) -> ISettingsService:
        """Get the settings service."""
        return self.resolve(ISettingsService)

    def get_state_service(self) -> ILauncherStateService:
        """Get the launcher state service."""
        return self.resolve(ILauncherStateService)

    def get_application_service(self) -> IApplicationService:
        """Get the application service."""
        return self.resolve(IApplicationService)

    def get_screen_service(self) -> IScreenService:
        """Get the screen service."""
        return self.resolve(IScreenService)

    def get_launch_service(self) -> IApplicationLaunchService:
        """Get the application launch service."""
        return self.resolve(IApplicationLaunchService)

    def cleanup(self):
        """Cleanup resources."""
        # Persist state before cleanup
        try:
            state_service = self.resolve(ILauncherStateService)
            state_service.persist_state()
            logger.info("Launcher state persisted during cleanup")
        except Exception as e:
            logger.error(f"Failed to persist state during cleanup: {e}")

        # Clear local containers
        self._services.clear()
        self._singletons.clear()

        logger.info("Launcher DI container cleaned up")


# Global launcher container instance
_launcher_container: Optional[LauncherDIContainer] = None


def get_launcher_container(use_tka_container: bool = True) -> LauncherDIContainer:
    """Get the global launcher DI container."""
    global _launcher_container

    if _launcher_container is None:
        _launcher_container = LauncherDIContainer(use_tka_container)

    return _launcher_container


def reset_launcher_container():
    """Reset the global launcher container (for testing)."""
    global _launcher_container

    if _launcher_container:
        _launcher_container.cleanup()

    _launcher_container = None


def configure_launcher_services(
    container: Optional[LauncherDIContainer] = None,
) -> LauncherDIContainer:
    """Configure launcher services in the DI container."""
    if container is None:
        container = get_launcher_container()

    # Services are already registered in the constructor
    # This function can be used for additional configuration

    logger.info("Launcher services configured")
    return container
