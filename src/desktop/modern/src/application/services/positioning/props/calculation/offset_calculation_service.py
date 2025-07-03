"""
Offset Calculation Service

Pure service for calculating prop positioning offsets.
Extracted from PropManagementService to follow single responsibility principle.

PROVIDES:
- Directional offset calculations based on prop types
- Prop size-based offset divisors
- Diagonal offset calculations
- Scene-relative offset scaling
"""

from typing import Dict, Tuple
from abc import ABC, abstractmethod
from PyQt6.QtCore import QPointF

from domain.models.pictograph_models import PropType
from ...props.calculation.direction_calculation_service import SeparationDirection


class IOffsetCalculationService(ABC):
    """Interface for offset calculation operations."""

    @abstractmethod
    def calculate_directional_offset(
        self, direction: SeparationDirection, prop_type: PropType
    ) -> QPointF:
        """Calculate offset based on direction and prop type."""

    @abstractmethod
    def calculate_separation_offsets(
        self,
        blue_direction: SeparationDirection,
        red_direction: SeparationDirection,
        prop_type: PropType,
    ) -> Tuple[QPointF, QPointF]:
        """Calculate separation offsets for blue and red props."""

    @abstractmethod
    def get_prop_offset_divisor(self, prop_type: PropType) -> int:
        """Get offset divisor for prop type."""


class OffsetCalculationService(IOffsetCalculationService):
    """
    Pure service for offset calculation operations.

    Handles all offset calculations without external dependencies.
    Uses the same logic as the BetaOffsetCalculator.
    """

    def __init__(self):
        """Initialize offset calculation service."""
        # Beta prop positioning constants
        self._large_offset_divisor = 60
        self._medium_offset_divisor = 50
        self._small_offset_divisor = 45
        self._scene_reference_size = 950

        # Initialize prop offset mapping
        self._prop_offset_map = self._build_prop_offset_map()

    def calculate_directional_offset(
        self, direction: SeparationDirection, prop_type: PropType
    ) -> QPointF:
        """
        Calculate offset based on direction and prop type.

        Uses the same logic as the BetaOffsetCalculator.
        """
        # Get offset divisor based on prop type
        offset_divisor = self._prop_offset_map.get(
            prop_type, self._small_offset_divisor
        )

        # Calculate base offset
        base_offset = self._scene_reference_size / offset_divisor

        # Calculate diagonal offset for diagonal directions
        diagonal_offset = base_offset / (2**0.5)

        # Direction to offset mapping using SeparationDirection enum
        offset_map = {
            SeparationDirection.LEFT: QPointF(-base_offset, 0),
            SeparationDirection.RIGHT: QPointF(base_offset, 0),
            SeparationDirection.UP: QPointF(0, -base_offset),
            SeparationDirection.DOWN: QPointF(0, base_offset),
            SeparationDirection.DOWNRIGHT: QPointF(diagonal_offset, diagonal_offset),
            SeparationDirection.UPLEFT: QPointF(-diagonal_offset, -diagonal_offset),
            SeparationDirection.DOWNLEFT: QPointF(-diagonal_offset, diagonal_offset),
            SeparationDirection.UPRIGHT: QPointF(diagonal_offset, -diagonal_offset),
        }

        return offset_map.get(direction, QPointF(0, 0))

    def calculate_separation_offsets(
        self,
        blue_direction: SeparationDirection,
        red_direction: SeparationDirection,
        prop_type: PropType,
    ) -> Tuple[QPointF, QPointF]:
        """Calculate separation offsets for blue and red props."""
        blue_offset = self.calculate_directional_offset(blue_direction, prop_type)
        red_offset = self.calculate_directional_offset(red_direction, prop_type)

        return blue_offset, red_offset

    def get_prop_offset_divisor(self, prop_type: PropType) -> int:
        """Get offset divisor for prop type."""
        return self._prop_offset_map.get(prop_type, self._small_offset_divisor)

    def calculate_base_offset(self, prop_type: PropType) -> float:
        """Calculate base offset for prop type."""
        offset_divisor = self.get_prop_offset_divisor(prop_type)
        return self._scene_reference_size / offset_divisor

    def calculate_diagonal_offset(self, prop_type: PropType) -> float:
        """Calculate diagonal offset for prop type."""
        base_offset = self.calculate_base_offset(prop_type)
        return base_offset / (2**0.5)

    def scale_offset_for_scene_size(
        self, offset: QPointF, scene_size: float
    ) -> QPointF:
        """Scale offset based on actual scene size vs reference size."""
        scale_factor = scene_size / self._scene_reference_size
        return QPointF(offset.x() * scale_factor, offset.y() * scale_factor)

    def get_offset_for_prop_size_category(self, size_category: str) -> int:
        """Get offset divisor for prop size category."""
        category_map = {
            "large": self._large_offset_divisor,
            "medium": self._medium_offset_divisor,
            "small": self._small_offset_divisor,
        }
        return category_map.get(size_category, self._small_offset_divisor)

    def _build_prop_offset_map(self) -> Dict[PropType, int]:
        """Build prop offset mapping based on modern PropType enum."""
        return {
            PropType.CLUB: self._large_offset_divisor,
            PropType.EIGHTRINGS: self._large_offset_divisor,
            PropType.BIG_EIGHT_RINGS: self._large_offset_divisor,
            PropType.DOUBLESTAR: self._medium_offset_divisor,
            PropType.BIGDOUBLESTAR: self._medium_offset_divisor,
            PropType.HAND: self._small_offset_divisor,
            PropType.BUUGENG: self._small_offset_divisor,
            PropType.TRIAD: self._small_offset_divisor,
            PropType.MINIHOOP: self._small_offset_divisor,
            PropType.BIGBUUGENG: self._medium_offset_divisor,
            PropType.BIGHOOP: self._large_offset_divisor,
            PropType.STAFF: self._small_offset_divisor,
            PropType.BIGSTAFF: self._large_offset_divisor,
            PropType.FAN: self._small_offset_divisor,
            PropType.SWORD: self._large_offset_divisor,
            PropType.GUITAR: self._large_offset_divisor,
            PropType.UKULELE: self._small_offset_divisor,
            PropType.SIMPLESTAFF: self._small_offset_divisor,
            PropType.FRACTALGENG: self._small_offset_divisor,
            PropType.QUIAD: self._small_offset_divisor,
            PropType.CHICKEN: self._small_offset_divisor,
            PropType.TRIQUETRA: self._small_offset_divisor,
            PropType.TRIQUETRA2: self._small_offset_divisor,
        }
