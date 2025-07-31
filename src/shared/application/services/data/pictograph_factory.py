"""
Pictograph Factory

Handles creation and conversion of PictographData and BeatData objects.
Focused solely on object creation and data transformation logic.
"""

import logging
from typing import Any, Optional

import pandas as pd

from desktop.modern.core.interfaces.data_builder_services import IPictographFactory
from desktop.modern.domain.models.arrow_data import ArrowData
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import (
    GridMode,
    Location,
    MotionType,
    Orientation,
    RotationDirection,
)
from desktop.modern.domain.models.grid_data import GridData
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData
from shared.application.services.glyphs.glyph_data_service import GlyphDataService

logger = logging.getLogger(__name__)


class PictographFactory(IPictographFactory):
    """
    Creates PictographData and BeatData objects from dataset entries.

    Responsible for:
    - Converting dataset entries to PictographData
    - Converting PictographData to BeatData (backward compatibility)
    - Parsing enum values from string representations
    - Creating proper domain model objects with glyph data
    """

    # Enum mapping constants
    MOTION_TYPE_MAP = {
        "pro": MotionType.PRO,
        "anti": MotionType.ANTI,
        "static": MotionType.STATIC,
        "dash": MotionType.DASH,
    }

    ROTATION_DIRECTION_MAP = {
        "cw": RotationDirection.CLOCKWISE,
        "ccw": RotationDirection.COUNTER_CLOCKWISE,
        "no_rot": RotationDirection.NO_ROTATION,
    }

    LOCATION_MAP = {
        "n": Location.NORTH,
        "ne": Location.NORTHEAST,
        "e": Location.EAST,
        "se": Location.SOUTHEAST,
        "s": Location.SOUTH,
        "sw": Location.SOUTHWEST,
        "w": Location.WEST,
        "nw": Location.NORTHWEST,
    }

    def __init__(self):
        """Initialize the pictograph factory."""
        self.glyph_service = GlyphDataService()

    def create_pictograph_data_from_entry(
        self, entry: pd.Series, grid_mode: str
    ) -> PictographData:
        """
        Create PictographData from a dataset entry.

        Args:
            entry: Pandas Series representing a dataset row
            grid_mode: Grid mode ("diamond" or "box")

        Returns:
            PictographData object with proper motion data and glyph data
        """
        try:
            # Parse motion data for both colors
            blue_motion = self._create_motion_data_from_entry(entry, "blue")
            red_motion = self._create_motion_data_from_entry(entry, "red")

            # Create arrow data (without motion_data - motion data now in motions dictionary)
            arrows = {}
            if blue_motion:
                arrows["blue"] = ArrowData(color="blue", is_visible=True)
            if red_motion:
                arrows["red"] = ArrowData(color="red", is_visible=True)

            # Create motions dictionary
            motions = {}
            if blue_motion:
                motions["blue"] = blue_motion
            if red_motion:
                motions["red"] = red_motion

            # Create grid data
            grid_data = GridData(
                grid_mode=GridMode.DIAMOND if grid_mode == "diamond" else GridMode.BOX
            )

            # Determine letter type from letter
            letter = entry.get("letter", "?")
            letter_type = None
            if letter and letter != "?":
                try:
                    from desktop.modern.domain.models.enums import LetterType
                    from desktop.modern.domain.models.letter_type_classifier import (
                        LetterTypeClassifier,
                    )

                    letter_type_str = LetterTypeClassifier.get_letter_type(letter)
                    logger.debug(
                        f"Letter '{letter}' classified as: '{letter_type_str}'"
                    )

                    # Convert string to enum - the classifier returns the enum value directly
                    # So we need to find the enum member that has this value
                    letter_type = None
                    for enum_member in LetterType:
                        logger.debug(
                            f"Checking enum member {enum_member} with value '{enum_member.value}' against '{letter_type_str}'"
                        )
                        if enum_member.value == letter_type_str:
                            letter_type = enum_member
                            logger.debug(f"✅ Found matching enum: {letter_type}")
                            break

                    if letter_type is None:
                        logger.debug(
                            f"❌ No matching enum found for letter_type_str: '{letter_type_str}'"
                        )
                        # List all available enum values for debugging
                        available_values = [
                            f"{member.name}='{member.value}'" for member in LetterType
                        ]
                        logger.debug(f"Available enum values: {available_values}")

                    if letter_type is None:
                        logger.warning(
                            f"Failed to convert letter_type_str '{letter_type_str}' to enum for letter '{letter}'"
                        )
                    else:
                        logger.debug(
                            f"✅ Set letter_type for '{letter}': {letter_type}"
                        )

                except Exception as e:
                    logger.error(
                        f"Failed to determine letter_type for letter '{letter}': {e}"
                    )
                    letter_type = None

            # Create initial pictograph data
            pictograph_data = PictographData(
                grid_data=grid_data,
                arrows=arrows,
                props={},  # Props will be generated during rendering
                motions=motions,  # NEW: Motion dictionary
                letter=letter,
                letter_type=letter_type,  # NEW: Set letter type for glyph rendering
                start_position=entry.get("start_pos"),
                end_position=entry.get("end_pos"),
                metadata={
                    "is_start_position": True,
                    "source": "dataset",
                },
            )

            # Glyph data is no longer needed - all glyph information is computed from PictographData
            self.glyph_service.determine_glyph_data(pictograph_data)
            return pictograph_data

        except Exception as e:
            logger.error(f"Error creating pictograph data from entry: {e}")
            # Return minimal valid pictograph data as fallback
            return self._create_fallback_pictograph_data(entry, grid_mode)

    def _create_motion_data_from_entry(
        self, entry: pd.Series, color: str
    ) -> Optional[MotionData]:
        """
        Create MotionData from dataset entry for a specific color.

        Args:
            entry: Dataset entry
            color: "blue" or "red"

        Returns:
            MotionData object or None if motion data is invalid
        """
        try:
            # Get column names for this color
            motion_type_col = f"{color}_motion_type"
            prop_rot_dir_col = f"{color}_prop_rot_dir"
            start_loc_col = f"{color}_start_loc"
            end_loc_col = f"{color}_end_loc"

            # Parse enum values
            motion_type = self._parse_motion_type(entry.get(motion_type_col, "static"))
            prop_rot_dir = self._parse_rotation_direction(
                entry.get(prop_rot_dir_col, "no_rot")
            )
            start_loc = self._parse_location(entry.get(start_loc_col, "n"))
            end_loc = self._parse_location(entry.get(end_loc_col, "n"))

            # Determine orientation based on motion type
            start_ori = Orientation.IN
            end_ori = (
                Orientation.OUT
                if motion_type in [MotionType.PRO, MotionType.ANTI]
                else Orientation.IN
            )

            # Determine turns based on motion type
            turns = 1.0 if motion_type in [MotionType.PRO, MotionType.ANTI] else 0.0

            return MotionData(
                motion_type=motion_type,
                prop_rot_dir=prop_rot_dir,
                start_loc=start_loc,
                end_loc=end_loc,
                turns=turns,
                start_ori=start_ori,
                end_ori=end_ori,
            )

        except Exception as e:
            logger.warning(f"Error creating {color} motion data: {e}")
            return None

    def convert_pictograph_to_beat_data(
        self, pictograph_data: PictographData, beat_number: int = 1
    ) -> BeatData:
        """
        Convert PictographData to BeatData using BeatFactory.

        Args:
            pictograph_data: The pictograph data to convert
            beat_number: Beat number to assign (default: 1)

        Returns:
            BeatData object with embedded pictograph data
        """
        # Use BeatFactory for consistent beat creation with embedded pictograph
        from shared.application.services.sequence.beat_factory import BeatFactory

        return BeatFactory.create_from_pictograph(pictograph_data, beat_number)

    def _parse_motion_type(self, motion_type_str: str) -> MotionType:
        """Parse motion type string to MotionType enum."""
        if not isinstance(motion_type_str, str):
            return MotionType.STATIC
        return self.MOTION_TYPE_MAP.get(motion_type_str.lower(), MotionType.STATIC)

    def _parse_rotation_direction(self, rot_dir_str: str) -> RotationDirection:
        """Parse rotation direction string to RotationDirection enum."""
        if not isinstance(rot_dir_str, str):
            return RotationDirection.NO_ROTATION
        return self.ROTATION_DIRECTION_MAP.get(
            rot_dir_str.lower(), RotationDirection.NO_ROTATION
        )

    def _parse_location(self, location_str: str) -> Location:
        """Parse location string to Location enum."""
        if not isinstance(location_str, str):
            return Location.NORTH
        return self.LOCATION_MAP.get(location_str.lower(), Location.NORTH)

    def _create_fallback_pictograph_data(
        self, entry: pd.Series, grid_mode: str
    ) -> PictographData:
        """Create minimal fallback pictograph data when parsing fails."""
        grid_data = GridData(
            grid_mode=GridMode.DIAMOND if grid_mode == "diamond" else GridMode.BOX
        )

        # Determine letter type for fallback too
        letter = entry.get("letter", "?")
        letter_type = None
        if letter and letter != "?":
            from desktop.modern.domain.models.enums import LetterType
            from desktop.modern.domain.models.letter_type_classifier import (
                LetterTypeClassifier,
            )

            letter_type_str = LetterTypeClassifier.get_letter_type(letter)
            # Convert string to enum - find the enum member with matching value
            letter_type = None
            for enum_member in LetterType:
                if enum_member.value == letter_type_str:
                    letter_type = enum_member
                    break

        return PictographData(
            grid_data=grid_data,
            arrows={},
            props={},
            letter=letter,
            letter_type=letter_type,
            metadata={
                "source": "fallback",
                "error": "Failed to parse dataset entry",
            },
        )

    # Interface implementation methods
    def create_pictograph(self, pictograph_type: str, config: dict[str, Any]) -> Any:
        """Create pictograph instance (interface implementation)."""
        if pictograph_type == "from_entry":
            entry = config.get("entry", {})
            grid_mode = config.get("grid_mode", "diamond")
            return self.create_pictograph_data_from_entry(entry, grid_mode)

        elif pictograph_type == "start_position":
            entry = config.get("entry", {})
            grid_mode = config.get("grid_mode", "diamond")
            return self.create_start_position_pictograph_data(entry, grid_mode)

        else:
            raise ValueError(f"Unknown pictograph type: {pictograph_type}")

    def get_available_types(self) -> list[str]:
        """Get available pictograph types (interface implementation)."""
        return ["from_entry", "start_position"]

    def validate_pictograph_config(
        self, pictograph_type: str, config: dict[str, Any]
    ) -> bool:
        """Validate pictograph configuration (interface implementation)."""
        if pictograph_type not in self.get_available_types():
            return False

        if pictograph_type in ["from_entry", "start_position"]:
            return "entry" in config and isinstance(config["entry"], dict)

        return False

    def create_from_beat_data(self, beat_data: Any) -> Any:
        """Create pictograph from beat data (interface implementation)."""
        # Extract pictograph data from beat data if it exists
        if hasattr(beat_data, "pictograph_data") and beat_data.pictograph_data:
            return beat_data.pictograph_data

        # Create minimal pictograph from beat metadata
        entry = {
            "letter": getattr(beat_data, "letter", "?"),
            "start_pos": getattr(beat_data, "start_position", None),
            "end_pos": getattr(beat_data, "end_position", None),
        }

        return self.create_pictograph_data_from_entry(entry, "diamond")
