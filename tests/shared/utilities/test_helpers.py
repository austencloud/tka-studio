"""
Shared test utilities for TKA testing.

Common helper functions used across all test types.
"""
from pathlib import Path
from typing import Dict, Any
import json
from unittest.mock import Mock

def load_test_data(filename: str) -> Dict[str, Any]:
    """Load test data from JSON file."""
    data_path = Path(__file__).parent.parent / "data" / filename
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_mock_sequence_data(**kwargs):
    """Create mock sequence data for testing."""
    defaults = {
        "id": "test_sequence_001",
        "length": 4,
        "beats": []
    }
    defaults.update(kwargs)
    return defaults

def create_mock_beat_data(**kwargs):
    """Create mock beat data for testing."""
    defaults = {
        "id": "test_beat_001",
        "blue_motion": None,
        "red_motion": None
    }
    defaults.update(kwargs)
    return defaults

def create_mock_container():
    """Create a mock dependency injection container."""
    container = Mock()
    container.resolve = Mock()
    return container

def assert_valid_pictograph_data(pictograph_data):
    """Assert that pictograph data is valid."""
    assert pictograph_data is not None
    assert hasattr(pictograph_data, 'blue_motion')
    assert hasattr(pictograph_data, 'red_motion')
    
def create_test_workspace_path():
    """Get the test workspace root path."""
    return Path(__file__).parent.parent.parent
