"""
Default Placement Service

This service loads and uses default placement JSON files for accurate
arrow positioning with comprehensive adjustment data.
"""

import codecs
import json
from pathlib import Path
from typing import Any, Optional

# Use framework-agnostic types from desktop.modern.core.types
from desktop.modern.core.types import Point
from desktop.modern.domain.models import MotionData, MotionType


class DefaultPlacementService:
    """Service that loads default placement data and provides adjustments."""

    def __init__(self):
        self.root_path = self._find_project_root()
        self.all_defaults: dict[str, dict[str, dict[str, Any]]] = {
            "diamond": {},
            "box": {},
        }

        self.placements_files = {
            "diamond": {
                "pro": "default/default_diamond_pro_placements.json",
                "anti": "default/default_diamond_anti_placements.json",
                "float": "default/default_diamond_float_placements.json",
                "dash": "default/default_diamond_dash_placements.json",
                "static": "default/default_diamond_static_placements.json",
            },
            "box": {
                "pro": "default/default_box_pro_placements.json",
                "anti": "default/default_box_anti_placements.json",
                "float": "default/default_box_float_placements.json",
                "dash": "default/default_box_dash_placements.json",
                "static": "default/default_box_static_placements.json",
            },
        }

        self._load_all_default_placements()

    def _find_project_root(self) -> Path:
        """Automatically find the project root by looking for pyproject.toml or .git."""
        current = Path(__file__).resolve()
        for parent in [current] + list(current.parents):
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                return parent
        return current.parent  # fallback

    def _load_all_default_placements(self) -> None:
        """Load all default placement JSON files using direct path resolution."""
        for grid_mode, motion_files in self.placements_files.items():
            for motion_type, filename in motion_files.items():
                filepath = (
                    self.root_path / "data" / "arrow_placement" / grid_mode / filename
                )
                self.all_defaults[grid_mode][motion_type] = self._load_json(
                    str(filepath)
                )

    def _load_json(self, path: str) -> dict[str, Any]:
        """Load JSON file with error handling."""
        try:
            with codecs.open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading default placements from {path}: {e}")
            return {}

    def get_default_adjustment(
        self,
        motion_data: MotionData,
        grid_mode: str = "diamond",
        placement_key: Optional[str] = None,
    ) -> Point:
        """
        Get default adjustment using validated placement system.

        Args:
            motion_data: The motion data
            grid_mode: Grid mode (diamond or box)
            placement_key: Specific placement key (e.g., "pro_to_layer1_alpha")
                          If None, will use basic motion type

        Returns:
            Point with adjustment values
        """
        if grid_mode not in ["diamond", "box"]:
            grid_mode = "diamond"

        motion_type_str = motion_data.motion_type.value
        default_placements = self.all_defaults.get(grid_mode, {}).get(
            motion_type_str, {}
        )

        if not default_placements:
            return Point(0, 0)

        # If specific placement key provided, use it
        if placement_key and placement_key in default_placements:
            adjustment_key = placement_key
        else:
            # Use basic motion type as fallback
            adjustment_key = motion_type_str

        # Get the adjustment values for the specific turns
        # Convert turns to the format used in JSON files (no decimal for whole numbers)
        turns_value = motion_data.turns
        if turns_value == int(turns_value):
            turns_str = str(int(turns_value))  # "1.0" → "1"
        else:
            turns_str = str(turns_value)  # "0.5" → "0.5"

        adjustment_data = default_placements.get(adjustment_key, {})

        if isinstance(adjustment_data, dict):
            x, y = adjustment_data.get(turns_str, (0, 0))
        else:
            x, y = (0, 0)

        return Point(x, y)

    def get_available_placement_keys(
        self, motion_type: MotionType, grid_mode: str = "diamond"
    ) -> list[str]:
        """Get all available placement keys for a motion type."""
        motion_type_str = motion_type.value
        default_placements = self.all_defaults.get(grid_mode, {}).get(
            motion_type_str, {}
        )
        return list(default_placements.keys())

    def get_placement_data(
        self, motion_type: MotionType, placement_key: str, grid_mode: str = "diamond"
    ) -> dict[str, tuple[int, int]]:
        """Get complete placement data for a specific key."""
        motion_type_str = motion_type.value
        default_placements = self.all_defaults.get(grid_mode, {}).get(
            motion_type_str, {}
        )
        return default_placements.get(placement_key, {})

    def debug_available_keys(
        self, motion_type: MotionType, grid_mode: str = "diamond"
    ) -> None:
        """Debug helper to print all available placement keys."""
        keys = self.get_available_placement_keys(motion_type, grid_mode)
        print(f"Available placement keys for {motion_type.value} in {grid_mode} mode:")
        for key in keys:
            placement_data = self.get_placement_data(motion_type, key, grid_mode)
            print(f"  {key}: {placement_data}")
