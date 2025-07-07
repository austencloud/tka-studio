"""
SequenceDataConverter

Handles conversion between legacy JSON format and modern domain models.
Responsible for maintaining compatibility with legacy sequence data structures.
"""

from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
    Orientation,
    SequenceData,
)


class SequenceDataConverter:
    """
    Service for converting between legacy JSON format and modern domain models.

    Responsibilities:
    - Converting legacy JSON to modern BeatData
    - Converting modern BeatData to legacy JSON
    - Handling start position conversions
    - Maintaining data fidelity during conversions
    """

    def convert_legacy_to_beat_data(
        self, beat_dict: dict, beat_number: int
    ) -> BeatData:
        """Convert legacy JSON format back to modern BeatData with full pictograph data"""

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
        # CORRECTED: Convert strings to proper enum values
        def convert_motion_type(motion_str: str) -> MotionType:
            """Convert motion type string to MotionType enum"""
            motion_map = {
                "pro": MotionType.PRO,
                "anti": MotionType.ANTI,
                "static": MotionType.STATIC,
                "dash": MotionType.DASH,
                "float": MotionType.FLOAT,
            }
            return motion_map.get(motion_str, MotionType.STATIC)

        def convert_location(loc_str: str) -> Location:
            """Convert location string to Location enum"""
            location_map = {
                "n": Location.NORTH,
                "s": Location.SOUTH,
                "e": Location.EAST,
                "w": Location.WEST,
                "ne": Location.NORTHEAST,
                "nw": Location.NORTHWEST,
                "se": Location.SOUTHEAST,
                "sw": Location.SOUTHWEST,
            }
            return location_map.get(loc_str, Location.NORTH)

        def convert_rotation_dir(rot_str: str) -> RotationDirection:
            """Convert rotation direction string to RotationDirection enum"""
            rotation_map = {
                "cw": RotationDirection.CLOCKWISE,
                "ccw": RotationDirection.COUNTER_CLOCKWISE,
                "no_rot": RotationDirection.NO_ROTATION,
            }
            return rotation_map.get(rot_str, RotationDirection.NO_ROTATION)

        def convert_orientation(ori_str: str) -> Orientation:
            """Convert orientation string to Orientation enum"""
            orientation_map = {
                "in": Orientation.IN,
                "out": Orientation.OUT,
                "clock": Orientation.CLOCK,
                "counter": Orientation.COUNTER,
            }
            return orientation_map.get(ori_str, Orientation.IN)

        blue_motion = MotionData(
            motion_type=convert_motion_type(blue_attrs.get("motion_type", "static")),
            start_loc=convert_location(blue_attrs.get("start_loc", "n")),
            end_loc=convert_location(blue_attrs.get("end_loc", "n")),
            start_ori=convert_orientation(blue_attrs.get("start_ori", "in")),
            end_ori=convert_orientation(blue_attrs.get("end_ori", "in")),
            prop_rot_dir=convert_rotation_dir(blue_attrs.get("prop_rot_dir", "no_rot")),
            turns=blue_attrs.get("turns", 0),
        )

        red_motion = MotionData(
            motion_type=convert_motion_type(red_attrs.get("motion_type", "static")),
            start_loc=convert_location(red_attrs.get("start_loc", "n")),
            end_loc=convert_location(red_attrs.get("end_loc", "n")),
            start_ori=convert_orientation(red_attrs.get("start_ori", "in")),
            end_ori=convert_orientation(red_attrs.get("end_ori", "in")),
            prop_rot_dir=convert_rotation_dir(red_attrs.get("prop_rot_dir", "no_rot")),
            turns=red_attrs.get("turns", 0),
        )

        # Create glyph data as proper GlyphData object
        from domain.models.core_models import GlyphData
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

    def convert_legacy_start_position_to_beat_data(
        self, start_pos_dict: dict
    ) -> BeatData:
        """Convert legacy start position JSON back to modern BeatData with full data"""

        # Extract basic start position info
        letter = start_pos_dict.get("letter", "A")
        end_pos = start_pos_dict.get("end_pos", "alpha1")
        sequence_start_position = start_pos_dict.get("sequence_start_position", "alpha")

        # Extract motion attributes
        blue_attrs = start_pos_dict.get("blue_attributes", {})
        red_attrs = start_pos_dict.get("red_attributes", {})

        # Create motion data for blue and red (start positions are typically static)
        # CORRECTED: Handle location and orientation conversion properly
        def convert_location(loc_str: str) -> Location:
            """Convert legacy location strings to valid Location enum values"""
            # Location strings are already correct: "n", "s", "e", "w", "ne", "nw", "se", "sw"
            # Do NOT convert "alpha", "beta", "gamma" - those are position TYPES, not locations
            location_map = {
                "n": Location.NORTH,
                "s": Location.SOUTH,
                "e": Location.EAST,
                "w": Location.WEST,
                "ne": Location.NORTHEAST,
                "nw": Location.NORTHWEST,
                "se": Location.SOUTHEAST,
                "sw": Location.SOUTHWEST,
            }
            return location_map.get(loc_str, Location.NORTH)

        def convert_orientation(ori_value) -> Orientation:
            """Convert legacy orientation values to valid Orientation enum values"""
            # Orientations are stored as strings in JSON: "in", "out", "clock", "counter"
            # Only convert if we get numeric values (legacy compatibility)
            if isinstance(ori_value, (int, float)):
                ori_map = {0: Orientation.IN, 90: Orientation.CLOCK, 180: Orientation.OUT, 270: Orientation.COUNTER}
                return ori_map.get(int(ori_value), Orientation.IN)

            orientation_map = {
                "in": Orientation.IN,
                "out": Orientation.OUT,
                "clock": Orientation.CLOCK,
                "counter": Orientation.COUNTER,
            }
            return orientation_map.get(str(ori_value), Orientation.IN)

        blue_motion = MotionData(
            motion_type=self._convert_motion_type(blue_attrs.get("motion_type", "static")),
            start_loc=(
                convert_location(blue_attrs.get("start_loc", sequence_start_position))
            ),
            end_loc=(
                convert_location(blue_attrs.get("end_loc", sequence_start_position))
            ),
            start_ori=convert_orientation(blue_attrs.get("start_ori", "in")),
            end_ori=convert_orientation(blue_attrs.get("end_ori", "in")),
            prop_rot_dir=self._convert_rotation_direction(blue_attrs.get("prop_rot_dir", "no_rot")),
            turns=blue_attrs.get("turns", 0),
        )

        red_motion = MotionData(
            motion_type=self._convert_motion_type(red_attrs.get("motion_type", "static")),
            start_loc=(
                convert_location(red_attrs.get("start_loc", sequence_start_position))
            ),
            end_loc=(
                convert_location(red_attrs.get("end_loc", sequence_start_position))
            ),
            start_ori=convert_orientation(red_attrs.get("start_ori", "in")),
            end_ori=convert_orientation(red_attrs.get("end_ori", "in")),
            prop_rot_dir=self._convert_rotation_direction(red_attrs.get("prop_rot_dir", "no_rot")),
            turns=red_attrs.get("turns", 0),
        )

        # Create glyph data with position information as proper GlyphData object
        from domain.models.core_models import GlyphData
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

    def convert_beat_data_to_legacy_format(
        self, beat: BeatData, beat_number: int
    ) -> dict:
        """Convert modern BeatData to legacy JSON format exactly like legacy pictograph_data"""
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
        blue_attrs = {
            "start_loc": (
                beat.blue_motion.start_loc.value if beat.blue_motion else "alpha"
            ),
            "end_loc": (
                beat.blue_motion.end_loc.value if beat.blue_motion else "alpha"
            ),
            "start_ori": (beat.blue_motion.start_ori.value if beat.blue_motion else 0),
            "end_ori": (beat.blue_motion.end_ori.value if beat.blue_motion else 0),
            "prop_rot_dir": (
                beat.blue_motion.prop_rot_dir.value if beat.blue_motion else "no_rot"
            ),
            "turns": beat.blue_motion.turns if beat.blue_motion else 0,
            "motion_type": (
                beat.blue_motion.motion_type.value if beat.blue_motion else "static"
            ),
        }

        # Convert red motion data
        red_attrs = {
            "start_loc": (
                beat.red_motion.start_loc.value if beat.red_motion else "alpha"
            ),
            "end_loc": (beat.red_motion.end_loc.value if beat.red_motion else "alpha"),
            "start_ori": (beat.red_motion.start_ori.value if beat.red_motion else 0),
            "end_ori": beat.red_motion.end_ori.value if beat.red_motion else 0,
            "prop_rot_dir": (
                beat.red_motion.prop_rot_dir.value if beat.red_motion else "no_rot"
            ),
            "turns": beat.red_motion.turns if beat.red_motion else 0,
            "motion_type": (
                beat.red_motion.motion_type.value if beat.red_motion else "static"
            ),
        }

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

    def convert_start_position_to_legacy_format(
        self, start_position_data: BeatData
    ) -> dict:
        """Convert start position BeatData to legacy format exactly like JsonStartPositionHandler"""
        # Extract start position type (alpha, beta, gamma) from glyph_data if available
        end_pos = "alpha1"  # Default
        sequence_start_position = "alpha"  # Default

        if (
            start_position_data.glyph_data
            and start_position_data.glyph_data.end_position
        ):
            end_pos = start_position_data.glyph_data.end_position
            if end_pos.startswith("alpha"):
                sequence_start_position = "alpha"
            elif end_pos.startswith("beta"):
                sequence_start_position = "beta"
            elif end_pos.startswith("gamma"):
                sequence_start_position = "gamma"
            else:
                sequence_start_position = end_pos.rstrip("0123456789")

        # Convert motion data
        blue_attrs = {
            "start_loc": (
                start_position_data.blue_motion.start_loc.value
                if start_position_data.blue_motion
                else sequence_start_position
            ),
            "end_loc": (
                start_position_data.blue_motion.end_loc.value
                if start_position_data.blue_motion
                else sequence_start_position
            ),
            "start_ori": (
                start_position_data.blue_motion.start_ori.value
                if start_position_data.blue_motion
                and hasattr(start_position_data.blue_motion.start_ori, "value")
                else (
                    start_position_data.blue_motion.start_ori
                    if start_position_data.blue_motion
                    else "in"
                )
            ),
            "end_ori": (
                start_position_data.blue_motion.end_ori.value
                if start_position_data.blue_motion
                and hasattr(start_position_data.blue_motion.end_ori, "value")
                else (
                    start_position_data.blue_motion.end_ori
                    if start_position_data.blue_motion
                    else "in"
                )
            ),
            "prop_rot_dir": "no_rot",  # Start positions don't rotate
            "turns": 0,  # Start positions don't have turns
            "motion_type": (
                start_position_data.blue_motion.motion_type.value
                if start_position_data.blue_motion
                else "static"
            ),
        }

        red_attrs = {
            "start_loc": (
                start_position_data.red_motion.start_loc.value
                if start_position_data.red_motion
                else sequence_start_position
            ),
            "end_loc": (
                start_position_data.red_motion.end_loc.value
                if start_position_data.red_motion
                else sequence_start_position
            ),
            "start_ori": (
                start_position_data.red_motion.start_ori.value
                if start_position_data.red_motion
                and hasattr(start_position_data.red_motion.start_ori, "value")
                else (
                    start_position_data.red_motion.start_ori
                    if start_position_data.red_motion
                    else "in"
                )
            ),
            "end_ori": (
                start_position_data.red_motion.end_ori.value
                if start_position_data.red_motion
                and hasattr(start_position_data.red_motion.end_ori, "value")
                else (
                    start_position_data.red_motion.end_ori
                    if start_position_data.red_motion
                    else "in"
                )
            ),
            "prop_rot_dir": "no_rot",  # Start positions don't rotate
            "turns": 0,  # Start positions don't have turns
            "motion_type": (
                start_position_data.red_motion.motion_type.value
                if start_position_data.red_motion
                else "static"
            ),
        }

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

    def convert_sequence_to_legacy_format(self, sequence: SequenceData) -> list:
        """Convert modern SequenceData back to legacy JSON format"""
        try:
            legacy_data = []

            # Separate start position from regular beats
            start_position_beat = None
            regular_beats = []

            for beat in sequence.beats:
                if beat.beat_number == 0 and beat.metadata.get(
                    "is_start_position", False
                ):
                    start_position_beat = beat
                else:
                    regular_beats.append(beat)

            # Add sequence metadata as first item [0]
            metadata = {
                "sequence_name": sequence.name,
                "beat_count": len(regular_beats),  # Only count regular beats
                "length": len(regular_beats),
                "level": 1,
                "sequence_start_position": "alpha",  # Default for now
            }
            legacy_data.append(metadata)

            # Only add start position if it actually exists (user selected one)
            if start_position_beat:
                start_pos_dict = self.convert_start_position_to_legacy_format(
                    start_position_beat
                )
                legacy_data.append(start_pos_dict)

            # Convert regular beats to legacy format (starting at index [2])
            for beat in regular_beats:
                beat_dict = self._convert_beat_to_legacy_dict(beat)
                legacy_data.append(beat_dict)

            return legacy_data

        except Exception as e:
            print(
                f"❌ [DATA_CONVERTER] Failed to convert sequence to legacy format: {e}"
            )
            return []

    def _convert_beat_to_legacy_dict(self, beat: BeatData) -> dict:
        """Convert a single BeatData to legacy dictionary format"""
        return {
            "beat": beat.beat_number,
            "letter": beat.letter,
            "duration": beat.duration,
            "start_pos": "alpha1",  # Default for now
            "end_pos": "alpha1",  # Default for now
            "timing": "same",
            "direction": "cw",
            "blue_attributes": {
                "start_loc": (
                    beat.blue_motion.start_loc.value if beat.blue_motion else "s"
                ),
                "end_loc": beat.blue_motion.end_loc.value if beat.blue_motion else "s",
                "start_ori": (
                    beat.blue_motion.start_ori.value if beat.blue_motion else "in"
                ),
                "end_ori": beat.blue_motion.end_ori.value if beat.blue_motion else "in",
                "prop_rot_dir": (
                    beat.blue_motion.prop_rot_dir.value
                    if beat.blue_motion
                    else "no_rot"
                ),
                "turns": beat.blue_motion.turns if beat.blue_motion else 0,
                "motion_type": (
                    beat.blue_motion.motion_type.value if beat.blue_motion else "static"
                ),
            },
            "red_attributes": {
                "start_loc": (
                    beat.red_motion.start_loc.value if beat.red_motion else "s"
                ),
                "end_loc": beat.red_motion.end_loc.value if beat.red_motion else "s",
                "start_ori": (
                    beat.red_motion.start_ori.value if beat.red_motion else "in"
                ),
                "end_ori": beat.red_motion.end_ori.value if beat.red_motion else "in",
                "prop_rot_dir": (
                    beat.red_motion.prop_rot_dir.value if beat.red_motion else "no_rot"
                ),
                "turns": beat.red_motion.turns if beat.red_motion else 0,
                "motion_type": (
                    beat.red_motion.motion_type.value if beat.red_motion else "static"
                ),
            },
        }

    def _convert_motion_type(self, motion_type_str: str) -> MotionType:
        """Convert string motion type to enum."""
        motion_type_map = {
            "pro": MotionType.PRO,
            "anti": MotionType.ANTI,
            "float": MotionType.FLOAT,
            "dash": MotionType.DASH,
            "static": MotionType.STATIC,
        }
        return motion_type_map.get(motion_type_str.lower(), MotionType.STATIC)

    def _convert_rotation_direction(self, rot_dir_str: str) -> RotationDirection:
        """Convert string rotation direction to enum."""
        rot_dir_map = {
            "cw": RotationDirection.CLOCKWISE,
            "ccw": RotationDirection.COUNTER_CLOCKWISE,
            "no_rot": RotationDirection.NO_ROTATION,
        }
        return rot_dir_map.get(rot_dir_str.lower(), RotationDirection.NO_ROTATION)
