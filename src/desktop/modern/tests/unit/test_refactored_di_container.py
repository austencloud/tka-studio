"""
Tests for the refactored DI container.
Verifies that the modular architecture works correctly.
"""
from __future__ import annotations

import os
import sys

import pytest


# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))


def test_di_container_imports():
    """Test that all refactored DI modules import correctly."""
    try:
        # Test main container import
        from core.dependency_injection import (
            DIContainer,
            get_container,
            reset_container,
        )

        assert DIContainer is not None
        assert get_container is not None
        assert reset_container is not None

        # Test focused module imports
        from core.dependency_injection import (
            DebuggingTools,
            IServiceResolver,
            LazyProxy,
            LifecycleManager,
            ResolverChain,
            ServiceDescriptor,
            ServiceRegistry,
            ServiceScope,
            ValidationEngine,
        )

        assert ServiceRegistry is not None
        assert ServiceScope is not None
        assert ServiceDescriptor is not None
        assert ResolverChain is not None
        assert LazyProxy is not None
        assert IServiceResolver is not None
        assert LifecycleManager is not None
        assert ValidationEngine is not None
        assert DebuggingTools is not None

        print("✅ All DI module imports successful")

    except Exception as e:
        pytest.fail(f"DI module import failed: {e}")


def test_di_container_creation():
    """Test that the refactored DI container can be created."""
    try:
        from core.dependency_injection import DIContainer

        container = DIContainer()
        assert container is not None

        # Test that modules are initialized
        assert hasattr(container, "_registry")
        assert hasattr(container, "_resolver_chain")
        assert hasattr(container, "_lifecycle_manager")
        assert hasattr(container, "_validation_engine")
        assert hasattr(container, "_debugging_tools")

        print("✅ DI container creation successful")

    except Exception as e:
        pytest.fail(f"DI container creation failed: {e}")


def test_basic_service_registration():
    """Test basic service registration functionality."""
    try:
        from core.dependency_injection import DIContainer

        # Create test classes
        class ITestService:
            def get_value(self) -> str:
                pass

        class TestService:
            def get_value(self) -> str:
                return "test_value"

        # Test registration
        container = DIContainer()
        container.register_singleton(ITestService, TestService)

        # Verify registration
        registrations = container.get_registrations()
        assert ITestService in registrations
        assert registrations[ITestService] == TestService

        print("✅ Basic service registration successful")

    except Exception as e:
        pytest.fail(f"Service registration failed: {e}")


def test_service_resolution():
    """Test service resolution functionality."""
    try:
        from core.dependency_injection import DIContainer

        # Create test classes
        class ITestService:
            def get_value(self) -> str:
                pass

        class TestService:
            def get_value(self) -> str:
                return "test_value"

        # Test resolution
        container = DIContainer()
        container.register_singleton(ITestService, TestService)

        # Resolve service
        service = container.resolve(ITestService)
        assert service is not None
        assert isinstance(service, TestService)
        assert service.get_value() == "test_value"

        # Test singleton behavior
        service2 = container.resolve(ITestService)
        assert service is service2  # Should be same instance

        print("✅ Service resolution successful")

    except Exception as e:
        pytest.fail(f"Service resolution failed: {e}")


def test_debugging_functionality():
    """Test debugging tools functionality."""
    try:
        from core.dependency_injection import DIContainer

        class ITestService:
            def get_value(self) -> str:
                pass

        class TestService:
            def get_value(self) -> str:
                return "test_value"

        container = DIContainer()
        container.register_singleton(ITestService, TestService)

        # Test debugging methods
        dependency_graph = container.get_dependency_graph()
        assert isinstance(dependency_graph, dict)

        performance_metrics = container.get_performance_metrics()
        assert isinstance(performance_metrics, dict)

        diagnostic_report = container.generate_diagnostic_report()
        assert isinstance(diagnostic_report, str)
        assert "DI Container Diagnostic Report" in diagnostic_report

        print("✅ Debugging functionality successful")

    except Exception as e:
        pytest.fail(f"Debugging functionality failed: {e}")


def test_lifecycle_management():
    """Test lifecycle management functionality."""
    try:
        from core.dependency_injection import DIContainer

        class TestServiceWithLifecycle:
            def __init__(self):
                self.initialized = False
                self.cleaned_up = False

            def initialize(self):
                self.initialized = True

            def cleanup(self):
                self.cleaned_up = True

            def get_value(self) -> str:
                return "test_value"

        container = DIContainer()
        container.register_singleton(TestServiceWithLifecycle, TestServiceWithLifecycle)

        # Resolve service (should trigger lifecycle)
        service = container.resolve(TestServiceWithLifecycle)
        assert service.initialized is True

        # Test cleanup
        container.cleanup_all()
        assert service.cleaned_up is True

        print("✅ Lifecycle management successful")

    except Exception as e:
        pytest.fail(f"Lifecycle management failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
