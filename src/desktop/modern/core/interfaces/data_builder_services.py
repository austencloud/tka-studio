"""
Data Builder and Factory Service Interfaces

Interface definitions for data building and factory services following TKA's clean architecture.
These interfaces complete the coverage for data building and factory operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import ElementalType, VTGMode
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)


class IBeatDataBuilder(ABC):
    """Interface for beat data building operations."""

    @abstractmethod
    def build_beat_data(self, beat_config: dict[str, Any]) -> Any:
        """
        Build beat data from configuration.

        Args:
            beat_config: Configuration dictionary for beat

        Returns:
            Beat data object

        Note:
            Web implementation: Creates beat data structure for client-side
        """

    @abstractmethod
    def validate_beat_config(self, beat_config: dict[str, Any]) -> bool:
        """
        Validate beat configuration.

        Args:
            beat_config: Configuration to validate

        Returns:
            True if configuration is valid
        """

    @abstractmethod
    def get_default_beat_config(self) -> dict[str, Any]:
        """
        Get default beat configuration.

        Returns:
            Default beat configuration dictionary
        """

    @abstractmethod
    def build_from_legacy_data(self, legacy_data: dict[str, Any]) -> Any:
        """
        Build beat data from legacy format.

        Args:
            legacy_data: Legacy beat data

        Returns:
            Modern beat data object
        """


class IPictographFactory(ABC):
    """Interface for pictograph factory operations."""

    @abstractmethod
    def create_pictograph(self, pictograph_type: str, config: dict[str, Any]) -> Any:
        """
        Create pictograph instance.

        Args:
            pictograph_type: Type of pictograph to create
            config: Configuration for pictograph

        Returns:
            Pictograph instance
        """

    @abstractmethod
    def get_available_types(self) -> list[str]:
        """
        Get available pictograph types.

        Returns:
            List of available pictograph types
        """

    @abstractmethod
    def validate_pictograph_config(
        self, pictograph_type: str, config: dict[str, Any]
    ) -> bool:
        """
        Validate pictograph configuration.

        Args:
            pictograph_type: Type of pictograph
            config: Configuration to validate

        Returns:
            True if configuration is valid
        """

    @abstractmethod
    def create_from_beat_data(self, beat_data: Any) -> Any:
        """
        Create pictograph from beat data.

        Args:
            beat_data: Beat data to convert

        Returns:
            Pictograph instance
        """


class IConversionUtils(ABC):
    """Interface for data conversion utility operations."""

    @abstractmethod
    def convert_coordinates(
        self, coords: tuple[float, float], from_system: str, to_system: str
    ) -> tuple[float, float]:
        """
        Convert coordinates between systems.

        Args:
            coords: (x, y) coordinates to convert
            from_system: Source coordinate system
            to_system: Target coordinate system

        Returns:
            Converted (x, y) coordinates
        """

    @abstractmethod
    def convert_color_format(self, color: str, from_format: str, to_format: str) -> str:
        """
        Convert color between formats.

        Args:
            color: Color value to convert
            from_format: Source format (hex, rgb, hsl, etc.)
            to_format: Target format

        Returns:
            Converted color value
        """

    @abstractmethod
    def convert_units(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert units between measurement systems.

        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit

        Returns:
            Converted value
        """

    @abstractmethod
    def normalize_data_format(self, data: Any, target_format: str) -> Any:
        """
        Normalize data to target format.

        Args:
            data: Data to normalize
            target_format: Target format specification

        Returns:
            Normalized data
        """


class IDatasetQuery(ABC):
    """Interface for dataset query operations."""

    @abstractmethod
    def query_pictographs(self, query_params: dict[str, Any]) -> list[Any]:
        """
        Query pictographs based on parameters.

        Args:
            query_params: Query parameters dictionary

        Returns:
            List of matching pictographs
        """

    @abstractmethod
    def filter_by_attributes(
        self, dataset: list[Any], attributes: dict[str, Any]
    ) -> list[Any]:
        """
        Filter dataset by attributes.

        Args:
            dataset: Dataset to filter
            attributes: Attributes to filter by

        Returns:
            Filtered dataset
        """

    @abstractmethod
    def sort_dataset(
        self, dataset: list[Any], sort_key: str, reverse: bool = False
    ) -> list[Any]:
        """
        Sort dataset by key.

        Args:
            dataset: Dataset to sort
            sort_key: Key to sort by
            reverse: Whether to reverse sort order

        Returns:
            Sorted dataset
        """

    @abstractmethod
    def search_text(self, dataset: list[Any], search_term: str) -> list[Any]:
        """
        Search dataset for text matches.

        Args:
            dataset: Dataset to search
            search_term: Text to search for

        Returns:
            Matching results
        """

    @abstractmethod
    def aggregate_data(
        self, dataset: list[Any], group_by: str, aggregation_func: str
    ) -> dict[str, Any]:
        """
        Aggregate dataset by grouping criteria.

        Args:
            dataset: Dataset to aggregate
            group_by: Field to group by
            aggregation_func: Aggregation function ('count', 'sum', 'avg', etc.)

        Returns:
            Aggregated results dictionary
        """

    @abstractmethod
    def apply_filters(
        self, dataset: list[Any], filters: list[dict[str, Any]]
    ) -> list[Any]:
        """
        Apply multiple filters to dataset.

        Args:
            dataset: Dataset to filter
            filters: List of filter configurations

        Returns:
            Filtered dataset
        """


class IPictographDataService(ABC):
    """Interface for pictograph data service operations."""

    @abstractmethod
    def get_pictograph_data(self, pictograph_id: str) -> Optional[Any]:
        """
        Get pictograph data by ID.

        Args:
            pictograph_id: Unique identifier for pictograph

        Returns:
            Pictograph data or None if not found

        Note:
            Web implementation: May load from server or local storage
        """

    @abstractmethod
    def get_pictograph_dataset(self) -> dict[str, list[dict[str, Any]]]:
        """
        Get the complete pictograph dataset for question generation.

        Returns:
            Dictionary mapping letters to lists of pictograph data dictionaries.
            Each pictograph data dictionary contains:
            - id: Unique identifier
            - letter: Associated letter
            - type: Type of pictograph ("real" or "mock")
            - data: PictographData object
            - beat_data: Optional BeatData object for real pictographs

        Note:
            Web implementation: May load from server or local storage
        """


class IPositionAttributeMapper(ABC):
    """Interface for position attribute mapping services."""

    @abstractmethod
    def map_position_attributes(self, position_data: dict[str, Any]) -> dict[str, Any]:
        """Map position attributes between formats."""

    @abstractmethod
    def validate_position_data(self, position_data: dict[str, Any]) -> bool:
        """Validate position data structure."""

    @abstractmethod
    def get_default_position_attributes(self) -> dict[str, Any]:
        """Get default position attributes."""


class IPositionResolver(ABC):
    """Interface for position resolution services."""

    @abstractmethod
    def resolve_position(self, position_key: str) -> Optional[Any]:
        """Resolve position from key."""

    @abstractmethod
    def get_valid_positions(self) -> list[str]:
        """Get list of valid position keys."""

    @abstractmethod
    def validate_position_key(self, position_key: str) -> bool:
        """Validate position key format."""


class IGlyphDataService(ABC):
    """Interface for glyph data services."""

    @abstractmethod
    def determine_glyph_data(self, pictograph_data: PictographData) -> None:
        """
        Determine glyph data from pictograph information.

        Note: This method no longer returns GlyphData as all glyph information
        is now computed directly from PictographData using utility functions.

        Args:
            pictograph_data: The pictograph data to analyze
        """

    @abstractmethod
    def determine_glyph_data_from_beat(self, beat_data: BeatData) -> None:
        """
        Backward compatibility method to determine glyph data from beat data.

        Note: This method no longer returns GlyphData as all glyph information
        is now computed directly from PictographData using utility functions.

        Args:
            beat_data: The beat data to analyze
        """

    @abstractmethod
    def _beat_data_to_pictograph_data(self, beat_data: BeatData) -> PictographData:
        """Convert BeatData to PictographData for glyph processing."""

    @abstractmethod
    def _determine_letter_type(self, letter: str) -> Optional[LetterType]:
        """Determine the letter type from the letter string."""

    @abstractmethod
    def _determine_vtg_mode(self, pictograph_data: PictographData) -> Optional[VTGMode]:
        """
        Determine VTG mode from motion data.

        This is a simplified implementation. The full logic is quite complex
        and involves grid mode checking, position analysis, etc.
        """

    @abstractmethod
    def _motions_same_direction(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Check if two motions are in the same direction."""

    @abstractmethod
    def _determine_timing(self, blue_motion: MotionData, red_motion: MotionData) -> str:
        """Determine if motions are split, together, or quarter pattern."""

    @abstractmethod
    def _vtg_to_elemental(self, vtg_mode: Optional[VTGMode]) -> Optional[ElementalType]:
        """Convert VTG mode to elemental type."""

    @abstractmethod
    def _determine_positions(
        self, pictograph_data: PictographData
    ) -> tuple[Optional[str], Optional[str]]:
        """Determine start and end positions from pictograph data."""
