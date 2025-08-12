"""
Shared Positioning Service Interfaces

Framework-agnostic interfaces for positioning services that can be used
across different UI frameworks (Qt, Web, etc.).
"""

from abc import ABC, abstractmethod

from desktop.modern.domain.models import Location, MotionData


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

    @abstractmethod
    def generate_directional_tuples(
        self, motion: MotionData, base_x: float, base_y: float
    ) -> list[tuple[float, float]]:
        """
        Generate directional tuples for the given motion and base adjustment.

        Args:
            motion: Motion data containing type, rotation, and location info
            base_x: Base X adjustment value
            base_y: Base Y adjustment value

        Returns:
            List of 4 directional tuples representing rotated adjustments
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


class IArrowLocationCalculator(ABC):
    """Interface for calculating arrow locations based on motion data."""

    @abstractmethod
    def calculate_arrow_location(
        self, motion: MotionData, is_blue_arrow: bool
    ) -> Location:
        """
        Calculate arrow location based on motion data.

        Args:
            motion: Motion data containing type and location information
            is_blue_arrow: True if calculating for blue arrow, False for red arrow

        Returns:
            Location enum value representing the calculated arrow location
        """


class IDashLocationCalculator(ABC):
    """Interface for calculating dash arrow locations."""

    @abstractmethod
    def calculate_dash_location_from_pictograph_data(
        self, pictograph_data, is_blue_arrow: bool
    ) -> Location:
        """
        Calculate dash location from pictograph data.

        Args:
            pictograph_data: The pictograph data containing motion information
            is_blue_arrow: True if calculating for blue arrow, False for red arrow

        Returns:
            Location enum value representing the calculated dash arrow location
        """
