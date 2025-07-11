"""
Beat Data Converter

Handles conversion of external pictograph data to BeatData format.
Provides backward compatibility for systems expecting BeatData objects.
"""

import logging
from typing import Any, Dict

try:
    from domain.models import BeatData

    from .external_data_converter import ExternalDataConverter
except ImportError:
    # Fallback for tests
    pass

logger = logging.getLogger(__name__)


class BeatDataConverter:
    """
    Converts external pictograph data to BeatData format.

    Provides backward compatibility by converting external data to PictographData first,
    then extracting the necessary information to create BeatData objects.
    """

    def __init__(self):
        """Initialize the beat data converter."""
        self.external_converter = ExternalDataConverter()

    def convert_external_pictograph_to_beat_data(
        self, external_data: Dict[str, Any]
    ) -> BeatData:
        """
        Convert external pictograph data to BeatData format.

        Args:
            external_data: External pictograph data dictionary

        Returns:
            BeatData object with converted motion information
        """
        # Convert to pictograph data first
        pictograph_data = (
            self.external_converter.convert_external_pictograph_to_pictograph_data(
                external_data
            )
        )

        # Extract motion data from arrows
        blue_motion = None
        red_motion = None

        if "blue" in pictograph_data.arrows:
            blue_motion = pictograph_data.motions["blue"]
        if "red" in pictograph_data.arrows:
            red_motion = pictograph_data.motions["red"]

        # Create BeatData with extracted information
        return BeatData(
            beat_number=1,  # Default beat number for external conversions
            pictograph_data=pictograph_data,  # NEW: Use pictograph data with motions
            letter=pictograph_data.letter,
            is_blank=pictograph_data.is_blank,
            glyph_data=pictograph_data.glyph_data,
        )

    def convert_multiple_external_to_beat_data(
        self, external_pictographs: list
    ) -> list:
        """
        Convert multiple external pictographs to BeatData format.

        Args:
            external_pictographs: List of external pictograph data dictionaries

        Returns:
            List of BeatData objects
        """
        beat_data_list = []

        for i, external_data in enumerate(external_pictographs):
            try:
                beat_data = self.convert_external_pictograph_to_beat_data(external_data)
                # Update beat number to reflect position in sequence
                beat_data = beat_data.update(beat_number=i + 1)
                beat_data_list.append(beat_data)
            except Exception as e:
                logger.warning(f"Failed to convert pictograph {i}: {e}")
                continue

        return beat_data_list

    def validate_external_data_for_beat(self, external_data: Dict[str, Any]) -> bool:
        """
        Validate external data for BeatData conversion.

        Args:
            external_data: External data to validate

        Returns:
            True if valid for BeatData conversion, False otherwise
        """
        return self.external_converter.validate_external_data(external_data)

    def get_supported_beat_fields(self) -> list:
        """Get list of fields supported in BeatData conversion."""
        return [
            "beat_number",
            "blue_motion",
            "red_motion",
            "letter",
            "start_position",
            "end_position",
            "is_blank",
            "glyph_data",
        ]
