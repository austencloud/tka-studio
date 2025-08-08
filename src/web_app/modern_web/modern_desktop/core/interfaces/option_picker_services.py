"""
Option Picker Service Interfaces

Interface definitions for option picker services following TKA's clean architecture.
These interfaces define contracts for option picker operations, configuration,
and state management that must work identically across desktop and web platforms.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional


class OptionType(Enum):
    """Option type enumeration."""

    POSITION = "position"
    MOTION = "motion"
    ARROW = "arrow"
    LETTER = "letter"


class IOptionConfigurationService(ABC):
    """Interface for option configuration service operations."""

    @abstractmethod
    def get_configuration(self, config_key: str) -> Optional[Any]:
        """
        Get configuration value by key.

        Args:
            config_key: Configuration key

        Returns:
            Configuration value or None if not found

        Note:
            Web implementation: Retrieved from browser storage or server config
        """

    @abstractmethod
    def set_configuration(self, config_key: str, value: Any) -> bool:
        """
        Set configuration value.

        Args:
            config_key: Configuration key
            value: Configuration value

        Returns:
            True if set successfully, False otherwise

        Note:
            Web implementation: Saves to browser storage or server config
        """

    @abstractmethod
    def get_all_configurations(self) -> dict[str, Any]:
        """
        Get all configuration values.

        Returns:
            dictionary of all configuration values

        Note:
            Web implementation: Retrieved from browser storage or server config
        """

    @abstractmethod
    def reset_configuration(self, config_key: str) -> bool:
        """
        Reset configuration to default value.

        Args:
            config_key: Configuration key to reset

        Returns:
            True if reset successfully, False otherwise

        Note:
            Web implementation: Resets to default and saves to storage
        """

    @abstractmethod
    def reset_all_configurations(self) -> bool:
        """
        Reset all configurations to default values.

        Returns:
            True if reset successfully, False otherwise

        Note:
            Web implementation: Resets all to defaults and saves to storage
        """

    @abstractmethod
    def export_configuration(self, filepath: str) -> bool:
        """
        Export configuration to file.

        Args:
            filepath: Path to export to

        Returns:
            True if exported successfully, False otherwise

        Note:
            Web implementation: Downloads configuration file
        """

    @abstractmethod
    def import_configuration(self, filepath: str) -> bool:
        """
        Import configuration from file.

        Args:
            filepath: Path to import from

        Returns:
            True if imported successfully, False otherwise

        Note:
            Web implementation: Loads from file upload
        """

    @abstractmethod
    def validate_configuration(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Validate configuration data.

        Args:
            config: Configuration data to validate

        Returns:
            tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation logic across platforms
        """


class IOptionLoader(ABC):
    """Interface for option loader operations."""

    @abstractmethod
    def load_options(self, option_type: OptionType) -> list[dict[str, Any]]:
        """
        Load options for a specific type.

        Args:
            option_type: Type of options to load

        Returns:
            list of option dictionaries

        Note:
            Web implementation: Loads from server or browser storage
        """

    @abstractmethod
    def load_filtered_options(
        self, option_type: OptionType, filters: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """
        Load filtered options for a specific type.

        Args:
            option_type: Type of options to load
            filters: Filters to apply

        Returns:
            list of filtered option dictionaries

        Note:
            Web implementation: Applies filters client-side or server-side
        """

    @abstractmethod
    def load_option_by_id(self, option_id: str) -> Optional[dict[str, Any]]:
        """
        Load specific option by ID.

        Args:
            option_id: ID of option to load

        Returns:
            Option dictionary or None if not found

        Note:
            Web implementation: Retrieved from server or browser storage
        """

    @abstractmethod
    def reload_options(self, option_type: OptionType) -> bool:
        """
        Reload options for a specific type.

        Args:
            option_type: Type of options to reload

        Returns:
            True if reloaded successfully, False otherwise

        Note:
            Web implementation: Refreshes from server or reprocesses data
        """

    @abstractmethod
    def get_option_count(self, option_type: OptionType) -> int:
        """
        Get count of options for a specific type.

        Args:
            option_type: Type of options to count

        Returns:
            Number of options

        Note:
            Web implementation: Retrieved from server or browser storage
        """

    @abstractmethod
    def cache_options(
        self, option_type: OptionType, options: list[dict[str, Any]]
    ) -> bool:
        """
        Cache options for a specific type.

        Args:
            option_type: Type of options to cache
            options: Options to cache

        Returns:
            True if cached successfully, False otherwise

        Note:
            Web implementation: Caches in browser storage
        """


class IOptionOrientationUpdater(ABC):
    """Interface for option orientation updater operations."""

    @abstractmethod
    def update_orientation(self, option_id: str, orientation: float) -> bool:
        """
        Update orientation for an option.

        Args:
            option_id: ID of option to update
            orientation: New orientation value

        Returns:
            True if updated successfully, False otherwise

        Note:
            Web implementation: Updates in browser storage or server
        """


class IOptionProvider(ABC):
    """Interface for option provider operations."""

    @abstractmethod
    def get_available_options(self, option_type: OptionType) -> list[dict[str, Any]]:
        """
        Get available options for a specific type.

        Args:
            option_type: Type of options to retrieve

        Returns:
            list of available option dictionaries

        Note:
            Web implementation: Retrieved from server or browser storage
        """

    @abstractmethod
    def get_option_details(self, option_id: str) -> Optional[dict[str, Any]]:
        """
        Get detailed information for a specific option.

        Args:
            option_id: ID of option to get details for

        Returns:
            Option details dictionary or None if not found

        Note:
            Web implementation: Retrieved from server or browser storage
        """

    @abstractmethod
    def filter_options(
        self, options: list[dict[str, Any]], filters: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """
        Filter options based on criteria.

        Args:
            options: list of options to filter
            filters: Filter criteria

        Returns:
            Filtered list of options

        Note:
            Web implementation: Client-side filtering for performance
        """

    @abstractmethod
    def sort_options(
        self, options: list[dict[str, Any]], sort_key: str, reverse: bool = False
    ) -> list[dict[str, Any]]:
        """
        Sort options by a key.

        Args:
            options: list of options to sort
            sort_key: Key to sort by
            reverse: Whether to reverse sort order

        Returns:
            Sorted list of options

        Note:
            Web implementation: Client-side sorting for performance
        """

    @abstractmethod
    def search_options(
        self, query: str, option_type: OptionType
    ) -> list[dict[str, Any]]:
        """
        Search options by query.

        Args:
            query: Search query string
            option_type: Type of options to search

        Returns:
            list of matching options

        Note:
            Web implementation: Client-side search with fuzzy matching
        """

    @abstractmethod
    def get_option_preview(self, option_id: str) -> Optional[Any]:
        """
        Get preview representation of an option.

        Args:
            option_id: ID of option to preview

        Returns:
            Preview representation or None if not available

        Note:
            Web implementation: Canvas/SVG preview generation
        """

    @abstractmethod
    def validate_option(self, option_data: dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Validate option data.

        Args:
            option_data: Option data to validate

        Returns:
            tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation logic across platforms
        """


class ISequenceOptionService(ABC):
    """Interface for sequence option service operations."""

    @abstractmethod
    def get_sequence_options(self, sequence_id: str) -> list[dict[str, Any]]:
        """
        Get options available for a specific sequence.

        Args:
            sequence_id: ID of sequence to get options for

        Returns:
            list of available options for the sequence

        Note:
            Web implementation: Retrieved from server or calculated client-side
        """

    @abstractmethod
    def apply_option_to_sequence(self, sequence_id: str, option_id: str) -> bool:
        """
        Apply an option to a sequence.

        Args:
            sequence_id: ID of sequence to modify
            option_id: ID of option to apply

        Returns:
            True if applied successfully, False otherwise

        Note:
            Web implementation: Updates sequence in browser storage or server
        """

    @abstractmethod
    def get_compatible_options(
        self, sequence_id: str, position: int
    ) -> list[dict[str, Any]]:
        """
        Get options compatible with a specific position in sequence.

        Args:
            sequence_id: ID of sequence
            position: Position in sequence

        Returns:
            list of compatible options

        Note:
            Web implementation: Compatibility checking client-side
        """

    @abstractmethod
    def validate_option_compatibility(
        self, sequence_id: str, option_id: str, position: int
    ) -> tuple[bool, list[str]]:
        """
        Validate option compatibility with sequence.

        Args:
            sequence_id: ID of sequence
            option_id: ID of option
            position: Position in sequence

        Returns:
            tuple of (is_compatible, incompatibility_reasons)

        Note:
            Web implementation: Same compatibility logic across platforms
        """

    @abstractmethod
    def get_next_recommended_options(self, sequence_id: str) -> list[dict[str, Any]]:
        """
        Get recommended next options for a sequence.

        Args:
            sequence_id: ID of sequence

        Returns:
            list of recommended options

        Note:
            Web implementation: Recommendation algorithm client-side
        """

    @abstractmethod
    def analyze_sequence_patterns(self, sequence_id: str) -> dict[str, Any]:
        """
        Analyze patterns in a sequence to suggest options.

        Args:
            sequence_id: ID of sequence to analyze

        Returns:
            dictionary of pattern analysis results

        Note:
            Web implementation: Pattern analysis client-side
        """


class IOptionPickerSizeCalculator(ABC):
    """Interface for option picker size calculator operations."""

    @abstractmethod
    def calculate_picker_size(self, container_size: tuple[int, int]) -> tuple[int, int]:
        """
        Calculate option picker size based on container.

        Args:
            container_size: Container size (width, height)

        Returns:
            Calculated picker size (width, height)

        Note:
            Web implementation: Uses viewport dimensions and CSS calculations
        """

    @abstractmethod
    def calculate_option_size(
        self, picker_size: tuple[int, int], option_count: int
    ) -> tuple[int, int]:
        """
        Calculate individual option size.

        Args:
            picker_size: Picker size (width, height)
            option_count: Number of options

        Returns:
            Calculated option size (width, height)

        Note:
            Web implementation: Uses CSS grid or flex calculations
        """

    @abstractmethod
    def calculate_grid_dimensions(
        self, option_count: int, picker_size: tuple[int, int]
    ) -> tuple[int, int]:
        """
        Calculate grid dimensions for options.

        Args:
            option_count: Number of options
            picker_size: Picker size (width, height)

        Returns:
            Grid dimensions (columns, rows)

        Note:
            Web implementation: Uses CSS grid calculations
        """

    @abstractmethod
    def get_minimum_picker_size(self) -> tuple[int, int]:
        """
        Get minimum picker size.

        Returns:
            Minimum picker size (width, height)

        Note:
            Web implementation: Uses CSS min-width/min-height values
        """

    @abstractmethod
    def get_maximum_picker_size(self) -> tuple[int, int]:
        """
        Get maximum picker size.

        Returns:
            Maximum picker size (width, height)

        Note:
            Web implementation: Uses CSS max-width/max-height values
        """


class IPositionMatcher(ABC):
    """Interface for position matcher operations."""

    @abstractmethod
    def match_position(self, position_data: dict[str, Any]) -> Optional[str]:
        """
        Match position data to a position ID.

        Args:
            position_data: Position data to match

        Returns:
            Position ID or None if no match

        Note:
            Web implementation: Same matching logic across platforms
        """

    @abstractmethod
    def get_matching_positions(self, criteria: dict[str, Any]) -> list[str]:
        """
        Get positions matching criteria.

        Args:
            criteria: Matching criteria

        Returns:
            list of matching position IDs

        Note:
            Web implementation: Same matching logic across platforms
        """

    @abstractmethod
    def get_position_similarity(self, position1: str, position2: str) -> float:
        """
        Get similarity score between two positions.

        Args:
            position1: First position ID
            position2: Second position ID

        Returns:
            Similarity score (0.0 to 1.0)

        Note:
            Web implementation: Same similarity calculation across platforms
        """

    @abstractmethod
    def update_position_mapping(
        self, position_id: str, position_data: dict[str, Any]
    ) -> bool:
        """
        Update position mapping.

        Args:
            position_id: Position ID to update
            position_data: New position data

        Returns:
            True if updated successfully, False otherwise

        Note:
            Web implementation: Updates in browser storage or server
        """
