"""
Orientation Calculation Service

Handles all orientation calculations using legacy logic porting.

This service provides:
- End orientation calculation for motions
- Handpath direction calculation
- Float, whole turn, and half turn orientation calculations
- Orientation switching logic

Ported from legacy MotionOriCalculator for accuracy.
"""

import logging
from typing import Any

from desktop.modern.core.interfaces.positioning_services import IOrientationCalculator
from desktop.modern.domain.models import (
    HandPath,
    Location,
    MotionData,
    MotionType,
    Orientation,
)
from desktop.modern.domain.models.enums import RotationDirection

logger = logging.getLogger(__name__)


class OrientationCalculator(IOrientationCalculator):
    """
    Pure service for orientation calculations using exact legacy logic.

    This implements the complete orientation calculation from the legacy system:
    - Float motion handling with handpath direction
    - Half-turn calculations with prop rotation direction
    - Proper motion type handling for all motion types
    """

    def calculate_end_orientation(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """
        Calculate end orientation using exact legacy MotionOriCalculator logic.

        Args:
            motion_data: Motion data with type, turns, locations, etc.
            start_orientation: Starting orientation

        Returns:
            Calculated end orientation
        """
        motion_type = motion_data.motion_type
        turns = motion_data.turns
        start_ori = start_orientation

        logger.debug(
            f"Calculating end orientation - type: {motion_type}, turns: {turns}, start: {start_ori}"
        )

        # Handle float case separately (requires handpath calculation)
        if motion_type == MotionType.FLOAT:
            if not motion_data.start_loc or not motion_data.end_loc:
                logger.debug(
                    "FLOAT motion missing start/end locations, using start orientation"
                )
                return start_orientation

            # Calculate handpath direction
            handpath_direction = self.calculate_handpath_direction(
                motion_data.start_loc, motion_data.end_loc
            )
            logger.debug(f"Float handpath direction: {handpath_direction}")

            return self._calculate_float_orientation(start_ori, handpath_direction)

        # Handle "fl" turns case
        if turns == "fl":
            logger.warning("Motion has 'fl' turns but is not FLOAT type")
            return start_orientation

        # Validate turns
        valid_turns = {0, 0.5, 1, 1.5, 2, 2.5, 3}
        if turns not in valid_turns:
            logger.warning(f"Invalid turns value: {turns}, using start orientation")
            return start_orientation

        # Whole turn calculations
        if turns in {0, 1, 2, 3}:
            return self._calculate_whole_turn_orientation(
                motion_type, int(turns), start_ori
            )

        # Half turn calculations
        elif turns in {0.5, 1.5, 2.5}:
            return self._calculate_half_turn_orientation(
                motion_type, turns, start_ori, motion_data
            )

        logger.debug(f"Unhandled turns case: {turns}, using start orientation")
        return start_orientation

    def calculate_handpath_direction(
        self, start_loc: Location, end_loc: Location
    ) -> HandPath:
        """Calculate handpath direction using legacy logic."""
        # Simplified handpath calculation based on legacy HandpathCalculator
        direction_map = {
            # Clockwise pairs
            (Location.NORTH, Location.EAST): HandPath.CLOCKWISE,
            (Location.EAST, Location.SOUTH): HandPath.CLOCKWISE,
            (Location.SOUTH, Location.WEST): HandPath.CLOCKWISE,
            (Location.WEST, Location.NORTH): HandPath.CLOCKWISE,
            (Location.NORTHEAST, Location.SOUTHEAST): HandPath.CLOCKWISE,
            (Location.SOUTHEAST, Location.SOUTHWEST): HandPath.CLOCKWISE,
            (Location.SOUTHWEST, Location.NORTHWEST): HandPath.CLOCKWISE,
            (Location.NORTHWEST, Location.NORTHEAST): HandPath.CLOCKWISE,
            # Counter-clockwise pairs
            (Location.NORTH, Location.WEST): HandPath.COUNTER_CLOCKWISE,
            (Location.WEST, Location.SOUTH): HandPath.COUNTER_CLOCKWISE,
            (Location.SOUTH, Location.EAST): HandPath.COUNTER_CLOCKWISE,
            (Location.EAST, Location.NORTH): HandPath.COUNTER_CLOCKWISE,
            (Location.NORTHEAST, Location.NORTHWEST): HandPath.COUNTER_CLOCKWISE,
            (Location.NORTHWEST, Location.SOUTHWEST): HandPath.COUNTER_CLOCKWISE,
            (Location.SOUTHWEST, Location.SOUTHEAST): HandPath.COUNTER_CLOCKWISE,
            (Location.SOUTHEAST, Location.NORTHEAST): HandPath.COUNTER_CLOCKWISE,
            # Dash pairs
            (Location.NORTH, Location.SOUTH): HandPath.DASH,
            (Location.SOUTH, Location.NORTH): HandPath.DASH,
            (Location.EAST, Location.WEST): HandPath.DASH,
            (Location.WEST, Location.EAST): HandPath.DASH,
            (Location.NORTHEAST, Location.SOUTHWEST): HandPath.DASH,
            (Location.SOUTHWEST, Location.NORTHEAST): HandPath.DASH,
            (Location.SOUTHEAST, Location.NORTHWEST): HandPath.DASH,
            (Location.NORTHWEST, Location.SOUTHEAST): HandPath.DASH,
            # Static pairs (same location)
            (Location.NORTH, Location.NORTH): HandPath.STATIC,
            (Location.EAST, Location.EAST): HandPath.STATIC,
            (Location.SOUTH, Location.SOUTH): HandPath.STATIC,
            (Location.WEST, Location.WEST): HandPath.STATIC,
            (Location.NORTHEAST, Location.NORTHEAST): HandPath.STATIC,
            (Location.SOUTHEAST, Location.SOUTHEAST): HandPath.STATIC,
            (Location.SOUTHWEST, Location.SOUTHWEST): HandPath.STATIC,
            (Location.NORTHWEST, Location.NORTHWEST): HandPath.STATIC,
        }

        return direction_map.get((start_loc, end_loc), HandPath.STATIC)

    def _calculate_float_orientation(
        self, start_ori: Orientation, handpath_direction: HandPath
    ) -> Orientation:
        """Calculate orientation for float motions using legacy logic."""
        orientation_map = {
            (Orientation.IN, HandPath.CLOCKWISE): Orientation.CLOCK,
            (Orientation.IN, HandPath.COUNTER_CLOCKWISE): Orientation.COUNTER,
            (Orientation.OUT, HandPath.CLOCKWISE): Orientation.COUNTER,
            (Orientation.OUT, HandPath.COUNTER_CLOCKWISE): Orientation.CLOCK,
            (Orientation.CLOCK, HandPath.CLOCKWISE): Orientation.OUT,
            (Orientation.CLOCK, HandPath.COUNTER_CLOCKWISE): Orientation.IN,
            (Orientation.COUNTER, HandPath.CLOCKWISE): Orientation.IN,
            (Orientation.COUNTER, HandPath.COUNTER_CLOCKWISE): Orientation.OUT,
        }

        result_ori = orientation_map.get((start_ori, handpath_direction), start_ori)
        logger.debug(
            f"Float orientation: {start_ori} + {handpath_direction} -> {result_ori}"
        )

        return result_ori

    def _calculate_whole_turn_orientation(
        self, motion_type: MotionType, turns: int, start_ori: Orientation
    ) -> Orientation:
        """Calculate orientation for whole turn motions using legacy logic."""
        if motion_type in [MotionType.PRO, MotionType.STATIC]:
            result_ori = (
                start_ori if turns % 2 == 0 else self._switch_orientation(start_ori)
            )
        elif motion_type in [MotionType.ANTI, MotionType.DASH]:
            result_ori = (
                self._switch_orientation(start_ori) if turns % 2 == 0 else start_ori
            )
        else:
            result_ori = start_ori

        logger.debug(
            f"Whole turn: {motion_type.value} {turns} turns, {start_ori} -> {result_ori}"
        )

        return result_ori

    def _calculate_half_turn_orientation(
        self,
        motion_type: MotionType,
        turns: float,
        start_ori: Orientation,
        motion_data: MotionData,
    ) -> Orientation:
        """Calculate orientation for half turn motions using legacy logic."""
        prop_rot_dir = (
            motion_data.prop_rot_dir
            if motion_data.prop_rot_dir
            else RotationDirection.CLOCKWISE
        )

        if motion_type in [MotionType.ANTI, MotionType.DASH]:
            orientation_map = {
                (Orientation.IN, RotationDirection.CLOCKWISE): (
                    Orientation.CLOCK if turns % 2 == 0.5 else Orientation.COUNTER
                ),
                (Orientation.IN, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.COUNTER if turns % 2 == 0.5 else Orientation.CLOCK
                ),
                (Orientation.OUT, RotationDirection.CLOCKWISE): (
                    Orientation.COUNTER if turns % 2 == 0.5 else Orientation.CLOCK
                ),
                (Orientation.OUT, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.CLOCK if turns % 2 == 0.5 else Orientation.COUNTER
                ),
                (Orientation.CLOCK, RotationDirection.CLOCKWISE): (
                    Orientation.OUT if turns % 2 == 0.5 else Orientation.IN
                ),
                (Orientation.CLOCK, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.IN if turns % 2 == 0.5 else Orientation.OUT
                ),
                (Orientation.COUNTER, RotationDirection.CLOCKWISE): (
                    Orientation.IN if turns % 2 == 0.5 else Orientation.OUT
                ),
                (Orientation.COUNTER, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.OUT if turns % 2 == 0.5 else Orientation.IN
                ),
            }
        elif motion_type in [MotionType.PRO, MotionType.STATIC]:
            orientation_map = {
                (Orientation.IN, RotationDirection.CLOCKWISE): (
                    Orientation.COUNTER if turns % 2 == 0.5 else Orientation.CLOCK
                ),
                (Orientation.IN, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.CLOCK if turns % 2 == 0.5 else Orientation.COUNTER
                ),
                (Orientation.OUT, RotationDirection.CLOCKWISE): (
                    Orientation.CLOCK if turns % 2 == 0.5 else Orientation.COUNTER
                ),
                (Orientation.OUT, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.COUNTER if turns % 2 == 0.5 else Orientation.CLOCK
                ),
                (Orientation.CLOCK, RotationDirection.CLOCKWISE): (
                    Orientation.IN if turns % 2 == 0.5 else Orientation.OUT
                ),
                (Orientation.CLOCK, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.OUT if turns % 2 == 0.5 else Orientation.IN
                ),
                (Orientation.COUNTER, RotationDirection.CLOCKWISE): (
                    Orientation.OUT if turns % 2 == 0.5 else Orientation.IN
                ),
                (Orientation.COUNTER, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.IN if turns % 2 == 0.5 else Orientation.OUT
                ),
            }
        else:
            # Default fallback
            orientation_map = {}

        result_ori = orientation_map.get((start_ori, prop_rot_dir), start_ori)
        logger.debug(
            f"Half turn: {motion_type.value} {turns} turns {prop_rot_dir}, {start_ori} -> {result_ori}"
        )

        return result_ori

    def _switch_orientation(self, ori: Orientation) -> Orientation:
        """Switch orientation using legacy logic."""
        switch_map = {
            Orientation.IN: Orientation.OUT,
            Orientation.OUT: Orientation.IN,
            Orientation.CLOCK: Orientation.COUNTER,
            Orientation.COUNTER: Orientation.CLOCK,
        }
        return switch_map.get(ori, ori)

    def switch_orientation(self, orientation: Orientation) -> Orientation:
        """Switch between orientations using enum values."""
        switch_map = {
            Orientation.IN: Orientation.OUT,
            Orientation.OUT: Orientation.IN,
            Orientation.CLOCK: Orientation.COUNTER,
            Orientation.COUNTER: Orientation.CLOCK,
        }
        return switch_map.get(orientation, orientation)

    # Interface implementation methods
    def calculate_orientation(self, motion_data: Any, context: Any) -> Any:
        """Calculate orientation based on motion and context (interface implementation)."""
        if isinstance(motion_data, MotionData):
            start_orientation = (
                getattr(context, "start_orientation", Orientation.IN)
                if context
                else Orientation.IN
            )
            return self.calculate_end_orientation(motion_data, start_orientation)
        else:
            # Handle other motion data formats
            return Orientation.IN

    def get_orientation_adjustments(self, orientation: Any) -> dict[str, Any]:
        """Get adjustments for orientation (interface implementation)."""
        if isinstance(orientation, Orientation):
            return {
                "orientation": orientation.value,
                "switched": self.switch_orientation(orientation).value,
                "is_in_out": orientation in [Orientation.IN, Orientation.OUT],
                "is_clock_counter": orientation
                in [Orientation.CLOCK, Orientation.COUNTER],
            }
        else:
            return {"orientation": "unknown", "switched": "unknown"}

    def validate_orientation(self, orientation: Any) -> bool:
        """Validate orientation data (interface implementation)."""
        try:
            if isinstance(orientation, Orientation):
                return True
            elif isinstance(orientation, str):
                # Check if string can be converted to Orientation
                return orientation.upper() in [o.value for o in Orientation]
            else:
                return False
        except Exception:
            return False
