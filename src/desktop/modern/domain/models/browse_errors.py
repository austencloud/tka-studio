"""
Browse Domain Errors

Error hierarchy for browse functionality, moved here to avoid circular imports
between application services and presentation layers.
"""

from __future__ import annotations


class BrowseError(Exception):
    """Base exception for browse tab operations."""


class DataLoadError(BrowseError):
    """Error loading sequence data from disk or database."""


class FilterError(BrowseError):
    """Error applying filters to sequence data."""


class StateError(BrowseError):
    """Error with state management or persistence."""


class ThumbnailError(BrowseError):
    """Error creating or loading sequence thumbnails."""


class NavigationError(BrowseError):
    """Error with panel navigation or UI state transitions."""
