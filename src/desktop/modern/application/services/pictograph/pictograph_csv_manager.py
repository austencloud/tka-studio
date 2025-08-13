"""
Pictograph Management Service

Consolidated pictograph management service that handles all pictograph-related
operations including creation, updates, dataset management, and data conversion.

REPLACES AND CONSOLIDATES:
- Various pictograph service wrappers
- Fragmented pictograph logic across multiple files

PROVIDES:
- Unified pictograph management interface
- Dataset operations and querying
- V1 to Modern data conversion
- Context-aware pictograph configuration
- CSV data loading and pictograph creation
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypedDict

import pandas as pd

from desktop.modern.domain.models.pictograph_data import PictographData


class IPictographCSVManager(ABC):
    """Interface for pictograph CSV management services."""

    @abstractmethod
    def _load_csv_data(self) -> pd.DataFrame:
        """Load CSV data if not already loaded."""


class PictographSearchQuery(TypedDict, total=False):
    """Type definition for pictograph search queries."""

    letter: str | None
    motion_type: str | None
    start_position: str | None
    max_results: int | None
    categories: list[str] | None


class PictographCSVManager(IPictographCSVManager):
    """
    Unified pictograph management service consolidating all pictograph operations.

    Provides comprehensive pictograph management including:
    - Pictograph creation and manipulation
    - Dataset management and querying
    - Data conversion between V1 and Modern formats
    - Context-aware configuration
    - Glyph data handling
    """

    def __init__(self):
        self._pictograph_cache: dict[str, PictographData] = {}
        self._dataset_index: dict[str, list[str]] = {}

        self._csv_data = None

        try:
            from desktop.modern.infrastructure.path_resolver import path_resolver

            self._data_path = path_resolver.get_data_path(
                "DiamondPictographDataframe.csv"
            )
        except Exception as e:
            print(f"Warning: Could not use centralized path resolver: {e}")
            # Fallback to manual discovery
            current_path = Path(__file__).resolve().parent
            data_path = None

            # First, try to find desktop/data directory
            while current_path.parent != current_path:
                if current_path.name == "desktop":
                    candidate = current_path / "data" / "DiamondPictographDataframe.csv"
                    if candidate.exists():
                        data_path = candidate
                        break
                current_path = current_path.parent

            # Fallback to old path method if desktop data not found
            if data_path is None:
                data_path = (
                    Path(__file__).parent.parent.parent.parent.parent.parent
                    / "data"
                    / "DiamondPictographDataframe.csv"
                )

            self._data_path = data_path

    def _load_csv_data(self) -> pd.DataFrame:
        """Load CSV data if not already loaded."""
        if self._csv_data is None:
            self._csv_data = pd.read_csv(self._data_path)
        return self._csv_data

    def _matches_query(
        self, pictograph: PictographData, query: PictographSearchQuery
    ) -> bool:
        """Check if pictograph matches search query."""
        if "letter" in query:
            letter = pictograph.letter
            query_letter = query["letter"].lower()
            if query_letter not in letter:
                return False

        # Motion type matching
        if "motion_type" in query:
            query_motion_type = query["motion_type"]
            has_matching_motion = False

            for arrow in pictograph.arrows.values():
                if (
                    arrow
                    and pictograph.motions[arrow.color].motion_type == query_motion_type
                ):
                    has_matching_motion = True
                    break

            if not has_matching_motion:
                return False

        return True
