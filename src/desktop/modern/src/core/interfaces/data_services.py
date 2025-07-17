"""
Data Service Interfaces

Interface definitions for data management services following TKA's clean architecture.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set


class IDataCacheManager(ABC):
    """Interface for data cache management operations."""

    @abstractmethod
    def get_position_cache(self, key: str) -> Optional[Any]:
        """
        Get item from position cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached value or None if not found
        """
        pass

    @abstractmethod
    def set_position_cache(self, key: str, value: Any) -> None:
        """
        Set item in position cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        pass

    @abstractmethod
    def get_sequence_cache(self, key: str) -> Optional[Any]:
        """
        Get item from sequence cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached value or None if not found
        """
        pass

    @abstractmethod
    def set_sequence_cache(self, key: str, value: Any) -> None:
        """
        Set item in sequence cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        pass

    @abstractmethod
    def get_pictograph_cache(self, key: str) -> Optional[Any]:
        """
        Get item from pictograph cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached value or None if not found
        """
        pass

    @abstractmethod
    def set_pictograph_cache(self, key: str, value: Any) -> None:
        """
        Set item in pictograph cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        pass

    @abstractmethod
    def get_conversion_cache(self, key: str) -> Optional[Any]:
        """
        Get item from conversion cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached value or None if not found
        """
        pass

    @abstractmethod
    def set_conversion_cache(self, key: str, value: Any) -> None:
        """
        Set item in conversion cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        pass

    @abstractmethod
    def clear_all(self) -> None:
        """Clear all caches."""
        pass

    @abstractmethod
    def clear_position_cache(self) -> None:
        """Clear only position cache."""
        pass

    @abstractmethod
    def clear_sequence_cache(self) -> None:
        """Clear only sequence cache."""
        pass

    @abstractmethod
    def clear_pictograph_cache(self) -> None:
        """Clear only pictograph cache."""
        pass

    @abstractmethod
    def clear_conversion_cache(self) -> None:
        """Clear only conversion cache."""
        pass

    @abstractmethod
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Return comprehensive cache statistics.

        Returns:
            Dictionary with cache sizes, hit rates, and other metrics
        """
        pass


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
        pass

    @abstractmethod
    def get_from_dataset(self, pictograph_id: str) -> Optional[Any]:
        """
        Get pictograph from dataset by ID.

        Args:
            pictograph_id: Unique identifier

        Returns:
            Pictograph data or None if not found
        """
        pass

    @abstractmethod
    def search_dataset(self, query: Any) -> List[Any]:
        """
        Search dataset with query.

        Args:
            query: Search query parameters

        Returns:
            List of matching pictographs
        """
        pass

    @abstractmethod
    def get_dataset_by_category(self, category: str) -> List[Any]:
        """
        Get all pictographs in a category.

        Args:
            category: Category name

        Returns:
            List of pictographs in category
        """
        pass

    @abstractmethod
    def get_all_categories(self) -> List[str]:
        """
        Get all available categories.

        Returns:
            List of category names
        """
        pass

    @abstractmethod
    def remove_from_dataset(self, pictograph_id: str) -> bool:
        """
        Remove pictograph from dataset.

        Args:
            pictograph_id: Unique identifier

        Returns:
            True if removed, False if not found
        """
        pass

    @abstractmethod
    def get_dataset_stats(self) -> Dict[str, Any]:
        """
        Get dataset statistics.

        Returns:
            Dictionary with dataset metrics
        """
        pass

    @abstractmethod
    def clear_dataset(self) -> None:
        """Clear entire dataset."""
        pass

    @abstractmethod
    def clear_category(self, category: str) -> bool:
        """
        Clear specific category.

        Args:
            category: Category name

        Returns:
            True if category existed and was cleared
        """
        pass


class ICsvReader(ABC):
    """Interface for CSV reading operations."""

    @abstractmethod
    def read_csv(self, file_path: str) -> Optional[List[Dict[str, Any]]]:
        """
        Read CSV file and return data.

        Args:
            file_path: Path to CSV file

        Returns:
            List of dictionaries representing CSV rows, or None if error
        """
        pass

    @abstractmethod
    def read_csv_with_headers(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Read CSV file with header processing.

        Args:
            file_path: Path to CSV file

        Returns:
            Dictionary with headers and data, or None if error
        """
        pass

    @abstractmethod
    def validate_csv_structure(
        self, file_path: str, expected_columns: List[str]
    ) -> bool:
        """
        Validate CSV file structure.

        Args:
            file_path: Path to CSV file
            expected_columns: List of expected column names

        Returns:
            True if structure is valid
        """
        pass


class IPositionResolver(ABC):
    """Interface for position resolution operations."""

    @abstractmethod
    def resolve_position(self, position_data: Dict[str, Any]) -> Optional[Any]:
        """
        Resolve position from position data.

        Args:
            position_data: Position data dictionary

        Returns:
            Resolved position object or None if cannot resolve
        """
        pass

    @abstractmethod
    def resolve_start_position(
        self, start_position_data: Dict[str, Any]
    ) -> Optional[Any]:
        """
        Resolve start position from data.

        Args:
            start_position_data: Start position data dictionary

        Returns:
            Resolved start position object or None if cannot resolve
        """
        pass

    @abstractmethod
    def resolve_end_position(self, end_position_data: Dict[str, Any]) -> Optional[Any]:
        """
        Resolve end position from data.

        Args:
            end_position_data: End position data dictionary

        Returns:
            Resolved end position object or None if cannot resolve
        """
        pass

    @abstractmethod
    def get_available_positions(self) -> List[str]:
        """
        Get list of available position identifiers.

        Returns:
            List of position identifiers
        """
        pass


class IPositionAttributeMapper(ABC):
    """Interface for position attribute mapping operations."""

    @abstractmethod
    def map_attributes(self, position_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map position attributes to standard format.

        Args:
            position_data: Raw position data

        Returns:
            Mapped position attributes
        """
        pass

    @abstractmethod
    def reverse_map_attributes(self, mapped_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reverse map attributes back to original format.

        Args:
            mapped_data: Mapped position data

        Returns:
            Original format position data
        """
        pass

    @abstractmethod
    def get_attribute_mapping(self) -> Dict[str, str]:
        """
        Get current attribute mapping configuration.

        Returns:
            Dictionary of attribute mappings
        """
        pass


class ILegacyToModernConverter(ABC):
    """Interface for legacy to modern data conversion."""

    @abstractmethod
    def convert_sequence(self, legacy_sequence: List[Dict[str, Any]]) -> Optional[Any]:
        """
        Convert legacy sequence to modern format.

        Args:
            legacy_sequence: Legacy sequence data

        Returns:
            Modern sequence object or None if conversion failed
        """
        pass

    @abstractmethod
    def convert_beat(self, legacy_beat: Dict[str, Any]) -> Optional[Any]:
        """
        Convert legacy beat to modern format.

        Args:
            legacy_beat: Legacy beat data

        Returns:
            Modern beat object or None if conversion failed
        """
        pass

    @abstractmethod
    def convert_pictograph(self, legacy_pictograph: Dict[str, Any]) -> Optional[Any]:
        """
        Convert legacy pictograph to modern format.

        Args:
            legacy_pictograph: Legacy pictograph data

        Returns:
            Modern pictograph object or None if conversion failed
        """
        pass


class IModernToLegacyConverter(ABC):
    """Interface for modern to legacy data conversion."""

    @abstractmethod
    def convert_sequence(self, modern_sequence: Any) -> Optional[List[Dict[str, Any]]]:
        """
        Convert modern sequence to legacy format.

        Args:
            modern_sequence: Modern sequence object

        Returns:
            Legacy sequence data or None if conversion failed
        """
        pass

    @abstractmethod
    def convert_beat(self, modern_beat: Any) -> Optional[Dict[str, Any]]:
        """
        Convert modern beat to legacy format.

        Args:
            modern_beat: Modern beat object

        Returns:
            Legacy beat data or None if conversion failed
        """
        pass

    @abstractmethod
    def convert_pictograph(self, modern_pictograph: Any) -> Optional[Dict[str, Any]]:
        """
        Convert modern pictograph to legacy format.

        Args:
            modern_pictograph: Modern pictograph object

        Returns:
            Legacy pictograph data or None if conversion failed
        """
        pass


class IDataManager(ABC):
    """Interface for core data operations."""

    @abstractmethod
    def load_diamond_dataset(self) -> Any:
        """Load diamond pictograph dataset with error handling."""
        pass

    @abstractmethod
    def load_box_dataset(self) -> Any:
        """Load box pictograph dataset with error handling."""
        pass

    @abstractmethod
    def load_combined_dataset(self) -> Any:
        """Load and combine both diamond and box datasets."""
        pass

    @abstractmethod
    def validate_data_files(self) -> Dict[str, Any]:
        """Validate data files and return status information."""
        pass

    @abstractmethod
    def get_data_config(self) -> Any:
        """Get the current data configuration."""
        pass

    @abstractmethod
    def reload_config(self, new_config: Any) -> None:
        """Reload with new configuration."""
        pass

    @abstractmethod
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get information about loaded datasets."""
        pass
