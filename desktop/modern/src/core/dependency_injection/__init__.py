"""
Dependency Injection Module
===========================

Provides dependency injection container and related utilities.
"""

from __future__ import annotations

from .di_container import DIContainer


# Global container instance
_container: DIContainer | None = None


def get_container() -> DIContainer:
    """Get the global dependency container."""
    global _container
    if _container is None:
        _container = DIContainer()
    return _container


def set_container(container: DIContainer) -> None:
    """Set the global dependency container."""
    global _container
    _container = container


__all__ = ["DIContainer", "get_container", "set_container"]
