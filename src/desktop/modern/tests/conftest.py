#!/usr/bin/env python3
"""
Global Test Configuration for TKA Modern Tests
==============================================

Provides global pytest fixtures and configuration for all TKA modern tests.
"""
from __future__ import annotations

from pathlib import Path
import sys

import pytest


# Add modern source to path
modern_src = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(modern_src))

# Import specific fixtures from graph editor to avoid conflicts


# Global pytest configuration
def pytest_configure(config):
    """Configure pytest for TKA tests."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "specification: marks tests as specification tests (permanent)"
    )
    config.addinivalue_line(
        "markers", "regression: marks tests as regression tests (bug prevention)"
    )
    config.addinivalue_line(
        "markers", "scaffolding: marks tests as scaffolding tests (temporary)"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line(
        "markers", "ui: marks tests as UI tests requiring QApplication"
    )
    config.addinivalue_line("markers", "critical: marks tests as critical (must pass)")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on location."""
    for item in items:
        # Add markers based on test location
        if "specification" in str(item.fspath):
            item.add_marker(pytest.mark.specification)
        elif "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

        # Add UI marker for tests that use qapp fixture
        if "qapp" in item.fixturenames:
            item.add_marker(pytest.mark.ui)
