"""
Interface definitions for arrow positioning services.

These interfaces define the contracts for the refactored positioning services
that follow TKA's clean architecture principles.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict, Any

from core.types import Point
from domain.models.core_models import MotionData, Location, BeatData
from domain.models.pictograph_models import ArrowData, PictographData


class IArrowLocationCalculator(ABC):
    """Interface for calculating arrow location based on motion data."""

    @abstractmethod
    def calculate_location(
        self, motion: MotionData, pictograph_data: PictographData = None
    ) -> Location:
        """
        Calculate the arrow location based on motion type and data.

        Args:
            motion: Motion data containing type, start/end locations, rotation direction
            pictograph_data: Optional pictograph context for Type 3 detection

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
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Point:
        """
        Calculate position adjustment for arrow based on placement rules.

        Args:
            arrow_data: Arrow data including motion and color
            pictograph_data: Pictograph context for special placement rules

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
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Tuple[float, float, float]:
        """
        Calculate complete arrow position using the positioning pipeline.

        Args:
            arrow_data: Arrow data including motion and visibility
            pictograph_data: Pictograph context

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


class IPositionMatchingService(ABC):
    """Interface for position matching and calculation services."""

    @abstractmethod
    def extract_end_position(self, last_beat: Dict[str, Any]) -> Optional[str]:
        """Extract end position from beat data."""

    @abstractmethod
    def calculate_end_position_from_motions(
        self, beat_data: Dict[str, Any]
    ) -> Optional[str]:
        """Calculate end position from motion attributes."""

    @abstractmethod
    def get_position_from_locations(
        self, start_loc: str, end_loc: str
    ) -> Optional[str]:
        """Get position key from start and end locations."""

    @abstractmethod
    def has_motion_attributes(self, beat_data: Dict[str, Any]) -> bool:
        """Check if beat data has motion attributes."""

    @abstractmethod
    def extract_modern_end_position(self, beat_data: BeatData) -> Optional[str]:
        """Extract end position directly from Modern BeatData."""
