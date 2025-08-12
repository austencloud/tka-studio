from __future__ import annotations
from typing import Any, TypeVar, cast

from interfaces.json_manager_interface import IJsonManager
from interfaces.settings_manager_interface import ISettingsManager

T = TypeVar("T")


class AppContextDI:
    """Transitional AppContext implementation that uses dependency injection."""

    _instance = None
    _services: dict[type, Any] = {}

    @classmethod
    def init(cls, **services):
        """Initialize the context with services."""
        cls._services = services
        cls._instance = cls()

    @classmethod
    def get_service(cls, service_type: type[T]) -> T:
        """Get a service by type."""
        if service_type in cls._services:
            return cast(T, cls._services[service_type])
        raise KeyError(f"Service {service_type} not registered")

    @classmethod
    def settings_manager(cls) -> ISettingsManager:
        """Get the settings manager."""
        return cls.get_service(ISettingsManager)

    @classmethod
    def json_manager(cls) -> IJsonManager:
        """Get the JSON manager."""
        return cls.get_service(IJsonManager)

    # Add other service getters as needed
