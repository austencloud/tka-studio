"""
Service Registry - Centralized Service Registration Management

Handles all service registration operations including:
- Singleton registration
- Transient registration
- Factory registration
- Instance registration
- Scoped registration
- Lazy registration
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
import logging
from typing import Any, TypeVar


logger = logging.getLogger(__name__)

T = TypeVar("T")


class ServiceScope(Enum):
    """Service scope definitions for advanced DI features."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"
    REQUEST = "request"
    SESSION = "session"


@dataclass
class ServiceDescriptor:
    """Enhanced service descriptor with scope and caching support."""

    interface: type
    implementation: type
    scope: ServiceScope = ServiceScope.SINGLETON
    factory: Callable | None = None
    lazy: bool = False


class ServiceRegistry:
    """
    Centralized service registration management.

    Handles all types of service registrations and maintains the service mappings
    used by the DI container for resolution.
    """

    def __init__(self):
        # Core service storage
        self.services: dict[type, type] = {}  # Singleton services
        self.singletons: dict[type, Any] = {}  # Singleton instances
        self._factories: dict[type, type] = {}  # Transient/factory services

        # Advanced features
        self._service_descriptors: dict[type, ServiceDescriptor] = {}
        self._scoped_instances: dict[str, dict[type, Any]] = {}
        self._current_scope: str | None = None

    def register_singleton(self, interface: type[T], implementation: type[T]) -> None:
        """Register a service as singleton (one instance per container)."""
        self.services[interface] = implementation
        logger.debug(
            f"Registered singleton: {interface.__name__} -> {implementation.__name__}"
        )

    def register_transient(self, interface: type[T], implementation: type[T]) -> None:
        """Register a service as transient (new instance each time)."""
        self._factories[interface] = implementation
        logger.debug(
            f"Registered transient: {interface.__name__} -> {implementation.__name__}"
        )

    def register_instance(self, interface: type[T], instance: T) -> None:
        """Register a specific instance."""
        self.singletons[interface] = instance
        logger.debug(f"Registered instance: {interface.__name__}")

    def register_factory(self, interface: type[T], factory_func: Callable) -> None:
        """Register a factory function for creating instances."""
        self._factories[interface] = factory_func
        logger.debug(f"Registered factory: {interface.__name__}")

    def register_scoped(
        self, interface: type[T], implementation: type[T], scope: ServiceScope
    ) -> None:
        """Register a service with specific scope (singleton, transient, request, session)."""
        descriptor = ServiceDescriptor(
            interface=interface, implementation=implementation, scope=scope
        )
        self._service_descriptors[interface] = descriptor

        # Also register in appropriate legacy collection for compatibility
        if scope == ServiceScope.SINGLETON:
            self.services[interface] = implementation
        else:
            self._factories[interface] = implementation

        logger.debug(
            f"Registered {scope.value}: {interface.__name__} -> {implementation.__name__}"
        )

    def register_lazy(self, interface: type[T], implementation: type[T]) -> None:
        """Register a service for lazy loading."""
        descriptor = ServiceDescriptor(
            interface=interface,
            implementation=implementation,
            scope=ServiceScope.SINGLETON,
            lazy=True,
        )
        self._service_descriptors[interface] = descriptor
        logger.debug(
            f"Registered lazy: {interface.__name__} -> {implementation.__name__}"
        )

    def is_registered(self, interface: type) -> bool:
        """Check if a service is registered."""
        return (
            interface in self.services
            or interface in self._factories
            or interface in self.singletons
        )

    def get_service_implementation(self, interface: type) -> type | None:
        """Get the implementation type for a service interface."""
        if interface in self.services:
            return self.services[interface]
        if interface in self._factories:
            return self._factories[interface]
        return None

    def get_singleton_instance(self, interface: type) -> Any | None:
        """Get existing singleton instance if available."""
        return self.singletons.get(interface)

    def set_singleton_instance(self, interface: type, instance: Any) -> None:
        """Store a singleton instance."""
        self.singletons[interface] = instance

    def has_singleton_instance(self, interface: type) -> bool:
        """Check if singleton instance exists."""
        return interface in self.singletons

    def has_factory_registration(self, interface: type) -> bool:
        """Check if service has factory registration."""
        return interface in self._factories

    def has_service_registration(self, interface: type) -> bool:
        """Check if service has singleton registration."""
        return interface in self.services

    def get_factory_or_implementation(self, interface: type) -> Any | None:
        """Get factory function or implementation class."""
        return self._factories.get(interface)

    def get_all_registrations(self) -> dict[type, type]:
        """Get all registered services for debugging."""
        registrations = {}

        # Add singleton instances
        for interface in self.singletons:
            registrations[interface] = type(self.singletons[interface])

        # Add service registrations
        registrations.update(self.services)

        # Add factory registrations
        registrations.update(self._factories)

        return registrations

    def get_service_descriptor(self, interface: type) -> ServiceDescriptor | None:
        """Get service descriptor for advanced features."""
        return self._service_descriptors.get(interface)

    def clear_all(self) -> None:
        """Clear all registrations (useful for testing)."""
        self.services.clear()
        self.singletons.clear()
        self._factories.clear()
        self._service_descriptors.clear()
        self._scoped_instances.clear()
        self._current_scope = None
        logger.debug("All service registrations cleared")

    def get_registration_count(self) -> int:
        """Get total number of registrations."""
        return len(self.services) + len(self._factories) + len(self.singletons)
