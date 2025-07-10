"""
Position Attribute Mapper

Handles mapping and conversion of position and orientation attributes between formats.
Focused solely on attribute transformation logic.
"""

import logging
from typing import Any, Union

logger = logging.getLogger(__name__)


class PositionAttributeMapper:
    """
    Maps and converts position and orientation attributes between different formats.
    
    Responsible for:
    - Converting location strings to valid enum values
    - Converting orientation values between numeric and string formats
    - Extracting position types from position strings
    - Handling legacy compatibility for attribute formats
    """

    def convert_location(self, loc_str: str) -> str:
        """
        Convert legacy location strings to valid Location enum values.
        
        Args:
            loc_str: Location string to convert
            
        Returns:
            Valid location string for enum conversion
        """
        if not loc_str:
            return "n"
            
        # Location strings are already correct: "n", "s", "e", "w", "ne", "nw", "se", "sw"
        # Do NOT convert "alpha", "beta", "gamma" - those are position TYPES, not locations
        return str(loc_str)

    def convert_orientation(self, ori_value: Union[str, int, float]) -> str:
        """
        Convert legacy orientation values to valid Orientation enum values.
        
        Args:
            ori_value: Orientation value (string or numeric)
            
        Returns:
            Valid orientation string for enum conversion
        """
        if not ori_value:
            return "in"
            
        # Orientations are stored as strings in JSON: "in", "out", "clock", "counter"
        # Only convert if we get numeric values (legacy compatibility)
        if isinstance(ori_value, (int, float)):
            ori_map = {0: "in", 90: "clock", 180: "out", 270: "counter"}
            return ori_map.get(int(ori_value), "in")
            
        return str(ori_value)

    def extract_position_type(self, position_string: str) -> str:
        """
        Extract position type (alpha, beta, gamma) from position string.
        
        Args:
            position_string: Position string like "alpha1", "beta5", "gamma11"
            
        Returns:
            Position type string ("alpha", "beta", "gamma")
        """
        if not position_string:
            return "alpha"
            
        position_string = str(position_string).lower()
        
        if position_string.startswith("alpha"):
            return "alpha"
        elif position_string.startswith("beta"):
            return "beta"
        elif position_string.startswith("gamma"):
            return "gamma"
        else:
            # Strip numeric suffix to get base position type
            return position_string.rstrip("0123456789") or "alpha"

    def convert_enum_value_to_string(self, enum_value: Any) -> str:
        """
        Convert enum value to string representation.
        
        Args:
            enum_value: Enum value or string
            
        Returns:
            String representation of the value
        """
        if hasattr(enum_value, 'value'):
            return str(enum_value.value)
        return str(enum_value) if enum_value else ""

    def convert_motion_attributes_to_legacy(self, motion_data, default_position: str = "alpha") -> dict:
        """
        Convert motion data to legacy attribute format.
        
        Args:
            motion_data: MotionData object or None
            default_position: Default position to use if motion_data is None
            
        Returns:
            Dictionary with legacy motion attributes
        """
        if not motion_data:
            return {
                "start_loc": default_position,
                "end_loc": default_position,
                "start_ori": "in",
                "end_ori": "in",
                "prop_rot_dir": "no_rot",
                "turns": 0,
                "motion_type": "static",
            }

        return {
            "start_loc": self.convert_enum_value_to_string(motion_data.start_loc),
            "end_loc": self.convert_enum_value_to_string(motion_data.end_loc),
            "start_ori": self._convert_orientation_to_legacy(motion_data.start_ori),
            "end_ori": self._convert_orientation_to_legacy(motion_data.end_ori),
            "prop_rot_dir": self.convert_enum_value_to_string(motion_data.prop_rot_dir),
            "turns": motion_data.turns if hasattr(motion_data, 'turns') else 0,
            "motion_type": self.convert_enum_value_to_string(motion_data.motion_type),
        }

    def _convert_orientation_to_legacy(self, orientation) -> str:
        """
        Convert orientation to legacy format, handling both enum and string values.
        
        Args:
            orientation: Orientation value
            
        Returns:
            Legacy orientation string
        """
        if hasattr(orientation, 'value'):
            return str(orientation.value)
        elif hasattr(orientation, '__str__'):
            return str(orientation)
        else:
            return "in"

    def create_motion_attributes_dict(
        self, 
        motion_type: str = "static",
        start_loc: str = "n",
        end_loc: str = "n", 
        start_ori: str = "in",
        end_ori: str = "in",
        prop_rot_dir: str = "no_rot",
        turns: int = 0
    ) -> dict:
        """
        Create a motion attributes dictionary with validated values.
        
        Args:
            motion_type: Motion type string
            start_loc: Start location string
            end_loc: End location string
            start_ori: Start orientation string
            end_ori: End orientation string
            prop_rot_dir: Prop rotation direction string
            turns: Number of turns
            
        Returns:
            Dictionary with motion attributes
        """
        return {
            "motion_type": str(motion_type),
            "start_loc": self.convert_location(start_loc),
            "end_loc": self.convert_location(end_loc),
            "start_ori": self.convert_orientation(start_ori),
            "end_ori": self.convert_orientation(end_ori),
            "prop_rot_dir": str(prop_rot_dir),
            "turns": int(turns) if turns else 0,
        }

    def validate_position_attributes(self, attributes: dict) -> dict:
        """
        Validate and normalize position attributes.
        
        Args:
            attributes: Dictionary of position attributes
            
        Returns:
            Dictionary with validated and normalized attributes
        """
        validated = {}
        
        # Validate and convert each attribute
        validated["motion_type"] = str(attributes.get("motion_type", "static"))
        validated["start_loc"] = self.convert_location(attributes.get("start_loc", "n"))
        validated["end_loc"] = self.convert_location(attributes.get("end_loc", "n"))
        validated["start_ori"] = self.convert_orientation(attributes.get("start_ori", "in"))
        validated["end_ori"] = self.convert_orientation(attributes.get("end_ori", "in"))
        validated["prop_rot_dir"] = str(attributes.get("prop_rot_dir", "no_rot"))
        validated["turns"] = int(attributes.get("turns", 0)) if attributes.get("turns") else 0
        
        return validated

    def get_default_attributes_for_position_type(self, position_type: str) -> dict:
        """
        Get default motion attributes for a specific position type.
        
        Args:
            position_type: Position type ("alpha", "beta", "gamma")
            
        Returns:
            Dictionary with default attributes for the position type
        """
        # Default location mapping for position types
        location_map = {
            "alpha": "n",
            "beta": "s", 
            "gamma": "e",
        }
        
        default_location = location_map.get(position_type.lower(), "n")
        
        return self.create_motion_attributes_dict(
            motion_type="static",
            start_loc=default_location,
            end_loc=default_location,
            start_ori="in",
            end_ori="in",
            prop_rot_dir="no_rot",
            turns=0
        )
