"""
Prop Overlap Detector Service

Pure service for detecting prop overlaps based on position and orientation.
Extracted from PropManagementService to follow single responsibility principle.

PROVIDES:
- Prop overlap detection based on end positions and orientations
- End orientation calculations
- Orientation switching logic
"""

from abc import ABC, abstractmethod

from desktop.modern.domain.models import BeatData, MotionData, MotionType, Orientation


class IPropOverlapDetector(ABC):
    """Interface for prop overlap detection operations."""

    @abstractmethod
    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """Detect if props overlap based on position and orientation."""

    @abstractmethod
    def calculate_end_orientation(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for placement calculations."""

    @abstractmethod
    def switch_orientation(self, orientation: Orientation) -> Orientation:
        """Switch between IN and OUT orientations."""


class PropOverlapDetector(IPropOverlapDetector):
    """
    Pure service for prop overlap detection.

    Handles detection of prop overlaps based on end positions and orientations.
    Uses motion data to calculate final prop positions and orientations.
    """

    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """
        Detect if props overlap based on their end positions and orientations.

        Props overlap when they end at the same location with the same orientation.
        """
        # Get motion data from pictograph_data
        blue_motion = None
        red_motion = None

        if beat_data.pictograph_data and beat_data.pictograph_data.motions:
            blue_motion = beat_data.pictograph_data.motions.get("blue")
            red_motion = beat_data.pictograph_data.motions.get("red")

        if not blue_motion or not red_motion:
            return False

        # Check if both motions end at same location
        if blue_motion.end_loc != red_motion.end_loc:
            return False

        # Calculate end orientations for both motions
        blue_end_ori = self.calculate_end_orientation(blue_motion)
        red_end_ori = self.calculate_end_orientation(red_motion)

        # Props overlap if they end at same location with same orientation
        return blue_end_ori == red_end_ori

    def calculate_end_orientation(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for placement calculations."""
        motion_type = motion_data.motion_type
        turns = motion_data.turns

        # Convert float turns to int for calculation
        int_turns = int(turns)

        if int_turns in {0, 1, 2, 3}:
            if motion_type in [MotionType.PRO, MotionType.STATIC]:
                return (
                    start_orientation
                    if int_turns % 2 == 0
                    else self.switch_orientation(start_orientation)
                )
            elif motion_type in [MotionType.ANTI, MotionType.DASH]:
                return (
                    self.switch_orientation(start_orientation)
                    if int_turns % 2 == 0
                    else start_orientation
                )

        return start_orientation

    def switch_orientation(self, orientation: Orientation) -> Orientation:
        """Switch between IN and OUT orientations."""
        return Orientation.OUT if orientation == Orientation.IN else Orientation.IN
