"""
Arrow Location Calculator Service

Pure algorithmic service for calculating arrow locations based on motion data.

This service handles:
- Static motion location calculation (uses start location)
- Shift motion location calculation (PRO/ANTI/FLOAT using start/end pair mapping)
- Dash motion location calculation (with Type 3 detection support)

No UI dependencies, completely testable in isolation.
"""

import logging
from typing import Optional

from desktop.modern.core.interfaces.positioning_services import IArrowLocationCalculator
from desktop.modern.domain.models import BeatData, Location, MotionData, MotionType
from desktop.modern.domain.models.pictograph_data import PictographData

from .dash_location_calculator import DashLocationCalculator

logger = logging.getLogger(__name__)


class ArrowLocationCalculatorService(IArrowLocationCalculator):
    """
    Pure algorithmic service for calculating arrow locations.

    Implements location calculation algorithms without any UI dependencies.
    Each motion type has its own calculation strategy.
    """

    def __init__(self, dash_location_service: Optional[DashLocationCalculator] = None):
        """
        Initialize the location calculator.

        Args:
            dash_location_service: Service for dash location calculations
        """
        self.dash_location_service = dash_location_service or DashLocationCalculator()

        # Direction pairs mapping for shift arrows (PRO/ANTI/FLOAT)
        # Maps start/end location pairs to their calculated arrow location
        self._shift_direction_pairs = {
            frozenset({Location.NORTH, Location.EAST}): Location.NORTHEAST,
            frozenset({Location.EAST, Location.SOUTH}): Location.SOUTHEAST,
            frozenset({Location.SOUTH, Location.WEST}): Location.SOUTHWEST,
            frozenset({Location.WEST, Location.NORTH}): Location.NORTHWEST,
            frozenset({Location.NORTHEAST, Location.NORTHWEST}): Location.NORTH,
            frozenset({Location.NORTHEAST, Location.SOUTHEAST}): Location.EAST,
            frozenset({Location.SOUTHWEST, Location.SOUTHEAST}): Location.SOUTH,
            frozenset({Location.NORTHWEST, Location.SOUTHWEST}): Location.WEST,
        }

    def calculate_location(
        self, motion_data: MotionData, pictograph_data: Optional[PictographData] = None
    ) -> Location:
        """
        Calculate arrow location based on motion type and data.

        Args:
            motion: Motion data containing type, start/end locations, rotation direction
            pictograph_data: Optional beat data for DASH motion Type 3 detection

        Returns:
            Location enum value representing the calculated arrow location

        Raises:
            ValueError: If dash motion requires beat data but none provided
        """
        if motion_data.motion_type == MotionType.STATIC:
            return self._calculate_static_location(motion_data)
        elif motion_data.motion_type in [
            MotionType.PRO,
            MotionType.ANTI,
            MotionType.FLOAT,
        ]:
            return self._calculate_shift_location(motion_data)
        elif motion_data.motion_type == MotionType.DASH:
            return self._calculate_dash_location(motion_data, pictograph_data)
        else:
            logger.warning(
                f"Unknown motion type: {motion_data.motion_type}, using start location"
            )
            return motion_data.start_loc

    def _calculate_static_location(self, motion: MotionData) -> Location:
        """
        Calculate location for static arrows.

        Static arrows use their start location directly.

        Args:
            motion: Motion data with STATIC type

        Returns:
            The start location of the motion
        """
        return motion.start_loc

    def _calculate_shift_location(self, motion_data: MotionData) -> Location:
        """
        Calculate location for shift arrows (PRO/ANTI/FLOAT).

        Shift arrows use a mapping from start/end location pairs to determine
        their arrow location. This implements the proven shift location algorithm.

        Args:
            motion: Motion data with PRO, ANTI, or FLOAT type

        Returns:
            Calculated location based on start/end pair mapping
        """
        location_pair = frozenset({motion_data.start_loc, motion_data.end_loc})
        calculated_location = self._shift_direction_pairs.get(
            location_pair, motion_data.start_loc
        )

        logger.debug(
            f"Shift location calculation: {motion_data.start_loc} -> {motion_data.end_loc} = {calculated_location}"
        )

        return calculated_location

    def _calculate_dash_location(
        self, motion: MotionData, pictograph_data: Optional[PictographData]
    ) -> Location:
        """
        Calculate location for dash arrows.

        Dash arrows use specialized logic that may require beat data
        for Type 3 detection and other special cases.

        Args:
            motion: Motion data with DASH type
            beat_data: Beat data for Type 3 detection

        Returns:
            Calculated dash location

        Raises:
            ValueError: If beat data is required but not provided
        """
        if pictograph_data is None:
            logger.warning(
                "No beat data provided for dash location calculation, using start location"
            )
            return motion.start_loc

        is_blue_arrow = self.is_blue_arrow_motion(motion, pictograph_data)

        return self.dash_location_service.calculate_dash_location_from_pictograph_data(
            pictograph_data, is_blue_arrow
        )

    def get_supported_motion_types(self) -> list[MotionType]:
        """
        Get list of motion types supported by this calculator.

        Returns:
            List of supported MotionType enum values
        """
        return [
            MotionType.STATIC,
            MotionType.PRO,
            MotionType.ANTI,
            MotionType.FLOAT,
            MotionType.DASH,
        ]

    def validate_motion_data(self, motion: MotionData) -> bool:
        """
        Validate that motion data is suitable for location calculation.

        Args:
            motion: Motion data to validate

        Returns:
            True if motion data is valid for location calculation
        """
        if not motion:
            return False

        if motion.motion_type not in self.get_supported_motion_types():
            return False

        # Validate required fields based on motion type
        if motion.motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
            # Shift motions require both start and end locations
            return motion.start_loc is not None and motion.end_loc is not None
        if motion.motion_type in [MotionType.STATIC, MotionType.DASH]:
            # Static and dash motions require at least start location
            return motion.start_loc is not None

        return True

    def extract_beat_data_from_pictograph(
        self, pictograph: PictographData
    ) -> Optional[BeatData]:
        """Extract beat data from pictograph for dash location calculation."""
        if not pictograph.arrows:
            return None

        # Extract motion data from motions dictionary
        blue_motion = None
        red_motion = None

        if "blue" in pictograph.motions:
            blue_motion = pictograph.motions["blue"]

        if "red" in pictograph.motions:
            red_motion = pictograph.motions["red"]

        # Create pictograph data for beat
        pictograph_data = PictographData(
            motions=(
                {"blue": blue_motion, "red": red_motion}
                if blue_motion or red_motion
                else {}
            )
        )

        # Create beat data
        return BeatData(
            beat_number=pictograph.metadata.get("created_from_beat", 1),
            letter=pictograph.metadata.get("letter"),
            pictograph_data=pictograph_data,
        )

    def is_blue_arrow_motion(
        self, motion: MotionData, pictograph_data: PictographData
    ) -> bool:
        """Determine if the given motion belongs to the blue arrow."""
        # Compare the motion with blue and red motions in beat data
        if pictograph_data.motions.get("blue") == motion:
            return True
        if pictograph_data.motions.get("red") == motion:
            return False
        # Fallback: if we can't determine, assume blue
        logger.warning("Could not determine arrow color for motion, assuming blue")
        return True
