"""
Interface definitions for arrow positioning services.

These interfaces define the contracts for the refactored positioning services
that follow TKA's clean architecture principles.
"""

from abc import ABC, abstractmethod
from typing import Tuple
from PyQt6.QtCore import QPointF

from desktop.modern.src.domain.models.core_models import MotionData, Location
from desktop.modern.src.domain.models.pictograph_models import ArrowData, PictographData


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
        pass


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
        pass


class IArrowAdjustmentCalculator(ABC):
    """Interface for calculating arrow position adjustments."""

    @abstractmethod
    def calculate_adjustment(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> QPointF:
        """
        Calculate position adjustment for arrow based on placement rules.

        Args:
            arrow_data: Arrow data including motion and color
            pictograph_data: Pictograph context for special placement rules

        Returns:
            QPointF representing the adjustment offset
        """
        pass


class IArrowCoordinateSystemService(ABC):
    """Interface for coordinate system management."""

    @abstractmethod
    def get_initial_position(self, motion: MotionData, location: Location) -> QPointF:
        """
        Get initial position coordinates based on motion type and location.

        Args:
            motion: Motion data to determine coordinate system (hand points vs layer2)
            location: Arrow location

        Returns:
            QPointF representing the initial position coordinates
        """
        pass

    @abstractmethod
    def get_scene_center(self) -> QPointF:
        """Get the center point of the scene coordinate system."""
        pass


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
        pass

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
        pass
