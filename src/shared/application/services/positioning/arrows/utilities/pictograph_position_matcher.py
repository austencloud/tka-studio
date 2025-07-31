"""
Position Matching Service - Data-Driven Motion Generation

This service implements a data-driven position matching algorithm for motion generation.
The algorithm is simple: find all pictographs where start_pos matches the target position.

REFACTORED: Now works with PictographData directly instead of BeatData, following
the principle that pictographs should be standalone without beat-specific fields.
"""

from typing import Any, Optional

import pandas as pd

from desktop.modern.domain.models import (
    ArrowData,
    GridData,
    GridMode,
    Location,
    MotionData,
    MotionType,
    PictographData,
    RotationDirection,
)
from shared.application.services.pictograph.pictograph_csv_manager import (
    PictographCSVManager,
)


class PictographPositionMatcher:
    """
    Data-driven position matching service for motion generation.

    This service implements the core algorithm:
    `if item.get("start_pos") == target_position: next_opts.append(item)`

    No complex validation or rule-based generation - just simple dataset lookups.
    """

    def __init__(self):
        """Initialize position matching service with Modern's native dataset."""
        self.pictograph_manager = PictographCSVManager()

        self.pictograph_dataset: Optional[dict[str, list[dict[str, Any]]]] = None
        self._load_dataset()

    def _load_dataset(self):
        """Load dataset using Modern's native pictograph management service."""
        try:
            # Get the raw CSV dataset from Modern's service
            raw_dataset = self.pictograph_manager._load_csv_data()

            if raw_dataset is None or raw_dataset.empty:
                print("❌ Dataset is empty")
                self.pictograph_dataset = {}
                return

            # Convert to grouped dictionary format: {letter: [pictograph_data_list]}
            self.pictograph_dataset = self._convert_dataframe_to_grouped_dict(
                raw_dataset
            )

            # Log statistics
            total_pictographs = sum(
                len(group) for group in self.pictograph_dataset.values()
            )

        except Exception as e:
            print(f"❌ Failed to load dataset: {e}")
            self.pictograph_dataset = {}

    def _convert_dataframe_to_grouped_dict(
        self, df: pd.DataFrame
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Convert pandas DataFrame to grouped dictionary format for position matching.

        Args:
            df: Pandas DataFrame with pictograph data

        Returns:
            Dictionary in format: {letter: [pictograph_data_list]}
        """
        grouped_dict = {}

        for _, row in df.iterrows():
            letter = str(row.get("letter", "Unknown"))

            # Convert row to pictograph data format
            pictograph_data = {
                "letter": letter,
                "start_pos": str(row.get("start_pos", "unknown")),
                "end_pos": str(row.get("end_pos", "unknown")),
                "blue_attributes": {
                    "motion_type": str(row.get("blue_motion_type", "static")),
                    "prop_rot_dir": str(row.get("blue_prop_rot_dir", "no_rotation")),
                    "start_loc": str(row.get("blue_start_loc", "n")),
                    "end_loc": str(row.get("blue_end_loc", "n")),
                    "start_ori": str(row.get("blue_start_ori", "in")),
                    "end_ori": str(row.get("blue_end_ori", "in")),
                },
                "red_attributes": {
                    "motion_type": str(row.get("red_motion_type", "static")),
                    "prop_rot_dir": str(row.get("red_prop_rot_dir", "no_rotation")),
                    "start_loc": str(row.get("red_start_loc", "s")),
                    "end_loc": str(row.get("red_end_loc", "s")),
                    "start_ori": str(row.get("red_start_ori", "out")),
                    "end_ori": str(row.get("red_end_ori", "out")),
                },
            }

            if letter not in grouped_dict:
                grouped_dict[letter] = []

            grouped_dict[letter].append(pictograph_data)

        return grouped_dict

    def get_next_options(self, last_beat_end_pos: str) -> list[PictographData]:
        """
        Validated algorithm: find all pictographs where start_pos matches.

        This is the complete algorithm from the option_getter.py lines 120-131:
        ```python
        for group in self.pictograph_dataset.values():
            for item in group:
                if item.get("start_pos") == start:
                    next_opts.append(item)
        ```

        Args:
            last_beat_end_pos: The end position of the last beat

        Returns:
            List of PictographData objects that can follow the given position
        """

        if not self.pictograph_dataset:
            print("❌ No dataset loaded")
            return []

        print(
            f"🔍 [POSITION_MATCHER] Looking for pictographs with start_pos='{last_beat_end_pos}'"
        )

        next_opts = []
        dataset_groups_checked = 0
        total_items_checked = 0
        matches_found = 0

        # Validated algorithm implementation
        for group_key, group in self.pictograph_dataset.items():
            dataset_groups_checked += 1
            for item in group:
                total_items_checked += 1
                if item.get("start_pos") == last_beat_end_pos:  # ← THE ENTIRE ALGORITHM
                    letter = item.get("letter", "Unknown")
                    end_pos = item.get("end_pos", "N/A")
                    matches_found += 1

                    try:
                        pictograph_data = self._convert_dict_to_pictograph_data(item)
                        next_opts.append(pictograph_data)  # ← ADD TO VALID OPTIONS
                    except Exception as e:
                        print(f"   ❌ Failed to convert match {matches_found}: {e}")
                        continue

        return next_opts

    def _convert_dict_to_pictograph_data(self, item: dict[str, Any]) -> PictographData:
        """Convert dictionary item to PictographData using actual motion data from the dictionary."""
        letter = item.get("letter", "")

        # Extract actual motion data from the dictionary
        blue_attrs = item.get("blue_attributes", {})
        red_attrs = item.get("red_attributes", {})

        # Convert blue motion
        blue_motion = MotionData(
            motion_type=self._parse_motion_type(
                blue_attrs.get("motion_type", "static")
            ),
            prop_rot_dir=self._parse_rotation_direction(
                blue_attrs.get("prop_rot_dir", "no_rot")
            ),
            start_loc=self._parse_location(blue_attrs.get("start_loc", "s")),
            end_loc=self._parse_location(blue_attrs.get("end_loc", "s")),
            turns=float(blue_attrs.get("turns", 0.0)),
            start_ori=blue_attrs.get("start_ori", "in"),
            end_ori=blue_attrs.get("end_ori", "in"),
        )

        # Convert red motion
        red_motion = MotionData(
            motion_type=self._parse_motion_type(red_attrs.get("motion_type", "static")),
            prop_rot_dir=self._parse_rotation_direction(
                red_attrs.get("prop_rot_dir", "no_rot")
            ),
            start_loc=self._parse_location(red_attrs.get("start_loc", "s")),
            end_loc=self._parse_location(red_attrs.get("end_loc", "s")),
            turns=float(red_attrs.get("turns", 0.0)),
            start_ori=red_attrs.get("start_ori", "in"),
            end_ori=red_attrs.get("end_ori", "in"),
        )

        # Create arrows (without motion data - motion data now lives in PictographData)
        arrows = {}
        if blue_motion:
            arrows["blue"] = ArrowData(
                color="blue",
                is_visible=True,
            )
        if red_motion:
            arrows["red"] = ArrowData(
                color="red",
                is_visible=True,
            )

        # Create grid data
        grid_data = GridData(
            grid_mode=GridMode.DIAMOND,
        )

        # Create motions dictionary
        motions = {}
        if blue_motion:
            motions["blue"] = blue_motion
        if red_motion:
            motions["red"] = red_motion

        # Create initial PictographData object with motion dictionary
        pictograph_data = PictographData(
            grid_data=grid_data,
            arrows=arrows,
            props={},  # Props will be generated during rendering
            motions=motions,  # NEW: Motion dictionary (consistent with arrows/props)
            letter=letter,
            start_position=item.get("start_pos", "unknown"),
            end_position=item.get("end_pos", "unknown"),
            is_blank=len(arrows) == 0,
            metadata={
                "source": "position_matching_service",
                "original_data": item,
            },
        )

        # Generate glyph data using the glyph data service
        self._generate_glyph_data(pictograph_data)

        # Return final PictographData object
        return pictograph_data

    def _generate_glyph_data(self, pictograph_data: PictographData) -> None:
        """Generate glyph data for pictograph data using the glyph data service."""
        from shared.application.services.glyphs.glyph_data_service import (
            GlyphDataService,
        )

        glyph_service = GlyphDataService()
        glyph_service.determine_glyph_data(pictograph_data)

    def _parse_motion_type(self, motion_type_str: str) -> "MotionType":
        """Parse motion type string to MotionType enum."""
        from desktop.modern.domain.models import MotionType

        motion_type_map = {
            "pro": MotionType.PRO,
            "anti": MotionType.ANTI,
            "static": MotionType.STATIC,
            "dash": MotionType.DASH,
            "float": MotionType.FLOAT,
        }
        return motion_type_map.get(motion_type_str.lower(), MotionType.STATIC)

    def _parse_rotation_direction(self, rot_dir_str: str) -> "RotationDirection":
        """Parse rotation direction string to RotationDirection enum."""
        from desktop.modern.domain.models import RotationDirection

        rot_dir_map = {
            "cw": RotationDirection.CLOCKWISE,
            "ccw": RotationDirection.COUNTER_CLOCKWISE,
            "no_rot": RotationDirection.NO_ROTATION,
        }
        return rot_dir_map.get(rot_dir_str.lower(), RotationDirection.NO_ROTATION)

    def _parse_location(self, location_str: str) -> "Location":
        """Parse location string to Location enum."""
        from desktop.modern.domain.models import Location

        location_map = {
            "n": Location.NORTH,
            "ne": Location.NORTHEAST,
            "e": Location.EAST,
            "se": Location.SOUTHEAST,
            "s": Location.SOUTH,
            "sw": Location.SOUTHWEST,
            "w": Location.WEST,
            "nw": Location.NORTHWEST,
        }
        return location_map.get(location_str.lower(), Location.SOUTH)

    def get_alpha1_options(self) -> list[PictographData]:
        """
        Convenience method to get Alpha 1 options (the canonical test case).

        Returns:
            List of PictographData objects that start from alpha1 position
        """
        return self.get_next_options("alpha1")

    def get_available_start_positions(self) -> list[str]:
        """
        Get all available start positions in the dataset.

        Returns:
            List of unique start position strings
        """
        if not self.pictograph_dataset:
            return []

        start_positions = set()
        for group in self.pictograph_dataset.values():
            for item in group:
                start_pos = item.get("start_pos")
                if start_pos:
                    start_positions.add(start_pos)

        return sorted(list(start_positions))

    def get_position_statistics(self, position: str) -> dict[str, Any]:
        """
        Get statistics for a specific position.

        Args:
            position: The position to analyze

        Returns:
            Dictionary with statistics about the position
        """
        options = self.get_next_options(position)

        if not options:
            return {
                "position": position,
                "total_options": 0,
                "letters": [],
                "letter_types": {},
            }

        # Import here to avoid circular imports
        from desktop.modern.domain.models.letter_type_classifier import (
            LetterTypeClassifier,
        )

        letters = [opt.letter or "Unknown" for opt in options]
        letter_types = {}

        for letter in letters:
            letter_type = LetterTypeClassifier.get_letter_type(letter)
            letter_types[letter_type] = letter_types.get(letter_type, 0) + 1

        return {
            "position": position,
            "total_options": len(options),
            "letters": letters,
            "letter_types": letter_types,
            "unique_letters": len(set(letters)),
        }

    def validate_dataset_integrity(self) -> dict[str, Any]:
        """
        Validate the integrity of the loaded dataset.

        Returns:
            Dictionary with validation results
        """
        if not self.pictograph_dataset:
            return {"valid": False, "error": "No dataset loaded"}

        issues = []
        total_pictographs = 0

        for letter, pictographs in self.pictograph_dataset.items():
            total_pictographs += len(pictographs)

            for i, pictograph in enumerate(pictographs):
                # Check required fields
                required_fields = [
                    "letter",
                    "start_pos",
                    "end_pos",
                    "blue_attributes",
                    "red_attributes",
                ]
                for field in required_fields:
                    if field not in pictograph:
                        issues.append(f"Letter {letter}[{i}]: Missing field '{field}'")

                # Check letter consistency
                if pictograph.get("letter") != letter:
                    issues.append(f"Letter {letter}[{i}]: Letter mismatch in data")

        return {
            "valid": len(issues) == 0,
            "total_pictographs": total_pictographs,
            "total_letters": len(self.pictograph_dataset),
            "issues": issues[:10],  # Limit to first 10 issues
            "total_issues": len(issues),
        }
