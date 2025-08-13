"""
Modern to Legacy Converter

Handles conversion from modern domain models to legacy JSON format.
Focused solely on modern-to-legacy data transformation.
"""

from __future__ import annotations

import logging
from typing import Any

from desktop.modern.core.interfaces.data_services import IModernToLegacyConverter
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import Orientation
from desktop.modern.domain.models.motion_data import MotionData


# from .position_attribute_mapper import PositionAttributeMapper  # Circular import issue

logger = logging.getLogger(__name__)


class ModernToLegacyConverter(IModernToLegacyConverter):
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
        # Lazy import to avoid circular dependency
        from .position_attribute_mapper import PositionAttributeMapper
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
            # Extract position data directly from pictograph_data
            start_pos = ""
            end_pos = ""
            # Use start/end positions directly from pictograph_data
            start_pos = beat.pictograph_data.start_position or ""
            end_pos = beat.pictograph_data.end_position or ""

            # Extract timing and direction from metadata
            timing = beat.metadata.get("timing", "same") if beat.metadata else "same"
            direction = beat.metadata.get("direction", "cw") if beat.metadata else "cw"

            # Get motion data from pictograph_data instead of beat
            blue_motion = None
            red_motion = None

            if beat.pictograph_data and beat.pictograph_data.motions:
                blue_motion = beat.pictograph_data.motions.get("blue")
                red_motion = beat.pictograph_data.motions.get("red")

            # Convert blue motion data
            blue_attrs = self.position_mapper.convert_motion_attributes_to_legacy(
                blue_motion, "alpha"
            )

            # Convert red motion data
            red_attrs = self.position_mapper.convert_motion_attributes_to_legacy(
                red_motion, "alpha"
            )

            return {
                "beat": beat_number,
                "letter": beat.letter or "?",
                "letter_type": (
                    beat.pictograph_data.letter_type.value
                    if beat.pictograph_data.letter_type
                    else "Type1"
                ),
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
            raise e

    def convert_start_position_to_legacy_format(
        self, start_position_beat_data: BeatData
    ) -> dict:
        """
        Convert start position BeatData to legacy format exactly like JsonStartPositionHandler.

        Args:
            start_position_data: BeatData representing start position

        Returns:
            Dictionary in legacy start position format
        """
        try:
            # Extract start position type (alpha, beta, gamma) directly from pictograph_data
            end_pos = "alpha1"  # Default
            sequence_start_position = "alpha"  # Default

            if start_position_beat_data.pictograph_data.end_position:
                end_pos = start_position_beat_data.pictograph_data.end_position
                sequence_start_position = self.position_mapper.extract_position_type(
                    end_pos
                )

            # Get motion data from pictograph_data instead of start_position_data
            blue_motion = None
            red_motion = None

            if (
                start_position_beat_data.pictograph_data
                and start_position_beat_data.pictograph_data.motions
            ):
                blue_motion = start_position_beat_data.pictograph_data.motions.get(
                    "blue"
                )
                red_motion = start_position_beat_data.pictograph_data.motions.get("red")

            # Convert motion data with start position handling
            blue_attrs = self._convert_start_position_motion_to_legacy(
                blue_motion, sequence_start_position
            )
            red_attrs = self._convert_start_position_motion_to_legacy(
                red_motion, sequence_start_position
            )

            return {
                "beat": 0,  # Start position is always beat 0
                "sequence_start_position": sequence_start_position,
                "letter": start_position_beat_data.letter or "A",
                "end_pos": end_pos,
                "timing": "same",  # Start positions use same timing
                "direction": "none",
                "blue_attributes": blue_attrs,
                "red_attributes": red_attrs,
            }

        except Exception as e:
            logger.error(f"Error converting start position to legacy format: {e}")
            raise e

    def _convert_start_position_motion_to_legacy(
        self, motion_data: MotionData, sequence_start_position: str
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
        start_ori = self._convert_orientation(motion_data.start_ori)
        end_ori = self._convert_orientation(motion_data.end_ori)

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

    def _convert_orientation(self, orientation: Orientation) -> str:
        """
        Convert orientation with fallback handling for complex cases.

        Args:
            orientation: Orientation value
            fallback: Fallback value if conversion fails

        Returns:
            Converted orientation string
        """
        if hasattr(orientation, "value"):
            return str(orientation.value)
        elif orientation is not None:
            return str(orientation)
        else:
            return "in"

    # Interface implementation methods
    def convert_modern_data(self, modern_data: Any) -> dict[str, Any]:
        """Convert modern data to legacy format (interface implementation)."""
        if hasattr(modern_data, "beats"):
            return self.convert_sequence_to_legacy(modern_data)
        elif hasattr(modern_data, "letter"):
            return self.convert_beat_to_legacy(modern_data)
        else:
            return {"error": "Unknown modern data type"}

    def validate_modern_format(self, data: Any) -> bool:
        """Validate modern data format (interface implementation)."""
        try:
            # Check if it's a modern sequence or beat
            if hasattr(data, "beats") or hasattr(data, "letter"):
                return True
            return False
        except Exception:
            return False

    def get_conversion_metadata(self, modern_data: Any) -> dict[str, Any]:
        """Get metadata about conversion (interface implementation)."""
        return {
            "source_format": "modern",
            "target_format": "legacy",
            "data_type": "sequence" if hasattr(modern_data, "beats") else "beat",
            "conversion_timestamp": "runtime",
            "converter_version": "1.0",
        }

    # Interface implementation methods
    def convert_sequence(self, modern_sequence: Any) -> list[dict[str, Any]] | None:
        """Convert modern sequence to legacy format."""
        try:
            if hasattr(modern_sequence, "beats"):
                result = []
                for i, beat in enumerate(modern_sequence.beats):
                    legacy_beat = self.convert_beat_data_to_legacy_format(beat, i + 1)
                    if legacy_beat:
                        result.append(legacy_beat)
                return result
            return None
        except Exception as e:
            logger.error(f"Error converting sequence: {e}")
            return None

    def convert_beat(self, modern_beat: Any) -> dict[str, Any] | None:
        """Convert modern beat to legacy format."""
        try:
            if hasattr(modern_beat, "beat_number"):
                return self.convert_beat_data_to_legacy_format(
                    modern_beat, modern_beat.beat_number
                )
            return None
        except Exception as e:
            logger.error(f"Error converting beat: {e}")
            return None

    def convert_pictograph(self, modern_pictograph: Any) -> dict[str, Any] | None:
        """Convert modern pictograph to legacy format."""
        try:
            # TODO: Implement pictograph conversion
            return None
        except Exception as e:
            logger.error(f"Error converting pictograph: {e}")
            return None
