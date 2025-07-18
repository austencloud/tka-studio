"""
Browse Tab Domain Models

Simple data models that enhance legacy tuples minimally while maintaining compatibility.
Based on the Legacy code audit findings that show the legacy system uses simple tuples
and straightforward data structures.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

# Import existing SequenceData from domain models
# from ...domain.models.sequence_data import SequenceData


@dataclass
class BrowseState:
    """Browse state for persistence"""

    filter_type: Optional[str] = None
    filter_values: Optional[Any] = None
    selected_sequence: Optional[str] = None
    selected_variation: Optional[int] = None
    navigation_mode: str = "filter_selector"
    sort_method: str = "alphabetical"


class FilterType(Enum):
    """Replaces legacy string filter types"""

    STARTING_LETTER = "starting_letter"
    CONTAINS_LETTERS = "contains_letters"
    LENGTH = "length"  # Changed from SEQUENCE_LENGTH
    DIFFICULTY = "difficulty"  # Changed from DIFFICULTY_LEVEL
    STARTING_POSITION = "starting_position"
    AUTHOR = "author"
    GRID_MODE = "grid_mode"
    ALL_SEQUENCES = "all_sequences"
    FAVORITES = "favorites"
    RECENT = "recent"  # Changed from MOST_RECENT


class NavigationMode(Enum):
    """Replaces legacy mode strings"""

    FILTER_SELECTION = "filter_selector"
    SEQUENCE_BROWSER = "sequence_picker"


class SortMethod(Enum):
    """Replaces legacy sort method strings"""

    ALPHABETICAL = "alphabetical"
    DATE_ADDED = "date_added"
    DIFFICULTY_LEVEL = "level"
    SEQUENCE_LENGTH = "length"
    AUTHOR = "author"
    POPULARITY = "popularity"


class GridMode(Enum):
    """Replaces legacy grid mode strings"""

    DIAMOND = "diamond"
    BOX = "box"


class BrowseTabSection(Enum):
    """Direct port from legacy enum with validation"""

    FILTER_SELECTOR = "filter_selector"
    STARTING_LETTER = "starting_letter"
    CONTAINS_LETTERS = "contains_letters"
    SEQUENCE_LENGTH = "sequence_length"
    LEVEL = "level"
    STARTING_POSITION = "starting_position"
    AUTHOR = "author"
    GRID_MODE = "grid_mode"
    SEQUENCE_PICKER = "sequence_picker"


class SequenceActionType(Enum):
    """New enum for sequence actions"""

    EDIT_IN_CONSTRUCT = "edit_in_construct"
    TOGGLE_FAVORITE = "toggle_favorite"
    EXPORT_IMAGE = "export_image"
    DELETE_SEQUENCE = "delete_sequence"
    DELETE_VARIATION = "delete_variation"
    VIEW_METADATA = "view_metadata"
