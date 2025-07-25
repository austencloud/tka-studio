"""
Data Builder and Factory Service Interfaces

Interface definitions for data building and factory services following TKA's clean architecture.
These interfaces complete the coverage for data building and factory operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from domain.models.beat_data import BeatData
from domain.models.enums import ElementalType, VTGMode
from domain.models.motion_data import MotionData
from domain.models.pictograph_data import PictographData
from presentation.components.option_picker.types.letter_types import LetterType


class IBeatDataBuilder(ABC):
    """Interface for beat data building operations."""

    @abstractmethod
    def build_beat_data(self, beat_config: Dict[str, Any]) -> Any:
        """
        Build beat data from configuration.

        Args:
            beat_config: Configuration dictionary for beat

        Returns:
            Beat data object

        Note:
            Web implementation: Creates beat data structure for client-side
        """
        pass

    @abstractmethod
    def validate_beat_config(self, beat_config: Dict[str, Any]) -> bool:
        """
        Validate beat configuration.

        Args:
            beat_config: Configuration to validate

        Returns:
            True if configuration is valid
        """
        pass

    @abstractmethod
    def get_default_beat_config(self) -> Dict[str, Any]:
        """
        Get default beat configuration.

        Returns:
            Default beat configuration dictionary
        """
        pass

    @abstractmethod
    def build_from_legacy_data(self, legacy_data: Dict[str, Any]) -> Any:
        """
        Build beat data from legacy format.

        Args:
            legacy_data: Legacy beat data

        Returns:
            Modern beat data object
        """
        pass


class IPictographFactory(ABC):
    """Interface for pictograph factory operations."""

    @abstractmethod
    def create_pictograph(self, pictograph_type: str, config: Dict[str, Any]) -> Any:
        """
        Create pictograph instance.

        Args:
            pictograph_type: Type of pictograph to create
            config: Configuration for pictograph

        Returns:
            Pictograph instance
        """
        pass

    @abstractmethod
    def get_available_types(self) -> List[str]:
        """
        Get available pictograph types.

        Returns:
            List of available pictograph types
        """
        pass

    @abstractmethod
    def validate_pictograph_config(
        self, pictograph_type: str, config: Dict[str, Any]
    ) -> bool:
        """
        Validate pictograph configuration.

        Args:
            pictograph_type: Type of pictograph
            config: Configuration to validate

        Returns:
            True if configuration is valid
        """
        pass

    @abstractmethod
    def create_from_beat_data(self, beat_data: Any) -> Any:
        """
        Create pictograph from beat data.

        Args:
            beat_data: Beat data to convert

        Returns:
            Pictograph instance
        """
        pass


class IConversionUtils(ABC):
    """Interface for data conversion utility operations."""

    @abstractmethod
    def convert_coordinates(
        self, coords: Tuple[float, float], from_system: str, to_system: str
    ) -> Tuple[float, float]:
        """
        Convert coordinates between systems.

        Args:
            coords: (x, y) coordinates to convert
            from_system: Source coordinate system
            to_system: Target coordinate system

        Returns:
            Converted (x, y) coordinates
        """
        pass

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
        pass

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
        pass

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
        pass


class IDatasetQuery(ABC):
    """Interface for dataset query operations."""

    @abstractmethod
    def query_pictographs(self, query_params: Dict[str, Any]) -> List[Any]:
        """
        Query pictographs based on parameters.

        Args:
            query_params: Query parameters dictionary

        Returns:
            List of matching pictographs
        """
        pass

    @abstractmethod
    def filter_by_attributes(
        self, dataset: List[Any], attributes: Dict[str, Any]
    ) -> List[Any]:
        """
        Filter dataset by attributes.

        Args:
            dataset: Dataset to filter
            attributes: Attributes to filter by

        Returns:
            Filtered dataset
        """
        pass

    @abstractmethod
    def sort_dataset(
        self, dataset: List[Any], sort_key: str, reverse: bool = False
    ) -> List[Any]:
        """
        Sort dataset by key.

        Args:
            dataset: Dataset to sort
            sort_key: Key to sort by
            reverse: Whether to reverse sort order

        Returns:
            Sorted dataset
        """
        pass

    @abstractmethod
    def search_text(self, dataset: List[Any], search_term: str) -> List[Any]:
        """
        Search dataset for text matches.

        Args:
            dataset: Dataset to search
            search_term: Text to search for

        Returns:
            Matching results
        """
        pass

    @abstractmethod
    def aggregate_data(
        self, dataset: List[Any], group_by: str, aggregation_func: str
    ) -> Dict[str, Any]:
        """
        Aggregate dataset by grouping criteria.

        Args:
            dataset: Dataset to aggregate
            group_by: Field to group by
            aggregation_func: Aggregation function ('count', 'sum', 'avg', etc.)

        Returns:
            Aggregated results dictionary
        """
        pass

    @abstractmethod
    def apply_filters(
        self, dataset: List[Any], filters: List[Dict[str, Any]]
    ) -> List[Any]:
        """
        Apply multiple filters to dataset.

        Args:
            dataset: Dataset to filter
            filters: List of filter configurations

        Returns:
            Filtered dataset
        """
        pass


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
        pass

    @abstractmethod
    def save_pictograph_data(self, pictograph_id: str, data: Any) -> bool:
        """
        Save pictograph data.

        Args:
            pictograph_id: Unique identifier for pictograph
            data: Pictograph data to save

        Returns:
            True if saved successfully

        Note:
            Web implementation: May save to server or local storage
        """
        pass

    @abstractmethod
    def delete_pictograph_data(self, pictograph_id: str) -> bool:
        """
        Delete pictograph data.

        Args:
            pictograph_id: Unique identifier for pictograph

        Returns:
            True if deleted successfully

        Note:
            Web implementation: Removes from server or local storage
        """
        pass

    @abstractmethod
    def list_pictograph_ids(self) -> List[str]:
        """
        List all pictograph IDs.

        Returns:
            List of pictograph identifiers

        Note:
            Web implementation: Retrieved from server or local storage
        """
        pass

    @abstractmethod
    def search_pictographs(self, search_criteria: Dict[str, Any]) -> List[Any]:
        """
        Search pictographs by criteria.

        Args:
            search_criteria: Search criteria dictionary

        Returns:
            List of matching pictographs

        Note:
            Web implementation: May search server-side or client-side
        """
        pass

    @abstractmethod
    def validate_pictograph_data(self, data: Any) -> Tuple[bool, List[str]]:
        """
        Validate pictograph data.

        Args:
            data: Pictograph data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        pass

    @abstractmethod
    def get_pictograph_metadata(self, pictograph_id: str) -> Optional[Dict[str, Any]]:
        """
        Get pictograph metadata.

        Args:
            pictograph_id: Unique identifier for pictograph

        Returns:
            Metadata dictionary or None if not found

        Note:
            Web implementation: Lightweight metadata for quick access
        """
        pass

    @abstractmethod
    def update_pictograph_metadata(
        self, pictograph_id: str, metadata: Dict[str, Any]
    ) -> bool:
        """
        Update pictograph metadata.

        Args:
            pictograph_id: Unique identifier for pictograph
            metadata: Metadata to update

        Returns:
            True if updated successfully

        Note:
            Web implementation: Updates cached metadata
        """
        pass


class IPositionAttributeMapper(ABC):
    """Interface for position attribute mapping services."""

    @abstractmethod
    def map_position_attributes(self, position_data: Dict[str, Any]) -> Dict[str, Any]:
        """Map position attributes between formats."""
        pass

    @abstractmethod
    def validate_position_data(self, position_data: Dict[str, Any]) -> bool:
        """Validate position data structure."""
        pass

    @abstractmethod
    def get_default_position_attributes(self) -> Dict[str, Any]:
        """Get default position attributes."""
        pass


class IPositionResolver(ABC):
    """Interface for position resolution services."""

    @abstractmethod
    def resolve_position(self, position_key: str) -> Optional[Any]:
        """Resolve position from key."""
        pass

    @abstractmethod
    def get_valid_positions(self) -> List[str]:
        """Get list of valid position keys."""
        pass

    @abstractmethod
    def validate_position_key(self, position_key: str) -> bool:
        """Validate position key format."""
        pass


class IGlyphDataService(ABC):
    """Interface for glyph data services."""

    @abstractmethod
    def determine_glyph_data(self, pictograph_data: "PictographData") -> None:
        """
        Determine glyph data from pictograph information.

        Note: This method no longer returns GlyphData as all glyph information
        is now computed directly from PictographData using utility functions.

        Args:
            pictograph_data: The pictograph data to analyze
        """
        pass

    @abstractmethod
    def determine_glyph_data_from_beat(self, beat_data: "BeatData") -> None:
        """
        Backward compatibility method to determine glyph data from beat data.

        Note: This method no longer returns GlyphData as all glyph information
        is now computed directly from PictographData using utility functions.

        Args:
            beat_data: The beat data to analyze
        """
        pass

    @abstractmethod
    def _beat_data_to_pictograph_data(self, beat_data: "BeatData") -> "PictographData":
        """Convert BeatData to PictographData for glyph processing."""
        pass

    @abstractmethod
    def _determine_letter_type(self, letter: str) -> Optional["LetterType"]:
        """Determine the letter type from the letter string."""
        pass

    @abstractmethod
    def _determine_vtg_mode(
        self, pictograph_data: "PictographData"
    ) -> Optional["VTGMode"]:
        """
        Determine VTG mode from motion data.

        This is a simplified implementation. The full logic is quite complex
        and involves grid mode checking, position analysis, etc.
        """
        pass

    @abstractmethod
    def _motions_same_direction(
        self, blue_motion: "MotionData", red_motion: "MotionData"
    ) -> bool:
        """Check if two motions are in the same direction."""
        pass

    @abstractmethod
    def _determine_timing(
        self, blue_motion: "MotionData", red_motion: "MotionData"
    ) -> str:
        """Determine if motions are split, together, or quarter pattern."""
        pass

    @abstractmethod
    def _vtg_to_elemental(
        self, vtg_mode: Optional["VTGMode"]
    ) -> Optional["ElementalType"]:
        """Convert VTG mode to elemental type."""
        pass

    @abstractmethod
    def _determine_positions(
        self, pictograph_data: "PictographData"
    ) -> Tuple[Optional[str], Optional[str]]:
        """Determine start and end positions from pictograph data."""
        pass
