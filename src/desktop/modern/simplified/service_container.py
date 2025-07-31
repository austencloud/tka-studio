"""
Simple Service Container - Replaces complex DI system
Single responsibility: Hold and provide service instances
"""

import logging
from typing import Any, Dict, Optional, Type, TypeVar

logger = logging.getLogger(__name__)
T = TypeVar("T")


class ServiceContainer:
    """
    Simple service container - no fancy DI framework needed.

    Just stores instances and provides them when asked.
    Much simpler than the complex DIContainer system.
    """

    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._singletons: Dict[Type, Any] = {}
        self._instances: Dict[Type, Any] = {}

    def register_core_services(self):
        """Register all core services in simple, clear order"""

        try:
            # File system services
            from desktop.modern.core.interfaces.organization_services import (
                IFileSystemService,
            )
            from desktop.modern.infrastructure.file_system.file_system_service import (
                FileSystemService,
            )

            self.register(IFileSystemService, FileSystemService)

            # Settings services
            from desktop.modern.core.interfaces.core_services import (
                ISettingsCoordinator,
            )
            from desktop.modern.infrastructure.storage.file_based_settings_service import (
                FileBasedSettingsService,
            )

            self.register(ISettingsCoordinator, FileBasedSettingsService)

            # Sequence services
            from desktop.modern.core.interfaces.core_services import (
                ISequenceDataService,
            )
            from desktop.modern.infrastructure.storage.file_based_sequence_data_service import (
                FileBasedSequenceDataService,
            )

            self.register(ISequenceDataService, FileBasedSequenceDataService)

            # Layout services
            from desktop.modern.core.interfaces.core_services import ILayoutService
            from shared.application.services.layout.layout_manager import LayoutManager

            self.register(ILayoutService, LayoutManager)

            # Pictograph services
            from desktop.modern.core.interfaces.core_services import IPictographManager
            from shared.application.services.pictograph.pictograph_csv_manager import (
                PictographCSVManager,
            )

            self.register(IPictographManager, PictographCSVManager)

            # Sequence operations
            from desktop.modern.application.services.sequence.sequence_beat_operations import (
                SequenceBeatOperations,
            )
            from desktop.modern.core.interfaces.core_services import ISequenceManager

            self.register(ISequenceManager, SequenceBeatOperations)

            # UI services
            from desktop.modern.core.interfaces.core_services import IUIStateManager
            from shared.application.services.ui.coordination.ui_coordinator import (
                UICoordinator,
            )

            self.register(IUIStateManager, UICoordinator)

            # Session services
            from desktop.modern.application.services.core.session_state_tracker import (
                SessionStateTracker,
            )
            from desktop.modern.core.interfaces.session_services import (
                ISessionStateTracker,
            )

            self.register(ISessionStateTracker, SessionStateTracker)

            # Register additional services using the service registration manager
            from shared.application.services.core.service_registration_manager import (
                ServiceRegistrationManager,
            )

            service_manager = ServiceRegistrationManager()
            service_manager.register_all_services(self)

            logger.info("✅ Core services registered")

        except Exception as e:
            logger.error(f"❌ Failed to register some services: {e}")
            # Continue anyway - app should work with minimal services

    def register(
        self, interface: Type[T], implementation: Type[T] = None, instance: T = None
    ) -> None:
        """Register a service class or instance"""
        if instance:
            self._instances[interface] = instance
            self._singletons[interface] = instance
        elif implementation:
            self._services[interface] = implementation
        else:
            # If no implementation provided, assume interface is the implementation
            self._services[interface] = interface

    def register_singleton(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register as singleton - compatible with old DI system"""
        self.register(interface, implementation)

    def register_transient(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register as transient - compatible with old DI system"""
        self.register(interface, implementation)

    def register_instance(self, interface: Type[T], instance: T) -> None:
        """Register specific instance - compatible with old DI system"""
        self.register(interface, instance=instance)

    def resolve(self, service_class: Type[T]) -> T:
        """Get a service instance - compatible with old DI system"""
        return self.get(service_class)

    def get(self, service_class: Type[T]) -> T:
        """Get a service instance"""

        # Return existing singleton if available
        if service_class in self._singletons:
            return self._singletons[service_class]

        # Return existing instance if available
        if service_class in self._instances:
            return self._instances[service_class]

        # Check if registered
        if service_class not in self._services:
            # Try to find by name for backward compatibility
            for registered_interface, implementation in self._services.items():
                if (
                    hasattr(registered_interface, "__name__")
                    and hasattr(service_class, "__name__")
                    and registered_interface.__name__ == service_class.__name__
                ):
                    service_class = registered_interface
                    break
            else:
                raise ValueError(f"Service {service_class.__name__} not registered")

        service_def = self._services[service_class]

        # If it's already an instance, return it
        if not isinstance(service_def, type):
            return service_def

        # Create new instance
        try:
            instance = service_def()
            self._singletons[service_class] = instance  # Store as singleton
            return instance
        except Exception as e:
            logger.error(f"❌ Failed to create {service_class.__name__}: {e}")
            raise

    def get_registrations(self) -> Dict[Type, Any]:
        """Get all registered services for debugging - compatible with old DI system"""
        return self._services.copy()

    def get_all_services(self) -> Dict[Type, Any]:
        """Get all registered services for debugging"""
        return self._services.copy()


# Global container instance for backward compatibility
_container: Optional[ServiceContainer] = None


def get_container() -> ServiceContainer:
    """Get the global container instance - backward compatibility"""
    global _container
    if _container is None:
        _container = ServiceContainer()
        _container.register_core_services()
    return _container


def set_container(container: ServiceContainer, force: bool = False) -> None:
    """Set the global container instance - backward compatibility"""
    global _container
    _container = container


def reset_container() -> None:
    """Reset the global container - backward compatibility"""
    global _container
    _container = None
