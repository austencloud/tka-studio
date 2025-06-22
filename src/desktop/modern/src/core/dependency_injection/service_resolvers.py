"""
Service Resolvers - Strategy Pattern Implementation for Service Resolution

Contains all resolver implementations using the Strategy Pattern:
- SingletonResolver: Handles existing singleton instances
- ConstructorResolver: Handles constructor injection for new instances
- FactoryResolver: Handles factory-based service creation
"""

from typing import Type, Any, Dict, get_type_hints, Set
from abc import ABC, abstractmethod
import inspect
import logging

logger = logging.getLogger(__name__)


class IServiceResolver(ABC):
    """Abstract base class for service resolvers using Strategy Pattern."""

    @abstractmethod
    def can_resolve(self, service_type: Type, registry: Any) -> bool:
        """Check if this resolver can handle the given service type."""
        pass

    @abstractmethod
    def resolve(self, service_type: Type, registry: Any, container: Any) -> Any:
        """Resolve the service instance."""
        pass


class SingletonResolver(IServiceResolver):
    """Resolver for singleton instances."""

    def can_resolve(self, service_type: Type, registry: Any) -> bool:
        """Check if singleton instance exists."""
        return registry.has_singleton_instance(service_type)

    def resolve(self, service_type: Type, registry: Any, container: Any) -> Any:
        """Return existing singleton instance."""
        return registry.get_singleton_instance(service_type)


class ConstructorResolver(IServiceResolver):
    """Resolver for constructor-based dependency injection."""

    def can_resolve(self, service_type: Type, registry: Any) -> bool:
        """Check if service is registered for constructor injection."""
        return registry.has_service_registration(service_type)

    def resolve(self, service_type: Type, registry: Any, container: Any) -> Any:
        """Resolve singleton service with constructor injection."""
        implementation = registry.get_service_implementation(service_type)
        instance = self._create_with_constructor_injection(implementation, container)
        registry.set_singleton_instance(service_type, instance)
        return instance

    def _create_with_constructor_injection(
        self, implementation_class: Type, container: Any
    ) -> Any:
        """Create instance with constructor injection - simplified and focused."""
        signature = inspect.signature(implementation_class.__init__)
        type_hints = get_type_hints(implementation_class.__init__)
        dependencies = {}

        for param_name, param in signature.parameters.items():
            if param_name == "self":
                continue

            # Skip parameters with default values
            if param.default != inspect.Parameter.empty:
                continue

            param_type = type_hints.get(param_name, param.annotation)

            # Skip if no type annotation or primitive type
            if (
                not param_type
                or param_type == inspect.Parameter.empty
                or self._is_primitive_type(param_type)
            ):
                continue

            # Resolve dependency
            dependencies[param_name] = container.resolve(param_type)

        return implementation_class(**dependencies)

    def _is_primitive_type(self, param_type: Type) -> bool:
        """Check if a type is a primitive type that should not be resolved as a dependency."""
        from pathlib import Path
        from datetime import datetime, timedelta
        from typing import Union

        primitive_types = {
            str,
            int,
            float,
            bool,
            bytes,
            type(None),
            list,
            dict,
            tuple,
            set,
            frozenset,
            Path,
            datetime,
            timedelta,
        }

        # Handle Union types (like Optional[str] which is Union[str, None])
        if hasattr(param_type, "__origin__"):
            origin = param_type.__origin__
            if origin is Union:
                # Check if it's Optional[T] (Union[T, None])
                args = getattr(param_type, "__args__", ())
                if len(args) == 2 and type(None) in args:
                    # It's Optional[T], check the non-None type
                    non_none_type = next(arg for arg in args if arg is not type(None))
                    return self._is_primitive_type(non_none_type)
                # For other Union types, check if all args are primitive
                return all(arg in primitive_types for arg in args)
            # Other generic types like List[str], Dict[str, int] are considered primitive
            if origin in primitive_types:
                return True

        # Check if it's a builtin type
        if hasattr(param_type, "__module__") and param_type.__module__ == "builtins":
            return True

        return param_type in primitive_types


class FactoryResolver(IServiceResolver):
    """Resolver for factory-based service creation."""

    def can_resolve(self, service_type: Type, registry: Any) -> bool:
        """Check if service has a factory registration."""
        return registry.has_factory_registration(service_type)

    def resolve(self, service_type: Type, registry: Any, container: Any) -> Any:
        """Resolve service using factory or transient creation."""
        factory_or_implementation = registry.get_factory_or_implementation(service_type)

        # Check if it's a callable factory function
        if callable(factory_or_implementation) and not inspect.isclass(
            factory_or_implementation
        ):
            return factory_or_implementation()
        else:
            # It's a class, create with constructor injection
            constructor_resolver = ConstructorResolver()
            return constructor_resolver._create_with_constructor_injection(
                factory_or_implementation, container
            )


class LazyProxy:
    """Lazy loading proxy for expensive dependencies."""

    def __init__(self, service_type: Type, container: Any):
        self._service_type = service_type
        self._container = container
        self._instance = None
        self._resolved = False

    def __getattr__(self, name):
        if not self._resolved:
            self._instance = self._container.resolve(self._service_type)
            self._resolved = True
        return getattr(self._instance, name)

    def __call__(self, *args, **kwargs):
        if not self._resolved:
            self._instance = self._container.resolve(self._service_type)
            self._resolved = True
        return self._instance(*args, **kwargs)


class ResolverChain:
    """
    Manages the chain of resolvers using Strategy Pattern.

    Provides a clean interface for adding resolvers and attempting resolution
    through the chain until one succeeds.
    """

    def __init__(self):
        self._resolvers = [
            SingletonResolver(),
            ConstructorResolver(),
            FactoryResolver(),
        ]

    def add_resolver(self, resolver: IServiceResolver) -> None:
        """Add a custom resolver to the chain."""
        self._resolvers.append(resolver)

    def resolve(self, service_type: Type, registry: Any, container: Any) -> Any:
        """Attempt resolution through the resolver chain."""
        for resolver in self._resolvers:
            if resolver.can_resolve(service_type, registry):
                return resolver.resolve(service_type, registry, container)

        # No resolver could handle this service type
        return None

    def can_resolve(self, service_type: Type, registry: Any) -> bool:
        """Check if any resolver in the chain can handle the service type."""
        return any(
            resolver.can_resolve(service_type, registry) for resolver in self._resolvers
        )

    def get_resolver_count(self) -> int:
        """Get the number of resolvers in the chain."""
        return len(self._resolvers)
