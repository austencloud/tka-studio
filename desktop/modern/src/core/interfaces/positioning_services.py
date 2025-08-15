"""
Positioning Services Interfaces

Defines interfaces for position and coordinate management services.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from desktop.modern.src.core.types.geometry import Point
    from desktop.modern.src.domain.models.arrow_data import ArrowData
    from desktop.modern.src.domain.models.motion_models import MotionData
    from desktop.modern.src.domain.models.pictograph_data import PictographData
    from domain.models import Location


class IPositionManager(ABC):
    """Interface for position management."""

    @abstractmethod
    def get_position_coordinates(self, position: str) -> tuple[int, int]:
        """Get coordinates for a position."""
        pass

    @abstractmethod
    def set_position_coordinates(self, position: str, x: int, y: int) -> None:
        """Set coordinates for a position."""
        pass

    @abstractmethod
    def get_all_positions(self) -> list[str]:
        """Get all available positions."""
        pass

    @abstractmethod
    def validate_position(self, position: str) -> bool:
        """Validate if a position is valid."""
        pass


class ICoordinateService(ABC):
    """Interface for coordinate system services."""

    @abstractmethod
    def transform_coordinates(
        self, x: int, y: int, from_system: str, to_system: str
    ) -> tuple[int, int]:
        """Transform coordinates between systems."""
        pass

    @abstractmethod
    def get_coordinate_systems(self) -> list[str]:
        """Get available coordinate systems."""
        pass

    @abstractmethod
    def set_default_coordinate_system(self, system: str) -> None:
        """Set the default coordinate system."""
        pass


class IPositioningService(ABC):
    """Interface for positioning calculations and management."""

    @abstractmethod
    def calculate_position(self, parameters: dict[str, Any]) -> dict[str, Any]:
        """Calculate position based on parameters."""
        pass

    @abstractmethod
    def get_position_data(self, position_id: str) -> dict[str, Any]:
        """Get position data."""
        pass

    @abstractmethod
    def update_position_data(self, position_id: str, data: dict[str, Any]) -> None:
        """Update position data."""
        pass

    @abstractmethod
    def validate_positioning_data(self, data: dict[str, Any]) -> bool:
        """Validate positioning data."""
        pass


class IArrowCoordinateSystemService(ABC):
    """Interface for arrow coordinate system management."""

    @abstractmethod
    def get_initial_position(self, motion: MotionData, location: Location) -> Point:
        """Get initial position coordinates based on motion type and location."""
        pass

    @abstractmethod
    def get_scene_center(self) -> Point:
        """Get the center point of the scene coordinate system."""
        pass

    @abstractmethod
    def get_coordinate_info(self, location: Location) -> dict:
        """Get detailed coordinate information for debugging."""
        pass

    @abstractmethod
    def validate_coordinates(self, point: Point) -> bool:
        """Validate that coordinates are within scene bounds."""
        pass

    @abstractmethod
    def get_all_hand_points(self) -> dict[Location, Point]:
        """Get all hand point coordinates."""
        pass

    @abstractmethod
    def get_all_layer2_points(self) -> dict[Location, Point]:
        """Get all layer2 point coordinates."""
        pass


class IArrowPositioningOrchestrator(ABC):
    """Interface for arrow positioning orchestration."""

    @abstractmethod
    def calculate_arrow_position(
        self,
        arrow_data: ArrowData,
        pictograph_data: PictographData,
        motion_data: MotionData = None,
    ) -> tuple[float, float, float]:
        """Calculate arrow position using streamlined microservices pipeline."""
        pass


class IArrowLocationCalculator(ABC):
    """Interface for arrow location calculations."""

    @abstractmethod
    def calculate_location(
        self, arrow_data: ArrowData, motion_data: MotionData
    ) -> Point:
        """Calculate arrow location."""
        pass


class IArrowRotationCalculator(ABC):
    """Interface for arrow rotation calculations."""

    @abstractmethod
    def calculate_rotation(
        self, arrow_data: ArrowData, motion_data: MotionData
    ) -> float:
        """Calculate arrow rotation."""
        pass


class IArrowAdjustmentCalculator(ABC):
    """Interface for arrow adjustment calculations."""

    @abstractmethod
    def calculate_adjustment(
        self, arrow_data: ArrowData, motion_data: MotionData
    ) -> Point:
        """Calculate arrow position adjustments."""
        pass
