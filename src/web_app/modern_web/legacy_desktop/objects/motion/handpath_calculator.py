from __future__ import annotations
from collections import defaultdict

from data.constants import (
    CCW_HANDPATH,
    CW_HANDPATH,
    DASH,
    EAST,
    NORTH,
    NORTHEAST,
    NORTHWEST,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    STATIC,
    WEST,
)


class HandpathCalculator:
    """Calculates the hand rotation direction based on the start and end locations."""

    def __init__(self):
        """Initialize hand rotation direction mapping."""
        self.hand_rot_dir_map: defaultdict[tuple[str, str], str]

        clockwise_pairs = [(SOUTH, WEST), (WEST, NORTH), (NORTH, EAST), (EAST, SOUTH)]
        counter_clockwise_pairs = [
            (WEST, SOUTH),
            (NORTH, WEST),
            (EAST, NORTH),
            (SOUTH, EAST),
        ]
        diagonal_clockwise = [
            (NORTHEAST, SOUTHEAST),
            (SOUTHEAST, SOUTHWEST),
            (SOUTHWEST, NORTHWEST),
            (NORTHWEST, NORTHEAST),
        ]
        diagonal_counter_clockwise = [
            (NORTHEAST, NORTHWEST),
            (NORTHWEST, SOUTHWEST),
            (SOUTHWEST, SOUTHEAST),
            (SOUTHEAST, NORTHEAST),
        ]
        dash_pairs = [
            (SOUTH, NORTH),
            (WEST, EAST),
            (NORTH, SOUTH),
            (EAST, WEST),
            (NORTHEAST, SOUTHWEST),
            (SOUTHEAST, NORTHWEST),
            (SOUTHWEST, NORTHEAST),
            (NORTHWEST, SOUTHEAST),
        ]
        static_pairs = [
            (NORTH, NORTH),
            (EAST, EAST),
            (SOUTH, SOUTH),
            (WEST, WEST),
            (NORTHEAST, NORTHEAST),
            (SOUTHEAST, SOUTHEAST),
            (SOUTHWEST, SOUTHWEST),
            (NORTHWEST, NORTHWEST),
        ]

        # Properly define as an instance variable
        self.hand_rot_dir_map = defaultdict(
            lambda: "NO HAND ROTATION FOUND",
            {
                **dict.fromkeys(clockwise_pairs + diagonal_clockwise, CW_HANDPATH),
                **dict.fromkeys(
                    counter_clockwise_pairs + diagonal_counter_clockwise, CCW_HANDPATH
                ),
                **dict.fromkeys(dash_pairs, DASH),
                **dict.fromkeys(static_pairs, STATIC),
            },
        )

    def get_hand_rot_dir(self, start_loc: str, end_loc: str) -> str:
        """
        Returns the hand rotation direction based on the start and end locations.

        :param start_loc: The starting location.
        :param end_loc: The ending location.
        :return: The hand rotation direction (CLOCKWISE, COUNTER_CLOCKWISE, DASH, or STATIC).
        """
        if not isinstance(start_loc, str) or not isinstance(end_loc, str):
            return "NO HAND ROTATION FOUND"
        return self.hand_rot_dir_map[(start_loc, end_loc)]
