"""
TKA Monorepo Global Pytest Configuration
========================================

This file ensures that pytest works seamlessly from any directory and with any
execution method. It automatically sets up the TKA monorepo import environment
before any tests run.
"""

import pytest

# Import our universal project setup
try:
    from project_root import ensure_project_setup

    ensure_project_setup()
    SETUP_SUCCESS = True
except Exception as e:
    SETUP_SUCCESS = False
    SETUP_ERROR = str(e)


def pytest_configure(config):
    """Configure pytest with TKA Monorepo setup."""
    if not SETUP_SUCCESS:
        pytest.exit(
            f"TKA Monorepo test setup failed: {SETUP_ERROR}\n"
            f"Make sure you're running pytest from within the TKA Monorepo.",
            returncode=1,
        )

    # Register custom markers
    config.addinivalue_line("markers", "modern: Tests for the modern codebase")
    config.addinivalue_line("markers", "legacy: Tests for the legacy codebase")
    config.addinivalue_line("markers", "launcher: Tests for the launcher")
    config.addinivalue_line("markers", "unit: Fast unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")


def pytest_sessionstart(session):
    """Called after the Session object has been created."""
    if session.config.option.verbose >= 1:
        print("\n🚀 TKA Monorepo test environment initialized successfully!")


@pytest.fixture(scope="session")
def tka_project_root():
    """Provide the TKA Monorepo project root path."""
    from project_root import get_project_root

    return get_project_root()


@pytest.fixture(scope="session")
def tka_modern_src():
    """Provide the TKA Modern src path."""
    from project_root import get_modern_src_root

    return get_modern_src_root()


@pytest.fixture(scope="session")
def tka_launcher_root():
    """Provide the TKA Launcher root path."""
    from project_root import get_launcher_root

    return get_launcher_root()


@pytest.fixture
def mock_container():
    """Mock dependency injection container."""
    from unittest.mock import Mock

    container = Mock()
    container.resolve = Mock()
    return container


@pytest.fixture
def mock_beat_data():
    """Real beat data for testing using PictographDatasetService."""
    try:
        from application.services.data.pictograph_dataset_service import (
            PictographDatasetService,
        )

        dataset_service = PictographDatasetService()
        beat_data = dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )

        if beat_data:
            return beat_data
    except ImportError:
        pass

    # Fallback to empty beat if dataset unavailable
    try:
        from domain.models.core_models import BeatData

        return BeatData.empty()
    except ImportError:
        # Final fallback
        return None
