"""
Browse Tab Error Hierarchy

Consistent error handling for browse tab operations.
"""


class BrowseError(Exception):
    """Base exception for browse tab operations."""
    pass


class DataLoadError(BrowseError):
    """Error loading sequence data from disk or database."""
    pass


class FilterError(BrowseError):
    """Error applying filters to sequence data."""
    pass


class StateError(BrowseError):
    """Error with state management or persistence."""
    pass


class ThumbnailError(BrowseError):
    """Error creating or loading sequence thumbnails."""
    pass


class NavigationError(BrowseError):
    """Error with panel navigation or UI state transitions."""
    pass
