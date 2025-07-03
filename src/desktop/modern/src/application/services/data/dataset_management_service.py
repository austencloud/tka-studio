"""
Dataset Management Service

Pure service for managing pictograph datasets and caching.
Extracted from PictographManagementService to follow single responsibility principle.

PROVIDES:
- In-memory dataset caching
- Category-based organization
- Search and filtering operations
- Dataset indexing
"""

from typing import List, Dict, Any, Optional, TypedDict
from abc import ABC, abstractmethod
import uuid

from domain.models.pictograph_models import PictographData


class PictographSearchQuery(TypedDict, total=False):
    """Type definition for pictograph search queries."""

    letter: Optional[str]
    motion_type: Optional[str]
    start_position: Optional[str]
    max_results: Optional[int]
    categories: Optional[List[str]]


class IDatasetManagementService(ABC):
    """Interface for dataset management operations."""

    @abstractmethod
    def add_to_dataset(
        self, pictograph: PictographData, category: str = "user_created"
    ) -> str:
        """Add pictograph to dataset."""

    @abstractmethod
    def search_dataset(self, query: PictographSearchQuery) -> List[PictographData]:
        """Search pictograph dataset with query."""

    @abstractmethod
    def get_dataset_categories(self) -> List[str]:
        """Get all available dataset categories."""

    @abstractmethod
    def get_pictographs_by_category(self, category: str) -> List[PictographData]:
        """Get all pictographs in a category."""


class DatasetManagementService(IDatasetManagementService):
    """
    Pure service for dataset management operations.

    Handles in-memory caching and organization without external dependencies.
    Uses immutable data patterns following TKA architecture.
    """

    def __init__(self):
        """Initialize dataset management service."""
        # Dataset management
        self._pictograph_cache: Dict[str, PictographData] = {}
        self._dataset_index: Dict[str, List[str]] = {}

    def add_to_dataset(
        self, pictograph: PictographData, category: str = "user_created"
    ) -> str:
        """Add pictograph to dataset."""
        pictograph_id = str(uuid.uuid4())

        # Cache the pictograph
        self._pictograph_cache[pictograph_id] = pictograph

        # Update dataset index
        if category not in self._dataset_index:
            self._dataset_index[category] = []
        self._dataset_index[category].append(pictograph_id)

        return pictograph_id

    def search_dataset(self, query: PictographSearchQuery) -> List[PictographData]:
        """Search pictograph dataset with query."""
        results = []

        # Extract search criteria with proper type handling
        max_results = query.get("max_results", 50)
        if max_results is None:
            max_results = 50

        # Search through cached pictographs
        for pictograph_id, pictograph in self._pictograph_cache.items():
            if self._matches_query(pictograph, query):
                results.append(pictograph)

                if len(results) >= max_results:
                    break

        return results

    def get_dataset_categories(self) -> List[str]:
        """Get all available dataset categories."""
        return list(self._dataset_index.keys())

    def get_pictographs_by_category(self, category: str) -> List[PictographData]:
        """Get all pictographs in a category."""
        pictograph_ids = self._dataset_index.get(category, [])
        return [
            self._pictograph_cache[pid]
            for pid in pictograph_ids
            if pid in self._pictograph_cache
        ]

    def get_pictograph_by_id(self, pictograph_id: str) -> Optional[PictographData]:
        """Get pictograph by ID."""
        return self._pictograph_cache.get(pictograph_id)

    def remove_from_dataset(self, pictograph_id: str) -> bool:
        """Remove pictograph from dataset."""
        if pictograph_id not in self._pictograph_cache:
            return False

        # Remove from cache
        del self._pictograph_cache[pictograph_id]

        # Remove from all category indices
        for category, ids in self._dataset_index.items():
            if pictograph_id in ids:
                ids.remove(pictograph_id)

        return True

    def update_pictograph(
        self, pictograph_id: str, updated_pictograph: PictographData
    ) -> bool:
        """Update pictograph in dataset."""
        if pictograph_id not in self._pictograph_cache:
            return False

        self._pictograph_cache[pictograph_id] = updated_pictograph
        return True

    def clear_dataset(self) -> None:
        """Clear all dataset data."""
        self._pictograph_cache.clear()
        self._dataset_index.clear()

    def get_dataset_stats(self) -> Dict[str, Any]:
        """Get dataset statistics."""
        total_pictographs = len(self._pictograph_cache)
        categories = self.get_dataset_categories()

        category_counts = {
            category: len(self._dataset_index[category]) for category in categories
        }

        return {
            "total_pictographs": total_pictographs,
            "total_categories": len(categories),
            "categories": categories,
            "category_counts": category_counts,
        }

    def _matches_query(
        self, pictograph: PictographData, query: PictographSearchQuery
    ) -> bool:
        """Check if pictograph matches search query."""
        # Letter matching
        if "letter" in query and query["letter"]:
            letter = pictograph.metadata.get("letter", "").lower()
            query_letter = query["letter"].lower()
            if query_letter not in letter:
                return False

        # Motion type matching
        if "motion_type" in query and query["motion_type"]:
            query_motion_type = query["motion_type"]
            has_matching_motion = False

            for arrow in pictograph.arrows.values():
                if (
                    arrow.motion_data
                    and arrow.motion_data.motion_type.value == query_motion_type
                ):
                    has_matching_motion = True
                    break

            if not has_matching_motion:
                return False

        # Start position matching
        if "start_position" in query and query["start_position"]:
            start_position = pictograph.start_position
            if not start_position or query["start_position"] not in start_position:
                return False

        # Category matching
        if "categories" in query and query["categories"]:
            pictograph_categories = pictograph.metadata.get("categories", [])
            if not any(cat in pictograph_categories for cat in query["categories"]):
                return False

        return True
