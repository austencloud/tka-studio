"""
Motion Domain Models

Immutable data structures for motion representation in TKA.
Handles prop and arrow motion data with type safety and serialization.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
import json
from typing import Any

from ._shared_utils import process_field_value
from .enums import Location, MotionType, Orientation, RotationDirection


@dataclass(frozen=True)
class MotionData:
    """
    REPLACES: Complex motion attribute dictionaries

    Immutable motion data for props and arrows.
    Uses Orientation enum for type safety while maintaining JSON compatibility.
    Extended with prefloat attributes for letter determination.
    """

    motion_type: MotionType
    prop_rot_dir: RotationDirection
    start_loc: Location
    end_loc: Location
    turns: float | str = 0.0  # Can be 'fl' for float motions
    start_ori: Orientation = Orientation.IN
    end_ori: Orientation = Orientation.IN
    is_visible: bool = True

    # Prefloat attributes for letter determination
    prefloat_motion_type: MotionType | None = None
    prefloat_prop_rot_dir: RotationDirection | None = None

    def __post_init__(self):
        """Validate and convert motion data fields to proper enum types."""
        # Handle 'fl' turns for float motions
        if (
            self.turns != "fl"
            and isinstance(self.turns, (int, float))
            and self.turns < 0
        ):
            raise ValueError("Turns must be non-negative")

        # Validate prefloat attributes for float motions
        if self.motion_type == MotionType.FLOAT:
            if not self.prefloat_motion_type:
                # This is okay - prefloat attributes can be set later
                pass

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

    # Letter determination properties and methods
    @property
    def is_float(self) -> bool:
        """Check if this motion is in a float state."""
        return self.motion_type == MotionType.FLOAT

    @property
    def is_static(self) -> bool:
        """Check if this motion is static."""
        return self.motion_type == MotionType.STATIC

    @property
    def is_shift(self) -> bool:
        """Check if this motion is a shift (pro or anti)."""
        return self.motion_type in [MotionType.PRO, MotionType.ANTI]

    @property
    def effective_motion_type(self) -> MotionType:
        """Get the effective motion type, considering prefloat states."""
        if self.is_float and self.prefloat_motion_type:
            return self.prefloat_motion_type
        return self.motion_type

    @property
    def effective_prop_rot_dir(self) -> RotationDirection:
        """Get the effective prop rotation direction, considering prefloat states."""
        if self.is_float and self.prefloat_prop_rot_dir:
            return self.prefloat_prop_rot_dir
        return self.prop_rot_dir

    def to_float_state(
        self, prefloat_motion_type: MotionType, prefloat_prop_rot_dir: RotationDirection
    ) -> MotionData:
        """Convert this motion to float state with prefloat attributes."""
        return self.update(
            motion_type=MotionType.FLOAT,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            turns="fl",
            prefloat_motion_type=prefloat_motion_type,
            prefloat_prop_rot_dir=prefloat_prop_rot_dir,
        )

    def with_prefloat_attributes(
        self, motion_type: MotionType, prop_rot_dir: RotationDirection
    ) -> MotionData:
        """Create new instance with prefloat attributes."""
        return self.update(
            prefloat_motion_type=motion_type, prefloat_prop_rot_dir=prop_rot_dir
        )

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

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary with snake_case keys."""
        result = {
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

        # Add prefloat attributes if present
        if self.prefloat_motion_type:
            result["prefloat_motion_type"] = self.prefloat_motion_type.value

        if self.prefloat_prop_rot_dir:
            result["prefloat_prop_rot_dir"] = self.prefloat_prop_rot_dir.value

        return result

    def to_camel_dict(self) -> dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON APIs."""
        from ..serialization import dataclass_to_camel_dict

        return dataclass_to_camel_dict(self)

    def to_json(self, camel_case: bool = True, **kwargs) -> str:
        """Serialize to JSON string."""
        from ..serialization import domain_model_to_json

        if camel_case:
            return domain_model_to_json(self, **kwargs)
        return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MotionData:
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

        # Handle prefloat attributes conversion
        if processed_data.get("prefloat_motion_type"):
            if isinstance(processed_data["prefloat_motion_type"], str):
                processed_data["prefloat_motion_type"] = MotionType(
                    processed_data["prefloat_motion_type"]
                )

        if processed_data.get("prefloat_prop_rot_dir"):
            if isinstance(processed_data["prefloat_prop_rot_dir"], str):
                processed_data["prefloat_prop_rot_dir"] = RotationDirection(
                    processed_data["prefloat_prop_rot_dir"]
                )

        return cls(**processed_data)

    @classmethod
    def from_json(cls, json_str: str, camel_case: bool = True) -> MotionData:
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json

        if camel_case:
            return domain_model_from_json(json_str, cls)
        data = json.loads(json_str)
        return cls.from_dict(data)

    def update(self, **kwargs) -> MotionData:
        """Create a new MotionData with updated fields."""
        from dataclasses import replace

        # Convert orientation fields if they're provided as strings
        if "start_ori" in kwargs:
            kwargs["start_ori"] = self._convert_orientation(kwargs["start_ori"])
        if "end_ori" in kwargs:
            kwargs["end_ori"] = self._convert_orientation(kwargs["end_ori"])

        return replace(self, **kwargs)
