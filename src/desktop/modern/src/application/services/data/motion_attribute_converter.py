"""
Motion Attribute Converter

Handles conversion of external motion attributes to modern domain model enums.
Provides centralized mapping logic for motion types, rotation directions, and locations.
"""

import logging
from typing import Any, Dict

from domain.models import (
    HandMotionType,
    Location,
    MotionData,
    MotionType,
    RotationDirection,
)

logger = logging.getLogger(__name__)


class MotionAttributeConverter:
    """
    Converts external motion attributes to modern domain model enums.
    
    Provides centralized mapping logic for:
    - Motion types (prop and hand motions)
    - Rotation directions
    - Locations
    - Orientation handling
    """

    # String to modern motion type mappings (for props)
    MOTION_TYPE_MAPPING = {
        "pro": MotionType.PRO,
        "anti": MotionType.ANTI,
        "float": MotionType.FLOAT,
        "dash": MotionType.DASH,
        "static": MotionType.STATIC,
    }

    # String to modern hand motion type mappings (for hands without props)
    HAND_MOTION_TYPE_MAPPING = {
        "shift": HandMotionType.SHIFT,
        "dash": HandMotionType.DASH,
        "static": HandMotionType.STATIC,
    }

    # String to modern rotation direction mappings
    ROTATION_DIRECTION_MAPPING = {
        "cw": RotationDirection.CLOCKWISE,
        "ccw": RotationDirection.COUNTER_CLOCKWISE,
        "no_rotation": RotationDirection.NO_ROTATION,
        "no_rot": RotationDirection.NO_ROTATION,
        "": RotationDirection.NO_ROTATION,
    }

    # String to modern location mappings
    LOCATION_MAPPING = {
        "n": Location.NORTH,
        "ne": Location.NORTHEAST,
        "e": Location.EAST,
        "se": Location.SOUTHEAST,
        "s": Location.SOUTH,
        "sw": Location.SOUTHWEST,
        "w": Location.WEST,
        "nw": Location.NORTHWEST,
    }

    def convert_motion_attributes(
        self, external_attrs: Dict[str, Any], color: str
    ) -> MotionData:
        """
        Convert external motion attributes to modern MotionData.

        Args:
            external_attrs: External motion attributes dictionary
            color: Color identifier for error reporting ("blue" or "red")

        Returns:
            MotionData object with converted attributes
        """
        try:
            # Convert motion type (handle both prop and hand motions)
            motion_type_str = str(external_attrs.get("motion_type", "static")).lower()

            # Check if it's a hand motion (shift) or prop motion
            if motion_type_str == "shift":
                # For hand motions, we'll use STATIC as the base motion type
                # The actual hand motion type can be stored in metadata if needed
                motion_type = MotionType.STATIC
            else:
                motion_type = self.MOTION_TYPE_MAPPING.get(
                    motion_type_str, MotionType.STATIC
                )

            # Convert rotation direction
            rot_dir_str = str(external_attrs.get("prop_rot_dir", "no_rotation")).lower()
            prop_rot_dir = self.ROTATION_DIRECTION_MAPPING.get(
                rot_dir_str, RotationDirection.NO_ROTATION
            )

            # Convert locations
            start_loc_str = str(external_attrs.get("start_loc", "n")).lower()
            start_loc = self.LOCATION_MAPPING.get(start_loc_str, Location.NORTH)

            end_loc_str = str(external_attrs.get("end_loc", "n")).lower()
            end_loc = self.LOCATION_MAPPING.get(end_loc_str, Location.NORTH)

            # Convert orientations to strings (MotionData will convert to enums)
            start_ori = str(external_attrs.get("start_ori", "in"))
            end_ori = str(external_attrs.get("end_ori", "in"))

            return MotionData(
                motion_type=motion_type,
                prop_rot_dir=prop_rot_dir,
                start_loc=start_loc,
                end_loc=end_loc,
                start_ori=start_ori,  # MotionData will convert string to Orientation enum
                end_ori=end_ori,  # MotionData will convert string to Orientation enum
            )

        except Exception as e:
            logger.error(
                f"Failed to convert {color} motion attributes: {e}",
                extra={"attributes": external_attrs, "color": color},
            )
            # Return default motion data on error
            return MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.NORTH,
                end_loc=Location.NORTH,
                start_ori="in",
                end_ori="in",
            )

    def get_motion_type_mapping(self) -> Dict[str, MotionType]:
        """Get the motion type mapping dictionary."""
        return self.MOTION_TYPE_MAPPING.copy()

    def get_rotation_direction_mapping(self) -> Dict[str, RotationDirection]:
        """Get the rotation direction mapping dictionary."""
        return self.ROTATION_DIRECTION_MAPPING.copy()

    def get_location_mapping(self) -> Dict[str, Location]:
        """Get the location mapping dictionary."""
        return self.LOCATION_MAPPING.copy()

    def get_hand_motion_type_mapping(self) -> Dict[str, HandMotionType]:
        """Get the hand motion type mapping dictionary."""
        return self.HAND_MOTION_TYPE_MAPPING.copy()
