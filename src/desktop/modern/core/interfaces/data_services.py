"""
Data Service Interfaces

Interface definitions for data management services following TKA's clean architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IDataCacheManager(ABC):
    """Interface for data cache management operations."""

    @abstractmethod
    def get_position_cache(self, key: str) -> Any | None:
        """
        Get item from position cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached value or None if not found
        """

    @abstractmethod
    def set_position_cache(self, key: str, value: Any) -> None:
        """
        Set item in position cache.

        Args:
            key: Cache key
            value: Value to cache
        """

    @abstractmethod
    def get_sequence_cache(self, key: str) -> Any | None:
        """
        Get item from sequence cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached value or None if not found
        """

    @abstractmethod
    def set_sequence_cache(self, key: str, value: Any) -> None:
        """
        Set item in sequence cache.

        Args:
            key: Cache key
            value: Value to cache
        """

    @abstractmethod
    def get_pictograph_cache(self, key: str) -> Any | None:
        """
        Get item from pictograph cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached value or None if not found
        """

    @abstractmethod
    def set_pictograph_cache(self, key: str, value: Any) -> None:
        """
        Set item in pictograph cache.

        Args:
            key: Cache key
            value: Value to cache
        """

    @abstractmethod
    def get_conversion_cache(self, key: str) -> Any | None:
        """
        Get item from conversion cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached value or None if not found
        """

    @abstractmethod
    def set_conversion_cache(self, key: str, value: Any) -> None:
        """
        Set item in conversion cache.

        Args:
            key: Cache key
            value: Value to cache
        """

    @abstractmethod
    def clear_all(self) -> None:
        """Clear all caches."""

    @abstractmethod
    def clear_position_cache(self) -> None:
        """Clear only position cache."""

    @abstractmethod
    def clear_sequence_cache(self) -> None:
        """Clear only sequence cache."""

    @abstractmethod
    def clear_pictograph_cache(self) -> None:
        """Clear only pictograph cache."""

    @abstractmethod
    def clear_conversion_cache(self) -> None:
        """Clear only conversion cache."""

    @abstractmethod
    def get_cache_stats(self) -> dict[str, Any]:
        """
        Return comprehensive cache statistics.

        Returns:
            Dictionary with cache sizes, hit rates, and other metrics
        """


class IDatasetManager(ABC):
    """Interface for dataset management operations."""

    @abstractmethod
    def add_to_dataset(self, pictograph: Any, category: str = "user_created") -> str:
        """
        Add pictograph to dataset.

        Args:
            pictograph: Pictograph data to add
            category: Category for organization

        Returns:
            Unique identifier for the added pictograph
        """

    @abstractmethod
    def get_from_dataset(self, pictograph_id: str) -> Any | None:
        """
        Get pictograph from dataset by ID.

        Args:
            pictograph_id: Unique identifier

        Returns:
            Pictograph data or None if not found
        """

    @abstractmethod
    def search_dataset(self, query: Any) -> list[Any]:
        """
        Search dataset with query.

        Args:
            query: Search query parameters

        Returns:
            List of matching pictographs
        """

    @abstractmethod
    def get_dataset_by_category(self, category: str) -> list[Any]:
        """
        Get all pictographs in a category.

        Args:
            category: Category name

        Returns:
            List of pictographs in category
        """

    @abstractmethod
    def get_all_categories(self) -> list[str]:
        """
        Get all available categories.

        Returns:
            List of category names
        """

    @abstractmethod
    def remove_from_dataset(self, pictograph_id: str) -> bool:
        """
        Remove pictograph from dataset.

        Args:
            pictograph_id: Unique identifier

        Returns:
            True if removed, False if not found
        """

    @abstractmethod
    def get_dataset_stats(self) -> dict[str, Any]:
        """
        Get dataset statistics.

        Returns:
            Dictionary with dataset metrics
        """

    @abstractmethod
    def clear_dataset(self) -> None:
        """Clear entire dataset."""

    @abstractmethod
    def clear_category(self, category: str) -> bool:
        """
        Clear specific category.

        Args:
            category: Category name

        Returns:
            True if category existed and was cleared
        """


class ICsvReader(ABC):
    """Interface for CSV reading operations."""

    @abstractmethod
    def read_csv(self, file_path: str) -> list[dict[str, Any]] | None:
        """
        Read CSV file and return data.

        Args:
            file_path: Path to CSV file

        Returns:
            List of dictionaries representing CSV rows, or None if error
        """

    @abstractmethod
    def read_csv_with_headers(self, file_path: str) -> dict[str, Any] | None:
        """
        Read CSV file with header processing.

        Args:
            file_path: Path to CSV file

        Returns:
            Dictionary with headers and data, or None if error
        """

    @abstractmethod
    def validate_csv_structure(
        self, file_path: str, expected_columns: list[str]
    ) -> bool:
        """
        Validate CSV file structure.

        Args:
            file_path: Path to CSV file
            expected_columns: List of expected column names

        Returns:
            True if structure is valid
        """


class IPositionResolver(ABC):
    """Interface for position resolution operations."""

    @abstractmethod
    def resolve_position(self, position_data: dict[str, Any]) -> Any | None:
        """
        Resolve position from position data.

        Args:
            position_data: Position data dictionary

        Returns:
            Resolved position object or None if cannot resolve
        """

    @abstractmethod
    def resolve_start_position(
        self, start_position_data: dict[str, Any]
    ) -> Any | None:
        """
        Resolve start position from data.

        Args:
            start_position_data: Start position data dictionary

        Returns:
            Resolved start position object or None if cannot resolve
        """

    @abstractmethod
    def resolve_end_position(self, end_position_data: dict[str, Any]) -> Any | None:
        """
        Resolve end position from data.

        Args:
            end_position_data: End position data dictionary

        Returns:
            Resolved end position object or None if cannot resolve
        """

    @abstractmethod
    def get_available_positions(self) -> list[str]:
        """
        Get list of available position identifiers.

        Returns:
            List of position identifiers
        """


class IPositionAttributeMapper(ABC):
    """Interface for position attribute mapping operations."""

    @abstractmethod
    def map_attributes(self, position_data: dict[str, Any]) -> dict[str, Any]:
        """
        Map position attributes to standard format.

        Args:
            position_data: Raw position data

        Returns:
            Mapped position attributes
        """

    @abstractmethod
    def reverse_map_attributes(self, mapped_data: dict[str, Any]) -> dict[str, Any]:
        """
        Reverse map attributes back to original format.

        Args:
            mapped_data: Mapped position data

        Returns:
            Original format position data
        """

    @abstractmethod
    def get_attribute_mapping(self) -> dict[str, str]:
        """
        Get current attribute mapping configuration.

        Returns:
            Dictionary of attribute mappings
        """


class ILegacyToModernConverter(ABC):
    """Interface for legacy to modern data conversion."""

    @abstractmethod
    def convert_sequence(self, legacy_sequence: list[dict[str, Any]]) -> Any | None:
        """
        Convert legacy sequence to modern format.

        Args:
            legacy_sequence: Legacy sequence data

        Returns:
            Modern sequence object or None if conversion failed
        """

    @abstractmethod
    def convert_beat(self, legacy_beat: dict[str, Any]) -> Any | None:
        """
        Convert legacy beat to modern format.

        Args:
            legacy_beat: Legacy beat data

        Returns:
            Modern beat object or None if conversion failed
        """

    @abstractmethod
    def convert_pictograph(self, legacy_pictograph: dict[str, Any]) -> Any | None:
        """
        Convert legacy pictograph to modern format.

        Args:
            legacy_pictograph: Legacy pictograph data

        Returns:
            Modern pictograph object or None if conversion failed
        """


class IModernToLegacyConverter(ABC):
    """Interface for modern to legacy data conversion."""

    @abstractmethod
    def convert_beat_data_to_legacy_format(
        self, beat: Any, beat_number: int
    ) -> dict[str, Any] | None:
        """
        Convert modern BeatData to legacy format.

        Args:
            beat: Modern BeatData object
            beat_number: Beat number for legacy format

        Returns:
            Legacy beat data or None if conversion failed
        """

    @abstractmethod
    def convert_start_position_to_legacy_format(
        self, start_position_beat_data: Any
    ) -> dict[str, Any] | None:
        """
        Convert start position BeatData to legacy format.

        Args:
            start_position_beat_data: BeatData representing start position

        Returns:
            Legacy start position data or None if conversion failed
        """


class IDataManager(ABC):
    """Interface for core data operations."""

    @abstractmethod
    def load_diamond_dataset(self) -> Any:
        """Load diamond pictograph dataset with error handling."""

    @abstractmethod
    def load_box_dataset(self) -> Any:
        """Load box pictograph dataset with error handling."""

    @abstractmethod
    def load_combined_dataset(self) -> Any:
        """Load and combine both diamond and box datasets."""

    @abstractmethod
    def validate_data_files(self) -> dict[str, Any]:
        """Validate data files and return status information."""

    @abstractmethod
    def get_data_config(self) -> Any:
        """Get the current data configuration."""

    @abstractmethod
    def reload_config(self, new_config: Any) -> None:
        """Reload with new configuration."""

    @abstractmethod
    def get_dataset_info(self) -> dict[str, Any]:
        """Get information about loaded datasets."""
