"""
Pytest configuration for TKA Desktop tests.
"""

import pytest
from unittest.mock import Mock

# Try to import BeatData, but don't fail if not available
try:
    from tka.desktop.modern.domain.models.core_models import BeatData

    BEAT_DATA_AVAILABLE = True
except ImportError:
    BEAT_DATA_AVAILABLE = False
    BeatData = None


@pytest.fixture
def mock_container():
    """Mock dependency injection container."""
    container = Mock()
    container.resolve = Mock()
    return container


@pytest.fixture
def qtbot_with_container(qtbot, mock_container):
    """Extended qtbot with dependency container."""
    qtbot.container = mock_container
    return qtbot


@pytest.fixture
def mock_beat_data():
    """Real beat data for testing using BeatData model."""
    if not BEAT_DATA_AVAILABLE or BeatData is None:
        return None

    try:
        return BeatData.empty()
    except Exception:
        # If BeatData.empty() doesn't exist, return None
        return None


@pytest.fixture
def dummy_conftest_fixture():
    """A simple fixture to test conftest loading."""
    return "hello_from_desktop_conftest"
