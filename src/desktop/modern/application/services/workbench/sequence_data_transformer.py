"""
Sequence Data Transformer Service

Handles all data transformation operations between different formats.
Follows the Single Responsibility Principle by focusing solely on
data format conversion.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from desktop.modern.core.interfaces.export_services import ISequenceDataTransformer
from desktop.modern.domain.models import BeatData, PictographData, SequenceData


logger = logging.getLogger(__name__)


class SequenceDataTransformer(ISequenceDataTransformer):
    """
    Service responsible for transforming sequence data between different formats.

    Responsibilities:
    - Convert SequenceData to image export format
    - Convert SequenceData to legacy JSON format
    - Extract and transform beat attributes
    - Handle position and motion data extraction
    """

    def to_image_export_format(self, sequence: SequenceData) -> list[dict[str, Any]]:
        """Convert SequenceData to format expected by image export services."""
        sequence_data = []

        for beat in sequence.beats:
            # Convert beat to dictionary format expected by image export
            beat_data = {
                "beat_number": beat.beat_number,
                "letter": self._extract_letter_from_beat(beat),
                "start_pos": self._extract_start_position_from_beat(beat),
                "end_pos": self._extract_end_position_from_beat(beat),
                "blue_attributes": self.extract_beat_attributes(
                    beat.pictograph_data, "blue"
                ),
                "red_attributes": self.extract_beat_attributes(
                    beat.pictograph_data, "red"
                ),
                "pictograph_data": (
                    beat.pictograph_data.to_dict() if beat.pictograph_data else None
                ),
                "is_blank": beat.is_blank,
                "blue_reversal": beat.blue_reversal,
                "red_reversal": beat.red_reversal,
            }
            sequence_data.append(beat_data)

        return sequence_data

    def to_legacy_json_format(self, sequence: SequenceData) -> list[dict[str, Any]]:
        """Convert SequenceData to legacy-compatible JSON format."""
        sequence_json = []

        # First element: sequence metadata (legacy format)
        metadata = {
            "word": sequence.word or "",
            "author": sequence.author or "",
            "level": sequence.level or 1,
            "prop_type": sequence.prop_type or "staff",
            "grid_mode": sequence.grid_mode or "diamond",
            "is_circular": sequence.is_circular,
            "can_be_CAP": sequence.metadata.get("can_be_CAP", True),
            "is_strict_rotated_CAP": sequence.metadata.get(
                "is_strict_rotated_CAP", False
            ),
            "is_strict_mirrored_CAP": sequence.metadata.get(
                "is_strict_mirrored_CAP", True
            ),
            "is_strict_swapped_CAP": sequence.metadata.get(
                "is_strict_swapped_CAP", False
            ),
            "is_mirrored_swapped_CAP": sequence.metadata.get(
                "is_mirrored_swapped_CAP", False
            ),
            "is_rotated_swapped_CAP": sequence.metadata.get(
                "is_rotated_swapped_CAP", False
            ),
        }
        sequence_json.append(metadata)

        # Add beat data in legacy format
        for beat in sequence.beats:
            beat_json = self._convert_beat_to_legacy_format(beat)
            if beat_json:
                sequence_json.append(beat_json)

        return sequence_json

    def extract_beat_attributes(
        self, pictograph_data: Optional[PictographData], color: str
    ) -> dict[str, Any]:
        """Extract motion attributes for a specific color from beat data."""
        attributes = {}

        if pictograph_data and hasattr(pictograph_data, "motions"):
            motion_data = pictograph_data.motions.get(color)
            if motion_data:
                # Extract the actual values from enums using .value if available, otherwise convert to string
                motion_type = getattr(motion_data, "motion_type", "")
                motion_type = (
                    getattr(motion_type, "value", str(motion_type))
                    if motion_type
                    else ""
                )

                prop_rot_dir = getattr(motion_data, "prop_rot_dir", "")
                prop_rot_dir = (
                    getattr(prop_rot_dir, "value", str(prop_rot_dir))
                    if prop_rot_dir
                    else ""
                )

                start_ori = getattr(motion_data, "start_ori", "")
                start_ori = (
                    getattr(start_ori, "value", str(start_ori)) if start_ori else ""
                )

                end_ori = getattr(motion_data, "end_ori", "")
                end_ori = getattr(end_ori, "value", str(end_ori)) if end_ori else ""

                attributes = {
                    "motion_type": motion_type,
                    "prop_rot_dir": prop_rot_dir,
                    "turns": getattr(motion_data, "turns", 0),
                    "start_ori": start_ori,
                    "end_ori": end_ori,
                }

        return attributes

    def _convert_beat_to_legacy_format(
        self, beat: BeatData
    ) -> Optional[dict[str, Any]]:
        """Convert modern BeatData to legacy JSON format."""
        try:
            if not beat.pictograph_data:
                logger.warning(f"Beat {beat.beat_number} has no pictograph data")
                return None

            pictograph_data = beat.pictograph_data

            # Extract letter from pictograph data
            letter = pictograph_data.letter or ""

            # Determine if this is a start position (beat 0)
            is_start_position = beat.beat_number == 0 or beat.metadata.get(
                "is_start_position", False
            )

            # Base beat data
            beat_json = {
                "beat": beat.beat_number,
                "letter": letter,
                "duration": beat.duration,
            }

            # Add start position specific fields
            if is_start_position:
                beat_json["sequence_start_position"] = (
                    self._extract_start_position_type(pictograph_data)
                )

            # Add position data
            beat_json.update(
                {
                    "start_pos": self._extract_position_string(
                        pictograph_data.start_position
                    ),
                    "end_pos": self._extract_position_string(
                        pictograph_data.end_position
                    ),
                    "timing": self._extract_timing_string(pictograph_data.timing),
                    "direction": self._extract_direction_string(
                        pictograph_data.direction
                    ),
                }
            )

            # Add letter type if available
            if hasattr(pictograph_data, "letter_type") and pictograph_data.letter_type:
                beat_json["letter_type"] = str(pictograph_data.letter_type)

            # Add motion attributes for blue and red
            beat_json["blue_attributes"] = self.extract_beat_attributes(
                pictograph_data, "blue"
            )
            beat_json["red_attributes"] = self.extract_beat_attributes(
                pictograph_data, "red"
            )

            return beat_json

        except Exception as e:
            logger.error(
                f"Failed to convert beat {beat.beat_number} to legacy format: {e}"
            )
            return None

    def _extract_letter_from_beat(self, beat: BeatData) -> str:
        """Extract letter from beat data."""
        if beat.pictograph_data and hasattr(beat.pictograph_data, "letter"):
            return beat.pictograph_data.letter
        return beat.metadata.get("letter", "A")

    def _extract_start_position_from_beat(self, beat: BeatData) -> str:
        """Extract start position from beat data."""
        if beat.pictograph_data and hasattr(beat.pictograph_data, "start_position"):
            return beat.pictograph_data.start_position
        return beat.metadata.get("start_pos", "alpha")

    def _extract_end_position_from_beat(self, beat: BeatData) -> str:
        """Extract end position from beat data."""
        if beat.pictograph_data and hasattr(beat.pictograph_data, "end_position"):
            return beat.pictograph_data.end_position
        return beat.metadata.get("end_pos", "beta")

    def _extract_start_position_type(self, pictograph: PictographData) -> str:
        """Extract start position type (alpha, beta, gamma) from pictograph."""
        if not pictograph.start_position:
            return "alpha"  # Default

        position_str = str(pictograph.start_position).lower()
        if "alpha" in position_str:
            return "alpha"
        if "beta" in position_str:
            return "beta"
        if "gamma" in position_str:
            return "gamma"
        return "alpha"  # Default fallback

    def _extract_position_string(self, position) -> str:
        """Extract position string from position object."""
        if not position:
            return ""
        return str(position)

    def _extract_timing_string(self, timing) -> str:
        """Extract timing string from timing enum."""
        if not timing:
            return "none"
        return str(timing).lower()

    def _extract_direction_string(self, direction) -> str:
        """Extract direction string from direction enum."""
        if not direction:
            return "none"
        return str(direction).lower()
