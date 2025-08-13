"""
Legacy to Modern Converter

Handles conversion from legacy JSON format to modern domain models.
Focused solely on legacy-to-modern data transformation.
"""

from __future__ import annotations

import logging

# Forward reference for PictographData
from typing import TYPE_CHECKING, Any

from desktop.modern.core.interfaces.data_services import ILegacyToModernConverter
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.motion_data import MotionData


if TYPE_CHECKING:
    from desktop.modern.domain.models.pictograph_data import PictographData

# from .position_attribute_mapper import PositionAttributeMapper  # Circular import issue

logger = logging.getLogger(__name__)


class LegacyToModernConverter(ILegacyToModernConverter):
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
        # Lazy import to avoid circular dependency
        from .position_attribute_mapper import PositionAttributeMapper
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
            duration = beat_dict.get("duration", 1.0)

            # Extract motion attributes
            blue_attrs = beat_dict.get("blue_attributes", {})
            red_attrs = beat_dict.get("red_attributes", {})

            # Create motion data for blue and red
            blue_motion = self._create_motion_data_from_attributes(blue_attrs)
            red_motion = self._create_motion_data_from_attributes(red_attrs)

            # Glyph data is no longer needed - all glyph information is computed from PictographData

            # Create PictographData with motion data
            pictograph_data = self._create_pictograph_data_from_legacy(
                beat_dict, blue_motion, red_motion
            )

            # Create complete beat data with pictograph reference
            beat_data = BeatData(
                beat_number=beat_number,
                duration=duration,
                pictograph_data=pictograph_data,  # NEW: Reference to pictograph with motion data
            )

            return beat_data

        except Exception as e:
            logger.error(f"Error converting legacy beat data: {e}")
            raise e

    def _create_motion_data_from_attributes(self, attrs: dict[str, Any]) -> MotionData:
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

    def _create_pictograph_data_from_legacy(
        self,
        beat_dict: dict,
        blue_motion: MotionData,
        red_motion: MotionData,
    ) -> PictographData:
        """Create PictographData from legacy beat data with motion data."""
        from desktop.modern.domain.models.arrow_data import ArrowData
        from desktop.modern.domain.models.enums import GridMode
        from desktop.modern.domain.models.grid_data import GridData
        from desktop.modern.domain.models.pictograph_data import PictographData

        # Create arrows (without motion data)
        arrows = {}
        if blue_motion:
            arrows["blue"] = ArrowData(color="blue", is_visible=True)
        if red_motion:
            arrows["red"] = ArrowData(color="red", is_visible=True)

        # Create grid data
        grid_data = GridData(grid_mode=GridMode.DIAMOND)

        # Create motions dictionary
        motions = {}
        if blue_motion:
            motions["blue"] = blue_motion
        if red_motion:
            motions["red"] = red_motion

        # Create pictograph with motion dictionary
        return PictographData(
            grid_data=grid_data,
            arrows=arrows,
            props={},
            motions=motions,  # NEW: Motion dictionary (consistent with arrows/props)
            letter=beat_dict.get("letter"),
            start_position=beat_dict.get("start_pos", ""),
            end_position=beat_dict.get("end_pos", ""),
            metadata={"source": "legacy_conversion"},
        )

    def convert_legacy_start_position_to_beat_data(
        self, legacy_start_position: str
    ) -> BeatData | None:
        """Convert a legacy start position to a BeatData object."""
        # TODO: Implement this method

    # Interface implementation methods
    def convert_legacy_data(self, legacy_data: dict[str, Any]) -> Any:
        """Convert legacy data to modern format (interface implementation)."""
        if "beats" in legacy_data:
            return self.convert_legacy_sequence_to_modern(legacy_data)
        elif "letter" in legacy_data:
            return self.convert_legacy_beat_to_modern(legacy_data)
        else:
            return legacy_data

    def validate_legacy_format(self, data: dict[str, Any]) -> bool:
        """Validate legacy data format (interface implementation)."""
        try:
            # Check for basic legacy structure
            if isinstance(data, dict):
                # Legacy sequence should have beats
                if "beats" in data:
                    return isinstance(data["beats"], list)
                # Legacy beat should have letter
                elif "letter" in data:
                    return isinstance(data["letter"], str)
            return False
        except Exception:
            return False

    def get_conversion_metadata(self, legacy_data: dict[str, Any]) -> dict[str, Any]:
        """Get metadata about conversion (interface implementation)."""
        return {
            "source_format": "legacy",
            "target_format": "modern",
            "data_type": "sequence" if "beats" in legacy_data else "beat",
            "conversion_timestamp": "runtime",
            "converter_version": "1.0",
        }

    # Interface implementation methods
    def convert_sequence(self, legacy_sequence: list[dict[str, Any]]) -> Any | None:
        """Convert legacy sequence to modern format."""
        try:
            from desktop.modern.domain.models.sequence_data import SequenceData

            beats = []
            for i, beat_dict in enumerate(legacy_sequence):
                beat_data = self.convert_legacy_to_beat_data(beat_dict, i + 1)
                if beat_data:
                    beats.append(beat_data)
            return SequenceData(beats=beats)
        except Exception as e:
            logger.error(f"Error converting legacy sequence: {e}")
            return None

    def convert_beat(self, legacy_beat: dict[str, Any]) -> Any | None:
        """Convert legacy beat to modern format."""
        try:
            beat_number = legacy_beat.get("beat_number", 1)
            return self.convert_legacy_to_beat_data(legacy_beat, beat_number)
        except Exception as e:
            logger.error(f"Error converting legacy beat: {e}")
            return None

    def convert_pictograph(self, legacy_pictograph: dict[str, Any]) -> Any | None:
        """Convert legacy pictograph to modern format."""
        try:
            # TODO: Implement pictograph conversion
            return None
        except Exception as e:
            logger.error(f"Error converting legacy pictograph: {e}")
            return None
