"""
Motion Domain Models

Immutable data structures for motion representation in TKA.
Handles prop and arrow motion data with type safety and serialization.
"""

import json
from dataclasses import dataclass, fields
from typing import Any, Dict

from ._shared_utils import process_field_value
from .enums import Location, MotionType, Orientation, RotationDirection


@dataclass(frozen=True)
class MotionData:
    """
    REPLACES: Complex motion attribute dictionaries

    Immutable motion data for props and arrows.
    Uses Orientation enum for type safety while maintaining JSON compatibility.
    """

    motion_type: MotionType
    prop_rot_dir: RotationDirection
    start_loc: Location
    end_loc: Location
    turns: float = 0.0

    # Orientation fields now use enum types
    start_ori: Orientation = Orientation.IN
    end_ori: Orientation = Orientation.IN

    def __post_init__(self):
        """Validate and convert motion data fields to proper enum types."""
        if self.turns < 0:
            raise ValueError("Turns must be non-negative")

        # Convert string values to enums if needed
        if isinstance(self.motion_type, str):
            object.__setattr__(
                self, "motion_type", self._convert_motion_type(self.motion_type)
            )

        if isinstance(self.prop_rot_dir, str):
            object.__setattr__(
                self,
                "prop_rot_dir",
                self._convert_rotation_direction(self.prop_rot_dir),
            )

        if isinstance(self.start_loc, str):
            object.__setattr__(
                self, "start_loc", self._convert_location(self.start_loc)
            )

        if isinstance(self.end_loc, str):
            object.__setattr__(self, "end_loc", self._convert_location(self.end_loc))

        if isinstance(self.start_ori, str):
            object.__setattr__(
                self, "start_ori", self._convert_orientation(self.start_ori)
            )

        if isinstance(self.end_ori, str):
            object.__setattr__(self, "end_ori", self._convert_orientation(self.end_ori))

    @staticmethod
    def _convert_orientation(value) -> Orientation:
        """Convert various orientation formats to Orientation enum."""
        if isinstance(value, Orientation):
            return value

        if isinstance(value, str):
            value_lower = value.lower()
            orientation_map = {
                "in": Orientation.IN,
                "out": Orientation.OUT,
                "clock": Orientation.CLOCK,
                "counter": Orientation.COUNTER,
            }
            return orientation_map.get(value_lower, Orientation.IN)

        if isinstance(value, (int, float)):
            # Handle legacy numeric values
            angle_map = {
                0: Orientation.IN,
                90: Orientation.CLOCK,
                180: Orientation.OUT,
                270: Orientation.COUNTER,
            }
            return angle_map.get(int(value), Orientation.IN)

        # Default fallback
        return Orientation.IN

    @staticmethod
    def _convert_motion_type(value) -> MotionType:
        """Convert string to MotionType enum."""
        if isinstance(value, MotionType):
            return value
        if isinstance(value, str):
            value_lower = value.lower()
            motion_type_map = {
                "pro": MotionType.PRO,
                "anti": MotionType.ANTI,
                "float": MotionType.FLOAT,
                "dash": MotionType.DASH,
                "static": MotionType.STATIC,
            }
            return motion_type_map.get(value_lower, MotionType.STATIC)
        return MotionType.STATIC

    @staticmethod
    def _convert_rotation_direction(value) -> RotationDirection:
        """Convert string to RotationDirection enum."""
        if isinstance(value, RotationDirection):
            return value
        if isinstance(value, str):
            value_lower = value.lower()
            rotation_map = {
                "cw": RotationDirection.CLOCKWISE,
                "ccw": RotationDirection.COUNTER_CLOCKWISE,
                "no_rot": RotationDirection.NO_ROTATION,
                "no_rotation": RotationDirection.NO_ROTATION,
            }
            return rotation_map.get(value_lower, RotationDirection.NO_ROTATION)
        return RotationDirection.NO_ROTATION

    @staticmethod
    def _convert_location(value) -> Location:
        """Convert string to Location enum."""
        if isinstance(value, Location):
            return value
        if isinstance(value, str):
            value_lower = value.lower()
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
            return location_map.get(value_lower, Location.NORTH)
        return Location.NORTH

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with snake_case keys."""
        return {
            "motion_type": (
                self.motion_type.value
                if hasattr(self.motion_type, "value")
                else self.motion_type
            ),
            "prop_rot_dir": (
                self.prop_rot_dir.value
                if hasattr(self.prop_rot_dir, "value")
                else self.prop_rot_dir
            ),
            "start_loc": (
                self.start_loc.value
                if hasattr(self.start_loc, "value")
                else self.start_loc
            ),
            "end_loc": (
                self.end_loc.value if hasattr(self.end_loc, "value") else self.end_loc
            ),
            "start_ori": (
                self.start_ori.value
                if hasattr(self.start_ori, "value")
                else self.start_ori
            ),
            "end_ori": (
                self.end_ori.value if hasattr(self.end_ori, "value") else self.end_ori
            ),
            "turns": self.turns,
        }

    def to_camel_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON APIs."""
        from ..serialization import dataclass_to_camel_dict

        return dataclass_to_camel_dict(self)

    def to_json(self, camel_case: bool = True, **kwargs) -> str:
        """Serialize to JSON string."""
        from ..serialization import domain_model_to_json

        if camel_case:
            return domain_model_to_json(self, **kwargs)
        else:
            return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MotionData":
        """Create instance from dictionary."""
        # Handle nested dataclasses and enums
        field_types = {f.name: f.type for f in fields(cls)}

        processed_data = {}
        for key, value in data.items():
            if key in field_types:
                field_type = field_types[key]
                processed_data[key] = process_field_value(value, field_type)
            else:
                processed_data[key] = value

        return cls(**processed_data)

    @classmethod
    def from_json(cls, json_str: str, camel_case: bool = True) -> "MotionData":
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        else:
            data = json.loads(json_str)
            return cls.from_dict(data)

    def update(self, **kwargs) -> "MotionData":
        """Create a new MotionData with updated fields."""
        from dataclasses import replace

        # Convert orientation fields if they're provided as strings
        if "start_ori" in kwargs:
            kwargs["start_ori"] = self._convert_orientation(kwargs["start_ori"])
        if "end_ori" in kwargs:
            kwargs["end_ori"] = self._convert_orientation(kwargs["end_ori"])

        return replace(self, **kwargs)
