"""
Browse Domain Models

Domain models for browse functionality, moved here to avoid circular imports
between application services and presentation layers.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


@dataclass
class BrowseState:
    """Browse state for persistence"""

    filter_type: str | None = None
    filter_values: Any | None = None
    selected_sequence: str | None = None
    selected_variation: int | None = None
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
    ALL_SEQUENCES = "all_sequences"
    FAVORITES = "favorites"
    RECENT = "recent"


# Legacy compatibility aliases
FILTER_TYPES = FilterType
NAVIGATION_MODES = NavigationMode
SORT_METHODS = SortMethod
