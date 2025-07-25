"""
Beat Data Builder - Builder pattern for creating BeatData objects

Provides a clean, testable way to construct complex BeatData objects
with optional fields and proper validation.
"""

import logging
from typing import Any, Dict, Optional

from core.interfaces.data_builder_services import IBeatDataBuilder
from domain.models.beat_data import BeatData
from domain.models.enums import GridMode, GridPosition
from domain.models.grid_data import GridData
from domain.models.motion_data import MotionData
from domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class BeatDataBuilder(IBeatDataBuilder):
    """Builder pattern for creating BeatData objects with complex construction."""

    def __init__(self):
        """Initialize builder with default values."""
        self._beat_number: int = 1
        self._letter: str = ""
        self._duration: float = 1.0
        self._is_blank: bool = True
        self._metadata: Dict[str, Any] = {}
        self._glyph_data: Optional[GlyphData] = None
        self._pictograph_data: Optional[PictographData] = None
        self._blue_motion: Optional[MotionData] = None
        self._red_motion: Optional[MotionData] = None
        self._start_position: Optional[GridPosition] = None
        self._end_position: Optional[GridPosition] = None

    def with_beat_number(self, beat_number: int) -> "BeatDataBuilder":
        """Set the beat number."""
        self._beat_number = beat_number
        return self

    def with_letter(self, letter: str) -> "BeatDataBuilder":
        """Set the beat letter."""
        self._letter = letter
        return self

    def with_duration(self, duration: float) -> "BeatDataBuilder":
        """Set the beat duration."""
        self._duration = duration
        return self

    def with_motion_data(
        self, blue: Optional[MotionData], red: Optional[MotionData]
    ) -> "BeatDataBuilder":
        """Set blue and red motion data."""
        self._blue_motion = blue
        self._red_motion = red
        self._is_blank = not (blue or red)
        return self

    def with_positions(self, start_pos: str, end_pos: str) -> "BeatDataBuilder":
        """Set start and end positions."""
        self._start_position = start_pos
        self._end_position = end_pos
        return self

    def with_glyph_data(self, start_pos: str, end_pos: str) -> "BeatDataBuilder":
        """Set glyph data with positions."""
        self._glyph_data = GlyphData(start_position=start_pos, end_position=end_pos)
        self._start_position = start_pos
        self._end_position = end_pos
        return self

    def with_metadata(self, metadata: Dict[str, Any]) -> "BeatDataBuilder":
        """Set metadata dictionary."""
        self._metadata = metadata.copy()
        return self

    def add_metadata(self, key: str, value: Any) -> "BeatDataBuilder":
        """Add a single metadata entry."""
        self._metadata[key] = value
        return self

    def as_start_position(
        self, sequence_start_position: str = "alpha1"
    ) -> "BeatDataBuilder":
        """Configure as start position beat."""
        self._beat_number = 0
        self._duration = 0.0
        self.add_metadata("is_start_position", True)
        self.add_metadata("sequence_start_position", sequence_start_position)
        return self

    def build(self) -> BeatData:
        """
        Build the BeatData object with all configured properties.

        Returns:
            Constructed BeatData object

        Raises:
            ValueError: If required data is missing or invalid
        """
        # Create motions dictionary
        motions = {}
        if self._blue_motion:
            motions["blue"] = self._blue_motion
        if self._red_motion:
            motions["red"] = self._red_motion

        # Create pictograph data if we have motions or positions
        pictograph_data = None
        if motions or self._start_position or self._end_position:
            pictograph_data = PictographData(
                motions=motions,
                letter=self._letter,
                start_position=self._start_position,
                end_position=self._end_position,
                grid_data=GridData(grid_mode=GridMode.DIAMOND),  # Default grid mode
                arrows={},  # Will be populated based on motions if needed
                is_blank=self._is_blank,
                metadata=self._metadata.copy(),
            )

        # Glyph data is no longer needed - all glyph information is computed from PictographData

        # Build the BeatData
        try:
            beat_data = BeatData(
                beat_number=self._beat_number,
                duration=self._duration,
                pictograph_data=pictograph_data,
                is_blank=self._is_blank,
                metadata=self._metadata.copy(),
            )

            logger.debug(
                f"Built BeatData: beat_number={self._beat_number}, letter={self._letter}"
            )
            return beat_data

        except Exception as e:
            error_msg = f"Failed to build BeatData: {e}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e

    def reset(self) -> "BeatDataBuilder":
        """Reset builder to default state for reuse."""
        self.__init__()
        return self

    # Interface implementation methods
    def build_beat_data(self, beat_config: Dict[str, Any]) -> Any:
        """Build beat data from configuration (interface implementation)."""
        # Reset builder and apply configuration
        self.reset()

        if "beat_number" in beat_config:
            self.with_beat_number(beat_config["beat_number"])
        if "letter" in beat_config:
            self.with_letter(beat_config["letter"])
        if "duration" in beat_config:
            self.with_duration(beat_config["duration"])
        if "blue_motion" in beat_config or "red_motion" in beat_config:
            self.with_motion_data(
                beat_config.get("blue_motion"), beat_config.get("red_motion")
            )
        if "start_position" in beat_config and "end_position" in beat_config:
            self.with_positions(
                beat_config["start_position"], beat_config["end_position"]
            )
        if "metadata" in beat_config:
            for key, value in beat_config["metadata"].items():
                self.add_metadata(key, value)

        return self.build()

    def validate_beat_config(self, beat_config: Dict[str, Any]) -> bool:
        """Validate beat configuration (interface implementation)."""
        try:
            # Check required fields exist and are valid types
            if "beat_number" in beat_config:
                if (
                    not isinstance(beat_config["beat_number"], int)
                    or beat_config["beat_number"] < 0
                ):
                    return False

            if "duration" in beat_config:
                if (
                    not isinstance(beat_config["duration"], (int, float))
                    or beat_config["duration"] < 0
                ):
                    return False

            if "letter" in beat_config:
                if not isinstance(beat_config["letter"], str):
                    return False

            # Validate motion data if present
            for motion_key in ["blue_motion", "red_motion"]:
                if motion_key in beat_config:
                    motion = beat_config[motion_key]
                    if motion is not None and not hasattr(motion, "__dict__"):
                        return False

            return True
        except Exception:
            return False

    def get_default_beat_config(self) -> Dict[str, Any]:
        """Get default beat configuration (interface implementation)."""
        return {
            "beat_number": 1,
            "letter": "",
            "duration": 1.0,
            "blue_motion": None,
            "red_motion": None,
            "start_position": None,
            "end_position": None,
            "metadata": {},
        }

    def build_from_legacy_data(self, legacy_data: Dict[str, Any]) -> Any:
        """Build beat data from legacy format (interface implementation)."""
        # Reset and configure from legacy data
        self.reset()

        # Map legacy fields to modern configuration
        if "beat" in legacy_data:
            self.with_beat_number(legacy_data["beat"])
        if "letter" in legacy_data:
            self.with_letter(legacy_data["letter"])
        if "duration" in legacy_data:
            self.with_duration(legacy_data["duration"])

        # Handle legacy motion format
        if "motions" in legacy_data:
            motions = legacy_data["motions"]
            blue_motion = motions.get("blue")
            red_motion = motions.get("red")
            self.with_motion_data(blue_motion, red_motion)

        # Handle legacy position format
        if "start_pos" in legacy_data and "end_pos" in legacy_data:
            self.with_positions(legacy_data["start_pos"], legacy_data["end_pos"])

        return self.build()
