#!/usr/bin/env python3
"""
Centralized Mock Configurations for TKA Tests
=============================================

Provides reusable mock configurations that return proper data types
to prevent "Mock object is not iterable" errors across the test suite.
"""

from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock


class IterableMock(Mock):
    """Mock that returns proper iterable types for common operations."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configure common iterable operations
        self.values = Mock(return_value=[])
        self.keys = Mock(return_value=[])
        self.items = Mock(return_value=[])
        self.__iter__ = Mock(return_value=iter([]))
        self.__len__ = Mock(return_value=0)
        self.__contains__ = Mock(return_value=False)


class DataCacheManagerMock(IterableMock):
    """Mock for DataCacheManager that returns proper cache stats."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure get_cache_stats to return proper dictionary
        self.get_cache_stats.return_value = {
            "position_cache_size": 0,
            "sequence_cache_size": 0,
            "pictograph_cache_size": 0,
            "conversion_cache_size": 0,
            "total_items": 0,
            "max_size_per_cache": 100,
            "position_keys": [],
            "sequence_keys": [],
            "pictograph_keys": [],
            "conversion_keys": [],
        }

        # Configure cache operations
        self.get_position_cache.return_value = None
        self.get_sequence_cache.return_value = None
        self.get_pictograph_cache.return_value = None
        self.get_conversion_cache.return_value = None


class SectionManagerMock(IterableMock):
    """Mock for section managers that handle pictograph collections."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure pictographs as proper dictionary
        self.pictographs = {}
        self.pictographs.values = Mock(return_value=[])
        self.pictographs.keys = Mock(return_value=[])
        self.pictographs.items = Mock(return_value=[])

        # Configure methods that return collections
        self.get_all_pictograph_frames.return_value = []
        self.get_sections_with_content.return_value = []


class WidgetPoolManagerMock(IterableMock):
    """Mock for widget pool managers that handle widget collections."""

    def __init__(self, max_widgets: int = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create mock widgets
        self._mock_widgets = [Mock() for _ in range(max_widgets)]

        # Configure _widget_pool as proper dictionary
        self._widget_pool = {i: widget for i, widget in enumerate(self._mock_widgets)}
        self._widget_pool.values = Mock(return_value=self._mock_widgets)
        self._widget_pool.keys = Mock(return_value=list(range(max_widgets)))
        self._widget_pool.items = Mock(return_value=list(enumerate(self._mock_widgets)))

        # Configure methods
        self.get_widget_count.return_value = max_widgets
        self.get_widget_by_id.side_effect = lambda id: self._widget_pool.get(id)


class DIContainerMock(IterableMock):
    """Mock for DI container that handles service registrations."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure registrations as proper dictionary
        self._registrations = {}
        self.get_registrations.return_value = self._registrations

        # Configure resolve to return appropriate mocks
        def mock_resolve(interface):
            if hasattr(interface, "__name__"):
                name = interface.__name__
                if "DataCache" in name:
                    return DataCacheManagerMock()
                elif "Section" in name:
                    return SectionManagerMock()
                elif "Pool" in name:
                    return WidgetPoolManagerMock()
            return Mock()

        self.resolve.side_effect = mock_resolve


def create_mock_with_iterables(mock_class=Mock, **kwargs) -> Mock:
    """
    Create a mock with proper iterable configurations.

    Args:
        mock_class: Base mock class to use
        **kwargs: Additional configuration for the mock

    Returns:
        Configured mock with proper iterable support
    """
    mock = mock_class(**kwargs)

    # Ensure common iterable operations work
    if not hasattr(mock, "values") or isinstance(mock.values, Mock):
        mock.values = Mock(return_value=[])
    if not hasattr(mock, "keys") or isinstance(mock.keys, Mock):
        mock.keys = Mock(return_value=[])
    if not hasattr(mock, "items") or isinstance(mock.items, Mock):
        mock.items = Mock(return_value=[])

    return mock


def configure_section_mock(section_mock: Mock, pictographs: List[Mock] = None) -> Mock:
    """
    Configure a section mock with proper pictograph handling.

    Args:
        section_mock: Mock object to configure
        pictographs: List of mock pictograph objects

    Returns:
        Configured section mock
    """
    if pictographs is None:
        pictographs = []

    # Create a mock object that behaves like a dictionary but supports iteration
    pictographs_mock = Mock()
    pictographs_mock.values = Mock(return_value=pictographs)
    pictographs_mock.keys = Mock(
        return_value=[f"frame_{i}" for i in range(len(pictographs))]
    )
    pictographs_mock.items = Mock(
        return_value=[(f"frame_{i}", frame) for i, frame in enumerate(pictographs)]
    )
    pictographs_mock.__iter__ = Mock(return_value=iter(pictographs))
    pictographs_mock.__len__ = Mock(return_value=len(pictographs))
    pictographs_mock.__contains__ = Mock(return_value=True)

    section_mock.pictographs = pictographs_mock

    return section_mock


def configure_widget_pool_mock(pool_mock: Mock, widget_count: int = 5) -> Mock:
    """
    Configure a widget pool mock with proper widget handling.

    Args:
        pool_mock: Mock object to configure
        widget_count: Number of mock widgets to create

    Returns:
        Configured widget pool mock
    """
    # Create mock widgets
    mock_widgets = [Mock() for _ in range(widget_count)]
    for widget in mock_widgets:
        widget.hide = Mock()
        widget.show = Mock()
        widget.isVisible = Mock(return_value=False)

    # Create a mock object that behaves like a dictionary but supports iteration
    widget_pool_mock = Mock()
    widget_pool_mock.values = Mock(return_value=mock_widgets)
    widget_pool_mock.keys = Mock(return_value=list(range(widget_count)))
    widget_pool_mock.items = Mock(return_value=list(enumerate(mock_widgets)))
    widget_pool_mock.__iter__ = Mock(return_value=iter(mock_widgets))
    widget_pool_mock.__len__ = Mock(return_value=widget_count)
    widget_pool_mock.__contains__ = Mock(return_value=True)
    widget_pool_mock.get = Mock(
        side_effect=lambda id, default=None: (
            mock_widgets[id] if 0 <= id < widget_count else default
        )
    )

    pool_mock._widget_pool = widget_pool_mock

    # Configure methods
    pool_mock.get_widget_count.return_value = widget_count
    pool_mock.get_widget_by_id.side_effect = lambda id: (
        mock_widgets[id] if 0 <= id < widget_count else None
    )
    pool_mock.reset_pool = Mock()

    return pool_mock


# Global registry of mock configurations
MOCK_CONFIGURATIONS = {
    "DataCacheManager": DataCacheManagerMock,
    "SectionManager": SectionManagerMock,
    "WidgetPoolManager": WidgetPoolManagerMock,
    "DIContainer": DIContainerMock,
}


def get_configured_mock(service_name: str, **kwargs) -> Mock:
    """
    Get a pre-configured mock for a specific service.

    Args:
        service_name: Name of the service to mock
        **kwargs: Additional configuration parameters

    Returns:
        Configured mock object
    """
    mock_class = MOCK_CONFIGURATIONS.get(service_name, IterableMock)
    return mock_class(**kwargs)
