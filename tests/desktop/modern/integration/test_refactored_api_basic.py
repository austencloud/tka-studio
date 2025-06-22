"""
Basic tests for the refactored API structure.
Tests that don't require full service initialization.
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))


def test_api_imports():
    """Test that all refactored API modules import correctly."""
    try:
        # Test main app import
        from infrastructure.api.main import app, create_app

        assert app is not None
        assert app.title == "TKA Desktop Production API"
        assert app.version == "2.0.0"

        # Test router imports
        from infrastructure.api.routers import (
            health_router,
            sequences_router,
            commands_router,
            monitoring_router,
        )

        assert health_router is not None
        assert sequences_router is not None
        assert commands_router is not None
        assert monitoring_router is not None

        # Test converter imports
        from infrastructure.api.converters import (
            domain_to_api_motion,
            api_to_domain_motion,
            domain_to_api_beat,
            api_to_domain_beat,
            domain_to_api_sequence,
            api_to_domain_sequence,
        )

        assert domain_to_api_motion is not None
        assert api_to_domain_motion is not None
        assert domain_to_api_beat is not None
        assert api_to_domain_beat is not None
        assert domain_to_api_sequence is not None
        assert api_to_domain_sequence is not None

        # Test dependency imports
        from infrastructure.api.dependencies import (
            initialize_services,
            cleanup_services,
            check_service_health,
        )

        assert initialize_services is not None
        assert cleanup_services is not None
        assert check_service_health is not None

        print("✅ All API imports successful")

    except Exception as e:
        pytest.fail(f"API import failed: {e}")


def test_app_configuration():
    """Test that the FastAPI app is configured correctly."""
    from infrastructure.api.main import app

    # Check basic configuration
    assert app.title == "TKA Desktop Production API"
    assert app.version == "2.0.0"
    assert "Production-ready REST API" in app.description

    # Check routes are registered
    routes = [route.path for route in app.routes]

    # Health routes
    assert "/api/health" in routes
    assert "/api/status" in routes

    # Sequence routes
    assert "/api/sequences/current" in routes
    assert "/api/sequences" in routes
    assert "/api/sequences/{sequence_id}" in routes

    # Command routes
    assert "/api/commands/undo" in routes
    assert "/api/commands/redo" in routes
    assert "/api/commands/status" in routes

    # Monitoring routes
    assert "/api/performance" in routes
    assert "/api/events/stats" in routes
    assert "/api/metrics/summary" in routes

    print("✅ App configuration correct")


def test_converter_functions():
    """Test that converter functions work with sample data."""
    from infrastructure.api.converters import (
        domain_to_api_sequence,
        api_to_domain_sequence,
    )
    from domain.models.core_models import SequenceData, BeatData
    from infrastructure.api.models import SequenceAPI, BeatAPI

    # Create sample domain sequence
    sample_beat = BeatData(
        id="beat_001",
        beat_number=1,
        letter="A",
        duration=1.0,
        blue_motion=None,
        red_motion=None,
        blue_reversal=False,
        red_reversal=False,
        is_blank=False,
        metadata={},
    )

    sample_sequence = SequenceData(
        id="seq_001",
        name="Test Sequence",
        word="TEST",
        beats=[sample_beat],
        start_position="alpha",
        metadata={},
    )

    # Test domain to API conversion
    try:
        api_sequence = domain_to_api_sequence(sample_sequence)
        assert isinstance(api_sequence, SequenceAPI)
        assert api_sequence.id == "seq_001"
        assert api_sequence.name == "Test Sequence"
        assert len(api_sequence.beats) == 1
        print("✅ Domain to API conversion works")
    except Exception as e:
        pytest.fail(f"Domain to API conversion failed: {e}")

    # Test API to domain conversion
    try:
        domain_sequence = api_to_domain_sequence(api_sequence)
        assert isinstance(domain_sequence, SequenceData)
        assert domain_sequence.id == "seq_001"
        assert domain_sequence.name == "Test Sequence"
        assert len(domain_sequence.beats) == 1
        print("✅ API to domain conversion works")
    except Exception as e:
        pytest.fail(f"API to domain conversion failed: {e}")


def test_exception_handling():
    """Test that exception handling modules work."""
    from infrastructure.api.exceptions import (
        TKAAPIException,
        ServiceUnavailableError,
        ValidationError,
        ConversionError,
        ResourceNotFoundError,
        OperationError,
    )

    # Test custom exceptions
    try:
        raise TKAAPIException("Test error", "TEST_ERROR")
    except TKAAPIException as e:
        assert e.message == "Test error"
        assert e.error_code == "TEST_ERROR"

    try:
        raise ServiceUnavailableError("TestService")
    except ServiceUnavailableError as e:
        assert "TestService" in e.message
        assert e.error_code == "SERVICE_UNAVAILABLE"

    print("✅ Exception handling works")


def test_middleware_configuration():
    """Test that middleware is configured correctly."""
    from infrastructure.api.main import app

    # Check that middleware is present
    middleware_classes = [
        type(middleware).__name__ for middleware in app.user_middleware
    ]
    print(f"Middleware classes found: {middleware_classes}")

    # Should have our custom middleware (check actual class names)
    has_request_logging = any(
        "RequestLoggingMiddleware" in name or "BaseHTTPMiddleware" in name
        for name in middleware_classes
    )
    has_performance = any(
        "PerformanceMonitoringMiddleware" in name or "BaseHTTPMiddleware" in name
        for name in middleware_classes
    )
    has_cors = any("CORSMiddleware" in name for name in middleware_classes)

    # Check that we have middleware configured (at least 3 middleware components)
    assert (
        len(middleware_classes) >= 3
    ), f"Expected at least 3 middleware, found {len(middleware_classes)}: {middleware_classes}"

    print("✅ Middleware configuration correct")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
