"""
Data and Filtering Module - Practical Generation Architecture

Handles data loading and filtering without over-engineered patterns.
Focused, testable, and maintainable - around 150 lines.
"""

from __future__ import annotations

from copy import deepcopy
import csv
import logging
from pathlib import Path
from typing import Any

from desktop.modern.core.interfaces.generation_services import (
    LetterType,
    PropContinuity,
)
from desktop.modern.domain.models.enums import (
    Location,
    MotionType,
    PropRotationDirection,
)
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData


logger = logging.getLogger(__name__)


class PictographDataManager:
    """
    Manages pictograph data loading and basic operations.
    Replaces over-engineered repository with simple, direct approach.
    """

    def __init__(self):
        self.diamond_data: list[dict[str, Any]] = []
        self.box_data: list[dict[str, Any]] = []
        self.all_data: list[dict[str, Any]] = []
        self._load_data()

    def _load_data(self) -> None:
        """Load CSV data once at startup."""
        try:
            data_dir = self._find_data_directory()
            if not data_dir:
                raise RuntimeError("Could not find data directory")

            # Load diamond pictographs
            diamond_file = data_dir / "DiamondPictographDataframe.csv"
            if diamond_file.exists():
                with open(diamond_file, encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    self.diamond_data = list(reader)

            # Load box pictographs
            box_file = data_dir / "BoxPictographDataframe.csv"
            if box_file.exists():
                with open(box_file, encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    self.box_data = list(reader)

            self.all_data = self.diamond_data + self.box_data
            logger.info(
                f"✅ Loaded {len(self.all_data)} pictographs ({len(self.diamond_data)} diamond, {len(self.box_data)} box)"
            )

        except Exception as e:
            logger.error(f"❌ Failed to load pictograph data: {e}")
            self.all_data = []

    def _find_data_directory(self) -> Path | None:
        """Find the data directory using multiple strategies."""
        # Try common locations
        possible_paths = [
            Path("src/desktop/data"),
            Path("desktop/data"),
            Path("data"),
            Path.cwd() / "src/desktop/data",
            Path.cwd() / "desktop/data",
        ]

        for path in possible_paths:
            if path.exists() and (path / "DiamondPictographDataframe.csv").exists():
                return path

        return None

    def get_all_data(self) -> list[dict[str, Any]]:
        """Get all pictograph data."""
        return self.all_data

    def get_diamond_data(self) -> list[dict[str, Any]]:
        """Get diamond pictograph data."""
        return self.diamond_data

    def get_box_data(self) -> list[dict[str, Any]]:
        """Get box pictograph data."""
        return self.box_data


class PictographFilter:
    """
    Simple, direct filtering without over-engineered chain patterns.
    Handles all filtering needs in one focused class.
    """

    # Letter type mappings - simplified but complete
    LETTER_TYPE_MAPPINGS = {
        LetterType.TYPE1: [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
        ],
        LetterType.TYPE2: ["W", "X", "Y", "Z"],
        LetterType.TYPE3: ["W-", "X-", "Y-", "Z-"],
        LetterType.TYPE4: ["Φ", "Ψ", "Λ"],
        LetterType.TYPE5: ["Φ-", "Ψ-", "Λ-"],
        LetterType.TYPE6: ["α", "β", "Γ"],
    }

    # Position mappings
    DIAMOND_POSITIONS = {
        "alpha1",
        "alpha3",
        "alpha5",
        "alpha7",
        "beta1",
        "beta3",
        "beta5",
        "beta7",
        "gamma1",
        "gamma3",
        "gamma5",
        "gamma7",
    }
    BOX_POSITIONS = {
        "alpha2",
        "alpha4",
        "alpha6",
        "alpha8",
        "beta2",
        "beta4",
        "beta6",
        "beta8",
        "gamma2",
        "gamma4",
        "gamma6",
        "gamma8",
    }

    def filter_options(
        self,
        options: list[dict[str, Any]],
        letter_types: set[LetterType] | None = None,
        current_end_position: str | None = None,
        grid_mode: str | None = None,
        prop_continuity: PropContinuity | None = None,
        blue_rot_dir: str | None = None,
        red_rot_dir: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Filter options using simple, direct logic.
        No complex chain patterns - just straightforward filtering.
        """
        if not options:
            return []

        filtered = deepcopy(options)

        # 1. Positional continuity (CRITICAL - must be first)
        if current_end_position:
            filtered = [
                opt for opt in filtered if opt.get("start_pos") == current_end_position
            ]
            logger.debug(
                f"Positional continuity: {len(filtered)} options start at {current_end_position}"
            )

        # 2. Letter type filtering
        if letter_types:
            allowed_letters = self._get_allowed_letters(letter_types)
            filtered = [opt for opt in filtered if opt.get("letter") in allowed_letters]
            logger.debug(
                f"Letter type filter: {len(filtered)} options match specified types"
            )

        # 3. Grid mode consistency
        if grid_mode:
            if grid_mode == "diamond":
                filtered = [
                    opt
                    for opt in filtered
                    if self._is_diamond_position(opt.get("start_pos"))
                ]
            elif grid_mode == "box":
                filtered = [
                    opt
                    for opt in filtered
                    if self._is_box_position(opt.get("start_pos"))
                ]
            logger.debug(f"Grid mode filter ({grid_mode}): {len(filtered)} options")

        # 4. Rotation continuity (if continuous mode)
        if prop_continuity == PropContinuity.CONTINUOUS and (
            blue_rot_dir or red_rot_dir
        ):
            filtered = self._filter_by_rotation_continuity(
                filtered, blue_rot_dir, red_rot_dir
            )
            logger.debug(f"Rotation continuity: {len(filtered)} options")

        return filtered

    def _get_allowed_letters(self, letter_types: set[LetterType]) -> set[str]:
        """Get allowed letters for specified types."""
        allowed = set()
        for letter_type in letter_types:
            allowed.update(self.LETTER_TYPE_MAPPINGS.get(letter_type, []))
        return allowed

    def _is_diamond_position(self, position: str) -> bool:
        """Check if position is diamond."""
        return position in self.DIAMOND_POSITIONS

    def _is_box_position(self, position: str) -> bool:
        """Check if position is box."""
        return position in self.BOX_POSITIONS

    def _filter_by_rotation_continuity(
        self,
        options: list[dict[str, Any]],
        blue_rot_dir: str | None,
        red_rot_dir: str | None,
    ) -> list[dict[str, Any]]:
        """Filter by rotation continuity for continuous prop mode."""
        if not (blue_rot_dir or red_rot_dir):
            return options

        filtered = []
        for opt in options:
            matches = True

            if blue_rot_dir and opt.get("blue_prop_rot_dir") != blue_rot_dir:
                matches = False

            if red_rot_dir and opt.get("red_prop_rot_dir") != red_rot_dir:
                matches = False

            if matches:
                filtered.append(opt)

        return filtered

    def determine_grid_mode(self, position: str) -> str | None:
        """Determine grid mode from position."""
        if self._is_diamond_position(position):
            return "diamond"
        if self._is_box_position(position):
            return "box"
        return None


class CSVToPictographConverter:
    """
    Simple converter from CSV data to PictographData objects.
    Direct, focused conversion without over-engineering.
    """

    def convert(
        self, csv_row: dict[str, Any], beat_number: int
    ) -> PictographData | None:
        """Convert CSV row to PictographData."""
        try:
            # Extract basic data
            letter = csv_row.get("letter", "").strip()
            start_pos = csv_row.get("start_pos", "").strip()
            end_pos = csv_row.get("end_pos", "").strip()

            # Create motion data
            motions = {}
            blue_motion = self._create_motion_data(csv_row, "blue")
            red_motion = self._create_motion_data(csv_row, "red")

            if blue_motion:
                motions["blue"] = blue_motion
            if red_motion:
                motions["red"] = red_motion

            return PictographData(
                letter=letter,
                start_position=start_pos,
                end_position=end_pos,
                beat=beat_number,
                motions=motions,
            )

        except Exception as e:
            logger.error(f"Failed to convert CSV row to PictographData: {e}")
            return None

    def _create_motion_data(
        self, csv_row: dict[str, Any], color: str
    ) -> MotionData | None:
        """Create MotionData from CSV row for specified color."""
        try:
            motion_type_str = csv_row.get(f"{color}_motion_type", "").strip()
            prop_rot_dir_str = csv_row.get(f"{color}_prop_rot_dir", "").strip()
            start_loc_str = csv_row.get(f"{color}_start_loc", "").strip()
            end_loc_str = csv_row.get(f"{color}_end_loc", "").strip()

            if not motion_type_str:
                return None

            # Convert to enums with fallbacks
            motion_type = self._str_to_motion_type(motion_type_str)
            prop_rot_dir = self._str_to_prop_rot_dir(prop_rot_dir_str)
            start_loc = self._str_to_location(start_loc_str)
            end_loc = self._str_to_location(end_loc_str)

            return MotionData(
                motion_type=motion_type,
                prop_rot_dir=prop_rot_dir,
                start_loc=start_loc,
                end_loc=end_loc,
                turns=0,  # Will be set later by turn application
            )

        except Exception as e:
            logger.error(f"Failed to create {color} motion data: {e}")
            return None

    def _str_to_motion_type(self, value: str) -> MotionType:
        """Convert string to MotionType enum."""
        mapping = {
            "static": MotionType.STATIC,
            "pro": MotionType.PRO,
            "anti": MotionType.ANTI,
            "dash": MotionType.DASH,
            "float": MotionType.FLOAT,
        }
        return mapping.get(value.lower(), MotionType.STATIC)

    def _str_to_prop_rot_dir(self, value: str) -> PropRotationDirection:
        """Convert string to PropRotationDirection enum."""
        mapping = {
            "cw": PropRotationDirection.CLOCKWISE,
            "ccw": PropRotationDirection.COUNTER_CLOCKWISE,
            "no_rot": PropRotationDirection.NO_ROT,
        }
        return mapping.get(value.lower(), PropRotationDirection.NO_ROT)

    def _str_to_location(self, value: str) -> Location:
        """Convert string to Location enum."""
        # Simplified location mapping
        mapping = {
            "n": Location.NORTH,
            "ne": Location.NORTHEAST,
            "e": Location.EAST,
            "se": Location.SOUTHEAST,
            "s": Location.SOUTH,
            "sw": Location.SOUTHWEST,
            "w": Location.WEST,
            "nw": Location.NORTHWEST,
        }
        return mapping.get(value.lower(), Location.NORTH)
