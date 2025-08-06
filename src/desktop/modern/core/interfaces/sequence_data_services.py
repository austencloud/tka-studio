"""
Sequence and Data Service Interfaces

Interface definitions for sequence and data services following TKA's clean architecture.
These interfaces define contracts for sequence operations, data management,
and transformation that must work identically across desktop and web platforms.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum
from typing import Any

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


class SequenceFormat(Enum):
    """Sequence data formats."""

    JSON = "json"
    XML = "xml"
    BINARY = "binary"


class ISequenceRepository(ABC):
    """Interface for sequence repository operations."""

    @abstractmethod
    def save_sequence(self, sequence: SequenceData, filepath: str) -> bool:
        """
        Save sequence data to file.

        Args:
            sequence: Sequence data to save
            filepath: Path to save to

        Returns:
            True if saved successfully, False otherwise

        Note:
            Web implementation: Uses browser storage or server API
        """

    @abstractmethod
    def load_sequence(self, filepath: str) -> SequenceData | None:
        """
        Load sequence data from file.

        Args:
            filepath: Path to load from

        Returns:
            Loaded sequence data or None if failed

        Note:
            Web implementation: Uses browser storage or server API
        """

    @abstractmethod
    def delete_sequence(self, filepath: str) -> bool:
        """
        Delete sequence file.

        Args:
            filepath: Path to delete

        Returns:
            True if deleted successfully, False otherwise

        Note:
            Web implementation: Uses browser storage or server API
        """

    @abstractmethod
    def list_sequences(self, directory: str = "") -> list[str]:
        """
        List available sequence files.

        Args:
            directory: Directory to list from (empty for default)

        Returns:
            List of sequence file paths

        Note:
            Web implementation: Lists from browser storage or server
        """

    @abstractmethod
    def get_sequence_metadata(self, filepath: str) -> dict[str, Any] | None:
        """
        Get metadata for a sequence file.

        Args:
            filepath: Path to get metadata for

        Returns:
            Metadata dictionary or None if not found

        Note:
            Web implementation: Metadata may be cached in browser storage
        """

    @abstractmethod
    def backup_sequence(self, filepath: str, backup_name: str) -> bool:
        """
        Create backup of sequence file.

        Args:
            filepath: Path to backup
            backup_name: Name for backup

        Returns:
            True if backup created successfully, False otherwise

        Note:
            Web implementation: Creates backup in browser storage
        """

    @abstractmethod
    def restore_sequence(self, backup_name: str, filepath: str) -> bool:
        """
        Restore sequence from backup.

        Args:
            backup_name: Name of backup to restore
            filepath: Path to restore to

        Returns:
            True if restored successfully, False otherwise

        Note:
            Web implementation: Restores from browser storage backup
        """

    @abstractmethod
    def get_recent_sequences(self, limit: int = 10) -> list[str]:
        """
        Get list of recently accessed sequences.

        Args:
            limit: Maximum number of sequences to return

        Returns:
            List of recent sequence file paths

        Note:
            Web implementation: Retrieved from browser storage history
        """


class ISequenceTransformer(ABC):
    """Interface for sequence transformation operations."""

    @abstractmethod
    def transform_sequence(
        self, sequence: SequenceData, transformation: str, parameters: dict[str, Any]
    ) -> SequenceData:
        """
        Transform sequence data.

        Args:
            sequence: Sequence data to transform
            transformation: Transformation type
            parameters: Transformation parameters

        Returns:
            Transformed sequence data

        Note:
            Web implementation: Same transformation logic across platforms
        """

    @abstractmethod
    def reverse_sequence(self, sequence: SequenceData) -> SequenceData:
        """
        Reverse sequence beat order.

        Args:
            sequence: Sequence data to reverse

        Returns:
            Reversed sequence data

        Note:
            Web implementation: Same logic across platforms
        """

    @abstractmethod
    def mirror_sequence(
        self, sequence: SequenceData, axis: str = "horizontal"
    ) -> SequenceData:
        """
        Mirror sequence across specified axis.

        Args:
            sequence: Sequence data to mirror
            axis: Axis to mirror across (horizontal/vertical)

        Returns:
            Mirrored sequence data

        Note:
            Web implementation: Same mirroring logic across platforms
        """

    @abstractmethod
    def scale_sequence(self, sequence: SequenceData, factor: float) -> SequenceData:
        """
        Scale sequence timing.

        Args:
            sequence: Sequence data to scale
            factor: Scaling factor

        Returns:
            Scaled sequence data

        Note:
            Web implementation: Same scaling logic across platforms
        """

    @abstractmethod
    def merge_sequences(
        self, sequences: list[SequenceData], merge_type: str = "concatenate"
    ) -> SequenceData:
        """
        Merge multiple sequences.

        Args:
            sequences: List of sequences to merge
            merge_type: Type of merge (concatenate/overlay/interleave)

        Returns:
            Merged sequence data

        Note:
            Web implementation: Same merging logic across platforms
        """

    @abstractmethod
    def split_sequence(
        self, sequence: SequenceData, split_points: list[int]
    ) -> list[SequenceData]:
        """
        Split sequence at specified points.

        Args:
            sequence: Sequence data to split
            split_points: List of beat indices to split at

        Returns:
            List of split sequence data

        Note:
            Web implementation: Same splitting logic across platforms
        """

    @abstractmethod
    def filter_beats(
        self, sequence: SequenceData, filter_criteria: dict[str, Any]
    ) -> SequenceData:
        """
        Filter beats based on criteria.

        Args:
            sequence: Sequence data to filter
            filter_criteria: Filtering criteria

        Returns:
            Filtered sequence data

        Note:
            Web implementation: Same filtering logic across platforms
        """

    @abstractmethod
    def get_available_transformations(self) -> list[str]:
        """
        Get list of available transformations.

        Returns:
            List of transformation names
        """


class IPictographDataManager(ABC):
    """Interface for pictograph data management operations."""

    @abstractmethod
    def get_pictograph_data(self, pictograph_id: str) -> dict[str, Any] | None:
        """
        Get pictograph data by ID.

        Args:
            pictograph_id: ID of pictograph to get

        Returns:
            Pictograph data dictionary or None if not found

        Note:
            Web implementation: Retrieved from browser storage or server
        """

    @abstractmethod
    def save_pictograph_data(self, pictograph_id: str, data: dict[str, Any]) -> bool:
        """
        Save pictograph data.

        Args:
            pictograph_id: ID of pictograph to save
            data: Pictograph data to save

        Returns:
            True if saved successfully, False otherwise

        Note:
            Web implementation: Saves to browser storage or server
        """

    @abstractmethod
    def delete_pictograph_data(self, pictograph_id: str) -> bool:
        """
        Delete pictograph data.

        Args:
            pictograph_id: ID of pictograph to delete

        Returns:
            True if deleted successfully, False otherwise

        Note:
            Web implementation: Deletes from browser storage or server
        """

    @abstractmethod
    def list_pictographs(self, category: str | None = None) -> list[str]:
        """
        List available pictographs.

        Args:
            category: Optional category filter

        Returns:
            List of pictograph IDs

        Note:
            Web implementation: Lists from browser storage or server
        """

    @abstractmethod
    def get_pictograph_metadata(self, pictograph_id: str) -> dict[str, Any] | None:
        """
        Get metadata for a pictograph.

        Args:
            pictograph_id: ID of pictograph to get metadata for

        Returns:
            Metadata dictionary or None if not found

        Note:
            Web implementation: Metadata may be cached in browser storage
        """

    @abstractmethod
    def search_pictographs(
        self, query: str, filters: dict[str, Any] | None = None
    ) -> list[str]:
        """
        Search pictographs by query.

        Args:
            query: Search query
            filters: Optional search filters

        Returns:
            List of matching pictograph IDs

        Note:
            Web implementation: May use client-side search or server API
        """

    @abstractmethod
    def get_pictograph_categories(self) -> list[str]:
        """
        Get list of pictograph categories.

        Returns:
            List of category names

        Note:
            Web implementation: Retrieved from browser storage or server
        """

    @abstractmethod
    def create_pictograph_category(self, category_name: str) -> bool:
        """
        Create new pictograph category.

        Args:
            category_name: Name of category to create

        Returns:
            True if created successfully, False otherwise

        Note:
            Web implementation: Creates in browser storage or server
        """


class IDataValidationService(ABC):
    """Interface for data validation operations."""

    @abstractmethod
    def validate_sequence_data(self, sequence: SequenceData) -> tuple[bool, list[str]]:
        """
        Validate sequence data.

        Args:
            sequence: Sequence data to validate

        Returns:
            Tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation logic across platforms
        """

    @abstractmethod
    def validate_beat_data(self, beat_data: BeatData) -> tuple[bool, list[str]]:
        """
        Validate beat data.

        Args:
            beat_data: Beat data to validate

        Returns:
            Tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation logic across platforms
        """

    @abstractmethod
    def validate_pictograph_data(
        self, pictograph_data: dict[str, Any]
    ) -> tuple[bool, list[str]]:
        """
        Validate pictograph data.

        Args:
            pictograph_data: Pictograph data to validate

        Returns:
            Tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation logic across platforms
        """

    @abstractmethod
    def validate_data_format(
        self, data: Any, format_type: str
    ) -> tuple[bool, list[str]]:
        """
        Validate data format.

        Args:
            data: Data to validate
            format_type: Expected format type

        Returns:
            Tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation logic across platforms
        """

    @abstractmethod
    def get_validation_schema(self, schema_type: str) -> dict[str, Any]:
        """
        Get validation schema.

        Args:
            schema_type: Type of schema to get

        Returns:
            Schema dictionary

        Note:
            Web implementation: Static schemas, can be shared configuration
        """

    @abstractmethod
    def register_custom_validator(
        self,
        validator_name: str,
        validator_func: Callable[[Any], tuple[bool, list[str]]],
    ) -> None:
        """
        Register custom validator function.

        Args:
            validator_name: Name of validator
            validator_func: Validator function

        Note:
            Web implementation: Custom validators stored in memory
        """

    @abstractmethod
    def get_available_validators(self) -> list[str]:
        """
        Get list of available validators.

        Returns:
            List of validator names
        """


class IDataExportService(ABC):
    """Interface for data export operations."""

    @abstractmethod
    def export_sequence(
        self, sequence: SequenceData, format_type: SequenceFormat, filepath: str
    ) -> bool:
        """
        Export sequence data.

        Args:
            sequence: Sequence data to export
            format_type: Export format
            filepath: Export file path

        Returns:
            True if exported successfully, False otherwise

        Note:
            Web implementation: Downloads file or saves to browser storage
        """

    @abstractmethod
    def export_beat_data(
        self, beat_data: BeatData, format_type: str, filepath: str
    ) -> bool:
        """
        Export beat data.

        Args:
            beat_data: Beat data to export
            format_type: Export format
            filepath: Export file path

        Returns:
            True if exported successfully, False otherwise

        Note:
            Web implementation: Downloads file or saves to browser storage
        """

    @abstractmethod
    def export_pictograph_data(
        self, pictograph_data: dict[str, Any], format_type: str, filepath: str
    ) -> bool:
        """
        Export pictograph data.

        Args:
            pictograph_data: Pictograph data to export
            format_type: Export format
            filepath: Export file path

        Returns:
            True if exported successfully, False otherwise

        Note:
            Web implementation: Downloads file or saves to browser storage
        """

    @abstractmethod
    def get_supported_formats(self) -> list[str]:
        """
        Get list of supported export formats.

        Returns:
            List of format names
        """

    @abstractmethod
    def get_format_options(self, format_type: str) -> dict[str, Any]:
        """
        Get options for export format.

        Args:
            format_type: Format to get options for

        Returns:
            Dictionary of format options
        """


class IDataImportService(ABC):
    """Interface for data import operations."""

    @abstractmethod
    def import_sequence(
        self, filepath: str, format_type: SequenceFormat
    ) -> SequenceData | None:
        """
        Import sequence data.

        Args:
            filepath: File path to import from
            format_type: Import format

        Returns:
            Imported sequence data or None if failed

        Note:
            Web implementation: Imports from file upload or browser storage
        """

    @abstractmethod
    def import_beat_data(self, filepath: str, format_type: str) -> BeatData | None:
        """
        Import beat data.

        Args:
            filepath: File path to import from
            format_type: Import format

        Returns:
            Imported beat data or None if failed

        Note:
            Web implementation: Imports from file upload or browser storage
        """

    @abstractmethod
    def import_pictograph_data(
        self, filepath: str, format_type: str
    ) -> dict[str, Any] | None:
        """
        Import pictograph data.

        Args:
            filepath: File path to import from
            format_type: Import format

        Returns:
            Imported pictograph data or None if failed

        Note:
            Web implementation: Imports from file upload or browser storage
        """

    @abstractmethod
    def get_supported_import_formats(self) -> list[str]:
        """
        Get list of supported import formats.

        Returns:
            List of format names
        """

    @abstractmethod
    def validate_import_file(
        self, filepath: str, format_type: str
    ) -> tuple[bool, list[str]]:
        """
        Validate import file.

        Args:
            filepath: File path to validate
            format_type: Expected format

        Returns:
            Tuple of (is_valid, error_messages)

        Note:
            Web implementation: Validates file upload or browser storage file
        """


class ISequenceLoader(ABC):
    """
    Interface for sequence loading operations.

    Handles sequence loading from persistence, startup restoration,
    and conversion between legacy and modern formats.
    """

    @abstractmethod
    def load_sequence_from_file(self, filepath: str) -> SequenceData | None:
        """
        Load sequence from file.

        Args:
            filepath: Path to sequence file

        Returns:
            Loaded sequence data, or None if failed
        """

    @abstractmethod
    def load_current_sequence(self) -> SequenceData | None:
        """
        Load the current sequence from default location.

        Returns:
            Current sequence data, or None if not found
        """


class ISequenceDictionaryManager(ABC):
    """
    Interface for sequence dictionary operations.

    Provides dictionary functionality for sequences including word calculation
    and difficulty assessment.
    """

    @abstractmethod
    def get_word_for_sequence(self, sequence: SequenceData) -> str | None:
        """
        Get word associated with sequence.

        Args:
            sequence: Sequence data

        Returns:
            Word string, or None if failed
        """

    @abstractmethod
    def calculate_difficulty(self, sequence: SequenceData) -> int:
        """
        Calculate sequence difficulty level.

        Args:
            sequence: Sequence data

        Returns:
            Difficulty level as integer
        """

    @abstractmethod
    def add_sequence_to_dictionary(self, sequence: SequenceData, word: str) -> bool:
        """
        Add sequence to dictionary.

        Args:
            sequence: Sequence data
            word: Associated word

        Returns:
            True if successfully added, False otherwise
        """


class ISequenceGenerator(ABC):
    """
    Interface for sequence generation operations.

    Handles sequence generation using various algorithms.
    """

    @abstractmethod
    def generate_sequence(
        self, sequence_type: Any, name: str, length: int = 16, **kwargs
    ) -> SequenceData:
        """
        Generate a sequence using the specified algorithm.

        Args:
            sequence_type: Type of sequence generation algorithm
            name: Name for the sequence
            length: Length of sequence
            **kwargs: Additional generation parameters

        Returns:
            Generated sequence data
        """


class ISequenceStartPositionManager(ABC):
    """
    Interface for sequence start position management.

    Handles start position operations and management.
    """

    @abstractmethod
    def set_start_position(self, start_position_beat_data: BeatData) -> None:
        """
        Set the start position.

        Args:
            start_position_beat_data: Beat data for start position
        """

    @abstractmethod
    def update_start_position_orientation(
        self, color: str, new_orientation: int
    ) -> None:
        """
        Update start position orientation.

        Args:
            color: Color identifier
            new_orientation: New orientation value
        """

    @abstractmethod
    def get_current_start_position(self) -> BeatData | None:
        """
        Get current start position.

        Returns:
            Current start position beat data, or None if not set
        """

    @abstractmethod
    def clear_start_position(self) -> None:
        """Clear the start position."""

    @abstractmethod
    def has_start_position(self) -> bool:
        """
        Check if sequence has start position.

        Returns:
            True if has start position, False otherwise
        """
