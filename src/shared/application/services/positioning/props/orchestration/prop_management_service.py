"""
Prop Management Service - Beta Positioning and Prop Operations

Handles all prop-related positioning logic including:
- Beta prop positioning for overlapping props
- Prop separation based on motion and letter types
- Special placement overrides for specific configurations
- Offset calculations based on prop types and sizes

This service is responsible for determining when and how to separate props
to avoid overlaps, particularly for beta-ending letters.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any

from desktop.modern.core.types import Point
from desktop.modern.domain.models import (
    BeatData,
    Location,
    MotionData,
    MotionType,
    Orientation,
)
from desktop.modern.domain.models.pictograph_data import PictographData

# Event-driven architecture imports
if TYPE_CHECKING:
    from desktop.modern.core.events import IEventBus

try:
    from desktop.modern.core.events import (
        EventPriority,
        IEventBus,
        PropPositionedEvent,
        get_event_bus,
    )

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    # For tests or when event system is not available
    IEventBus = None
    get_event_bus = None
    PropPositionedEvent = None
    EventPriority = None
    EVENT_SYSTEM_AVAILABLE = False
from desktop.modern.domain.models.enums import PropType


class SeparationDirection(Enum):
    """Separation directions for prop positioning."""

    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    DOWNRIGHT = "downright"
    UPLEFT = "upleft"
    DOWNLEFT = "downleft"
    UPRIGHT = "upright"


class IPropManagementService(ABC):
    """Interface for prop management operations."""

    @abstractmethod
    def should_apply_beta_positioning(self, beat_data: BeatData) -> bool:
        """Determine if beta positioning should be applied."""

    @abstractmethod
    def apply_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """Apply beta prop positioning if conditions are met."""

    @abstractmethod
    def calculate_separation_offsets(self, beat_data: BeatData) -> tuple[Point, Point]:
        """Calculate separation offsets for blue and red props."""

    @abstractmethod
    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """Detect if props overlap based on position and category."""


class PropManagementService(IPropManagementService):
    """
    Prop management service handling beta positioning and prop operations.

    This service manages:
    - Detection of beta-ending letters requiring prop separation
    - Calculation of prop separation offsets based on size and type
    - Application of special placement overrides
    - Prop overlap detection and resolution
    """

    def __init__(self):
        # Event system integration

        self._subscription_ids: list[str] = []

        # Beta prop positioning constants
        self._large_offset_divisor = 60
        self._medium_offset_divisor = 50
        self._small_offset_divisor = 45
        self._scene_reference_size = 950

        # Initialize prop offset mapping based on available PropType
        self._init_prop_offset_map()

        # Direction constants
        self.LEFT = "left"
        self.RIGHT = "right"
        self.UP = "up"
        self.DOWN = "down"
        self.UPLEFT = "upleft"
        self.UPRIGHT = "upright"
        self.DOWNLEFT = "downleft"
        self.DOWNRIGHT = "downright"

        # Use JSONConfigurator singleton for special placements
        self._json_configurator = self._get_json_configurator()

    def _init_prop_offset_map(self) -> None:
        """Initialize prop offset mapping based on modern PropType enum."""
        self._prop_offset_map = {
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

    def should_apply_beta_positioning(self, beat_data: BeatData) -> bool:
        """
        Determine if beta positioning should be applied.

        Beta positioning is applied when:
        1. Letter is one that ends at beta positions (G, H, I, J, K, L, Y, Z, Y-, Z-, Ψ, Ψ-, β)
        """
        if not beat_data or not beat_data.letter:
            return False

        # Letters that end at beta positions
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

        return beat_data.letter in beta_ending_letters

    def detect_prop_overlap(self, beat_data: BeatData) -> bool:
        """
        Detect if props overlap based on their end positions and orientations.

        Props overlap when they end at the same location with the same orientation.
        """
        # Get motion data from pictograph_data instead of beat_data
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
        blue_end_ori = self._calculate_end_orientation(blue_motion)
        red_end_ori = self._calculate_end_orientation(red_motion)

        # Props overlap if they end at same location with same orientation
        overlap_detected = blue_end_ori == red_end_ori

        return overlap_detected

    def apply_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """
        Apply beta prop positioning if conditions are met.

        First checks for manual swap overrides, then applies algorithmic positioning.
        """
        if not self.should_apply_beta_positioning(beat_data):
            return beat_data

        # Check for swap overrides first
        if self._has_swap_override(beat_data):
            result = self._apply_swap_override(beat_data)
        else:
            # Apply algorithmic beta positioning
            result = self._apply_algorithmic_beta_positioning(beat_data)

        return result

    def calculate_separation_offsets(
        self, pictograph_data: PictographData
    ) -> tuple[Point, Point]:
        """
        Calculate separation offsets for blue and red props.

        Returns tuple of (blue_offset, red_offset) as Point objects.
        """
        # Get motion data from pictograph_data instead of beat_data
        blue_motion = None
        red_motion = None

        if pictograph_data and pictograph_data.motions:
            blue_motion = pictograph_data.motions.get("blue")
            red_motion = pictograph_data.motions.get("red")

        if not blue_motion or not red_motion:
            return Point(0, 0), Point(0, 0)

        # SPECIAL CASE: Letter I positioning coordination
        if pictograph_data.letter == "I":
            blue_direction, red_direction = self._calculate_letter_I_directions(
                blue_motion, red_motion
            )
        else:
            # Calculate separation directions based on motion types and letter
            blue_direction = self._calculate_separation_direction(
                blue_motion, "blue", pictograph_data.letter
            )
            red_direction = self._calculate_separation_direction(
                red_motion, "red", pictograph_data.letter
            )

        # Calculate offsets based on directions and prop types
        blue_offset = self.calculate_directional_offset(
            blue_direction, self._get_current_prop_type()
        )
        red_offset = self.calculate_directional_offset(
            red_direction, self._get_current_prop_type()
        )

        return blue_offset, red_offset

    def _calculate_end_orientation(
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
                    else self._switch_orientation(start_orientation)
                )
            elif motion_type in [MotionType.ANTI, MotionType.DASH]:
                return (
                    self._switch_orientation(start_orientation)
                    if int_turns % 2 == 0
                    else start_orientation
                )

        return start_orientation

    def _switch_orientation(self, orientation: Orientation) -> Orientation:
        """Switch between IN and OUT orientations."""
        return Orientation.OUT if orientation == Orientation.IN else Orientation.IN

    def _calculate_separation_direction(
        self, motion: MotionData, color: str, letter: str | None = None
    ) -> SeparationDirection:
        """
        Calculate the direction props should be separated.

        SPECIAL CASE: Letter I positioning
        Letter I uses PRO/ANTI motion type logic instead of location-based logic
        """

        # SPECIAL CASE: Letter I positioning
        if letter == "I":
            return self._calculate_letter_I_direction(motion, color, letter)

        # Standard positioning logic (replicate the get_dir_for_non_shift method exactly)
        location = motion.end_loc

        # Determine if prop is radial or nonradial based on end orientation
        # Validated logic: RADIAL = IN/OUT, NONRADIAL = CLOCK/COUNTER
        is_radial = motion.end_ori in [Orientation.IN, Orientation.OUT]

        # Determine grid mode based on location
        if location in [
            Location.NORTH,
            Location.EAST,
            Location.SOUTH,
            Location.WEST,
        ]:
            grid_mode = "diamond"
        else:
            grid_mode = "box"

        if grid_mode == "diamond":
            if is_radial:
                # Diamond layer reposition map for RADIAL
                direction_map = {
                    (Location.NORTH, "red"): SeparationDirection.RIGHT,
                    (Location.NORTH, "blue"): SeparationDirection.LEFT,
                    (Location.EAST, "red"): SeparationDirection.DOWN,
                    (Location.EAST, "blue"): SeparationDirection.UP,
                    (Location.SOUTH, "red"): SeparationDirection.LEFT,
                    (Location.SOUTH, "blue"): SeparationDirection.RIGHT,
                    (Location.WEST, "blue"): SeparationDirection.DOWN,
                    (Location.WEST, "red"): SeparationDirection.UP,
                }
            else:
                # Diamond layer reposition map for NONRADIAL
                direction_map = {
                    (Location.NORTH, "red"): SeparationDirection.UP,
                    (Location.NORTH, "blue"): SeparationDirection.DOWN,
                    (Location.SOUTH, "red"): SeparationDirection.UP,
                    (Location.SOUTH, "blue"): SeparationDirection.DOWN,
                    (Location.EAST, "red"): SeparationDirection.RIGHT,
                    (Location.WEST, "blue"): SeparationDirection.LEFT,
                    (Location.WEST, "red"): SeparationDirection.RIGHT,
                    (Location.EAST, "blue"): SeparationDirection.LEFT,
                }
        else:  # box grid
            if is_radial:
                # Box layer reposition map for RADIAL
                direction_map = {
                    (Location.NORTHEAST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.NORTHEAST, "blue"): SeparationDirection.UPLEFT,
                    (Location.SOUTHEAST, "red"): SeparationDirection.UPRIGHT,
                    (Location.SOUTHEAST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.SOUTHWEST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.SOUTHWEST, "blue"): SeparationDirection.UPLEFT,
                    (Location.NORTHWEST, "red"): SeparationDirection.UPRIGHT,
                    (Location.NORTHWEST, "blue"): SeparationDirection.DOWNLEFT,
                }
            else:
                # Box layer reposition map for NONRADIAL
                direction_map = {
                    (Location.NORTHEAST, "red"): SeparationDirection.UPRIGHT,
                    (Location.NORTHEAST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.SOUTHEAST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.SOUTHEAST, "blue"): SeparationDirection.UPLEFT,
                    (Location.SOUTHWEST, "red"): SeparationDirection.UPRIGHT,
                    (Location.SOUTHWEST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.NORTHWEST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.NORTHWEST, "blue"): SeparationDirection.UPLEFT,
                }

        return direction_map.get((location, color), SeparationDirection.RIGHT)

    def _calculate_letter_I_directions(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> tuple[SeparationDirection, SeparationDirection]:
        """
        Calculate directions for letter I using PRO/ANTI coordination.

        This replicates the legacy reposition_I logic:
        1. Find which motion is PRO
        2. Calculate direction for the PRO motion
        3. ANTI motion gets opposite direction

        Returns:
            (blue_direction, red_direction)
        """
        from desktop.modern.domain.models.enums import MotionType

        # Identify PRO and ANTI motions
        if red_motion.motion_type == MotionType.PRO:
            pro_motion = red_motion
            pro_color = "red"
        elif blue_motion.motion_type == MotionType.PRO:
            pro_motion = blue_motion
            pro_color = "blue"
        else:
            # Fallback if neither is PRO (shouldn't happen in letter I)
            # Use standard directions
            blue_direction = self._calculate_standard_direction(blue_motion, "blue")
            red_direction = self._calculate_standard_direction(red_motion, "red")
            return blue_direction, red_direction

        # Calculate direction for PRO motion
        pro_direction = self._calculate_standard_direction(pro_motion, pro_color)

        # ANTI motion gets opposite direction
        anti_direction = self._get_opposite_direction(pro_direction)

        # Return directions in correct order (blue, red)
        if pro_color == "red":
            return anti_direction, pro_direction  # blue=anti, red=pro
        else:
            return pro_direction, anti_direction  # blue=pro, red=anti

    def _calculate_letter_I_direction(
        self, motion: MotionData, color: str, letter: str
    ) -> SeparationDirection:
        """
        Calculate direction for letter I props using PRO/ANTI motion logic.

        For letter I, the PRO prop and ANTI prop should always move in opposite directions,
        regardless of their end locations. This replicates the legacy reposition_I() logic.

        Algorithm:
        1. Find the PRO motion (regardless of color)
        2. Calculate direction for the PRO motion
        3. ANTI motion always gets the opposite of PRO direction
        """
        from desktop.modern.domain.models.enums import MotionType

        # We need both motions to determine which is PRO and which is ANTI
        # For now, we'll handle the current motion and assume the caller
        # will handle the pairing logic correctly
        # Calculate the standard direction for this motion
        standard_direction = self._calculate_standard_direction(motion, color)

        if motion.motion_type == MotionType.PRO:
            # PRO motion uses its standard direction
            return standard_direction
        elif motion.motion_type == MotionType.ANTI:
            # ANTI motion should use opposite of PRO motion's direction
            # Since we don't have access to the PRO motion here,
            # we'll need to implement this differently

            # For now, we need to rethink this approach
            # The legacy system calculates PRO direction first, then makes ANTI opposite
            # But our service calculates each motion independently

            # Temporary fix: return opposite of standard direction
            # This may not be correct in all cases
            return self._get_opposite_direction(standard_direction)
        else:
            # Fallback to standard logic for non-PRO/ANTI motions
            return standard_direction

    def _calculate_standard_direction(
        self, motion: MotionData, color: str
    ) -> SeparationDirection:
        """Calculate direction using standard location/color mapping."""
        location = motion.end_loc
        is_radial = motion.end_ori in [Orientation.IN, Orientation.OUT]

        # Determine grid mode based on location
        if location in [Location.NORTH, Location.EAST, Location.SOUTH, Location.WEST]:
            grid_mode = "diamond"
        else:
            grid_mode = "box"

        if grid_mode == "diamond":
            if is_radial:
                direction_map = {
                    (Location.NORTH, "red"): SeparationDirection.RIGHT,
                    (Location.NORTH, "blue"): SeparationDirection.LEFT,
                    (Location.EAST, "red"): SeparationDirection.DOWN,
                    (Location.EAST, "blue"): SeparationDirection.UP,
                    (Location.SOUTH, "red"): SeparationDirection.LEFT,
                    (Location.SOUTH, "blue"): SeparationDirection.RIGHT,
                    (Location.WEST, "blue"): SeparationDirection.DOWN,
                    (Location.WEST, "red"): SeparationDirection.UP,
                }
            else:
                direction_map = {
                    (Location.NORTH, "red"): SeparationDirection.UP,
                    (Location.NORTH, "blue"): SeparationDirection.DOWN,
                    (Location.SOUTH, "red"): SeparationDirection.UP,
                    (Location.SOUTH, "blue"): SeparationDirection.DOWN,
                    (Location.EAST, "red"): SeparationDirection.RIGHT,
                    (Location.WEST, "blue"): SeparationDirection.LEFT,
                    (Location.WEST, "red"): SeparationDirection.RIGHT,
                    (Location.EAST, "blue"): SeparationDirection.LEFT,
                }
        else:  # box grid
            if is_radial:
                direction_map = {
                    (Location.NORTHEAST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.NORTHEAST, "blue"): SeparationDirection.UPLEFT,
                    (Location.SOUTHEAST, "red"): SeparationDirection.UPRIGHT,
                    (Location.SOUTHEAST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.SOUTHWEST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.SOUTHWEST, "blue"): SeparationDirection.UPLEFT,
                    (Location.NORTHWEST, "red"): SeparationDirection.UPRIGHT,
                    (Location.NORTHWEST, "blue"): SeparationDirection.DOWNLEFT,
                }
            else:
                direction_map = {
                    (Location.NORTHEAST, "red"): SeparationDirection.UPRIGHT,
                    (Location.NORTHEAST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.SOUTHEAST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.SOUTHEAST, "blue"): SeparationDirection.UPLEFT,
                    (Location.SOUTHWEST, "red"): SeparationDirection.UPRIGHT,
                    (Location.SOUTHWEST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.NORTHWEST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.NORTHWEST, "blue"): SeparationDirection.UPLEFT,
                }

        return direction_map.get((location, color), SeparationDirection.RIGHT)

    def _get_opposite_direction(
        self, direction: SeparationDirection
    ) -> SeparationDirection:
        """Get opposite direction for symmetric positioning."""
        opposite_map = {
            SeparationDirection.LEFT: SeparationDirection.RIGHT,
            SeparationDirection.RIGHT: SeparationDirection.LEFT,
            SeparationDirection.UP: SeparationDirection.DOWN,
            SeparationDirection.DOWN: SeparationDirection.UP,
            SeparationDirection.UPLEFT: SeparationDirection.DOWNRIGHT,
            SeparationDirection.UPRIGHT: SeparationDirection.DOWNLEFT,
            SeparationDirection.DOWNLEFT: SeparationDirection.UPRIGHT,
            SeparationDirection.DOWNRIGHT: SeparationDirection.UPLEFT,
        }
        return opposite_map.get(direction, direction)

    def calculate_directional_offset(
        self, direction: SeparationDirection, prop_type: PropType
    ) -> Point:
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
            SeparationDirection.LEFT: Point(-base_offset, 0),
            SeparationDirection.RIGHT: Point(base_offset, 0),
            SeparationDirection.UP: Point(0, -base_offset),
            SeparationDirection.DOWN: Point(0, base_offset),
            SeparationDirection.DOWNRIGHT: Point(diagonal_offset, diagonal_offset),
            SeparationDirection.UPLEFT: Point(-diagonal_offset, -diagonal_offset),
            SeparationDirection.DOWNLEFT: Point(-diagonal_offset, diagonal_offset),
            SeparationDirection.UPRIGHT: Point(diagonal_offset, -diagonal_offset),
        }

        return offset_map.get(direction, Point(0, 0))

    def _get_current_prop_type(self) -> PropType:
        """
        Get current prop type from settings.

        For now returns a default, but should integrate with settings system.
        """  # TODO: Integrate with actual settings system
        return PropType.HAND  # Default to smallest offset

    def _has_swap_override(self, beat_data: BeatData) -> bool:
        """Check if beat has manual swap override in special placements."""
        special_placements = self._get_special_placements()
        if not special_placements:
            return False

        override_key = self._generate_override_key(beat_data)
        return override_key in special_placements

    def _generate_override_key(self, beat_data: BeatData) -> str:
        """
        Generate key for swap override lookup.

        Based on validated logic for special placement keys.
        """
        # Get motion data from pictograph_data instead of beat_data
        blue_motion = None
        red_motion = None

        if beat_data.pictograph_data and beat_data.pictograph_data.motions:
            blue_motion = beat_data.pictograph_data.motions.get("blue")
            red_motion = beat_data.pictograph_data.motions.get("red")

        if not blue_motion or not red_motion:
            return ""

        blue_type = blue_motion.motion_type.value
        red_type = red_motion.motion_type.value
        letter = beat_data.letter or ""

        # Generate key in standard format
        return f"{letter}_{blue_type}_{red_type}"

    def _apply_swap_override(self, beat_data: BeatData) -> BeatData:
        """
        Apply manual swap override from special placements.

        Loads specific positioning data for this configuration.
        """
        override_key = self._generate_override_key(beat_data)
        special_placements = self._get_special_placements()

        # Apply override adjustments
        # TODO: Implement specific override application logic
        # This would modify the beat_data with specific positioning overrides
        return beat_data

    def _apply_algorithmic_beta_positioning(self, beat_data: BeatData) -> BeatData:
        """
        Apply algorithmic beta prop positioning.

        Uses classification and repositioning logic.
        """
        # Get motion data from pictograph_data instead of beat_data
        blue_motion = None
        red_motion = None

        if beat_data.pictograph_data and beat_data.pictograph_data.motions:
            blue_motion = beat_data.pictograph_data.motions.get("blue")
            red_motion = beat_data.pictograph_data.motions.get("red")

        if not blue_motion or not red_motion:
            return beat_data

        # Calculate separation offsets
        blue_offset, red_offset = self.calculate_separation_offsets(beat_data)

        # TODO: Apply offsets to beat_data
        # This would modify the actual positioning data in beat_data
        # For now, return unmodified data as we need renderer integration

        return beat_data

    def _get_json_configurator(self):
        """Get JSONConfigurator singleton from DI container."""
        try:
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )
            from shared.application.services.positioning.props.configuration.json_configuration_service import (
                IJSONConfigurator,
            )

            container = get_container()
            return container.resolve(IJSONConfigurator)
        except Exception as e:
            # Log the DI failure for debugging
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"Failed to resolve IJSONConfigurator from DI container: {e}"
            )

            # Fallback to creating new instance if DI fails
            from shared.application.services.positioning.props.configuration.json_configuration_service import (
                JSONConfigurator,
            )

            return JSONConfigurator()

    def _get_special_placements(self) -> dict[str, Any]:
        """Get special placements using JSONConfigurator singleton."""
        return self._json_configurator.load_special_placements()

    def classify_props_by_size(self, beat_data: BeatData) -> dict[str, list]:
        """
        Classify props by size categories (big, small, hands).

        Based on PropClassifier logic.
        """
        classification = {
            "big_props": [],
            "small_props": [],
            "hands": [],
        }

        # TODO: Implement prop classification logic
        # This would analyze the prop types in beat_data and categorize them

        return classification

    def get_repositioning_strategy(
        self, beat_data: BeatData, prop_classification: dict[str, list]
    ) -> str:
        """
        Determine repositioning strategy based on prop classification and letter.

        Returns strategy name that determines how props should be separated.
        """
        letter = beat_data.letter or ""

        # Check prop categories
        has_big_props = bool(prop_classification["big_props"])
        has_small_props = bool(prop_classification["small_props"])
        has_hands = bool(prop_classification["hands"])

        if has_big_props and len(prop_classification["big_props"]) == 2:
            return "big_prop_repositioning"
        elif has_small_props and len(prop_classification["small_props"]) == 2:
            return "small_prop_repositioning"
        elif has_hands:
            return "hand_repositioning"
        else:
            return "default_repositioning"

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

    def cleanup(self):
        """Clean up event subscriptions when service is destroyed."""
        if self.event_bus:
            for sub_id in self._subscription_ids:
                self.event_bus.unsubscribe(sub_id)
            self._subscription_ids.clear()
