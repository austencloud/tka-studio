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

from domain.models.core_models import Location, MotionData, MotionType, Orientation

logger = logging.getLogger(__name__)


class OrientationCalculator:
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
        start_ori = start_orientation.value.lower()

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
    ) -> str:
        """Calculate handpath direction using legacy logic."""
        # Simplified handpath calculation based on legacy HandpathCalculator
        direction_map = {
            # Clockwise pairs
            (Location.NORTH, Location.EAST): "cw_handpath",
            (Location.EAST, Location.SOUTH): "cw_handpath",
            (Location.SOUTH, Location.WEST): "cw_handpath",
            (Location.WEST, Location.NORTH): "cw_handpath",
            (Location.NORTHEAST, Location.SOUTHEAST): "cw_handpath",
            (Location.SOUTHEAST, Location.SOUTHWEST): "cw_handpath",
            (Location.SOUTHWEST, Location.NORTHWEST): "cw_handpath",
            (Location.NORTHWEST, Location.NORTHEAST): "cw_handpath",
            # Counter-clockwise pairs
            (Location.NORTH, Location.WEST): "ccw_handpath",
            (Location.WEST, Location.SOUTH): "ccw_handpath",
            (Location.SOUTH, Location.EAST): "ccw_handpath",
            (Location.EAST, Location.NORTH): "ccw_handpath",
            (Location.NORTHEAST, Location.NORTHWEST): "ccw_handpath",
            (Location.NORTHWEST, Location.SOUTHWEST): "ccw_handpath",
            (Location.SOUTHWEST, Location.SOUTHEAST): "ccw_handpath",
            (Location.SOUTHEAST, Location.NORTHEAST): "ccw_handpath",
            # Dash pairs
            (Location.NORTH, Location.SOUTH): "dash",
            (Location.SOUTH, Location.NORTH): "dash",
            (Location.EAST, Location.WEST): "dash",
            (Location.WEST, Location.EAST): "dash",
            (Location.NORTHEAST, Location.SOUTHWEST): "dash",
            (Location.SOUTHWEST, Location.NORTHEAST): "dash",
            (Location.SOUTHEAST, Location.NORTHWEST): "dash",
            (Location.NORTHWEST, Location.SOUTHEAST): "dash",
            # Static pairs (same location)
            (Location.NORTH, Location.NORTH): "static",
            (Location.EAST, Location.EAST): "static",
            (Location.SOUTH, Location.SOUTH): "static",
            (Location.WEST, Location.WEST): "static",
            (Location.NORTHEAST, Location.NORTHEAST): "static",
            (Location.SOUTHEAST, Location.SOUTHEAST): "static",
            (Location.SOUTHWEST, Location.SOUTHWEST): "static",
            (Location.NORTHWEST, Location.NORTHWEST): "static",
        }

        return direction_map.get((start_loc, end_loc), "static")

    def _calculate_float_orientation(
        self, start_ori: str, handpath_direction: str
    ) -> Orientation:
        """Calculate orientation for float motions using legacy logic."""
        orientation_map = {
            ("in", "cw_handpath"): "clock",
            ("in", "ccw_handpath"): "counter",
            ("out", "cw_handpath"): "counter",
            ("out", "ccw_handpath"): "clock",
            ("clock", "cw_handpath"): "out",
            ("clock", "ccw_handpath"): "in",
            ("counter", "cw_handpath"): "in",
            ("counter", "ccw_handpath"): "out",
        }

        result_ori = orientation_map.get((start_ori, handpath_direction), start_ori)
        logger.debug(
            f"Float orientation: {start_ori} + {handpath_direction} -> {result_ori}"
        )

        # Convert back to Orientation enum
        ori_map = {
            "in": Orientation.IN,
            "out": Orientation.OUT,
            "clock": Orientation.CLOCK,
            "counter": Orientation.COUNTER,
        }
        return ori_map.get(result_ori, Orientation.IN)

    def _calculate_whole_turn_orientation(
        self, motion_type: MotionType, turns: int, start_ori: str
    ) -> Orientation:
        """Calculate orientation for whole turn motions using legacy logic."""
        if motion_type in [MotionType.PRO, MotionType.STATIC]:
            result_ori = (
                start_ori if turns % 2 == 0 else self._switch_orientation_str(start_ori)
            )
        elif motion_type in [MotionType.ANTI, MotionType.DASH]:
            result_ori = (
                self._switch_orientation_str(start_ori) if turns % 2 == 0 else start_ori
            )
        else:
            result_ori = start_ori

        logger.debug(
            f"Whole turn: {motion_type.value} {turns} turns, {start_ori} -> {result_ori}"
        )

        # Convert back to Orientation enum
        ori_map = {
            "in": Orientation.IN,
            "out": Orientation.OUT,
            "clock": Orientation.CLOCK,
            "counter": Orientation.COUNTER,
        }
        return ori_map.get(result_ori, Orientation.IN)

    def _calculate_half_turn_orientation(
        self,
        motion_type: MotionType,
        turns: float,
        start_ori: str,
        motion_data: MotionData,
    ) -> Orientation:
        """Calculate orientation for half turn motions using legacy logic."""
        prop_rot_dir = (
            motion_data.prop_rot_dir.value.lower()
            if motion_data.prop_rot_dir
            else "clockwise"
        )

        if motion_type in [MotionType.ANTI, MotionType.DASH]:
            orientation_map = {
                ("in", "clockwise"): ("clock" if turns % 2 == 0.5 else "counter"),
                ("in", "counter_clockwise"): (
                    "counter" if turns % 2 == 0.5 else "clock"
                ),
                ("out", "clockwise"): ("counter" if turns % 2 == 0.5 else "clock"),
                ("out", "counter_clockwise"): (
                    "clock" if turns % 2 == 0.5 else "counter"
                ),
                ("clock", "clockwise"): ("out" if turns % 2 == 0.5 else "in"),
                ("clock", "counter_clockwise"): ("in" if turns % 2 == 0.5 else "out"),
                ("counter", "clockwise"): ("in" if turns % 2 == 0.5 else "out"),
                ("counter", "counter_clockwise"): ("out" if turns % 2 == 0.5 else "in"),
            }
        elif motion_type in [MotionType.PRO, MotionType.STATIC]:
            orientation_map = {
                ("in", "clockwise"): ("counter" if turns % 2 == 0.5 else "clock"),
                ("in", "counter_clockwise"): (
                    "clock" if turns % 2 == 0.5 else "counter"
                ),
                ("out", "clockwise"): ("clock" if turns % 2 == 0.5 else "counter"),
                ("out", "counter_clockwise"): (
                    "counter" if turns % 2 == 0.5 else "clock"
                ),
                ("clock", "clockwise"): ("in" if turns % 2 == 0.5 else "out"),
                ("clock", "counter_clockwise"): ("out" if turns % 2 == 0.5 else "in"),
                ("counter", "clockwise"): ("out" if turns % 2 == 0.5 else "in"),
                ("counter", "counter_clockwise"): ("in" if turns % 2 == 0.5 else "out"),
            }
        else:
            # Default fallback
            orientation_map = {}

        result_ori = orientation_map.get((start_ori, prop_rot_dir), start_ori)
        logger.debug(
            f"Half turn: {motion_type.value} {turns} turns {prop_rot_dir}, {start_ori} -> {result_ori}"
        )

        # Convert back to Orientation enum
        ori_map = {
            "in": Orientation.IN,
            "out": Orientation.OUT,
            "clock": Orientation.CLOCK,
            "counter": Orientation.COUNTER,
        }
        return ori_map.get(result_ori, Orientation.IN)

    def _switch_orientation_str(self, ori: str) -> str:
        """Switch orientation string using legacy logic."""
        switch_map = {"in": "out", "out": "in", "clock": "counter", "counter": "clock"}
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
