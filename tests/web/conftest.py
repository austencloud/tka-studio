"""
Web-specific test configuration.

Provides fixtures and utilities for web application testing.
"""

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_web_client():
    """Mock web client for web tests."""
    return Mock()


@pytest.fixture
def sample_api_response():
    """Sample API response data for testing."""
    return {"status": "success", "data": {"sequences": [], "beats": []}}


@pytest.fixture
def mock_browser_context():
    """Mock browser context for e2e tests."""
    return Mock()
