#!/usr/bin/env python3
"""
Dependency Injection Container
==============================

Simple dependency injection container for TKA application.
Provides service registration and resolution with lifecycle management.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, TypeVar


logger = logging.getLogger(__name__)

T = TypeVar("T")


class DIContainer:
    """
    Simple dependency injection container.

    Supports singleton and transient service registration with automatic
    dependency resolution.
    """

    def __init__(self):
        """Initialize the DI container."""
        self._services: dict[str, Any] = {}
        self._factories: dict[str, Callable] = {}
        self._singletons: dict[str, Any] = {}

        logger.debug("DIContainer initialized")

    def register_singleton(
        self, interface: str | type, implementation: type | Any
    ) -> None:
        """
        Register a singleton service.

        Args:
            interface: Service interface (string key or type)
            implementation: Service implementation (class or instance)
        """
        key = self._get_key(interface)

        if isinstance(implementation, type):
            # Store class for lazy instantiation
            self._factories[key] = implementation
        else:
            # Store instance directly
            self._singletons[key] = implementation

        logger.debug(f"Registered singleton: {key}")

    def register_transient(self, interface: str | type, implementation: type) -> None:
        """
        Register a transient service (new instance each time).

        Args:
            interface: Service interface (string key or type)
            implementation: Service implementation class
        """
        key = self._get_key(interface)
        self._services[key] = implementation
        logger.debug(f"Registered transient: {key}")

    def register_instance(self, interface: str | type, instance: Any) -> None:
        """
        Register a specific instance.

        Args:
            interface: Service interface (string key or type)
            instance: Service instance to register
        """
        key = self._get_key(interface)
        self._singletons[key] = instance
        logger.debug(f"Registered instance: {key}")

    def register_factory(self, interface: str | type, factory: callable) -> None:
        """
        Register a factory function for creating service instances.

        Args:
            interface: Service interface (string key or type)
            factory: Factory function that creates service instances
        """
        key = self._get_key(interface)
        self._factories[key] = factory
        logger.debug(f"Registered factory: {key}")

    def resolve(self, interface: str | type) -> Any:
        """
        Resolve a service instance.

        Args:
            interface: Service interface to resolve

        Returns:
            Service instance

        Raises:
            KeyError: If service is not registered
        """
        key = self._get_key(interface)

        # Check singletons first
        if key in self._singletons:
            return self._singletons[key]

        # Check singleton factories
        if key in self._factories:
            instance = self._factories[key]()
            self._singletons[key] = instance
            return instance

        # Check transient services
        if key in self._services:
            return self._services[key]()

        raise KeyError(f"Service not registered: {key}")

    def is_registered(self, interface: str | type) -> bool:
        """Check if a service is registered."""
        key = self._get_key(interface)
        return (
            key in self._services or key in self._factories or key in self._singletons
        )

    def clear(self) -> None:
        """Clear all registered services."""
        self._services.clear()
        self._factories.clear()
        self._singletons.clear()
        logger.debug("DIContainer cleared")

    def _get_key(self, interface: str | type) -> str:
        """Get string key for interface."""
        if isinstance(interface, str):
            return interface
        if hasattr(interface, "__name__"):
            return interface.__name__
        return str(interface)

    def __contains__(self, interface: str | type) -> bool:
        """Check if service is registered using 'in' operator."""
        return self.is_registered(interface)
