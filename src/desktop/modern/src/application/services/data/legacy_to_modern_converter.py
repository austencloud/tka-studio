"""
Legacy to Modern Converter

Handles conversion from legacy JSON format to modern domain models.
Focused solely on legacy-to-modern data transformation.
"""

import logging
from typing import Any, Dict

from domain.models.beat_data import BeatData
from domain.models.glyph_models import GlyphData
from domain.models.motion_models import MotionData

from .position_attribute_mapper import PositionAttributeMapper

logger = logging.getLogger(__name__)


class LegacyToModernConverter:
    """
    Converts legacy JSON format to modern domain models.

    Responsible for:
    - Converting legacy beat JSON to BeatData
    - Converting legacy start position JSON to BeatData
    - Handling legacy attribute format transformations
    - Maintaining data fidelity during conversion
    """

    def __init__(self):
        """Initialize the legacy to modern converter."""
        self.position_mapper = PositionAttributeMapper()

    def convert_legacy_to_beat_data(
        self, beat_dict: dict, beat_number: int
    ) -> BeatData:
        """
        Convert legacy JSON format to modern BeatData with full pictograph data.

        Args:
            beat_dict: Legacy beat dictionary
            beat_number: Beat number to assign

        Returns:
            BeatData object with converted motion information
        """
        try:
            # Extract basic beat info
            letter = beat_dict.get("letter", "?")
            duration = beat_dict.get("duration", 1.0)

            # Extract position data
            start_pos = beat_dict.get("start_pos", "")
            end_pos = beat_dict.get("end_pos", "")

            # Extract motion attributes
            blue_attrs = beat_dict.get("blue_attributes", {})
            red_attrs = beat_dict.get("red_attributes", {})

            # Create motion data for blue and red
            blue_motion = self._create_motion_data_from_attributes(blue_attrs)
            red_motion = self._create_motion_data_from_attributes(red_attrs)

            # Create glyph data as proper GlyphData object
            glyph_data = GlyphData(
                start_position=start_pos,
                end_position=end_pos,
            )

            # Create complete beat data
            beat_data = BeatData(
                letter=letter,
                beat_number=beat_number,
                duration=duration,
                glyph_data=glyph_data,
                blue_motion=blue_motion,
                red_motion=red_motion,
            )

            return beat_data

        except Exception as e:
            logger.error(f"Error converting legacy beat data: {e}")
            # Return minimal valid beat data as fallback
            return self._create_fallback_beat_data(beat_number)

    def convert_legacy_start_position_to_beat_data(
        self, start_pos_dict: dict
    ) -> BeatData:
        """
        Convert legacy start position JSON to modern BeatData with full data.

        Args:
            start_pos_dict: Legacy start position dictionary

        Returns:
            BeatData object representing the start position
        """
        try:
            # Extract basic start position info
            letter = start_pos_dict.get("letter", "A")
            end_pos = start_pos_dict.get("end_pos", "alpha1")
            sequence_start_position = start_pos_dict.get(
                "sequence_start_position", "alpha"
            )

            # Extract motion attributes
            blue_attrs = start_pos_dict.get("blue_attributes", {})
            red_attrs = start_pos_dict.get("red_attributes", {})

            # Create motion data for blue and red (start positions are typically static)
            blue_motion = self._create_start_position_motion_data(
                blue_attrs, sequence_start_position
            )
            red_motion = self._create_start_position_motion_data(
                red_attrs, sequence_start_position
            )

            # Create glyph data with position information as proper GlyphData object
            from domain.models.glyph_models import GlyphData

            glyph_data = GlyphData(
                start_position=sequence_start_position,
                end_position=end_pos,
            )

            # Create start position beat data
            start_position_beat = BeatData(
                letter=letter,
                beat_number=0,  # Start position is beat 0
                duration=1.0,
                glyph_data=glyph_data,
                blue_motion=blue_motion,
                red_motion=red_motion,
                metadata={
                    "timing": start_pos_dict.get("timing", "same"),
                    "direction": start_pos_dict.get("direction", "none"),
                    "is_start_position": True,
                },
            )

            return start_position_beat

        except Exception as e:
            logger.error(f"Error converting legacy start position data: {e}")
            # Return minimal valid start position as fallback
            return self._create_fallback_start_position()

    def _create_motion_data_from_attributes(self, attrs: Dict[str, Any]) -> MotionData:
        """
        Create MotionData from legacy motion attributes.

        Args:
            attrs: Legacy motion attributes dictionary

        Returns:
            MotionData object
        """
        # Validate and convert attributes
        validated_attrs = self.position_mapper.validate_position_attributes(attrs)

        return MotionData(
            motion_type=validated_attrs["motion_type"],
            start_loc=validated_attrs["start_loc"],
            end_loc=validated_attrs["end_loc"],
            start_ori=validated_attrs["start_ori"],
            end_ori=validated_attrs["end_ori"],
            prop_rot_dir=validated_attrs["prop_rot_dir"],
            turns=validated_attrs["turns"],
        )

    def _create_start_position_motion_data(
        self, attrs: Dict[str, Any], sequence_start_position: str
    ) -> MotionData:
        """
        Create MotionData for start position with special handling.

        Args:
            attrs: Legacy motion attributes dictionary
            sequence_start_position: Sequence start position type

        Returns:
            MotionData object for start position
        """
        # Use sequence start position as default for missing locations
        start_loc = attrs.get("start_loc", sequence_start_position)
        end_loc = attrs.get("end_loc", sequence_start_position)

        # Create attributes with start position defaults
        start_attrs = {
            "motion_type": attrs.get("motion_type", "static"),
            "start_loc": start_loc,
            "end_loc": end_loc,
            "start_ori": attrs.get("start_ori", "in"),
            "end_ori": attrs.get("end_ori", "in"),
            "prop_rot_dir": attrs.get("prop_rot_dir", "no_rot"),
            "turns": attrs.get("turns", 0),
        }

        return self._create_motion_data_from_attributes(start_attrs)

    def _create_fallback_beat_data(self, beat_number: int) -> BeatData:
        """Create minimal fallback beat data when conversion fails."""
        return BeatData(
            letter="?",
            beat_number=beat_number,
            duration=1.0,
            glyph_data={"start_position": "", "end_position": ""},
            blue_motion=MotionData(
                motion_type="static",
                start_loc="n",
                end_loc="n",
                start_ori="in",
                end_ori="in",
                prop_rot_dir="no_rot",
                turns=0,
            ),
            red_motion=MotionData(
                motion_type="static",
                start_loc="n",
                end_loc="n",
                start_ori="in",
                end_ori="in",
                prop_rot_dir="no_rot",
                turns=0,
            ),
            metadata={"source": "fallback_conversion"},
        )

    def _create_fallback_start_position(self) -> BeatData:
        """Create minimal fallback start position when conversion fails."""
        return BeatData(
            letter="A",
            beat_number=0,
            duration=1.0,
            glyph_data={"start_position": "alpha", "end_position": "alpha1"},
            blue_motion=MotionData(
                motion_type="static",
                start_loc="n",
                end_loc="n",
                start_ori="in",
                end_ori="in",
                prop_rot_dir="no_rot",
                turns=0,
            ),
            red_motion=MotionData(
                motion_type="static",
                start_loc="n",
                end_loc="n",
                start_ori="in",
                end_ori="in",
                prop_rot_dir="no_rot",
                turns=0,
            ),
            metadata={
                "timing": "same",
                "direction": "none",
                "is_start_position": True,
                "source": "fallback_conversion",
            },
        )

    def validate_legacy_beat_format(self, beat_dict: dict) -> bool:
        """
        Validate that a dictionary has the expected legacy beat format.

        Args:
            beat_dict: Dictionary to validate

        Returns:
            True if format is valid, False otherwise
        """
        if not isinstance(beat_dict, dict):
            return False

        # Check for required fields
        required_fields = ["letter"]
        for field in required_fields:
            if field not in beat_dict:
                return False

        # Check for motion attributes structure
        for color in ["blue_attributes", "red_attributes"]:
            if color in beat_dict:
                attrs = beat_dict[color]
                if not isinstance(attrs, dict):
                    return False

        return True

    def get_supported_legacy_fields(self) -> list:
        """Get list of supported legacy beat fields."""
        return [
            "letter",
            "beat",
            "duration",
            "start_pos",
            "end_pos",
            "timing",
            "direction",
            "blue_attributes",
            "red_attributes",
        ]
