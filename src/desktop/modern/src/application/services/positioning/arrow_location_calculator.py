"""
Arrow Location Calculator Service - Working Implementation

This service calculates arrow locations based on motion data.
"""

from typing import Any, Optional, Protocol, runtime_checkable
from domain.models.core_models import MotionData, MotionType, Location


@runtime_checkable
class IArrowLocationCalculator(Protocol):
    """Interface for arrow location calculator."""

    def calculate_location(self, motion: MotionData) -> Location:
        """Calculate arrow location for given motion."""
        ...


class ArrowLocationCalculator:
    """Arrow location calculator service implementation."""

    def __init__(self):
        """Initialize the service."""
        pass

    def calculate_location(self, motion: MotionData) -> Location:
        """Calculate arrow location based on motion data."""
        if motion.motion_type == MotionType.STATIC:
            return motion.start_loc
        elif motion.motion_type == MotionType.DASH:
            # For now, return start location - would delegate to dash service in real implementation
            return motion.start_loc
        elif motion.motion_type in [MotionType.PRO, MotionType.ANTI]:
            # Calculate shift location (simplified logic)
            return self._calculate_shift_location(motion.start_loc, motion.end_loc)
        else:
            return motion.start_loc
    
    def _calculate_shift_location(self, start_loc: Location, end_loc: Location) -> Location:
        """Calculate shift location between two positions."""
        # Simplified shift calculation logic
        shift_map = {
            (Location.NORTH, Location.EAST): Location.NORTHEAST,
            (Location.EAST, Location.SOUTH): Location.SOUTHEAST,
            (Location.SOUTH, Location.WEST): Location.SOUTHWEST,
            (Location.WEST, Location.NORTH): Location.NORTHWEST,
            (Location.NORTHEAST, Location.NORTHWEST): Location.NORTH,
            (Location.NORTHEAST, Location.SOUTHEAST): Location.EAST,
            (Location.SOUTHWEST, Location.SOUTHEAST): Location.SOUTH,
            (Location.NORTHWEST, Location.SOUTHWEST): Location.WEST,
        }
        
        return shift_map.get((start_loc, end_loc), start_loc)


# Export the service class and interface
__all__ = ["ArrowLocationCalculator", "IArrowLocationCalculator"]
