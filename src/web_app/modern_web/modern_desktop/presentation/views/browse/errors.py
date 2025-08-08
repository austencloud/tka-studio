"""
Browse Tab Error Hierarchy

Consistent error handling for browse tab operations.

NOTE: These errors have been moved to the domain layer to avoid circular imports.
This file now imports from the domain layer.
"""

# Import from domain layer to avoid circular imports
from __future__ import annotations

from desktop.modern.domain.models.browse_errors import (
    BrowseError,
    DataLoadError,
    FilterError,
    NavigationError,
    StateError,
    ThumbnailError,
)


# Re-export for backward compatibility
__all__ = [
    "BrowseError",
    "DataLoadError",
    "FilterError",
    "NavigationError",
    "StateError",
    "ThumbnailError",
]
