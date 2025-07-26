#!/usr/bin/env python3
"""
Comprehensive tests for the enhanced DI container implementation.

Tests all enhanced features including:
- Complex dependency chains
- Enhanced error reporting
- Circular dependency detection
- Service lifecycle management
- Primitive type handling
- Auto-registration with validation
"""

from pathlib import Path
from typing import Optional, Protocol
from unittest.mock import Mock

import pytest
from desktop.modern.core.dependency_injection.di_container import DIContainer, reset_container
from core.exceptions import DependencyInjectionError
from desktop.modern.domain.models.beat_data import BeatData


class IRepository(Protocol):
    """Test repository interface."""

    def save(self, data: str) -> None: ...

    def load(self, id: str) -> str: ...


class IService(Protocol):
    """Test service interface."""

    def process(self, input: str) -> str: ...


class IController(Protocol):
    """Test controller interface."""

    def handle(self, request: str) -> str: ...


class Repository:
    """Test repository implementation."""

    def __init__(self):
        self.data = {}

    def save(self, data: str) -> None:
        self.data["test"] = data

    def load(self, id: str) -> str:
        return self.data.get(id, "not found")


class Service:
    """Test service implementation with dependency."""

    def __init__(self, repo: IRepository):
        self.repo = repo

    def process(self, input: str) -> str:
        self.repo.save(input)
        return f"processed: {input}"


class Controller:
    """Test controller with multiple dependencies and default parameter."""

    def __init__(self, service: IService, config: str = "default"):
        self.service = service
        self.config = config

    def handle(self, request: str) -> str:
        result = self.service.process(request)
        return f"[{self.config}] {result}"


class ServiceWithLifecycle:
    """Test service with lifecycle methods."""

    def __init__(self):
        self.initialized = False
        self.cleaned_up = False

    def initialize(self):
        self.initialized = True

    def cleanup(self):
        self.cleaned_up = True


class CircularA:
    """Test class for circular dependency detection."""

    def __init__(self, b: "CircularB"):
        self.b = b


class CircularB:
    """Test class for circular dependency detection."""

    def __init__(self, a: CircularA):
        self.a = a


class ServiceWithPrimitives:
    """Test service with primitive type parameters."""

    def __init__(self, count: int = 5, enabled: bool = True, name: str = "default"):
        self.name = name
        self.count = count
        self.enabled = enabled


class TestEnhancedDIContainer:
    """Test suite for enhanced DI container features."""

    def setup_method(self):
        """Reset container before each test."""
        reset_container()
        self.container = DIContainer()

    def test_basic_dependency_injection(self):
        """Test basic dependency injection works."""
        self.container.register_singleton(IRepository, Repository)
        self.container.register_singleton(IService, Service)

        service = self.container.resolve(IService)
        assert isinstance(service, Service)
        assert hasattr(service, "repo")
        assert isinstance(service.repo, Repository)

    def test_complex_dependency_chain(self):
        """Test complex multi-level dependency chain using resolve()."""
        self.container.register_singleton(IRepository, Repository)
        self.container.register_singleton(IService, Service)

        # Register Controller as IController to enable resolution
        self.container.register_singleton(IController, Controller)

        controller = self.container.resolve(IController)

        assert isinstance(controller, Controller)
        assert isinstance(controller.service, Service)
        assert isinstance(controller.service.repo, Repository)
        assert controller.config == "default"  # Default parameter used

    def test_default_parameter_handling(self):
        """Test that default parameters are handled correctly."""
        # Register the class so it can be resolved
        self.container.register_singleton(ServiceWithPrimitives, ServiceWithPrimitives)

        controller = self.container.resolve(ServiceWithPrimitives)

        # Should skip primitive types and use defaults
        assert controller.count == 5
        assert controller.enabled == True

    def test_enhanced_error_reporting(self):
        """Test enhanced error messages for missing dependencies."""
        self.container.register_singleton(IRepository, Repository)
        # Don't register IService - this should cause a detailed error
        self.container.register_singleton(IController, Controller)

        with pytest.raises(DependencyInjectionError) as exc_info:
            self.container.resolve(IController)

        error_msg = str(exc_info.value)
        assert "IService" in error_msg
        assert "is not registered" in error_msg

    def test_auto_register_with_validation(self):
        """Test auto-registration with comprehensive validation."""
        # This should work - Repository implements IRepository
        self.container.auto_register_with_validation(IRepository, Repository)

        repo = self.container.resolve(IRepository)
        assert isinstance(repo, Repository)

    def test_dependency_chain_validation(self):
        """Test dependency chain validation during registration."""
        # Register Repository first
        self.container.register_singleton(IRepository, Repository)

        # This should work - Service's dependency (IRepository) is registered
        self.container.auto_register_with_validation(IService, Service)

        # Test the failure case with a new container
        fresh_container = DIContainer()
        fresh_container.register_singleton(IRepository, Repository)
        # Don't register IService - this should fail validation

        with pytest.raises(Exception) as exc_info:
            # Try to register Controller without IService being registered
            fresh_container.auto_register_with_validation(IController, Controller)

        error_msg = str(exc_info.value)
        assert "IService" in error_msg

    def test_validate_all_registrations(self):
        """Test validation of all registered services."""
        self.container.register_singleton(IRepository, Repository)
        self.container.register_singleton(IService, Service)

        # This should pass - all dependencies can be resolved
        self.container.validate_all_registrations()

    def test_primitive_type_detection(self):
        """Test comprehensive primitive type detection."""
        container = self.container

        # Test basic primitives
        assert container._is_primitive_type(str)
        assert container._is_primitive_type(int)
        assert container._is_primitive_type(bool)
        assert container._is_primitive_type(list)
        assert container._is_primitive_type(dict)

        # Test Optional types
        from typing import Optional

        assert container._is_primitive_type(Optional[str])
        assert container._is_primitive_type(Optional[int])

        # Test Path and datetime
        from datetime import datetime
        from pathlib import Path

        assert container._is_primitive_type(Path)
        assert container._is_primitive_type(datetime)

        # Test non-primitives
        assert not container._is_primitive_type(Repository)
        assert not container._is_primitive_type(IRepository)

    def test_dependency_graph_generation(self):
        """Test dependency graph generation for debugging."""
        self.container.register_singleton(IRepository, Repository)
        self.container.register_singleton(IService, Service)

        graph = self.container.get_dependency_graph()

        assert isinstance(graph, dict)
        # The exact format may vary, but it should contain information about services
        assert len(graph) > 0

    def test_constructor_dependency_analysis(self):
        """Test constructor dependency analysis via validation engine."""
        # Access the validation engine to test dependency analysis
        validation_engine = self.container._validation_engine

        deps = validation_engine._get_constructor_dependencies(Service)

        assert len(deps) == 1
        assert IRepository in deps

        # Test class with default parameters
        deps = validation_engine._get_constructor_dependencies(Controller)
        assert len(deps) == 1  # Only IService, not the default 'config' parameter
        assert IService in deps

    def test_lifecycle_management(self):
        """Test service lifecycle management."""
        # Register a service with lifecycle
        self.container.register_singleton(ServiceWithLifecycle, ServiceWithLifecycle)

        # Use the lifecycle manager directly for testing
        lifecycle_manager = self.container._lifecycle_manager
        instance = lifecycle_manager.create_with_lifecycle(ServiceWithLifecycle())

        assert isinstance(instance, ServiceWithLifecycle)

        # Test cleanup
        self.container.cleanup_all()

    def test_circular_dependency_detection(self):
        """Test circular dependency detection."""
        # Register both classes that depend on each other
        self.container.register_singleton(CircularA, CircularA)
        self.container.register_singleton(CircularB, CircularB)

        # This should detect the circular dependency when trying to resolve
        with pytest.raises(Exception) as exc_info:
            self.container.resolve(CircularA)

        error_msg = str(exc_info.value)
        assert "Circular dependency" in error_msg or "CircularA" in error_msg

    def test_transient_services(self):
        """Test transient service registration and resolution."""
        self.container.register_transient(IRepository, Repository)

        # Should get different instances each time
        repo1 = self.container.resolve(IRepository)
        repo2 = self.container.resolve(IRepository)

        assert isinstance(repo1, Repository)
        assert isinstance(repo2, Repository)
        assert repo1 is not repo2  # Different instances

    def test_singleton_services(self):
        """Test singleton service registration and resolution."""
        self.container.register_singleton(IRepository, Repository)

        # Should get same instance each time
        repo1 = self.container.resolve(IRepository)
        repo2 = self.container.resolve(IRepository)

        assert isinstance(repo1, Repository)
        assert isinstance(repo2, Repository)
        assert repo1 is repo2  # Same instance

    def test_instance_registration(self):
        """Test direct instance registration."""
        repo_instance = Repository()
        repo_instance.save("test_data")

        self.container.register_instance(IRepository, repo_instance)

        resolved = self.container.resolve(IRepository)
        assert resolved is repo_instance
        assert resolved.load("test") == "test_data"

    def test_missing_service_error(self):
        """Test error when resolving unregistered service."""
        with pytest.raises(DependencyInjectionError) as exc_info:
            self.container.resolve(IRepository)

        error_msg = str(exc_info.value)
        assert "IRepository" in error_msg
        assert "is not registered" in error_msg

    def test_complex_error_scenario(self):
        """Test complex error scenario with detailed reporting."""
        # Register some services but not all
        self.container.register_singleton(IRepository, Repository)
        # Missing IService registration
        self.container.register_singleton(IController, Controller)

        with pytest.raises(DependencyInjectionError) as exc_info:
            self.container.resolve(IController)

        error_msg = str(exc_info.value)
        assert "IService" in error_msg

    def test_get_registrations(self):
        """Test getting all registrations for debugging."""
        self.container.register_singleton(IRepository, Repository)
        self.container.register_transient(IService, Service)

        registrations = self.container.get_registrations()

        assert IRepository in registrations
        assert IService in registrations
        assert registrations[IRepository] == Repository
        assert registrations[IService] == Service


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
