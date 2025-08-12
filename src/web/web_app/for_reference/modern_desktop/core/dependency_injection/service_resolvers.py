"""
Service Resolvers - Strategy Pattern Implementation for Service Resolution

Contains all resolver implementations using the Strategy Pattern:
- SingletonResolver: Handles existing singleton instances
- ConstructorResolver: Handles constructor injection for new instances
- FactoryResolver: Handles factory-based service creation
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import inspect
import logging
from typing import Any, get_type_hints


logger = logging.getLogger(__name__)


class IServiceResolver(ABC):
    """Abstract base class for service resolvers using Strategy Pattern."""

    @abstractmethod
    def can_resolve(self, service_type: type, registry: Any) -> bool:
        """Check if this resolver can handle the given service type."""

    @abstractmethod
    def resolve(self, service_type: type, registry: Any, container: Any) -> Any:
        """Resolve the service instance."""


class SingletonResolver(IServiceResolver):
    """Resolver for singleton instances."""

    def can_resolve(self, service_type: type, registry: Any) -> bool:
        """Check if singleton instance exists."""
        return registry.has_singleton_instance(service_type)

    def resolve(self, service_type: type, registry: Any, container: Any) -> Any:
        """Return existing singleton instance."""
        return registry.get_singleton_instance(service_type)


class ConstructorResolver(IServiceResolver):
    """Resolver for constructor-based dependency injection with signature caching."""

    # Class-level caches for constructor signatures and type hints
    _signature_cache: dict[type, inspect.Signature] = {}
    _type_hints_cache: dict[type, dict[str, type]] = {}
    _cache_stats: dict[str, int] = {"hits": 0, "misses": 0, "total_cached": 0}

    def can_resolve(self, service_type: type, registry: Any) -> bool:
        """Check if service is registered for constructor injection."""
        return registry.has_service_registration(service_type)

    def resolve(self, service_type: type, registry: Any, container: Any) -> Any:
        """Resolve singleton service with constructor injection."""
        implementation = registry.get_service_implementation(service_type)
        instance = self._create_with_constructor_injection(implementation, container)
        registry.set_singleton_instance(service_type, instance)
        return instance

    def _create_with_constructor_injection(
        self, implementation_class: type, container: Any
    ) -> Any:
        """Create instance with constructor injection using cached signatures."""
        # Use cached signature and type hints for performance
        signature = self._get_cached_signature(implementation_class)
        type_hints = self._get_cached_type_hints(implementation_class)
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

    def _get_cached_signature(self, implementation_class: type) -> inspect.Signature:
        """Get cached constructor signature for the implementation class."""
        if implementation_class not in self._signature_cache:
            self._cache_stats["misses"] += 1
            logger.debug(f"Cache miss for signature: {implementation_class.__name__}")

            # Cache the signature
            self._signature_cache[implementation_class] = inspect.signature(
                implementation_class.__init__
            )
            self._cache_stats["total_cached"] = len(self._signature_cache)
        else:
            self._cache_stats["hits"] += 1
            logger.debug(f"Cache hit for signature: {implementation_class.__name__}")

        return self._signature_cache[implementation_class]

    def _get_cached_type_hints(self, implementation_class: type) -> dict[str, type]:
        """Get cached type hints for the implementation class."""
        if implementation_class not in self._type_hints_cache:
            logger.debug(f"Cache miss for type hints: {implementation_class.__name__}")

            # Cache the type hints
            self._type_hints_cache[implementation_class] = get_type_hints(
                implementation_class.__init__
            )
        else:
            logger.debug(f"Cache hit for type hints: {implementation_class.__name__}")

        return self._type_hints_cache[implementation_class]

    @classmethod
    def get_cache_stats(cls) -> dict[str, int]:
        """Get current cache statistics for monitoring."""
        return cls._cache_stats.copy()

    @classmethod
    def clear_cache(cls) -> None:
        """Clear all cached signatures and type hints."""
        cls._signature_cache.clear()
        cls._type_hints_cache.clear()
        cls._cache_stats = {"hits": 0, "misses": 0, "total_cached": 0}
        logger.info("DI constructor cache cleared")

    @classmethod
    def get_cache_info(cls) -> str:
        """Get detailed cache information for debugging."""
        hit_rate = (
            cls._cache_stats["hits"]
            / (cls._cache_stats["hits"] + cls._cache_stats["misses"])
            * 100
            if (cls._cache_stats["hits"] + cls._cache_stats["misses"]) > 0
            else 0
        )

        return (
            f"DI Cache Info: {cls._cache_stats['hits']} hits, {cls._cache_stats['misses']} misses, "
            f"hit rate: {hit_rate:.1f}%, signatures cached: {len(cls._signature_cache)}, "
            f"type hints cached: {len(cls._type_hints_cache)}"
        )

    def _is_primitive_type(self, param_type: type) -> bool:
        """Check if a type is a primitive type that should not be resolved as a dependency."""
        from datetime import datetime, timedelta
        from pathlib import Path
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

    def can_resolve(self, service_type: type, registry: Any) -> bool:
        """Check if service has a factory registration."""
        return registry.has_factory_registration(service_type)

    def resolve(self, service_type: type, registry: Any, container: Any) -> Any:
        """Resolve service using factory or transient creation."""
        factory_or_implementation = registry.get_factory_or_implementation(service_type)

        # Check if it's a callable factory function
        if callable(factory_or_implementation) and not inspect.isclass(
            factory_or_implementation
        ):
            # Try to call with container parameter first, fallback to no parameters
            try:
                return factory_or_implementation(container)
            except TypeError:
                # Factory doesn't accept container parameter
                return factory_or_implementation()
        else:
            # It's a class, create with constructor injection
            constructor_resolver = ConstructorResolver()
            return constructor_resolver._create_with_constructor_injection(
                factory_or_implementation, container
            )


class LazyProxy:
    """Lazy loading proxy for expensive dependencies."""

    def __init__(self, service_type: type, container: Any):
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

    def resolve(self, service_type: type, registry: Any, container: Any) -> Any:
        """Attempt resolution through the resolver chain."""
        for resolver in self._resolvers:
            if resolver.can_resolve(service_type, registry):
                return resolver.resolve(service_type, registry, container)

        # No resolver could handle this service type
        return None

    def can_resolve(self, service_type: type, registry: Any) -> bool:
        """Check if any resolver in the chain can handle the service type."""
        return any(
            resolver.can_resolve(service_type, registry) for resolver in self._resolvers
        )

    def get_resolver_count(self) -> int:
        """Get the number of resolvers in the chain."""
        return len(self._resolvers)
