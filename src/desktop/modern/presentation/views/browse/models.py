"""
Browse Tab Domain Models

Simple data models that enhance legacy tuples minimally while maintaining compatibility.
Based on the Legacy code audit findings that show the legacy system uses simple tuples
and straightforward data structures.

NOTE: These models have been moved to the domain layer to avoid circular imports.
This file now imports from the domain layer.
"""

# Import from domain layer to avoid circular imports
# Additional enums specific to presentation layer
from __future__ import annotations

from enum import Enum

from desktop.modern.domain.models.browse_models import (
    # Legacy compatibility aliases
    FILTER_TYPES,
    NAVIGATION_MODES,
    SORT_METHODS,
    BrowseState,
    BrowseTabSection,
    FilterType,
    GridMode,
    NavigationMode,
    SortMethod,
)


class SequenceActionType(Enum):
    """New enum for sequence actions"""

    EDIT_IN_CONSTRUCT = "edit_in_construct"
    TOGGLE_FAVORITE = "toggle_favorite"
    EXPORT_IMAGE = "export_image"
    DELETE_SEQUENCE = "delete_sequence"
    DELETE_VARIATION = "delete_variation"
    VIEW_METADATA = "view_metadata"


# Re-export domain models for backward compatibility
__all__ = [
    "BrowseState",
    "BrowseTabSection",
    "FilterType",
    "GridMode",
    "NavigationMode",
    "SortMethod",
    "SequenceActionType",
    # Legacy compatibility aliases
    "FILTER_TYPES",
    "NAVIGATION_MODES",
    "SORT_METHODS",
]
