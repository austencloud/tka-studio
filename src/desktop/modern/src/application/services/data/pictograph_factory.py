"""
Pictograph Factory

Handles creation and conversion of PictographData and BeatData objects.
Focused solely on object creation and data transformation logic.
"""

import logging
from typing import Optional

import pandas as pd
from application.services.glyphs.glyph_data_service import GlyphDataService
from domain.models.arrow_data import ArrowData
from domain.models.beat_data import BeatData
from domain.models.enums import (
    GridMode,
    Location,
    MotionType,
    Orientation,
    RotationDirection,
)
from domain.models.grid_data import GridData
from domain.models.motion_models import MotionData
from domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class PictographFactory:
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

            # Create initial pictograph data
            pictograph_data = PictographData(
                grid_data=grid_data,
                arrows=arrows,
                props={},  # Props will be generated during rendering
                motions=motions,  # NEW: Motion dictionary
                letter=entry.get("letter", "?"),
                start_position=entry.get("start_pos"),
                end_position=entry.get("end_pos"),
                metadata={
                    "is_start_position": True,
                    "source": "dataset",
                },
            )

            # Generate and attach glyph data
            glyph_data = self.glyph_service.determine_glyph_data(pictograph_data)
            return pictograph_data.update(glyph_data=glyph_data)

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
        Convert PictographData to BeatData for backward compatibility.

        Args:
            pictograph_data: The pictograph data to convert
            beat_number: Beat number to assign (default: 1)

        Returns:
            BeatData object with motion data extracted from pictograph
        """
        # Extract motion data from motions dictionary
        blue_motion = None
        red_motion = None

        if "blue" in pictograph_data.motions:
            blue_motion = pictograph_data.motions["blue"]
        if "red" in pictograph_data.motions:
            red_motion = pictograph_data.motions["red"]

        # Create BeatData with extracted information
        # Note: start_position and end_position should be in glyph_data, not as direct BeatData parameters
        return BeatData(
            beat_number=beat_number,
            blue_motion=blue_motion,
            red_motion=red_motion,
            letter=pictograph_data.letter,
            is_blank=pictograph_data.is_blank,
            glyph_data=pictograph_data.glyph_data,
        )

    def convert_beat_to_pictograph_data(
        self, beat_data: BeatData, grid_mode: str
    ) -> PictographData:
        """
        Convert BeatData to PictographData.

        Args:
            beat_data: BeatData to convert
            grid_mode: Grid mode ("diamond" or "box")

        Returns:
            PictographData object
        """
        # Create arrow data (without motion_data - motion data now in motions dictionary)
        arrows = {}
        motions = {}

        if beat_data.blue_motion:
            arrows["blue"] = ArrowData(color="blue", is_visible=True)
            motions["blue"] = beat_data.blue_motion

        if beat_data.red_motion:
            arrows["red"] = ArrowData(color="red", is_visible=True)
            motions["red"] = beat_data.red_motion

        # Create grid data
        grid_data = GridData(
            grid_mode=GridMode.DIAMOND if grid_mode == "diamond" else GridMode.BOX
        )

        # Create pictograph data
        return PictographData(
            grid_data=grid_data,
            arrows=arrows,
            props={},  # Props will be generated during rendering
            motions=motions,  # NEW: Motion dictionary
            letter=beat_data.letter,
            start_position=beat_data.start_position,
            end_position=beat_data.end_position,
            glyph_data=beat_data.glyph_data,
            metadata={
                "source": "beat_conversion",
                "beat_number": beat_data.beat_number,
            },
        )

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

        return PictographData(
            grid_data=grid_data,
            arrows={},
            props={},
            letter=entry.get("letter", "?"),
            metadata={
                "source": "fallback",
                "error": "Failed to parse dataset entry",
            },
        )
