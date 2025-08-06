"""
Motion Attributes Domain Model

Immutable data class representing the attributes of a motion in a pictograph.
This replaces the legacy dictionary-based motion attribute storage with a
type-safe, immutable domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..enums import Location, MotionType, Orientation, PropRotationDirection


@dataclass(frozen=True)
class MotionAttributes:
    """
    Immutable representation of motion attributes for a single prop.

    This model encapsulates all the motion data that was previously stored
    in dictionaries like blue_attributes and red_attributes in the legacy system.
    """

    motion_type: MotionType
    start_ori: Orientation
    end_ori: Orientation
    start_loc: Location
    end_loc: Location
    prop_rot_dir: PropRotationDirection
    turns: int | float | str  # Can be 'fl' for float transitions

    # Prefloat attributes for handling float state transitions
    prefloat_motion_type: Optional[MotionType] = None
    prefloat_prop_rot_dir: Optional[PropRotationDirection] = None

    def __post_init__(self):
        """Validate motion attributes after initialization."""
        # Validate that turns is a valid value
        if isinstance(self.turns, str) and self.turns != "fl":
            raise ValueError(
                f"Invalid turn value: {self.turns}. String turns must be 'fl'"
            )

        # Validate that if motion_type is FLOAT, we have prefloat attributes
        if self.motion_type == MotionType.FLOAT:
            if self.prefloat_motion_type is None:
                raise ValueError("Float motions must have prefloat_motion_type")

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
    def effective_prop_rot_dir(self) -> PropRotationDirection:
        """Get the effective prop rotation direction, considering prefloat states."""
        if self.is_float and self.prefloat_prop_rot_dir:
            return self.prefloat_prop_rot_dir
        return self.prop_rot_dir

    def with_turns(self, new_turns: int | float | str) -> MotionAttributes:
        """Create a new MotionAttributes with different turns value."""
        from dataclasses import replace

        return replace(self, turns=new_turns)

    def with_orientations(
        self, start_ori: Orientation, end_ori: Orientation
    ) -> MotionAttributes:
        """Create a new MotionAttributes with different orientations."""
        from dataclasses import replace

        return replace(self, start_ori=start_ori, end_ori=end_ori)

    def to_float_state(
        self,
        prefloat_motion_type: MotionType,
        prefloat_prop_rot_dir: PropRotationDirection,
    ) -> MotionAttributes:
        """Convert this motion to float state with prefloat attributes."""
        from dataclasses import replace

        return replace(
            self,
            motion_type=MotionType.FLOAT,
            prop_rot_dir=PropRotationDirection.NO_ROT,
            turns="fl",
            prefloat_motion_type=prefloat_motion_type,
            prefloat_prop_rot_dir=prefloat_prop_rot_dir,
        )
