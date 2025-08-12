"""
Lifecycle Manager - Service Lifecycle and Cleanup Management

Handles:
- Service initialization
- Service cleanup and disposal
- Scoped instance management
- Lifecycle event coordination
"""

from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any


logger = logging.getLogger(__name__)


class LifecycleManager:
    """
    Manages service lifecycle including initialization, cleanup, and scoped instances.

    Provides centralized lifecycle management for all services in the DI container,
    ensuring proper initialization and cleanup of resources.
    """

    def __init__(self):
        self.cleanup_handlers: list[Callable] = []
        self._scoped_instances: dict[str, dict[type, Any]] = {}
        self._current_scope: str | None = None
        self._initialized_services: list[Any] = []

    def create_with_lifecycle(self, instance: Any) -> Any:
        """Create instance with proper lifecycle management."""
        # Call initialization method if it exists
        if hasattr(instance, "initialize") and callable(instance.initialize):
            try:
                instance.initialize()
                self._initialized_services.append(instance)
                logger.debug(f"Initialized service: {type(instance).__name__}")
            except Exception as e:
                logger.error(
                    f"Failed to initialize service {type(instance).__name__}: {e}"
                )
                raise

        # Register for cleanup if it has cleanup method
        if hasattr(instance, "cleanup") and callable(instance.cleanup):
            self.cleanup_handlers.append(instance.cleanup)
            logger.debug(f"Registered cleanup for service: {type(instance).__name__}")

        return instance

    def cleanup_all(self) -> None:
        """Cleanup all registered services."""
        logger.info(f"Starting cleanup of {len(self.cleanup_handlers)} services")

        for cleanup_handler in reversed(self.cleanup_handlers):
            try:
                cleanup_handler()
                logger.debug("Service cleanup completed successfully")
            except Exception as e:
                logger.error(f"Error during service cleanup: {e}")

        self.cleanup_handlers.clear()
        self._initialized_services.clear()
        logger.info("All services cleaned up")

    def create_scope(self, scope_id: str) -> None:
        """Create a new scope for scoped services."""
        if scope_id in self._scoped_instances:
            logger.warning(f"Scope {scope_id} already exists, overwriting")

        self._scoped_instances[scope_id] = {}
        self._current_scope = scope_id
        logger.debug(f"Created scope: {scope_id}")

    def dispose_scope(self, scope_id: str) -> None:
        """Dispose a scope and cleanup its instances."""
        if scope_id not in self._scoped_instances:
            logger.warning(f"Scope {scope_id} does not exist")
            return

        scope_instances = self._scoped_instances[scope_id]
        logger.debug(
            f"Disposing scope {scope_id} with {len(scope_instances)} instances"
        )

        # Cleanup scoped instances
        for instance in scope_instances.values():
            if hasattr(instance, "cleanup") and callable(instance.cleanup):
                try:
                    instance.cleanup()
                    logger.debug(
                        f"Cleaned up scoped instance: {type(instance).__name__}"
                    )
                except Exception as e:
                    logger.error(f"Error cleaning up scoped instance: {e}")

        del self._scoped_instances[scope_id]
        if self._current_scope == scope_id:
            self._current_scope = None

        logger.debug(f"Disposed scope: {scope_id}")

    def get_scoped_instance(self, scope_id: str, service_type: type) -> Any | None:
        """Get an instance from a specific scope."""
        if scope_id not in self._scoped_instances:
            return None
        return self._scoped_instances[scope_id].get(service_type)

    def set_scoped_instance(
        self, scope_id: str, service_type: type, instance: Any
    ) -> None:
        """Store an instance in a specific scope."""
        if scope_id not in self._scoped_instances:
            self.create_scope(scope_id)

        self._scoped_instances[scope_id][service_type] = instance
        logger.debug(
            f"Stored scoped instance: {type(instance).__name__} in scope {scope_id}"
        )

    def get_current_scope(self) -> str | None:
        """Get the current active scope."""
        return self._current_scope

    def set_current_scope(self, scope_id: str | None) -> None:
        """Set the current active scope."""
        self._current_scope = scope_id
        logger.debug(f"Set current scope to: {scope_id}")

    def has_scope(self, scope_id: str) -> bool:
        """Check if a scope exists."""
        return scope_id in self._scoped_instances

    def get_scope_instance_count(self, scope_id: str) -> int:
        """Get the number of instances in a scope."""
        if scope_id not in self._scoped_instances:
            return 0
        return len(self._scoped_instances[scope_id])

    def get_total_scoped_instances(self) -> int:
        """Get total number of scoped instances across all scopes."""
        return sum(len(instances) for instances in self._scoped_instances.values())

    def get_active_scopes(self) -> list[str]:
        """Get list of all active scope IDs."""
        return list(self._scoped_instances.keys())

    def dispose_all_scopes(self) -> None:
        """Dispose all scopes and their instances."""
        scope_ids = list(self._scoped_instances.keys())
        for scope_id in scope_ids:
            self.dispose_scope(scope_id)

        self._current_scope = None
        logger.info("All scopes disposed")

    def get_cleanup_handler_count(self) -> int:
        """Get the number of registered cleanup handlers."""
        return len(self.cleanup_handlers)

    def get_initialized_service_count(self) -> int:
        """Get the number of initialized services."""
        return len(self._initialized_services)

    def force_cleanup_service(self, service_instance: Any) -> bool:
        """Force cleanup of a specific service instance."""
        if hasattr(service_instance, "cleanup") and callable(service_instance.cleanup):
            try:
                service_instance.cleanup()

                # Remove from cleanup handlers if present
                if service_instance.cleanup in self.cleanup_handlers:
                    self.cleanup_handlers.remove(service_instance.cleanup)

                # Remove from initialized services if present
                if service_instance in self._initialized_services:
                    self._initialized_services.remove(service_instance)

                logger.debug(
                    f"Force cleaned up service: {type(service_instance).__name__}"
                )
                return True
            except Exception as e:
                logger.error(
                    f"Error during force cleanup of {type(service_instance).__name__}: {e}"
                )
                return False

        logger.warning(
            f"Service {type(service_instance).__name__} has no cleanup method"
        )
        return False

    def get_lifecycle_stats(self) -> dict[str, Any]:
        """Get comprehensive lifecycle statistics."""
        return {
            "cleanup_handlers": len(self.cleanup_handlers),
            "initialized_services": len(self._initialized_services),
            "active_scopes": len(self._scoped_instances),
            "total_scoped_instances": self.get_total_scoped_instances(),
            "current_scope": self._current_scope,
            "scope_details": {
                scope_id: len(instances)
                for scope_id, instances in self._scoped_instances.items()
            },
        }
