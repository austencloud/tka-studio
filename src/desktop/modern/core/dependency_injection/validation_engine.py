"""
Validation Engine - Comprehensive Dependency Validation

Handles:
- Service registration validation
- Protocol compliance validation
- Dependency chain validation
- Circular dependency detection
- Type safety validation
"""

from __future__ import annotations

import inspect
import logging
from typing import Any, get_type_hints


try:
    from ..exceptions import DependencyInjectionError
except ImportError:
    # Fallback for tests
    class DependencyInjectionError(Exception):
        def __init__(
            self,
            message: str,
            interface_name: str = None,
            dependency_chain: list = None,
            context: dict[str, Any] = None,
        ):
            super().__init__(message)
            self.interface_name = interface_name
            self.dependency_chain = dependency_chain or []


logger = logging.getLogger(__name__)


class ValidationEngine:
    """
    Comprehensive validation engine for dependency injection operations.

    Provides validation for service registrations, dependency chains,
    Protocol compliance, and circular dependency detection.
    """

    def __init__(self):
        self._validation_cache: dict[type, bool] = {}

    def validate_registration(self, interface: type, implementation: type) -> None:
        """Validate that implementation can fulfill interface contract."""
        if not inspect.isclass(implementation):
            raise DependencyInjectionError(
                f"Implementation {implementation} must be a class",
                interface_name=getattr(interface, "__name__", str(interface)),
            )

        # Basic validation - implementation should be a subclass or implement interface
        if hasattr(interface, "__origin__") and interface.__origin__ is not None:
            # Handle generic types
            return

        # Skip Protocol validation in basic registration - only validate in auto_register
        if hasattr(interface, "_is_protocol") and interface._is_protocol:
            return  # Protocol validation handled separately

        if inspect.isclass(interface) and not issubclass(implementation, interface):
            # For concrete classes, check inheritance
            if not hasattr(interface, "__annotations__"):
                logger.warning(
                    f"No inheritance relationship between {interface} and {implementation}"
                )

    def validate_protocol_implementation(
        self, protocol: type, implementation: type
    ) -> None:
        """Validate implementation fulfills Protocol contract."""
        if not hasattr(protocol, "_is_protocol") or not protocol._is_protocol:
            return  # Not a Protocol, skip validation

        # Get protocol methods from annotations
        protocol_methods = getattr(protocol, "__annotations__", {})

        # Also check for methods defined in the protocol
        for attr_name in dir(protocol):
            if not attr_name.startswith("_") and attr_name not in protocol_methods:
                attr = getattr(protocol, attr_name)
                if callable(attr):
                    protocol_methods[attr_name] = attr

        # Check implementation has all required methods
        for method_name in protocol_methods:
            if not hasattr(implementation, method_name):
                raise DependencyInjectionError(
                    f"{implementation.__name__} doesn't implement {method_name} from {protocol.__name__}",
                    interface_name=protocol.__name__,
                )

    def validate_dependency_chain(self, implementation: type, registry: Any) -> None:
        """Validate that all constructor dependencies can be resolved."""
        signature = inspect.signature(implementation.__init__)
        type_hints = get_type_hints(implementation.__init__)

        for param_name, param in signature.parameters.items():
            if param_name == "self":
                continue

            # Skip if has default value
            if param.default != inspect.Parameter.empty:
                continue

            param_type = type_hints.get(param_name, param.annotation)

            # Skip primitives
            if self.is_primitive_type(param_type):
                continue

            # Check if dependency is registered
            if not registry.is_registered(param_type):
                raise DependencyInjectionError(
                    f"Dependency {param_type.__name__} for {implementation.__name__} "
                    f"is not registered. Register it first or make parameter optional.",
                    interface_name=implementation.__name__,
                )

    def validate_all_registrations(self, registry: Any) -> None:
        """
        Validate all service registrations can be resolved.

        Raises:
            DependencyInjectionError: If any registration cannot be resolved
        """
        errors = []

        # Get all registrations from registry
        all_registrations = registry.get_all_registrations()

        # Validate each registration
        for interface, implementation in all_registrations.items():
            try:
                self._validate_single_registration(interface, implementation, registry)
            except Exception as e:
                errors.append(f"{interface.__name__}: {e}")

        if errors:
            raise DependencyInjectionError(
                f"Registration validation failed: {'; '.join(errors)}"
            )

    def _validate_single_registration(
        self, interface: type, implementation: type, registry: Any
    ) -> None:
        """Validate a single registration without creating instances."""
        # Check if implementation is a class
        if not inspect.isclass(implementation):
            raise DependencyInjectionError(
                f"Implementation {implementation} must be a class",
                interface_name=interface.__name__,
            )

        # Check constructor dependencies
        try:
            signature = inspect.signature(implementation.__init__)
            type_hints = get_type_hints(implementation.__init__)

            for param_name, param in signature.parameters.items():
                if param_name == "self":
                    continue

                param_type = type_hints.get(param_name, param.annotation)

                # Skip primitive types, optional parameters, and special parameters
                if (
                    param_type == inspect.Parameter.empty
                    or param_type == inspect._empty
                    or str(param_type) == "_empty"
                    or self.is_primitive_type(param_type)
                    or param.default != inspect.Parameter.empty
                    or param.kind
                    in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
                ):
                    continue

                # Check if dependency is registered
                if not registry.is_registered(param_type):
                    available_services = list(registry.get_all_registrations().keys())
                    available_names = [svc.__name__ for svc in available_services]
                    raise DependencyInjectionError(
                        f"Dependency {param_type.__name__} for parameter '{param_name}' "
                        f"is not registered. Available: {available_names}",
                        interface_name=interface.__name__,
                    )

        except Exception as e:
            if isinstance(e, DependencyInjectionError):
                raise
            raise DependencyInjectionError(
                f"Validation failed for {interface.__name__}: {e}",
                interface_name=interface.__name__,
            ) from e

    def detect_circular_dependencies(
        self, start_type: type, registry: Any, visited: set[type] = None
    ) -> None:
        """Detect circular dependencies in the service graph."""
        if visited is None:
            visited = set()

        if start_type in visited:
            cycle_path = (
                " -> ".join(t.__name__ for t in visited) + f" -> {start_type.__name__}"
            )
            raise DependencyInjectionError(
                f"Circular dependency detected: {cycle_path}"
            )

        visited.add(start_type)

        # Get implementation for this type
        implementation = registry.get_service_implementation(start_type)
        if implementation:
            dependencies = self._get_constructor_dependencies(implementation)
            for dep in dependencies:
                self.detect_circular_dependencies(dep, registry, visited.copy())

    def _get_constructor_dependencies(self, implementation: type) -> list[type]:
        """Get list of constructor dependencies for a class."""
        try:
            signature = inspect.signature(implementation.__init__)
            type_hints = get_type_hints(implementation.__init__)
            dependencies = []

            for param_name, param in signature.parameters.items():
                if param_name == "self":
                    continue

                # Skip if has default value
                if param.default != inspect.Parameter.empty:
                    continue

                param_type = type_hints.get(param_name, param.annotation)

                # Skip if no type annotation
                if not param_type or param_type == inspect.Parameter.empty:
                    continue

                # Skip primitive types
                if self.is_primitive_type(param_type):
                    continue

                dependencies.append(param_type)

            return dependencies

        except Exception:
            return []

    def is_primitive_type(self, param_type: type) -> bool:
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
                    return self.is_primitive_type(non_none_type)
                # For other Union types, check if all args are primitive
                return all(arg in primitive_types for arg in args)
            # Other generic types like List[str], Dict[str, int] are considered primitive
            if origin in primitive_types:
                return True

        # Check if it's a builtin type
        if hasattr(param_type, "__module__") and param_type.__module__ == "builtins":
            return True

        return param_type in primitive_types

    def auto_register_with_validation(
        self, interface: type, implementation: type, registry: Any
    ) -> None:
        """Register service with comprehensive validation."""
        # Step 1: Validate Protocol implementation
        self.validate_protocol_implementation(interface, implementation)

        # Step 2: Validate dependency chain can be resolved
        self.validate_dependency_chain(implementation, registry)

        # Step 3: Register if validation passes
        registry.register_singleton(interface, implementation)

        logger.info(
            f"✅ Successfully registered {interface.__name__} -> {implementation.__name__}"
        )

    def clear_validation_cache(self) -> None:
        """Clear the validation cache."""
        self._validation_cache.clear()
        logger.debug("Validation cache cleared")
