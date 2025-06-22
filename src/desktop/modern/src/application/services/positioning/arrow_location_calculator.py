"""
Arrow Location Calculator Service

Pure algorithmic service for calculating arrow locations based on motion data.
Extracted from ArrowManagementService to follow single responsibility principle.

PROVIDES:
- Static arrow location calculation (start_loc)
- Shift arrow location calculation (PRO/ANTI/FLOAT)
- Dash arrow location calculation (with Type 3 support)
- Pure algorithms with no Qt dependencies
"""

from typing import Optional
from abc import ABC, abstractmethod

from desktop.modern.src.domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
)
from desktop.modern.src.domain.models.pictograph_models import PictographData
from desktop.modern.src.domain.models.letter_type_classifier import LetterTypeClassifier
from .dash_location_service import DashLocationService


class IArrowLocationCalculator(ABC):
    """Interface for arrow location calculation."""

    @abstractmethod
    def calculate_location(
        self, motion: MotionData, pictograph_data: Optional[PictographData] = None
    ) -> Location:
        """Calculate arrow location based on motion data."""
        pass


class ArrowLocationCalculator(IArrowLocationCalculator):
    """
    Pure algorithmic service for arrow location calculation.

    Handles all arrow location algorithms without Qt dependencies.
    Uses immutable data patterns following TKA architecture.
    """

    def __init__(self, dash_location_service: Optional[DashLocationService] = None):
        """Initialize with dependency injection."""
        self.dash_location_service = dash_location_service or DashLocationService()

    def calculate_location(
        self, motion: MotionData, pictograph_data: Optional[PictographData] = None
    ) -> Location:
        """Calculate arrow location using motion-type-specific algorithms."""
        if motion.motion_type == MotionType.STATIC:
            return self._calculate_static_location(motion)
        elif motion.motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
            return self._calculate_shift_location(motion)
        elif motion.motion_type == MotionType.DASH:
            return self._calculate_dash_location(motion, pictograph_data)
        else:
            return motion.start_loc

    def _calculate_static_location(self, motion: MotionData) -> Location:
        """Calculate location for static arrows (always start_loc)."""
        return motion.start_loc

    def _calculate_shift_location(self, motion: MotionData) -> Location:
        """Calculate location for shift arrows (PRO/ANTI/FLOAT) based on start/end pair."""
        # Direction pairs mapping for shift arrows
        direction_pairs = {
            frozenset({Location.NORTH, Location.EAST}): Location.NORTHEAST,
            frozenset({Location.EAST, Location.SOUTH}): Location.SOUTHEAST,
            frozenset({Location.SOUTH, Location.WEST}): Location.SOUTHWEST,
            frozenset({Location.WEST, Location.NORTH}): Location.NORTHWEST,
            frozenset({Location.NORTHEAST, Location.NORTHWEST}): Location.NORTH,
            frozenset({Location.NORTHEAST, Location.SOUTHEAST}): Location.EAST,
            frozenset({Location.SOUTHWEST, Location.SOUTHEAST}): Location.SOUTH,
            frozenset({Location.NORTHWEST, Location.SOUTHWEST}): Location.WEST,
        }
        return direction_pairs.get(
            frozenset({motion.start_loc, motion.end_loc}), motion.start_loc
        )

    def _calculate_dash_location(
        self, motion: MotionData, pictograph_data: Optional[PictographData] = None
    ) -> Location:
        """Calculate location for dash arrows using dash location service."""
        # Extract context for dash calculation
        letter_type = None
        if (
            pictograph_data
            and hasattr(pictograph_data, "letter")
            and pictograph_data.letter
        ):
            letter_type = LetterTypeClassifier.get_letter_type(pictograph_data.letter)

        # Use dash location service for complex dash calculations
        return self.dash_location_service.calculate_dash_location(
            motion=motion,
            letter_type=letter_type,
        )
