#!/usr/bin/env python3
"""
Mock Infrastructure Tests
========================

Tests to verify our mock infrastructure is working correctly.
"""

import pytest
import sys
from pathlib import Path

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


@pytest.mark.unit
def test_mock_services_creation():
    """Test that mock services can be created."""
    from tests.fixtures.graph_editor import create_all_mock_services

    services = create_all_mock_services()

    assert "graph_service" in services
    assert "data_flow_service" in services
    assert "hotkey_service" in services

    # Test basic functionality
    graph_service = services["graph_service"]
    assert graph_service.get_selected_beat() is None

    # Test method call tracking
    assert graph_service.get_call_count("get_selected_beat") == 1


@pytest.mark.unit
def test_mock_beat_data_creation():
    """Test that mock beat data can be created."""
    from tests.fixtures.graph_editor import create_sample_beat_data

    beat_data = create_sample_beat_data()

    assert beat_data is not None
    assert beat_data.beat_number == 1
    assert beat_data.letter == "A"
    assert beat_data.blue_motion is not None
    assert beat_data.red_motion is not None


@pytest.mark.unit
def test_mock_sequence_data_creation():
    """Test that mock sequence data can be created."""
    from tests.fixtures.graph_editor import create_sample_sequence_data

    sequence_data = create_sample_sequence_data()

    assert sequence_data is not None
    assert sequence_data.name == "Test Sequence"
    assert sequence_data.word == "ABC"
    assert len(sequence_data.beats) == 3


@pytest.mark.unit
def test_fixtures_available(qapp, all_mock_services, sample_beat_data):
    """Test that pytest fixtures are available."""
    assert qapp is not None
    assert all_mock_services is not None
    assert sample_beat_data is not None

    # Test fixture contents
    assert "graph_service" in all_mock_services
    assert sample_beat_data.beat_number == 1


@pytest.mark.unit
def test_signal_spy_fixture(signal_spy):
    """Test that signal spy fixture works."""
    # signal_spy is already an instance
    assert signal_spy is not None

    # Test signal spy functionality
    signal_spy("test", "value1")
    assert signal_spy.was_called()
    assert signal_spy.call_count() == 1
    assert signal_spy.was_called_with("test", "value1")

    signal_spy.reset()
    assert signal_spy.call_count() == 0
