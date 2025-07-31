"""
Enhanced dependency injection container for Kinetic Constructor.

This is the main container that coordinates all DI operations using focused modules.
The container has been refactored into specialized components for better maintainability.
"""

import logging
from typing import Any, Optional, TypeVar

from .debugging_tools import DebuggingTools
from .lifecycle_manager import LifecycleManager

# Import refactored modules
from .service_registry import ServiceRegistry, ServiceScope
from .service_resolvers import LazyProxy, ResolverChain
from .validation_engine import ValidationEngine

try:
    from ..exceptions import DependencyInjectionError, di_error
except ImportError:
    # Fallback for tests
    class DependencyInjectionError(Exception):
        def __init__(
            self,
            message: str,
            interface_name: str | None = None,
            dependency_chain: list | None = None,
            context: dict[str, Any] | None = None,
        ):
            super().__init__(message)
            self.interface_name = interface_name
            self.dependency_chain = dependency_chain or []

    def di_error(
        message: str, interface_name: str, **context
    ) -> DependencyInjectionError:
        return DependencyInjectionError(message, interface_name)


T = TypeVar("T")
logger = logging.getLogger(__name__)

# Global container instance
_container: Optional["DIContainer"] = None
_container_initialized: bool = False


class DIContainer:
    """
    Enhanced dependency injection container with automatic constructor injection.

    Uses focused modules for better maintainability:
    - ServiceRegistry: Handles all service registrations
    - ResolverChain: Manages service resolution strategies
    - LifecycleManager: Handles service lifecycle and cleanup
    - ValidationEngine: Provides comprehensive validation
    - DebuggingTools: Offers debugging and analysis capabilities

    Features:
    - Singleton and transient service lifetimes
    - Automatic constructor injection with type resolution
    - Protocol compliance validation
    - Circular dependency detection
    - Type safety validation
    - Service lifecycle management
    - Enhanced error reporting
    - Comprehensive debugging tools
    """

    def __init__(self):
        # Initialize focused modules
        self._registry = ServiceRegistry()
        self._resolver_chain = ResolverChain()
        self._lifecycle_manager = LifecycleManager()
        self._validation_engine = ValidationEngine()
        self._debugging_tools = DebuggingTools()

        # Resolution state
        self._resolution_stack: set[type] = set()

    def register_singleton(self, interface: type[T], implementation: type[T]) -> None:
        """Register a service as singleton (one instance per container)."""
        self._validation_engine.validate_registration(interface, implementation)
        self._registry.register_singleton(interface, implementation)

    def register_transient(self, interface: type[T], implementation: type[T]) -> None:
        """Register a service as transient (new instance each time)."""
        self._validation_engine.validate_registration(interface, implementation)
        self._registry.register_transient(interface, implementation)

    def register_instance(self, interface: type[T], instance: T) -> None:
        """Register a specific instance."""
        self._registry.register_instance(interface, instance)

    def register_factory(self, interface: type[T], factory_func: callable) -> None:
        """Register a factory function for creating instances."""
        self._registry.register_factory(interface, factory_func)

    def auto_register(self, interface: type[T], implementation: type[T]) -> None:
        """Register with automatic Protocol validation."""
        self._validation_engine.validate_protocol_implementation(
            interface, implementation
        )
        self.register_singleton(interface, implementation)

    # ============================================================================
    # ADVANCED DI FEATURES - Delegated to Specialized Modules
    # ============================================================================

    def register_scoped(
        self, interface: type[T], implementation: type[T], scope: ServiceScope
    ) -> None:
        """Register a service with specific scope (singleton, transient, request, session)."""
        self._validation_engine.validate_registration(interface, implementation)
        self._registry.register_scoped(interface, implementation, scope)

    def register_lazy(self, interface: type[T], implementation: type[T]) -> None:
        """Register a service for lazy loading."""
        self._validation_engine.validate_registration(interface, implementation)
        self._registry.register_lazy(interface, implementation)

    def create_scope(self, scope_id: str) -> None:
        """Create a new scope for scoped services."""
        self._lifecycle_manager.create_scope(scope_id)

    def dispose_scope(self, scope_id: str) -> None:
        """Dispose a scope and cleanup its instances."""
        self._lifecycle_manager.dispose_scope(scope_id)

    def resolve_lazy(self, interface: type[T]) -> LazyProxy:
        """Resolve a service as a lazy proxy."""
        return LazyProxy(interface, self)

    def clear_cache(self) -> None:
        """Clear the resolution cache."""
        # Note: Cache clearing is now handled by individual modules
        self._validation_engine.clear_validation_cache()
        self._debugging_tools.clear_history()
        logger.debug("All caches cleared")

    def resolve(self, interface: type[T]) -> T:
        """
        Resolve a service instance using refactored resolver chain.

        Uses specialized modules for clean separation of concerns.

        Args:
            interface: The interface/type to resolve

        Returns:
            An instance of the requested type

        Raises:
            DependencyInjectionError: If the service is not registered or circular dependency detected
        """
        import time

        start_time = time.time()

        # Check for circular dependencies
        if interface in self._resolution_stack:
            dependency_chain = list(self._resolution_stack) + [interface]
            chain_names = [dep.__name__ for dep in dependency_chain]
            raise DependencyInjectionError(
                f"Circular dependency detected: {' -> '.join(chain_names)}",
                interface_name=interface.__name__,
                dependency_chain=chain_names,
            )

        self._resolution_stack.add(interface)
        try:
            # Use resolver chain to attempt resolution
            instance = self._resolver_chain.resolve(interface, self._registry, self)

            if instance is not None:
                # Apply lifecycle management
                instance = self._lifecycle_manager.create_with_lifecycle(instance)

                # Record successful resolution
                resolution_time = time.time() - start_time
                self._debugging_tools.record_resolution(
                    interface, resolution_time, True
                )

                return instance

            # Service not registered - provide helpful error message
            all_registrations = self._registry.get_all_registrations()
            available_names = [svc.__name__ for svc in all_registrations.keys()]

            # Record failed resolution
            resolution_time = time.time() - start_time
            self._debugging_tools.record_resolution(interface, resolution_time, False)

            raise ValueError(
                f"Service {interface.__name__} is not registered. Available services: {available_names}"
            )
        except DependencyInjectionError:
            raise
        except Exception as e:
            # Record failed resolution
            resolution_time = time.time() - start_time
            self._debugging_tools.record_resolution(interface, resolution_time, False)

            raise DependencyInjectionError(
                f"Failed to resolve {interface.__name__}: {e}",
                interface_name=interface.__name__,
            ) from e
        finally:
            self._resolution_stack.discard(interface)

    # ============================================================================
    # LIFECYCLE MANAGEMENT - Delegated to LifecycleManager
    # ============================================================================

    def cleanup_all(self) -> None:
        """Cleanup all registered services."""
        self._lifecycle_manager.cleanup_all()

    # ============================================================================
    # VALIDATION - Delegated to ValidationEngine
    # ============================================================================

    def auto_register_with_validation(
        self, interface: type[T], implementation: type[T]
    ) -> None:
        """Register service with comprehensive validation."""
        self._validation_engine.auto_register_with_validation(
            interface, implementation, self._registry
        )

    def validate_all_registrations(self) -> None:
        """Validate all service registrations can be resolved."""
        self._validation_engine.validate_all_registrations(self._registry)

    def get_registrations(self) -> dict[type, type]:
        """Get all registered services for testing/debugging."""
        return self._registry.get_all_registrations()

    # ============================================================================
    # DEBUGGING - Delegated to DebuggingTools
    # ============================================================================

    def get_dependency_graph(self) -> dict[str, Any]:
        """Generate dependency graph for debugging."""
        return self._debugging_tools.get_dependency_graph(self._registry)

    def get_performance_metrics(self) -> dict[str, Any]:
        """Get performance metrics for service resolution."""
        return self._debugging_tools.get_performance_metrics()

    def generate_diagnostic_report(self) -> str:
        """Generate a comprehensive diagnostic report."""
        return self._debugging_tools.generate_diagnostic_report(
            self._registry, self._lifecycle_manager
        )

    # ============================================================================
    # BACKWARD COMPATIBILITY - Legacy method support
    # ============================================================================

    def _is_primitive_type(self, param_type: type) -> bool:
        """Check if a type is a primitive type (delegated to validation engine)."""
        return self._validation_engine.is_primitive_type(param_type)

    @property
    def _singletons(self) -> dict[type, Any]:
        """Backward compatibility property for accessing singleton instances."""
        # Delegate to service registry
        return self._registry.singletons

    @property
    def _services(self) -> dict[type, Any]:
        """Backward compatibility property for accessing service registrations."""
        # Delegate to service registry
        return self._registry.services

    @property
    def _cleanup_handlers(self) -> list[Any]:
        """Backward compatibility property for accessing cleanup handlers."""
        # Delegate to lifecycle manager
        return self._lifecycle_manager.cleanup_handlers


def get_container() -> DIContainer:
    """Get the global container instance."""
    global _container, _container_initialized
    if _container is None:
        # Only create a new container if one hasn't been explicitly set
        if not _container_initialized:
            logger.warning(
                f"🚨 [DI_CONTAINER] Creating new container instance (ID will be {id(DIContainer())}). "
                "This should only happen once during application startup!"
            )
            _container = DIContainer()
            _container_initialized = True
        else:
            # This should never happen - container was set but then became None
            raise RuntimeError(
                "Global DI container was unexpectedly reset after initialization"
            )
    return _container


def set_container(container: DIContainer, force: bool = False) -> None:
    """Set the global container instance with improved safety."""
    global _container, _container_initialized

    # Validate input
    if container is None:
        raise ValueError("Cannot set container to None. Use reset_container() instead.")

    # Prevent overwriting an existing container unless forced
    if _container is not None and not force:
        error_msg = (
            f"Attempted to overwrite existing container {id(_container)} "
            f"with new container {id(container)}. Use force=True to override."
        )
        logger.error(f"🚨 [DI_CONTAINER] {error_msg}")
        # CRITICAL FIX: Raise exception instead of silent failure
        raise RuntimeError(error_msg)

    # Container replacement/initialization (logging removed for cleaner startup)

    _container = container
    _container_initialized = True

    # Initialize the service locator with the new container
    try:
        from desktop.modern.core.service_locator import initialize_service_locator

        initialize_service_locator(container)
    except ImportError as e:
        logger.warning(f"Could not initialize service locator: {e}")


def reset_container() -> None:
    """Reset the global container (useful for testing)."""
    global _container, _container_initialized

    # Clean up the service locator
    try:
        from desktop.modern.core.service_locator import cleanup

        cleanup()
    except ImportError:
        pass  # Service locator not available, that's fine

    _container = None
    _container_initialized = False


# Backward compatibility alias
DIContainer = DIContainer
