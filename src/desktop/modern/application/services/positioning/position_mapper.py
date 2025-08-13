"""
Position Matching Service - Business Logic for Position Calculations

This service contains the pure business logic for position matching and calculations,
extracted from the presentation layer. It has no PyQt6 dependencies and can be used
across different UI frameworks.

RESPONSIBILITIES:
- Position mapping and calculation logic
- End position extraction from beat data
- Motion attribute validation
- Location to position conversion

USAGE:
    service = container.resolve(IPositionMatchingService)
    end_pos = service.extract_end_position(beat_data)
    position = service.get_position_from_locations("s", "n")
"""

import logging
from typing import Any, Optional

from desktop.modern.core.interfaces.positioning_services import IPositionMapper
from desktop.modern.domain.models.beat_data import BeatData

logger = logging.getLogger(__name__)


class PositionMapper(IPositionMapper):
    """
    Business logic service for position matching and calculations.

    This service implements the core position mapping logic that was previously
    embedded in the presentation layer. It provides a clean interface for
    position calculations without any UI dependencies.
    """

    # Position mapping from (blue_end_loc, red_end_loc) to position key
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
        """Initialize the position matching service."""
        self._location_to_position_map = self.POSITIONS_MAP.copy()
        logger.debug("Position matching service initialized")

    def extract_end_position(self, last_beat: dict[str, Any]) -> Optional[str]:
        """
        Extract end position from beat data using Legacy-compatible logic.

        Args:
            last_beat: Beat data dictionary in legacy format

        Returns:
            End position string if found, None otherwise
        """
        try:
            # Check direct end_pos field
            if "end_pos" in last_beat:
                end_pos = last_beat.get("end_pos")
                if end_pos:
                    logger.debug(f"Found direct end_pos: {end_pos}")
                    return end_pos

            # Check metadata for end_pos
            if "metadata" in last_beat and "end_pos" in last_beat["metadata"]:
                end_pos = last_beat["metadata"].get("end_pos")
                if end_pos:
                    logger.debug(f"Found end_pos in metadata: {end_pos}")
                    return end_pos

            # Calculate from motion attributes if available
            if self.has_motion_attributes(last_beat):
                end_pos = self.calculate_end_position_from_motions(last_beat)
                if end_pos:
                    logger.debug(f"Calculated end_pos from motions: {end_pos}")
                    return end_pos

            # Fallback to default position
            logger.debug("No end position found, using fallback")
            return "alpha1"  # Default fallback position

        except Exception as e:
            logger.error(f"Error extracting end position: {e}")
            return None

    def calculate_end_position_from_motions(
        self, beat_data: dict[str, Any]
    ) -> Optional[str]:
        """
        Calculate end position from motion attributes.

        Args:
            beat_data: Beat data dictionary containing motion attributes

        Returns:
            Calculated position string if successful, None otherwise
        """
        try:
            blue_attrs = beat_data.get("blue_attributes", {})
            red_attrs = beat_data.get("red_attributes", {})

            blue_end_loc = blue_attrs.get("end_loc")
            red_end_loc = red_attrs.get("end_loc")

            if blue_end_loc and red_end_loc:
                position_key = (blue_end_loc, red_end_loc)
                end_position = self._location_to_position_map.get(position_key)

                if end_position:
                    logger.debug(
                        f"Calculated position {end_position} from locations {position_key}"
                    )
                    return end_position
                else:
                    logger.warning(
                        f"No position mapping found for locations {position_key}"
                    )

        except Exception as e:
            logger.error(f"Error calculating end position from motions: {e}")

        return None

    def get_position_from_locations(
        self, start_loc: str, end_loc: str
    ) -> Optional[str]:
        """
        Get position key from start and end locations.

        Args:
            start_loc: Start location string
            end_loc: End location string

        Returns:
            Position key if mapping exists, None otherwise
        """
        try:
            position_key = (start_loc, end_loc)
            position = self._location_to_position_map.get(position_key)

            if position:
                logger.debug(f"Found position {position} for locations {position_key}")
            else:
                logger.debug(f"No position mapping for locations {position_key}")

            return position

        except Exception as e:
            logger.error(f"Error getting position from locations: {e}")
            return None

    def has_motion_attributes(self, beat_data: dict[str, Any]) -> bool:
        """
        Check if beat data has motion attributes for end position calculation.

        Args:
            beat_data: Beat data dictionary to check

        Returns:
            True if motion attributes are present, False otherwise
        """
        try:
            return (
                "blue_attributes" in beat_data
                and "red_attributes" in beat_data
                and "end_loc" in beat_data["blue_attributes"]
                and "end_loc" in beat_data["red_attributes"]
            )
        except Exception as e:
            logger.error(f"Error checking motion attributes: {e}")
            return False

    def extract_modern_end_position(self, beat_data: BeatData) -> Optional[str]:
        """
        Extract end position directly from Modern BeatData.

        Args:
            beat_data: Modern BeatData object

        Returns:
            End position string if found, None otherwise
        """
        try:
            # Check metadata first
            if beat_data.metadata and "end_pos" in beat_data.metadata:
                end_pos = beat_data.metadata["end_pos"]
                logger.debug(f"Found end_pos in modern metadata: {end_pos}")
                return end_pos

            # Calculate from motion data
            if (
                beat_data.pictograph_data.motions["blue"]
                and beat_data.pictograph_data.motions["red"]
            ):
                blue_end = (
                    beat_data.pictograph_data.motions["blue"].end_loc.value
                    if beat_data.pictograph_data.motions["blue"].end_loc
                    else "s"
                )
                red_end = (
                    beat_data.pictograph_data.motions["red"].end_loc.value
                    if beat_data.pictograph_data.motions["red"].end_loc
                    else "s"
                )
                position_key = (blue_end, red_end)
                end_pos = self._location_to_position_map.get(position_key, "beta5")
                logger.debug(
                    f"Calculated modern end_pos {end_pos} from locations {position_key}"
                )
                return end_pos

            # Fallback
            logger.debug("No modern end position found, using beta5 fallback")
            return "beta5"

        except Exception as e:
            logger.error(f"Error extracting modern end position: {e}")
            return "beta5"  # Safe fallback
