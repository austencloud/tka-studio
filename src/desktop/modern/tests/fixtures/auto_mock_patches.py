#!/usr/bin/env python3
"""
Automatic Mock Patches for Common Test Patterns
===============================================

Provides automatic patching of common services and components that
frequently cause "Mock object is not iterable" errors in tests.
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch
from typing import Dict, Any, List

import pytest

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


class AutoMockPatcher:
    """Automatically patches common services with proper mock configurations."""
    
    def __init__(self):
        self.active_patches = []
        self.mock_registry = {}
    
    def start_patches(self):
        """Start all automatic patches."""
        self._patch_data_cache_manager()
        self._patch_section_managers()
        self._patch_widget_pool_managers()
        self._patch_di_container()
    
    def stop_patches(self):
        """Stop all active patches."""
        for patcher in self.active_patches:
            try:
                patcher.stop()
            except RuntimeError:
                pass  # Patch was already stopped
        self.active_patches.clear()
        self.mock_registry.clear()
    
    def _patch_data_cache_manager(self):
        """Patch DataCacheManager with proper mock."""
        from tests.fixtures.mock_configurations import DataCacheManagerMock
        
        # Patch the actual class
        patcher = patch(
            'application.services.data.cache_manager.DataCacheManager',
            DataCacheManagerMock
        )
        self.active_patches.append(patcher)
        mock = patcher.start()
        self.mock_registry['DataCacheManager'] = mock
    
    def _patch_section_managers(self):
        """Patch section managers with proper mocks."""
        from tests.fixtures.mock_configurations import SectionManagerMock
        
        # Patch OptionPickerSectionManager
        patcher = patch(
            'presentation.components.option_picker.components.option_picker_section_manager.OptionPickerSectionManager',
            SectionManagerMock
        )
        self.active_patches.append(patcher)
        mock = patcher.start()
        self.mock_registry['OptionPickerSectionManager'] = mock
    
    def _patch_widget_pool_managers(self):
        """Patch widget pool managers with proper mocks."""
        from tests.fixtures.mock_configurations import WidgetPoolManagerMock
        
        # Patch OptionPickerWidgetPoolManager
        patcher = patch(
            'presentation.components.option_picker.components.option_picker_widget_pool_manager.OptionPickerWidgetPoolManager',
            WidgetPoolManagerMock
        )
        self.active_patches.append(patcher)
        mock = patcher.start()
        self.mock_registry['OptionPickerWidgetPoolManager'] = mock
    
    def _patch_di_container(self):
        """Patch DI container with proper mock."""
        from tests.fixtures.mock_configurations import DIContainerMock
        
        # Patch DIContainer
        patcher = patch(
            'core.dependency_injection.di_container.DIContainer',
            DIContainerMock
        )
        self.active_patches.append(patcher)
        mock = patcher.start()
        self.mock_registry['DIContainer'] = mock


# Global patcher instance
_auto_patcher = AutoMockPatcher()


@pytest.fixture(scope="function")
def auto_mock_patches():
    """
    Fixture that automatically patches common problematic services.
    
    Use this fixture in tests that need automatic mock patching:
    
    def test_something(auto_mock_patches):
        # Common services are automatically mocked with proper iterables
        pass
    """
    _auto_patcher.start_patches()
    yield _auto_patcher.mock_registry
    _auto_patcher.stop_patches()


@pytest.fixture(scope="function") 
def mock_data_cache_manager():
    """Fixture providing a properly configured DataCacheManager mock."""
    from tests.fixtures.mock_configurations import DataCacheManagerMock
    return DataCacheManagerMock()


@pytest.fixture(scope="function")
def mock_section_manager():
    """Fixture providing a properly configured section manager mock."""
    from tests.fixtures.test_isolation import create_section_mock_with_pictographs
    return create_section_mock_with_pictographs()


@pytest.fixture(scope="function")
def mock_widget_pool_manager():
    """Fixture providing a properly configured widget pool manager mock."""
    from tests.fixtures.test_isolation import create_widget_pool_mock
    return create_widget_pool_mock()


@pytest.fixture(scope="function")
def mock_di_container():
    """Fixture providing a properly configured DI container mock."""
    from tests.fixtures.mock_configurations import DIContainerMock
    return DIContainerMock()


# Decorator for automatic mock configuration
def with_auto_mocks(test_func):
    """
    Decorator that automatically configures mocks in test functions.
    
    Usage:
        @with_auto_mocks
        def test_something():
            # Any Mock objects created in this test will be automatically configured
            pass
    """
    def wrapper(*args, **kwargs):
        # Start auto patches
        _auto_patcher.start_patches()
        
        try:
            result = test_func(*args, **kwargs)
        finally:
            # Stop auto patches
            _auto_patcher.stop_patches()
        
        return result
    
    return wrapper


# Utility functions for common mock patterns
def create_mock_sections_dict(section_count: int = 2) -> Dict[str, Mock]:
    """Create a dictionary of properly configured section mocks."""
    from tests.fixtures.test_isolation import create_section_mock_with_pictographs
    
    sections = {}
    for i in range(section_count):
        section_mock = create_section_mock_with_pictographs()
        sections[f"Type{i+1}"] = section_mock
    
    return sections


def create_mock_widget_pool_dict(widget_count: int = 5) -> Dict[int, Mock]:
    """Create a dictionary of properly configured widget mocks."""
    widgets = {}
    for i in range(widget_count):
        widget_mock = Mock()
        widget_mock.hide = Mock()
        widget_mock.show = Mock()
        widget_mock.isVisible = Mock(return_value=False)
        widgets[i] = widget_mock
    
    return widgets


def patch_mock_for_iteration(mock_obj: Mock, collection_attrs: List[str] = None):
    """
    Patch a mock object to support iteration operations.
    
    Args:
        mock_obj: Mock object to patch
        collection_attrs: List of attributes that should return collections
    """
    if collection_attrs is None:
        collection_attrs = ['values', 'keys', 'items']
    
    for attr in collection_attrs:
        if hasattr(mock_obj, attr):
            getattr(mock_obj, attr).return_value = []
    
    # Add iteration support
    mock_obj.__iter__ = Mock(return_value=iter([]))
    mock_obj.__len__ = Mock(return_value=0)
    mock_obj.__contains__ = Mock(return_value=False)


# Context manager for temporary mock patches
class TemporaryMockPatch:
    """Context manager for temporary mock patches."""
    
    def __init__(self, target: str, mock_class):
        self.target = target
        self.mock_class = mock_class
        self.patcher = None
        self.mock = None
    
    def __enter__(self):
        self.patcher = patch(self.target, self.mock_class)
        self.mock = self.patcher.start()
        return self.mock
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.patcher:
            self.patcher.stop()


# Convenience functions for specific service patches
def patch_data_cache_manager():
    """Context manager to patch DataCacheManager."""
    from tests.fixtures.mock_configurations import DataCacheManagerMock
    return TemporaryMockPatch(
        'application.services.data.cache_manager.DataCacheManager',
        DataCacheManagerMock
    )


def patch_section_manager():
    """Context manager to patch OptionPickerSectionManager."""
    from tests.fixtures.mock_configurations import SectionManagerMock
    return TemporaryMockPatch(
        'presentation.components.option_picker.components.option_picker_section_manager.OptionPickerSectionManager',
        SectionManagerMock
    )


def patch_widget_pool_manager():
    """Context manager to patch OptionPickerWidgetPoolManager."""
    from tests.fixtures.mock_configurations import WidgetPoolManagerMock
    return TemporaryMockPatch(
        'presentation.components.option_picker.components.option_picker_widget_pool_manager.OptionPickerWidgetPoolManager',
        WidgetPoolManagerMock
    )
