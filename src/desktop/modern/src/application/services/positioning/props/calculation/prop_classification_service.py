"""
Prop Classification Service

Pure service for classifying props by size and type.
Extracted from PropManagementService to follow single responsibility principle.

PROVIDES:
- Prop size classification (big, medium, small)
- Repositioning strategy determination
- Prop rotation angle calculations
- Overlap detection logic
"""

from typing import Dict, List
from abc import ABC, abstractmethod

from domain.models.core_models import (
    BeatData,
    MotionData,
    Location,
    Orientation,
)
from domain.models.pictograph_models import PropType


class IPropClassificationService(ABC):
    """Interface for prop classification operations."""

    @abstractmethod
    def classify_props_by_size(self, beat_data: BeatData) -> Dict[str, List]:
        """Classify props by size categories (big, small, hands)."""

    @abstractmethod
    def get_repositioning_strategy(
        self, beat_data: BeatData, prop_classification: Dict[str, List]
    ) -> str:
        """Determine repositioning strategy based on prop classification and letter."""

    @abstractmethod
    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """Detect if props overlap based on position and category."""

    @abstractmethod
    def calculate_prop_rotation_angle(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> float:
        """Calculate prop rotation angle based on motion data and orientation."""


class PropClassificationService(IPropClassificationService):
    """
    Pure service for prop classification operations.

    Handles prop categorization and strategy determination without external dependencies.
    Uses immutable data patterns following TKA architecture.
    """

    def __init__(self):
        """Initialize prop classification service."""
        # Prop size categories
        self._big_props = {
            PropType.CLUB,
            PropType.EIGHTRINGS,
            PropType.BIG_EIGHT_RINGS,
            PropType.BIGHOOP,
            PropType.BIGSTAFF,
            PropType.SWORD,
            PropType.GUITAR,
        }

        self._medium_props = {
            PropType.DOUBLESTAR,
            PropType.BIGDOUBLESTAR,
            PropType.BIGBUUGENG,
        }

        self._small_props = {
            PropType.BUUGENG,
            PropType.TRIAD,
            PropType.MINIHOOP,
            PropType.STAFF,
            PropType.FAN,
            PropType.UKULELE,
            PropType.SIMPLESTAFF,
            PropType.FRACTALGENG,
            PropType.QUIAD,
            PropType.CHICKEN,
            PropType.TRIQUETRA,
            PropType.TRIQUETRA2,
        }

        self._hand_props = {
            PropType.HAND,
        }

    def classify_props_by_size(self, beat_data: BeatData) -> Dict[str, List]:
        """
        Classify props by size categories (big, small, hands).

        Based on PropClassifier logic.
        """
        classification = {
            "big_props": [],
            "medium_props": [],
            "small_props": [],
            "hands": [],
        }

        # Get current prop type (would normally come from settings)
        current_prop_type = self._get_current_prop_type()

        # Classify the current prop type
        if current_prop_type in self._big_props:
            classification["big_props"].append(current_prop_type)
        elif current_prop_type in self._medium_props:
            classification["medium_props"].append(current_prop_type)
        elif current_prop_type in self._small_props:
            classification["small_props"].append(current_prop_type)
        elif current_prop_type in self._hand_props:
            classification["hands"].append(current_prop_type)

        # If both blue and red motions exist, add prop for both
        if beat_data.blue_motion and beat_data.red_motion:
            # Duplicate the classification for both props
            for category in classification:
                if classification[category]:
                    classification[category].append(current_prop_type)

        return classification

    def get_repositioning_strategy(
        self, beat_data: BeatData, prop_classification: Dict[str, List]
    ) -> str:
        """
        Determine repositioning strategy based on prop classification and letter.

        Returns strategy name that determines how props should be separated.
        """
        letter = beat_data.letter or ""

        # Check prop categories
        has_big_props = bool(prop_classification["big_props"])
        has_medium_props = bool(prop_classification["medium_props"])
        has_small_props = bool(prop_classification["small_props"])
        has_hands = bool(prop_classification["hands"])

        if has_big_props and len(prop_classification["big_props"]) == 2:
            return "big_prop_repositioning"
        elif has_medium_props and len(prop_classification["medium_props"]) == 2:
            return "medium_prop_repositioning"
        elif has_small_props and len(prop_classification["small_props"]) == 2:
            return "small_prop_repositioning"
        elif has_hands:
            return "hand_repositioning"
        else:
            return "default_repositioning"

    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """
        Detect if props overlap based on their end positions and orientations.

        Props overlap when they end at the same location with the same orientation.
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return False

        blue_motion = beat_data.blue_motion
        red_motion = beat_data.red_motion

        # Check if both motions end at same location
        if blue_motion.end_loc != red_motion.end_loc:
            return False

        # Calculate end orientations for both motions
        blue_end_ori = self._calculate_end_orientation(blue_motion)
        red_end_ori = self._calculate_end_orientation(red_motion)

        # Props overlap if they end at same location with same orientation
        return blue_end_ori == red_end_ori

    def calculate_prop_rotation_angle(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> float:
        """Calculate prop rotation angle based on motion data and orientation."""
        location = motion_data.end_loc

        # Diamond grid orientation-based rotation mapping (simplified for Modern)
        angle_map = {
            Orientation.IN: {
                Location.NORTH: 90,
                Location.SOUTH: 270,
                Location.WEST: 0,
                Location.EAST: 180,
            },
            Orientation.OUT: {
                Location.NORTH: 270,
                Location.SOUTH: 90,
                Location.WEST: 180,
                Location.EAST: 0,
            },
        }

        # Calculate end orientation for this motion
        end_orientation = self._calculate_end_orientation(
            motion_data, start_orientation
        )

        # Get rotation angle from mapping
        orientation_map = angle_map.get(end_orientation, angle_map[Orientation.IN])
        rotation_angle = orientation_map.get(location, 0)

        return float(rotation_angle)

    def get_prop_size_category(self, prop_type: PropType) -> str:
        """Get size category for prop type."""
        if prop_type in self._big_props:
            return "big"
        elif prop_type in self._medium_props:
            return "medium"
        elif prop_type in self._small_props:
            return "small"
        elif prop_type in self._hand_props:
            return "hand"
        else:
            return "unknown"

    def is_beta_ending_letter(self, letter: str) -> bool:
        """Check if letter ends at beta positions."""
        beta_ending_letters = [
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "Y",
            "Z",
            "Y-",
            "Z-",
            "Ψ",
            "Ψ-",
            "β",
        ]
        return letter in beta_ending_letters

    def _calculate_end_orientation(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for placement calculations."""
        motion_type = motion_data.motion_type
        turns = motion_data.turns

        if turns in {0, 1, 2, 3}:
            if motion_type.value in ["pro", "static"]:
                return (
                    start_orientation
                    if int(turns) % 2 == 0
                    else self._switch_orientation(start_orientation)
                )
            elif motion_type.value in ["anti", "dash"]:
                return (
                    self._switch_orientation(start_orientation)
                    if int(turns) % 2 == 0
                    else start_orientation
                )

        return start_orientation

    def _switch_orientation(self, orientation: Orientation) -> Orientation:
        """Switch between IN and OUT orientations."""
        return Orientation.OUT if orientation == Orientation.IN else Orientation.IN

    def _get_current_prop_type(self) -> PropType:
        """
        Get current prop type from settings.

        For now returns a default, but should integrate with settings system.
        """
        # TODO: Integrate with actual settings system
        return PropType.HAND  # Default to smallest prop
