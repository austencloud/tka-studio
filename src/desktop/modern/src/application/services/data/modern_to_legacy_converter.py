"""
Modern to Legacy Converter

Handles conversion from modern domain models to legacy JSON format.
Focused solely on modern-to-legacy data transformation.
"""

import logging
from typing import Any, Dict

from domain.models.beat_data import BeatData

from .position_attribute_mapper import PositionAttributeMapper

logger = logging.getLogger(__name__)


class ModernToLegacyConverter:
    """
    Converts modern domain models to legacy JSON format.

    Responsible for:
    - Converting BeatData to legacy beat JSON
    - Converting start position BeatData to legacy start position JSON
    - Handling modern attribute format transformations
    - Maintaining compatibility with legacy systems
    """

    def __init__(self):
        """Initialize the modern to legacy converter."""
        self.position_mapper = PositionAttributeMapper()

    def convert_beat_data_to_legacy_format(
        self, beat: BeatData, beat_number: int
    ) -> dict:
        """
        Convert modern BeatData to legacy JSON format exactly like legacy pictograph_data.

        Args:
            beat: BeatData object to convert
            beat_number: Beat number for the legacy format

        Returns:
            Dictionary in legacy JSON format
        """
        try:
            # Extract position data from glyph_data if available
            start_pos = ""
            end_pos = ""
            if beat.glyph_data:
                start_pos = beat.glyph_data.start_position or ""
                end_pos = beat.glyph_data.end_position or ""

            # Extract timing and direction from metadata
            timing = beat.metadata.get("timing", "same") if beat.metadata else "same"
            direction = beat.metadata.get("direction", "cw") if beat.metadata else "cw"

            # Convert blue motion data
            blue_attrs = self.position_mapper.convert_motion_attributes_to_legacy(
                beat.blue_motion, "alpha"
            )

            # Convert red motion data
            red_attrs = self.position_mapper.convert_motion_attributes_to_legacy(
                beat.red_motion, "alpha"
            )

            return {
                "beat": beat_number,
                "letter": beat.letter or "?",
                "letter_type": "Type1",  # Default for now - could extract from glyph_data.letter_type
                "duration": int(beat.duration),
                "start_pos": start_pos,
                "end_pos": end_pos,
                "timing": timing,
                "direction": direction,
                "blue_attributes": blue_attrs,
                "red_attributes": red_attrs,
            }

        except Exception as e:
            logger.error(f"Error converting beat data to legacy format: {e}")
            return self._create_fallback_legacy_beat(beat_number)

    def convert_start_position_to_legacy_format(
        self, start_position_data: BeatData
    ) -> dict:
        """
        Convert start position BeatData to legacy format exactly like JsonStartPositionHandler.

        Args:
            start_position_data: BeatData representing start position

        Returns:
            Dictionary in legacy start position format
        """
        try:
            # Extract start position type (alpha, beta, gamma) from glyph_data if available
            end_pos = "alpha1"  # Default
            sequence_start_position = "alpha"  # Default

            if (
                start_position_data.glyph_data
                and start_position_data.glyph_data.end_position
            ):
                end_pos = start_position_data.glyph_data.end_position
                sequence_start_position = self.position_mapper.extract_position_type(
                    end_pos
                )

            # Convert motion data with start position handling
            blue_attrs = self._convert_start_position_motion_to_legacy(
                start_position_data.blue_motion, sequence_start_position
            )
            red_attrs = self._convert_start_position_motion_to_legacy(
                start_position_data.red_motion, sequence_start_position
            )

            return {
                "beat": 0,  # Start position is always beat 0
                "sequence_start_position": sequence_start_position,
                "letter": start_position_data.letter or "A",
                "end_pos": end_pos,
                "timing": "same",  # Start positions use same timing
                "direction": "none",
                "blue_attributes": blue_attrs,
                "red_attributes": red_attrs,
            }

        except Exception as e:
            logger.error(f"Error converting start position to legacy format: {e}")
            return self._create_fallback_legacy_start_position()

    def convert_beat_to_legacy_dict(self, beat: BeatData) -> dict:
        """
        Convert a single BeatData to legacy dictionary format (simplified version).

        Args:
            beat: BeatData object to convert

        Returns:
            Dictionary in legacy format
        """
        try:
            # Convert motion attributes
            blue_attrs = self.position_mapper.convert_motion_attributes_to_legacy(
                beat.blue_motion, "s"
            )
            red_attrs = self.position_mapper.convert_motion_attributes_to_legacy(
                beat.red_motion, "s"
            )

            return {
                "beat": beat.beat_number,
                "letter": beat.letter,
                "duration": beat.duration,
                "start_pos": "alpha1",  # Default for now
                "end_pos": "alpha1",  # Default for now
                "timing": "same",
                "direction": "cw",
                "blue_attributes": blue_attrs,
                "red_attributes": red_attrs,
            }

        except Exception as e:
            logger.error(f"Error converting beat to legacy dict: {e}")
            return self._create_fallback_legacy_beat(beat.beat_number)

    def _convert_start_position_motion_to_legacy(
        self, motion_data, sequence_start_position: str
    ) -> dict:
        """
        Convert motion data to legacy format with start position special handling.

        Args:
            motion_data: MotionData object or None
            sequence_start_position: Sequence start position type

        Returns:
            Dictionary with legacy motion attributes
        """
        if not motion_data:
            return {
                "start_loc": sequence_start_position,
                "end_loc": sequence_start_position,
                "start_ori": "in",
                "end_ori": "in",
                "prop_rot_dir": "no_rot",  # Start positions don't rotate
                "turns": 0,  # Start positions don't have turns
                "motion_type": "static",
            }

        # Handle orientation conversion with special logic for start positions
        start_ori = self._convert_orientation_with_fallback(motion_data.start_ori, "in")
        end_ori = self._convert_orientation_with_fallback(motion_data.end_ori, "in")

        return {
            "start_loc": self.position_mapper.convert_enum_value_to_string(
                motion_data.start_loc
            )
            or sequence_start_position,
            "end_loc": self.position_mapper.convert_enum_value_to_string(
                motion_data.end_loc
            )
            or sequence_start_position,
            "start_ori": start_ori,
            "end_ori": end_ori,
            "prop_rot_dir": "no_rot",  # Start positions don't rotate
            "turns": 0,  # Start positions don't have turns
            "motion_type": self.position_mapper.convert_enum_value_to_string(
                motion_data.motion_type
            ),
        }

    def _convert_orientation_with_fallback(self, orientation, fallback: str) -> str:
        """
        Convert orientation with fallback handling for complex cases.

        Args:
            orientation: Orientation value
            fallback: Fallback value if conversion fails

        Returns:
            Converted orientation string
        """
        try:
            if hasattr(orientation, "value"):
                return str(orientation.value)
            elif orientation is not None:
                return str(orientation)
            else:
                return fallback
        except Exception:
            return fallback

    def _create_fallback_legacy_beat(self, beat_number: int) -> dict:
        """Create fallback legacy beat when conversion fails."""
        return {
            "beat": beat_number,
            "letter": "?",
            "letter_type": "Type1",
            "duration": 1,
            "start_pos": "",
            "end_pos": "",
            "timing": "same",
            "direction": "cw",
            "blue_attributes": self.position_mapper.get_default_attributes_for_position_type(
                "alpha"
            ),
            "red_attributes": self.position_mapper.get_default_attributes_for_position_type(
                "alpha"
            ),
        }

    def _create_fallback_legacy_start_position(self) -> dict:
        """Create fallback legacy start position when conversion fails."""
        return {
            "beat": 0,
            "sequence_start_position": "alpha",
            "letter": "A",
            "end_pos": "alpha1",
            "timing": "same",
            "direction": "none",
            "blue_attributes": self.position_mapper.get_default_attributes_for_position_type(
                "alpha"
            ),
            "red_attributes": self.position_mapper.get_default_attributes_for_position_type(
                "alpha"
            ),
        }

    def validate_beat_data_for_conversion(self, beat: BeatData) -> bool:
        """
        Validate that BeatData can be converted to legacy format.

        Args:
            beat: BeatData to validate

        Returns:
            True if conversion is possible, False otherwise
        """
        if not isinstance(beat, BeatData):
            return False

        # Check for required fields
        if not hasattr(beat, "letter") or not hasattr(beat, "beat_number"):
            return False

        return True

    def get_legacy_format_fields(self) -> list:
        """Get list of fields in legacy format."""
        return [
            "beat",
            "letter",
            "letter_type",
            "duration",
            "start_pos",
            "end_pos",
            "timing",
            "direction",
            "blue_attributes",
            "red_attributes",
        ]
