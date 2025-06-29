"""
Position Matcher - Position Matching Logic
Split from beat_data_loader.py - contains position matching and calculation logic
"""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from application.services.positioning.arrows.utilities.position_matching_service import (
        PositionMatchingService,
    )
    from domain.models.core_models import BeatData


class PositionMatcher:
    """Handles position matching logic and calculations."""

    POSITIONS_MAP = {
        ("s", "n"): "alpha1",
        ("sw", "ne"): "alpha2",
        ("w", "e"): "alpha3",
        ("nw", "se"): "alpha4",
        ("n", "s"): "alpha5",
        ("ne", "sw"): "alpha6",
        ("e", "w"): "alpha7",
        ("se", "nw"): "alpha8",
        ("n", "n"): "beta1",
        ("ne", "ne"): "beta2",
        ("e", "e"): "beta3",
        ("se", "se"): "beta4",
        ("s", "s"): "beta5",
        ("sw", "sw"): "beta6",
        ("w", "w"): "beta7",
        ("nw", "nw"): "beta8",
        ("w", "n"): "gamma1",
        ("nw", "ne"): "gamma2",
        ("n", "e"): "gamma3",
        ("ne", "se"): "gamma4",
        ("e", "s"): "gamma5",
        ("se", "sw"): "gamma6",
        ("s", "w"): "gamma7",
        ("sw", "nw"): "gamma8",
        ("e", "n"): "gamma9",
        ("se", "ne"): "gamma10",
        ("s", "e"): "gamma11",
        ("sw", "se"): "gamma12",
        ("w", "s"): "gamma13",
        ("nw", "sw"): "gamma14",
        ("n", "w"): "gamma15",
        ("ne", "nw"): "gamma16",
    }

    def __init__(self):
        self._location_to_position_map = self.POSITIONS_MAP.copy()

    def extract_end_position(
        self, last_beat: Dict[str, Any], position_service: "PositionMatchingService"
    ) -> Optional[str]:
        """Extract end position from last beat data using Legacy-compatible logic."""
        if "end_pos" in last_beat:
            return last_beat.get("end_pos")

        if "metadata" in last_beat and "end_pos" in last_beat["metadata"]:
            return last_beat["metadata"].get("end_pos")

        if self._has_motion_attributes(last_beat):
            end_pos = self._calculate_end_position_from_motions(last_beat)
            if end_pos:
                return end_pos

        try:
            available_positions = position_service.get_available_start_positions()
            if available_positions:
                return available_positions[0]
            else:
                alpha1_options = position_service.get_alpha1_options()
                return "alpha1" if alpha1_options else None
        except Exception:
            return None

    def extract_modern_end_position(self, beat_data: "BeatData") -> Optional[str]:
        """Extract end position directly from Modern BeatData."""
        if beat_data.metadata and "end_pos" in beat_data.metadata:
            return beat_data.metadata["end_pos"]

        if beat_data.blue_motion and beat_data.red_motion:
            blue_end = (
                beat_data.blue_motion.end_loc.value
                if beat_data.blue_motion.end_loc
                else "s"
            )
            red_end = (
                beat_data.red_motion.end_loc.value
                if beat_data.red_motion.end_loc
                else "s"
            )
            position_key = (blue_end, red_end)
            end_pos = self._location_to_position_map.get(position_key, "beta5")
            return end_pos

        return "beta5"

    def _has_motion_attributes(self, beat_data: Dict[str, Any]) -> bool:
        """Check if beat data has motion attributes for end position calculation."""
        return (
            "blue_attributes" in beat_data
            and "red_attributes" in beat_data
            and "end_loc" in beat_data["blue_attributes"]
            and "end_loc" in beat_data["red_attributes"]
        )

    def _calculate_end_position_from_motions(self, beat_data: Dict[str, Any]) -> Optional[str]:
        """Calculate end position from motion data using positions mapping."""
        try:
            blue_attrs = beat_data.get("blue_attributes", {})
            red_attrs = beat_data.get("red_attributes", {})

            blue_end_loc = blue_attrs.get("end_loc")
            red_end_loc = red_attrs.get("end_loc")

            if blue_end_loc and red_end_loc:
                position_key = (blue_end_loc, red_end_loc)
                end_position = self._location_to_position_map.get(position_key)
                return end_position if end_position else None
        except Exception:
            pass

        return None
