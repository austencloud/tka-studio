"""
Interface definitions for arrow positioning services.

These interfaces define the contracts for the refactored positioning services
that follow TKA's clean architecture principles.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from desktop.modern.core.types import Point
from desktop.modern.domain.models.arrow_data import ArrowData
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import Location
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData


class IArrowLocationCalculator(ABC):
    """Interface for calculating arrow location based on motion data."""

    @abstractmethod
    def calculate_location(
        self, motion: MotionData, pictograph_data: PictographData | None = None
    ) -> Location:
        """
        Calculate the arrow location based on motion type and data.

        Args:
            motion: Motion data containing type, start/end locations, rotation direction
            beat_data: Optional beat data for DASH motion Type 3 detection

        Returns:
            Location enum value representing the calculated arrow location
        """


class IArrowRotationCalculator(ABC):
    """Interface for calculating arrow rotation based on motion and location."""

    @abstractmethod
    def calculate_rotation(self, motion: MotionData, location: Location) -> float:
        """
        Calculate the arrow rotation angle based on motion type and location.

        Args:
            motion: Motion data containing type and rotation direction
            location: Calculated arrow location

        Returns:
            Rotation angle in degrees (0-360)
        """


class IArrowAdjustmentCalculator(ABC):
    """Interface for calculating arrow position adjustments."""

    @abstractmethod
    def calculate_adjustment(
        self, motion_data: MotionData, letter: str, location: Location
    ) -> Point:
        """
        Calculate position adjustment for arrow based on placement rules.

        Args:
            motion_data: Motion data containing type, rotation, and location info
            letter: Letter for special placement lookup
            location: Pre-calculated arrow location

        Returns:
            Point representing the adjustment offset
        """


class IArrowCoordinateSystemService(ABC):
    """Interface for coordinate system management."""

    @abstractmethod
    def get_initial_position(self, motion: MotionData, location: Location) -> Point:
        """
        Get initial position coordinates based on motion type and location.

        Args:
            motion: Motion data to determine coordinate system (hand points vs layer2)
            location: Arrow location

        Returns:
            Point representing the initial position coordinates
        """

    @abstractmethod
    def get_scene_center(self) -> Point:
        """Get the center point of the scene coordinate system."""


class IArrowPositioningOrchestrator(ABC):
    """Interface for orchestrating the complete arrow positioning pipeline."""

    @abstractmethod
    def calculate_arrow_position(
        self,
        arrow_data: ArrowData,
        pictograph_data: PictographData,
        motion_data: MotionData | None = None,
    ) -> tuple[float, float, float]:
        """
        Calculate complete arrow position using the positioning pipeline.

        Args:
            arrow_data: Arrow data including color and visibility
            pictograph_data: Pictograph context
            motion_data: Optional pre-extracted motion data

        Returns:
            Tuple of (x, y, rotation_angle)
        """

    @abstractmethod
    def calculate_all_arrow_positions(
        self, pictograph_data: PictographData
    ) -> PictographData:
        """
        Calculate positions for all arrows in the pictograph.

        Args:
            pictograph_data: Pictograph containing all arrows

        Returns:
            Updated pictograph data with calculated positions
        """

    @abstractmethod
    def should_mirror_arrow(self, arrow_data: ArrowData) -> bool:
        """
        Determine if arrow should be mirrored based on motion type.

        Args:
            arrow_data: Arrow data including motion type and rotation direction

        Returns:
            True if arrow should be mirrored, False otherwise
        """

    @abstractmethod
    def apply_mirror_transform(self, arrow_item, should_mirror: bool) -> None:
        """
        Apply mirror transformation to arrow graphics item.

        Args:
            arrow_item: Arrow graphics item to transform
            should_mirror: Whether to apply mirror transformation

        Returns:
            None
        """


class IPositionMapper(ABC):
    """Interface for position matching and calculation services."""

    @abstractmethod
    def extract_end_position(self, last_beat: dict[str, Any]) -> str | None:
        """Extract end position from beat data."""

    @abstractmethod
    def calculate_end_position_from_motions(
        self, beat_data: dict[str, Any]
    ) -> str | None:
        """Calculate end position from motion attributes."""

    @abstractmethod
    def get_position_from_locations(self, start_loc: str, end_loc: str) -> str | None:
        """Get position key from start and end locations."""

    @abstractmethod
    def has_motion_attributes(self, beat_data: dict[str, Any]) -> bool:
        """Check if beat data has motion attributes."""

    @abstractmethod
    def extract_modern_end_position(self, beat_data: BeatData) -> str | None:
        """Extract end position directly from Modern BeatData."""


class IDashLocationCalculator(ABC):
    """Interface for calculating dash arrow locations."""

    @abstractmethod
    def calculate_dash_location_from_pictograph_data(
        self, pictograph_data: PictographData, is_blue_arrow: bool
    ) -> Location:
        """
        Calculate dash location from pictograph data.

        Args:
            pictograph_data: The pictograph data containing motion information
            is_blue_arrow: True if calculating for blue arrow, False for red arrow

        Returns:
            Location enum value representing the calculated dash arrow location
        """

    @abstractmethod
    def calculate_dash_location(
        self,
        dash_motion: MotionData,
        blue_motion: MotionData,
        red_motion: MotionData,
        is_blue_arrow: bool,
        grid_mode: str = "diamond",
    ) -> Location:
        """
        Calculate dash location based on motion data.

        Args:
            dash_motion: The dash motion data
            blue_motion: The blue motion data
            red_motion: The red motion data
            is_blue_arrow: True if calculating for blue arrow, False for red arrow
        Returns:
            Location enum value representing the calculated dash arrow location
        """


class IDirectionalTupleCalculator(ABC):
    """Interface for calculating directional tuples for arrow positioning."""

    @abstractmethod
    def calculate_directional_tuple(
        self, motion: MotionData, location: Location
    ) -> tuple[float, float]:
        """
        Calculate directional tuple for arrow positioning.

        Args:
            motion: Motion data containing type and rotation direction
            location: Arrow location

        Returns:
            Tuple of (x_offset, y_offset) directional adjustments
        """


class IQuadrantIndexCalculator(ABC):
    """Interface for calculating quadrant indices for arrow positioning."""

    @abstractmethod
    def calculate_quadrant_index(self, location: Location) -> int:
        """
        Calculate quadrant index for the given location.

        Args:
            location: Arrow location

        Returns:
            Quadrant index (0-3)
        """


class IAttributeKeyGenerator(ABC):
    """Interface for generating attribute keys for arrow positioning."""

    @abstractmethod
    def get_key_from_arrow(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> str:
        """
        Get attribute key from arrow data.

        Args:
            arrow_data: Arrow data containing color and other attributes
            pictograph_data: Pictograph data for context

        Returns:
            Attribute key string for positioning lookups
        """

    @abstractmethod
    def generate_key(
        self,
        motion_type: Any,
        letter: str,
        start_ori: Any,
        color: str,
        lead_state: str,
        has_hybrid_motions: bool,
        starts_from_mixed_orientation: bool,
        starts_from_standard_orientation: bool,
    ) -> str:
        """
        Generate attribute key from components.

        Args:
            motion_type: Motion type
            letter: Letter string
            start_ori: Start orientation
            color: Arrow color
            lead_state: Lead state
            has_hybrid_motions: Whether there are hybrid motions
            starts_from_mixed_orientation: Whether starts from mixed orientation
            starts_from_standard_orientation: Whether starts from standard orientation

        Returns:
            Generated attribute key string
        """


class IPlacementKeyGenerator(ABC):
    """Interface for generating placement keys for arrow positioning."""

    @abstractmethod
    def get_key_from_arrow(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> str:
        """
        Get placement key from arrow data.

        Args:
            arrow_data: Arrow data containing color and other attributes
            pictograph_data: Pictograph data for context

        Returns:
            Placement key string for positioning lookups
        """


class ITurnsTupleKeyGenerator(ABC):
    """Interface for generating turns tuple keys for arrow positioning."""

    @abstractmethod
    def get_key_from_motion(self, motion_data: MotionData) -> str:
        """
        Get turns tuple key from motion data.

        Args:
            motion_data: Motion data containing turns information

        Returns:
            Turns tuple key string for positioning lookups
        """


class IOrientationCalculator(ABC):
    """Interface for orientation calculation operations."""

    @abstractmethod
    def calculate_orientation(self, motion_data: Any, context: Any) -> Any:
        """Calculate orientation based on motion and context."""

    @abstractmethod
    def get_orientation_adjustments(self, orientation: Any) -> dict[str, Any]:
        """Get adjustments for orientation."""

    @abstractmethod
    def validate_orientation(self, orientation: Any) -> bool:
        """Validate orientation data."""
