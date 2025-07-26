#!/usr/bin/env python3
"""
Global Test Configuration for TKA Modern Tests
==============================================

Provides global pytest fixtures and configuration for all TKA modern tests.
"""

import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

# Add modern source to path
modern_src = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(modern_src))

# Import specific fixtures from graph editor (excluding problematic autouse fixtures)
from desktop.modern.tests.fixtures.graph_editor.conftest import (
    basic_test_data,
    complex_beat,
    complex_test_data,
    comprehensive_test_data,
    edge_case_data,
    mock_data_flow_service,
    mock_graph_service,
    mock_hotkey_service,
    mock_parent_widget,
    qapp,
    regular_beat,
    sample_beat_data,
    sample_sequence_data,
    signal_spy,
    start_position_beat,
    test_di_container,
    tka_test_helper,
)

# Import mock configurations for manual use
from desktop.modern.tests.fixtures.mock_configurations import (
    DataCacheManagerMock,
    SectionManagerMock,
    WidgetPoolManagerMock,
    create_mock_with_iterables,
    get_configured_mock,
)


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


def pytest_runtest_teardown(item, nextitem):
    """
    Clean up Qt objects and global state between tests.

    This follows pytest-qt best practices for preventing Qt memory leaks
    and ensures proper test isolation by cleaning up global state.
    """
    import gc

    from PyQt6.QtWidgets import QApplication

    # Clean up Qt objects
    app = QApplication.instance()
    if app is not None:
        # Process any pending Qt events
        app.processEvents()

        # Close any remaining windows (except main application windows)
        for widget in app.allWidgets():
            if widget.isWindow() and not widget.isVisible():
                widget.close()
                widget.deleteLater()

        # Process deletion events
        app.processEvents()

    # Clean up DI container global state
    try:
        from desktop.modern.core.dependency_injection.di_container import reset_container

        reset_container()
    except ImportError:
        pass  # DI container not available

    # Force garbage collection to clean up Python objects
    gc.collect()
