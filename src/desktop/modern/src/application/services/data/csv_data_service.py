"""
CSV Data Service

Pure service for loading and processing CSV pictograph data.
Extracted from PictographManagementService to follow single responsibility principle.

PROVIDES:
- CSV file loading and parsing
- Data conversion from CSV rows to domain models
- Pandas DataFrame operations
- File I/O error handling
"""

from typing import List, Optional
from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)


class ICSVDataService(ABC):
    """Interface for CSV data operations."""

    @abstractmethod
    def load_csv_data(self, file_path: Path) -> pd.DataFrame:
        """Load CSV data from file."""

    @abstractmethod
    def convert_row_to_beat_data(self, row: pd.Series) -> BeatData:
        """Convert CSV row to BeatData."""

    @abstractmethod
    def get_pictographs_by_letter(self, letter: str) -> List[BeatData]:
        """Get all pictographs for a specific letter."""


class CSVDataService(ICSVDataService):
    def __init__(self, data_path: Optional[Path] = None):
        if data_path is None:
            # Find project root by searching for a 'data' folder upwards from this file
            current = Path(__file__).resolve().parent
            root_data = None
            for parent in [current] + list(current.parents):
                candidate = parent / "data"
                if candidate.is_dir():
                    root_data = candidate
                    break
            if root_data is None:
                raise FileNotFoundError(
                    "Could not locate 'data' directory in parent paths."
                )
            data_path = root_data / "DiamondPictographDataframe.csv"
        self._data_path = data_path
        self._csv_data: Optional[pd.DataFrame] = None

    def load_csv_data(self, file_path: Optional[Path] = None) -> pd.DataFrame:
        """Load CSV data from file."""
        path_to_use = file_path or self._data_path

        try:
            return pd.read_csv(path_to_use)
        except Exception as e:
            print(f"Error reading CSV file {path_to_use}: {e}")
            return pd.DataFrame()  # Return empty DataFrame on error

    def convert_row_to_beat_data(self, row: pd.Series) -> BeatData:
        """Convert a CSV row to BeatData object."""
        # Map CSV values to enums
        motion_type_map = {
            "pro": MotionType.PRO,
            "anti": MotionType.ANTI,
            "static": MotionType.STATIC,
            "dash": MotionType.DASH,
            "float": MotionType.FLOAT,
        }
        rotation_map = {
            "cw": RotationDirection.CLOCKWISE,
            "ccw": RotationDirection.COUNTER_CLOCKWISE,
            "no_rot": RotationDirection.NO_ROTATION,
        }
        location_map = {
            "n": Location.NORTH,
            "e": Location.EAST,
            "s": Location.SOUTH,
            "w": Location.WEST,
            "ne": Location.NORTHEAST,
            "se": Location.SOUTHEAST,
            "sw": Location.SOUTHWEST,
            "nw": Location.NORTHWEST,
        }

        # Create motion data if motion type exists
        blue_motion = None
        if row.get("blue_motion_type") in motion_type_map:
            blue_motion = MotionData(
                motion_type=motion_type_map[row["blue_motion_type"]],
                prop_rot_dir=rotation_map.get(
                    row.get("blue_prop_rot_dir"), RotationDirection.CLOCKWISE
                ),
                start_loc=location_map[row["blue_start_loc"]],
                end_loc=location_map[row["blue_end_loc"]],
            )

        red_motion = None
        if row.get("red_motion_type") in motion_type_map:
            red_motion = MotionData(
                motion_type=motion_type_map[row["red_motion_type"]],
                prop_rot_dir=rotation_map.get(
                    row.get("red_prop_rot_dir"), RotationDirection.CLOCKWISE
                ),
                start_loc=location_map[row["red_start_loc"]],
                end_loc=location_map[row["red_end_loc"]],
            )

        # Create beat data
        return BeatData(
            beat_number=row.get("beat_number", 1),
            letter=row.get("letter"),
            blue_motion=blue_motion,
            red_motion=red_motion,
        )

    def get_pictographs_by_letter(self, letter: str) -> List[BeatData]:
        """Get all pictographs for a specific letter."""
        df = self._load_cached_data()
        letter_data = df[df["letter"] == letter]

        return [self.convert_row_to_beat_data(row) for _, row in letter_data.iterrows()]

    def get_specific_pictograph(
        self, letter: str, index: int = 0
    ) -> Optional[BeatData]:
        """Get a specific pictograph by letter and index."""
        df = self._load_cached_data()

        # Filter by letter
        letter_data = df[df["letter"] == letter]

        if letter_data.empty or index >= len(letter_data):
            return None

        row = letter_data.iloc[index]
        return self.convert_row_to_beat_data(row)

    def get_start_position_pictograph(
        self, position_key: str, grid_mode: str = "diamond"
    ) -> Optional[BeatData]:
        """Get start position pictograph by position key and grid mode."""
        # Map position keys to letters
        position_to_letter = {
            "alpha1_alpha1": "A",
            "beta5_beta5": "B",
            "gamma11_gamma11": "C",
            "alpha2_alpha2": "A",
            "beta4_beta4": "B",
            "gamma12_gamma12": "C",
        }

        letter = position_to_letter.get(position_key)
        if not letter:
            return None  # Silent return for invalid position keys

        # Get the first pictograph for this letter
        pictographs = self.get_pictographs_by_letter(letter)
        if pictographs:
            return pictographs[0]
        else:
            print(f"⚠️ No pictographs found for letter: {letter}")
            return None

    def _load_cached_data(self) -> pd.DataFrame:
        """Load CSV data with caching."""
        if self._csv_data is None:
            self._csv_data = self.load_csv_data()
        return self._csv_data

    def clear_cache(self) -> None:
        """Clear cached CSV data."""
        self._csv_data = None
