#!/usr/bin/env python3
"""
Centralized Test Isolation System
=================================

Provides automatic test isolation and cleanup mechanisms to prevent
state contamination between tests without requiring per-class modifications.
"""

import gc
import sys
from pathlib import Path
from typing import Any, Dict, Set
from unittest.mock import Mock

import pytest

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


class TestIsolationManager:
    """Manages test isolation and cleanup across the test suite."""
    
    def __init__(self):
        self._global_state_backup: Dict[str, Any] = {}
        self._mock_registry: Set[Mock] = set()
        self._cleanup_callbacks = []
    
    def setup_test_isolation(self):
        """Set up test isolation before each test."""
        # Reset DI container
        self._reset_di_container()
        
        # Clear mock registry
        self._mock_registry.clear()
        
        # Reset global state
        self._reset_global_state()
    
    def teardown_test_isolation(self):
        """Clean up after each test."""
        # Reset all registered mocks
        self._reset_registered_mocks()
        
        # Reset DI container
        self._reset_di_container()
        
        # Run cleanup callbacks
        self._run_cleanup_callbacks()
        
        # Force garbage collection
        gc.collect()
    
    def register_mock(self, mock_obj: Mock):
        """Register a mock for automatic cleanup."""
        self._mock_registry.add(mock_obj)
    
    def add_cleanup_callback(self, callback):
        """Add a cleanup callback to run during teardown."""
        self._cleanup_callbacks.append(callback)
    
    def _reset_di_container(self):
        """Reset the DI container to clean state."""
        try:
            from core.dependency_injection.di_container import reset_container
            reset_container()
        except ImportError:
            pass  # DI container not available
    
    def _reset_registered_mocks(self):
        """Reset all registered mocks."""
        for mock_obj in self._mock_registry:
            if hasattr(mock_obj, 'reset_mock'):
                mock_obj.reset_mock()
    
    def _reset_global_state(self):
        """Reset any global state that might affect tests."""
        # Reset any global caches or singletons
        pass
    
    def _run_cleanup_callbacks(self):
        """Run all registered cleanup callbacks."""
        for callback in self._cleanup_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Warning: Cleanup callback failed: {e}")
        self._cleanup_callbacks.clear()


# Global isolation manager instance
_isolation_manager = TestIsolationManager()


@pytest.fixture(autouse=True)
def test_isolation():
    """
    Automatic test isolation fixture.
    
    This fixture runs for every test and ensures proper cleanup
    without requiring manual setup/teardown methods.
    """
    # Setup before test
    _isolation_manager.setup_test_isolation()
    
    yield _isolation_manager
    
    # Cleanup after test
    _isolation_manager.teardown_test_isolation()


@pytest.fixture
def isolation_manager():
    """Provide access to the isolation manager for manual control."""
    return _isolation_manager


def auto_configure_mocks(*mocks):
    """
    Decorator to automatically configure mocks with proper iterable support.
    
    Usage:
        @auto_configure_mocks
        def test_something():
            mock_service = Mock()
            # mock_service is automatically configured with iterable support
    """
    def decorator(test_func):
        def wrapper(*args, **kwargs):
            # Import here to avoid circular dependencies
            from tests.fixtures.mock_configurations import create_mock_with_iterables
            
            # Configure any Mock objects in the test
            frame = sys._getframe(1)
            for name, value in frame.f_locals.items():
                if isinstance(value, Mock):
                    create_mock_with_iterables(value)
                    _isolation_manager.register_mock(value)
            
            return test_func(*args, **kwargs)
        return wrapper
    return decorator


def configure_mock_for_iteration(mock_obj: Mock, iterable_attrs: list = None):
    """
    Configure a mock object to support iteration operations.
    
    Args:
        mock_obj: Mock object to configure
        iterable_attrs: List of attributes that should return iterables
    """
    if iterable_attrs is None:
        iterable_attrs = ['values', 'keys', 'items']
    
    for attr in iterable_attrs:
        if hasattr(mock_obj, attr):
            getattr(mock_obj, attr).return_value = []
    
    # Configure basic iteration support
    mock_obj.__iter__ = Mock(return_value=iter([]))
    mock_obj.__len__ = Mock(return_value=0)
    mock_obj.__contains__ = Mock(return_value=False)
    
    # Register for cleanup
    _isolation_manager.register_mock(mock_obj)


def create_section_mock_with_pictographs(pictograph_count: int = 2):
    """
    Create a properly configured section mock with pictographs.
    
    Args:
        pictograph_count: Number of mock pictographs to create
        
    Returns:
        Configured section mock
    """
    from tests.fixtures.mock_configurations import configure_section_mock
    
    section_mock = Mock()
    pictographs = [Mock() for _ in range(pictograph_count)]
    configure_section_mock(section_mock, pictographs)
    
    _isolation_manager.register_mock(section_mock)
    return section_mock


def create_widget_pool_mock(widget_count: int = 5):
    """
    Create a properly configured widget pool mock.
    
    Args:
        widget_count: Number of mock widgets to create
        
    Returns:
        Configured widget pool mock
    """
    from tests.fixtures.mock_configurations import configure_widget_pool_mock
    
    pool_mock = Mock()
    configure_widget_pool_mock(pool_mock, widget_count)
    
    _isolation_manager.register_mock(pool_mock)
    return pool_mock


def create_data_cache_mock():
    """
    Create a properly configured data cache manager mock.
    
    Returns:
        Configured data cache mock
    """
    from tests.fixtures.mock_configurations import DataCacheManagerMock
    
    cache_mock = DataCacheManagerMock()
    _isolation_manager.register_mock(cache_mock)
    return cache_mock


# Convenience functions for common mock patterns
def mock_with_iterable_values(return_values: list = None):
    """Create a mock that returns proper iterable values."""
    if return_values is None:
        return_values = []
    
    mock = Mock()
    mock.values.return_value = return_values
    mock.keys.return_value = [f"key_{i}" for i in range(len(return_values))]
    mock.items.return_value = [(f"key_{i}", val) for i, val in enumerate(return_values)]
    
    _isolation_manager.register_mock(mock)
    return mock


def mock_with_empty_collections():
    """Create a mock that returns empty collections for all iterable operations."""
    mock = Mock()
    configure_mock_for_iteration(mock)
    return mock
